from __future__ import annotations

import argparse
import json
from pathlib import Path

from .atlas import make_contact_sheet, validate_atlas, write_validation
from .backends import BACKENDS
from .hardware import doctor_json
from .install import install_pet
from .pipeline import ENGINE_CHOICES, QUALITY_CHOICES, SUBJECT_TYPES, create_pet
from .styles import STYLE_PRESETS


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pocketmen", description="PocketMen local/neural Codex-pet toolkit")
    sub = p.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="create a Codex pet from 2+ reference images")
    create.add_argument("--reference", action="append", required=True, help="reference image path; repeat 2+ times")
    create.add_argument("--name", required=True)
    create.add_argument("--pet-id")
    create.add_argument("--style", default="auto", choices=STYLE_PRESETS)
    create.add_argument("--subject-type", default="auto", choices=SUBJECT_TYPES)
    create.add_argument("--identity-notes", help="stable visible identity details prepared from the reference images")
    create.add_argument("--description")
    create.add_argument("--prefer-reference", help="use this supplied reference as the deterministic canonical cutout")
    create.add_argument("--engine", default="auto", choices=ENGINE_CHOICES)
    create.add_argument("--backend", default="auto", choices=BACKENDS)
    create.add_argument("--quality", default="balanced", choices=QUALITY_CHOICES)
    create.add_argument("--seed", type=int, default=42)
    create.add_argument("--no-cpu-offload", action="store_true")
    create.add_argument("--no-neural-fallback", action="store_true")
    create.add_argument("--output", required=True)
    create.add_argument("--install", action="store_true")

    sub.add_parser("doctor", help="report local hardware and the recommended PocketMen engine")

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
    if args.command == "doctor":
        print(doctor_json())
        return 0
    if args.command == "create":
        summary = create_pet(
            args.reference,
            name=args.name,
            pet_id=args.pet_id,
            style=args.style,
            subject_type=args.subject_type,
            identity_notes=args.identity_notes,
            description=args.description,
            output_dir=args.output,
            preferred_reference=args.prefer_reference,
            engine=args.engine,
            backend=args.backend,
            quality=args.quality,
            seed=args.seed,
            cpu_offload=not args.no_cpu_offload,
            neural_fallback=not args.no_neural_fallback,
        )
        if args.install:
            package_dir = Path(args.output).expanduser().resolve() / "package" / summary["pet_id"]
            summary["installed_to"] = str(install_pet(package_dir))
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0 if summary["ok"] else 1
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
