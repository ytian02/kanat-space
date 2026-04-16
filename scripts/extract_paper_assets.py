from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def find_tool(name: str) -> str:
    tool = shutil.which(name)
    if not tool:
        raise SystemExit(f"Required tool not found: {name}")
    return tool


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def parse_pages(value: str | None) -> list[int]:
    if not value:
        return []
    pages: list[int] = []
    for chunk in value.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        pages.append(int(chunk))
    return sorted(set(pages))


def extract_paper_assets(pdf: str | Path, out_dir: str | Path, pages: list[int] | None = None) -> dict[str, object]:
    pdf = Path(pdf).expanduser().resolve()
    out_dir = Path(out_dir).expanduser().resolve()
    if not pdf.exists():
        raise SystemExit(f"PDF not found: {pdf}")

    pdftotext = find_tool("pdftotext")
    pdfimages = find_tool("pdfimages")
    pdftoppm = find_tool("pdftoppm")

    text_dir = out_dir / "text"
    figures_dir = out_dir / "figures"
    pages_dir = out_dir / "pages"

    ensure_dir(text_dir)
    ensure_dir(figures_dir)
    ensure_dir(pages_dir)

    text_path = text_dir / "paper.txt"
    subprocess.run([pdftotext, "-layout", "-enc", "UTF-8", str(pdf), str(text_path)], check=True)

    image_prefix = figures_dir / "image"
    subprocess.run([pdfimages, "-png", str(pdf), str(image_prefix)], check=True)

    image_listing = run([pdfimages, "-list", str(pdf)]).stdout
    (figures_dir / "pdfimages-list.txt").write_text(image_listing, encoding="utf-8")

    rendered_pages: list[str] = []
    for page in sorted(set(pages or [])):
        page_prefix = pages_dir / f"page-{page}"
        subprocess.run(
            [pdftoppm, "-png", "-f", str(page), "-singlefile", str(pdf), str(page_prefix)],
            check=True,
        )
        rendered_pages.append(str(page_prefix.with_suffix(".png").relative_to(out_dir)))

    extracted_images = sorted(str(p.relative_to(out_dir)) for p in figures_dir.glob("*.png"))

    manifest = {
        "pdf": str(pdf),
        "text": str(text_path.relative_to(out_dir)),
        "extracted_images": extracted_images,
        "rendered_pages": rendered_pages,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text and candidate figure assets from a PDF.")
    parser.add_argument("pdf", help="Path to the source PDF")
    parser.add_argument("out_dir", help="Directory where extracted assets will be written")
    parser.add_argument("--pages", help="Comma-separated 1-based pages to render as PNG snapshots")
    args = parser.parse_args()

    manifest = extract_paper_assets(args.pdf, args.out_dir, parse_pages(args.pages))
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
