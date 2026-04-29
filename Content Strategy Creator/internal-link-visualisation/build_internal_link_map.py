#!/usr/bin/env python3
"""Build a standalone internal-link network visualisation from an Ahrefs export."""

from __future__ import annotations

import csv
import html
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse, urlunparse


CLIENTS = [
    {
        "name": "United Telecoms",
        "domain": "unitedtelecoms.co.za",
        "input": Path(
            "/Users/stuartmarsden/Downloads/"
            "united-telecoms-za_07-apr-2026_links_2026-04-21_11-12-46.csv"
        ),
        "output": Path(__file__).with_name("united-telecoms-internal-link-map.html"),
    },
    {
        "name": "Baracuda",
        "domain": "baracuda.co.za",
        "input": Path(
            "/Users/stuartmarsden/Downloads/"
            "baracuda.co_21-apr-2026_links_2026-04-21_12-48-20.csv"
        ),
        "output": Path(__file__).with_name("baracuda-internal-link-map.html"),
    },
    {
        "name": "Food Label Maker",
        "domain": "foodlabelmaker.com",
        "input": Path(
            "/Users/stuartmarsden/Downloads/"
            "food-label-maker_24-apr-2026_links_2026-04-29_21-53-49.csv"
        ),
        "output": Path(__file__).with_name("food-label-maker-internal-link-map.html"),
    },
]

INPUT = CLIENTS[0]["input"]
OUTPUT = CLIENTS[0]["output"]
DOMAIN = CLIENTS[0]["domain"]
CLIENT_NAME = CLIENTS[0]["name"]
INDEX_OUTPUT = Path(__file__).with_name("index.html")
PUBLIC_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "public" / "internal-link-visualisation"


def canonical_url(raw_url: str) -> str:
    parsed = urlparse((raw_url or "").strip())
    if not parsed.scheme or not parsed.netloc:
        return ""

    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]

    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]

    return urlunparse((parsed.scheme.lower(), netloc, path, "", "", ""))


def path_group(url: str) -> str:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    return "/" + (parts[0] if parts else "home")


def page_label(url: str) -> str:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        return "Homepage"
    return parts[-1].replace("-", " ").replace("_", " ").title()


def normalize_anchor(anchor: str) -> str:
    return re.sub(r"\s+", " ", (anchor or "").strip()).lower()


GENERIC_COMPONENT_ANCHORS = {
    "read more",
    "read full post",
    "learn more",
    "view more",
    "view product",
    "view products",
    "shop now",
    "see more",
    "find out more",
    "discover more",
    "continue reading",
    "read article",
    "read post",
}


def normalized_page_label(url: str) -> str:
    return normalize_anchor(page_label(url))


