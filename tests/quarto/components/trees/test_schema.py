from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest


REPOSITORY = Path(__file__).resolve().parents[4]
COMPONENTS = REPOSITORY / "classlib" / "quarto" / "components"
sys.path.insert(0, str(COMPONENTS))

from trees import TreeSchemaError, load_tree, validate_tree


def valid_data() -> dict:
    return {
        "schema_version": 1,
        "id": "test-tree",
        "status": "ready",
        "image": {
            "file": "../artwork/tree.png",
            "alt": "Test tree",
            "aspect_ratio": "4 / 3",
        },
        "defaults": {
            "width": "100%",
            "font_scale": 1,
            "label_align": "left",
            "group_align": "center",
        },
        "groups": {
            "first-group": {
                "text": "First",
                "labels": ["first-label", "second-label"],
                "position": {"left": "10%", "top": "20%"},
            }
        },
        "labels": {
            "first-label": {
                "text": "Escaped",
                "position": {"left": "30%", "top": "40%"},
            },
            "second-label": {
                "html": "Trusted<br>HTML",
                "position": {"left": "50%", "top": "60%"},
                "align": "right",
            },
        },
        "masks": {"canopy": {"description": "Show the canopy"}},
    }


class TreeSchemaTests(unittest.TestCase):
    def test_loads_migrated_qmc_tree_in_declared_order(self) -> None:
        tree = load_tree("qmc")
        self.assertEqual(tree.schema_version, 1)
        self.assertEqual(tuple(tree.groups), ("foundation", "theory", "practice"))
        self.assertEqual(len(tree.labels), 24)
        self.assertEqual(
            tree.groups["foundation"].labels,
            ("algebra", "analysis", "cs", "domain", "statistics"),
        )
        self.assertEqual(tuple(tree.masks), ("root", "canopy"))
        self.assertTrue(tree.labels["cs"].content.trusted_html)

    def test_loads_mc_tree(self) -> None:
        tree = load_tree("mc")
        self.assertEqual(tree.status, "ready")
        self.assertEqual(tuple(tree.groups), ("foundation", "methods", "practice"))
        self.assertEqual(len(tree.labels), 28)
        self.assertIsNotNone(tree.image)

    def test_rejects_unknown_and_missing_fields(self) -> None:
        unknown = valid_data()
        unknown["surprise"] = True
        with self.assertRaisesRegex(TreeSchemaError, "unknown fields"):
            validate_tree(unknown)

        missing = valid_data()
        del missing["defaults"]
        with self.assertRaisesRegex(TreeSchemaError, "ready tree is missing"):
            validate_tree(missing)

    def test_rejects_wrong_schema_version(self) -> None:
        data = valid_data()
        data["schema_version"] = 2
        with self.assertRaisesRegex(TreeSchemaError, "unsupported version 2"):
            validate_tree(data)

    def test_rejects_unsafe_identifiers(self) -> None:
        data = valid_data()
        data["id"] = "Bad Tree"
        with self.assertRaisesRegex(TreeSchemaError, "must match"):
            validate_tree(data)

        data = valid_data()
        data["labels"]["bad_label"] = data["labels"].pop("first-label")
        data["groups"]["first-group"]["labels"][0] = "bad_label"
        with self.assertRaisesRegex(TreeSchemaError, "must match"):
            validate_tree(data)

    def test_rejects_undefined_group_label(self) -> None:
        data = valid_data()
        data["groups"]["first-group"]["labels"].append("missing-label")
        with self.assertRaisesRegex(TreeSchemaError, "undefined label"):
            validate_tree(data)

    def test_validates_positions_alignments_and_content_mode(self) -> None:
        data = valid_data()
        data["labels"]["first-label"]["position"]["left"] = "calc(1% + 2px)"
        with self.assertRaisesRegex(TreeSchemaError, "unsupported CSS length"):
            validate_tree(data)

        data = valid_data()
        data["labels"]["first-label"]["align"] = "middle"
        with self.assertRaisesRegex(TreeSchemaError, "must be one of"):
            validate_tree(data)

        data = valid_data()
        data["labels"]["first-label"]["html"] = "<b>also HTML</b>"
        with self.assertRaisesRegex(TreeSchemaError, "exactly one"):
            validate_tree(data)

    def test_defaults_and_overrides_are_retained(self) -> None:
        tree = validate_tree(valid_data())
        self.assertEqual(tree.groups["first-group"].align, "center")
        self.assertEqual(tree.labels["first-label"].align, "left")
        self.assertEqual(tree.labels["second-label"].align, "right")

    def test_placeholder_is_minimal(self) -> None:
        tree = validate_tree(
            {"schema_version": 1, "id": "future-tree", "status": "placeholder"}
        )
        self.assertEqual(tree.status, "placeholder")

        invalid = {
            "schema_version": 1,
            "id": "future-tree",
            "status": "placeholder",
            "labels": {},
        }
        with self.assertRaisesRegex(TreeSchemaError, "placeholder tree cannot"):
            validate_tree(invalid)

    def test_input_is_not_mutated(self) -> None:
        data = valid_data()
        before = deepcopy(data)
        validate_tree(data)
        self.assertEqual(data, before)


if __name__ == "__main__":
    unittest.main()
