---
title: 论文阅读工作流补全
date: 2026-04-16
summary: 为论文笔记补齐统一元信息、原文入口、图表资产约定和本地 PDF 提取脚本。
tags:
  - maintenance
  - papers
---

# 论文阅读工作流补全

本次维护补齐了论文阅读与整理的闭环能力：

- 统一 `paper-note` 模板，补充 authors、institutions、source、pdf、arxiv、reading_status 等字段。
- 为论文页增加 `PaperMeta` 组件，统一展示来源、作者、机构和原文入口。
- 为 `docs/papers/` 增加 `PapersList` 列表组件，后续已发布笔记可直接在入口页展示。
- 新增本地 PDF 提取脚本，用于抽取文本、图片和页图，减少手工整理图表的成本。
- 约定论文图表资源统一放入 `docs/public/papers/<slug>/`。