def build_graph() -> dict:
    edge_counts: Counter[tuple[str, str]] = Counter()
    anchors: defaultdict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    in_counts: Counter[str] = Counter()
    out_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    source_pages: set[str] = set()
    target_source_pages: defaultdict[str, set[str]] = defaultdict(set)
    anchor_source_pages: defaultdict[tuple[str, str], set[str]] = defaultdict(set)
    edge_anchor_keys: defaultdict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
    source_noindex_by_url: dict[str, bool] = {}
    target_noindex_by_url: dict[str, bool] = {}
    source_status_by_url: dict[str, str] = {}
    target_status_by_url: dict[str, str] = {}
    edge_noindex: dict[tuple[str, str], dict[str, bool]] = {}
    edge_status: dict[tuple[str, str], dict[str, str]] = {}

    row_count = 0
    retained_count = 0
    self_ref_count = 0

    with INPUT.open("r", encoding="utf-16", newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")
        for row in reader:
            row_count += 1
            source = canonical_url(row.get("Source URL", ""))
            target = canonical_url(row.get("Target URL", ""))
            if not source or not target:
                continue

            target_host = urlparse(target).netloc
            is_internal = row.get("Is source internal") == "true" and target_host == DOMAIN
            target_is_html_page = "HTML Page" in (row.get("Target URL type") or "")
            if not is_internal or not target_is_html_page:
                continue

            if source == target or row.get("Is link self-referencing") == "true":
                self_ref_count += 1
                continue

            edge_key = (source, target)
            edge_counts[edge_key] += 1
            source_pages.add(source)
            target_source_pages[target].add(source)
            source_noindex = row.get("Is source noindex") == "true"
            target_noindex = row.get("Is target noindex") == "true"
            source_status = (row.get("Source HTTP status code") or "").strip()
            target_status = (row.get("Target HTTP status code") or "").strip()
            source_noindex_by_url[source] = source_noindex
            target_noindex_by_url[target] = target_noindex
            source_status_by_url[source] = source_status
            target_status_by_url[target] = target_status
            edge_noindex[edge_key] = {
                "sourceNoindex": source_noindex,
                "targetNoindex": target_noindex,
            }
            edge_status[edge_key] = {
                "sourceStatusCode": source_status,
                "targetStatusCode": target_status,
            }
            anchor = (row.get("Anchor") or "").strip()
            if anchor:
                anchors[edge_key][anchor] += 1
                anchor_key = (target, normalize_anchor(anchor))
                anchor_source_pages[anchor_key].add(source)
                edge_anchor_keys[edge_key].add(anchor_key)
            out_counts[source] += 1
            in_counts[target] += 1
            retained_count += 1

    urls = sorted(set(in_counts) | set(out_counts))
    nodes = []
    source_page_count = len(source_pages)
    for index, url in enumerate(urls):
        group = path_group(url)
        source_coverage_count = len(target_source_pages[url])
        source_coverage_share = (
            source_coverage_count / source_page_count if source_page_count else 0
        )
        status_counts[group] += 1
        nodes.append(
            {
                "id": url,
                "label": page_label(url),
                "path": urlparse(url).path or "/",
                "group": group,
                "in": in_counts[url],
                "out": out_counts[url],
                "degree": in_counts[url] + out_counts[url],
                "targetSourcePages": source_coverage_count,
                "targetSourceShare": source_coverage_share,
                "sourceNoindex": source_noindex_by_url.get(url, False),
                "targetNoindex": target_noindex_by_url.get(url, False),
                "sourceStatusCode": source_status_by_url.get(url, ""),
                "targetStatusCode": target_status_by_url.get(url, ""),
                "index": index,
            }
        )

    edges = []
    for (source, target), count in edge_counts.items():
        target_coverage_count = len(target_source_pages[target])
        target_coverage_share = (
            target_coverage_count / source_page_count if source_page_count else 0
        )
        normalized_target_label = normalized_page_label(target)
        anchor_texts = [text for text, _anchor_count in anchors[(source, target)].most_common(5)]
        generic_anchor = any(
            normalize_anchor(text) in GENERIC_COMPONENT_ANCHORS for text in anchor_texts
        )
        label_like_anchor = any(
            normalize_anchor(text) == normalized_target_label for text in anchor_texts
        )
        anchor_shares = [
            len(anchor_source_pages[anchor_key]) / source_page_count
            for anchor_key in edge_anchor_keys[(source, target)]
        ]
        anchor_source_share = min(anchor_shares) if anchor_shares else 0
        top_anchors = [
            {"text": text, "count": anchor_count}
            for text, anchor_count in anchors[(source, target)].most_common(5)
        ]
        edges.append(
            {
                "source": source,
                "target": target,
                "count": count,
                "targetSourcePages": target_coverage_count,
                "targetSourceShare": target_coverage_share,
                "anchorSourceShare": anchor_source_share,
                "genericAnchor": generic_anchor,
                "labelLikeAnchor": label_like_anchor,
                "sourceNoindex": edge_noindex[(source, target)]["sourceNoindex"],
                "targetNoindex": edge_noindex[(source, target)]["targetNoindex"],
                "sourceStatusCode": edge_status[(source, target)]["sourceStatusCode"],
                "targetStatusCode": edge_status[(source, target)]["targetStatusCode"],
                "anchors": top_anchors,
            }
        )

    source_group_counts: defaultdict[tuple[str, str], int] = defaultdict(int)
    for edge in edges:
        if edge["genericAnchor"] or edge["labelLikeAnchor"]:
            source_group_counts[(edge["source"], path_group(edge["target"]))] += 1

    for edge in edges:
        source_group_total = source_group_counts[(edge["source"], path_group(edge["target"]))]
        edge["componentLike"] = edge["genericAnchor"] or (
            edge["labelLikeAnchor"] and source_group_total >= 3
        )

    edges.sort(key=lambda edge: edge["count"], reverse=True)
    nodes.sort(key=lambda node: node["degree"], reverse=True)

    return {
        "meta": {
            "sourceFile": str(INPUT),
            "domain": DOMAIN,
            "clientName": CLIENT_NAME,
            "rowsRead": row_count,
            "linksRetained": retained_count,
            "selfReferencesExcluded": self_ref_count,
            "sourcePages": source_page_count,
            "uniquePages": len(nodes),
            "uniqueEdges": len(edges),
            "groups": status_counts.most_common(),
            "sourceStatusCodes": sorted(
                {code for code in source_status_by_url.values() if code},
                key=lambda value: (len(value), value),
            ),
            "targetStatusCodes": sorted(
                {code for code in target_status_by_url.values() if code},
                key=lambda value: (len(value), value),
            ),
            "importType": "ahrefs",
        },
        "nodes": nodes,
        "edges": edges,
    }


def render_html(graph: dict) -> str:
    data_json = json.dumps(graph, ensure_ascii=True, separators=(",", ":"))
    escaped_source = html.escape(graph["meta"]["sourceFile"])
    escaped_client = html.escape(graph["meta"]["clientName"])
    node_limit_default = min(180, graph["meta"]["uniquePages"])
    node_limit_max = max(40, graph["meta"]["uniquePages"])

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escaped_client} Internal Link Map</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f5;
      --panel: #ffffff;
      --panel-soft: #fbfbfa;
      --ink: #111314;
      --muted: #687076;
      --faint: #8c949b;
      --line: #e4e4e0;
      --line-strong: #d2d2cc;
      --teal: #0f766e;
      --blue: #2563eb;
      --red: #b83a3a;
      --gold: #b7791f;
      --green: #2f855a;
      --violet: #6b46c1;
      --shadow: 0 18px 50px rgb(17 19 20 / 10%);
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.45 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    header {{
      position: sticky;
      top: 0;
      z-index: 4;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      align-items: end;
      gap: 18px;
      padding: 18px clamp(18px, 3vw, 34px) 16px;
      border-bottom: 1px solid var(--line);
      background: rgb(247 247 245 / 92%);
      backdrop-filter: blur(18px);
    }}

    h1 {{
      margin: 0;
      font-size: clamp(28px, 4vw, 48px);
      line-height: .96;
      letter-spacing: 0;
    }}

    .subtitle {{
      max-width: 840px;
      margin: 10px 0 0;
      color: var(--muted);
      font-size: 14px;
    }}

    .subtitle code {{
      color: var(--ink);
      font-family: var(--mono);
      font-size: 12px;
      background: #ecece8;
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 2px 6px;
    }}

    .index-link {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 36px;
      padding: 0 14px;
      border: 1px solid var(--line-strong);
      border-radius: 999px;
      color: var(--ink);
      background: white;
      text-decoration: none;
      font-weight: 750;
      white-space: nowrap;
      box-shadow: 0 4px 14px rgb(17 19 20 / 5%);
    }}

    .overview-band {{
      display: grid;
      grid-template-columns: minmax(0, 1.9fr) minmax(320px, .95fr);
      gap: 1px;
      padding: 0 clamp(18px, 3vw, 34px);
      background: var(--line);
      border-bottom: 1px solid var(--line);
    }}

    .overview-card {{
      display: grid;
      align-content: start;
      gap: 14px;
      padding: 18px 18px 16px;
      background: var(--panel);
    }}

    .overview-card h2 {{
      margin: 0 0 12px;
      font-size: 14px;
    }}

    .guide-columns {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }}

    .metrics-inline {{
      display: grid;
      grid-template-columns: repeat(5, minmax(120px, 1fr));
      gap: 1px;
      margin-top: 14px;
      background: var(--line);
      border: 1px solid var(--line);
    }}

    .guide-step {{
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel-soft);
    }}

    .guide-step strong {{
      display: block;
      margin-bottom: 4px;
      font-size: 12px;
    }}

    .guide-step span,
    .preset-card p,
    .preset-list,
    .metric-note {{
      color: var(--muted);
      font-size: 12px;
    }}

    .preset-card {{
      gap: 10px;
    }}

    .preset-card h3 {{
      margin: 0;
      font-size: 18px;
    }}

    .preset-header {{
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: start;
      gap: 12px;
    }}

    .preset-nav {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .icon-button {{
      width: 34px;
      min-width: 34px;
      min-height: 34px;
      padding: 0;
      border: 1px solid var(--line-strong);
      border-radius: 999px;
      background: white;
      color: var(--ink);
      font-size: 18px;
      line-height: 1;
      font-weight: 700;
      cursor: pointer;
    }}

    .preset-counter {{
      color: var(--muted);
      font-family: var(--mono);
      font-size: 12px;
    }}

    .preset-list {{
      margin: 0;
      padding-left: 16px;
    }}

    .preset-list li + li {{
      margin-top: 4px;
    }}

    .metric {{
      min-width: 0;
      padding: 14px 12px 13px;
      background: var(--panel-soft);
      border: 0;
      border-radius: 0;
      box-shadow: none;
    }}

    .metric strong {{
      display: block;
      font-family: var(--mono);
      font-size: 20px;
      line-height: 1.1;
      letter-spacing: 0;
    }}

    .metric span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
    }}

    .metric-note {{
      display: block;
      margin-top: 5px;
      line-height: 1.35;
    }}

    .import-bar {{
      display: grid;
      grid-template-columns: minmax(280px, 1fr) minmax(320px, 1fr);
      gap: 12px;
      padding: 14px clamp(18px, 3vw, 34px);
      border-bottom: 1px solid var(--line);
      background: #fcfcfa;
    }}

    main {{
      display: grid;
      grid-template-columns: minmax(300px, 360px) minmax(0, 1fr);
      min-height: calc(100vh - 178px);
    }}

    .workspace {{
      display: grid;
      grid-template-rows: minmax(560px, 1fr) auto;
      min-height: 0;
      min-width: 0;
    }}

    .canvas-shell {{
      display: grid;
      grid-template-columns: minmax(0, 1fr);
      min-height: 0;
      min-width: 0;
    }}

    .canvas-shell.summary-active {{
      grid-template-columns: minmax(0, 1fr) minmax(300px, 360px);
    }}

    aside {{
      border-right: 1px solid var(--line);
      background: #fdfdfb;
      padding: 18px 16px 22px;
      overflow: auto;
    }}

    .control {{
      margin-bottom: 16px;
    }}

    label {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 7px;
      font-weight: 760;
      font-size: 13px;
    }}

    label span {{
      color: var(--muted);
      font-weight: 600;
    }}

    input[type="range"], select {{
      width: 100%;
      accent-color: var(--teal);
    }}

    input[type="checkbox"] {{
      accent-color: var(--teal);
    }}

    select, input[type="search"] {{
      min-height: 42px;
      border: 1px solid var(--line-strong);
      border-radius: 8px;
      padding: 8px 11px;
      background: white;
      color: var(--ink);
      box-shadow: 0 1px 0 rgb(17 19 20 / 3%);
    }}

    select:focus, input[type="search"]:focus {{
      outline: 2px solid rgb(15 118 110 / 18%);
      border-color: var(--teal);
    }}

    input[type="search"] {{
      width: 100%;
    }}

    .search-stack {{
      display: grid;
      gap: 8px;
    }}

    .search-suggestions {{
      display: none;
      gap: 6px;
      padding: 8px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
    }}

    .search-suggestions.active {{
      display: grid;
    }}

    .suggestion-item {{
      width: 100%;
      min-height: 0;
      padding: 8px 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel-soft);
      color: var(--ink);
      text-align: left;
      font-weight: 650;
      cursor: pointer;
    }}

    .suggestion-item small {{
      display: block;
      margin-top: 3px;
      color: var(--muted);
      font-size: 11px;
      font-weight: 500;
    }}

    button {{
      width: 100%;
      min-height: 42px;
      border: 0;
      border-radius: 8px;
      background: var(--ink);
      color: white;
      font-weight: 780;
      cursor: pointer;
    }}

    .toggle {{
      display: grid;
      grid-template-columns: auto 1fr;
      align-items: start;
      gap: 9px;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
    }}

    .toggle input {{
      margin-top: 3px;
    }}

    .toggle strong {{
      display: block;
      font-size: 13px;
    }}

    .toggle span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
    }}

    .hint {{
      margin-top: 7px;
      color: var(--muted);
      font-size: 12px;
    }}

    .import-panel {{
      display: grid;
      gap: 10px;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
      min-width: 0;
    }}

    .import-panel h2 {{
      margin: 0;
      font-size: 13px;
    }}

    .upload-row {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 8px;
      align-items: center;
    }}

    .upload-pick {{
      position: relative;
      overflow: hidden;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 42px;
      padding: 0 14px;
      border: 1px solid var(--line-strong);
      border-radius: 8px;
      background: white;
      color: var(--ink);
      font-weight: 760;
      cursor: pointer;
      white-space: nowrap;
    }}

    .upload-pick input {{
      position: absolute;
      inset: 0;
      opacity: 0;
      cursor: pointer;
    }}

    .import-url {{
      width: 100%;
      min-height: 42px;
      border: 1px solid var(--line-strong);
      border-radius: 8px;
      padding: 8px 11px;
      background: white;
      color: var(--ink);
      box-shadow: 0 1px 0 rgb(17 19 20 / 3%);
    }}

    .import-url:focus {{
      outline: 2px solid rgb(15 118 110 / 18%);
      border-color: var(--teal);
    }}

    .secondary-button {{
      width: 100%;
      min-height: 38px;
      border: 1px solid var(--line-strong);
      border-radius: 8px;
      background: white;
      color: var(--ink);
      font-weight: 730;
      cursor: pointer;
    }}

    .legend {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 20px;
      padding-top: 16px;
      border-top: 1px solid var(--line);
    }}

    .legend-item {{
      display: flex;
      align-items: center;
      min-width: 0;
      gap: 7px;
      color: var(--muted);
      font-size: 12px;
    }}

    .swatch {{
      width: 12px;
      height: 12px;
      border-radius: 50%;
      flex: 0 0 12px;
    }}

    .top-list {{
      margin-top: 22px;
    }}

    .top-list h2 {{
      font-size: 14px;
      margin: 0 0 10px;
    }}

    .page-row {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px;
      padding: 10px 0;
      border-top: 1px solid var(--line);
      cursor: pointer;
    }}

    .page-row:hover strong {{
      color: var(--teal);
    }}

    .page-row strong {{
      min-width: 0;
      overflow-wrap: anywhere;
      font-size: 12px;
    }}

    .page-row span {{
      color: var(--muted);
      font-size: 12px;
    }}

    .stage {{
      position: relative;
      min-height: 640px;
      min-width: 0;
      overflow: hidden;
      background:
        linear-gradient(rgb(17 19 20 / 4%) 1px, transparent 1px),
        linear-gradient(90deg, rgb(17 19 20 / 4%) 1px, transparent 1px),
        radial-gradient(circle at 18% 12%, rgb(15 118 110 / 8%), transparent 30%),
        radial-gradient(circle at 86% 18%, rgb(37 99 235 / 6%), transparent 28%),
        #fafaf8;
      background-size: 36px 36px, 36px 36px, auto, auto, auto;
    }}

    .match-summary {{
      display: none;
      border-left: 1px solid var(--line);
      background: #fdfdfb;
      padding: 16px;
      overflow: auto;
      min-width: 0;
    }}

    .canvas-shell.summary-active .match-summary {{
      display: block;
    }}

    .match-summary h2 {{
      margin: 0 0 4px;
      font-size: 15px;
    }}

    .match-summary p {{
      margin: 0 0 12px;
      color: var(--muted);
      font-size: 12px;
    }}

    .summary-group + .summary-group {{
      margin-top: 16px;
    }}

    .summary-group h3 {{
      margin: 0 0 8px;
      font-size: 12px;
    }}

    .summary-table {{
      display: grid;
      gap: 8px;
    }}

    .summary-row {{
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
      display: grid;
      gap: 4px;
    }}

    .summary-row strong {{
      font-size: 12px;
      overflow-wrap: anywhere;
    }}

    .summary-row span {{
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }}

    .summary-empty {{
      padding: 16px;
      border: 1px dashed var(--line-strong);
      border-radius: 8px;
      color: var(--muted);
      font-size: 12px;
      background: rgb(255 255 255 / 60%);
    }}

    canvas {{
      display: block;
      width: 100%;
      height: 100%;
    }}

    .tooltip {{
      position: absolute;
      z-index: 2;
      width: min(380px, calc(100% - 32px));
      padding: 14px;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: rgb(255 255 255 / 94%);
      box-shadow: var(--shadow);
      pointer-events: none;
      opacity: 0;
      transform: translate(12px, 12px);
      backdrop-filter: blur(18px);
    }}

    .tooltip.pinned {{
      pointer-events: auto;
    }}

    .focus-panel {{
      position: absolute;
      z-index: 1;
      top: 14px;
      left: 14px;
      width: min(520px, calc(100% - 28px));
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgb(255 255 255 / 90%);
      box-shadow: var(--shadow);
      display: none;
      backdrop-filter: blur(18px);
    }}

    .focus-panel-header {{
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: start;
      gap: 10px;
    }}

    .focus-close {{
      width: 28px;
      min-height: 28px;
      border: 1px solid var(--line);
      border-radius: 50%;
      background: white;
      color: var(--ink);
      font-size: 18px;
      line-height: 1;
      font-weight: 700;
    }}

    .focus-panel strong {{
      display: block;
      font-size: 13px;
      margin-bottom: 2px;
    }}

    .focus-panel p {{
      margin: 0 0 8px;
      color: var(--muted);
      font-size: 12px;
    }}

    .focus-chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}

    .focus-chip {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 1px solid rgb(184 58 58 / 28%);
      border-radius: 999px;
      background: rgb(184 58 58 / 8%);
      color: var(--ink);
      padding: 8px 12px;
      min-height: 38px;
      font-size: 12px;
      font-weight: 700;
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      cursor: pointer;
    }}

    .tooltip strong {{
      display: block;
      margin-bottom: 4px;
      overflow-wrap: anywhere;
    }}

    .tooltip a {{
      color: var(--blue);
      overflow-wrap: anywhere;
      pointer-events: auto;
      text-underline-offset: 3px;
    }}

    .tooltip .small {{
      margin-top: 7px;
      color: var(--muted);
      font-size: 12px;
    }}

    .tooltip ul {{
      margin: 8px 0 0;
      padding-left: 16px;
      color: var(--muted);
      font-size: 12px;
    }}

    .tooltip li + li {{
      margin-top: 4px;
    }}

    .empty {{
      position: absolute;
      inset: 0;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 30px;
      text-align: center;
      color: var(--muted);
    }}

    .recommendations-shell {{
      border-top: 1px solid var(--line);
      background: #fcfcfa;
      padding: 16px 18px 20px;
    }}

    .recommendations-header {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 12px;
      align-items: end;
      margin-bottom: 14px;
    }}

    .recommendations-header h2 {{
      margin: 0;
      font-size: 16px;
    }}

    .recommendations-header p {{
      margin: 4px 0 0;
      color: var(--muted);
      font-size: 12px;
    }}

    .recommendation-controls {{
      display: grid;
      grid-template-columns: auto auto;
      gap: 10px;
      align-items: end;
    }}

    .recommendation-controls label,
    .view-mode-shell label {{
      margin-bottom: 5px;
      display: block;
      font-size: 12px;
      font-weight: 760;
    }}

    .view-mode-shell {{
      margin-bottom: 16px;
    }}

    .segmented {{
      display: inline-grid;
      grid-auto-flow: column;
      gap: 6px;
      align-items: center;
    }}

    .segmented button {{
      min-height: 36px;
      width: auto;
      padding: 0 12px;
      border: 1px solid var(--line-strong);
      border-radius: 999px;
      background: white;
      color: var(--ink);
      font-weight: 730;
    }}

    .segmented button.active {{
      background: var(--ink);
      color: white;
      border-color: var(--ink);
    }}

    .recommendation-list {{
      display: grid;
      gap: 12px;
    }}

    .recommendation-group {{
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
      display: grid;
      gap: 10px;
    }}

    .recommendation-group > strong {{
      font-size: 13px;
    }}

    .recommendation-group .recommendation-pair {{
      margin-top: -6px;
    }}

    .recommendation-group-items {{
      display: grid;
      gap: 10px;
    }}

    .recommendation-item {{
      padding-top: 10px;
      border-top: 1px solid var(--line);
      display: grid;
      gap: 8px;
    }}

    .recommendation-card {{
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
      display: grid;
      gap: 8px;
    }}

    .recommendation-card strong {{
      font-size: 13px;
    }}

    .recommendation-meta {{
      display: grid;
      grid-template-columns: auto auto 1fr;
      gap: 8px;
      align-items: center;
      color: var(--muted);
      font-size: 12px;
    }}

    .recommendation-badge {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 0 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel-soft);
      color: var(--ink);
      font-family: var(--mono);
      font-size: 11px;
    }}

    .recommendation-pair {{
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }}

    .recommendation-reasons {{
      margin: 0;
      padding-left: 16px;
      color: var(--muted);
      font-size: 12px;
    }}

    .recommendation-reasons li + li {{
      margin-top: 4px;
    }}

    .recommendation-empty {{
      padding: 18px;
      border: 1px dashed var(--line-strong);
      border-radius: 8px;
      color: var(--muted);
      font-size: 12px;
      background: rgb(255 255 255 / 60%);
    }}

    @media (max-width: 900px) {{
      .overview-band {{
        grid-template-columns: 1fr;
      }}

      .guide-columns {{
        grid-template-columns: 1fr;
      }}

      .metrics-inline {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      main {{
        grid-template-columns: 1fr;
      }}

      .recommendations-header {{
        grid-template-columns: 1fr;
      }}

      .recommendation-controls {{
        grid-template-columns: 1fr;
      }}

      aside {{
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }}

      .import-bar {{
        grid-template-columns: 1fr;
      }}

      .stage {{
        min-height: 560px;
      }}

      header {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>{escaped_client} Internal Link Map</h1>
      <p class="subtitle">Explore internal link structure, focused page relationships, noindex states, and global navigation patterns from <code>{escaped_source}</code>.</p>
    </div>
    <a class="index-link" id="indexLink" href="index.html">All maps</a>
  </header>

  <section class="overview-band">
    <div class="overview-card">
      <h2>Quick start</h2>
      <div class="guide-columns">
        <div class="guide-step">
          <strong>1. Load a site</strong>
          <span>Use the bundled map or upload an Ahrefs internal links export to rebuild the visualisation in-browser.</span>
        </div>
        <div class="guide-step">
          <strong>2. Focus a page set</strong>
          <span>Search for a page path or folder, then switch link direction to isolate incoming, outgoing, or two-way relationships.</span>
        </div>
        <div class="guide-step">
          <strong>3. Strip out noise</strong>
          <span>Use repeated-pattern and component controls to reduce nav, footer, related-post, and card-driven links.</span>
        </div>
      </div>
      <div class="metrics-inline">
        <div class="metric"><strong id="metric-pages">0</strong><span>unique internal pages</span><small class="metric-note">Retained internal HTML pages after crawl filtering.</small></div>
        <div class="metric"><strong id="metric-edges">0</strong><span>unique source-to-target pairs</span><small class="metric-note">Distinct directed links from one retained page to another.</small></div>
        <div class="metric"><strong id="metric-links">0</strong><span>retained link instances</span><small class="metric-note">All retained internal link occurrences from the export.</small></div>
        <div class="metric"><strong id="metric-visible-pages">0</strong><span>pages in current view</span><small class="metric-note">Pages still shown after the current filters and search.</small></div>
        <div class="metric"><strong id="metric-visible-edges">0</strong><span>links in current view</span><small class="metric-note">Directed links currently visible between shown pages.</small></div>
      </div>
    </div>
    <div class="overview-card preset-card">
      <div class="preset-header">
        <div>
          <h2>Preset</h2>
          <h3 id="presetTitle">Blog incoming links</h3>
          <p id="presetDescription">Applies a focused setup for reviewing links pointing into blog pages while suppressing repeated UI-driven patterns.</p>
        </div>
        <div class="preset-nav">
          <span class="preset-counter" id="presetCounter">1 / 3</span>
          <button class="icon-button" id="presetPrev" type="button" title="Previous preset" aria-label="Previous preset">&#8592;</button>
          <button class="icon-button" id="presetNext" type="button" title="Next preset" aria-label="Next preset">&#8594;</button>
        </div>
      </div>
      <ul class="preset-list" id="presetList"></ul>
      <button id="applyPreset" type="button">Apply Blog Preset</button>
    </div>
  </section>

  <section class="import-bar">
    <div class="import-panel">
      <h2>Upload Ahrefs file</h2>
      <div class="upload-row">
        <div></div>
        <label class="upload-pick">Choose file
          <input id="uploadInput" type="file" accept=".csv,.txt,.xml">
        </label>
      </div>
    </div>
    <div class="import-panel">
      <h2>Import sitemap link</h2>
      <div class="upload-row">
        <input id="sitemapUrlInput" class="import-url" type="url" placeholder="https://example.com/sitemap.xml">
        <button id="importSitemapUrl" class="secondary-button" type="button">Import</button>
      </div>
    </div>
  </section>

  <main>
    <aside>
      <div class="control">
        <label for="sectionFilter">Section <span id="sectionCount">all</span></label>
        <select id="sectionFilter"></select>
      </div>

      <div class="control">
        <label for="searchBox">Search path <span id="searchCount">optional</span></label>
        <div class="search-stack">
          <input id="searchBox" type="search" placeholder="/cloud-pbx/ or pabx">
          <div class="search-suggestions" id="searchSuggestions"></div>
        </div>
      </div>

      <div class="view-mode-shell">
        <label for="viewMode">View mode</label>
        <select id="viewMode">
          <option value="network">Network</option>
          <option value="tree">Tree</option>
          <option value="cluster">Cluster</option>
        </select>
      </div>

      <div class="control">
        <label for="directionFilter">Link direction <span id="directionCount">all</span></label>
        <select id="directionFilter">
          <option value="all">To and from matches</option>
          <option value="out">Links from matches</option>
          <option value="in">Links pointing to matches</option>
        </select>
      </div>

      <div class="control">
        <label for="sourcePathFilter">Source URL path <span id="sourcePathCount">optional</span></label>
        <input id="sourcePathFilter" type="search" placeholder="/blog/ or author">
        <div class="hint">Useful when reviewing links pointing to the current matches.</div>
      </div>

      <div class="control">
        <label for="targetPathFilter">Target URL path <span id="targetPathCount">optional</span></label>
        <input id="targetPathFilter" type="search" placeholder="/product/ or vs">
        <div class="hint">Useful when reviewing links from the current matches.</div>
      </div>

      <div class="control">
        <label for="sourceNoindexFilter">Source noindex <span id="sourceNoindexCount">all</span></label>
        <select id="sourceNoindexFilter">
          <option value="">All source pages</option>
          <option value="true">Yes only</option>
          <option value="false">No only</option>
        </select>
      </div>

      <div class="control">
        <label for="targetNoindexFilter">Target noindex <span id="targetNoindexCount">all</span></label>
        <select id="targetNoindexFilter">
          <option value="">All target pages</option>
          <option value="true">Yes only</option>
          <option value="false">No only</option>
        </select>
      </div>

      <div class="control">
        <label for="sourceStatusFilter">Source status code <span id="sourceStatusCount">all</span></label>
        <select id="sourceStatusFilter">
          <option value="">All source statuses</option>
        </select>
      </div>

      <div class="control">
        <label for="targetStatusFilter">Target status code <span id="targetStatusCount">all</span></label>
        <select id="targetStatusFilter">
          <option value="">All target statuses</option>
        </select>
      </div>

      <div class="control">
        <label for="nodeLimit">Pages shown <span id="nodeLimitValue">{node_limit_default}</span></label>
        <input id="nodeLimit" type="range" min="40" max="{node_limit_max}" value="{node_limit_default}" step="10">
      </div>

      <div class="control">
        <label for="minDegree">Minimum total links <span id="minDegreeValue">20</span></label>
        <input id="minDegree" type="range" min="0" max="600" value="20" step="5">
      </div>

      <div class="control">
        <label for="globalLinkMode">Global nav/footer links <span id="globalLinkModeCount">dim</span></label>
        <select id="globalLinkMode">
          <option value="dim">Dim repeated patterns</option>
          <option value="hide">Hide repeated patterns</option>
          <option value="show">Show all links</option>
        </select>
        <div class="hint" id="sitewideHiddenCount">Repeated target-and-anchor patterns stay visible but muted.</div>
      </div>

      <div class="control">
        <label for="componentLinkMode">Component links <span id="componentLinkModeCount">dim</span></label>
        <select id="componentLinkMode">
          <option value="dim">Dim likely components</option>
          <option value="hide">Hide likely components</option>
          <option value="show">Show all links</option>
        </select>
        <div class="hint" id="componentHint">Likely related-post, related-product, preview-card, and generic CTA links stay visible but muted.</div>
      </div>

      <div class="control">
        <label for="sitewideThreshold">Sitewide threshold <span id="sitewideThresholdValue">80%</span></label>
        <input id="sitewideThreshold" type="range" min="50" max="100" value="80" step="5">
      </div>

      <div class="control">
        <button id="resetView">Reset View</button>
      </div>

      <div class="legend" id="legend"></div>
      <div class="top-list">
        <h2>Most Connected Pages</h2>
        <div id="topPages"></div>
      </div>
    </aside>

    <section class="workspace">
      <div class="canvas-shell" id="canvasShell">
        <section class="stage" id="stage">
          <canvas id="graph"></canvas>
          <div class="focus-panel" id="focusPanel"></div>
          <div class="tooltip" id="tooltip"></div>
          <div class="empty" id="empty">No pages match these filters.</div>
        </section>
        <aside class="match-summary" id="matchSummary"></aside>
      </div>
      <section class="recommendations-shell">
        <div class="recommendations-header">
          <div>
            <h2>Link recommendations</h2>
            <p>Suggested internal-link gaps and indexing cleanups from the current scope, prioritised for valuable content pages rather than archive or UI-driven URLs.</p>
          </div>
          <div class="recommendation-controls">
            <div>
              <label for="recommendationLimit">Max recommendations</label>
              <select id="recommendationLimit">
                <option value="6">6</option>
                <option value="10" selected>10</option>
                <option value="16">16</option>
              </select>
            </div>
            <div>
              <label for="recommendationThreshold">Confidence threshold</label>
              <select id="recommendationThreshold">
                <option value="40">40</option>
                <option value="55" selected>55</option>
                <option value="70">70</option>
              </select>
            </div>
          </div>
        </div>
        <div class="segmented" id="recommendationTabs">
          <button type="button" data-type="blog-blog" class="active">Blog -> Blog</button>
          <button type="button" data-type="blog-money">Blog -> Money Pages</button>
          <button type="button" data-type="indexing-cleanup">Indexing Cleanup</button>
        </div>
        <div class="recommendation-list" id="recommendationList"></div>
      </section>
    </section>
  </main>

  <script>
    const PRELOADED_GRAPH = {data_json};

    const palette = ["#0f766e", "#2457a6", "#b7791f", "#b83a3a", "#2f855a", "#6b46c1", "#315c72", "#8a4d1f", "#64748b", "#be185d", "#047857", "#7c3aed"];
    let currentGraph = PRELOADED_GRAPH;
    let groupColor = new Map();
    let nodesById = new Map();
    const canvas = document.getElementById("graph");
    const stage = document.getElementById("stage");
    const ctx = canvas.getContext("2d");
    const focusPanel = document.getElementById("focusPanel");
    const tooltip = document.getElementById("tooltip");
    const empty = document.getElementById("empty");
    const sectionFilter = document.getElementById("sectionFilter");
    const searchBox = document.getElementById("searchBox");
    const searchSuggestions = document.getElementById("searchSuggestions");
    const viewMode = document.getElementById("viewMode");
    const directionFilter = document.getElementById("directionFilter");
    const sourcePathFilter = document.getElementById("sourcePathFilter");
    const targetPathFilter = document.getElementById("targetPathFilter");
    const sourceNoindexFilter = document.getElementById("sourceNoindexFilter");
    const targetNoindexFilter = document.getElementById("targetNoindexFilter");
    const sourceStatusFilter = document.getElementById("sourceStatusFilter");
    const targetStatusFilter = document.getElementById("targetStatusFilter");
    const nodeLimit = document.getElementById("nodeLimit");
    const minDegree = document.getElementById("minDegree");
    const globalLinkMode = document.getElementById("globalLinkMode");
    const sitewideThreshold = document.getElementById("sitewideThreshold");
    const topPages = document.getElementById("topPages");
    const uploadInput = document.getElementById("uploadInput");
    const sitemapUrlInput = document.getElementById("sitemapUrlInput");
    const importSitemapUrl = document.getElementById("importSitemapUrl");
    const componentLinkMode = document.getElementById("componentLinkMode");
    const componentHint = document.getElementById("componentHint");
    const indexLink = document.getElementById("indexLink");
    const presetTitle = document.getElementById("presetTitle");
    const presetDescription = document.getElementById("presetDescription");
    const presetList = document.getElementById("presetList");
    const presetCounter = document.getElementById("presetCounter");
    const presetPrev = document.getElementById("presetPrev");
    const presetNext = document.getElementById("presetNext");
    const applyPreset = document.getElementById("applyPreset");
    const recommendationTabs = document.getElementById("recommendationTabs");
    const recommendationList = document.getElementById("recommendationList");
    const recommendationLimit = document.getElementById("recommendationLimit");
    const recommendationThreshold = document.getElementById("recommendationThreshold");
    const canvasShell = document.getElementById("canvasShell");
    const matchSummary = document.getElementById("matchSummary");
    const UPLOADED_MAP_INDEX_KEY = "internal-link-map-uploaded-v1";

    let viewNodes = [];
    let viewEdges = [];
    let matchedSearchIds = new Set();
    let focusedSearchNodes = [];
    let simulationId = 0;
    let hovered = null;
    let selectedIds = new Set();
    let dragNode = null;
    let transform = {{ x: 0, y: 0, scale: 1 }};
    let panStart = null;
    let tooltipPinned = false;
    let focusPanelDismissed = false;
    let lastFocusQuery = "";
    let activePresetIndex = 0;
    let activeRecommendationType = "blog-blog";
    let recommendationState = {{ "blog-blog": [], "blog-money": [], "indexing-cleanup": [] }};
    let graphCaches = {{
      outgoingTargetsBySource: new Map(),
      incomingSourcesByTarget: new Map(),
      outgoingEdgesBySource: new Map(),
      incomingEdgesByTarget: new Map(),
      edgeKeySet: new Set()
    }};

    const PRESETS = [
      {{
        title: "Blog incoming links",
        buttonLabel: "Apply Blog Preset",
        description: "Focused review of links pointing into blog pages while suppressing repeated UI-driven patterns.",
        bullets: [
          "Search path: /blog/",
          "Link direction: links pointing to matches",
          "Source / target noindex: no only",
          "Pages shown: 100",
          "Minimum total links: 10",
          "Repeated patterns: hide",
          "Likely components: hide",
          "Sitewide threshold: 100%"
        ],
        apply() {{
          searchBox.value = "/blog/";
          directionFilter.value = "in";
          sourceNoindexFilter.value = "false";
          targetNoindexFilter.value = "false";
          sourceStatusFilter.value = "";
          targetStatusFilter.value = "";
          nodeLimit.value = String(Math.min(100, Number(nodeLimit.max)));
          minDegree.value = "10";
          globalLinkMode.value = "hide";
          componentLinkMode.value = "hide";
          sitewideThreshold.value = "100";
        }}
      }},
      {{
        title: "Product incoming links",
        buttonLabel: "Apply Product Preset",
        description: "Focused review of links pointing into product pages while suppressing repeated UI-driven patterns.",
        bullets: [
          "Search path: /product/",
          "Link direction: links pointing to matches",
          "Source / target noindex: no only",
          "Pages shown: 100",
          "Minimum total links: 10",
          "Repeated patterns: hide",
          "Likely components: hide",
          "Sitewide threshold: 100%"
        ],
        apply() {{
          searchBox.value = "/product/";
          directionFilter.value = "in";
          sourceNoindexFilter.value = "false";
          targetNoindexFilter.value = "false";
          sourceStatusFilter.value = "";
          targetStatusFilter.value = "";
          nodeLimit.value = String(Math.min(100, Number(nodeLimit.max)));
          minDegree.value = "10";
          globalLinkMode.value = "hide";
          componentLinkMode.value = "hide";
          sitewideThreshold.value = "100";
        }}
      }},
      {{
        title: "Category incoming links",
        buttonLabel: "Apply Category Preset",
        description: "Focused review of links pointing into product-category pages while suppressing repeated UI-driven patterns.",
        bullets: [
          "Search path: /product-category/",
          "Link direction: links pointing to matches",
          "Source / target noindex: no only",
          "Pages shown: 100",
          "Minimum total links: 10",
          "Repeated patterns: hide",
          "Likely components: hide",
          "Sitewide threshold: 100%"
        ],
        apply() {{
          searchBox.value = "/product-category/";
          directionFilter.value = "in";
          sourceNoindexFilter.value = "false";
          targetNoindexFilter.value = "false";
          sourceStatusFilter.value = "";
          targetStatusFilter.value = "";
          nodeLimit.value = String(Math.min(100, Number(nodeLimit.max)));
          minDegree.value = "10";
          globalLinkMode.value = "hide";
          componentLinkMode.value = "hide";
          sitewideThreshold.value = "100";
        }}
      }},
      {{
        title: "Body-copy opportunities",
        buttonLabel: "Apply Body-Copy Preset",
        description: "Reduces repeated navigation and component-style links so contextual internal links and thin-link pages stand out more clearly.",
        bullets: [
          "Search path: all pages",
          "Link direction: to and from matches",
          "Source / target noindex: no only",
          "Pages shown: 120",
          "Minimum total links: 5",
          "Repeated patterns: hide",
          "Likely components: hide",
          "Sitewide threshold: 100%"
        ],
        apply() {{
          searchBox.value = "";
          directionFilter.value = "all";
          sourceNoindexFilter.value = "false";
          targetNoindexFilter.value = "false";
          sourceStatusFilter.value = "";
          targetStatusFilter.value = "";
          nodeLimit.value = String(Math.min(120, Number(nodeLimit.max)));
          minDegree.value = "5";
          globalLinkMode.value = "hide";
          componentLinkMode.value = "hide";
          sitewideThreshold.value = "100";
        }}
      }},
      {{
        title: "Noindex target audit",
        buttonLabel: "Apply Noindex Audit",
        description: "Surfaces visible internal links that point into noindex pages so crawl waste and cleanup opportunities are easier to spot.",
        bullets: [
          "Search path: all pages",
          "Link direction: to and from matches",
          "Source noindex: no only",
          "Target noindex: yes only",
          "Pages shown: 120",
          "Minimum total links: 0",
          "Repeated patterns: hide",
          "Likely components: dim",
          "Sitewide threshold: 100%"
        ],
        apply() {{
          searchBox.value = "";
          directionFilter.value = "all";
          sourceNoindexFilter.value = "false";
          targetNoindexFilter.value = "true";
          sourceStatusFilter.value = "";
          targetStatusFilter.value = "";
          nodeLimit.value = String(Math.min(120, Number(nodeLimit.max)));
          minDegree.value = "0";
          globalLinkMode.value = "hide";
          componentLinkMode.value = "dim";
          sitewideThreshold.value = "100";
        }}
      }}
    ];

    function formatNumber(value) {{
      return new Intl.NumberFormat("en-ZA").format(value);
    }}

    function escapeHtml(value) {{
      return String(value ?? "").replace(/[<>&"]/g, char => ({{ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }}[char]));
    }}

    const STOPWORDS = new Set(["the","and","for","with","your","this","that","into","from","how","what","why","can","best","guide","south","africa","page","blog"]);

    function tokenizeValue(value) {{
      return [...new Set(String(value || "")
        .toLowerCase()
        .replace(/https?:\/\/[^/\s]+/g, "")
        .split(/[^a-z0-9]+/g)
        .filter(token => token.length >= 3 && !STOPWORDS.has(token)))];
    }}

    function getNodeTokens(node) {{
      return tokenizeValue(`${{node.label}} ${{node.path}} ${{node.group}}`);
    }}

    function intersectionCount(a, b) {{
      const setB = new Set(b);
      return a.filter(item => setB.has(item)).length;
    }}

    function isBlogNode(node) {{
      return node.group === "/blog" || node.path.startsWith("/blog/");
    }}

    function isBlogRootNode(node) {{
      return normalizeSearchText(node.path) === "/blog";
    }}

    function isBlogPaginationNode(node) {{
      return /^\/blog\/page\/\d+$/i.test(node.path);
    }}

    function isBlogAuthorNode(node) {{
      return /^\/blog\/author\//i.test(node.path);
    }}

    function isBlogTaxonomyArchiveNode(node) {{
      return /^\/blog\/(?:category|tag)\//i.test(node.path);
    }}

    function isBlogDateArchiveNode(node) {{
      return /^\/blog\/\d{{4}}(?:\/\d{{2}}(?:\/\d{{2}})?)?$/i.test(node.path);
    }}

    function isUtilityLowValueNode(node) {{
      return /\/(privacy-policy|terms(?:-and-conditions)?|thank-you|my-account|cart|checkout|feed|author|page\/\d+)$/i.test(node.path);
    }}

    function getIndexingCleanupReason(node) {{
      if (isBlogPaginationNode(node)) return "Paginated blog archive pages rarely deserve indexation and usually dilute crawl focus.";
      if (isBlogAuthorNode(node)) return "Author archive pages are usually low-value indexable URLs unless they carry unique editorial value.";
      if (isBlogTaxonomyArchiveNode(node)) return "Category and tag archive pages are usually weak search landing pages unless they are deliberately curated.";
      if (isBlogDateArchiveNode(node)) return "Date-based blog archives are usually low-value and tend to create thin archive index bloat.";
      if (isBlogRootNode(node)) return "The main blog listing is often weaker than the actual articles and may not deserve priority as an indexable target.";
      if (/\/thank-you$/i.test(node.path)) return "Thank-you pages are utility endpoints and are usually better excluded from indexation.";
      if (/\/(my-account|cart|checkout)$/i.test(node.path)) return "Account and transaction pages are utility URLs and usually should not be indexed.";
      if (/\/privacy-policy$/i.test(node.path) || /\/terms(?:-and-conditions)?$/i.test(node.path)) return "Policy pages should rarely be strategic internal-link targets or index priorities.";
      return "This URL looks like a low-value archive or utility page that may be better handled with noindex.";
    }}

    function isLowValueNode(node) {{
      return isBlogRootNode(node) ||
        isBlogPaginationNode(node) ||
        isBlogAuthorNode(node) ||
        isBlogTaxonomyArchiveNode(node) ||
        isBlogDateArchiveNode(node) ||
        isUtilityLowValueNode(node);
    }}

    function isImportantBlogNode(node) {{
      if (!isBlogNode(node) || isLowValueNode(node)) return false;
      const parts = node.path.split("/").filter(Boolean);
      return parts.length >= 2;
    }}

    function isMoneyPageNode(node) {{
      if (isBlogNode(node) || node.path === "/" || node.group === "/home" || isLowValueNode(node)) return false;
      return /(product|category|shop|pricing|quote|service|cloud|voice|connectivity|software|solution|contact|pbx|voip|phones)/i.test(node.path + " " + node.group);
    }}

    function buildGraphCaches() {{
      const outgoingTargetsBySource = new Map();
      const incomingSourcesByTarget = new Map();
      const outgoingEdgesBySource = new Map();
      const incomingEdgesByTarget = new Map();
      const edgeKeySet = new Set();

      currentGraph.edges.forEach(edge => {{
        const edgeKey = `${{edge.source}}|||${{edge.target}}`;
        edgeKeySet.add(edgeKey);
        if (!outgoingTargetsBySource.has(edge.source)) outgoingTargetsBySource.set(edge.source, new Set());
        if (!incomingSourcesByTarget.has(edge.target)) incomingSourcesByTarget.set(edge.target, new Set());
        if (!outgoingEdgesBySource.has(edge.source)) outgoingEdgesBySource.set(edge.source, []);
        if (!incomingEdgesByTarget.has(edge.target)) incomingEdgesByTarget.set(edge.target, []);
        outgoingTargetsBySource.get(edge.source).add(edge.target);
        incomingSourcesByTarget.get(edge.target).add(edge.source);
        outgoingEdgesBySource.get(edge.source).push(edge);
        incomingEdgesByTarget.get(edge.target).push(edge);
      }});

      graphCaches = {{ outgoingTargetsBySource, incomingSourcesByTarget, outgoingEdgesBySource, incomingEdgesByTarget, edgeKeySet }};
    }}

    function getSelectedNodes() {{
      return viewNodes.filter(node => selectedIds.has(node.id));
    }}

    function getSelectedEdges() {{
      return viewEdges.filter(edge => selectedIds.has(edge.source) && selectedIds.has(edge.target));
    }}

    function buildMapHrefForStorageKey(storageKey) {{
      const currentFile = window.location.pathname.split("/").pop() || "index.html";
      return resolveInternalHtmlHref(currentFile, `uploadedMapKey=${{encodeURIComponent(storageKey)}}`);
    }}

    function slugifyValue(value) {{
      return String(value || "")
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "")
        .slice(0, 80) || "site";
    }}

    function getHtmlPreviewSourceUrl() {{
      if (window.location.hostname !== "htmlpreview.github.io") return "";
      const raw = window.location.href.split("?").slice(1).join("?");
      return raw.startsWith("https://") ? raw : "";
    }}

    function resolveInternalHtmlHref(fileName, query = "") {{
      const suffix = query ? `${{fileName}}?${{query}}` : fileName;
      const previewSource = getHtmlPreviewSourceUrl();
      if (previewSource) {{
        const baseDir = previewSource.replace(/[^/?#]+(?:\?.*)?$/, "");
        return `https://htmlpreview.github.io/?${{baseDir}}${{suffix}}`;
      }}
      return suffix;
    }}

    function saveUploadedGraph(graph, fileName) {{
      try {{
        const registry = JSON.parse(window.localStorage.getItem(UPLOADED_MAP_INDEX_KEY) || "[]");
        const storageKey = `uploaded-map::${{slugifyValue(graph.meta.domain || graph.meta.clientName || "site")}}::${{Date.now()}}::${{slugifyValue(fileName)}}`;
        window.localStorage.setItem(storageKey, JSON.stringify({{ graph, fileName }}));
        const next = Array.isArray(registry) ? registry.filter(item => item && item.storageKey !== storageKey) : [];
        next.unshift({{
          storageKey,
          clientName: graph.meta.clientName,
          domain: graph.meta.domain,
          fileName,
          uniquePages: graph.meta.uniquePages,
          uniqueEdges: graph.meta.uniqueEdges,
          linksRetained: graph.meta.linksRetained,
          importedAt: new Date().toISOString(),
          href: buildMapHrefForStorageKey(storageKey)
        }});
        window.localStorage.setItem(UPLOADED_MAP_INDEX_KEY, JSON.stringify(next.slice(0, 24)));
      }} catch {{
      }}
    }}

    function loadStoredUploadedGraph() {{
      try {{
        const params = new URLSearchParams(window.location.search);
        const storageKey = params.get("uploadedMapKey");
        if (!storageKey) return null;
        const raw = window.localStorage.getItem(storageKey);
        if (!raw) return null;
        return JSON.parse(raw);
      }} catch {{
        return null;
      }}
    }}

    function normalizeSearchText(value) {{
      return (value || "")
        .toLowerCase()
        .replace(/https?:\\/\\/(www\\.)?[^\\s/]+/g, "")
        .replace(/[?#].*$/g, "")
        .replace(/\\/+$/g, "");
    }}

    function splitPathParts(value) {{
      return normalizeSearchText(value).split("/").filter(Boolean);
    }}

    function getPathSearchMatchType(node, rawQuery) {{
      const query = normalizeSearchText(rawQuery);
      if (!query) return "";
      const nodeText = normalizeSearchText(node.path + " " + node.label + " " + node.id);
      if (!query.includes("/")) return nodeText.includes(query) ? "text" : "";

      const path = normalizeSearchText(node.path);
      if (!path) return "";
      if (path === query) return "exact";

      const pathParts = splitPathParts(path);
      const queryParts = splitPathParts(query);
      if (!queryParts.length || pathParts.length < queryParts.length) return nodeText.includes(query) ? "text" : "";

      const suffixParts = pathParts.slice(-queryParts.length);
      const suffixMatches = suffixParts.length === queryParts.length && suffixParts.every((part, index) => part === queryParts[index]);

      if (suffixMatches) {{
        if (pathParts.length === queryParts.length + 1) return "locale-root";
        if (pathParts.length === queryParts.length) return "exact";
      }}

      if (path.startsWith(`${{query}}/`)) return "descendant";
      const localizedPrefix = pathParts.findIndex((part, index) => index < pathParts.length - queryParts.length && queryParts[0] === pathParts[index + 1]);
      if (localizedPrefix === 0 && path.includes(`${{query}}/`)) return "descendant";

      return nodeText.includes(query) ? "text" : "";
    }}

    function canonicalUrl(rawUrl) {{
      try {{
        const url = new URL((rawUrl || "").trim());
        const path = url.pathname && url.pathname !== "/" ? url.pathname.replace(/\\/+$/g, "") : "/";
        const host = url.hostname.toLowerCase().replace(/^www\\./, "");
        return `${{url.protocol.toLowerCase()}}//${{host}}${{path}}`;
      }} catch {{
        return "";
      }}
    }}

    function pathGroup(url) {{
      try {{
        const parsed = new URL(url);
        const parts = parsed.pathname.split("/").filter(Boolean);
        return "/" + (parts[0] || "home");
      }} catch {{
        return "/home";
      }}
    }}

    function pageLabel(url) {{
      try {{
        const parsed = new URL(url);
        const parts = parsed.pathname.split("/").filter(Boolean);
        if (!parts.length) return "Homepage";
        return parts[parts.length - 1].replace(/[-_]/g, " ").replace(/\\b\\w/g, char => char.toUpperCase());
      }} catch {{
        return "Page";
      }}
    }}

    function normalizeAnchor(anchor) {{
      return (anchor || "").trim().replace(/\\s+/g, " ").toLowerCase();
    }}

    const GENERIC_COMPONENT_ANCHORS = new Set([
      "read more",
      "read full post",
      "learn more",
      "view more",
      "view product",
      "view products",
      "shop now",
      "see more",
      "find out more",
      "discover more",
      "continue reading",
      "read article",
      "read post"
    ]);

    function parseDelimited(text, delimiter = "\\t") {{
      const rows = [];
      let row = [];
      let value = "";
      let inQuotes = false;

      for (let i = 0; i < text.length; i++) {{
        const char = text[i];
        const next = text[i + 1];

        if (char === '"') {{
          if (inQuotes && next === '"') {{
            value += '"';
            i += 1;
          }} else {{
            inQuotes = !inQuotes;
          }}
          continue;
        }}

        if (!inQuotes && char === delimiter) {{
          row.push(value);
          value = "";
          continue;
        }}

        if (!inQuotes && (char === "\\n" || char === "\\r")) {{
          if (char === "\\r" && next === "\\n") i += 1;
          row.push(value);
          value = "";
          if (row.some(cell => cell !== "")) rows.push(row);
          row = [];
          continue;
        }}

        value += char;
      }}

      if (value.length || row.length) {{
        row.push(value);
        if (row.some(cell => cell !== "")) rows.push(row);
      }}

      return rows;
    }}

    function decodeFileText(buffer) {{
      const bytes = new Uint8Array(buffer);
      if (bytes[0] === 255 && bytes[1] === 254) return new TextDecoder("utf-16le").decode(bytes);
      if (bytes[0] === 254 && bytes[1] === 255) return new TextDecoder("utf-16be").decode(bytes);
      if (bytes[0] === 239 && bytes[1] === 187 && bytes[2] === 191) return new TextDecoder("utf-8").decode(bytes);
      try {{
        return new TextDecoder("utf-16le").decode(bytes);
      }} catch {{
        return new TextDecoder("utf-8").decode(bytes);
      }}
    }}

    function inferDomain(rows) {{
      const counts = new Map();
      rows.forEach(row => {{
        [row["Source URL"], row["Target URL"]].forEach(rawUrl => {{
          try {{
            const host = new URL(rawUrl).hostname.toLowerCase().replace(/^www\\./, "");
            counts.set(host, (counts.get(host) || 0) + 1);
          }} catch {{
          }}
        }});
      }});
      return [...counts.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] || "";
    }}

    function inferClientName(domain) {{
      const parts = (domain || "").split(".").filter(Boolean);
      const relevant = parts.length > 2 ? parts.slice(0, -2) : parts.slice(0, -1);
      const name = (relevant.length ? relevant : parts.slice(0, 1))
        .map(part => part.charAt(0).toUpperCase() + part.slice(1))
        .join(" ");
      return name || "Uploaded site";
    }}

    function buildGraphFromSitemapUrls(urls, sourceFileName) {{
      const canonicalUrls = [...new Set(urls.map(rawUrl => canonicalUrl(rawUrl)).filter(Boolean))].sort();
      if (!canonicalUrls.length) {{
        throw new Error("No page URLs were found in this sitemap file.");
      }}

      const domain = (() => {{
        try {{
          return new URL(canonicalUrls[0]).hostname.toLowerCase().replace(/^www\\./, "");
        }} catch {{
          return "";
        }}
      }})();

      const groupCounts = new Map();
      const nodes = canonicalUrls.map((url, index) => {{
        const group = pathGroup(url);
        groupCounts.set(group, (groupCounts.get(group) || 0) + 1);
        const parsed = new URL(url);
        return {{
          id: url,
          label: pageLabel(url),
          path: parsed.pathname || "/",
          group,
          in: 0,
          out: 0,
          degree: 0,
          targetSourcePages: 0,
          targetSourceShare: 0,
          sourceNoindex: false,
          targetNoindex: false,
          sourceStatusCode: "",
          targetStatusCode: "",
          index
        }};
      }});

      return {{
        meta: {{
          sourceFile: sourceFileName,
          domain,
          clientName: inferClientName(domain),
          rowsRead: canonicalUrls.length,
          linksRetained: 0,
          selfReferencesExcluded: 0,
          sourcePages: 0,
          uniquePages: nodes.length,
          uniqueEdges: 0,
          groups: [...groupCounts.entries()].sort((a, b) => b[1] - a[1]),
          sourceStatusCodes: [],
          targetStatusCodes: [],
          importType: "sitemap"
        }},
        nodes,
        edges: []
      }};
    }}

    function parseSitemapGraphFromText(text, sourceFileName) {{
      const xml = new DOMParser().parseFromString(text, "application/xml");
      if (xml.querySelector("parsererror")) {{
        throw new Error("This XML file could not be parsed as a sitemap.");
      }}
      const rootName = (xml.documentElement?.localName || "").toLowerCase();
      const urlLocs = [...xml.querySelectorAll("url > loc")].map(node => node.textContent?.trim() || "");
      if (urlLocs.length) {{
        return buildGraphFromSitemapUrls(urlLocs, sourceFileName);
      }}
      if (rootName === "sitemapindex") {{
        throw new Error("This looks like a sitemap index, not a page sitemap. Upload a page-level sitemap with <url><loc> entries, or use the Ahrefs export for full link mapping.");
      }}
      throw new Error("No page URLs were found in this sitemap file.");
    }}

    async function fetchSitemapFromUrl(url) {{
      const apiUrl = `/api/fetch-sitemap?url=${{encodeURIComponent(url)}}`;
      const response = await fetch(apiUrl);
      if (!response.ok) {{
        let message = "Could not fetch this sitemap URL.";
        try {{
          const data = await response.json();
          if (data?.error) message = data.error;
        }} catch {{
        }}
        throw new Error(message);
      }}
      const data = await response.json();
      if (!data?.xml) throw new Error("The sitemap response was empty.");
      return data.xml;
    }}

    function buildGraphFromRows(rows, sourceFileName) {{
      const edgeCounts = new Map();
      const anchors = new Map();
      const inCounts = new Map();
      const outCounts = new Map();
      const groupCounts = new Map();
      const sourcePages = new Set();
      const targetSourcePages = new Map();
      const anchorSourcePages = new Map();
      const edgeAnchorKeys = new Map();
      const sourceNoindexByUrl = new Map();
      const targetNoindexByUrl = new Map();
      const sourceStatusByUrl = new Map();
      const targetStatusByUrl = new Map();
      const edgeNoindex = new Map();
      const edgeStatus = new Map();
      const domain = inferDomain(rows);
      let retainedCount = 0;
      let rowCount = 0;
      let selfRefCount = 0;

      const bump = (map, key, amount = 1) => map.set(key, (map.get(key) || 0) + amount);
      const ensureSet = (map, key) => {{
        if (!map.has(key)) map.set(key, new Set());
        return map.get(key);
      }};
      const ensureMap = (map, key) => {{
        if (!map.has(key)) map.set(key, new Map());
        return map.get(key);
      }};

      rows.forEach(row => {{
        rowCount += 1;
        const source = canonicalUrl(row["Source URL"] || "");
        const target = canonicalUrl(row["Target URL"] || "");
        if (!source || !target) return;

        let targetHost = "";
        try {{
          targetHost = new URL(target).hostname.toLowerCase().replace(/^www\\./, "");
        }} catch {{
          return;
        }}

        const isInternal = row["Is source internal"] === "true" && targetHost === domain;
        const targetIsHtmlPage = (row["Target URL type"] || "").includes("HTML Page");

        if (!isInternal || !targetIsHtmlPage) return;
        if (source === target || row["Is link self-referencing"] === "true") {{
          selfRefCount += 1;
          return;
        }}

        const edgeKey = `${{source}}|||${{target}}`;
        bump(edgeCounts, edgeKey);
        sourcePages.add(source);
        ensureSet(targetSourcePages, target).add(source);

        const sourceNoindex = row["Is source noindex"] === "true";
        const targetNoindex = row["Is target noindex"] === "true";
        const sourceStatusCode = (row["Source HTTP status code"] || "").trim();
        const targetStatusCode = (row["Target HTTP status code"] || "").trim();
        sourceNoindexByUrl.set(source, sourceNoindex);
        targetNoindexByUrl.set(target, targetNoindex);
        sourceStatusByUrl.set(source, sourceStatusCode);
        targetStatusByUrl.set(target, targetStatusCode);
        edgeNoindex.set(edgeKey, {{ sourceNoindex, targetNoindex }});
        edgeStatus.set(edgeKey, {{ sourceStatusCode, targetStatusCode }});

        const anchor = (row["Anchor"] || "").trim();
        if (anchor) {{
          const anchorMap = ensureMap(anchors, edgeKey);
          bump(anchorMap, anchor);
          const anchorKey = `${{target}}|||${{normalizeAnchor(anchor)}}`;
          ensureSet(anchorSourcePages, anchorKey).add(source);
          ensureSet(edgeAnchorKeys, edgeKey).add(anchorKey);
        }}

        bump(outCounts, source);
        bump(inCounts, target);
        retainedCount += 1;
      }});

      const urls = [...new Set([...inCounts.keys(), ...outCounts.keys()])].sort();
      const sourcePageCount = sourcePages.size;
      const nodes = urls.map((url, index) => {{
        const group = pathGroup(url);
        const sourceCoverageCount = (targetSourcePages.get(url) || new Set()).size;
        const sourceCoverageShare = sourcePageCount ? sourceCoverageCount / sourcePageCount : 0;
        bump(groupCounts, group);
        const parsed = new URL(url);
        return {{
          id: url,
          label: pageLabel(url),
          path: parsed.pathname || "/",
          group,
          in: inCounts.get(url) || 0,
          out: outCounts.get(url) || 0,
          degree: (inCounts.get(url) || 0) + (outCounts.get(url) || 0),
          targetSourcePages: sourceCoverageCount,
          targetSourceShare: sourceCoverageShare,
          sourceNoindex: sourceNoindexByUrl.get(url) || false,
          targetNoindex: targetNoindexByUrl.get(url) || false,
          sourceStatusCode: sourceStatusByUrl.get(url) || "",
          targetStatusCode: targetStatusByUrl.get(url) || "",
          index
        }};
      }}).sort((a, b) => b.degree - a.degree);

      const edges = [...edgeCounts.entries()].map(([edgeKey, count]) => {{
        const [source, target] = edgeKey.split("|||");
        const targetCoverageCount = (targetSourcePages.get(target) || new Set()).size;
        const targetCoverageShare = sourcePageCount ? targetCoverageCount / sourcePageCount : 0;
        const normalizedTargetLabel = normalizeAnchor(pageLabel(target));
        const anchorShares = [...(edgeAnchorKeys.get(edgeKey) || new Set())].map(anchorKey => {{
          const sourceSet = anchorSourcePages.get(anchorKey) || new Set();
          return sourcePageCount ? sourceSet.size / sourcePageCount : 0;
        }});
        const anchorSourceShare = anchorShares.length ? Math.min(...anchorShares) : 0;
        const topAnchors = [...(anchors.get(edgeKey) || new Map()).entries()]
          .sort((a, b) => b[1] - a[1])
          .slice(0, 5)
          .map(([text, anchorCount]) => ({{ text, count: anchorCount }}));
        const genericAnchor = topAnchors.some(anchor => GENERIC_COMPONENT_ANCHORS.has(normalizeAnchor(anchor.text)));
        const labelLikeAnchor = topAnchors.some(anchor => normalizeAnchor(anchor.text) === normalizedTargetLabel);
        const noindex = edgeNoindex.get(edgeKey) || {{ sourceNoindex: false, targetNoindex: false }};
        const status = edgeStatus.get(edgeKey) || {{ sourceStatusCode: "", targetStatusCode: "" }};
        return {{
          source,
          target,
          count,
          targetSourcePages: targetCoverageCount,
          targetSourceShare: targetCoverageShare,
          anchorSourceShare,
          genericAnchor,
          labelLikeAnchor,
          sourceNoindex: noindex.sourceNoindex,
          targetNoindex: noindex.targetNoindex,
          sourceStatusCode: status.sourceStatusCode,
          targetStatusCode: status.targetStatusCode,
          anchors: topAnchors
        }};
      }}).sort((a, b) => b.count - a.count);

      const sourceGroupCounts = new Map();
      edges.forEach(edge => {{
        if (!(edge.genericAnchor || edge.labelLikeAnchor)) return;
        const key = `${{edge.source}}|||${{pathGroup(edge.target)}}`;
        sourceGroupCounts.set(key, (sourceGroupCounts.get(key) || 0) + 1);
      }});

      edges.forEach(edge => {{
        const key = `${{edge.source}}|||${{pathGroup(edge.target)}}`;
        const sourceGroupTotal = sourceGroupCounts.get(key) || 0;
        edge.componentLike = edge.genericAnchor || (edge.labelLikeAnchor && sourceGroupTotal >= 3);
      }});

      return {{
        meta: {{
          sourceFile: sourceFileName,
          domain,
          clientName: inferClientName(domain),
          rowsRead: rowCount,
          linksRetained: retainedCount,
          selfReferencesExcluded: selfRefCount,
          sourcePages: sourcePageCount,
          uniquePages: nodes.length,
          uniqueEdges: edges.length,
          groups: [...groupCounts.entries()].sort((a, b) => b[1] - a[1]),
          sourceStatusCodes: [...new Set([...sourceStatusByUrl.values()].filter(Boolean))].sort((a, b) => a.localeCompare(b, undefined, {{ numeric: true }})),
          targetStatusCodes: [...new Set([...targetStatusByUrl.values()].filter(Boolean))].sort((a, b) => a.localeCompare(b, undefined, {{ numeric: true }})),
          importType: "ahrefs"
        }},
        nodes,
        edges
      }};
    }}

    function setMetrics() {{
      document.getElementById("metric-pages").textContent = formatNumber(currentGraph.meta.uniquePages);
      document.getElementById("metric-edges").textContent = formatNumber(currentGraph.meta.uniqueEdges);
      document.getElementById("metric-links").textContent = formatNumber(currentGraph.meta.linksRetained);
      document.getElementById("metric-visible-pages").textContent = formatNumber(viewNodes.length);
      document.getElementById("metric-visible-edges").textContent = formatNumber(viewEdges.length);
    }}

    function syncGraphState() {{
      groupColor = new Map();
      currentGraph.meta.groups.forEach(([group], index) => groupColor.set(group, palette[index % palette.length]));
      nodesById = new Map(currentGraph.nodes.map(node => [node.id, node]));
      buildGraphCaches();
      document.title = `${{currentGraph.meta.clientName}} Internal Link Map`;
      document.querySelector("h1").textContent = `${{currentGraph.meta.clientName}} Internal Link Map`;
      document.querySelector(".subtitle").innerHTML = (currentGraph.meta.importType || "ahrefs") === "sitemap"
        ? `Explore URL coverage and folder structure from <code>${{String(currentGraph.meta.sourceFile).replace(/[<>&]/g, char => ({{"<":"&lt;",">":"&gt;","&":"&amp;"}}[char]))}}</code>. This sitemap-based view does not include true internal-link relationships.`
        : `Explore internal link structure, focused page relationships, noindex states, and global navigation patterns from <code>${{String(currentGraph.meta.sourceFile).replace(/[<>&]/g, char => ({{"<":"&lt;",">":"&gt;","&":"&amp;"}}[char]))}}</code>.`;
      nodeLimit.max = Math.max(40, currentGraph.meta.uniquePages);
      const defaultLimit = Math.min(180, currentGraph.meta.uniquePages);
      nodeLimit.value = String(defaultLimit);
      document.getElementById("nodeLimitValue").textContent = defaultLimit;
    }}

    function setupControls() {{
      sectionFilter.innerHTML = '<option value="">All sections</option>' + currentGraph.meta.groups
        .map(([group, count]) => `<option value="${{group}}">${{group}} (${{formatNumber(count)}})</option>`)
        .join("");
      sourceStatusFilter.innerHTML = '<option value="">All source statuses</option>' + (currentGraph.meta.sourceStatusCodes || [])
        .map(code => `<option value="${{code}}">${{code}}</option>`)
        .join("");
      targetStatusFilter.innerHTML = '<option value="">All target statuses</option>' + (currentGraph.meta.targetStatusCodes || [])
        .map(code => `<option value="${{code}}">${{code}}</option>`)
        .join("");
      document.getElementById("legend").innerHTML = currentGraph.meta.groups.slice(0, 12)
        .map(([group]) => `<div class="legend-item"><span class="swatch" style="background:${{groupColor.get(group)}}"></span><span>${{group}}</span></div>`)
        .join("");
    }}

    function renderPreset() {{
      const preset = PRESETS[activePresetIndex];
      presetTitle.textContent = preset.title;
      presetDescription.textContent = preset.description;
      presetCounter.textContent = `${{activePresetIndex + 1}} / ${{PRESETS.length}}`;
      presetList.innerHTML = preset.bullets.map(item => `<li>${{escapeHtml(item)}}</li>`).join("");
      applyPreset.textContent = preset.buttonLabel;
    }}

    function renderSearchSuggestions(rawQuery, matchesQuery) {{
      const query = normalizeSearchText(rawQuery);
      if (!query || query.length < 2) {{
        searchSuggestions.classList.remove("active");
        searchSuggestions.innerHTML = "";
        return;
      }}
      const suggestions = currentGraph.nodes
        .filter(node => matchesQuery(node))
        .slice(0, 8);
      if (!suggestions.length) {{
        searchSuggestions.classList.remove("active");
        searchSuggestions.innerHTML = "";
        return;
      }}
      searchSuggestions.innerHTML = suggestions.map(node => `
        <button class="suggestion-item" type="button" data-path="${{escapeHtml(node.path)}}">
          ${{escapeHtml(node.label)}}
          <small>${{escapeHtml(node.path)}}</small>
        </button>
      `).join("");
      searchSuggestions.classList.add("active");
      searchSuggestions.querySelectorAll(".suggestion-item").forEach(button => {{
        button.addEventListener("click", () => {{
          searchBox.value = button.dataset.path;
          searchSuggestions.classList.remove("active");
          searchSuggestions.innerHTML = "";
          updateView();
        }});
      }});
    }}

    function diversifyRecommendations(recs, limit) {{
      const grouped = new Map();
      recs.forEach(rec => {{
        if (!grouped.has(rec.sourceId)) grouped.set(rec.sourceId, []);
        grouped.get(rec.sourceId).push(rec);
      }});
      const queues = [...grouped.values()].map(items => items.sort((a, b) => b.confidence - a.confidence));
      queues.sort((a, b) => (b[0]?.confidence || 0) - (a[0]?.confidence || 0));
      const picked = [];
      while (picked.length < limit && queues.some(queue => queue.length)) {{
        queues.forEach(queue => {{
          if (queue.length && picked.length < limit) picked.push(queue.shift());
        }});
      }}
      return picked;
    }}

    function scoreRecommendation(sourceNode, targetNode, targetType) {{
      const sourceTokens = getNodeTokens(sourceNode);
      const targetTokens = getNodeTokens(targetNode);
      const tokenOverlap = intersectionCount(sourceTokens, targetTokens);
      const sharedIncoming = intersectionCount(
        [...(graphCaches.incomingSourcesByTarget.get(sourceNode.id) || new Set())],
        [...(graphCaches.incomingSourcesByTarget.get(targetNode.id) || new Set())]
      );
      const sharedOutgoing = intersectionCount(
        [...(graphCaches.outgoingTargetsBySource.get(sourceNode.id) || new Set())],
        [...(graphCaches.outgoingTargetsBySource.get(targetNode.id) || new Set())]
      );
      const sameGroup = sourceNode.group === targetNode.group ? 1 : 0;
      const sameLeadPath = sourceNode.path.split("/").slice(1, 3).join("/") === targetNode.path.split("/").slice(1, 3).join("/") ? 1 : 0;
      const similarPagesLinkingTarget = [...(graphCaches.incomingSourcesByTarget.get(targetNode.id) || new Set())]
        .map(sourceId => nodesById.get(sourceId))
        .filter(node => node && node.id !== sourceNode.id && intersectionCount(sourceTokens, getNodeTokens(node)) >= 2).length;
      const targetImportance = Math.min(12, Math.round((targetNode.in + targetNode.degree) / 12));
      const rawScore =
        tokenOverlap * 18 +
        sharedIncoming * 4 +
        sharedOutgoing * 4 +
        sameGroup * 8 +
        sameLeadPath * 10 +
        similarPagesLinkingTarget * 6 +
        targetImportance;
      const confidence = Math.min(99, Math.round(rawScore));
      const reasons = [];
      if (tokenOverlap) reasons.push(`Shares topic terms: ${{targetTokens.filter(token => sourceTokens.includes(token)).slice(0, 4).join(", ")}}`);
      if (sameGroup || sameLeadPath) reasons.push("Sits in the same content cluster or adjacent folder structure.");
      if (sharedIncoming || sharedOutgoing) reasons.push(`Has a similar internal-link neighborhood (${{sharedIncoming + sharedOutgoing}} shared link relationships).`);
      if (similarPagesLinkingTarget) reasons.push(`${{similarPagesLinkingTarget}} related page${{similarPagesLinkingTarget === 1 ? "" : "s"}} already link to this target.`);
      reasons.push(targetType === "blog-blog"
        ? `Target already attracts ${{formatNumber(targetNode.in)}} incoming internal links from relevant pages.`
        : `Commercial target has ${{formatNumber(targetNode.in)}} incoming internal links and likely deserves stronger blog support.`);
      return {{ confidence, reasons: reasons.slice(0, 4) }};
    }}

    function buildRecommendations(scopeNodes) {{
      if ((currentGraph.meta.importType || "ahrefs") === "sitemap") {{
        recommendationState = {{
          "blog-blog": [],
          "blog-money": [],
          "indexing-cleanup": []
        }};
        return;
      }}
      const limit = Number(recommendationLimit.value);
      const threshold = Number(recommendationThreshold.value);
      const scopedNodes = (scopeNodes && scopeNodes.length ? scopeNodes : (viewNodes.length ? viewNodes : currentGraph.nodes));
      const focusedScope = matchedSearchIds.size > 0;
      const sourceCandidates = (scopedNodes.filter(node => isImportantBlogNode(node) && !node.sourceNoindex).length
        ? scopedNodes.filter(node => isImportantBlogNode(node) && !node.sourceNoindex)
        : viewNodes.filter(node => isImportantBlogNode(node) && !node.sourceNoindex)
      );
      const blogTargets = (focusedScope ? scopedNodes : viewNodes).filter(node => isImportantBlogNode(node) && !node.targetNoindex);
      const moneyTargets = (focusedScope ? scopedNodes : currentGraph.nodes).filter(node => isMoneyPageNode(node) && !node.targetNoindex);
      const indexingTargets = scopedNodes
        .filter(node => isLowValueNode(node) && !node.targetNoindex)
        .map(node => {{
          const incomingEdges = currentGraph.edges.filter(edge => edge.target === node.id && !edge.targetNoindex);
          const visibleSources = incomingEdges.filter(edge => !isLowValueNode(nodesById.get(edge.source) || {{ path: "" }}));
          let confidence = 58;
          if (isBlogPaginationNode(node) || isBlogAuthorNode(node) || isBlogDateArchiveNode(node)) confidence = 86;
          else if (isBlogRootNode(node)) confidence = 68;
          else if (isUtilityLowValueNode(node)) confidence = 82;
          return {{
            type: "indexing-cleanup",
            nodeId: node.id,
            nodeLabel: node.label,
            nodePath: node.path,
            confidence,
            reasons: [
              getIndexingCleanupReason(node),
              `This URL currently has ${{formatNumber(node.in)}} incoming internal links in the retained graph.`,
              visibleSources.length
                ? `${{formatNumber(visibleSources.length)}} non-low-value page${{visibleSources.length === 1 ? "" : "s"}} still point to it internally.`
                : "It does not appear to be a strong destination from valuable retained pages."
            ].slice(0, 3)
          }};
        }})
        .sort((a, b) => b.confidence - a.confidence || b.reasons.length - a.reasons.length)
        .slice(0, limit);

      const collect = (targets, targetType) => {{
        const recs = [];
        sourceCandidates.forEach(sourceNode => {{
          targets.forEach(targetNode => {{
            if (!targetNode || sourceNode.id === targetNode.id) return;
            if (graphCaches.edgeKeySet.has(`${{sourceNode.id}}|||${{targetNode.id}}`)) return;
            const score = scoreRecommendation(sourceNode, targetNode, targetType);
            if (score.confidence < threshold) return;
            recs.push({{
              type: targetType,
              sourceId: sourceNode.id,
              targetId: targetNode.id,
              sourceLabel: sourceNode.label,
              targetLabel: targetNode.label,
              sourcePath: sourceNode.path,
              targetPath: targetNode.path,
              confidence: score.confidence,
              reasons: score.reasons
            }});
          }});
        }});
        return diversifyRecommendations(
          recs.sort((a, b) => b.confidence - a.confidence || a.sourceLabel.localeCompare(b.sourceLabel)),
          limit
        );
      }};

      recommendationState = {{
        "blog-blog": collect(blogTargets, "blog-blog"),
        "blog-money": collect(moneyTargets, "blog-money"),
        "indexing-cleanup": indexingTargets
      }};
    }}

    function renderRecommendations() {{
      recommendationTabs.querySelectorAll("button").forEach(button => {{
        button.classList.toggle("active", button.dataset.type === activeRecommendationType);
      }});
      const recs = recommendationState[activeRecommendationType] || [];
      if (!recs.length) {{
        recommendationList.innerHTML = `<div class="recommendation-empty">No recommendations cleared the current threshold in this view yet. Broaden the filters, lower the threshold, or switch recommendation type.</div>`;
        return;
      }}
      if (activeRecommendationType !== "indexing-cleanup") {{
        const grouped = new Map();
        recs.forEach(rec => {{
          if (!grouped.has(rec.sourceId)) grouped.set(rec.sourceId, []);
          grouped.get(rec.sourceId).push(rec);
        }});
        recommendationList.innerHTML = [...grouped.entries()].map(([_sourceId, items]) => {{
          const source = items[0];
          const itemMarkup = items.map(rec => `
            <div class="recommendation-item">
              <div class="recommendation-meta">
                <span class="recommendation-badge">${{rec.type === "blog-blog" ? "Blog -> Blog" : "Blog -> Money"}}</span>
                <span class="recommendation-badge">${{rec.confidence}} confidence</span>
                <span></span>
              </div>
              <strong>${{escapeHtml(rec.targetLabel)}}</strong>
              <div class="recommendation-pair">${{escapeHtml(rec.targetPath)}}</div>
              <ul class="recommendation-reasons">${{rec.reasons.map(reason => `<li>${{escapeHtml(reason)}}</li>`).join("")}}</ul>
            </div>
          `).join("");
          return `
            <article class="recommendation-group">
              <strong>${{escapeHtml(source.sourceLabel)}}</strong>
              <div class="recommendation-pair">${{escapeHtml(source.sourcePath)}}</div>
              <div class="recommendation-group-items">${{itemMarkup}}</div>
            </article>
          `;
        }}).join("");
        return;
      }}
      recommendationList.innerHTML = recs.map(rec => {{
        if (rec.type === "indexing-cleanup") {{
          return `
            <article class="recommendation-card">
              <div class="recommendation-meta">
                <span class="recommendation-badge">Indexing cleanup</span>
                <span class="recommendation-badge">${{rec.confidence}} confidence</span>
                <span></span>
              </div>
              <strong>${{escapeHtml(rec.nodeLabel)}} should likely be noindex</strong>
              <div class="recommendation-pair">${{escapeHtml(rec.nodePath)}}</div>
              <ul class="recommendation-reasons">${{rec.reasons.map(reason => `<li>${{escapeHtml(reason)}}</li>`).join("")}}</ul>
            </article>
          `;
        }}
        return `
          <article class="recommendation-card">
            <div class="recommendation-meta">
              <span class="recommendation-badge">${{rec.type === "blog-blog" ? "Blog -> Blog" : "Blog -> Money"}}</span>
              <span class="recommendation-badge">${{rec.confidence}} confidence</span>
              <span></span>
            </div>
            <strong>${{escapeHtml(rec.sourceLabel)}} -> ${{escapeHtml(rec.targetLabel)}}</strong>
            <div class="recommendation-pair">${{escapeHtml(rec.sourcePath)}} -> ${{escapeHtml(rec.targetPath)}}</div>
            <ul class="recommendation-reasons">${{rec.reasons.map(reason => `<li>${{escapeHtml(reason)}}</li>`).join("")}}</ul>
          </article>
        `;
      }}).join("");
    }}

    function renderMatchSummary(query) {{
      const wasActive = canvasShell.classList.contains("summary-active");
      if (!query || !matchedSearchIds.size) {{
        canvasShell.classList.remove("summary-active");
        matchSummary.innerHTML = "";
        if (wasActive) requestAnimationFrame(resizeCanvas);
        return;
      }}
      const direction = directionFilter.value;
      const rowsFor = mode => viewEdges
        .filter(edge => mode === "in" ? matchedSearchIds.has(edge.target) : matchedSearchIds.has(edge.source))
        .slice()
        .sort((a, b) => b.count - a.count || a.target.localeCompare(b.target))
        .slice(0, 24);

      const renderRows = (rows, mode) => {{
        if (!rows.length) return `<div class="summary-empty">No visible links match the current direction and path filters.</div>`;
        const rowMarkup = rows.map(edge => {{
          const source = nodesById.get(edge.source);
          const target = nodesById.get(edge.target);
          const title = mode === "in"
            ? `${{escapeHtml(source?.label || edge.source)}} -> ${{escapeHtml(target?.label || edge.target)}}`
            : `${{escapeHtml(source?.label || edge.source)}} -> ${{escapeHtml(target?.label || edge.target)}}`;
          const path = mode === "in"
            ? `${{escapeHtml(source?.path || edge.source)}}`
            : `${{escapeHtml(target?.path || edge.target)}}`;
          const anchors = (edge.anchors || []).map(anchor => anchor.text).join(", ") || "No anchors captured";
          return `<div class="summary-row"><strong>${{title}}</strong><span>${{path}}</span><span>Anchors: ${{escapeHtml(anchors)}}</span><span>Visible link count: ${{formatNumber(edge.count)}}</span></div>`;
        }}).join("");
        return `<div class="summary-table">${{rowMarkup}}</div>`;
      }};

      let body = "";
      if (direction === "in") {{
        body = `<div class="summary-group"><h3>Links Pointing To Matches</h3>${{renderRows(rowsFor("in"), "in")}}</div>`;
      }} else if (direction === "out") {{
        body = `<div class="summary-group"><h3>Links From Matches</h3>${{renderRows(rowsFor("out"), "out")}}</div>`;
      }} else {{
        body = `
          <div class="summary-group"><h3>Links Pointing To Matches</h3>${{renderRows(rowsFor("in"), "in")}}</div>
          <div class="summary-group"><h3>Links From Matches</h3>${{renderRows(rowsFor("out"), "out")}}</div>
        `;
      }}

      canvasShell.classList.add("summary-active");
      matchSummary.innerHTML = `<h2>Focused link summary</h2><p>Visible links for <strong>${{escapeHtml(query)}}</strong>, based on the current direction and path filters.</p>${{body}}`;
      if (!wasActive) requestAnimationFrame(resizeCanvas);
    }}

    function applyNonNetworkLayout() {{
      const rect = stage.getBoundingClientRect();
      if (!viewNodes.length) return;
      if (viewMode.value === "cluster") {{
        const groups = [...new Set(viewNodes.map(node => node.group))];
        const columns = new Map(groups.map((group, index) => [group, index]));
        const buckets = new Map(groups.map(group => [group, viewNodes.filter(node => node.group === group)]));
        const colWidth = rect.width / Math.max(1, groups.length);
        groups.forEach(group => {{
          const nodes = buckets.get(group) || [];
          nodes.forEach((node, index) => {{
            node.x = colWidth * columns.get(group) + colWidth / 2;
            node.y = 70 + index * Math.max(34, (rect.height - 120) / Math.max(1, nodes.length));
          }});
        }});
      }} else if (viewMode.value === "tree") {{
        const roots = matchedSearchIds.size
          ? viewNodes.filter(node => matchedSearchIds.has(node.id))
          : selectedIds.size
            ? viewNodes.filter(node => selectedIds.has(node.id))
            : viewNodes.slice().sort((a, b) => b.degree - a.degree).slice(0, 1);
        const levelMap = new Map();
        const queue = roots.map(node => [node.id, 0]);
        queue.forEach(([id, level]) => levelMap.set(id, level));
        while (queue.length) {{
          const [nodeId, level] = queue.shift();
          const neighbors = viewEdges
            .filter(edge => directionFilter.value === "in" ? edge.target === nodeId : edge.source === nodeId || (directionFilter.value === "all" && edge.target === nodeId))
            .map(edge => directionFilter.value === "in" ? edge.source : edge.source === nodeId ? edge.target : edge.source);
          neighbors.forEach(neighborId => {{
            if (!levelMap.has(neighborId)) {{
              levelMap.set(neighborId, level + 1);
              queue.push([neighborId, level + 1]);
            }}
          }});
        }}
        const maxLevel = Math.max(...[...levelMap.values(), 0]);
        const columns = new Map();
        viewNodes.forEach(node => {{
          const level = levelMap.has(node.id) ? levelMap.get(node.id) : maxLevel + 1;
          if (!columns.has(level)) columns.set(level, []);
          columns.get(level).push(node);
        }});
        const levels = [...columns.keys()].sort((a, b) => a - b);
        levels.forEach((level, levelIndex) => {{
          const nodes = columns.get(level) || [];
          nodes.sort((a, b) => a.label.localeCompare(b.label));
          const x = 80 + levelIndex * ((rect.width - 160) / Math.max(1, levels.length - 1 || 1));
          nodes.forEach((node, index) => {{
            node.x = x;
            node.y = 70 + index * Math.max(32, (rect.height - 120) / Math.max(1, nodes.length));
          }});
        }});
      }}
      viewNodes.forEach(node => {{
        node.vx = 0;
        node.vy = 0;
      }});
      fitGraphToViewport();
      draw();
    }}

    function setGraph(graph, fileName) {{
      currentGraph = graph;
      syncGraphState();
      setupControls();
      sectionFilter.value = "";
      searchBox.value = "";
      sourcePathFilter.value = "";
      targetPathFilter.value = "";
      directionFilter.value = "all";
      sourceNoindexFilter.value = "";
      targetNoindexFilter.value = "";
      sourceStatusFilter.value = "";
      targetStatusFilter.value = "";
      minDegree.value = 20;
      globalLinkMode.value = "dim";
      componentLinkMode.value = "dim";
      sitewideThreshold.value = 80;
      transform = {{ x: 0, y: 0, scale: 1 }};
      selectedIds = new Set();
      hovered = null;
      tooltipPinned = false;
      focusPanelDismissed = false;
      lastFocusQuery = "";
      tooltip.style.opacity = 0;
      searchSuggestions.classList.remove("active");
      searchSuggestions.innerHTML = "";
      canvasShell.classList.remove("summary-active");
      matchSummary.innerHTML = "";
      updateView();
    }}

    function resizeCanvas() {{
      const rect = stage.getBoundingClientRect();
      const ratio = window.devicePixelRatio || 1;
      canvas.width = Math.max(1, Math.floor(rect.width * ratio));
      canvas.height = Math.max(1, Math.floor(rect.height * ratio));
      canvas.style.width = rect.width + "px";
      canvas.style.height = rect.height + "px";
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
      draw();
    }}

    function fitGraphToViewport(padding = 36) {{
      if (!viewNodes.length) return;
      const rect = stage.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      const minX = Math.min(...viewNodes.map(node => node.x - node.radius));
      const maxX = Math.max(...viewNodes.map(node => node.x + node.radius));
      const minY = Math.min(...viewNodes.map(node => node.y - node.radius));
      const maxY = Math.max(...viewNodes.map(node => node.y + node.radius));
      const graphWidth = Math.max(1, maxX - minX);
      const graphHeight = Math.max(1, maxY - minY);
      const availableWidth = Math.max(1, rect.width - padding * 2);
      const availableHeight = Math.max(1, rect.height - padding * 2);
      const nextScale = Math.max(0.7, Math.min(2.2, Math.min(availableWidth / graphWidth, availableHeight / graphHeight)));
      const graphCenterX = (minX + maxX) / 2;
      const graphCenterY = (minY + maxY) / 2;
      transform.scale = nextScale;
      transform.x = rect.width / 2 - graphCenterX * nextScale;
      transform.y = rect.height / 2 - graphCenterY * nextScale;
    }}

    function updateView() {{
      const section = sectionFilter.value;
      const rawQuery = searchBox.value.trim();
      const query = normalizeSearchText(rawQuery);
      const sourcePathQuery = normalizeSearchText(sourcePathFilter.value.trim());
      const targetPathQuery = normalizeSearchText(targetPathFilter.value.trim());
      const direction = directionFilter.value;
      const sourceNoindex = sourceNoindexFilter.value;
      const targetNoindex = targetNoindexFilter.value;
      const sourceStatusCode = sourceStatusFilter.value;
      const targetStatusCode = targetStatusFilter.value;
      const limit = Number(nodeLimit.value);
      const degree = Number(minDegree.value);
      const globalMode = globalLinkMode.value;
      const componentMode = componentLinkMode.value;
      const shouldHideSitewide = globalMode === "hide";
      const shouldMarkSitewide = globalMode !== "show";
      const shouldHideComponents = componentMode === "hide";
      const sitewideShare = Number(sitewideThreshold.value) / 100;
      document.getElementById("nodeLimitValue").textContent = limit;
      document.getElementById("minDegreeValue").textContent = degree;
      document.getElementById("sitewideThresholdValue").textContent = `${{sitewideThreshold.value}}%`;
      document.getElementById("sectionCount").textContent = section || "all";
      document.getElementById("searchCount").textContent = query ? "active" : "optional";
      document.getElementById("directionCount").textContent = query ? direction : "all";
      document.getElementById("sourcePathCount").textContent = sourcePathQuery ? "active" : "optional";
      document.getElementById("targetPathCount").textContent = targetPathQuery ? "active" : "optional";
      document.getElementById("globalLinkModeCount").textContent = globalMode;
      document.getElementById("componentLinkModeCount").textContent = componentMode;
      document.getElementById("sourceNoindexCount").textContent = sourceNoindex || "all";
      document.getElementById("targetNoindexCount").textContent = targetNoindex || "all";
      document.getElementById("sourceStatusCount").textContent = sourceStatusCode || "all";
      document.getElementById("targetStatusCount").textContent = targetStatusCode || "all";
      if (query !== lastFocusQuery) {{
        focusPanelDismissed = false;
        lastFocusQuery = query;
      }}

      const matchPriority = new Map([
        ["exact", 0],
        ["locale-root", 1],
        ["descendant", 2],
        ["text", 3]
      ]);
      const getQueryMatchType = node => getPathSearchMatchType(node, rawQuery);
      const matchesQuery = node => Boolean(getQueryMatchType(node));
      const matchesSourcePath = edge => !sourcePathQuery || normalizeSearchText(edge.source + " " + (nodesById.get(edge.source)?.path || "") + " " + (nodesById.get(edge.source)?.label || "")).includes(sourcePathQuery);
      const matchesTargetPath = edge => !targetPathQuery || normalizeSearchText(edge.target + " " + (nodesById.get(edge.target)?.path || "") + " " + (nodesById.get(edge.target)?.label || "")).includes(targetPathQuery);
      renderSearchSuggestions(rawQuery, matchesQuery);
      let candidates;
      matchedSearchIds = new Set();
      focusedSearchNodes = [];
      if (query) {{
        const matchedNodes = currentGraph.nodes
          .filter(node => (!section || node.group === section))
          .map(node => ({{ node, matchType: getQueryMatchType(node) }}))
          .filter(item => item.matchType);
        const preferredMatches = matchedNodes.filter(item => item.matchType === "exact" || item.matchType === "locale-root");
        const rootScopedMatch = preferredMatches.length >= 2;
        const directMatches = (preferredMatches.length ? preferredMatches : matchedNodes)
          .slice()
          .sort((a, b) => {{
            const priorityDiff = (matchPriority.get(a.matchType) ?? 9) - (matchPriority.get(b.matchType) ?? 9);
            if (priorityDiff) return priorityDiff;
            return b.node.degree - a.node.degree;
          }})
          .map(item => item.node);
        focusedSearchNodes = matchedNodes
          .slice()
          .sort((a, b) => {{
            const priorityDiff = (matchPriority.get(a.matchType) ?? 9) - (matchPriority.get(b.matchType) ?? 9);
            if (priorityDiff) return priorityDiff;
            return b.node.degree - a.node.degree;
          }})
          .map(item => item.node);
        matchedSearchIds = new Set(directMatches.map(node => node.id));
        const expandedIds = new Set(matchedSearchIds);
        if (rootScopedMatch) {{
          const neighborLimit = 6;
          directMatches.forEach(node => {{
            if (direction === "all" || direction === "out") {{
              currentGraph.edges
                .filter(edge => edge.source === node.id)
                .sort((a, b) => b.count - a.count)
                .slice(0, neighborLimit)
                .forEach(edge => expandedIds.add(edge.target));
            }}
            if (direction === "all" || direction === "in") {{
              currentGraph.edges
                .filter(edge => edge.target === node.id)
                .sort((a, b) => b.count - a.count)
                .slice(0, neighborLimit)
                .forEach(edge => expandedIds.add(edge.source));
            }}
          }});
        }} else {{
          currentGraph.edges.forEach(edge => {{
            if ((direction === "all" || direction === "out") && matchedSearchIds.has(edge.source)) expandedIds.add(edge.target);
            if ((direction === "all" || direction === "in") && matchedSearchIds.has(edge.target)) expandedIds.add(edge.source);
          }});
        }}
        candidates = currentGraph.nodes
          .filter(node => expandedIds.has(node.id))
          .sort((a, b) => {{
            const aMatched = matchedSearchIds.has(a.id) ? 1 : 0;
            const bMatched = matchedSearchIds.has(b.id) ? 1 : 0;
            if (aMatched !== bMatched) return bMatched - aMatched;
            return b.degree - a.degree;
          }});
      }} else {{
        candidates = currentGraph.nodes.filter(node => node.degree >= degree);
        if (section) candidates = candidates.filter(node => node.group === section);
        candidates = candidates.slice().sort((a, b) => b.degree - a.degree).slice(0, limit);
      }}
      const ids = new Set(candidates.map(node => node.id));
      viewEdges = currentGraph.edges.filter(edge =>
        ids.has(edge.source) &&
        ids.has(edge.target) &&
        (!query || direction === "all" || (direction === "out" && matchedSearchIds.has(edge.source)) || (direction === "in" && matchedSearchIds.has(edge.target))) &&
        matchesSourcePath(edge) &&
        matchesTargetPath(edge) &&
        (!sourceNoindex || String(edge.sourceNoindex) === sourceNoindex) &&
        (!targetNoindex || String(edge.targetNoindex) === targetNoindex) &&
        (!sourceStatusCode || String(edge.sourceStatusCode) === sourceStatusCode) &&
        (!targetStatusCode || String(edge.targetStatusCode) === targetStatusCode) &&
        (!shouldHideSitewide || edge.anchorSourceShare < sitewideShare) &&
        (!shouldHideComponents || !edge.componentLike)
      );
      const linkedIds = new Set(shouldHideSitewide ? [] : ids);
      viewEdges.forEach(edge => {{
        linkedIds.add(edge.source);
        linkedIds.add(edge.target);
      }});
      const hiddenCount = currentGraph.edges.filter(edge =>
        ids.has(edge.source) &&
        ids.has(edge.target) &&
        (!query || direction === "all" || (direction === "out" && matchedSearchIds.has(edge.source)) || (direction === "in" && matchedSearchIds.has(edge.target))) &&
        (!sourceNoindex || String(edge.sourceNoindex) === sourceNoindex) &&
        (!targetNoindex || String(edge.targetNoindex) === targetNoindex) &&
        (!sourceStatusCode || String(edge.sourceStatusCode) === sourceStatusCode) &&
        (!targetStatusCode || String(edge.targetStatusCode) === targetStatusCode) &&
        edge.anchorSourceShare >= sitewideShare
      ).length;
      const componentCount = currentGraph.edges.filter(edge =>
        ids.has(edge.source) &&
        ids.has(edge.target) &&
        (!query || direction === "all" || (direction === "out" && matchedSearchIds.has(edge.source)) || (direction === "in" && matchedSearchIds.has(edge.target))) &&
        (!sourceNoindex || String(edge.sourceNoindex) === sourceNoindex) &&
        (!targetNoindex || String(edge.targetNoindex) === targetNoindex) &&
        (!sourceStatusCode || String(edge.sourceStatusCode) === sourceStatusCode) &&
        (!targetStatusCode || String(edge.targetStatusCode) === targetStatusCode) &&
        edge.componentLike
      ).length;
      document.getElementById("sitewideHiddenCount").textContent = globalMode === "hide"
        ? `${{formatNumber(hiddenCount)}} visible-scope pairs hidden at this threshold.`
        : globalMode === "dim"
          ? `${{formatNumber(hiddenCount)}} repeated target-and-anchor pairs muted at this threshold.`
          : "All repeated patterns are visible at full strength.";
      componentHint.textContent = componentMode === "hide"
        ? `${{formatNumber(componentCount)}} likely component-driven pairs hidden in this view.`
        : componentMode === "dim"
          ? `${{formatNumber(componentCount)}} likely component-driven pairs muted so body-copy links are easier to scan.`
          : "All likely related-post, related-product, preview-card, and CTA patterns are visible at full strength.";
      viewNodes = candidates.filter(node => linkedIds.has(node.id) || matchedSearchIds.has(node.id)).map(node => ({{
        ...node,
        x: node.x ?? Math.random() * stage.clientWidth,
        y: node.y ?? Math.random() * stage.clientHeight,
        vx: 0,
        vy: 0,
        radius: Math.max(5, Math.min(18, 4 + Math.sqrt(node.degree) / 3))
      }}));

      empty.style.display = viewNodes.length ? "none" : "flex";
      setMetrics();
      const recommendationScopeNodes = query
        ? currentGraph.nodes.filter(node => matchesQuery(node) && (!section || node.group === section))
        : section
          ? currentGraph.nodes.filter(node => node.group === section)
          : currentGraph.nodes;
      buildRecommendations(recommendationScopeNodes);
      renderFocusPanel(query);
      renderMatchSummary(query);
      renderTopPages();
      renderRecommendations();
      transform = {{ x: 0, y: 0, scale: 1 }};
      if (viewMode.value === "network") startSimulation();
      else applyNonNetworkLayout();
    }}

    function renderFocusPanel(query) {{
      if (!query || focusPanelDismissed) {{
        focusPanel.style.display = "none";
        focusPanel.innerHTML = "";
        return;
      }}

      const visibleMatched = focusedSearchNodes.filter(node => viewNodes.some(viewNode => viewNode.id === node.id));
      const chips = visibleMatched.slice(0, 8)
        .map(node => `<button class="focus-chip" data-id="${{node.id}}" title="${{node.path}}">${{node.label}}</button>`)
        .join("");
      const extra = visibleMatched.length > 8 ? ` +${{visibleMatched.length - 8}} more` : "";
      const directionText = directionFilter.value === "out" ? "showing links from matched pages" : directionFilter.value === "in" ? "showing links pointing to matched pages" : "showing links to and from matched pages";
      focusPanel.innerHTML = `<div class="focus-panel-header"><div><strong>Focused search: ${{query}}</strong><p>${{formatNumber(visibleMatched.length)}} matched page${{visibleMatched.length === 1 ? "" : "s"}} highlighted; ${{directionText}}.${{extra}}</p></div><button class="focus-close" id="focusClose" type="button" aria-label="Close focused search panel">&times;</button></div><div class="focus-chips">${{chips}}</div>`;
      focusPanel.style.display = "block";
      document.getElementById("focusClose").addEventListener("click", () => {{
        focusPanelDismissed = true;
        renderFocusPanel(query);
      }});
      focusPanel.querySelectorAll(".focus-chip").forEach(chip => {{
        chip.addEventListener("click", () => {{
          const node = currentGraph.nodes.find(item => item.id === chip.dataset.id);
          if (!node) return;
          searchBox.value = node.path;
          focusPanelDismissed = true;
          selectedIds = new Set();
          hovered = null;
          tooltipPinned = false;
          tooltip.style.opacity = 0;
          updateView();
        }});
      }});
    }}

    function renderTopPages() {{
      topPages.innerHTML = viewNodes
        .slice()
        .sort((a, b) => b.degree - a.degree)
        .slice(0, 12)
        .map(node => `<div class="page-row" data-id="${{node.id}}"><strong>${{node.label}}</strong><span>${{formatNumber(node.degree)}}</span><span>${{node.path}}</span><span>in ${{formatNumber(node.in)}} / out ${{formatNumber(node.out)}}</span></div>`)
        .join("");
      topPages.querySelectorAll(".page-row").forEach(row => {{
        row.addEventListener("click", () => {{
          selectedIds = new Set([row.dataset.id]);
          tooltipPinned = true;
          draw();
          showTooltip(stage.clientWidth / 2, 24);
        }});
      }});
    }}

    function startSimulation() {{
      simulationId += 1;
      const current = simulationId;
      const rect = stage.getBoundingClientRect();
      const nodeMap = new Map(viewNodes.map(node => [node.id, node]));
      const matchedNodeIds = [...matchedSearchIds];
      const matchedCount = matchedNodeIds.length;
      const matchedIndexById = new Map(matchedNodeIds.map((id, index) => [id, index]));
      const links = viewEdges.map(edge => ({{
        ...edge,
        sourceNode: nodeMap.get(edge.source),
        targetNode: nodeMap.get(edge.target)
      }})).filter(edge => edge.sourceNode && edge.targetNode);

      viewNodes.forEach((node, index) => {{
        const isMatched = matchedSearchIds.has(node.id);
        const angle = (index / Math.max(1, viewNodes.length)) * Math.PI * 2;
        if (isMatched && matchedCount > 1) {{
          const matchedIndex = matchedIndexById.get(node.id) || 0;
          const matchedAngle = (matchedIndex / matchedCount) * Math.PI * 2;
          const ringRadius = Math.min(rect.width, rect.height) * Math.max(0.18, Math.min(0.3, 0.12 + matchedCount * 0.012));
          node.x = rect.width / 2 + Math.cos(matchedAngle) * ringRadius;
          node.y = rect.height / 2 + Math.sin(matchedAngle) * ringRadius;
        }} else {{
          const spread = isMatched ? 0.14 : 0.36;
          node.x = rect.width / 2 + Math.cos(angle) * Math.min(rect.width, rect.height) * spread * Math.random();
          node.y = rect.height / 2 + Math.sin(angle) * Math.min(rect.width, rect.height) * spread * Math.random();
        }}
      }});
      fitGraphToViewport();

      let alpha = 1;
      function tick() {{
        if (current !== simulationId) return;
        alpha *= 0.985;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        for (let i = 0; i < viewNodes.length; i++) {{
          const a = viewNodes[i];
          for (let j = i + 1; j < viewNodes.length; j++) {{
            const b = viewNodes[j];
            const dx = a.x - b.x || 0.01;
            const dy = a.y - b.y || 0.01;
            const dist2 = dx * dx + dy * dy;
            const force = Math.min(1.5, 850 / dist2) * alpha;
            a.vx += dx * force;
            a.vy += dy * force;
            b.vx -= dx * force;
            b.vy -= dy * force;
          }}
        }}

        links.forEach(link => {{
          const a = link.sourceNode;
          const b = link.targetNode;
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const distance = Math.sqrt(dx * dx + dy * dy) || 1;
          const desired = 80 + Math.max(0, 22 - Math.min(a.degree, b.degree) / 8);
          const force = (distance - desired) * 0.006 * alpha;
          const fx = dx / distance * force;
          const fy = dy / distance * force;
          a.vx += fx;
          a.vy += fy;
          b.vx -= fx;
          b.vy -= fy;
        }});

        viewNodes.forEach(node => {{
          if (node === dragNode) return;
          const isMatched = matchedSearchIds.has(node.id);
          if (isMatched && matchedCount > 1) {{
            const matchedIndex = matchedIndexById.get(node.id) || 0;
            const matchedAngle = (matchedIndex / matchedCount) * Math.PI * 2;
            const ringRadius = Math.min(rect.width, rect.height) * Math.max(0.18, Math.min(0.3, 0.12 + matchedCount * 0.012));
            const targetX = centerX + Math.cos(matchedAngle) * ringRadius;
            const targetY = centerY + Math.sin(matchedAngle) * ringRadius;
            node.vx += (targetX - node.x) * 0.012 * alpha;
            node.vy += (targetY - node.y) * 0.012 * alpha;
          }} else {{
            const centerPull = isMatched ? 0.006 : matchedSearchIds.size ? 0.0014 : 0.002;
            node.vx += (centerX - node.x) * centerPull * alpha;
            node.vy += (centerY - node.y) * centerPull * alpha;
          }}
          node.vx *= 0.82;
          node.vy *= 0.82;
          node.x = Math.max(20, Math.min(rect.width - 20, node.x + node.vx));
          node.y = Math.max(20, Math.min(rect.height - 20, node.y + node.vy));
        }});

        draw();
        if (alpha > 0.025) requestAnimationFrame(tick);
        else {{
          fitGraphToViewport();
          draw();
        }}
      }}
      tick();
    }}

    function toScreen(node) {{
      return {{
        x: node.x * transform.scale + transform.x,
        y: node.y * transform.scale + transform.y
      }};
    }}

    function toWorld(x, y) {{
      return {{
        x: (x - transform.x) / transform.scale,
        y: (y - transform.y) / transform.scale
      }};
    }}

    function draw() {{
      const rect = stage.getBoundingClientRect();
      ctx.clearRect(0, 0, rect.width, rect.height);
      ctx.save();
      ctx.translate(transform.x, transform.y);
      ctx.scale(transform.scale, transform.scale);

      const nodeMap = new Map(viewNodes.map(node => [node.id, node]));
      const selectedNodes = getSelectedNodes();
      const active = hovered || selectedNodes[0] || null;
      const shouldMarkSitewide = globalLinkMode.value === "dim";
      const shouldMarkComponents = componentLinkMode.value === "dim";
      const sitewideShare = Number(sitewideThreshold.value) / 100;
      const activeLinks = new Set();
      if (selectedIds.size) {{
        viewEdges.forEach(edge => {{
          if (selectedIds.has(edge.source) || selectedIds.has(edge.target)) activeLinks.add(edge);
        }});
      }} else if (active) {{
        viewEdges.forEach(edge => {{
          if (edge.source === active.id || edge.target === active.id) activeLinks.add(edge);
        }});
      }}

      viewEdges.forEach(edge => {{
        const source = nodeMap.get(edge.source);
        const target = nodeMap.get(edge.target);
        if (!source || !target) return;
        const isActive = activeLinks.has(edge);
        const isFocusEdge = matchedSearchIds.has(edge.source) || matchedSearchIds.has(edge.target);
        const isGlobalEdge = shouldMarkSitewide && edge.anchorSourceShare >= sitewideShare;
        const isComponentEdge = shouldMarkComponents && edge.componentLike;
        ctx.beginPath();
        ctx.moveTo(source.x, source.y);
        ctx.lineTo(target.x, target.y);
        ctx.strokeStyle = isActive
          ? "rgba(184,58,58,0.95)"
          : isGlobalEdge
            ? "rgba(183,121,31,0.16)"
            : isComponentEdge
              ? "rgba(36,87,166,0.14)"
          : isFocusEdge
            ? "rgba(184,58,58,0.58)"
            : matchedSearchIds.size
              ? "rgba(23,35,38,0.045)"
              : "rgba(23,35,38,0.12)";
        ctx.lineWidth = isActive
          ? 2.3
          : isGlobalEdge
            ? 0.55
            : isComponentEdge
              ? 0.65
          : isFocusEdge
            ? 1.15
            : Math.max(0.35, Math.min(2.2, Math.sqrt(edge.count) * 0.45));
        ctx.stroke();
      }});

      viewNodes.forEach(node => {{
        const isSelected = selectedIds.has(node.id);
        const isActive = isSelected || node === hovered;
        const isMatched = matchedSearchIds.has(node.id);
        const connected = selectedIds.size
          ? viewEdges.some(edge =>
              (selectedIds.has(edge.source) && edge.target === node.id) ||
              (selectedIds.has(edge.target) && edge.source === node.id)
            )
          : active && viewEdges.some(edge =>
              (edge.source === active.id && edge.target === node.id) ||
              (edge.target === active.id && edge.source === node.id)
            );
        if (isMatched) {{
          ctx.beginPath();
          ctx.arc(node.x, node.y, node.radius + 10, 0, Math.PI * 2);
          ctx.fillStyle = "rgba(184,58,58,0.13)";
          ctx.fill();
          ctx.strokeStyle = "rgba(184,58,58,0.72)";
          ctx.lineWidth = 2.2;
          ctx.stroke();
        }}
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius + (isActive ? 3 : isMatched ? 2 : 0), 0, Math.PI * 2);
        ctx.fillStyle = groupColor.get(node.group) || "#64748b";
        ctx.globalAlpha = !active || isActive || connected || isMatched ? 1 : 0.28;
        ctx.fill();
        ctx.globalAlpha = 1;
        ctx.strokeStyle = isSelected ? "#172326" : isMatched ? "#b83a3a" : "#fff";
        ctx.lineWidth = isSelected ? 3.2 : isMatched ? 2.8 : 1.4;
        ctx.stroke();

        const shouldShowLabel = isActive || isMatched || node.degree > 220 || (matchedSearchIds.size && viewNodes.length <= 140);
        if (shouldShowLabel) {{
          ctx.font = `${{isMatched ? "700 " : ""}}12px Inter, system-ui, sans-serif`;
          ctx.fillStyle = "#172326";
          ctx.fillText(node.label.slice(0, 34), node.x + node.radius + 4, node.y + 4);
        }}
      }});

      ctx.restore();
    }}

    function findNodeAt(clientX, clientY) {{
      const rect = canvas.getBoundingClientRect();
      const point = toWorld(clientX - rect.left, clientY - rect.top);
      for (let i = viewNodes.length - 1; i >= 0; i--) {{
        const node = viewNodes[i];
        const dx = point.x - node.x;
        const dy = point.y - node.y;
        if (Math.sqrt(dx * dx + dy * dy) <= node.radius + 5) return node;
      }}
      return null;
    }}

    function summarizeAnchors(edges) {{
      const counts = new Map();
      edges.forEach(edge => {{
        (edge.anchors || []).forEach(anchor => {{
          counts.set(anchor.text, (counts.get(anchor.text) || 0) + anchor.count);
        }});
      }});
      return [...counts.entries()]
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([text, count]) => `<li>${{escapeHtml(text)}} <strong>(${{formatNumber(count)}})</strong></li>`)
        .join("");
    }}

    function showTooltip(x, y) {{
      const selectedNodes = getSelectedNodes();
      if (!selectedNodes.length) {{
        tooltip.style.opacity = 0;
        tooltip.classList.remove("pinned");
        return;
      }}
      if (selectedNodes.length === 1) {{
        const node = selectedNodes[0];
        const incomingEdges = viewEdges.filter(edge => edge.target === node.id);
        const outgoingEdges = viewEdges.filter(edge => edge.source === node.id);
        const topAnchors = summarizeAnchors([...incomingEdges, ...outgoingEdges]);
        tooltip.innerHTML = `<strong>${{escapeHtml(node.label)}}</strong><a href="${{node.id}}" target="_blank" rel="noopener">${{escapeHtml(node.id)}}</a><div class="small">Section: ${{escapeHtml(node.group)}}<br>Noindex: source ${{node.sourceNoindex ? "yes" : "no"}} / target ${{node.targetNoindex ? "yes" : "no"}}<br>Status: source ${{escapeHtml(node.sourceStatusCode || "n/a")}} / target ${{escapeHtml(node.targetStatusCode || "n/a")}}<br>All links: in ${{formatNumber(node.in)}} / out ${{formatNumber(node.out)}}<br>Linked from ${{formatNumber(node.targetSourcePages)}} of ${{formatNumber(currentGraph.meta.sourcePages)}} source pages<br>Visible pairs: in ${{formatNumber(incomingEdges.length)}} / out ${{formatNumber(outgoingEdges.length)}}</div>${{topAnchors ? `<div class="small"><strong>Top visible anchors</strong><ul>${{topAnchors}}</ul></div>` : ""}}`;
      }} else {{
        const linksBetween = getSelectedEdges();
        const directional = linksBetween
          .slice()
          .sort((a, b) => b.count - a.count)
          .slice(0, 8)
          .map(edge => {{
            const source = nodesById.get(edge.source);
            const target = nodesById.get(edge.target);
            const anchors = (edge.anchors || []).slice(0, 3).map(anchor => escapeHtml(anchor.text)).join(", ") || "No anchors captured";
            return `<li><strong>${{escapeHtml(source?.label || edge.source)}}</strong> -> <strong>${{escapeHtml(target?.label || edge.target)}}</strong><br>${{anchors}}</li>`;
          }})
          .join("");
        const topAnchors = summarizeAnchors(linksBetween);
        tooltip.innerHTML = `<strong>${{formatNumber(selectedNodes.length)}} pages selected</strong><div class="small">Hold <strong>Shift</strong> while clicking nodes to add or remove them from the current selection.<br>Visible links between selected pages: ${{formatNumber(linksBetween.length)}}</div>${{topAnchors ? `<div class="small"><strong>Top anchors between selected pages</strong><ul>${{topAnchors}}</ul></div>` : ""}}${{directional ? `<div class="small"><strong>Links between selected pages</strong><ul>${{directional}}</ul></div>` : `<div class="small">No visible links connect these selected pages in the current view.</div>`}}`;
      }}
      tooltip.style.left = Math.min(stage.clientWidth - 390, Math.max(4, x)) + "px";
      tooltip.style.top = Math.min(stage.clientHeight - 170, Math.max(4, y)) + "px";
      tooltip.style.opacity = 1;
      tooltip.classList.toggle("pinned", tooltipPinned);
    }}

    uploadInput.addEventListener("change", async event => {{
      const file = event.target.files?.[0];
      if (!file) return;
      try {{
        const buffer = await file.arrayBuffer();
        const text = decodeFileText(buffer);
        let graph;
        if (/\.xml$/i.test(file.name) || /^\s*</.test(text)) {{
          graph = parseSitemapGraphFromText(text, file.name);
        }} else {{
          const rows = parseDelimited(text, "\\t");
          if (rows.length < 2) throw new Error("The file did not contain enough rows to parse.");
          const headers = rows[0];
          const records = rows.slice(1).map(row => Object.fromEntries(headers.map((header, index) => [header, row[index] || ""])));
          if (!headers.includes("Source URL") || !headers.includes("Target URL")) {{
            throw new Error("This does not look like the Ahrefs internal links export.");
          }}
          graph = buildGraphFromRows(records, file.name);
        }}
        if (!graph.meta.uniquePages) throw new Error("No internal HTML pages were retained from this file.");
        setGraph(graph, file.name);
        saveUploadedGraph(graph, file.name);
      }} catch (error) {{
        console.error(error);
        window.alert(error.message || "Could not parse this file.");
      }} finally {{
        uploadInput.value = "";
      }}
    }});

    importSitemapUrl.addEventListener("click", async () => {{
      const url = sitemapUrlInput.value.trim();
      if (!url) return;
      try {{
        const xml = await fetchSitemapFromUrl(url);
        const graph = parseSitemapGraphFromText(xml, url);
        if (!graph.meta.uniquePages) throw new Error("No internal HTML pages were retained from this sitemap.");
        setGraph(graph, url);
        saveUploadedGraph(graph, url);
      }} catch (error) {{
        console.error(error);
        window.alert(error.message || "Could not import this sitemap URL.");
      }}
    }});

    sitemapUrlInput.addEventListener("keydown", event => {{
      if (event.key === "Enter") {{
        event.preventDefault();
        importSitemapUrl.click();
      }}
    }});

    canvas.addEventListener("mousemove", event => {{
      if (dragNode) {{
        const rect = canvas.getBoundingClientRect();
        const point = toWorld(event.clientX - rect.left, event.clientY - rect.top);
        dragNode.x = point.x;
        dragNode.y = point.y;
        draw();
        return;
      }}
      if (panStart) {{
        transform.x = panStart.x + event.clientX - panStart.clientX;
        transform.y = panStart.y + event.clientY - panStart.clientY;
        draw();
        return;
      }}
      if (tooltipPinned) return;
      hovered = findNodeAt(event.clientX, event.clientY);
      canvas.style.cursor = hovered ? "pointer" : "grab";
      draw();
      tooltip.style.opacity = 0;
    }});

    canvas.addEventListener("mouseleave", () => {{
      hovered = null;
      if (!selectedIds.size || !tooltipPinned) tooltip.style.opacity = 0;
      draw();
    }});

    canvas.addEventListener("mousedown", event => {{
      const node = findNodeAt(event.clientX, event.clientY);
      if (node) {{
        dragNode = node;
        if (!(event.shiftKey || event.metaKey || event.ctrlKey) && !selectedIds.has(node.id)) {{
          selectedIds = new Set([node.id]);
        }}
        tooltipPinned = false;
      }} else {{
        panStart = {{ clientX: event.clientX, clientY: event.clientY, x: transform.x, y: transform.y }};
      }}
      draw();
    }});

    window.addEventListener("mouseup", () => {{
      dragNode = null;
      panStart = null;
    }});

    canvas.addEventListener("click", event => {{
      const node = findNodeAt(event.clientX, event.clientY);
      if (node && (event.shiftKey || event.metaKey || event.ctrlKey)) {{
        if (selectedIds.has(node.id)) selectedIds.delete(node.id);
        else selectedIds.add(node.id);
      }} else if (node) {{
        selectedIds = new Set([node.id]);
      }} else {{
        selectedIds = new Set();
      }}
      tooltipPinned = selectedIds.size > 0;
      const rect = canvas.getBoundingClientRect();
      showTooltip(event.clientX - rect.left, event.clientY - rect.top);
      draw();
    }});

    canvas.addEventListener("wheel", event => {{
      event.preventDefault();
      const rect = canvas.getBoundingClientRect();
      const mouse = {{ x: event.clientX - rect.left, y: event.clientY - rect.top }};
      const before = toWorld(mouse.x, mouse.y);
      const factor = event.deltaY > 0 ? 0.9 : 1.1;
      transform.scale = Math.max(0.45, Math.min(3.5, transform.scale * factor));
      transform.x = mouse.x - before.x * transform.scale;
      transform.y = mouse.y - before.y * transform.scale;
      draw();
    }}, {{ passive: false }});

    [sectionFilter, searchBox, sourcePathFilter, targetPathFilter, viewMode, directionFilter, sourceNoindexFilter, targetNoindexFilter, sourceStatusFilter, targetStatusFilter, nodeLimit, minDegree, globalLinkMode, componentLinkMode, sitewideThreshold, recommendationLimit, recommendationThreshold].forEach(control => {{
      control.addEventListener("input", updateView);
      control.addEventListener("change", updateView);
    }});

    recommendationTabs.querySelectorAll("button").forEach(button => {{
      button.addEventListener("click", () => {{
        activeRecommendationType = button.dataset.type;
        renderRecommendations();
      }});
    }});

    presetPrev.addEventListener("click", () => {{
      activePresetIndex = (activePresetIndex - 1 + PRESETS.length) % PRESETS.length;
      renderPreset();
    }});

    presetNext.addEventListener("click", () => {{
      activePresetIndex = (activePresetIndex + 1) % PRESETS.length;
      renderPreset();
    }});

    applyPreset.addEventListener("click", () => {{
      PRESETS[activePresetIndex].apply();
      transform = {{ x: 0, y: 0, scale: 1 }};
      selectedIds = new Set();
      tooltipPinned = false;
      tooltip.style.opacity = 0;
      updateView();
    }});

    document.getElementById("resetView").addEventListener("click", () => {{
      sectionFilter.value = "";
      searchBox.value = "";
      sourcePathFilter.value = "";
      targetPathFilter.value = "";
      directionFilter.value = "all";
      sourceNoindexFilter.value = "";
      targetNoindexFilter.value = "";
      sourceStatusFilter.value = "";
      targetStatusFilter.value = "";
      nodeLimit.value = String(Math.min(180, currentGraph.meta.uniquePages));
      minDegree.value = 20;
      globalLinkMode.value = "dim";
      componentLinkMode.value = "dim";
      sitewideThreshold.value = 80;
      transform = {{ x: 0, y: 0, scale: 1 }};
      selectedIds = new Set();
      tooltipPinned = false;
      tooltip.style.opacity = 0;
      updateView();
    }});

    window.addEventListener("resize", resizeCanvas);

    syncGraphState();
    setupControls();
    indexLink.href = resolveInternalHtmlHref("index.html");
    renderPreset();
    const storedUploadedGraph = loadStoredUploadedGraph();
    if (storedUploadedGraph?.graph) {{
      setGraph(storedUploadedGraph.graph, storedUploadedGraph.fileName || storedUploadedGraph.graph.meta?.sourceFile || "");
    }}
    resizeCanvas();
    updateView();
  </script>
</body>
</html>"""


def render_index(graphs: list[dict]) -> str:
    cards_data = []
    cards = []
    for graph in graphs:
        output_name = Path(graph["meta"]["outputFile"]).name
        cards_data.append(
            {
                "href": output_name,
                "domain": graph["meta"]["domain"],
                "clientName": graph["meta"]["clientName"],
                "uniquePages": graph["meta"]["uniquePages"],
                "uniqueEdges": graph["meta"]["uniqueEdges"],
                "linksRetained": graph["meta"]["linksRetained"],
                "source": "bundled",
            }
        )
        cards.append(
            f"""
      <a class="client-card" href="{html.escape(output_name)}">
        <span>{html.escape(graph["meta"]["domain"])}</span>
        <strong>{html.escape(graph["meta"]["clientName"])}</strong>
        <small>{graph["meta"]["uniquePages"]:,} pages · {graph["meta"]["uniqueEdges"]:,} link pairs · {graph["meta"]["linksRetained"]:,} retained links</small>
      </a>"""
        )

    cards_json = json.dumps(cards_data, ensure_ascii=True, separators=(",", ":"))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Internal Link Maps</title>
  <style>
    :root {{
      --bg: #f7f7f5;
      --panel: #ffffff;
      --ink: #172326;
      --muted: #5d6a6d;
      --line: #e4e4e0;
      --teal: #0f766e;
      --shadow: 0 18px 50px rgb(17 19 20 / 10%);
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 15px/1.45 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{
      max-width: 1080px;
      margin: 0 auto;
      padding: clamp(28px, 7vw, 78px) clamp(18px, 4vw, 36px);
    }}
    h1 {{
      margin: 0;
      font-size: clamp(42px, 8vw, 86px);
      line-height: .92;
      letter-spacing: 0;
    }}
    p {{
      max-width: 760px;
      color: var(--muted);
      margin: 18px 0 34px;
      font-size: 17px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1px;
      border: 1px solid var(--line);
      background: var(--line);
      box-shadow: var(--shadow);
    }}
    .client-card {{
      display: block;
      min-height: 190px;
      padding: 22px;
      border: 0;
      border-radius: 0;
      background: var(--panel);
      color: var(--ink);
      text-decoration: none;
      box-shadow: none;
    }}
    .client-card:hover {{
      background: #fbfbfa;
    }}
    .client-card span {{
      display: block;
      color: var(--teal);
      font-weight: 800;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .04em;
      font-family: var(--mono);
    }}
    .client-card strong {{
      display: block;
      margin-top: 18px;
      font-size: 26px;
    }}
    .client-card small {{
      display: block;
      margin-top: 8px;
      color: var(--muted);
    }}
    .client-card em {{
      display: inline-block;
      margin-top: 14px;
      color: var(--muted);
      font-style: normal;
      font-size: 12px;
      font-family: var(--mono);
    }}
  </style>
</head>
<body>
  <main>
    <h1>Internal Link Maps</h1>
    <p>Open a client map to explore internal links, focused page searches, incoming and outgoing link direction, noindex filters, and global navigation/footer handling.</p>
    <div class="grid" id="mapGrid">{"".join(cards)}</div>
  </main>
  <script>
    const PRELOADED_MAPS = {cards_json};
    const UPLOADED_MAP_INDEX_KEY = "internal-link-map-uploaded-v1";

    function formatNumber(value) {{
      return new Intl.NumberFormat("en-ZA").format(value);
    }}

    function escapeHtml(value) {{
      return String(value ?? "").replace(/[<>&"]/g, char => ({{ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }}[char]));
    }}

    function renderCard(map) {{
      const sourceLabel = map.source === "uploaded" ? "uploaded" : "bundled";
      return `<a class="client-card" href="${{escapeHtml(resolveInternalHtmlHref(map.href))}}"><span>${{escapeHtml(map.domain)}}</span><strong>${{escapeHtml(map.clientName)}}</strong><small>${{formatNumber(map.uniquePages)}} pages · ${{formatNumber(map.uniqueEdges)}} link pairs · ${{formatNumber(map.linksRetained)}} retained links</small><em>${{sourceLabel}}</em></a>`;
    }}

    function getHtmlPreviewSourceUrl() {{
      if (window.location.hostname !== "htmlpreview.github.io") return "";
      const raw = window.location.href.split("?").slice(1).join("?");
      return raw.startsWith("https://") ? raw : "";
    }}

    function resolveInternalHtmlHref(href) {{
      const previewSource = getHtmlPreviewSourceUrl();
      if (previewSource) {{
        const baseDir = previewSource.replace(/[^/?#]+(?:\?.*)?$/, "");
        return `https://htmlpreview.github.io/?${{baseDir}}${{href}}`;
      }}
      return href;
    }}

    function isValidMapHref(href) {{
      return typeof href === "string" && /^[-a-z0-9]+\.html(?:\?uploadedMapKey=[^"\s]+)?$/i.test(href);
    }}

    function loadUploadedMaps() {{
      try {{
        const registry = JSON.parse(window.localStorage.getItem(UPLOADED_MAP_INDEX_KEY) || "[]");
        return (Array.isArray(registry) ? registry : [])
          .filter(item => item && typeof item.storageKey === "string" && window.localStorage.getItem(item.storageKey))
          .map(item => ({{
            ...item,
            source: "uploaded"
          }}));
      }} catch {{
        return [];
      }}
    }}

    const grid = document.getElementById("mapGrid");
    const uploadedMaps = loadUploadedMaps();
    const seen = new Set();
    const maps = [...uploadedMaps.filter(map => isValidMapHref(map.href)), ...PRELOADED_MAPS].filter(map => {{
      const key = `${{map.source}}::${{map.href}}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    }});
    grid.innerHTML = maps.map(renderCard).join("");
  </script>
</body>
</html>"""


def main() -> None:
    global INPUT, OUTPUT, DOMAIN, CLIENT_NAME

    PUBLIC_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    graphs = []
    for client in CLIENTS:
        INPUT = client["input"]
        OUTPUT = client["output"]
        DOMAIN = client["domain"]
        CLIENT_NAME = client["name"]

        graph = build_graph()
        graph["meta"]["outputFile"] = str(OUTPUT)
        OUTPUT.write_text(render_html(graph), encoding="utf-8")
        shutil.copyfile(OUTPUT, PUBLIC_OUTPUT_DIR / OUTPUT.name)
        graphs.append(graph)
        print(f"Wrote {OUTPUT}")
        print(
            f"{graph['meta']['clientName']}: "
            f"{graph['meta']['uniquePages']} pages, "
            f"{graph['meta']['uniqueEdges']} unique links, "
            f"{graph['meta']['linksRetained']} retained link instances"
        )

    INDEX_OUTPUT.write_text(render_index(graphs), encoding="utf-8")
    shutil.copyfile(INDEX_OUTPUT, PUBLIC_OUTPUT_DIR / INDEX_OUTPUT.name)
    print(f"Wrote {INDEX_OUTPUT}")


if __name__ == "__main__":
    main()
