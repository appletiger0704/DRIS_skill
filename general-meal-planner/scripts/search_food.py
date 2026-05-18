#!/usr/bin/env python3
"""Search DRIS food database index for official food names.

Supported index formats:
1. {"foods": [{"sample_name": "...", "search_text": "..."}]}
2. [{"sample_name": "..."}]
3. {"白飯": {...}}

Usage:
  python scripts/search_food.py 雞胸肉
  python scripts/search_food.py --index assets/food_database_index.json --common assets/common_ingredients.json 雞胸肉
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_index(path: Path) -> list[dict[str, Any]]:
    data = load_json(path)
    if isinstance(data, dict) and isinstance(data.get("foods"), list):
        return data["foods"]
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        rows = []
        for key, value in data.items():
            if isinstance(value, dict):
                item = dict(value)
                item.setdefault("sample_name", key)
                rows.append(item)
        return rows
    raise ValueError(f"Unsupported food index schema: {path}")


def load_aliases(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    data = load_json(path)
    if isinstance(data, dict) and isinstance(data.get("aliases"), dict):
        return {str(k): str(v) for k, v in data["aliases"].items()}
    if isinstance(data, dict):
        return {str(k): str(v) for k, v in data.items() if isinstance(v, str)}
    return {}


def item_text(item: dict[str, Any]) -> str:
    preferred = [
        item.get("sample_name"),
        item.get("sample_id"),
        item.get("category"),
        item.get("description"),
        item.get("search_text"),
    ]
    return " ".join(str(v) for v in preferred if v not in (None, ""))


def score_item(item: dict[str, Any], query: str, alias_target: str | None = None) -> int:
    text = item_text(item)
    name = str(item.get("sample_name", ""))
    score = 0
    if alias_target and name == alias_target:
        score += 1000
    if query == name:
        score += 500
    if query in name:
        score += 100
    if query in text:
        score += 30
    for ch in query:
        if ch in text:
            score += 1
    return score


def search(index: list[dict[str, Any]], query: str, aliases: dict[str, str], topn: int = 10) -> list[dict[str, Any]]:
    alias_target = aliases.get(query)
    scored = [(score_item(item, query, alias_target), item) for item in index]
    scored = [(s, i) for s, i in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:topn]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--index", default="assets/food_database_index.json")
    parser.add_argument("--common", default="assets/common_ingredients.json")
    parser.add_argument("--topn", type=int, default=10)
    args = parser.parse_args()

    index = load_index(Path(args.index))
    aliases = load_aliases(Path(args.common))
    results = search(index, args.query, aliases, args.topn)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
