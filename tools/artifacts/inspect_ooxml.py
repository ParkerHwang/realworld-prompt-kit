#!/usr/bin/env python3
"""Dependency-free structural inspection for v0.2 artifact files."""

from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


DOCX_MIME = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
PPTX_MIME = (
    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
)
XLSX_MIME = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

MEDIA_TYPES = {
    ".docx": DOCX_MIME,
    ".pptx": PPTX_MIME,
    ".xlsx": XLSX_MIME,
    ".pdf": "application/pdf",
    ".json": "application/json",
    ".csv": "text/csv",
    ".txt": "text/plain",
}


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _xml(path: str, payload: bytes) -> ElementTree.Element:
    try:
        return ElementTree.fromstring(payload)
    except ElementTree.ParseError as exc:
        raise ValueError(f"{path}: invalid XML: {exc}") from exc


def _text_from_xml(root: ElementTree.Element) -> list[str]:
    values: list[str] = []
    for element in root.iter():
        if _local_name(element.tag) in {"t", "v"} and element.text:
            values.append(element.text)
    return values


def _zip_payloads(path: Path) -> dict[str, bytes]:
    try:
        with zipfile.ZipFile(path) as archive:
            bad_member = archive.testzip()
            if bad_member is not None:
                raise ValueError(f"corrupt ZIP member {bad_member}")
            return {name: archive.read(name) for name in archive.namelist()}
    except (OSError, zipfile.BadZipFile) as exc:
        raise ValueError(f"invalid ZIP package: {exc}") from exc


def _inspect_docx(path: Path) -> dict[str, Any]:
    payloads = _zip_payloads(path)
    required = {"[Content_Types].xml", "word/document.xml"}
    missing = sorted(required - set(payloads))
    if missing:
        raise ValueError(f"missing DOCX parts: {missing}")
    document = _xml("word/document.xml", payloads["word/document.xml"])
    text = _text_from_xml(document)
    paragraph_count = sum(_local_name(node.tag) == "p" for node in document.iter())
    table_count = sum(_local_name(node.tag) == "tbl" for node in document.iter())
    heading_count = 0
    for node in document.iter():
        if _local_name(node.tag) != "pStyle":
            continue
        value = next(
            (
                attr_value
                for attr_name, attr_value in node.attrib.items()
                if _local_name(attr_name) == "val"
            ),
            "",
        )
        if value.casefold().startswith("heading"):
            heading_count += 1
    features = {"editable_text"} if text else set()
    if heading_count:
        features.add("headings")
    if table_count:
        features.add("tables")
    return {
        "media_type": DOCX_MIME,
        "parseable": True,
        "features": sorted(features),
        "paragraph_count": paragraph_count,
        "heading_count": heading_count,
        "table_count": table_count,
        "text": "\n".join(text),
    }


def _inspect_pptx(path: Path) -> dict[str, Any]:
    payloads = _zip_payloads(path)
    required = {"[Content_Types].xml", "ppt/presentation.xml"}
    missing = sorted(required - set(payloads))
    if missing:
        raise ValueError(f"missing PPTX parts: {missing}")
    slide_names = sorted(
        name
        for name in payloads
        if re.fullmatch(r"ppt/slides/slide[0-9]+\.xml", name)
    )
    chart_names = sorted(
        name
        for name in payloads
        if re.search(r"(?:^|/)charts/chart[0-9]+\.xml$", name)
    )
    notes_names = sorted(
        name
        for name in payloads
        if re.fullmatch(r"ppt/notesSlides/notesSlide[0-9]+\.xml", name)
    )
    text: list[str] = []
    table_count = 0
    for name in slide_names:
        root = _xml(name, payloads[name])
        text.extend(_text_from_xml(root))
        table_count += sum(_local_name(node.tag) == "tbl" for node in root.iter())
    features = {"slides"} if slide_names else set()
    if text:
        features.add("editable_text")
    if chart_names:
        features.add("charts")
    if table_count:
        features.add("tables")
    return {
        "media_type": PPTX_MIME,
        "parseable": True,
        "features": sorted(features),
        "slide_count": len(slide_names),
        "chart_count": len(chart_names),
        "notes_count": len(notes_names),
        "table_count": table_count,
        "text": "\n".join(text),
    }


