from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io import read_json, write_json
from .models import VideoModel, load_models


def render_prompt(pattern: dict[str, Any], overrides: dict[str, Any] | None = None) -> str:
    slots = dict(pattern.get("default_slots", {}))
    if overrides:
        slots.update(overrides)
    return pattern["prompt_template"].format(**slots)


def build_run_plan(
    prompt_library_path: Path,
    model_catalog_path: Path,
    output_path: Path,
    max_estimated_cost: float,
    include_research_only: bool = False,
    include_variants: bool = False,
    variant_ids: list[str] | None = None,
    max_runs: int | None = None,
) -> dict[str, Any]:
    patterns = read_json(prompt_library_path) if prompt_library_path.exists() else []
    sample_manifest_path = Path("artifacts/samples/manifest.json")
    sample_manifest = read_json(sample_manifest_path) if sample_manifest_path.exists() else []
    models = load_models(model_catalog_path)
    runs: list[dict[str, Any]] = []
    spent = 0.0
    for pattern in patterns:
        for prompt_unit in prompt_units(pattern, include_variants, variant_ids):
            candidates = select_candidates(prompt_unit, models, include_research_only)
            for model in candidates:
                if max_runs is not None and len(runs) >= max_runs:
                    break
                if spent + model.estimated_cost_usd > max_estimated_cost:
                    continue
                run_id = f"{prompt_unit['unit_id']}__{model.id}"
                prompt = prompt_unit["prompt"]
                input_context = dict(pattern)
                if "preferred_keyframe_index" in prompt_unit:
                    input_context["preferred_keyframe_index"] = prompt_unit["preferred_keyframe_index"]
                runs.append(
                    {
                        "run_id": run_id,
                        "pattern_id": pattern["pattern_id"],
                        "variant_id": prompt_unit.get("variant_id"),
                        "model_id": model.id,
                        "endpoint": model.endpoint,
                        "mode": model.mode,
                        "estimated_cost_usd": model.estimated_cost_usd,
                        "prompt": prompt,
                        "required_inputs": model.required_inputs,
                        "input": build_input(model, prompt, input_context, sample_manifest),
                        "status": "planned",
                    }
                )
                spent += model.estimated_cost_usd
            if max_runs is not None and len(runs) >= max_runs:
                break
        if max_runs is not None and len(runs) >= max_runs:
            break
    plan = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "max_estimated_cost_usd": max_estimated_cost,
        "total_estimated_cost_usd": round(spent, 4),
        "run_count": len(runs),
        "runs": runs,
    }
    write_json(output_path, plan)
    latest_path = output_path.parent / "latest.json"
    write_json(latest_path, plan)
    return plan


def prompt_units(
    pattern: dict[str, Any],
    include_variants: bool,
    variant_ids: list[str] | None = None,
) -> list[dict[str, Any]]:
    if not include_variants:
        return [
            {
                "unit_id": pattern["pattern_id"],
                "prompt": render_prompt(pattern),
                "recommended_mode": pattern.get("recommended_mode"),
            }
        ]
    allowed = set(variant_ids or [])
    units: list[dict[str, Any]] = []
    for variant in pattern.get("prompt_variants", []):
        variant_id = variant["variant_id"]
        if allowed and variant_id not in allowed:
            continue
        if "hyperframes" in variant_id:
            continue
        units.append(
            {
                "unit_id": f"{pattern['pattern_id']}__{variant_id}",
                "variant_id": variant_id,
                "prompt": variant["prompt"],
                "recommended_mode": infer_variant_mode(variant, pattern.get("recommended_mode")),
                "preferred_keyframe_index": preferred_keyframe_index(variant_id),
            }
        )
    return units


def preferred_keyframe_index(variant_id: str) -> int:
    if variant_id == "checkout_proof":
        return 2
    return 0


def infer_variant_mode(variant: dict[str, Any], fallback: str | None) -> str | None:
    best_for = " ".join(variant.get("best_for", [])).lower()
    if "image-to-video" in best_for:
        return "image-to-video"
    if "text-to-video" in best_for:
        return "text-to-video"
    return fallback


def select_candidates(
    pattern: dict[str, Any],
    models: list[VideoModel],
    include_research_only: bool,
) -> list[VideoModel]:
    preferred = pattern.get("recommended_mode")
    ranked = sorted(models, key=lambda model: model.estimated_cost_usd)
    allowed = [
        model
        for model in ranked
        if include_research_only or model.license != "research-only"
    ]
    exact = [model for model in allowed if model.mode == preferred]
    exploratory = [model for model in allowed if model.mode == "text-to-video"]
    merged: list[VideoModel] = []
    for model in exact + exploratory + allowed:
        if model not in merged:
            merged.append(model)
    if preferred in {"image-to-video", "text-to-video"}:
        return merged[:2]
    return merged[:3]


def build_input(
    model: VideoModel,
    prompt: str,
    pattern: dict[str, Any] | None = None,
    sample_manifest: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    payload = dict(model.default_input)
    default_slots = pattern.get("default_slots", {}) if pattern else {}
    if "aspect_ratio" in payload and default_slots.get("aspect_ratio"):
        payload["aspect_ratio"] = default_slots["aspect_ratio"]
    if "prompt" in model.required_inputs:
        payload["prompt"] = prompt
    if "subject" in model.required_inputs:
        payload.setdefault("subject", "main subject")
    if "image_url" in model.required_inputs:
        payload.setdefault("image_url", "REQUIRED_IMAGE_URL")
        image_path = first_keyframe_for_pattern(pattern, sample_manifest)
        if image_path:
            payload["image_path"] = image_path
    return payload


def first_keyframe_for_pattern(
    pattern: dict[str, Any] | None,
    sample_manifest: list[dict[str, Any]] | None,
) -> str | None:
    if not pattern or not sample_manifest:
        return None
    sample_id = pattern.get("source_sample_id")
    for sample in sample_manifest:
        if sample.get("sample_id") == sample_id and sample.get("keyframes"):
            index = int(pattern.get("preferred_keyframe_index", 0))
            keyframes = sample["keyframes"]
            return keyframes[min(index, len(keyframes) - 1)]
    return None
