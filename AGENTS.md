# Agent Maintenance Guide

This repository is a VitePress notes site. Use this file as the shared project-level guide when maintaining the project with Codex or another coding agent from different terminals.

## Project Context

- The site is built with VitePress and deployed from `docs/.vitepress/dist`.
- The main content types are research notes, technical posts, maintenance logs, and paper notes.
- Do not restore Hugo files or generated Hugo output. The project should remain VitePress-only.
- Static assets that must be served by VitePress belong in `docs/public/`.

## Commands

- Use `npm.cmd` on Windows PowerShell when `npm.ps1` is blocked by execution policy.
- Local development: `npm.cmd run docs:dev`.
- Production build: `npm.cmd run docs:build`.
- Production preview: `npm.cmd run docs:preview`.
- After structural changes, run `npm.cmd run docs:build` before reporting completion.

## Maintenance Rules

- Check `git status --short` before making edits.
- Never revert user changes unless the user explicitly asks for it.
- Keep generated VitePress output out of commits; `docs/.vitepress/dist/` is ignored.
- Prefer small, direct changes over broad rewrites when the task is narrow.
- If a change affects navigation, loaders, Markdown rendering, or content directories, verify with a build.

## Writing Style

- Write notes primarily in Chinese.
- Keep method names, model names, dataset names, metrics, paper titles, and key technical terms in English when that preserves precision.
- Distinguish clearly between paper claims and personal interpretation.
- Avoid presenting uncertain inference as fact.
- For formulas, preserve LaTeX and add concise Chinese explanations.

## Paper Note Workflow

- The user provides paper materials: PDF, arXiv/DOI/PDF link, abstract, selected sections, or reading excerpts.
- Codex summarizes and organizes the material into a Markdown draft using `templates/paper-note.md`.
- Drafts go under `docs/papers/drafts/` with `draft: true`.
- `docs/papers/drafts/**/*.md` is excluded from VitePress output via `srcExclude`.
- After review, move the note to `docs/papers/`, set `draft: false`, and build the site.
- Do not commit original PDF files. Record source links in the note metadata instead.

## Logs

- Use `docs/logs/` for maintenance records that affect project structure, build behavior, workflows, or published note organization.
- Keep log summaries short enough for the home page recent-log panel.
- Add a log entry when introducing a new workflow, changing navigation, or publishing a meaningful paper-note batch.

## Interaction Preferences

- Before substantial work, briefly state what will be changed and how it will be verified.
- Ask before high-impact product or content-structure decisions.
- For straightforward maintenance tasks, make the change directly and report the result.
- Final responses should state the main files changed and the verification performed.
