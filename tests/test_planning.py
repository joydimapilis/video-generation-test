from __future__ import annotations

import unittest
from pathlib import Path

from amarillo.briefing import choose_variant
from amarillo.evaluation import blank_risk, decode_luminance, parse_fps, technical_score
from amarillo.knowledge import load_optional_json
from amarillo.models import VideoModel
from amarillo.outputs import inferred_output_path, remote_video_url
from amarillo.pipeline import refresh_artifacts
from amarillo.planning import build_input, prompt_units, render_prompt, select_candidates
from amarillo.reference_compare import aspect_ratio, normalized_delta, production_alignment_score, visual_similarity_score
from amarillo.review_pack import best_cheap_output, suggested_decision
from amarillo.scoring import infer_variant_id, score_record
from amarillo.selector import recommendation_for_group


class PlanningTests(unittest.TestCase):
    def test_render_prompt_uses_pattern_slots(self) -> None:
        pattern = {
            "prompt_template": "Make {subject} in {setting}.",
            "default_slots": {"subject": "a shoe", "setting": "a studio"},
        }
        self.assertEqual(render_prompt(pattern), "Make a shoe in a studio.")
        self.assertEqual(render_prompt(pattern, {"subject": "a bottle"}), "Make a bottle in a studio.")

    def test_select_candidates_prefers_mode_and_excludes_research(self) -> None:
        models = [
            make_model("cheap_research", "image-to-video", "research-only", 0.01),
            make_model("i2v", "image-to-video", "commercial", 0.35),
            make_model("t2v", "text-to-video", "commercial", 0.20),
        ]
        selected = select_candidates({"recommended_mode": "image-to-video"}, models, include_research_only=False)
        self.assertEqual([model.id for model in selected][:2], ["i2v", "t2v"])

    def test_build_input_marks_missing_image_url(self) -> None:
        model = make_model("i2v", "image-to-video", "commercial", 0.35)
        model = VideoModel(
            **{**model.__dict__, "required_inputs": ["prompt", "image_url"], "default_input": {}}
        )
        payload = build_input(model, "Prompt")
        self.assertEqual(payload["prompt"], "Prompt")
        self.assertEqual(payload["image_url"], "REQUIRED_IMAGE_URL")

    def test_build_input_adds_sample_keyframe_path(self) -> None:
        model = make_model("i2v", "image-to-video", "commercial", 0.35)
        model = VideoModel(
            **{**model.__dict__, "required_inputs": ["prompt", "image_url"], "default_input": {}}
        )
        payload = build_input(
            model,
            "Prompt",
            {"source_sample_id": "sample-1"},
            [{"sample_id": "sample-1", "keyframes": ["artifacts/samples/sample-1/keyframes/frame_001.jpg"]}],
        )
        self.assertEqual(payload["image_path"], "artifacts/samples/sample-1/keyframes/frame_001.jpg")

    def test_build_input_uses_pattern_aspect_ratio_when_supported(self) -> None:
        model = make_model("t2v", "text-to-video", "commercial", 0.20)
        model = VideoModel(
            **{**model.__dict__, "default_input": {"aspect_ratio": "9:16"}}
        )
        payload = build_input(
            model,
            "Prompt",
            {"default_slots": {"aspect_ratio": "16:9"}},
            [],
        )
        self.assertEqual(payload["aspect_ratio"], "16:9")

    def test_score_record_merges_review_score(self) -> None:
        row = score_record(
            {
                "run_id": "run-1",
                "model_id": "model",
                "endpoint": "endpoint",
                "status": "completed",
                "estimated_cost_usd": 0.2,
            },
            {
                "prompt_adherence": 8,
                "temporal_coherence": 8,
                "motion_quality": 8,
                "subject_fidelity": 8,
                "artifact_control": 8,
                "commercial_usefulness": 8,
                "pattern_reusability": 8,
                "notes": "good",
            },
        )
        self.assertEqual(row["quality_score"], 80.0)
        self.assertIn("score_final", row)

    def test_prompt_units_can_use_variants(self) -> None:
        pattern = {
            "pattern_id": "pattern",
            "recommended_mode": "text-to-video",
            "prompt_template": "Primary {subject}",
            "default_slots": {"subject": "subject"},
            "prompt_variants": [
                {
                    "variant_id": "single_shot_launch",
                    "prompt": "Launch",
                    "best_for": ["image-to-video"],
                },
                {
                    "variant_id": "hyperframes_overlay_plan",
                    "prompt": "Overlay",
                    "best_for": ["HyperFrames"],
                },
            ],
        }
        units = prompt_units(pattern, include_variants=True)
        self.assertEqual(len(units), 1)
        self.assertEqual(units[0]["recommended_mode"], "image-to-video")

    def test_recommendation_picks_highest_final_score(self) -> None:
        rec = recommendation_for_group(
            "checkout_proof",
            [
                {"model_id": "wan", "endpoint": "a", "score_final": 60},
                {"model_id": "kling", "endpoint": "b", "score_final": 82},
            ],
        )
        self.assertEqual(rec["recommended_model"], "kling")

    def test_infer_variant_id_from_legacy_run_id(self) -> None:
        self.assertEqual(
            infer_variant_id("pattern__checkout_proof__wan_2_1_t2v"),
            "checkout_proof",
        )
        self.assertIsNone(infer_variant_id("pattern__wan_2_1_t2v"))

    def test_choose_variant_from_brief(self) -> None:
        self.assertEqual(choose_variant("make a checkout payment proof shot"), "checkout_proof")
        self.assertEqual(choose_variant("make an opening city launch hook"), "single_shot_launch")
        self.assertEqual(choose_variant("make a full campaign ad"), "primary_full_prompt")

    def test_remote_video_url_finds_nested_url(self) -> None:
        self.assertEqual(
            remote_video_url({"video": {"url": "https://example.com/out.mp4"}}),
            "https://example.com/out.mp4",
        )

    def test_inferred_output_path_returns_none_for_missing_file(self) -> None:
        self.assertIsNone(inferred_output_path("missing-run"))

    def test_parse_fps_fraction(self) -> None:
        self.assertEqual(parse_fps("30000/1001"), 29.97)

    def test_decode_luminance_reads_ppm_pixels(self) -> None:
        values = decode_luminance(b"P6\n1 1\n255\n\xff\x00\x00")
        self.assertEqual(round(values[0], 2), 54.21)

    def test_blank_risk_thresholds(self) -> None:
        self.assertEqual(blank_risk({"avg_luminance": 120, "avg_contrast": 30}), "low")
        self.assertEqual(blank_risk({"avg_luminance": 2, "avg_contrast": 30}), "high")

    def test_technical_score_penalizes_low_resolution(self) -> None:
        score = technical_score(
            {"width": 832, "height": 480, "duration_seconds": 5},
            {"avg_luminance": 120, "avg_contrast": 30, "avg_motion_delta": 4},
        )
        self.assertEqual(score, 85)

    def test_load_optional_json_uses_fallback_for_missing_file(self) -> None:
        self.assertEqual(load_optional_json(Path("missing.json"), {"ok": True}), {"ok": True})

    def test_refresh_artifacts_is_callable(self) -> None:
        self.assertTrue(callable(refresh_artifacts))

    def test_reference_compare_scores_identical_metrics_high(self) -> None:
        reference = {"avg_luminance": 90, "avg_contrast": 60, "avg_motion_delta": 30}
        self.assertEqual(visual_similarity_score(reference, reference), 100.0)
        self.assertEqual(normalized_delta(0, 50, 100), 0.5)

    def test_production_alignment_penalizes_low_resolution(self) -> None:
        reference = {"width": 1920, "height": 1080, "duration_seconds": 30, "aspect_ratio": "16:9"}
        evaluation = {"width": 832, "height": 480, "duration_seconds": 5}
        self.assertEqual(aspect_ratio(1920, 1080), "16:9")
        self.assertEqual(production_alignment_score(reference, evaluation), 57.0)

    def test_review_pack_selects_best_cheap_unselected_output(self) -> None:
        outputs = [
            {"type": "fal_generation", "run_id": "selected", "estimated_cost_usd": 0.2, "score_final": 90},
            {"type": "fal_generation", "run_id": "cheap-a", "estimated_cost_usd": 0.2, "score_final": 60},
            {"type": "fal_generation", "run_id": "cheap-b", "estimated_cost_usd": 0.2, "score_final": 70},
            {"type": "fal_generation", "run_id": "expensive", "estimated_cost_usd": 0.6, "score_final": 99},
        ]
        self.assertEqual(best_cheap_output(outputs, {"selected"})["run_id"], "cheap-b")

    def test_review_pack_suggests_decision_from_scores(self) -> None:
        output = {"type": "fal_generation", "score_final": 78, "estimated_cost_usd": 0.35}
        self.assertEqual(
            suggested_decision(output, {"technical_score": 100}, {"reference_similarity_score": 70}),
            "usable",
        )
        cheap = {"type": "fal_generation", "score_final": 62, "estimated_cost_usd": 0.2}
        self.assertEqual(suggested_decision(cheap, {"technical_score": 85}, {}), "rerun_on_stronger_model")


def make_model(model_id: str, mode: str, license_name: str, cost: float) -> VideoModel:
    return VideoModel(
        id=model_id,
        provider="fal",
        endpoint=f"fal-ai/{model_id}",
        mode=mode,
        license=license_name,
        default_duration_seconds=5,
        estimated_cost_usd=cost,
        cost_basis="test",
        strengths=[],
        risks=[],
        required_inputs=["prompt"],
        default_input={},
        source_url="https://fal.ai",
    )


if __name__ == "__main__":
    unittest.main()
