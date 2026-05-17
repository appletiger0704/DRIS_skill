#!/usr/bin/env python3
"""Write a structured meal plan into the 計算 sheet of a DRIs Excel workbook.

Expected JSON schema:
{
  "menu_name": "example",
  "meals": [
    {
      "meal": "2午餐",
      "dishes": [
        {
          "dish_category": "主食",
          "dish_name": "白飯",
          "ingredients": [
            {"colloquial": "白米", "db_name": "粳米平均值", "weight_g": 50}
          ]
        }
      ]
    }
  ]
}

Lunch and dinner must contain exactly:
- 1 主食
- 1 主菜 or 主餐
- 3 副菜
"""

import argparse
import json
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook


VALID_MAIN_DISH = {"主菜", "主餐"}


def validate_lunch_dinner_structure(menu: dict) -> None:
    """Validate 2午餐 and 3晚餐 structure."""
    errors = []
    for meal in menu.get("meals", []):
        meal_name = str(meal.get("meal", ""))
        if not (meal_name.startswith("2午餐") or meal_name.startswith("3晚餐")):
            continue

        categories = [dish.get("dish_category") for dish in meal.get("dishes", [])]
        counts = Counter(categories)
        main_count = sum(counts[c] for c in VALID_MAIN_DISH)

        if counts.get("主食", 0) != 1 or main_count != 1 or counts.get("副菜", 0) != 3:
            errors.append(
                f"{meal_name} 結構錯誤：需要 1 主食 + 1 主菜/主餐 + 3 副菜；目前={dict(counts)}"
            )

    if errors:
        raise ValueError("\n".join(errors))


def write_menu_to_sheet(xlsx_path: Path, menu_json: Path, output_path: Path) -> None:
    with menu_json.open("r", encoding="utf-8") as f:
        menu = json.load(f)

    validate_lunch_dinner_structure(menu)

    wb = load_workbook(xlsx_path)
    if "計算" not in wb.sheetnames:
        raise ValueError("Workbook must contain a 計算 sheet")
    ws = wb["計算"]

    # Clear previous input rows conservatively.
    for row in range(6, ws.max_row + 1):
        for col in [1, 2, 3, 4, 8]:
            ws.cell(row=row, column=col).value = None

    row = 6
    for meal in menu.get("meals", []):
        meal_name = meal.get("meal")
        for dish in meal.get("dishes", []):
            dish_name = dish.get("dish_name")
            first = True
            for ing in dish.get("ingredients", []):
                ws.cell(row=row, column=1).value = meal_name
                ws.cell(row=row, column=2).value = dish_name if first else None
                ws.cell(row=row, column=3).value = ing.get("colloquial")
                ws.cell(row=row, column=4).value = ing.get("db_name")
                ws.cell(row=row, column=8).value = float(ing.get("weight_g", 0))
                row += 1
                first = False

    wb.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("xlsx_path")
    parser.add_argument("menu_json")
    parser.add_argument("output_path")
    args = parser.parse_args()
    write_menu_to_sheet(Path(args.xlsx_path), Path(args.menu_json), Path(args.output_path))


if __name__ == "__main__":
    main()
