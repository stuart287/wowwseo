#!/usr/bin/env python3
"""Build a standalone internal-link network visualisation from an Ahrefs export."""

from __future__ import annotations

import csv
import html
import json
import re
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
]

INPUT = CLIENTS[0]["input"]
OUTPUT = CLIENTS[0]["output"]
DOMAIN = CLIENTS[0]["domain"]
CLIENT_NAME = CLIENTS[0]["name"]
INDEX_OUTPUT = Path(__file__).with_name("index.html")


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
    edge_noindex: dict[tuple[str, str], dict[str, bool]] = {}

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
            is_html_200 = (
                row.get("Source HTTP status code") == "200"
                and row.get("Target HTTP status code") == "200"
                and "HTML Page" in (row.get("Target URL type") or "")
            )
            if not is_internal or not is_html_200:
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
            source_noindex_by_url[source] = source_noindex
            target_noindex_by_url[target] = target_noindex
            edge_noindex[edge_key] = {
                "sourceNoindex": source_noindex,
                "targetNoindex": target_noindex,
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

    .metrics {{
      display: grid;
      grid-template-columns: repeat(5, minmax(130px, 1fr));
      gap: 1px;
      padding: 0 clamp(18px, 3vw, 34px);
      background: var(--line);
      border-bottom: 1px solid var(--line);
    }}

    .overview-band {{
      display: grid;
      grid-template-columns: minmax(0, 2.2fr) minmax(280px, 1fr);
      gap: 1px;
      padding: 0 clamp(18px, 3vw, 34px);
      background: var(--line);
      border-bottom: 1px solid var(--line);
    }}

    .overview-card {{
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
    .preset-list {{
      color: var(--muted);
      font-size: 12px;
    }}

    .preset-card {{
      display: grid;
      gap: 12px;
    }}

    .preset-card h3 {{
      margin: 0;
      font-size: 18px;
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
      padding: 16px 14px 15px;
      background: var(--panel-soft);
      border: 0;
      border-radius: 0;
      box-shadow: none;
    }}

    .metric strong {{
      display: block;
      font-family: var(--mono);
      font-size: 23px;
      line-height: 1.1;
      letter-spacing: 0;
    }}

    .metric span {{
      color: var(--muted);
      font-size: 12px;
    }}

    main {{
      display: grid;
      grid-template-columns: minmax(300px, 360px) minmax(0, 1fr);
      min-height: calc(100vh - 178px);
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

    .upload-shell {{
      margin-bottom: 18px;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: linear-gradient(180deg, #ffffff, #fbfbfa);
      box-shadow: 0 1px 0 rgb(17 19 20 / 3%);
    }}

    .upload-shell h2 {{
      margin: 0;
      font-size: 13px;
    }}

    .upload-shell p {{
      margin: 6px 0 12px;
      color: var(--muted);
      font-size: 12px;
    }}

    .upload-row {{
      display: grid;
      grid-template-columns: 1fr auto;
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

    .upload-meta {{
      min-width: 0;
    }}

    .upload-file {{
      display: block;
      font-size: 12px;
      font-weight: 700;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    .upload-status {{
      display: block;
      margin-top: 3px;
      color: var(--muted);
      font-size: 12px;
    }}

    .upload-status.error {{
      color: var(--red);
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
      background:
        linear-gradient(rgb(17 19 20 / 4%) 1px, transparent 1px),
        linear-gradient(90deg, rgb(17 19 20 / 4%) 1px, transparent 1px),
        radial-gradient(circle at 18% 12%, rgb(15 118 110 / 8%), transparent 30%),
        radial-gradient(circle at 86% 18%, rgb(37 99 235 / 6%), transparent 28%),
        #fafaf8;
      background-size: 36px 36px, 36px 36px, auto, auto, auto;
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

    @media (max-width: 900px) {{
      .overview-band {{
        grid-template-columns: 1fr;
      }}

      .guide-columns {{
        grid-template-columns: 1fr;
      }}

      .metrics {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      main {{
        grid-template-columns: 1fr;
      }}

      aside {{
        border-right: 0;
        border-bottom: 1px solid var(--line);
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
    <a class="index-link" href="index.html">All maps</a>
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
    </div>
    <div class="overview-card preset-card">
      <div>
        <h2>Preset</h2>
        <h3>Blog incoming links</h3>
        <p>Applies a focused setup for reviewing links pointing into blog pages while suppressing repeated UI-driven patterns.</p>
      </div>
      <ul class="preset-list">
        <li>Search path: <code>/blog/</code></li>
        <li>Link direction: links pointing to matches</li>
        <li>Source / target noindex: no only</li>
        <li>Pages shown: 100</li>
        <li>Minimum total links: 10</li>
        <li>Repeated patterns: hide</li>
        <li>Likely components: dim</li>
        <li>Sitewide threshold: 100%</li>
      </ul>
      <button id="applyBlogPreset" type="button">Apply Blog Preset</button>
    </div>
  </section>

  <section class="metrics">
    <div class="metric"><strong id="metric-pages">0</strong><span>unique internal pages</span></div>
    <div class="metric"><strong id="metric-edges">0</strong><span>unique source-to-target pairs</span></div>
    <div class="metric"><strong id="metric-links">0</strong><span>retained link instances</span></div>
    <div class="metric"><strong id="metric-visible-pages">0</strong><span>pages in current view</span></div>
    <div class="metric"><strong id="metric-visible-edges">0</strong><span>links in current view</span></div>
  </section>

  <main>
    <aside>
      <section class="upload-shell">
        <h2>Load Ahrefs export</h2>
        <p>Upload a links export to rebuild the visualisation in this browser without running the Python script.</p>
        <div class="upload-row">
          <div class="upload-meta">
            <span class="upload-file" id="uploadFileName">Using bundled {escaped_client} dataset</span>
            <span class="upload-status" id="uploadStatus">Ready for a UTF-16 Ahrefs links export.</span>
          </div>
          <label class="upload-pick">Choose file
            <input id="uploadInput" type="file" accept=".csv,.txt">
          </label>
        </div>
      </section>

      <div class="control">
        <label for="sectionFilter">Section <span id="sectionCount">all</span></label>
        <select id="sectionFilter"></select>
      </div>

      <div class="control">
        <label for="searchBox">Search path <span id="searchCount">optional</span></label>
        <input id="searchBox" type="search" placeholder="/cloud-pbx/ or pabx">
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

    <section class="stage" id="stage">
      <canvas id="graph"></canvas>
      <div class="focus-panel" id="focusPanel"></div>
      <div class="tooltip" id="tooltip"></div>
      <div class="empty" id="empty">No pages match these filters.</div>
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
    const directionFilter = document.getElementById("directionFilter");
    const sourceNoindexFilter = document.getElementById("sourceNoindexFilter");
    const targetNoindexFilter = document.getElementById("targetNoindexFilter");
    const nodeLimit = document.getElementById("nodeLimit");
    const minDegree = document.getElementById("minDegree");
    const globalLinkMode = document.getElementById("globalLinkMode");
    const sitewideThreshold = document.getElementById("sitewideThreshold");
    const topPages = document.getElementById("topPages");
    const uploadInput = document.getElementById("uploadInput");
    const uploadFileName = document.getElementById("uploadFileName");
    const uploadStatus = document.getElementById("uploadStatus");
    const componentLinkMode = document.getElementById("componentLinkMode");
    const componentHint = document.getElementById("componentHint");
    const applyBlogPreset = document.getElementById("applyBlogPreset");
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

    function formatNumber(value) {{
      return new Intl.NumberFormat("en-ZA").format(value);
    }}

    function setUploadStatus(message, isError = false) {{
      uploadStatus.textContent = message;
      uploadStatus.classList.toggle("error", isError);
    }}

    function escapeHtml(value) {{
      return String(value ?? "").replace(/[<>&"]/g, char => ({{ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }}[char]));
    }}

    function getSelectedNodes() {{
      return viewNodes.filter(node => selectedIds.has(node.id));
    }}

    function getSelectedEdges() {{
      return viewEdges.filter(edge => selectedIds.has(edge.source) && selectedIds.has(edge.target));
    }}

    function buildMapHrefForStorageKey(storageKey) {{
      const currentFile = window.location.pathname.split("/").pop() || "index.html";
      return `${{currentFile}}?uploadedMapKey=${{encodeURIComponent(storageKey)}}`;
    }}

    function saveUploadedGraph(graph, fileName) {{
      try {{
        const registry = JSON.parse(window.localStorage.getItem(UPLOADED_MAP_INDEX_KEY) || "[]");
        const storageKey = `uploaded-map::${{graph.meta.domain || "site"}}`;
        window.localStorage.setItem(storageKey, JSON.stringify({{ graph, fileName }}));
        const next = registry.filter(item => item.storageKey !== storageKey);
        next.unshift({{
          storageKey,
          clientName: graph.meta.clientName,
          domain: graph.meta.domain,
          fileName,
          uniquePages: graph.meta.uniquePages,
          uniqueEdges: graph.meta.uniqueEdges,
          linksRetained: graph.meta.linksRetained,
          href: buildMapHrefForStorageKey(storageKey)
        }});
        window.localStorage.setItem(UPLOADED_MAP_INDEX_KEY, JSON.stringify(next.slice(0, 12)));
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
      const edgeNoindex = new Map();
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
        const isHtml200 =
          row["Source HTTP status code"] === "200" &&
          row["Target HTTP status code"] === "200" &&
          (row["Target URL type"] || "").includes("HTML Page");

        if (!isInternal || !isHtml200) return;
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
        sourceNoindexByUrl.set(source, sourceNoindex);
        targetNoindexByUrl.set(target, targetNoindex);
        edgeNoindex.set(edgeKey, {{ sourceNoindex, targetNoindex }});

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
          groups: [...groupCounts.entries()].sort((a, b) => b[1] - a[1])
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
      document.title = `${{currentGraph.meta.clientName}} Internal Link Map`;
      document.querySelector("h1").textContent = `${{currentGraph.meta.clientName}} Internal Link Map`;
      document.querySelector(".subtitle").innerHTML = `Explore internal link structure, focused page relationships, noindex states, and global navigation patterns from <code>${{String(currentGraph.meta.sourceFile).replace(/[<>&]/g, char => ({{"<":"&lt;",">":"&gt;","&":"&amp;"}}[char]))}}</code>.`;
      nodeLimit.max = Math.max(40, currentGraph.meta.uniquePages);
      const defaultLimit = Math.min(180, currentGraph.meta.uniquePages);
      nodeLimit.value = String(defaultLimit);
      document.getElementById("nodeLimitValue").textContent = defaultLimit;
    }}

    function setupControls() {{
      sectionFilter.innerHTML = '<option value="">All sections</option>' + currentGraph.meta.groups
        .map(([group, count]) => `<option value="${{group}}">${{group}} (${{formatNumber(count)}})</option>`)
        .join("");
      document.getElementById("legend").innerHTML = currentGraph.meta.groups.slice(0, 12)
        .map(([group]) => `<div class="legend-item"><span class="swatch" style="background:${{groupColor.get(group)}}"></span><span>${{group}}</span></div>`)
        .join("");
    }}

    function setGraph(graph, fileName) {{
      currentGraph = graph;
      syncGraphState();
      setupControls();
      sectionFilter.value = "";
      searchBox.value = "";
      directionFilter.value = "all";
      sourceNoindexFilter.value = "";
      targetNoindexFilter.value = "";
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
      uploadFileName.textContent = fileName ? `Loaded ${{fileName}}` : `Using bundled ${{currentGraph.meta.clientName}} dataset`;
      setUploadStatus(`Ready. Showing ${{currentGraph.meta.uniquePages.toLocaleString("en-ZA")}} pages from ${{currentGraph.meta.domain}}.`);
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

    function updateView() {{
      const section = sectionFilter.value;
      const rawQuery = searchBox.value.trim();
      const query = normalizeSearchText(rawQuery);
      const direction = directionFilter.value;
      const sourceNoindex = sourceNoindexFilter.value;
      const targetNoindex = targetNoindexFilter.value;
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
      document.getElementById("globalLinkModeCount").textContent = globalMode;
      document.getElementById("componentLinkModeCount").textContent = componentMode;
      document.getElementById("sourceNoindexCount").textContent = sourceNoindex || "all";
      document.getElementById("targetNoindexCount").textContent = targetNoindex || "all";
      if (query !== lastFocusQuery) {{
        focusPanelDismissed = false;
        lastFocusQuery = query;
      }}

      const matchesQuery = node => normalizeSearchText(node.path + " " + node.label + " " + node.id).includes(query);
      let candidates;
      matchedSearchIds = new Set();
      focusedSearchNodes = [];
      if (query) {{
        const directMatches = currentGraph.nodes.filter(node => matchesQuery(node) && (!section || node.group === section));
        focusedSearchNodes = directMatches.slice().sort((a, b) => b.degree - a.degree);
        matchedSearchIds = new Set(directMatches.map(node => node.id));
        const expandedIds = new Set(matchedSearchIds);
        currentGraph.edges.forEach(edge => {{
          if ((direction === "all" || direction === "out") && matchedSearchIds.has(edge.source)) expandedIds.add(edge.target);
          if ((direction === "all" || direction === "in") && matchedSearchIds.has(edge.target)) expandedIds.add(edge.source);
        }});
        candidates = currentGraph.nodes.filter(node => expandedIds.has(node.id));
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
        (!sourceNoindex || String(edge.sourceNoindex) === sourceNoindex) &&
        (!targetNoindex || String(edge.targetNoindex) === targetNoindex) &&
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
        edge.anchorSourceShare >= sitewideShare
      ).length;
      const componentCount = currentGraph.edges.filter(edge =>
        ids.has(edge.source) &&
        ids.has(edge.target) &&
        (!query || direction === "all" || (direction === "out" && matchedSearchIds.has(edge.source)) || (direction === "in" && matchedSearchIds.has(edge.target))) &&
        (!sourceNoindex || String(edge.sourceNoindex) === sourceNoindex) &&
        (!targetNoindex || String(edge.targetNoindex) === targetNoindex) &&
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
      renderFocusPanel(query);
      renderTopPages();
      startSimulation();
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
      const links = viewEdges.map(edge => ({{
        ...edge,
        sourceNode: nodeMap.get(edge.source),
        targetNode: nodeMap.get(edge.target)
      }})).filter(edge => edge.sourceNode && edge.targetNode);

      viewNodes.forEach((node, index) => {{
        const isMatched = matchedSearchIds.has(node.id);
        const angle = (index / Math.max(1, viewNodes.length)) * Math.PI * 2;
        const spread = isMatched ? 0.08 : 0.36;
        node.x = rect.width / 2 + Math.cos(angle) * Math.min(rect.width, rect.height) * spread * Math.random();
        node.y = rect.height / 2 + Math.sin(angle) * Math.min(rect.width, rect.height) * spread * Math.random();
      }});

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
          const centerPull = isMatched ? 0.012 : matchedSearchIds.size ? 0.0014 : 0.002;
          node.vx += (centerX - node.x) * centerPull * alpha;
          node.vy += (centerY - node.y) * centerPull * alpha;
          node.vx *= 0.82;
          node.vy *= 0.82;
          node.x = Math.max(20, Math.min(rect.width - 20, node.x + node.vx));
          node.y = Math.max(20, Math.min(rect.height - 20, node.y + node.vy));
        }});

        draw();
        if (alpha > 0.025) requestAnimationFrame(tick);
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

        if (isActive || isMatched || node.degree > 220) {{
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
        tooltip.innerHTML = `<strong>${{escapeHtml(node.label)}}</strong><a href="${{node.id}}" target="_blank" rel="noopener">${{escapeHtml(node.id)}}</a><div class="small">Section: ${{escapeHtml(node.group)}}<br>Noindex: source ${{node.sourceNoindex ? "yes" : "no"}} / target ${{node.targetNoindex ? "yes" : "no"}}<br>All links: in ${{formatNumber(node.in)}} / out ${{formatNumber(node.out)}}<br>Linked from ${{formatNumber(node.targetSourcePages)}} of ${{formatNumber(currentGraph.meta.sourcePages)}} source pages<br>Visible pairs: in ${{formatNumber(incomingEdges.length)}} / out ${{formatNumber(outgoingEdges.length)}}</div>${{topAnchors ? `<div class="small"><strong>Top visible anchors</strong><ul>${{topAnchors}}</ul></div>` : ""}}`;
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
      uploadFileName.textContent = `Loading ${{file.name}}`;
      setUploadStatus("Parsing Ahrefs export and rebuilding graph...");
      try {{
        const buffer = await file.arrayBuffer();
        const text = decodeFileText(buffer);
        const rows = parseDelimited(text, "\\t");
        if (rows.length < 2) throw new Error("The file did not contain enough rows to parse.");
        const headers = rows[0];
        const records = rows.slice(1).map(row => Object.fromEntries(headers.map((header, index) => [header, row[index] || ""])));
        if (!headers.includes("Source URL") || !headers.includes("Target URL")) {{
          throw new Error("This does not look like the Ahrefs internal links export.");
        }}
        const graph = buildGraphFromRows(records, file.name);
        if (!graph.meta.uniquePages) throw new Error("No internal HTML pages were retained from this file.");
        setGraph(graph, file.name);
        saveUploadedGraph(graph, file.name);
      }} catch (error) {{
        console.error(error);
        uploadFileName.textContent = file.name;
        setUploadStatus(error.message || "Could not parse this file.", true);
      }} finally {{
        uploadInput.value = "";
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

    [sectionFilter, searchBox, directionFilter, sourceNoindexFilter, targetNoindexFilter, nodeLimit, minDegree, globalLinkMode, componentLinkMode, sitewideThreshold].forEach(control => {{
      control.addEventListener("input", updateView);
    }});

    applyBlogPreset.addEventListener("click", () => {{
      searchBox.value = "/blog/";
      directionFilter.value = "in";
      sourceNoindexFilter.value = "false";
      targetNoindexFilter.value = "false";
      nodeLimit.value = String(Math.min(100, Number(nodeLimit.max)));
      minDegree.value = "10";
      globalLinkMode.value = "hide";
      componentLinkMode.value = "dim";
      sitewideThreshold.value = "100";
      transform = {{ x: 0, y: 0, scale: 1 }};
      selectedIds = new Set();
      tooltipPinned = false;
      tooltip.style.opacity = 0;
      updateView();
    }});

    document.getElementById("resetView").addEventListener("click", () => {{
      sectionFilter.value = "";
      searchBox.value = "";
      directionFilter.value = "all";
      sourceNoindexFilter.value = "";
      targetNoindexFilter.value = "";
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
    const storedUploadedGraph = loadStoredUploadedGraph();
    if (storedUploadedGraph?.graph) {{
      setGraph(storedUploadedGraph.graph, storedUploadedGraph.fileName || storedUploadedGraph.graph.meta?.sourceFile || "");
    }}
    resizeCanvas();
    setUploadStatus(`Ready. Showing ${{currentGraph.meta.uniquePages.toLocaleString("en-ZA")}} pages from ${{currentGraph.meta.domain}}.`);
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
      return `<a class="client-card" href="${{escapeHtml(map.href)}}"><span>${{escapeHtml(map.domain)}}</span><strong>${{escapeHtml(map.clientName)}}</strong><small>${{formatNumber(map.uniquePages)}} pages · ${{formatNumber(map.uniqueEdges)}} link pairs · ${{formatNumber(map.linksRetained)}} retained links</small><em>${{sourceLabel}}</em></a>`;
    }}

    function loadUploadedMaps() {{
      try {{
        return JSON.parse(window.localStorage.getItem(UPLOADED_MAP_INDEX_KEY) || "[]").map(item => ({{
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
    const maps = [...uploadedMaps, ...PRELOADED_MAPS].filter(map => {{
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

    graphs = []
    for client in CLIENTS:
        INPUT = client["input"]
        OUTPUT = client["output"]
        DOMAIN = client["domain"]
        CLIENT_NAME = client["name"]

        graph = build_graph()
        graph["meta"]["outputFile"] = str(OUTPUT)
        OUTPUT.write_text(render_html(graph), encoding="utf-8")
        graphs.append(graph)
        print(f"Wrote {OUTPUT}")
        print(
            f"{graph['meta']['clientName']}: "
            f"{graph['meta']['uniquePages']} pages, "
            f"{graph['meta']['uniqueEdges']} unique links, "
            f"{graph['meta']['linksRetained']} retained link instances"
        )

    INDEX_OUTPUT.write_text(render_index(graphs), encoding="utf-8")
    print(f"Wrote {INDEX_OUTPUT}")


if __name__ == "__main__":
    main()
