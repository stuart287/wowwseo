#!/usr/bin/env python3
"""Normalize common technical audit exports into review-ready CSV files."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


SCHEMA_FIELDS = [
    "source_file",
    "sheet_name",
    "url",
    "source_url",
    "target_url",
    "status_code",
    "issue_type",
    "severity_hint",
    "notes",
]

ALIASES = {
    "url": {"url", "address", "page", "final url", "page url"},
    "source_url": {"source", "source url", "from", "origin url"},
    "target_url": {"destination", "target", "redirect url", "to", "final destination"},
    "status_code": {"status code", "status", "http status"},
    "notes": {"notes", "comment", "comments", "details"},
}

ISSUE_RULES = {
    "301 redirects": "redirect",
    "404 errors": "broken_link",
    "redirect chains": "redirect_chain",
    "orphan pages": "orphan_page",
    "duplicate content": "duplicate_content",
    "internal links to http": "http_internal_link",
}


def normalize_header(value: str) -> str:
    return " ".join(value.strip().lower().replace("_", " ").split())


def detect_issue_type(filename: str) -> str:
    label = filename.lower()
    for marker, issue_type in ISSUE_RULES.items():
        if marker in label:
            return issue_type
    return "review_required"


def csv_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        reader = csv.reader(handle)
        rows = [[cell.strip() for cell in row] for row in reader]
    for index, row in enumerate(rows):
        values = [cell for cell in row if cell]
        if len(values) >= 2:
            return row, rows[index + 1 :]
    return [], []


def shared_strings(zf: ZipFile) -> list[str]:
    try:
        xml = zf.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    tree = ET.fromstring(xml)
    strings: list[str] = []
    for node in tree.findall(".//{*}si"):
        strings.append("".join(part.text or "" for part in node.findall(".//{*}t")))
    return strings


def workbook_sheets(zf: ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall(".//{*}Relationship")
    }
    output: list[tuple[str, str]] = []
    for sheet in workbook.findall(".//{*}sheet"):
        rel_id = sheet.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = rel_map.get(rel_id)
        if target:
            output.append((sheet.attrib.get("name", "Sheet"), f"xl/{target}"))
    return output


def sheet_rows(zf: ZipFile, worksheet_path: str, strings: list[str]) -> list[list[str]]:
    tree = ET.fromstring(zf.read(worksheet_path))
    rows: list[list[str]] = []
    for row in tree.findall(".//{*}sheetData/{*}row"):
        values: list[str] = []
        for cell in row.findall("{*}c"):
            cell_type = cell.attrib.get("t")
            value = cell.findtext("{*}v", default="").strip()
            if cell_type == "s" and value.isdigit():
                values.append(strings[int(value)].strip())
            else:
                values.append(value)
        rows.append(values)
    return rows


def xlsx_sheets(path: Path) -> list[tuple[str, list[str], list[list[str]]]]:
    with ZipFile(path) as zf:
        strings = shared_strings(zf)
        output: list[tuple[str, list[str], list[list[str]]]] = []
        for sheet_name, worksheet_path in workbook_sheets(zf):
            rows = sheet_rows(zf, worksheet_path, strings)
            headers: list[str] = []
            body: list[list[str]] = []
            for index, row in enumerate(rows):
                values = [cell for cell in row if cell]
                if len(values) >= 2:
                    headers = row
                    body = rows[index + 1 :]
                    break
            output.append((sheet_name, headers, body))
    return output


def map_headers(headers: list[str]) -> dict[str, int]:
    header_map: dict[str, int] = {}
    for index, header in enumerate(headers):
        normalized = normalize_header(header)
        for schema_field, aliases in ALIASES.items():
            if normalized in aliases and schema_field not in header_map:
                header_map[schema_field] = index
    return header_map


def row_to_record(row: list[str], header_map: dict[str, int], source_file: str, sheet_name: str) -> dict[str, str]:
    record = {field: "" for field in SCHEMA_FIELDS}
    record["source_file"] = source_file
    record["sheet_name"] = sheet_name
    record["issue_type"] = detect_issue_type(source_file)
    for field, index in header_map.items():
        if index < len(row):
            record[field] = row[index].strip()
    return record


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_folder(root: Path) -> int:
    normalized_rows: list[dict[str, str]] = []
    unmapped_rows: list[dict[str, str]] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("~$"):
            continue
        suffix = path.suffix.lower()
        rel = str(path.relative_to(root))

        if suffix == ".csv":
            headers, body = csv_rows(path)
            header_map = map_headers(headers)
            if not header_map or ("url" not in header_map and "source_url" not in header_map and "target_url" not in header_map):
                unmapped_rows.append({"source_file": rel, "sheet_name": "", "reason": "no mappable URL columns"})
                continue
            for row in body:
                normalized_rows.append(row_to_record(row, header_map, rel, "CSV"))
        elif suffix in {".xlsx", ".xlsm"}:
            for sheet_name, headers, body in xlsx_sheets(path):
                header_map = map_headers(headers)
                if not header_map or ("url" not in header_map and "source_url" not in header_map and "target_url" not in header_map):
                    unmapped_rows.append({"source_file": rel, "sheet_name": sheet_name, "reason": "no mappable URL columns"})
                    continue
                for row in body:
                    normalized_rows.append(row_to_record(row, header_map, rel, sheet_name))
        elif suffix == ".xls":
            unmapped_rows.append({"source_file": rel, "sheet_name": "", "reason": "convert .xls to .xlsx or .csv"})

    write_csv(root / "normalized_rows.csv", normalized_rows, SCHEMA_FIELDS)
    write_csv(root / "unmapped_files.csv", unmapped_rows, ["source_file", "sheet_name", "reason"])
    print(f"Wrote {len(normalized_rows)} normalized rows")
    print(f"Wrote {len(unmapped_rows)} unmapped file notes")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: normalize_audit_exports.py <audit-folder>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).expanduser()
    if not root.exists():
        print(f"Folder not found: {root}", file=sys.stderr)
        return 1
    return normalize_folder(root)


if __name__ == "__main__":
    raise SystemExit(main())
