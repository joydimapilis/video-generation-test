"""Run the two bounded Motion-5 hook experiments, preserving completed results."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from amarillo.fal_runner import existing_completed_run_ids, run_one
from amarillo.io import append_jsonl, read_json, write_json


def main():
    notes = read_json(Path("analysis_notes/motion5.json"))
    prompt = notes["prompt_variants"][0]["prompt"]
    pattern_id = notes["sample_id"] + "-pattern"
    variants = [
        ("kling_2_6_pro_i2v", "fal-ai/kling-video/v2.6/pro/image-to-video", 0.35,
         {"duration": "5", "generate_audio": False,
          "start_image_url": "REQUIRED_IMAGE_URL", "image_path": "artifacts/motion5/reference/hero.png"}),
        ("wan_2_1_t2v", "fal-ai/wan-t2v", 0.20,
         {"resolution": "480p", "aspect_ratio": "16:9", "enable_prompt_expansion": False}),
    ]
    runs = [{"run_id": f"{pattern_id}__mascot_team_hook__{model}",
             "pattern_id": pattern_id, "variant_id": "mascot_team_hook", "model_id": model,
             "endpoint": endpoint, "estimated_cost_usd": cost,
             "required_inputs": ["prompt"], "input": {"prompt": prompt, **payload}}
            for model, endpoint, cost, payload in variants]
    write_json(Path("artifacts/motion5/run_plan.json"), {
        "runs": runs, "run_count": len(runs), "total_estimated_cost_usd": 0.55,
        "cost_note": "Catalog estimates, not a provider invoice; one 5s run per model, no automatic retries.",
        "schema_sources": ["https://fal.ai/models/fal-ai/kling-video/v2.6/pro/image-to-video/api",
                           "https://fal.ai/models/fal-ai/wan-t2v/api"]})
    results = Path("artifacts/results/latest.jsonl")
    completed = existing_completed_run_ids(results)
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending = {pool.submit(run_one, run, True): run for run in runs if run["run_id"] not in completed}
        for future in as_completed(pending):
            record = future.result()
            append_jsonl(results, record)
            append_jsonl(Path("artifacts/motion5/results.jsonl"), record)
            print(record["model_id"], record["status"], record.get("output_path") or record.get("error"), flush=True)


if __name__ == "__main__":
    main()
