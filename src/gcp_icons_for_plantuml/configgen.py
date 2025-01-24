import sys
import re
import yaml
from pathlib import Path

TEMPLATE_DEFAULT = """
Defaults:
  Colors:
    GoogleBlue: "#4284F3"
  Category:
    Color: GoogleBlue
  TargetMaxSize: 64
"""

def create():
    source_files = _build_file_list()
    entries = []
    current_category = None
    category_dict = {}
    seen_targets = set()

    for file_str in sorted(str(f) for f in source_files):
        parts = file_str.split("/")
        # The first part might be "source", the second "official", the third is category
        # If there's no third part, default to "Uncategorized"
        category = parts[2] if len(parts) > 2 else "Uncategorized"
        source_name = parts[-1]
        target_name = _make_target_name(source_name)

        if category != current_category:
            if current_category is not None:
                entries.append(category_dict)
            current_category = category
            category_dict = {"Name": category, "SourceDir": category, "Services": []}

        service_entry = {"Source": source_name, "Target": target_name}
        if target_name in seen_targets:
            service_entry["ZComment"] = "******* Duplicate target name *******"
        category_dict["Services"].append(service_entry)
        seen_targets.add(target_name)

    if category_dict:
        entries.append(category_dict)

    template_yaml = yaml.safe_load(TEMPLATE_DEFAULT)
    template_yaml["Categories"] = entries

    with open("scripts/config-template.yml", "w") as f:
        yaml.dump(template_yaml, f, sort_keys=False)
    print("Successfully created config-template.yml.")
    sys.exit(0)

def _build_file_list():
    p = Path("source") / "official"
    return p.glob("**/*.png")

def _make_target_name(name):
    # e.g. app_engine.png -> app_engine
    base = name.replace(".png", "")
    # Replace non-alphanumeric with underscores
    return re.sub(r'\W+', '_', base)