from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml

spec = importlib.util.spec_from_file_location(
    "collaborator_assets", Path(__file__).resolve().parents[1] / "tools/collaborator_assets.py"
)
assets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assets)


class CollaboratorAssetsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "talk"
        self.project.mkdir()
        self.archive = self.root / "photos"
        self.archive.mkdir()
        self.master = self.root / "master.yml"
        self.master.write_text(yaml.safe_dump({"schema_version": 1, "collaborators": {
            "alpha-ann": {"name": "Ann Alpha"}, "beta-bob": {"name": "Bob Beta"},
        }}))
        entries = []
        for person in ["alpha-ann", "beta-bob"]:
            data = f"fixture portrait bytes: {person}".encode()
            (self.archive / f"{person}.jpg").write_bytes(data)
            entries.append({"id": person, "file": f"{person}.jpg",
                            "sha256": hashlib.sha256(data).hexdigest()})
        (self.archive / "catalog.yml").write_text(yaml.safe_dump({
            "schema_version": 1, "headshots": entries,
        }))
        self.config = {"schema_version": 1, "photo_directory": "photos",
                       "manifest": "photos/manifest.json", "extra_ids": ["alpha-ann"],
                       "galleries": {"selected": {"ids": ["beta-bob", "alpha-ann"],
                           "output": "selected.qmd", "image_prefix": "../photos"}}}
        self.config_path = self.project / "selection.yml"
        self.save_config()

    def save_config(self):
        self.config_path.write_text(yaml.safe_dump(self.config, sort_keys=False))

    def run_assets(self, refresh=False):
        return assets.run(self.config_path, self.project, self.master, self.archive, refresh)

    def test_explicit_order_master_names_and_unchanged_unselected_files(self):
        unrelated = self.project / "unrelated.jpg"
        unrelated.write_bytes(b"preserve")
        result = self.run_assets(refresh=True)
        self.assertEqual(result["portraits"], 2)
        markup = (self.project / "selected.qmd").read_text()
        self.assertLess(markup.index("Bob Beta"), markup.index("Ann Alpha"))
        self.assertEqual(unrelated.read_bytes(), b"preserve")
        self.assertEqual((self.project / "photos/alpha-ann.jpg").read_bytes(),
                         (self.archive / "alpha-ann.jpg").read_bytes())

    def test_check_needs_no_archive_and_does_not_write(self):
        self.run_assets(refresh=True)
        before = {p: p.stat().st_mtime_ns for p in self.project.rglob("*") if p.is_file()}
        self.archive.rename(self.root / "unavailable-icloud")
        self.run_assets()
        self.assertEqual(before, {p: p.stat().st_mtime_ns for p in before})

    def test_unknown_person_fails_before_any_asset_writes(self):
        self.config["extra_ids"].append("new-person")
        self.save_config()
        with self.assertRaisesRegex(ValueError, "Unknown ID"):
            self.run_assets(refresh=True)
        self.assertFalse((self.project / "photos").exists())

    def test_bad_archive_hash_fails_before_any_asset_writes(self):
        (self.archive / "beta-bob.jpg").write_bytes(b"changed in iCloud")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.run_assets(refresh=True)
        self.assertFalse((self.project / "photos").exists())

    def test_missing_photo_fails_before_any_asset_writes(self):
        (self.archive / "beta-bob.jpg").unlink()
        with self.assertRaises(FileNotFoundError):
            self.run_assets(refresh=True)
        self.assertFalse((self.project / "photos").exists())

    def test_stale_caption_and_changed_publishing_copy_are_detected(self):
        self.run_assets(refresh=True)
        include = self.project / "selected.qmd"
        include.write_text(include.read_text().replace("Bob Beta", "Wrong Name"))
        with self.assertRaisesRegex(ValueError, "stale"):
            self.run_assets()
        self.run_assets(refresh=True)
        (self.project / "photos/beta-bob.jpg").write_bytes(b"edited locally")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.run_assets()

    def test_adding_unselected_person_does_not_change_the_talk(self):
        self.run_assets(refresh=True)
        master = yaml.safe_load(self.master.read_text())
        master["collaborators"]["gamma-gail"] = {"name": "Gail Gamma"}
        self.master.write_text(yaml.safe_dump(master))
        self.run_assets()
        manifest = json.loads((self.project / "photos/manifest.json").read_text())
        self.assertNotIn("gamma-gail", manifest["headshots"])

    def test_changed_master_name_requires_deliberate_refresh(self):
        self.run_assets(refresh=True)
        master = yaml.safe_load(self.master.read_text())
        master["collaborators"]["beta-bob"]["name"] = "Robert Beta"
        self.master.write_text(yaml.safe_dump(master))
        with self.assertRaisesRegex(ValueError, "Name changed"):
            self.run_assets()
        self.run_assets(refresh=True)
        self.assertIn("Robert Beta", (self.project / "selected.qmd").read_text())

    def test_unsafe_output_and_duplicate_gallery_people_are_rejected(self):
        self.config["galleries"]["selected"]["output"] = "../outside.qmd"
        self.save_config()
        with self.assertRaisesRegex(ValueError, "inside the consumer"):
            self.run_assets(refresh=True)
        self.config["galleries"]["selected"]["output"] = "selected.qmd"
        self.config["galleries"]["selected"]["ids"].append("beta-bob")
        self.save_config()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.run_assets(refresh=True)


if __name__ == "__main__":
    unittest.main()
