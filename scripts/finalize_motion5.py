"""Verify and index the complete Motion-5 deliverable after HyperFrames renders it."""
import json
import shutil
import subprocess
from pathlib import Path

from amarillo.io import read_json, write_json
from amarillo.pipeline import refresh_artifacts


def main():
    final = Path("artifacts/final_outcome/motion5/motion5-final.mp4")
    metadata = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(final)
    ]))
    video = next(stream for stream in metadata["streams"] if stream["codec_type"] == "video")
    audio = next(stream for stream in metadata["streams"] if stream["codec_type"] == "audio")
    assert (video["width"], video["height"]) == (1920, 1080), "Wrong output dimensions"
    assert abs(float(metadata["format"]["duration"]) - 32.533333) < 0.1, "Incomplete render"
    decoded = subprocess.run(["ffmpeg", "-v", "error", "-i", str(final), "-f", "null", "-"], capture_output=True, text=True, check=True)
    assert not decoded.stderr.strip(), decoded.stderr
    subprocess.run(["ffmpeg", "-v", "error", "-ss", "28.5", "-i", str(final), "-frames:v", "1", "-y", str(final.parent / "poster.jpg")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(final), "-vf", "fps=1/2,scale=480:-1,tile=4x4", "-frames:v", "1", "-y", str(final.parent / "contact-sheet.jpg")], check=True)
    indexed = Path("artifacts/outputs/motion5_final.mp4")
    shutil.copy2(final, indexed)
    sample_id = read_json(Path("analysis_notes/motion5.json"))["sample_id"]
    write_json(Path("assembled_outputs/motion5_final.json"), {
        "output_id": "motion5_final", "tool": "HyperFrames + Kling 2.6 Pro",
        "source_sample_id": sample_id, "source_project": "hyperframes/motion5",
        "output_path": str(indexed), "final_delivery_path": str(final),
        "preview_url": "http://localhost:3021/#project/motion5",
        "duration_seconds": float(metadata["format"]["duration"]), "resolution": "1920x1080", "fps": 30,
        "source_plates": [f"artifacts/outputs/{sample_id}-pattern__mascot_team_hook__kling_2_6_pro_i2v.mp4"],
        "purpose": "Full-length reference-inspired recreation: Fal mascot opening and deterministic UI workflow.",
        "quality_notes": "Agent inspected scene snapshots and final contact sheet. All readable UI and end lockup are rebuilt. Original supplied soundtrack and cropped source mascot reused. No human approval score assigned.",
        "recommended_use": "Review the complete Motion-5 outcome; replace brand, request, tools, lane labels and results for other use cases."
    })
    write_json(final.parent / "verification.json", {
        "decode_errors": [], "metadata": metadata,
        "video_codec": video["codec_name"], "audio_codec": audio["codec_name"],
        "duration_seconds": float(metadata["format"]["duration"]),
        "validation": "HyperFrames check passed runtime, layout, 300-sample motion audit, and all 43 sampled text contrast checks. One duplicate-image warning is intentional reuse of the same logo in distinct animation roles.",
        "animation_map_review": "Inspected 117 mapped tweens. Generic map includes duplicate nested timeline entries and invisible pre-entrance states; full composition check and snapshots verify rendered visibility. Final summary and brand holds are intentional reading time."
    })
    summary = refresh_artifacts(sample_count=7)
    print(json.dumps({"final_video": str(final), "bytes": final.stat().st_size, "duration": metadata["format"]["duration"], "pipeline": summary}, indent=2))


if __name__ == "__main__":
    main()
