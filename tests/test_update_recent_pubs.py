import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


def load_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "scripts" / "update_recent_pubs.py"
    spec = importlib.util.spec_from_file_location("update_recent_pubs", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


updater = load_module()


class UpdateRecentPubsTests(unittest.TestCase):
    def test_replace_recent_section_replaces_existing_tail(self):
        content = """### Highlighted Papers\n- old\n\n### Recent Papers\n\n- stale entry\n"""
        new_entries = "- new entry"

        updated = updater.replace_recent_section(content, new_entries)

        self.assertIn("### Recent Papers", updated)
        self.assertIn("- new entry", updated)
        self.assertNotIn("stale entry", updated)
        self.assertIn("### Highlighted Papers", updated)

    def test_replace_recent_section_appends_if_missing(self):
        content = "### Highlighted Papers\n- one\n"

        updated = updater.replace_recent_section(content, "- new entry")

        self.assertIn("### Recent Papers", updated)
        self.assertIn("- new entry", updated)
        self.assertIn("---", updated)

    def test_parse_ads_response_validates_shape(self):
        with self.assertRaises(RuntimeError):
            updater.parse_ads_response({"no_response": {}})

        with self.assertRaises(RuntimeError):
            updater.parse_ads_response({"response": {"numFound": "3", "docs": []}})

        with self.assertRaises(RuntimeError):
            updater.parse_ads_response({"response": {"numFound": 3, "docs": "bad"}})

    def test_write_text_atomic_replaces_contents(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = os.path.join(tmp_dir, "out.md")
            with open(target, "w", encoding="utf-8") as file_handle:
                file_handle.write("old")

            updater.write_text_atomic(target, "new")

            with open(target, "r", encoding="utf-8") as file_handle:
                self.assertEqual(file_handle.read(), "new")


if __name__ == "__main__":
    unittest.main()
