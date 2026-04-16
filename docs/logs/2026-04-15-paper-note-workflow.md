---
title: 论文笔记草稿工作流
date: 2026-04-15
summary: 建立 Codex 辅助论文阅读与笔记整理流程，草稿默认放入 docs/papers/drafts 并排除公开构建。
tags:
  - maintenance
  - papers
---

# 论文笔记草稿工作流

本次维护明确论文笔记第一阶段采用 Codex 辅助整理：用户提供论文材料，Codex 生成 Markdown 草稿，人工确认后再发布。

## 约定

- 草稿放入 `docs/papers/drafts/`，设置 `draft: true`。
- `docs/papers/drafts/` 从 VitePress 构建中排除，避免未确认内容公开。
- 正式笔记移动到 `docs/papers/` 后设置 `draft: false`。
- 论文原文只记录链接，不提交 PDF。
