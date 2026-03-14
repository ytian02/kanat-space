---
title: "L2正则化和权重衰减"
slug: "ml-iii-l2-regularization-and-weight-decay"
subtitle: ""
description: "L2 正则化与权重衰减在 SGD/Adam 中的关系。"
date: 2026-03-14T22:24:00+08:00
lastmod: 2026-03-14T22:24:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 机器学习
- 优化器

categories:
- 基础知识

collections:
- Machine Learning

math: false
collectionList: true
collectionNavigation: true

hiddenFromHomePage: false
hiddenFromSearch: false

featuredImage: ""
featuredImagePreview: ""
---

## AI 含量说明

本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。

## 本文概览

- 🎯 **目标读者**：关心优化器细节与正则策略差异的读者
- ⏱️ **阅读时间**：约 3 分钟
- 📚 **知识要点**：L2 正则化与 Weight Decay 的关系、SGD 与 AdamW 的差异

# Machine Learning

## L2正则化和权重衰减

### 核心结论
- 在标准 SGD 中，L2 正则化与权重衰减常可视作等价。
- 在 Adam 中，两者不严格等价。
- 实践中常使用 `AdamW`，将 Weight Decay 与梯度更新解耦。
