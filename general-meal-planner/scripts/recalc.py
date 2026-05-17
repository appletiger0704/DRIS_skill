#!/usr/bin/env python3
"""Recalculate Excel formulas using LibreOffice headless mode.

Usage:
  python recalc.py <xlsx_path>

This script requires LibreOffice to be installed in the execution environment.
"""

import argparse
import shutil
import subprocess
from pathlib import Path


def recalc(xlsx_path: Path) -> None:
    soffice = shutil.which("libreoffice") or shutil.which("soffice")
    if not soffice:
        raise RuntimeError("LibreOffice/soffice not found. Install LibreOffice to recalculate formulas.")

    xlsx_path = xlsx_path.resolve()
    out_dir = xlsx_path.parent
    subprocess.run(
        [
            soffice,
            "--headless",
            "--convert-to",
            "xlsx",
            "--outdir",
            str(out_dir),
            str(xlsx_path),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("xlsx_path")
    args = parser.parse_args()
    recalc(Path(args.xlsx_path))


if __name__ == "__main__":
    main()
