---
title: 本地论文共读面板
date: 2026-04-16
summary: 为已准备的论文自动生成阅读地图与本地共读面板，减少逐页找证据的摩擦。
tags:
  - maintenance
  - papers
  - workflow
---

# 本地论文共读面板

本次维护把论文工作流从“命令定位页码”扩展为“先看阅读地图，再围绕关键页和关键图讨论”。

- `paper_session.py prepare` 现在会自动生成 `reading-map.json`
- 同时会生成 `docs/papers/local/<slug>.md` 本地共读面板
- 面板页展示阅读顺序、关键页、关键图表和继续讨论的入口提示
- 草稿正文仍然留在 `docs/papers/drafts/`，继续不公开
