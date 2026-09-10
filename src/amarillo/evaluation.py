from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path
from typing import Any

from .io import ensure_dir, read_json, write_json


def evaluate_output_manifest(manifest_path: Path, output_path: Path, sample_count: int = 5) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    rows = []
    for output in manifest.get("outputs", []):
        output_path_value = output.get("output_path")
        if not output_path_value or not Path(output_path_value).exists():
            continue
        if Path(output_path_value).suffix.lower() not in {".mp4", ".mov", ".webm", ".mkv"}:
            continue
        rows.append(evaluate_video(Path(output_path_value), output, sample_count))
    document = {
        "evaluated_count": len(rows),
        "evaluations": rows,
        "warnings": collect_warnings(rows),
    }
    write_json(output_path, document)
    write_markdown(output_path.with_suffix(".md"), document)
    latest = output_path.parent / "latest.json"
    write_json(latest, document)
    write_markdown(output_path.parent / "latest.md", document)
    return document


def evaluate_video(path: Path, output: dict[str, Any], sample_count: int) -> dict[str, Any]:
    probe = probe_video(path)
    frames = sample_frames(path, probe["duration_seconds"], sample_count)
    metrics = frame_metrics(frames)
    return {
        "id": output.get("run_id") or output.get("output_id"),
        "type": output.get("type"),
        "model_or_tool": output.get("model_id") or output.get("tool"),
        "variant_id": output.get("variant_id"),
        "output_path": str(path),
        "duration_seconds": probe["duration_seconds"],
        "width": probe["width"],
        "height": probe["height"],
        "fps": probe["fps"],
        "sampled_frames": len(frames),
        "avg_luminance": metrics["avg_luminance"],
        "avg_contrast": metrics["avg_contrast"],
        "avg_motion_delta": metrics["avg_motion_delta"],
        "blank_risk": blank_risk(metrics),
        "technical_score": technical_score(probe, metrics),
    }


def probe_video(path: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)
    stream = data["streams"][0]
    return {
        "duration_seconds": round(float(data["format"]["duration"]), 3),
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "fps": parse_fps(stream.get("r_frame_rate", "0/1")),
    }


def parse_fps(value: str) -> float:
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        denominator_value = float(denominator)
        if denominator_value == 0:
            return 0.0
        return round(float(numerator) / denominator_value, 3)
    return round(float(value), 3)


def sample_frames(path: Path, duration_seconds: float, sample_count: int) -> list[bytes]:
    if duration_seconds <= 0 or sample_count <= 0:
        return []
    times = [
        duration_seconds * ((index + 1) / (sample_count + 1))
        for index in range(sample_count)
    ]
    return [extract_ppm_frame(path, timestamp) for timestamp in times]


def extract_ppm_frame(path: Path, timestamp: float) -> bytes:
    completed = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-vf",
            "scale=160:-1",
            "-f",
            "image2pipe",
            "-vcodec",
            "ppm",
            "-",
        ],
        check=True,
        capture_output=True,
    )
    return completed.stdout


def frame_metrics(frames: list[bytes]) -> dict[str, float]:
    luminance_values = [decode_luminance(frame) for frame in frames]
    flat_values = [value for frame in luminance_values for value in frame]
    avg_luminance = mean(flat_values)
    avg_contrast = pstdev(flat_values)
    deltas = [
        mean(abs(a - b) for a, b in zip(previous, current))
        for previous, current in zip(luminance_values, luminance_values[1:])
        if previous and current
    ]
    return {
        "avg_luminance": round(avg_luminance, 2),
        "avg_contrast": round(avg_contrast, 2),
        "avg_motion_delta": round(mean(deltas), 2),
    }


def decode_luminance(ppm: bytes) -> list[float]:
    header_end = ppm.find(b"\n255\n")
    if header_end == -1:
        return []
    header = ppm[:header_end].decode("ascii", errors="ignore").split()
    if len(header) < 3 or header[0] != "P6":
        return []
    rgb = ppm[header_end + len(b"\n255\n") :]
    values = []
    for index in range(0, len(rgb) - 2, 3):
        r, g, b = rgb[index], rgb[index + 1], rgb[index + 2]
        values.append((0.2126 * r) + (0.7152 * g) + (0.0722 * b))
    return values


def mean(values: list[float] | Any) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)


def pstdev(values: list[float]) -> float:
    if not values:
        return 0.0
    avg = mean(values)
    return math.sqrt(sum((value - avg) ** 2 for value in values) / len(values))


def blank_risk(metrics: dict[str, float]) -> str:
    luminance = metrics["avg_luminance"]
    contrast = metrics["avg_contrast"]
    if luminance < 8 or luminance > 247 or contrast < 5:
        return "high"
    if luminance < 18 or luminance > 237 or contrast < 12:
        return "medium"
    return "low"


def technical_score(probe: dict[str, Any], metrics: dict[str, float]) -> int:
    score = 100
    if probe["width"] < 1280 or probe["height"] < 720:
        score -= 15
    if probe["duration_seconds"] < 4:
        score -= 10
    if blank_risk(metrics) == "medium":
        score -= 15
    if blank_risk(metrics) == "high":
        score -= 35
    if metrics["avg_motion_delta"] < 1:
        score -= 10
    return max(score, 0)


def collect_warnings(rows: list[dict[str, Any]]) -> list[str]:
    warnings = []
    for row in rows:
        if row["blank_risk"] != "low":
            warnings.append(f"{row['id']} has {row['blank_risk']} blank-frame risk")
        if row["width"] < 1280 or row["height"] < 720:
            warnings.append(f"{row['id']} is below 720p")
    return warnings


def write_markdown(path: Path, document: dict[str, Any]) -> None:
    lines = [
        "# Technical Evaluation",
        "",
        f"- Evaluated outputs: {document['evaluated_count']}",
        f"- Warnings: {len(document['warnings'])}",
        "",
        "| Output | Model/Tool | Resolution | Duration | Luma | Contrast | Motion | Blank Risk | Tech Score |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: |",
    ]
    for row in document["evaluations"]:
        lines.append(
            f"| `{row['id']}` | `{row['model_or_tool']}` | {row['width']}x{row['height']} | "
            f"{row['duration_seconds']} | {row['avg_luminance']} | {row['avg_contrast']} | "
            f"{row['avg_motion_delta']} | {row['blank_risk']} | {row['technical_score']} |"
        )
    if document["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in document["warnings"])
    ensure_dir(path.parent)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
