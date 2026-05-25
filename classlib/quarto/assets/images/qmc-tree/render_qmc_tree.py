import html
from pathlib import Path

import yaml


HERE = Path(__file__).parent
DEFAULT_YAML = HERE / "qmc-tree.yml"
DEFAULT_IMAGE = "../classlib/classlib/quarto/assets/images/qmc-tree/qmc-tree.png"


def render_qmc_tree(
    groups=None,
    labels=None,
    mask=None,
    yaml_path=None,
    image_path=None,
    tree_class="",
    tree_style="",
    tree_width="100%",
    tree_font_scale=1.0,
    show_group_labels=False,
    group_labels=None,
):
    yaml_path = Path(yaml_path or DEFAULT_YAML)
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

    image = image_path or DEFAULT_IMAGE

    all_labels = []

    if groups:
        for group in groups:
            all_labels.extend(data["groups"][group]["labels"])

    if labels:
        all_labels.extend(labels)

    seen = set()
    final_labels = []

    for label in all_labels:
        if label not in seen:
            final_labels.append(label)
            seen.add(label)

    class_attr = f'tree-slide {tree_class}'.strip()

    style_items = [
        f"--tree-width: {tree_width};",
        f"--tree-font-scale: {tree_font_scale};",
    ]

    if tree_style:
        style_items.append(tree_style)

    style_attr = f' style="{" ".join(style_items)}"'

    print(f'<div class="{html.escape(class_attr)}"{style_attr}>')
    print(f'<img src="{html.escape(image)}" class="tree-img">')

    if mask == "canopy":
        print('<div class="tree-mask-canopy"></div>')
    elif mask == "root":
        print('<div class="tree-only-root"></div>')

    if show_group_labels:
        group_labels = list(data["groups"].keys())

    if group_labels:
        for group_key in group_labels:
            group = data["groups"][group_key]

            print(
                f'<div class="tree-label {html.escape(group_key)}">'
                f'{group["label"]}</div>'
            )

    for label in final_labels:
        text = data["labels"][label]
        print(f'<div class="tree-example-label {html.escape(label)}">{text}</div>')

    print("</div>")
