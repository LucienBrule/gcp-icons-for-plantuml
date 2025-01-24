import shutil
import os
import sys
import multiprocessing
import subprocess
from pathlib import Path
from multiprocessing import Pool
import yaml

from .env import verify  # optional: if you want to re-check before building
from .icon import Icon

MARKDOWN_PREFIX_TEMPLATE = """# GCP Symbols

Category | PUML Macro (Name) | Image (PNG) | PUML Url |
--- | --- | --- | --- |
"""

PUML_COPYRIGHT = """'SPDX-License-Identifier: MIT
"""

def build_all():
    # Optionally re-check env:
    # verify()

    # Load config
    config = _load_config()

    # Clear dist/
    dist_path = Path("dist")
    if dist_path.exists():
        shutil.rmtree(dist_path)
    dist_path.mkdir()

    # Copy .puml files from source/
    for puml_file in Path("source").glob("*.puml"):
        shutil.copy(puml_file, dist_path)

    # Gather icons
    icons = _collect_icons(config)

    # Create category folders
    categories = sorted({icon.category for icon in icons})
    for c in categories:
        (dist_path / c).mkdir(exist_ok=True)

    # Generate images and puml concurrently
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(_process_icon, icons)

    # Create an all.puml per category
    for c in categories:
        _create_category_all_file(dist_path / c)

    # Generate Markdown sheet
    _generate_markdown(icons, dist_path)


def _load_config():
    try:
        with open("scripts/config.yml") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config.yml: {e}")
        sys.exit(1)

def _collect_icons(config):
    files = list(Path("source", "official").glob("**/*.png"))
    return [Icon(str(f), config) for f in files]

def _process_icon(icon):
    icon_dir = Path("dist") / icon.category
    icon_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory is created correctly
    icon.generate_image(icon_dir, color=True, max_target_size=128, transparency=False)
    icon.generate_puml(icon_dir)
    icon.generate_image(icon_dir, color=True, max_target_size=128, transparency=True)

def _create_category_all_file(category_path):
    data = ""
    for f in sorted(category_path.glob("*.puml")):
        with open(f, "r") as rf:
            data += rf.read() + "\n"

    # Remove individual comments and add a single header
    filtered_lines = []
    for line in data.splitlines():
        if not line.startswith("'"):
            filtered_lines.append(line)
    content = PUML_COPYRIGHT + "\n".join(filtered_lines) + "\n"

    with open(category_path / "all.puml", "w") as af:
        af.write(content)

def _generate_markdown(icons, dist_path):
    icons_sorted = sorted(icons, key=lambda x: (x.category, x.target))
    categories = sorted({icon.category for icon in icons})
    md = MARKDOWN_PREFIX_TEMPLATE

    for cat in categories:
        md += f"**{cat}**||||\n"  # Just an extra line for grouping
        md += f"{cat}|(all macros)| - | [all.puml](dist/{cat}/all.puml) |\n"
        for icon in icons_sorted:
            if icon.category == cat:
                png_rel = f"dist/{cat}/{icon.target}.png"
                puml_rel = f"dist/{cat}/{icon.target}.puml"
                md_line = f"{cat}|{icon.target}|![{icon.target}]({png_rel})|{puml_rel}|"
                md += md_line + "\n"

    (dist_path / "GCPSymbols.md").write_text(md, encoding="utf-8")