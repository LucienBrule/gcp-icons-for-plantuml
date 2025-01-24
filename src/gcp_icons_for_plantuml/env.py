import subprocess
import sys
from pathlib import Path

def verify():
    # Ensure config.yml exists
    config_path = Path("scripts/config.yml")
    if not config_path.is_file():
        print("Error: config.yml not found in scripts/ directory.")
        sys.exit(1)

    # Check for essential source files
    source_dir = Path("source")
    if not (source_dir / "GCPCommon.puml").exists():
        print("Error: GCPCommon.puml not found in source/ directory.")
        sys.exit(1)

    official_dir = source_dir / "official"
    if not official_dir.is_dir():
        print("Error: source/official directory not found.")
        sys.exit(1)

    # Check PlantUML jar availability
    jar_path = Path("scripts/plantuml.jar")
    if not jar_path.is_file():
        print("Error: plantuml.jar not found in scripts/ directory.")
        sys.exit(1)

    try:
        subprocess.run(
            ["java", "-jar", str(jar_path), "-version"],
            capture_output=True,
            check=True,
        )
    except Exception as e:
        print(f"Error running plantuml.jar: {e}")
        sys.exit(1)

    print("Prerequisites met.")