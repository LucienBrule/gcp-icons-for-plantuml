import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

import requests

ICON_ZIP_URL = "https://cloud.google.com/icons/files/google-cloud-icons.zip"
OFFICIAL_DIR = Path("source") / "official"

def fetch_and_prepare_icons():
    # Download zip
    zip_path = download_zip(ICON_ZIP_URL)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_extracted = Path(tmpdir, "extracted")
        tmp_extracted.mkdir(parents=True, exist_ok=True)

        # Unzip
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp_extracted)

        # Copy files into source/official, skipping __MACOSX & .svg
        copy_and_normalize(tmp_extracted)

    # Remove local zip after extraction
    zip_path.unlink(missing_ok=True)
    print("Icon set successfully fetched and placed in source/official.")

def download_zip(url: str) -> Path:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    zip_path = Path("google_cloud_icons.zip")
    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return zip_path

def copy_and_normalize(extracted_dir: Path):
    """
    Recursively walk the unzipped directory,
    skip .svg if we only want PNG,
    and copy everything into source/official without renaming.
    """
    if OFFICIAL_DIR.exists():
        shutil.rmtree(OFFICIAL_DIR)
    OFFICIAL_DIR.mkdir(parents=True)

    for root, dirs, files in os.walk(extracted_dir):
        # Skip `__MACOSX` directories
        if "__MACOSX" in root:
            continue
        dirs[:] = [d for d in dirs if d != "__MACOSX"]

        rel_parts = Path(root).relative_to(extracted_dir).parts
        target_dir = OFFICIAL_DIR.joinpath(*rel_parts)
        target_dir.mkdir(parents=True, exist_ok=True)

        for fname in files:
            if fname.startswith("._"):
                continue  # skip Apple resource forks
            src_file = Path(root, fname)
            if not src_file.is_file():
                continue

            # Skip .svg if you only want PNG
            if src_file.suffix.lower() == ".svg":
                continue

            # Copy file *exactly* as is
            shutil.copy2(src_file, target_dir / fname)