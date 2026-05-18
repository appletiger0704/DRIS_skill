#!/usr/bin/env python3
"""Generate patient-tailored candidate dish names from recipe-source notes.

Input is a manually/web collected JSON list. This script does not scrape websites;
it turns cited source notes into structured candidate names that can be adapted
into therapeutic menus.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PATIENT_RULES = {
    "ckd_non_dialysis": {
        "prefix": "低鈉低鉀低磷",
        "avoid": ["濃湯", "高鹽醬汁", "大量堅果", "大量乳酪", "加工醬料", "低鈉鹽"],
        "preferred": ["檸檬", "米醋", "薑", "蔥", "胡椒", "香草", "汆燙瀝乾", "小份量高生物價蛋白質"],
    },
    "general": {"prefix": "均衡", "avoid": [], "preferred": []},
}


def listify(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    return [str(value)] if str(value).strip() else []


def build_candidate(item: dict[str, Any], patient: str) -> dict[str, Any]:
    rules = PATIENT_RULES.get(patient, PATIENT_RULES["general"])
    style = str(item.get("dish_or_style") or item.get("style") or "regional dish")
    region = str(item.get("region", ""))
    flavors = listify(item.get("flavor_notes"))
    techniques = listify(item.get("techniques"))
    flavor_part = "、".join(flavors[:2]) if flavors else "香草酸香"
    technique_part = techniques[0] if techniques else "改良"
    region_part = f"{region}風" if region else ""
    name = f"{rules['prefix']}-{region_part}{flavor_part}-{technique_part}-{style}".replace("--", "-").strip("-")
    return {
        "candidate_name": name,
        "source_type": item.get("source_type", "manual"),
        "source_name": item.get("source_name"),
        "source_url": item.get("source_url"),
        "inspiration": style,
        "keep": flavors[:4] + techniques[:2],
        "remove_or_replace": sorted(set(rules["avoid"] + listify(item.get("risk_notes"))))[:8],
        "patient_adaptation": rules["preferred"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_json")
    parser.add_argument("--patient", default="general", choices=sorted(PATIENT_RULES))
    parser.add_argument("--output")
    args = parser.parse_args()

    payload = json.loads(Path(args.source_json).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("sources", [])
    candidates = [build_candidate(item, args.patient) for item in payload]
    text = json.dumps({"patient": args.patient, "candidates": candidates}, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
