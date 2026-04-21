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


INPUT = Path(
    "/Users/stuartmarsden/Downloads/"
    "united-telecoms-za_07-apr-2026_links_2026-04-21_11-12-46.csv"
)
OUTPUT = Path(__file__).with_name("united-telecoms-internal-link-map.html")
DOMAIN = "unitedtelecoms.co.za"


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
                "sourceNoindex": edge_noindex[(source, target)]["sourceNoindex"],
                "targetNoindex": edge_noindex[(source, target)]["targetNoindex"],
                "anchors": top_anchors,
            }
        )

    edges.sort(key=lambda edge: edge["count"], reverse=True)
    nodes.sort(key=lambda node: node["degree"], reverse=True)

    return {
        "meta": {
            "sourceFile": str(INPUT),
            "domain": DOMAIN,
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

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>United Telecoms Internal Link Map</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f4ef;
      --panel: #ffffff;
      --ink: #172326;
      --muted: #5d6a6d;
      --line: #d8d2c6;
      --teal: #0f766e;
      --blue: #2457a6;
      --red: #b83a3a;
      --gold: #b7791f;
      --green: #2f855a;
      --violet: #6b46c1;
      --shadow: 0 10px 28px rgb(23 35 38 / 12%);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.45 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    header {{
      padding: 22px clamp(18px, 3vw, 36px) 14px;
      border-bottom: 1px solid var(--line);
      background: #fffdf8;
    }}

    h1 {{
      margin: 0;
      font-size: clamp(24px, 4vw, 42px);
      line-height: 1.05;
      letter-spacing: 0;
    }}

    .subtitle {{
      max-width: 900px;
      margin: 9px 0 0;
      color: var(--muted);
      font-size: 15px;
    }}

    .metrics {{
      display: grid;
      grid-template-columns: repeat(5, minmax(130px, 1fr));
      gap: 10px;
      padding: 16px clamp(18px, 3vw, 36px);
      background: #fbfaf6;
      border-bottom: 1px solid var(--line);
    }}

    .metric {{
      min-width: 0;
      padding: 11px 12px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 3px 12px rgb(23 35 38 / 5%);
    }}

    .metric strong {{
      display: block;
      font-size: 20px;
      line-height: 1.1;
    }}

    .metric span {{
      color: var(--muted);
      font-size: 12px;
    }}

    main {{
      display: grid;
      grid-template-columns: minmax(280px, 340px) minmax(0, 1fr);
      min-height: calc(100vh - 190px);
    }}

    aside {{
      border-right: 1px solid var(--line);
      background: #fffdf8;
      padding: 18px;
      overflow: auto;
    }}

    .control {{
      margin-bottom: 18px;
    }}

    label {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 7px;
      font-weight: 700;
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
      min-height: 40px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px 10px;
      background: white;
      color: var(--ink);
    }}

    input[type="search"] {{
      width: 100%;
    }}

    button {{
      width: 100%;
      min-height: 40px;
      border: 0;
      border-radius: 8px;
      background: var(--ink);
      color: white;
      font-weight: 800;
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

    .legend {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 18px;
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
      margin-top: 20px;
    }}

    .top-list h2 {{
      font-size: 14px;
      margin: 0 0 8px;
    }}

    .page-row {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px;
      padding: 8px 0;
      border-top: 1px solid var(--line);
      cursor: pointer;
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
        linear-gradient(rgb(23 35 38 / 4%) 1px, transparent 1px),
        linear-gradient(90deg, rgb(23 35 38 / 4%) 1px, transparent 1px);
      background-size: 36px 36px;
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
      padding: 12px;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: rgb(255 255 255 / 96%);
      box-shadow: var(--shadow);
      pointer-events: none;
      opacity: 0;
      transform: translate(12px, 12px);
    }}

    .focus-panel {{
      position: absolute;
      z-index: 1;
      top: 14px;
      left: 14px;
      width: min(460px, calc(100% - 28px));
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgb(255 253 248 / 94%);
      box-shadow: var(--shadow);
      display: none;
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
      border: 1px solid rgb(184 58 58 / 35%);
      border-radius: 999px;
      background: rgb(184 58 58 / 10%);
      color: var(--ink);
      padding: 4px 8px;
      font-size: 12px;
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
    }}

    .tooltip .small {{
      margin-top: 7px;
      color: var(--muted);
      font-size: 12px;
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
    }}
  </style>
</head>
<body>
  <header>
    <h1>United Telecoms Internal Link Map</h1>
    <p class="subtitle">Interactive page-to-page map from <code>{escaped_source}</code>. Filter by section, search for a URL path, and click any node to inspect its incoming and outgoing links.</p>
  </header>

  <section class="metrics">
    <div class="metric"><strong id="metric-pages">0</strong><span>unique internal pages</span></div>
    <div class="metric"><strong id="metric-edges">0</strong><span>unique source-to-target pairs</span></div>
    <div class="metric"><strong id="metric-links">0</strong><span>retained link instances</span></div>
    <div class="metric"><strong id="metric-visible-pages">0</strong><span>pages in current view</span></div>
    <div class="metric"><strong id="metric-visible-edges">0</strong><span>links in current view</span></div>
  </section>

  <main>
    <aside>
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
        <label for="nodeLimit">Pages shown <span id="nodeLimitValue">180</span></label>
        <input id="nodeLimit" type="range" min="40" max="588" value="180" step="10">
      </div>

      <div class="control">
        <label for="minDegree">Minimum total links <span id="minDegreeValue">20</span></label>
        <input id="minDegree" type="range" min="0" max="600" value="20" step="5">
      </div>

      <div class="control">
        <label class="toggle" for="hideSitewideLinks">
          <input id="hideSitewideLinks" type="checkbox">
          <span><strong>Hide global nav/footer links</strong><span id="sitewideHiddenCount">Removes repeated target-and-anchor patterns found on most source pages.</span></span>
        </label>
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
    const GRAPH = {data_json};

    const palette = ["#0f766e", "#2457a6", "#b7791f", "#b83a3a", "#2f855a", "#6b46c1", "#315c72", "#8a4d1f", "#64748b", "#be185d", "#047857", "#7c3aed"];
    const groupColor = new Map();
    GRAPH.meta.groups.forEach(([group], index) => groupColor.set(group, palette[index % palette.length]));

    const nodesById = new Map(GRAPH.nodes.map(node => [node.id, node]));
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
    const hideSitewideLinks = document.getElementById("hideSitewideLinks");
    const sitewideThreshold = document.getElementById("sitewideThreshold");
    const topPages = document.getElementById("topPages");

    let viewNodes = [];
    let viewEdges = [];
    let matchedSearchIds = new Set();
    let focusedSearchNodes = [];
    let simulationId = 0;
    let hovered = null;
    let selected = null;
    let dragNode = null;
    let transform = {{ x: 0, y: 0, scale: 1 }};
    let panStart = null;

    function formatNumber(value) {{
      return new Intl.NumberFormat("en-ZA").format(value);
    }}

    function setMetrics() {{
      document.getElementById("metric-pages").textContent = formatNumber(GRAPH.meta.uniquePages);
      document.getElementById("metric-edges").textContent = formatNumber(GRAPH.meta.uniqueEdges);
      document.getElementById("metric-links").textContent = formatNumber(GRAPH.meta.linksRetained);
      document.getElementById("metric-visible-pages").textContent = formatNumber(viewNodes.length);
      document.getElementById("metric-visible-edges").textContent = formatNumber(viewEdges.length);
    }}

    function setupControls() {{
      sectionFilter.innerHTML = '<option value="">All sections</option>' + GRAPH.meta.groups
        .map(([group, count]) => `<option value="${{group}}">${{group}} (${{formatNumber(count)}})</option>`)
        .join("");
      document.getElementById("legend").innerHTML = GRAPH.meta.groups.slice(0, 12)
        .map(([group]) => `<div class="legend-item"><span class="swatch" style="background:${{groupColor.get(group)}}"></span><span>${{group}}</span></div>`)
        .join("");
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
      const query = searchBox.value.trim().toLowerCase();
      const direction = directionFilter.value;
      const sourceNoindex = sourceNoindexFilter.value;
      const targetNoindex = targetNoindexFilter.value;
      const limit = Number(nodeLimit.value);
      const degree = Number(minDegree.value);
      const shouldHideSitewide = hideSitewideLinks.checked;
      const sitewideShare = Number(sitewideThreshold.value) / 100;
      document.getElementById("nodeLimitValue").textContent = limit;
      document.getElementById("minDegreeValue").textContent = degree;
      document.getElementById("sitewideThresholdValue").textContent = `${{sitewideThreshold.value}}%`;
      document.getElementById("sectionCount").textContent = section || "all";
      document.getElementById("searchCount").textContent = query ? "active" : "optional";
      document.getElementById("directionCount").textContent = query ? direction : "all";
      document.getElementById("sourceNoindexCount").textContent = sourceNoindex || "all";
      document.getElementById("targetNoindexCount").textContent = targetNoindex || "all";

      const matchesQuery = node => (node.path + " " + node.label + " " + node.id).toLowerCase().includes(query);
      let candidates;
      matchedSearchIds = new Set();
      focusedSearchNodes = [];
      if (query) {{
        const directMatches = GRAPH.nodes.filter(node => matchesQuery(node) && (!section || node.group === section));
        focusedSearchNodes = directMatches.slice().sort((a, b) => b.degree - a.degree);
        matchedSearchIds = new Set(directMatches.map(node => node.id));
        const expandedIds = new Set(matchedSearchIds);
        GRAPH.edges.forEach(edge => {{
          if ((direction === "all" || direction === "out") && matchedSearchIds.has(edge.source)) expandedIds.add(edge.target);
          if ((direction === "all" || direction === "in") && matchedSearchIds.has(edge.target)) expandedIds.add(edge.source);
        }});
        candidates = GRAPH.nodes.filter(node => expandedIds.has(node.id));
      }} else {{
        candidates = GRAPH.nodes.filter(node => node.degree >= degree);
        if (section) candidates = candidates.filter(node => node.group === section);
        candidates = candidates.slice().sort((a, b) => b.degree - a.degree).slice(0, limit);
      }}
      const ids = new Set(candidates.map(node => node.id));
      viewEdges = GRAPH.edges.filter(edge =>
        ids.has(edge.source) &&
        ids.has(edge.target) &&
        (!query || direction === "all" || (direction === "out" && matchedSearchIds.has(edge.source)) || (direction === "in" && matchedSearchIds.has(edge.target))) &&
        (!sourceNoindex || String(edge.sourceNoindex) === sourceNoindex) &&
        (!targetNoindex || String(edge.targetNoindex) === targetNoindex) &&
        (!shouldHideSitewide || edge.anchorSourceShare < sitewideShare)
      );
      const linkedIds = new Set(shouldHideSitewide ? [] : ids);
      viewEdges.forEach(edge => {{
        linkedIds.add(edge.source);
        linkedIds.add(edge.target);
      }});
      const hiddenCount = GRAPH.edges.filter(edge =>
        ids.has(edge.source) &&
        ids.has(edge.target) &&
        (!query || direction === "all" || (direction === "out" && matchedSearchIds.has(edge.source)) || (direction === "in" && matchedSearchIds.has(edge.target))) &&
        (!sourceNoindex || String(edge.sourceNoindex) === sourceNoindex) &&
        (!targetNoindex || String(edge.targetNoindex) === targetNoindex) &&
        edge.anchorSourceShare >= sitewideShare
      ).length;
      document.getElementById("sitewideHiddenCount").textContent = shouldHideSitewide
        ? `${{formatNumber(hiddenCount)}} visible-scope pairs hidden at this threshold.`
        : "Removes repeated target-and-anchor patterns found on most source pages.";
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
      if (!query) {{
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
      focusPanel.innerHTML = `<strong>Focused search: ${{query}}</strong><p>${{formatNumber(visibleMatched.length)}} matched page${{visibleMatched.length === 1 ? "" : "s"}} highlighted; ${{directionText}}.${{extra}}</p><div class="focus-chips">${{chips}}</div>`;
      focusPanel.style.display = "block";
      focusPanel.querySelectorAll(".focus-chip").forEach(chip => {{
        chip.addEventListener("click", () => {{
          selected = viewNodes.find(node => node.id === chip.dataset.id);
          draw();
          showTooltip(selected, 18, focusPanel.offsetHeight + 18);
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
          selected = viewNodes.find(node => node.id === row.dataset.id);
          draw();
          showTooltip(selected, stage.clientWidth / 2, 24);
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
      const active = selected || hovered;
      const activeLinks = new Set();
      if (active) {{
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
        ctx.beginPath();
        ctx.moveTo(source.x, source.y);
        ctx.lineTo(target.x, target.y);
        ctx.strokeStyle = isActive
          ? "rgba(184,58,58,0.95)"
          : isFocusEdge
            ? "rgba(184,58,58,0.58)"
            : matchedSearchIds.size
              ? "rgba(23,35,38,0.045)"
              : "rgba(23,35,38,0.12)";
        ctx.lineWidth = isActive
          ? 2.3
          : isFocusEdge
            ? 1.15
            : Math.max(0.35, Math.min(2.2, Math.sqrt(edge.count) * 0.45));
        ctx.stroke();
      }});

      viewNodes.forEach(node => {{
        const isActive = node === selected || node === hovered;
        const isMatched = matchedSearchIds.has(node.id);
        const connected = active && viewEdges.some(edge =>
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
        ctx.strokeStyle = isActive ? "#172326" : isMatched ? "#b83a3a" : "#fff";
        ctx.lineWidth = isActive ? 3 : isMatched ? 2.8 : 1.4;
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

    function showTooltip(node, x, y) {{
      if (!node) {{
        tooltip.style.opacity = 0;
        return;
      }}
      const incoming = viewEdges.filter(edge => edge.target === node.id).length;
      const outgoing = viewEdges.filter(edge => edge.source === node.id).length;
      const topAnchor = GRAPH.edges.find(edge => edge.source === node.id || edge.target === node.id)?.anchors?.[0]?.text || "No anchor captured";
      tooltip.innerHTML = `<strong>${{node.label}}</strong><a href="${{node.id}}" target="_blank" rel="noopener">${{node.id}}</a><div class="small">Section: ${{node.group}}<br>Noindex: source ${{node.sourceNoindex ? "yes" : "no"}} / target ${{node.targetNoindex ? "yes" : "no"}}<br>All links: in ${{formatNumber(node.in)}} / out ${{formatNumber(node.out)}}<br>Linked from ${{formatNumber(node.targetSourcePages)}} of ${{formatNumber(GRAPH.meta.sourcePages)}} source pages<br>Visible pairs: in ${{formatNumber(incoming)}} / out ${{formatNumber(outgoing)}}<br>Example anchor: ${{topAnchor}}</div>`;
      tooltip.style.left = Math.min(stage.clientWidth - 390, Math.max(4, x)) + "px";
      tooltip.style.top = Math.min(stage.clientHeight - 170, Math.max(4, y)) + "px";
      tooltip.style.opacity = 1;
    }}

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
      hovered = findNodeAt(event.clientX, event.clientY);
      canvas.style.cursor = hovered ? "pointer" : "grab";
      draw();
      const rect = canvas.getBoundingClientRect();
      showTooltip(hovered || selected, event.clientX - rect.left, event.clientY - rect.top);
    }});

    canvas.addEventListener("mouseleave", () => {{
      hovered = null;
      if (!selected) tooltip.style.opacity = 0;
      draw();
    }});

    canvas.addEventListener("mousedown", event => {{
      const node = findNodeAt(event.clientX, event.clientY);
      if (node) {{
        dragNode = node;
        selected = node;
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
      selected = findNodeAt(event.clientX, event.clientY);
      const rect = canvas.getBoundingClientRect();
      showTooltip(selected, event.clientX - rect.left, event.clientY - rect.top);
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

    [sectionFilter, searchBox, directionFilter, sourceNoindexFilter, targetNoindexFilter, nodeLimit, minDegree, hideSitewideLinks, sitewideThreshold].forEach(control => {{
      control.addEventListener("input", updateView);
    }});

    document.getElementById("resetView").addEventListener("click", () => {{
      sectionFilter.value = "";
      searchBox.value = "";
      directionFilter.value = "all";
      sourceNoindexFilter.value = "";
      targetNoindexFilter.value = "";
      nodeLimit.value = 180;
      minDegree.value = 20;
      hideSitewideLinks.checked = false;
      sitewideThreshold.value = 80;
      transform = {{ x: 0, y: 0, scale: 1 }};
      selected = null;
      tooltip.style.opacity = 0;
      updateView();
    }});

    window.addEventListener("resize", resizeCanvas);

    setupControls();
    resizeCanvas();
    updateView();
  </script>
</body>
</html>"""


def main() -> None:
    graph = build_graph()
    OUTPUT.write_text(render_html(graph), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(
        f"{graph['meta']['uniquePages']} pages, "
        f"{graph['meta']['uniqueEdges']} unique links, "
        f"{graph['meta']['linksRetained']} retained link instances"
    )


if __name__ == "__main__":
    main()
