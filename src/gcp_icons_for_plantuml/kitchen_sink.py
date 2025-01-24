import os
import random
from pathlib import Path

def generate_kitchen_sync_example(grid_size, output_dir):
    """
    Generate a PlantUML file with an NxN grid of all icons.
    """
    dist_path = Path("dist")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Prepare the .puml content
    puml_content = "@startuml KitchenSink\n\n"
    puml_content += "' Shared macros\n"
    puml_content += "!include ../dist/GCPCommon.puml\n\n"

    # Gather all individual macros from `dist/*/*.puml` (excluding `all.puml`)
    all_macro_files = sorted(dist_path.glob("*/**/*.puml"))
    all_macros = [file.stem for file in all_macro_files if file.name != "all.puml"]

    if not all_macros:
        raise FileNotFoundError("No individual macros found in dist/. Run the build command first.")

    # Include all categories' `all.puml` files (for completeness)
    all_puml_files = sorted(dist_path.glob("*/all.puml"))
    for puml_file in all_puml_files:
        puml_content += f"!include ../{str(puml_file)}\n"

    puml_content += "\nLAYOUT_TOP_DOWN\n"
    puml_content += f"title \"Kitchen Sink Example: {grid_size}x{grid_size}\"\n\n"

    # Add grid layout
    puml_content += "rectangle \"Icon Grid\" as grid {\n"

    # Generate a grid of icons using available macros
    macro_index = 0
    for row in range(grid_size):
        for col in range(grid_size):
            # Cycle through available macros (wrap-around if necessary)
            macro_name = all_macros[macro_index % len(all_macros)]
            alias = f"icon_{row}_{col}"
            label = macro_name.replace("_", " ").title()  # Convert macro name to Title Case
            puml_content += f"  {macro_name}({alias}, \"{label}\", \"Technology\")\n"
            macro_index += 1

    puml_content += "}\n"
    puml_content += "\n@enduml"

    # Save to file
    output_file = output_path / f"kitchen-sync-{grid_size}x{grid_size}.puml"
    output_file.write_text(puml_content, encoding="utf-8")
    print(f"Generated kitchen-sync example at {output_file}")

def generate_verification_examples(output_dir):
    """
    Generate a .puml file for each icon in the library for verification purposes.
    """
    dist_path = Path("dist")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Gather all individual macros from `dist/*/*.puml` (excluding `all.puml`)
    all_macro_files = sorted(dist_path.glob("*/**/*.puml"))
    all_macros = [file.stem for file in all_macro_files if file.name != "all.puml"]

    if not all_macros:
        raise FileNotFoundError("No individual macros found in dist/. Run the build command first.")

    for macro_file in all_macro_files:
        category = macro_file.parent.name
        macro_name = macro_file.stem
        label = macro_name.replace("_", " ").title()

        # Generate a .puml file for the macro
        puml_content = f"""@startuml Verification-{macro_name}

' Include shared macros
!include ../../dist/GCPCommon.puml
!include ../../dist/{category}/{macro_name}.puml

' Test the macro
{macro_name}(alias, "{label}", "Technology")

@enduml
"""
        output_file = output_path / f"{macro_name}.puml"
        output_file.write_text(puml_content, encoding="utf-8")

    print(f"Generated verification examples in {output_path}")

import random
from pathlib import Path


def generate_complex_diagram(output_dir, max_connections=5, num_nodes=100):
    """
    Generate a large, interconnected network diagram with icons.
    """
    dist_path = Path("dist")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Gather all individual macros from `dist/*/*.puml` (excluding `all.puml`)
    all_macro_files = sorted(dist_path.glob("*/**/*.puml"))
    all_macros = [file.stem for file in all_macro_files if file.name != "all.puml"]

    if not all_macros:
        raise FileNotFoundError("No individual macros found in dist/. Run the build command first.")

    # Prepare the .puml content
    puml_content = "@startuml ComplexDiagram\n\n"
    puml_content += "' Shared macros\n"
    puml_content += "!include ../dist/GCPCommon.puml\n\n"

    # Include all macros
    for macro_file in all_macro_files:
        category = macro_file.parent.name
        puml_content += f"!include ../dist/{category}/{macro_file.name}\n"

    puml_content += "\nLAYOUT_LEFT_RIGHT\n"
    puml_content += "title \"Complex Network Diagram\"\n\n"

    # Create nodes
    nodes = []
    used_aliases = set()  # Track used aliases
    for i in range(num_nodes):
        macro_name = all_macros[i % len(all_macros)]  # Cycle through macros
        alias = f"node_{i}"  # Unique alias for each node
        while alias in used_aliases:  # Ensure no duplicates
            alias = f"node_{i}_{random.randint(0, 9999)}"
        used_aliases.add(alias)  # Mark alias as used
        label = macro_name.replace("_", " ").title()
        nodes.append((alias, macro_name, label))
        puml_content += f"{macro_name}({alias}, \"{label}\", \"Technology\")\n"

    # Randomly connect nodes
    for node in nodes:
        alias, _, _ = node
        connections = random.sample(nodes, min(max_connections, len(nodes)))
        for conn in connections:
            target_alias, _, _ = conn
            if alias != target_alias:  # Avoid self-loops
                puml_content += f"{alias} --> {target_alias}\n"

    puml_content += "\n@enduml"

    # Save to file
    output_file = output_path / "complex-network-diagram.puml"
    output_file.write_text(puml_content, encoding="utf-8")
    print(f"Generated complex network diagram at {output_file}")