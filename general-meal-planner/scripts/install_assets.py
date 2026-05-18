#!/usr/bin/env python3
"""Install generated assets into the general-meal-planner skill folder.

Usage:
  python scripts/install_assets.py /path/to/general-meal-planner-assets.zip
  python scripts/install_assets.py /path/to/assets
"""

from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path


REQUIRED = [
    "DRIs_template.xlsx",
    "food_database_index.json",
    "common_ingredients.json",
]


def copy_assets(src_assets: Path, dst_assets: Path) -> None:
    dst_assets.mkdir(parents=True, exist_ok=True)
    for filename in REQUIRED:
        src = src_assets / filename
        if not src.exists():
            raise FileNotFoundError(f"missing required asset in source: {src}")
        shutil.copy2(src, dst_assets / filename)


def install_from_zip(zip_path: Path, dst_assets: Path) -> None:
    temp_dir = dst_assets.parent / ".asset_install_tmp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(temp_dir)
        candidates = [p for p in temp_dir.rglob("DRIs_template.xlsx")]
        if not candidates:
            raise FileNotFoundError("DRIs_template.xlsx not found in zip")
        src_assets = candidates[0].parent
        copy_assets(src_assets, dst_assets)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="assets directory or general-meal-planner-assets.zip")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    dst_assets = root / "assets"
    source = Path(args.source).expanduser().resolve()

    if source.is_file() and source.suffix.lower() == ".zip":
        install_from_zip(source, dst_assets)
    elif source.is_dir():
        copy_assets(source, dst_assets)
    else:
        raise FileNotFoundError(f"source must be an assets directory or zip file: {source}")

    print(f"Assets installed to: {dst_assets}")
    print("Next: python scripts/validate_assets.py")


if __name__ == "__main__":
    main()
