#!/usr/bin/env python3
"""Inventory technical audit source files and spreadsheet schemas."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


def docx_headings(path: Path, limit: int = 80) -> list[str]:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    tree = ET.fromstring(xml)
    lines: list[str] = []
    for para in tree.findall(".//w:p", ns):
        text = "".join(node.text or "" for node in para.findall(".//w:t", ns)).strip()
        if text:
            lines.append(text)
        if len(lines) >= limit:
            break
    return lines


def csv_headers(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        reader = csv.reader(handle)
        for row in reader:
            values = [cell.strip() for cell in row if cell.strip()]
            if values:
                return values
    return []


def shared_strings(zf: ZipFile) -> list[str]:
    try:
        xml = zf.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    tree = ET.fromstring(xml)
    strings: list[str] = []
    for node in tree.findall(".//{*}si"):
        text = "".join(part.text or "" for part in node.findall(".//{*}t"))
        strings.append(text)
    return strings


def workbook_sheets(zf: ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall(".//{*}Relationship")
    }
    sheets: list[tuple[str, str]] = []
    for sheet in workbook.findall(".//{*}sheet"):
        rel_id = sheet.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = rel_map.get(rel_id, "")
        if target:
            sheets.append((sheet.attrib.get("name", "Sheet"), f"xl/{target}"))
    return sheets


def sheet_headers(zf: ZipFile, worksheet_path: str, strings: list[str]) -> list[str]:
    tree = ET.fromstring(zf.read(worksheet_path))
    for row in tree.findall(".//{*}sheetData/{*}row"):
        values: list[str] = []
        for cell in row.findall("{*}c"):
            cell_type = cell.attrib.get("t")
            value = cell.findtext("{*}v", default="").strip()
            if not value:
                continue
            if cell_type == "s" and value.isdigit():
                values.append(strings[int(value)].strip())
            else:
                values.append(value)
        if len([value for value in values if value]) >= 2:
            return values[:20]
    return []


def xlsx_headers(path: Path) -> list[tuple[str, list[str]]]:
    if path.suffix.lower() == ".xlsm":
        # Macro-enabled workbooks still use the XLSX container layout.
        pass

    if path.suffix.lower() not in {".xlsx", ".xlsm"}:
        return [("unsupported workbook type", [])]

    output: list[tuple[str, list[str]]] = []
    with ZipFile(path) as zf:
        strings = shared_strings(zf)
        for sheet_name, worksheet_path in workbook_sheets(zf):
            headers = sheet_headers(zf, worksheet_path, strings)
            output.append((sheet_name, headers))
    return output


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: inventory_audit_sources.py <audit-folder>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).expanduser()
    if not root.exists():
        print(f"Folder not found: {root}", file=sys.stderr)
        return 1

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("~$"):
            continue

        suffix = path.suffix.lower()
        rel = path.relative_to(root)
        if suffix in {".xlsx", ".xlsm"}:
            print(f"\n## {rel}")
            for sheet, headers in xlsx_headers(path):
                print(f"- {sheet}: {', '.join(headers) if headers else 'no obvious header row'}")
        elif suffix == ".xls":
            print(f"\n## {rel}")
            print("- XLS source file (convert to .xlsx or .csv before normalization)")
        elif suffix == ".csv":
            print(f"\n## {rel}")
            headers = csv_headers(path)
            print(f"- CSV: {', '.join(headers[:20]) if headers else 'no obvious header row'}")
        elif suffix == ".docx":
            print(f"\n## {rel}")
            for line in docx_headings(path, limit=30):
                print(f"- {line}")
        elif suffix in {".html", ".pdf"}:
            print(f"\n## {rel}")
            print(f"- {suffix[1:].upper()} source file")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
