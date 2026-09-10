from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from .io import ensure_dir, write_json

VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"}


def stable_id(path: Path) -> str:
    digest = hashlib.sha1(str(path.resolve()).encode("utf-8")).hexdigest()[:10]
    return f"{path.stem.lower().replace(' ', '-')}-{digest}"


def discover_videos(samples_dir: Path) -> list[Path]:
    if not samples_dir.exists():
        return []
    return sorted(
        path
        for path in samples_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
    )


def ffprobe(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


def summarize_probe(probe: dict[str, Any]) -> dict[str, Any]:
    video_stream = next(
        (stream for stream in probe.get("streams", []) if stream.get("codec_type") == "video"),
        {},
    )
    audio_stream = next(
        (stream for stream in probe.get("streams", []) if stream.get("codec_type") == "audio"),
        {},
    )
    duration = float(probe.get("format", {}).get("duration") or video_stream.get("duration") or 0)
    width = int(video_stream.get("width") or 0)
    height = int(video_stream.get("height") or 0)
    return {
        "duration_seconds": round(duration, 3),
        "width": width,
        "height": height,
        "aspect_ratio": aspect_ratio(width, height),
        "fps": video_stream.get("r_frame_rate"),
        "video_codec": video_stream.get("codec_name"),
        "has_audio": bool(audio_stream),
        "audio_codec": audio_stream.get("codec_name"),
    }


def aspect_ratio(width: int, height: int) -> str:
    if not width or not height:
        return "unknown"
    ratio = width / height
    if ratio > 1.6:
        return "16:9"
    if ratio < 0.75:
        return "9:16"
    return "1:1"


def extract_keyframes(
    video_path: Path,
    output_dir: Path,
    interval_seconds: int = 2,
    max_keyframes: int = 8,
) -> list[Path]:
    ensure_dir(output_dir)
    pattern = output_dir / "frame_%03d.jpg"
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(video_path),
        "-vf",
        f"fps=1/{interval_seconds},scale='min(960,iw)':-2",
        "-frames:v",
        str(max_keyframes),
        str(pattern),
    ]
    subprocess.run(command, check=True)
    return sorted(output_dir.glob("frame_*.jpg"))


def ingest_samples(
    samples_dir: Path,
    artifacts_dir: Path,
    interval_seconds: int,
    max_keyframes: int,
) -> list[dict[str, Any]]:
    manifest: list[dict[str, Any]] = []
    for video in discover_videos(samples_dir):
        sample_id = stable_id(video)
        sample_dir = artifacts_dir / "samples" / sample_id
        probe = ffprobe(video)
        metadata = summarize_probe(probe)
        frames = extract_keyframes(video, sample_dir / "keyframes", interval_seconds, max_keyframes)
        record = {
            "sample_id": sample_id,
            "source_path": str(video),
            "metadata": metadata,
            "keyframes": [str(path) for path in frames],
        }
        write_json(sample_dir / "metadata.json", {"probe": probe, "summary": metadata})
        manifest.append(record)
    write_json(artifacts_dir / "samples" / "manifest.json", manifest)
    return manifest
