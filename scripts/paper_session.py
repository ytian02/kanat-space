from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

from extract_paper_assets import extract_paper_assets, parse_pages


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_PUBLIC_PAPERS = REPO_ROOT / "docs" / "public" / "papers"
DOCS_PAPER_DRAFTS = REPO_ROOT / "docs" / "papers" / "drafts"
DOCS_PAPER_LOCAL = REPO_ROOT / "docs" / "papers" / "local"

PANEL_TITLE_PREFIX = "\u5171\u8bfb\u5bfc\u822a"
READING_MAP_SUMMARY = "\u5148\u7528\u9605\u8bfb\u5730\u56fe\u9501\u5b9a\u5173\u952e\u9875\u548c\u5173\u952e\u56fe\uff0c\u518d\u56de\u5230\u5bf9\u8bdd\u91cc\u56f4\u7ed5\u5177\u4f53\u8bc1\u636e\u8ba8\u8bba\u3002"
KEY_PAGE_LABEL_TITLE = "\u6807\u9898\u3001\u6458\u8981\u4e0e\u95ee\u9898\u5b9a\u4e49"
KEY_PAGE_LABEL_RESULTS = "\u4e3b\u7ed3\u679c\u6216\u5206\u6790\u9875"
KEY_PAGE_LABEL_FOCUS = "\u5efa\u8bae\u91cd\u70b9\u67e5\u770b\u9875"
ROUTE_OPEN = "\u5148\u770b\u7b2c {page} \u9875\uff0c\u7406\u89e3\u6807\u9898\u3001\u6458\u8981\u548c\u8bba\u6587\u4efb\u52a1\u3002"
ROUTE_RESULTS = "\u518d\u770b\u7b2c {page} \u9875\uff0c\u786e\u8ba4\u4e3b\u7ed3\u679c\u6216\u6700\u6838\u5fc3\u7684\u6bd4\u8f83\u3002"
ROUTE_FIGURES = "\u7136\u540e\u68c0\u67e5 {figures}\uff0c\u7406\u89e3\u6a21\u578b\u56fe\u6216\u4e3b\u7ed3\u679c\u56fe\u3002"
QUESTIONS = [
    "\u8fd9\u7bc7\u8bba\u6587\u771f\u6b63\u7684\u6838\u5fc3\u521b\u65b0\u662f\u4ec0\u4e48\uff1f",
    "\u4e3b\u7ed3\u679c\u63d0\u5347\u6765\u81ea\u65b9\u6cd5\u672c\u8eab\uff0c\u8fd8\u662f\u6765\u81ea\u8868\u793a\u65b9\u5f0f\u6216\u5b9e\u9a8c\u8bbe\u5b9a\uff1f",
    "\u5982\u679c\u628a\u5b83\u8fc1\u79fb\u5230\u66f4\u5927\u89c4\u6a21\u6216\u5de5\u4e1a\u73af\u5883\uff0c\u6700\u5927\u7684\u98ce\u9669\u70b9\u5728\u54ea\u91cc\uff1f",
]
PAGE_PROMPT = "\u770b\u7b2c {page} \u9875\uff0c\u89e3\u91ca\u8fd9\u4e00\u9875\u6700\u91cd\u8981\u7684\u8bba\u70b9\u548c\u5b83\u5728\u6574\u7bc7\u8bba\u6587\u4e2d\u7684\u4f5c\u7528\u3002"
FIGURE_PROMPT = "\u770b {figure}\uff0c\u89e3\u91ca\u8fd9\u5f20\u56fe\u6700\u5173\u952e\u7684\u7ed3\u6784\u6216\u7ed3\u679c\u3002"


def is_http_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def resolve_source_url(source: str, pdf_url: str, arxiv: str) -> str:
    if pdf_url and is_http_url(pdf_url):
        return pdf_url
    if arxiv and is_http_url(arxiv):
        return arxiv
    if source:
        return source
    return pdf_url or arxiv


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "paper"


def paper_assets_dir(slug: str) -> Path:
    return DOCS_PUBLIC_PAPERS / slug


def default_note_path(slug: str) -> Path:
    return DOCS_PAPER_DRAFTS / f"{slug}.md"


def default_panel_path(slug: str) -> Path:
    return DOCS_PAPER_LOCAL / f"{slug}.md"


def derive_title(pdf: Path) -> str:
    return pdf.stem


def load_manifest(slug: str) -> tuple[Path, dict]:
    manifest_path = paper_assets_dir(slug) / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found for slug '{slug}': {manifest_path}")
    return manifest_path, json.loads(manifest_path.read_text(encoding="utf-8"))


