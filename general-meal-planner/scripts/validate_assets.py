#!/usr/bin/env python3
"""Validate required assets for general-meal-planner skill."""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


REQUIRED = [
    "DRIs_template.xlsx",
    "food_database_index.json",
    "common_ingredients.json",
]


def validate_xlsx(path: Path) -> list[str]:
    errors: list[str] = []
    if not zipfile.is_zipfile(path):
        return [f"{path} is not a valid xlsx/zip file"]
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        required_parts = [
            "[Content_Types].xml",
            "xl/workbook.xml",
            "xl/_rels/workbook.xml.rels",
        ]
        for part in required_parts:
            if part not in names:
                errors.append(f"missing xlsx part: {part}")
        if len(names) < 40:
            errors.append(f"xlsx internal part count seems too low: {len(names)}")
        for name in names:
            if name.endswith(".xml"):
                try:
                    ET.fromstring(zf.read(name))
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"invalid xml {name}: {exc}")
    return errors


def validate_food_index(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"invalid food_database_index.json: {exc}"]
    foods = data.get("foods") if isinstance(data, dict) else data
    if not isinstance(foods, list):
        errors.append("food index must contain a foods list or be a list")
    elif len(foods) < 1000:
        errors.append(f"food index item count seems too low: {len(foods)}")
    return errors


def validate_common(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"invalid common_ingredients.json: {exc}"]
    aliases = data.get("aliases") if isinstance(data, dict) else data
    if not isinstance(aliases, dict) or not aliases:
        return ["common_ingredients.json must contain a non-empty aliases object or mapping"]
    return []


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    assets = root / "assets"
    errors: list[str] = []

    for filename in REQUIRED:
        path = assets / filename
        if not path.exists():
            errors.append(f"missing required asset: {path}")

    if (assets / "DRIs_template.xlsx").exists():
        errors.extend(validate_xlsx(assets / "DRIs_template.xlsx"))
    if (assets / "food_database_index.json").exists():
        errors.extend(validate_food_index(assets / "food_database_index.json"))
    if (assets / "common_ingredients.json").exists():
        errors.extend(validate_common(assets / "common_ingredients.json"))

    if errors:
        print("Asset validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Asset validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
