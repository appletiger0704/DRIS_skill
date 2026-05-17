#!/usr/bin/env python3
"""Search food database index for DRIs workbook db_name mapping.

Usage:
  python search_food.py 雞胸肉
  python search_food.py --index assets/food_database_index.json 雞胸肉
"""

import argparse
import json
from pathlib import Path


def load_index(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"Food index not found: {path}. Place food_database_index.json under assets/."
        )
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        return list(data.values())
    return data


def score_item(item: dict, query: str) -> int:
    text = " ".join(str(v) for v in item.values())
    score = 0
    if query in text:
        score += 10
    for ch in query:
        if ch in text:
            score += 1
    return score


def search(index: list[dict], query: str, topn: int = 10) -> list[dict]:
    scored = [(score_item(item, query), item) for item in index]
    scored = [(s, i) for s, i in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:topn]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--index", default="assets/food_database_index.json")
    parser.add_argument("--topn", type=int, default=10)
    args = parser.parse_args()

    data = load_index(Path(args.index))
    results = search(data, args.query, args.topn)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