def ensure_note(path: Path, title: str, source: str, pdf_url: str, arxiv: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
title: "{title}"
description: ""
date: {date.today().isoformat()}
draft: true
summary: ""
authors:
  - \u4f5c\u8005 1
institutions:
  - \u673a\u6784 1
venue: arXiv / Conference / Journal
year: YYYY
source: "{source}"
pdf: "{pdf_url}"
arxiv: "{arxiv}"
reading_status: \u901f\u8bfb
tags:
  - paper
categories:
  - Papers
collections:
  - Paper Notes
math: true
---

<PaperMeta />

# {title}

## \u4e00\u53e5\u8bdd\u603b\u7ed3

\u5f85\u8865\u5145\u3002

## \u5b8c\u6574 Abstract

\u5f85\u8865\u5145\u3002

## \u6838\u5fc3\u95ee\u9898

\u5f85\u8865\u5145\u3002

## \u4e3b\u8981\u8d21\u732e

- \u5f85\u8865\u5145

## \u65b9\u6cd5\u6982\u89c8

\u5f85\u8865\u5145\u3002

## \u4ee3\u8868\u6027\u56fe\u8868

\u5f85\u8865\u5145\u3002

## \u5173\u952e\u516c\u5f0f

\u5f85\u8865\u5145\u3002

## \u5b9e\u9a8c\u8bbe\u7f6e

- \u6570\u636e\u96c6\uff1a
- Baseline\uff1a
- \u6307\u6807\uff1a
- \u4e3b\u8981\u7ed3\u679c\uff1a

## \u7ed3\u8bba

\u5f85\u8865\u5145\u3002

## \u5c40\u9650\u4e0e\u8fb9\u754c

\u5f85\u8865\u5145\u3002

## \u53ef\u590d\u7528\u60f3\u6cd5

\u5f85\u8865\u5145\u3002

## \u6211\u7684\u95ee\u9898

- \u5f85\u8865\u5145

## \u8ba8\u8bba\u540e\u66f4\u65b0\u7684\u7406\u89e3

\u5f85\u8865\u5145\u3002
""",
        encoding="utf-8",
    )


def upsert_h2_section(markdown: str, heading: str, body: str) -> str:
    normalized_body = body.strip()
    pattern = re.compile(rf"(^## {re.escape(heading)}\n\n)(.*?)(?=^## |\Z)", re.M | re.S)
    match = pattern.search(markdown)
    if match:
        existing = match.group(2).strip()
        merged = existing
        if normalized_body and normalized_body not in existing:
            merged = f"{existing}\n\n{normalized_body}".strip()
        return markdown[: match.start(2)] + f"{merged}\n\n" + markdown[match.end(2) :]
    tail = "" if markdown.endswith("\n") else "\n"
    return f"{markdown}{tail}\n## {heading}\n\n{normalized_body}\n"


def rel_public_asset(slug: str, rel_path: str) -> str:
    return f"/papers/{slug}/{rel_path.replace(chr(92), '/')}"


def choose_key_pages(requested_pages: list[int]) -> list[dict[str, object]]:
    if not requested_pages:
        requested_pages = [1]
    unique_pages = sorted(set(requested_pages))
    items: list[dict[str, object]] = []
    for page in unique_pages[:4]:
        label = KEY_PAGE_LABEL_TITLE
        if page >= 5:
            label = KEY_PAGE_LABEL_RESULTS
        elif page != 1:
            label = KEY_PAGE_LABEL_FOCUS
        items.append({"page": page, "label": label})
    return items


def choose_key_figures(out_dir: Path, limit: int = 3) -> list[str]:
    figures_dir = out_dir / "figures"
    if not figures_dir.exists():
        return []
    items = sorted(
        (p for p in figures_dir.glob("*.png") if p.is_file()),
        key=lambda p: p.stat().st_size,
        reverse=True,
    )
    return [p.name for p in items[:limit]]


def build_page_text_index(out_dir: Path) -> dict[str, object]:
    text_path = out_dir / "text" / "paper.txt"
    raw = text_path.read_text(encoding="utf-8", errors="replace")
    pages = raw.split("\f")
    payload = {
        "pages": [
            {"page": idx, "text": page_text.replace("\r\n", "\n").strip()}
            for idx, page_text in enumerate(pages, start=1)
            if page_text.strip()
        ]
    }
    (out_dir / "page-text.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


def build_reading_map(title: str, slug: str, manifest: dict[str, object], requested_pages: list[int]) -> dict[str, object]:
    key_pages = choose_key_pages(requested_pages)
    key_figures = choose_key_figures(paper_assets_dir(slug))
    route: list[str] = []
    if key_pages:
        route.append(ROUTE_OPEN.format(page=key_pages[0]["page"]))
    if len(key_pages) > 1:
        route.append(ROUTE_RESULTS.format(page=key_pages[1]["page"]))
    if key_figures:
        route.append(ROUTE_FIGURES.format(figures=", ".join(key_figures[:2])))

    return {
        "title": title,
        "paper_slug": slug,
        "summary": READING_MAP_SUMMARY,
        "suggested_route": route,
        "key_pages": key_pages,
        "key_figures": key_figures,
        "questions": QUESTIONS,
        "source": manifest.get("source", ""),
        "draft_note_path": manifest.get("draft_note_path", ""),
    }


def build_workspace_data(slug: str, manifest: dict[str, object], reading_map: dict[str, object], page_text: dict[str, object]) -> dict[str, object]:
    key_pages = [
        {
            "page": int(item["page"]),
            "label": item["label"],
            "image": rel_public_asset(slug, f"pages/page-{int(item['page'])}.png"),
            "prompt": PAGE_PROMPT.format(page=int(item["page"])),
        }
        for item in reading_map.get("key_pages", [])
    ]
    key_figures = [
        {
            "id": figure,
            "image": rel_public_asset(slug, f"figures/{figure}"),
            "prompt": FIGURE_PROMPT.format(figure=figure),
        }
        for figure in reading_map.get("key_figures", [])
    ]
    return {
        "paperSlug": slug,
        "title": manifest.get("title"),
        "source": manifest.get("source"),
        "pdf": manifest.get("pdf"),
        "arxiv": manifest.get("arxiv"),
        "sourcePdf": manifest.get("source_pdf"),
        "draftNotePath": manifest.get("draft_note_path"),
        "readingMap": reading_map,
        "keyPages": key_pages,
        "keyFigures": key_figures,
        "pageTextCount": len(page_text.get("pages", [])),
        "pageTextPath": rel_public_asset(slug, "page-text.json"),
    }


def write_reading_map(out_dir: Path, reading_map: dict[str, object]) -> Path:
    path = out_dir / "reading-map.json"
    path.write_text(json.dumps(reading_map, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_workspace_data(out_dir: Path, workspace_data: dict[str, object]) -> Path:
    path = out_dir / "workspace-data.json"
    path.write_text(json.dumps(workspace_data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_panel_markdown(slug: str, title: str, reading_map: dict[str, object], manifest: dict[str, object]) -> Path:
    panel_path = default_panel_path(slug)
    panel_path.parent.mkdir(parents=True, exist_ok=True)
    panel_path.write_text(
        f"""---
title: {PANEL_TITLE_PREFIX}：{title}
date: {date.today().isoformat()}
summary: {reading_map["summary"]}
paper_slug: {slug}
source: "{str(manifest.get("source") or "")}"
draft: false
---

# {PANEL_TITLE_PREFIX}：{title}

<PaperWorkspace paper-slug="{slug}" />
""",
        encoding="utf-8",
    )
    return panel_path


def cmd_prepare(args: argparse.Namespace) -> None:
    pdf_path = Path(args.pdf).expanduser().resolve()
    slug = args.slug or slugify(pdf_path.stem)
    out_dir = paper_assets_dir(slug)
    note_path = Path(args.note).resolve() if args.note else default_note_path(slug)
    requested_pages = parse_pages(args.pages)
    manifest = extract_paper_assets(pdf_path, out_dir, requested_pages)

    title = args.title or derive_title(pdf_path)
    pdf_url = args.pdf_url or str(pdf_path)
    arxiv = args.arxiv or ""
    source = resolve_source_url(args.source or "", pdf_url, arxiv)

    ensure_note(note_path, title, source, pdf_url, arxiv)

    manifest["title"] = title
    manifest["paper_slug"] = slug
    manifest["source_pdf"] = str(pdf_path)
    manifest["source"] = source
    manifest["pdf"] = pdf_url
    manifest["arxiv"] = arxiv
    manifest["draft_note_path"] = str(note_path)

    page_text = build_page_text_index(out_dir)
    reading_map = build_reading_map(title, slug, manifest, requested_pages)
    workspace_data = build_workspace_data(slug, manifest, reading_map, page_text)

    reading_map_path = write_reading_map(out_dir, reading_map)
    workspace_path = write_workspace_data(out_dir, workspace_data)
    panel_path = write_panel_markdown(slug, title, reading_map, manifest)

    manifest["page_text"] = "page-text.json"
    manifest["reading_map"] = str(reading_map_path.relative_to(out_dir))
    manifest["workspace_data"] = str(workspace_path.relative_to(out_dir))
    manifest["local_panel_path"] = str(panel_path)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


def cmd_inspect(args: argparse.Namespace) -> None:
    _, manifest = load_manifest(args.slug)
    out_dir = paper_assets_dir(args.slug)
    result: dict[str, object] = {
        "paper_slug": manifest.get("paper_slug", args.slug),
        "title": manifest.get("title"),
        "source_pdf": manifest.get("source_pdf", manifest.get("pdf")),
        "draft_note_path": manifest.get("draft_note_path"),
        "local_panel_path": manifest.get("local_panel_path"),
        "text": str(out_dir / str(manifest["text"])),
        "reading_map": str(out_dir / str(manifest.get("reading_map", "reading-map.json"))),
        "page_text": str(out_dir / str(manifest.get("page_text", "page-text.json"))),
        "workspace_data": str(out_dir / str(manifest.get("workspace_data", "workspace-data.json"))),
    }
    if args.page is not None:
        page_path = out_dir / "pages" / f"page-{args.page}.png"
        result["page"] = args.page
        result["page_image"] = str(page_path)
        result["page_exists"] = page_path.exists()
    if args.figure:
        figure_path = out_dir / "figures" / args.figure
        result["figure"] = str(figure_path)
        result["figure_exists"] = figure_path.exists()
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_sync_note(args: argparse.Namespace) -> None:
    _, manifest = load_manifest(args.slug)
    note_path = Path(args.note).resolve() if args.note else Path(manifest.get("draft_note_path") or default_note_path(args.slug)).resolve()
    title = args.title or str(manifest.get("title") or derive_title(Path(str(manifest.get("source_pdf") or manifest.get("pdf")))))
    source = args.source or str(manifest.get("source") or manifest.get("pdf") or "")
    pdf_url = args.pdf_url or str(manifest.get("pdf") or "")
    arxiv = args.arxiv or str(manifest.get("arxiv") or "")
    ensure_note(note_path, title, source, pdf_url, arxiv)
    markdown = note_path.read_text(encoding="utf-8")
    markdown = upsert_h2_section(markdown, args.section, args.content)
    note_path.write_text(markdown, encoding="utf-8")
    print(json.dumps({"note_path": str(note_path), "section": args.section}, indent=2, ensure_ascii=False))


def cmd_build_panel(args: argparse.Namespace) -> None:
    _, manifest = load_manifest(args.slug)
    slug = args.slug
    title = str(manifest.get("title") or slug)
    out_dir = paper_assets_dir(slug)
    reading_map_path = out_dir / str(manifest.get("reading_map", "reading-map.json"))
    if reading_map_path.exists():
        reading_map = json.loads(reading_map_path.read_text(encoding="utf-8"))
    else:
        reading_map = build_reading_map(title, slug, manifest, [])
        write_reading_map(out_dir, reading_map)
    panel_path = write_panel_markdown(slug, title, reading_map, manifest)
    manifest["local_panel_path"] = str(panel_path)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"panel_path": str(panel_path)}, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Paper reading workflow entrypoint.")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="Prepare extracted assets and manifest for a paper.")
    prepare.add_argument("--pdf", required=True, help="Path to local PDF")
    prepare.add_argument("--slug", help="Paper slug used under docs/public/papers")
    prepare.add_argument("--pages", help="Comma-separated 1-based pages to render")
    prepare.add_argument("--note", help="Optional draft note path")
    prepare.add_argument("--title", help="Override paper title")
    prepare.add_argument("--source", help="Fallback source page URL")
    prepare.add_argument("--pdf-url", help="Canonical PDF URL")
    prepare.add_argument("--arxiv", help="arXiv URL")
    prepare.set_defaults(func=cmd_prepare)

    inspect = sub.add_parser("inspect", help="Locate text/page/figure assets for discussion.")
    inspect.add_argument("--slug", required=True, help="Paper slug")
    inspect.add_argument("--page", type=int, help="Page number to inspect")
    inspect.add_argument("--figure", help="Figure asset filename under figures/")
    inspect.set_defaults(func=cmd_inspect)

    sync = sub.add_parser("sync-note", help="Append stable discussion notes into a draft note.")
    sync.add_argument("--slug", required=True, help="Paper slug")
    sync.add_argument("--section", required=True, help="Target H2 section title")
    sync.add_argument("--content", required=True, help="Content appended into the target section")
    sync.add_argument("--note", help="Override note path")
    sync.add_argument("--title", help="Title when creating a new note")
    sync.add_argument("--source", help="Source URL when creating a new note")
    sync.add_argument("--pdf-url", help="PDF URL when creating a new note")
    sync.add_argument("--arxiv", help="arXiv URL when creating a new note")
    sync.set_defaults(func=cmd_sync_note)

    panel = sub.add_parser("build-panel", help="Rebuild the local reading panel for a prepared paper.")
    panel.add_argument("--slug", required=True, help="Paper slug")
    panel.set_defaults(func=cmd_build_panel)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
