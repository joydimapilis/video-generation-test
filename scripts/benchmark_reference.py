"""Compare a chosen reference hook through Fal using the shared run logger."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from amarillo.fal_runner import existing_completed_run_ids, run_one
from amarillo.io import append_jsonl, read_json, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--notes", type=Path, required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    args = parser.parse_args()
    notes = read_json(args.notes)
    variant = next(row for row in notes["prompt_variants"] if row["variant_id"] == args.variant)
    if not args.image.is_file():
        parser.error("Reference image is missing")
    pattern_id = notes["sample_id"] + "-pattern"
    models = [
        ("kling_2_6_pro_i2v", "fal-ai/kling-video/v2.6/pro/image-to-video", 0.35,
         {"duration": "5", "generate_audio": False, "start_image_url": "REQUIRED_IMAGE_URL", "image_path": str(args.image)}),
        ("wan_2_1_t2v", "fal-ai/wan-t2v", 0.20,
         {"resolution": "480p", "aspect_ratio": "16:9", "enable_prompt_expansion": False}),
    ]
    runs = [{"run_id": f"{pattern_id}__{args.variant}__{model}", "pattern_id": pattern_id,
             "variant_id": args.variant, "model_id": model, "endpoint": endpoint,
             "estimated_cost_usd": cost, "required_inputs": ["prompt"],
             "input": {"prompt": variant["prompt"], **payload}}
            for model, endpoint, cost, payload in models]
    write_json(args.artifacts / "run_plan.json", {
        "runs": runs, "run_count": len(runs), "total_estimated_cost_usd": 0.55,
        "cost_note": "Existing catalog estimate; actual invoice not queried. One attempt per model, no automatic retry.",
        "comparison_note": "Practical workflow comparison: Kling receives a reference image; WAN receives text only."
    })
    results = Path("artifacts/results/latest.jsonl")
    completed = existing_completed_run_ids(results)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run_one, run, True) for run in runs if run["run_id"] not in completed]
        for future in as_completed(futures):
            record = future.result()
            append_jsonl(results, record)
            append_jsonl(args.artifacts / "results.jsonl", record)
            print(record["model_id"], record["status"], record.get("output_path") or record.get("error"), flush=True)


if __name__ == "__main__":
    main()