def _inspect_xlsx(path: Path) -> dict[str, Any]:
    payloads = _zip_payloads(path)
    required = {"[Content_Types].xml", "xl/workbook.xml"}
    missing = sorted(required - set(payloads))
    if missing:
        raise ValueError(f"missing XLSX parts: {missing}")
    workbook = _xml("xl/workbook.xml", payloads["xl/workbook.xml"])
    sheet_names = [
        next(
            (
                attr_value
                for attr_name, attr_value in node.attrib.items()
                if _local_name(attr_name) == "name"
            ),
            "",
        )
        for node in workbook.iter()
        if _local_name(node.tag) == "sheet"
    ]
    worksheet_names = sorted(
        name
        for name in payloads
        if re.fullmatch(r"xl/worksheets/sheet[0-9]+\.xml", name)
    )
    shared_strings: list[str] = []
    if "xl/sharedStrings.xml" in payloads:
        shared_root = _xml("xl/sharedStrings.xml", payloads["xl/sharedStrings.xml"])
        shared_strings = _text_from_xml(shared_root)
    text = list(shared_strings)
    formula_count = 0
    for name in worksheet_names:
        root = _xml(name, payloads[name])
        formula_count += sum(_local_name(node.tag) == "f" for node in root.iter())
        text.extend(_text_from_xml(root))
    chart_count = sum(
        bool(re.search(r"(?:^|/)charts/chart[0-9]+\.xml$", name))
        for name in payloads
    )
    table_count = sum(name.startswith("xl/tables/table") for name in payloads)
    features = {"worksheets", "editable_cells"} if sheet_names else set()
    if formula_count:
        features.add("formulas")
    if chart_count:
        features.add("charts")
    if table_count:
        features.add("tables")
    return {
        "media_type": XLSX_MIME,
        "parseable": True,
        "features": sorted(features),
        "sheet_names": sheet_names,
        "worksheet_count": len(sheet_names),
        "formula_count": formula_count,
        "chart_count": chart_count,
        "table_count": table_count,
        "text": "\n".join(text),
    }


def _inspect_pdf(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    if not payload.startswith(b"%PDF-"):
        raise ValueError("missing PDF header")
    if b"%%EOF" not in payload[-4096:]:
        raise ValueError("missing PDF EOF marker")
    page_count = len(re.findall(rb"/Type\s*/Page\b", payload))
    return {
        "media_type": "application/pdf",
        "parseable": True,
        "features": ["pages"],
        "page_count": page_count,
        "text": "",
    }


def _inspect_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    features = ["json_object"] if isinstance(value, dict) else ["json_array"]
    if isinstance(value, dict) and isinstance(value.get("files"), list):
        features.append("file_manifest")
    return {
        "media_type": "application/json",
        "parseable": True,
        "features": features,
        "json_keys": sorted(value) if isinstance(value, dict) else [],
        "json_value": value,
        "text": json.dumps(value, ensure_ascii=False, sort_keys=True),
    }


def _inspect_csv(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise ValueError("CSV is empty")
    return {
        "media_type": "text/csv",
        "parseable": True,
        "features": ["tabular_text"],
        "row_count": max(0, len(rows) - 1),
        "column_count": len(rows[0]),
        "text": "\n".join(",".join(row) for row in rows),
    }


def _inspect_text(path: Path) -> dict[str, Any]:
    value = path.read_text(encoding="utf-8")
    if not value.strip():
        raise ValueError("text file is empty")
    return {
        "media_type": "text/plain",
        "parseable": True,
        "features": ["text"],
        "text": value,
    }


def inspect_artifact(path: Path) -> dict[str, Any]:
    path = path.resolve()
    if not path.is_file():
        return {
            "path": str(path),
            "parseable": False,
            "error": "file does not exist",
            "features": [],
            "text": "",
        }
    suffix = path.suffix.lower()
    try:
        if suffix == ".docx":
            result = _inspect_docx(path)
        elif suffix == ".pptx":
            result = _inspect_pptx(path)
        elif suffix == ".xlsx":
            result = _inspect_xlsx(path)
        elif suffix == ".pdf":
            result = _inspect_pdf(path)
        elif suffix == ".json":
            result = _inspect_json(path)
        elif suffix == ".csv":
            result = _inspect_csv(path)
        elif suffix == ".txt":
            result = _inspect_text(path)
        else:
            raise ValueError(f"unsupported extension {suffix!r}")
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        return {
            "path": str(path),
            "media_type": MEDIA_TYPES.get(suffix, "application/octet-stream"),
            "parseable": False,
            "error": str(exc),
            "features": [],
            "text": "",
        }
    result["path"] = str(path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    result = inspect_artifact(args.path)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("parseable") else 1


if __name__ == "__main__":
    raise SystemExit(main())
