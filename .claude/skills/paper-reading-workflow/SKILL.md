---
name: paper-reading-workflow
description: Use when the user wants to read a local research paper with a generated reading map, browse a local reading panel in the VitePress site, inspect specific PDF pages or extracted figures, and sync stable conclusions back into a paper-note draft in this repository.
---

# Paper Reading Workflow

Use this skill when the user wants to discuss a paper while looking at its original content through the repository workflow.

This repository already has:
- `templates/paper-note.md`
- `docs/papers/drafts/`
- `docs/papers/local/`
- `docs/public/papers/<slug>/`
- `scripts/paper_session.py`

## What This Skill Does

1. Prepare a local PDF into discussion-ready assets:
   - extracted text
   - rendered page PNGs
   - candidate embedded figures
   - a manifest that ties the paper to its draft note
   - a generated reading map
   - a local reading panel page
2. Let the conversation anchor on specific pages or figure files.
3. Write stable discussion outcomes back into the paper draft.

## Workflow

### 1. Prepare the paper

Run:

```powershell
python scripts/paper_session.py prepare --pdf "<local-pdf-path>" --slug "<paper-slug>" --pages 1,6,12
```

This creates assets under `docs/public/papers/<paper-slug>/` and writes a manifest with:
- `source_pdf`
- `paper_slug`
- `draft_note_path`
- `reading_map`
- `local_panel_path`
- text path
- rendered page list
- extracted figure list

It also generates a local reading panel at:

```text
docs/papers/local/<paper-slug>.md
```

Preferred usage:
1. run `prepare`
2. open the local reading panel in the VitePress site
3. follow the reading map to decide which page or figure to inspect next
4. return to the IDE conversation and continue discussing that exact evidence

### 2. Inspect the exact page or figure being discussed

For a page:

```powershell
python scripts/paper_session.py inspect --slug "<paper-slug>" --page 6
```

For a specific extracted figure:

```powershell
python scripts/paper_session.py inspect --slug "<paper-slug>" --figure "image-008.png"
```

Use the returned paths to discuss the exact page, table, or model diagram. If the user wants you to look at a local image directly and they provide the full path, use the image-viewing tool on that path.

If the user asks for a faster entry, prefer the local reading panel first instead of asking them to choose a page manually.

### 3. Sync stable conclusions back to the draft

When a discussion reaches a stable conclusion, write it into the draft note:

```powershell
python scripts/paper_session.py sync-note --slug "<paper-slug>" --section "讨论后更新的理解" --content "<finalized-note>"
```

Prefer these target sections:
- `我的问题`
- `讨论后更新的理解`
- another existing H2 section only when the discussion corrects factual content already summarized there

## Guidance

- Do not treat tentative speculation as a paper claim.
- Keep quotes short; prefer paraphrase plus precise page or figure references.
- Default to page-based discussion when the user says “看这页” or references a figure/table visually.
- Default to text-based discussion when the user asks about a method detail, assumption, or experiment setup that is easier to trace from extracted text.
- If the draft does not exist, `sync-note` can create it from the repository template.

## Files To Read Only When Needed

- `scripts/paper_session.py` for exact command semantics
- `scripts/extract_paper_assets.py` for extraction details
- `templates/paper-note.md` for draft structure
