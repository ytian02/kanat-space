---
title: 论文笔记
---

# 论文笔记

这里用于沉淀论文阅读笔记。当前工作流以 Codex 辅助整理为主：你提供论文材料或本地 PDF，我负责提取信息、抽取代表性图表、生成 Markdown 草稿，并在讨论后把稳定结论回写到笔记中。

## 工作流

1. 提供论文 PDF、本地路径、arXiv/DOI/PDF 链接，或你已经读到的摘要和段落。
2. Codex 按 `templates/paper-note.md` 生成草稿，默认放入 `docs/papers/drafts/` 并设置 `draft: true`。
3. 本地脚本自动提取文本、候选图片和页图，为“边看边讨论”准备原文上下文。
4. 准备完成后，会额外生成一份本地专用的“论文共读面板”，展示阅读地图、关键页和关键图表。
5. 你基于草稿或面板继续提问，我们把新的理解回写到“我的问题 / 讨论后更新的理解”区块。
6. 确认后再移动到 `docs/papers/`，设置 `draft: false`，作为已发布论文笔记公开展示。

`docs/papers/drafts/` 已在 VitePress 配置中排除，不会生成公开页面。

## 站内约定

- 原文入口优先使用外链：`source`、`pdf`、`arxiv`
- 原始 PDF 不提交到仓库
- 图表资源统一放到 `docs/public/papers/<slug>/`
- 本地共读面板统一放到 `docs/papers/local/`
- 论文页保留完整 Abstract、来源、作者、机构、代表性图表和讨论后更新内容

## 已发布笔记

<PapersList />

## 本地共读面板

<LocalPaperPanelsList />
