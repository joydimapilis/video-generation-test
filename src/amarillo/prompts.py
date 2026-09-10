from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io import ensure_dir, read_json, write_json


def analyze_samples(artifacts_dir: Path) -> list[dict[str, Any]]:
    manifest_path = artifacts_dir / "samples" / "manifest.json"
    manifest = read_json(manifest_path) if manifest_path.exists() else []
    notes = load_analysis_notes(Path("analysis_notes"))
    analyses = [build_analysis(record, notes.get(record["sample_id"])) for record in manifest]
    write_json(artifacts_dir / "analysis" / "sample_analyses.json", analyses)
    return analyses


def load_analysis_notes(notes_dir: Path) -> dict[str, dict[str, Any]]:
    if not notes_dir.exists():
        return {}
    notes: dict[str, dict[str, Any]] = {}
    for path in sorted(notes_dir.glob("*.json")):
        row = read_json(path)
        sample_id = row.get("sample_id")
        if sample_id:
            notes[sample_id] = row
    return notes


def build_analysis(sample: dict[str, Any], notes: dict[str, Any] | None = None) -> dict[str, Any]:
    if notes:
        return build_analysis_from_notes(sample, notes)
    metadata = sample.get("metadata", {})
    aspect = metadata.get("aspect_ratio", "9:16")
    duration = metadata.get("duration_seconds", 5)
    has_audio = metadata.get("has_audio", False)
    filename = Path(sample.get("source_path", "sample")).stem.replace("_", " ")
    tags = infer_tags(filename, aspect, has_audio)
    return {
        "sample_id": sample["sample_id"],
        "source_path": sample["source_path"],
        "observed_facts": {
            "filename_hint": filename,
            "duration_seconds": duration,
            "aspect_ratio": aspect,
            "has_audio": has_audio,
            "keyframe_count": len(sample.get("keyframes", [])),
        },
        "reusable_pattern": {
            "pattern_name": title_from_tags(tags),
            "shot_family": tags["shot_family"],
            "recommended_mode": tags["recommended_mode"],
            "structure": [
                "Establish the subject immediately",
                "Use one clear camera move or transformation",
                "Keep the motion readable within a 5-6 second clip",
                "End on a stable frame that can cut cleanly into the next asset",
            ],
            "style_axes": tags["style_axes"],
            "prompt_slots": ["subject", "setting", "primary_action", "camera_move", "lighting", "mood"],
            "negative_constraints": [
                "no warped anatomy",
                "no unreadable text",
                "no abrupt identity changes",
                "no random extra objects",
            ],
        },
        "analysis_status": "heuristic_initial_pass",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def build_analysis_from_notes(sample: dict[str, Any], notes: dict[str, Any]) -> dict[str, Any]:
    metadata = sample.get("metadata", {})
    reusable = notes["reusable_pattern"]
    facts = notes.get("sample_specific_facts", {})
    return {
        "sample_id": sample["sample_id"],
        "source_path": sample["source_path"],
        "observed_facts": {
            "duration_seconds": metadata.get("duration_seconds", 5),
            "aspect_ratio": metadata.get("aspect_ratio", facts.get("orientation", "9:16")),
            "has_audio": metadata.get("has_audio", False),
            "keyframe_count": len(sample.get("keyframes", [])),
            "visible_brand_or_product": facts.get("visible_brand_or_product"),
            "visible_moments": facts.get("visible_moments", []),
            "dominant_colors": facts.get("dominant_colors", []),
        },
        "reusable_pattern": {
            "pattern_name": reusable["pattern_name"],
            "shot_family": reusable["shot_family"],
            "recommended_mode": reusable["recommended_mode"],
            "secondary_tools": reusable.get("secondary_tools", []),
            "structure": reusable["structure"],
            "style_axes": reusable["style_axes"],
            "camera_and_motion": reusable.get("camera_and_motion", []),
            "prompt_slots": ["subject", "setting", "primary_action", "camera_move", "lighting", "mood"],
            "negative_constraints": reusable["negative_constraints"],
        },
        "prompt_defaults": notes.get("prompt_defaults", {}),
        "prompt_variants": notes.get("prompt_variants"),
        "analysis_status": notes.get("inspection_method", "manual_notes"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def infer_tags(filename: str, aspect: str, has_audio: bool) -> dict[str, Any]:
    lowered = filename.lower()
    style_axes = ["clean commercial polish", "controlled subject motion"]
    shot_family = "short-form social clip" if aspect == "9:16" else "cinematic marketing clip"
    recommended_mode = "text-to-video"
    if any(word in lowered for word in ["product", "pack", "bottle", "shoe", "watch"]):
        shot_family = "product hero motion"
        recommended_mode = "image-to-video"
        style_axes.append("product fidelity")
    if any(word in lowered for word in ["transition", "cut", "swipe", "match"]):
        shot_family = "transition pattern"
        style_axes.append("edit-driven motion")
    if has_audio:
        style_axes.append("audio-aware pacing")
    return {
        "shot_family": shot_family,
        "recommended_mode": recommended_mode,
        "style_axes": style_axes,
    }


def title_from_tags(tags: dict[str, Any]) -> str:
    return tags["shot_family"].replace("-", " ").title()


def build_prompt_library(artifacts_dir: Path, prompt_library_dir: Path) -> list[dict[str, Any]]:
    analyses_path = artifacts_dir / "analysis" / "sample_analyses.json"
    analyses = read_json(analyses_path) if analyses_path.exists() else []
    patterns = [pattern_from_analysis(analysis) for analysis in analyses]
    ensure_dir(prompt_library_dir)
    write_json(prompt_library_dir / "patterns.json", patterns)
    return patterns


def pattern_from_analysis(analysis: dict[str, Any]) -> dict[str, Any]:
    pattern = analysis["reusable_pattern"]
    sample_id = analysis["sample_id"]
    pattern_id = f"{sample_id}-pattern"
    structure = "; ".join(pattern.get("structure", []))
    style_axes = ", ".join(pattern.get("style_axes", []))
    camera_notes = "; ".join(pattern.get("camera_and_motion", []))
    negatives = ", ".join(pattern.get("negative_constraints", []))
    prompt = (
        "Create a {duration_seconds}-second {aspect_ratio} commercial video of {subject} in {setting}. "
        "{primary_action}. Camera and edit language: {camera_move}. Lighting: {lighting}. Mood: {mood}. "
        f"Reusable structure: {structure}. Style axes: {style_axes}. Camera references: {camera_notes}. "
        f"Avoid: {negatives}."
    )
    defaults = {
        "duration_seconds": 5,
        "aspect_ratio": analysis["observed_facts"].get("aspect_ratio", "9:16"),
        "subject": "the chosen product or main subject",
        "setting": "a visually simple setting that supports the use case",
        "primary_action": "the subject performs one clear motion or transformation",
        "camera_move": "slow push-in with stable framing",
        "lighting": "soft directional light with controlled highlights",
        "mood": "polished, modern, commercially useful",
    }
    defaults.update(analysis.get("prompt_defaults", {}))
    return {
        "pattern_id": pattern_id,
        "source_sample_id": sample_id,
        "pattern_name": pattern["pattern_name"],
        "shot_family": pattern["shot_family"],
        "recommended_mode": pattern["recommended_mode"],
        "style_axes": pattern["style_axes"],
        "prompt_template": prompt,
        "prompt_variants": analysis.get("prompt_variants") or build_prompt_variants(pattern, defaults),
        "default_slots": defaults,
        "model_notes": {
            "text-to-video": "Use when the subject can be invented from the brief.",
            "image-to-video": "Use when product, character, or brand consistency matters.",
            "hyperframes": "Use for deterministic typography, overlays, captions, edits, and final assembly.",
        },
        "status": "draft_from_heuristic_analysis",
    }


def build_prompt_variants(pattern: dict[str, Any], defaults: dict[str, Any]) -> list[dict[str, Any]]:
    family = pattern["shot_family"]
    if family != "product app reward montage":
        return [{
            "variant_id": "reference_structure",
            "purpose": "Explore the observed reference structure without importing another sample's scenes.",
            "best_for": [pattern.get("recommended_mode", "text-to-video")],
            "prompt": (
                f"Create a {defaults['duration_seconds']}-second {defaults['aspect_ratio']} {family} "
                f"of {defaults['subject']} in {defaults['setting']}. {defaults['primary_action']}. "
                f"Sequence: {'; '.join(pattern.get('structure', []))}. "
                f"Camera: {defaults['camera_move']}. Lighting: {defaults['lighting']}. "
                f"Mood: {defaults['mood']}. Avoid: {', '.join(pattern.get('negative_constraints', []))}."
            ),
        }]
    return [
        {
            "variant_id": "full_montage",
            "purpose": "Recreate the reusable multi-beat structure from the reference.",
            "best_for": ["premium text-to-video", "first-pass model comparison"],
            "prompt": (
                f"Create a 5-second 16:9 {family} commercial for {defaults['subject']}. "
                f"Show a fast readable sequence: physical launch in the real world, phone reward proof, "
                f"checkout interaction, clean product insert, floating reward burst, final app proof. "
                f"Use {defaults['lighting']}. Mood: {defaults['mood']}. Keep UI text minimal and legible."
            ),
        },
        {
            "variant_id": "single_shot_launch",
            "purpose": "Isolate the strongest visual hook as one controllable shot.",
            "best_for": ["image-to-video", "product fidelity tests", "opening shot generation"],
            "prompt": (
                f"Animate {defaults['subject']} launching upward between tall city buildings, "
                "leaving subtle neon-lime reward particles behind it. Keep the camera looking upward, "
                "the product centered, and the movement smooth enough to become an opening shot."
            ),
        },
        {
            "variant_id": "checkout_proof",
            "purpose": "Turn the abstract reward idea into grounded product proof.",
            "best_for": ["image-to-video", "retail proof shots", "commercial cutaways"],
            "prompt": (
                "Create a close retail checkout shot where a hand presents a smartphone with a clean "
                "mobile rewards screen beside a payment terminal. The interaction should feel practical, "
                "trustworthy, and commercially polished. Avoid unreadable UI text and distorted phone edges."
            ),
        },
        {
            "variant_id": "hyperframes_overlay_plan",
            "purpose": "Deterministic final assembly guidance rather than a generative-video prompt.",
            "best_for": ["HyperFrames", "controlled typography", "app UI replacement", "score counters"],
            "prompt": (
                "Use generated footage only for background/action plates. Replace app screens, progress "
                "numbers, reward claims, and end cards with deterministic HTML/CSS overlays rendered in "
                "HyperFrames so the final ad has legible text and repeatable brand/UI control."
            ),
        },
    ]
