from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from .briefing import compose_brief_plan
from .evaluation import evaluate_output_manifest
from .fal_runner import run_plan as execute_run_plan
from .io import ensure_dir, read_json
from .knowledge import build_knowledge_base
from .media import ingest_samples
from .outputs import build_output_manifest
from .pipeline import refresh_artifacts
from .planning import build_run_plan
from .prompts import analyze_samples, build_prompt_library
from .reference_compare import compare_reference_outputs
from .reports import write_report
from .review_pack import build_review_pack
from .scoring import score_results
from .selector import build_recommendations


ROOT = Path.cwd()
DEFAULTS_PATH = ROOT / "configs" / "project_defaults.json"


def defaults() -> dict:
    return read_json(DEFAULTS_PATH)


def main() -> None:
    parser = argparse.ArgumentParser(prog="amarillo")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    ingest = sub.add_parser("ingest")
    ingest.add_argument("--samples", default=None)
    analyze = sub.add_parser("analyze")
    analyze.add_argument("--artifacts", default=None)
    build = sub.add_parser("build-prompts")
    build.add_argument("--artifacts", default=None)
    build.add_argument("--library", default=None)
    plan = sub.add_parser("plan-runs")
    plan.add_argument("--max-estimated-cost", type=float, default=None)
    plan.add_argument("--include-research-only", action="store_true")
    plan.add_argument("--include-variants", action="store_true")
    plan.add_argument("--variant-id", action="append", default=None)
    plan.add_argument("--max-runs", type=int, default=None)
    run = sub.add_parser("run-fal")
    run.add_argument("--run-plan", default="artifacts/run_plans/latest.json")
    run.add_argument("--results", default=None)
    run.add_argument("--live", action="store_true")
    run.add_argument("--rerun-completed", action="store_true")
    run.add_argument("--max-estimated-cost", type=float, default=None)
    score = sub.add_parser("score")
    score.add_argument("--results", default="artifacts/results/latest.jsonl")
    recommend = sub.add_parser("recommend")
    recommend.add_argument("--scoreboard", default="artifacts/scoreboards/latest.json")
    compose = sub.add_parser("compose-brief")
    compose.add_argument("--brief", required=True)
    outputs = sub.add_parser("catalog-outputs")
    outputs.add_argument("--results", default="artifacts/results/latest.jsonl")
    evaluate = sub.add_parser("evaluate-outputs")
    evaluate.add_argument("--manifest", default="artifacts/output_manifest/latest.json")
    evaluate.add_argument("--sample-count", type=int, default=5)
    compare = sub.add_parser("compare-reference")
    compare.add_argument("--sample-count", type=int, default=5)
    sub.add_parser("build-review-pack")
    sub.add_parser("build-knowledge")
    refresh = sub.add_parser("refresh-artifacts")
    refresh.add_argument("--sample-count", type=int, default=5)
    report = sub.add_parser("report")
    args = parser.parse_args()
    config = defaults()
    if args.command == "init":
        command_init(config)
    elif args.command == "ingest":
        command_ingest(config, args)
    elif args.command == "analyze":
        artifacts = Path(args.artifacts or config["artifacts_dir"])
        analyses = analyze_samples(artifacts)
        print(f"Analyzed {len(analyses)} sample(s).")
    elif args.command == "build-prompts":
        artifacts = Path(args.artifacts or config["artifacts_dir"])
        library = Path(args.library or config["prompt_library_dir"])
        patterns = build_prompt_library(artifacts, library)
        print(f"Built {len(patterns)} prompt pattern(s).")
    elif args.command == "plan-runs":
        max_cost = args.max_estimated_cost or config["budget"]["default_max_estimated_cost_usd"]
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = Path(config["artifacts_dir"]) / "run_plans" / f"{stamp}.json"
        plan_doc = build_run_plan(
            Path(config["prompt_library_dir"]) / "patterns.json",
            ROOT / "catalog" / "fal_video_models.json",
            path,
            max_cost,
            args.include_research_only,
            args.include_variants,
            args.variant_id,
            args.max_runs,
        )
        print(f"Planned {plan_doc['run_count']} run(s), estimated ${plan_doc['total_estimated_cost_usd']:.2f}.")
    elif args.command == "run-fal":
        max_cost = args.max_estimated_cost or config["budget"]["default_max_estimated_cost_usd"]
        results_path = Path(args.results or "artifacts/results/latest.jsonl")
        records = execute_run_plan(
            Path(args.run_plan),
            results_path,
            live=args.live,
            max_estimated_cost=max_cost,
            skip_completed=not args.rerun_completed,
        )
        print(f"Logged {len(records)} result record(s) to {results_path}.")
    elif args.command == "score":
        scored = score_results(Path(args.results), Path("artifacts/scoreboards/latest.json"))
        print(f"Scored {len(scored)} run(s).")
    elif args.command == "recommend":
        recommendations = build_recommendations(
            Path(args.scoreboard),
            Path("artifacts/recommendations/latest.json"),
        )
        print(f"Built {len(recommendations['recommendations'])} recommendation group(s).")
    elif args.command == "compose-brief":
        plan = compose_brief_plan(
            args.brief,
            Path("prompt_library/patterns.json"),
            Path("artifacts/recommendations/latest.json"),
            Path("artifacts/brief_plans/latest.json"),
        )
        print(f"Selected {plan['selected_variant_id']} with {plan['recommended_model']}.")
    elif args.command == "catalog-outputs":
        manifest = build_output_manifest(
            Path(args.results),
            Path("artifacts/scoreboards/latest.json"),
            Path("assembled_outputs"),
            Path("artifacts/output_manifest/latest.json"),
        )
        print(
            f"Cataloged {manifest['generated_count']} generated output(s) "
            f"and {manifest['assembled_count']} assembled output(s)."
        )
    elif args.command == "evaluate-outputs":
        document = evaluate_output_manifest(
            Path(args.manifest),
            Path("artifacts/evaluations/latest.json"),
            args.sample_count,
        )
        print(f"Evaluated {document['evaluated_count']} output video(s).")
    elif args.command == "compare-reference":
        document = compare_reference_outputs(
            Path("artifacts/samples/manifest.json"),
            Path("artifacts/output_manifest/latest.json"),
            Path("artifacts/evaluations/latest.json"),
            Path("artifacts/reference_comparisons/latest.json"),
            args.sample_count,
        )
        print(f"Compared {document['comparison_count']} output video(s) to the reference sample.")
    elif args.command == "build-review-pack":
        document = build_review_pack(
            Path("artifacts/output_manifest/latest.json"),
            Path("artifacts/recommendations/latest.json"),
            Path("artifacts/evaluations/latest.json"),
            Path("artifacts/reference_comparisons/latest.json"),
            Path("artifacts/review_pack/latest.json"),
        )
        print(f"Built review pack with {document['entry_count']} video(s).")
    elif args.command == "build-knowledge":
        document = build_knowledge_base(Path("artifacts/knowledge/latest.json"))
        print(
            f"Built knowledge base with {len(document['prompt_patterns'])} pattern(s), "
            f"{len(document['scoreboard'])} scored run(s), and "
            f"{len(document['outputs'].get('outputs', []))} output(s)."
        )
    elif args.command == "refresh-artifacts":
        summary = refresh_artifacts(args.sample_count)
        print(
            "Refreshed artifacts: "
            f"{summary['scored_runs']} scored run(s), "
            f"{summary['recommendation_groups']} recommendation group(s), "
            f"{summary['indexed_outputs']} indexed output(s), "
            f"{summary['evaluated_outputs']} evaluated output(s), "
            f"{summary['reference_comparisons']} reference comparison(s), "
            f"{summary['review_pack_entries']} review-pack entry(s)."
        )
    elif args.command == "report":
        body = write_report(
            Path("artifacts/reports/latest.md"),
            Path("artifacts/samples/manifest.json"),
            Path("prompt_library/patterns.json"),
            Path("artifacts/run_plans/latest.json"),
            Path("artifacts/results/latest.jsonl"),
            Path("artifacts/scoreboards/latest.json"),
        )
        print(body)


def command_init(config: dict) -> None:
    paths = [
        Path(config["samples_dir"]),
        Path(config["artifacts_dir"]) / "samples",
        Path(config["artifacts_dir"]) / "analysis",
        Path(config["artifacts_dir"]) / "run_plans",
        Path(config["artifacts_dir"]) / "results",
        Path(config["artifacts_dir"]) / "scoreboards",
        Path(config["artifacts_dir"]) / "reports",
        Path(config["prompt_library_dir"]),
    ]
    for path in paths:
        ensure_dir(path)
    print("Initialized Amarillo workspace directories.")


def command_ingest(config: dict, args: argparse.Namespace) -> None:
    samples = Path(args.samples or config["samples_dir"])
    analysis_config = config["analysis"]
    manifest = ingest_samples(
        samples,
        Path(config["artifacts_dir"]),
        int(analysis_config["keyframe_interval_seconds"]),
        int(analysis_config["max_keyframes_per_video"]),
    )
    print(f"Ingested {len(manifest)} video sample(s).")


if __name__ == "__main__":
    main()
