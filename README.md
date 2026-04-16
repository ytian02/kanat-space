# Kanat Space

Kanat Space is a VitePress notes site for research notes, technical posts, maintenance logs, and future paper-note workflows.

## Commands

```sh
npm ci
npm run docs:dev
npm run docs:build
npm run docs:preview
```

On Windows PowerShell, use `npm.cmd` if script execution policy blocks `npm.ps1`.

```sh
npm.cmd run docs:dev
npm.cmd run docs:build
```

## Structure

- `docs/`: VitePress source files.
- `docs/posts/`: regular notes and articles.
- `docs/logs/`: public maintenance logs shown on the logs page and summarized on the home page.
- `docs/papers/`: paper-note entrypoint and future paper notes.
- `docs/papers/drafts/`: paper-note drafts excluded from VitePress output.
- `docs/public/`: static assets copied by VitePress.
- `templates/paper-note.md`: paper-note template for manual or future automated generation.

## Writing Notes

Use this frontmatter shape for posts:

```yaml
---
title: "Title"
description: ""
date: 2026-04-15T00:00:00+08:00
draft: false
tags:
  - tag
categories:
  - Category
collections:
  - Collection
math: true
---
```

Use this frontmatter shape for maintenance logs:

```yaml
---
title: "Log title"
date: 2026-04-15
summary: "One-line maintenance summary."
tags:
  - maintenance
---
```

Use `templates/paper-note.md` for paper notes. Drafts should stay under `docs/papers/drafts/` with `draft: true`; after review, move the note to `docs/papers/` and set `draft: false`.

## Deployment

GitHub Actions builds the site with `npm run docs:build` and publishes `docs/.vitepress/dist` to GitHub Pages.
