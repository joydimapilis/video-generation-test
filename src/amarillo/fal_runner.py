from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any
from decimal import Decimal, ROUND_CEILING
import hashlib
import json

from urllib.request import urlretrieve

from .io import append_jsonl, ensure_dir, read_json, read_jsonl, write_json
from .references import resolve_local_images
from .budget import BudgetLedger


def money_cents(value):
    if isinstance(value, bool):
        raise ValueError('Invalid cost')
    amount = Decimal(str(value))
    if not amount.is_finite() or amount <= 0:
        raise ValueError('Cost must be positive and finite')
    return int((amount * 100).to_integral_value(rounding=ROUND_CEILING))


def run_plan(
    run_plan_path: Path,
    results_path: Path,
    live: bool,
    max_estimated_cost: float,
    skip_completed: bool = True,
) -> list[dict[str, Any]]:
    plan = read_json(run_plan_path)
    limit = money_cents(max_estimated_cost)
    if Decimal(str(max_estimated_cost)) > 10:
        raise ValueError('The maximum live experiment cap is $10')
    total = sum(money_cents(r['estimated_cost_usd']) for r in plan.get('runs', [])) / 100
    if total > max_estimated_cost:
        raise SystemExit(
            f"Run plan estimates ${total:.2f}, above allowed ${max_estimated_cost:.2f}."
        )
    records: list[dict[str, Any]] = []
    completed_run_ids = existing_completed_run_ids(results_path) if skip_completed else set()
    ledger = None
    historical_ids = set()
    if live:
        ledger = BudgetLedger(results_path.with_suffix('.budget.json'), limit)
        # Import historical attempts individually, including failures. This is
        # idempotent even if interrupted halfway through migration.
        for index, old in enumerate(read_jsonl(results_path)):
            if old.get('status') == 'dry_run':
                continue
            token = hashlib.sha256(json.dumps(old, sort_keys=True).encode()).hexdigest()
            run_id = old.get('run_id')
            historical_ids.add(run_id)
            # Current calls already have reservations; do not charge them twice.
            if run_id in ledger.read()['runs']:
                continue
            ledger.reserve(f'historical-{index}-{token}', money_cents(old['estimated_cost_usd']), old)
    for run in plan.get("runs", []):
        if run["run_id"] in completed_run_ids:
            continue
        if live and run['run_id'] in historical_ids and run['run_id'] not in ledger.read()['runs']:
            # Imported history has no recoverable queue ID. A failed/unknown old
            # call is still a paid attempt, never an implicit retry.
            continue
        if ledger is not None and not ledger.reserve(run['run_id'], money_cents(run['estimated_cost_usd']), run):
            continue
        record = run_one(run, live=live)
        if ledger is not None:
            ledger.update(run['run_id'], status=record['status'])
        append_jsonl(results_path, record)
        records.append(record)
    write_json(results_path.with_suffix(".summary.json"), summarize(read_jsonl(results_path)))
    return records


def run_one(run: dict[str, Any], live: bool) -> dict[str, Any]:
    started = datetime.now(timezone.utc).isoformat()
    if not live:
        return {
            "run_id": run["run_id"],
            "pattern_id": run.get("pattern_id"),
            "variant_id": run.get("variant_id"),
            "model_id": run["model_id"],
            "endpoint": run["endpoint"],
            "status": "dry_run",
            "estimated_cost_usd": run["estimated_cost_usd"],
            "input": run["input"],
            "started_at": started,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "result": None,
        }
    try:
        import fal_client  # type: ignore
    except ImportError:
        return failure_record(run, started, "Install fal support with: python3 -m pip install -e '.[fal]'")
    try:
        input_payload = resolve_local_images(run["input"], fal_client.upload_file)
    except Exception as exc:
        return failure_record(run, started, f"Image reference resolution failed: {exc}")
    upload_error = fill_uploaded_image_url(input_payload, fal_client)
    if upload_error:
        return failure_record(run, started, upload_error)
    missing = [
        key
        for key in run.get("required_inputs", [])
        if input_payload.get(key) in (None, "", "REQUIRED_IMAGE_URL")
    ]
    if missing:
        return failure_record(run, started, f"Missing required live inputs: {', '.join(missing)}")
    input_payload.pop("image_path", None)
    timer = perf_counter()
    try:
        result = fal_client.subscribe(
            run["endpoint"],
            input_payload,
            with_logs=True,
            interval=5,
            client_timeout=900,
        )
    except Exception as exc:  # Fal errors should be preserved in the experiment log.
        return failure_record(run, started, f"{type(exc).__name__}: {exc}")
    output_path = download_video_result(result, run["run_id"])
    return {
        "run_id": run["run_id"],
        "pattern_id": run.get("pattern_id"),
        "variant_id": run.get("variant_id"),
        "model_id": run["model_id"],
        "endpoint": run["endpoint"],
        "status": "completed",
        "estimated_cost_usd": run["estimated_cost_usd"],
        "latency_seconds": round(perf_counter() - timer, 3),
        "input": input_payload,
        "started_at": started,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "output_path": output_path,
        "result": result,
    }


def fill_uploaded_image_url(input_payload: dict[str, Any], fal_client: Any) -> str | None:
    image_field = next((key for key in ("image_url", "start_image_url")
                        if input_payload.get(key) == "REQUIRED_IMAGE_URL"), None)
    if image_field is None:
        return None
    image_path = input_payload.get("image_path")
    if not image_path:
        return None
    path = Path(image_path)
    if not path.exists():
        return f"Local image_path does not exist: {image_path}"
    try:
        input_payload[image_field] = fal_client.upload_file(path)
    except Exception as exc:
        return f"Fal image upload failed: {type(exc).__name__}: {exc}"
    return None


def failure_record(run: dict[str, Any], started: str, message: str) -> dict[str, Any]:
    return {
        "run_id": run["run_id"],
        "pattern_id": run.get("pattern_id"),
        "variant_id": run.get("variant_id"),
        "model_id": run["model_id"],
        "endpoint": run["endpoint"],
        "status": "failed",
        "estimated_cost_usd": run["estimated_cost_usd"],
        "input": run["input"],
        "started_at": started,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "error": message,
    }


def existing_completed_run_ids(results_path: Path) -> set[str]:
    return {
        record["run_id"]
        for record in read_jsonl(results_path)
        if record.get("status") == "completed"
    }


def download_video_result(result: dict[str, Any], run_id: str) -> str | None:
    url = find_video_url(result)
    if not url:
        return None
    suffix = Path(url.split("?")[0]).suffix or ".mp4"
    output_path = ensure_dir(Path("artifacts/outputs")) / f"{run_id}{suffix}"
    try:
        urlretrieve(url, output_path)
    except Exception:
        return None
    return str(output_path)


def find_video_url(value: Any) -> str | None:
    if isinstance(value, str) and value.startswith("http") and any(
        ext in value.split("?")[0].lower() for ext in [".mp4", ".mov", ".webm"]
    ):
        return value
    if isinstance(value, dict):
        for key in ["url", "video_url"]:
            found = find_video_url(value.get(key))
            if found:
                return found
        for child in value.values():
            found = find_video_url(child)
            if found:
                return found
    if isinstance(value, list):
        for child in value:
            found = find_video_url(child)
            if found:
                return found
    return None


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "record_count": len(records),
        "completed": sum(1 for record in records if record["status"] == "completed"),
        "dry_run": sum(1 for record in records if record["status"] == "dry_run"),
        "failed": sum(1 for record in records if record["status"] == "failed"),
        "estimated_cost_usd": round(sum(float(record.get("estimated_cost_usd", 0)) for record in records), 4),
    }
