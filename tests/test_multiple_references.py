import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from amarillo.fal_runner import fill_uploaded_image_url
from amarillo.prompts import build_analysis, build_analysis_from_notes, pattern_from_analysis
from amarillo.reference_compare import reference_id_for_output
from amarillo.io import read_json


class MultipleReferenceTests(unittest.TestCase):
    def test_unknown_reference_does_not_inherit_reward_ad_scenes(self):
        sample = {"sample_id": "new", "source_path": "landscape.mp4", "metadata": {"aspect_ratio": "16:9"}}
        pattern = pattern_from_analysis(build_analysis(sample))
        self.assertEqual(pattern["prompt_variants"][0]["variant_id"], "reference_structure")
        self.assertNotIn("checkout", pattern["prompt_variants"][0]["prompt"])

    def test_motion_variants_survive_analysis_and_library_build(self):
        notes = read_json(Path("analysis_notes/motion5.json"))
        sample = {"sample_id": notes["sample_id"], "source_path": "motion.mp4", "metadata": {}}
        pattern = pattern_from_analysis(build_analysis_from_notes(sample, notes))
        self.assertEqual(pattern["prompt_variants"], notes["prompt_variants"])
        self.assertNotIn("checkout", pattern["prompt_variants"][0]["prompt"])

    def test_second_sample_does_not_compare_to_first_reference(self):
        self.assertEqual(reference_id_for_output({"pattern_id": "motion-pattern"}, ["cero", "motion"]), "motion")
        self.assertEqual(reference_id_for_output({"source_sample_id": "motion"}, ["cero", "motion"]), "motion")

    def test_legacy_assembled_output_resolves_from_source_plate(self):
        self.assertEqual(reference_id_for_output({"source_plates": ["artifacts/cero-pattern__launch__kling.mp4"]}, ["cero", "motion"]), "cero")

    def test_legacy_run_without_pattern_metadata_resolves_by_exact_prefix(self):
        self.assertEqual(reference_id_for_output({"run_id": "cero-pattern__launch__kling"}, ["cero", "motion"]), "cero")

    def test_ambiguous_output_is_not_silently_assigned_to_first_sample(self):
        self.assertIsNone(reference_id_for_output({}, ["cero", "motion"]))

    def test_current_fal_start_image_field_uploads(self):
        with tempfile.NamedTemporaryFile() as image:
            client = Mock()
            client.upload_file.return_value = "https://example.test/upload.png"
            payload = {"start_image_url": "REQUIRED_IMAGE_URL", "image_path": image.name}
            self.assertIsNone(fill_uploaded_image_url(payload, client))
            self.assertEqual(payload["start_image_url"], "https://example.test/upload.png")
            self.assertNotIn("image_url", payload)
