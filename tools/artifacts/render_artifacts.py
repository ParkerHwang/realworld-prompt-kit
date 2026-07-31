#!/usr/bin/env python3
"""Render a v0.2 artifact package to reviewable PNG or text previews."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

try:
    from .validation import ROOT, load_json
except ImportError:  # pragma: no cover - direct script execution
    from validation import ROOT, load_json  # type: ignore


OFFICE_SUFFIXES = {".docx", ".pptx", ".xlsx"}
TEXT_SUFFIXES = {".csv", ".json", ".md", ".txt"}


def _run(command: list[str]) -> None:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"{' '.join(command)} failed: {detail}")


def _render_pdf(pdf_path: Path, output_dir: Path, stem: str) -> list[Path]:
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm is None:
        raise RuntimeError("pdftoppm is required to render PDF pages")
    target_dir = output_dir / stem
    target_dir.mkdir(parents=True, exist_ok=True)
    prefix = target_dir / "page"
    _run([pdftoppm, "-png", "-r", "144", str(pdf_path), str(prefix)])
    return sorted(target_dir.glob("page-*.png"))


def _office_to_pdf(path: Path, scratch: Path) -> Path:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice is None:
        raise RuntimeError("LibreOffice is required to render Office files")
    _run(
        [
            soffice,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(scratch),
            str(path),
        ]
    )
    pdf_path = scratch / f"{path.stem}.pdf"
    if not pdf_path.is_file():
        raise RuntimeError(f"LibreOffice did not create {pdf_path.name}")
    return pdf_path


def _write_text_preview(path: Path, output_dir: Path) -> list[Path]:
    target_dir = output_dir / path.stem
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "preview.txt"
    if path.suffix.lower() == ".json":
        value: Any = json.loads(path.read_text(encoding="utf-8"))
        text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    else:
        text = path.read_text(encoding="utf-8")
    target.write_text(text.rstrip() + "\n", encoding="utf-8")
    return [target]


def render(path: Path, output_dir: Path) -> list[Path]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _render_pdf(path, output_dir, path.stem)
    if suffix in OFFICE_SUFFIXES:
        with tempfile.TemporaryDirectory(prefix="rwpk-render-") as scratch_name:
            pdf_path = _office_to_pdf(path, Path(scratch_name))
            return _render_pdf(pdf_path, output_dir, path.stem)
    if suffix in TEXT_SUFFIXES:
        return _write_text_preview(path, output_dir)
    raise RuntimeError(f"unsupported artifact type: {path.suffix}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path)
    parser.add_argument("--reference", action="store_true")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.reference == (args.artifact_dir is not None):
        raise SystemExit("choose exactly one of --reference or --artifact-dir")

    scenario_path = (
        args.scenario if args.scenario.is_absolute() else ROOT / args.scenario
    )
    scenario = load_json(scenario_path)
    output_dir = (
        args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    rendered: list[Path] = []
    for output in scenario["artifact_contract"]["outputs"]:
        if args.reference:
            artifact_path = ROOT / output["reference_path"]
        else:
            artifact_dir = (
                args.artifact_dir
                if args.artifact_dir.is_absolute()
                else ROOT / args.artifact_dir
            )
            artifact_path = artifact_dir / output["filename"]
        if not artifact_path.is_file():
            raise SystemExit(f"missing artifact: {artifact_path}")
        rendered.extend(render(artifact_path, output_dir))

    print(f"rendered {len(rendered)} previews to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
