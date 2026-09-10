from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import ensure_dir, read_json, write_json


def compose_brief_plan(
    brief: str,
    prompt_library_path: Path,
    recommendations_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    patterns = read_json(prompt_library_path) if prompt_library_path.exists() else []
    recommendations = read_json(recommendations_path) if recommendations_path.exists() else {"recommendations": []}
    variant_id = choose_variant(brief)
    pattern = patterns[0] if patterns else {}
    variant = find_variant(pattern, variant_id)
    rec = find_recommendation(recommendations, variant_id) or find_recommendation(recommendations, "primary_full_prompt")
    prompt = variant.get("prompt") or pattern.get("prompt_template", "")
    plan = {
        "brief": brief,
        "selected_pattern_id": pattern.get("pattern_id"),
        "selected_variant_id": variant_id,
        "recommended_model": rec.get("recommended_model") if rec else None,
        "recommended_endpoint": rec.get("recommended_endpoint") if rec else None,
        "selection_reason": rec.get("evidence") if rec else "No scored recommendation available yet.",
        "prompt": prompt,
        "tool_chain": tool_chain_for_variant(variant_id),
        "human_review_focus": review_focus_for_variant(variant_id),
    }
    write_json(output_path, plan)
    write_markdown(output_path.with_suffix(".md"), plan)
    latest = output_path.parent / "latest.json"
    write_json(latest, plan)
    write_markdown(output_path.parent / "latest.md", plan)
    return plan


def choose_variant(brief: str) -> str:
    lowered = brief.lower()
    if any(word in lowered for word in ["checkout", "payment", "pay", "retail", "proof", "terminal"]):
        return "checkout_proof"
    if any(word in lowered for word in ["launch", "opening", "hook", "sky", "city"]):
        return "single_shot_launch"
    if any(word in lowered for word in ["montage", "ad", "campaign", "sequence", "commercial"]):
        return "primary_full_prompt"
    return "primary_full_prompt"


def find_variant(pattern: dict[str, Any], variant_id: str) -> dict[str, Any]:
    for variant in pattern.get("prompt_variants", []):
        if variant.get("variant_id") == variant_id:
            return variant
    return {}


def find_recommendation(recommendations: dict[str, Any], shot_type: str) -> dict[str, Any] | None:
    for rec in recommendations.get("recommendations", []):
        if rec.get("shot_type") == shot_type:
            return rec
    return None


def tool_chain_for_variant(variant_id: str) -> list[str]:
    if variant_id in {"checkout_proof", "single_shot_launch"}:
        return ["Fal image-to-video", "HyperFrames overlay/assembly"]
    return ["Fal text-to-video", "HyperFrames overlay/assembly"]


def review_focus_for_variant(variant_id: str) -> list[str]:
    if variant_id == "checkout_proof":
        return ["phone-screen legibility", "payment interaction clarity", "hand/phone geometry", "overlay placement"]
    if variant_id == "single_shot_launch":
        return ["product stability", "particle motion", "city perspective", "opening-hook readability"]
    return ["beat coverage", "subject identity", "UI/text replacement needs", "commercial usefulness"]


def write_markdown(path: Path, plan: dict[str, Any]) -> None:
    lines = [
        "# Brief Plan",
        "",
        f"Brief: {plan['brief']}",
        "",
        f"- Pattern: `{plan.get('selected_pattern_id')}`",
        f"- Variant: `{plan.get('selected_variant_id')}`",
        f"- Model: `{plan.get('recommended_model')}`",
        f"- Endpoint: `{plan.get('recommended_endpoint')}`",
        f"- Tool chain: {', '.join(plan['tool_chain'])}",
        f"- Reason: {plan['selection_reason']}",
        "",
        "## Prompt",
        "",
        plan["prompt"],
        "",
        "## Review Focus",
        "",
    ]
    lines.extend(f"- {item}" for item in plan["human_review_focus"])
    ensure_dir(path.parent)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
