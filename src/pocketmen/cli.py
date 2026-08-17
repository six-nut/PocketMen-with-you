from __future__ import annotations

import argparse
import json
from pathlib import Path

from .atlas import make_contact_sheet, validate_atlas, write_validation
from .install import install_pet


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pocketmen", description="PocketMen deterministic Codex-pet utilities")
    sub = p.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate", help="validate a Codex pet atlas")
    v.add_argument("atlas")
    v.add_argument("--json-out")

    c = sub.add_parser("contact-sheet", help="render a QA contact sheet")
    c.add_argument("atlas")
    c.add_argument("--output", required=True)

    i = sub.add_parser("install", help="install a finished pet package locally")
    i.add_argument("package_dir")
    return p


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "validate":
        result = validate_atlas(args.atlas)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if args.json_out:
            write_validation(result, args.json_out)
        return 0 if result["ok"] else 1
    if args.command == "contact-sheet":
        make_contact_sheet(args.atlas, args.output)
        print(Path(args.output).resolve())
        return 0
    if args.command == "install":
        dest = install_pet(args.package_dir)
        print(dest)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
