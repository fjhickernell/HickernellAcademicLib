from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPOSITORY = Path(__file__).resolve().parents[4]
COMPONENTS = REPOSITORY / "classlib" / "quarto" / "components"
sys.path.insert(0, str(COMPONENTS))

from trees import TreeNotReadyError, TreeRenderError, render_tree, validate_tree


ASSET_BASE = "../classlib/classlib/quarto/components/trees"


class TreeRendererTests(unittest.TestCase):
    def test_returns_namespaced_html_and_resolves_shared_artwork(self) -> None:
        result = render_tree("qmc", labels=["algebra"], asset_base_url=ASSET_BASE)
        self.assertIn('class="tree-component tree-component--qmc"', result)
        self.assertIn('data-tree-id="qmc"', result)
        self.assertIn(
            'src="../classlib/classlib/quarto/components/trees/artwork/tree.png"',
            result,
        )
        self.assertIn('class="tree-component__label"', result)
        self.assertIn(">Algebra</div>", result)
        self.assertNotIn("tree-slide", result)
        self.assertNotIn("tree-example-label", result)

    def test_groups_expand_in_order_and_labels_are_deduplicated(self) -> None:
        result = render_tree(
            "qmc",
            groups=["foundation"],
            labels=["analysis", "sequence", "algebra"],
            asset_base_url=ASSET_BASE,
        )
        identifiers = [
            'data-label-id="algebra"',
            'data-label-id="analysis"',
            'data-label-id="cs"',
            'data-label-id="domain"',
            'data-label-id="statistics"',
            'data-label-id="sequence"',
        ]
        positions = [result.index(identifier) for identifier in identifiers]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(result.count('data-label-id="algebra"'), 1)
        self.assertEqual(result.count('data-label-id="analysis"'), 1)

    def test_direct_labels_do_not_require_groups(self) -> None:
        result = render_tree(
            "qmc",
            labels=["discrepancy", "software"],
            asset_base_url=ASSET_BASE,
        )
        self.assertIn('data-label-id="discrepancy"', result)
        self.assertIn('data-label-id="software"', result)
        self.assertNotIn('data-group-id="theory"', result)

    def test_group_headings_can_be_selected_or_all_shown(self) -> None:
        selected = render_tree(
            "qmc", group_headings=["theory"], asset_base_url=ASSET_BASE
        )
        self.assertIn('data-group-id="theory"', selected)
        self.assertNotIn('data-group-id="foundation"', selected)

        all_headings = render_tree(
            "qmc", show_group_headings=True, asset_base_url=ASSET_BASE
        )
        self.assertEqual(all_headings.count('data-group-id="'), 3)

        with self.assertRaisesRegex(TreeRenderError, "mutually exclusive"):
            render_tree(
                "qmc",
                group_headings=["theory"],
                show_group_headings=True,
                asset_base_url=ASSET_BASE,
            )

    def test_masks_are_namespaced_and_validated(self) -> None:
        result = render_tree("qmc", mask="canopy", asset_base_url=ASSET_BASE)
        self.assertIn("tree-component__mask--canopy", result)
        self.assertIn('data-mask-id="canopy"', result)
        with self.assertRaisesRegex(TreeRenderError, "undefined mask"):
            render_tree("qmc", mask="branches", asset_base_url=ASSET_BASE)

    def test_safe_classes_and_identifiers_are_enforced(self) -> None:
        result = render_tree(
            "qmc", classes=["lecture-tree"], asset_base_url=ASSET_BASE
        )
        self.assertIn("tree-component--qmc lecture-tree", result)
        with self.assertRaisesRegex(TreeRenderError, "safe kebab-case"):
            render_tree(
                "qmc", classes=["unsafe class"], asset_base_url=ASSET_BASE
            )
        with self.assertRaisesRegex(TreeRenderError, "sequence, not a string"):
            render_tree("qmc", groups="theory", asset_base_url=ASSET_BASE)

    def test_plain_text_is_escaped_and_inline_html_is_trusted(self) -> None:
        qmc = render_tree("qmc", labels=["cs"], asset_base_url=ASSET_BASE)
        self.assertIn("Computer<br>Science", qmc)

        data = {
            "schema_version": 1,
            "id": "escape-test",
            "status": "ready",
            "image": {
                "file": "../artwork/tree.png",
                "alt": "A & B",
                "aspect_ratio": "4 / 3",
            },
            "defaults": {
                "width": "100%",
                "font_scale": 1,
                "label_align": "left",
                "group_align": "left",
            },
            "groups": {},
            "labels": {
                "plain": {
                    "text": "<em>not markup</em>",
                    "position": {"left": "1%", "top": "2%"},
                }
            },
            "masks": {},
        }
        result = render_tree(
            validate_tree(data),
            labels=["plain"],
            asset_base_url=ASSET_BASE,
        )
        self.assertIn("&lt;em&gt;not markup&lt;/em&gt;", result)
        self.assertIn('alt="A &amp; B"', result)

    def test_output_contains_coordinates_alignment_and_overrides(self) -> None:
        result = render_tree(
            "qmc",
            labels=["cs"],
            width="80%",
            font_scale=1.25,
            asset_base_url=ASSET_BASE,
        )
        self.assertIn("--tree-width: 80%", result)
        self.assertIn("--tree-font-scale: 1.25", result)
        self.assertIn("--tree-left: 42%", result)
        self.assertIn("--tree-top: 90%", result)
        self.assertIn("--tree-align: center", result)

    def test_undefined_selection_and_placeholder_fail_cleanly(self) -> None:
        with self.assertRaisesRegex(TreeRenderError, "undefined group"):
            render_tree("qmc", groups=["unknown"], asset_base_url=ASSET_BASE)
        with self.assertRaisesRegex(TreeRenderError, "undefined label"):
            render_tree("qmc", labels=["unknown"], asset_base_url=ASSET_BASE)
        with self.assertRaises(TreeNotReadyError):
            render_tree("mc", asset_base_url=ASSET_BASE)


if __name__ == "__main__":
    unittest.main()
