---
title: "Scaling law"
slug: "dl-v-scaling-law"
subtitle: ""
description: "LLM 缩放定律的核心变量与演进。"
date: 2026-03-14T22:30:00+08:00
lastmod: 2026-03-14T22:30:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 深度学习
- 大模型
- Scaling Law

categories:
- 基础知识

collections:
- Deep Learning

math: true
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

- 🎯 **目标读者**：想理解大模型缩放规律演进脉络的读者
- ⏱️ **阅读时间**：约 6 分钟
- 📚 **知识要点**：N/D/C 三要素、Kaplan、Chinchilla、Inference Scaling

# Deep Learning

## Scaling law

### 1. 核心三要素
- 参数量 $N$
- 数据量 $D$
- 计算量 $C$

常见表达：
$$L(N,D)\approx\frac{A}{N^\alpha}+\frac{B}{D^\beta}+L_{min}.$$

### 2. Kaplan 定律 (OpenAI, 2020)
强调“大模型规模”带来的性能收益。

### 3. Chinchilla 定律 (DeepMind, 2022)
强调固定算力预算下参数与数据需要更平衡。

### 4. Inference Scaling (2024 - 至今)
除训练侧扩展外，推理侧增加计算也可带来显著收益。

### 总结
Scaling law 的价值在于让大模型训练从“经验试错”走向“可预测规划”。
