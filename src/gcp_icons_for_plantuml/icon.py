import sys
import re
import subprocess
from pathlib import Path
from PIL import Image

PUML_LICENSE_HEADER = """' SPDX-License-Identifier: CC-BY-ND-2.0
"""

class Icon:
    def __init__(self, file_path, config):
        self.file_path = Path(file_path)
        self.config = config
        self.source_name = self.file_path.name
        self.source_category = self.file_path.parent.name
        self.category = "Uncategorized"
        self.target = None
        self.color = "#000000"
        self._set_values()

    def generate_image(self, out_dir, color=True, max_target_size=128, transparency=False):
        im = Image.open(self.file_path)
        im.thumbnail((max_target_size, max_target_size))
        if not transparency:
            im = self._remove_transparency(im)
        out_file = out_dir / f"{self.target}.png"
        im.save(out_file, "PNG")

    def generate_puml(self, out_dir):
        png_file = out_dir / f"{self.target}.png"
        content = PUML_LICENSE_HEADER
        try:
            result = subprocess.run(
                ["java", "-jar", "scripts/plantuml.jar", "-encodesprite", "16z", str(png_file)],
                capture_output=True,
                check=True,
            )
            content += result.stdout.decode("UTF-8")
            content += f"GCPEntityColoring({self.target})\n"
            content += f"!define {self.target}(e_alias, e_label, e_techn) GCPEntity(e_alias, e_label, e_techn, {self.color}, {self.target}, {self.target})\n"
            content += f"!define {self.target}(e_alias, e_label, e_techn, e_descr) GCPEntity(e_alias, e_label, e_techn, e_descr, {self.color}, {self.target}, {self.target})\n"
            content += f"!define {self.target}Participant(p_alias, p_label, p_techn) GCPParticipant(p_alias, p_label, p_techn, {self.color}, {self.target}, {self.target})\n"
            content += f"!define {self.target}Participant(p_alias, p_label, p_techn, p_descr) GCPParticipant(p_alias, p_label, p_techn, p_descr, {self.color}, {self.target}, {self.target})\n"
        except Exception as e:
            print(f"Error generating puml for {self.target}: {e}")
            sys.exit(1)
        out_path = out_dir / f"{self.target}.puml"
        out_path.write_text(content, encoding="utf-8")

    def _set_values(self):
        # Attempt to find matching config entry
        cats = self.config.get("Categories", [])
        for cat_item in cats:
            cat_name = cat_item.get("Name", "Uncategorized")
            src_dir = cat_item.get("SourceDir", "")
            for svc in cat_item.get("Services", []):
                if svc["Source"] == self.source_name and src_dir == self.source_category:
                    self.category = cat_name
                    self.target = svc["Target"]
                    self.color = _resolve_color(svc, cat_item, self.config)
                    return

        # If no match, use fallback
        self.target = self._make_name(self.source_name)
        self.color = self.config["Defaults"]["Category"].get("Color", "#000000")

    def _make_name(self, name):
        base = name.replace(".png", "")
        if base.startswith("GCP-"):
            base = base.split("-", 1)[1]
        return re.sub(r'\W+', '_', base)

    def _remove_transparency(self, image, bg=(255,255,255)):
        if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
            alpha = image.convert("RGBA").split()[-1]
            new_bg = Image.new("RGBA", image.size, bg + (255,))
            new_bg.paste(image, mask=alpha)
            return new_bg
        return image

def _resolve_color(service_entry, category_entry, config):
    # Check service, category, or default
    if "Color" in service_entry:
        return _lookup_color(service_entry["Color"], config)
    if "Color" in category_entry:
        return _lookup_color(category_entry["Color"], config)
    defaults = config.get("Defaults", {}).get("Category", {})
    return defaults.get("Color", "#000000")

def _lookup_color(color_key, config):
    colors = config.get("Defaults", {}).get("Colors", {})
    return colors.get(color_key, "#4284F3")