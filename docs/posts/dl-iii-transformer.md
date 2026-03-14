---
title: "Transformer"
slug: "dl-iii-transformer"
subtitle: ""
description: "Transformer 结构、设计动机与复杂度整理。"
date: 2026-03-14T22:28:00+08:00
lastmod: 2026-03-14T22:28:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 深度学习
- Transformer

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

- 🎯 **目标读者**：需要系统回顾 Transformer 核心机制的读者
- ⏱️ **阅读时间**：约 12 分钟
- 📚 **知识要点**：模型结构、注意力设计、位置编码、归一化选择、时间复杂度

# Deep Learning

## Transformer

### 3.1 模型结构
- Encoder：多头自注意力 + 前馈网络（残差连接 + LayerNorm）。
- Decoder：掩码自注意力 + 交叉注意力 + 前馈网络，最终线性层 + softmax 输出。

> [待插入图片：Transformer 结构图（原文 `Pasted image 20251217193941.png`）]

### 3.2 为什么不用循环神经网络？
1. 自注意力可并行处理整段序列，RNN 更偏串行。
2. 自注意力在长距离依赖建模上更直接。

> [待插入图片：并行与串行对比图（原文 `Pasted image 20251217195345.png`）]

### 3.3 为什么使用点积注意力而不是加性注意力？
点积注意力在现代硬件上通常更高效，空间与时间开销更友好。

> [待插入图片：点积与加性注意力对比图（原文 `Pasted image 20251217200235.png`）]

### 3.4 为什么使用缩放点积注意力而不是标准的点积注意力？
不缩放时，随维度上升点积方差变大，softmax 容易饱和导致梯度变小，因此使用
$$\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right).$$

> [待插入图片：缩放点积注意力示意图（原文 `Pasted image 20251217200352.png`）]

### 3.5 嵌入层与softmax
- 常见做法是输入 embedding 与输出层权重共享，减少参数并增强语义一致性。
- embedding 常乘以 $\sqrt{d_{model}}$ 以匹配位置编码量级。

> [待插入图片：嵌入层与 softmax 共享权重图（原文 `Pasted image 20251217203636.png`）]

### 3.6 位置编码
$$
\text{PE}_{(pos,2i)}=\sin\left(\frac{pos}{10000^{2i/d_{model}}}\right),\quad
\text{PE}_{(pos,2i+1)}=\cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)
$$
用于给模型注入序列位置信息，并具备一定外推能力。

### 3.7 为什么使用Layernorm不用BatchNorm?
- LayerNorm 对变长序列更友好。
- BatchNorm 对 batch 统计量更敏感，小 batch 时波动更明显。

### 3.8 Transformer的时间复杂度
单层常见复杂度：
$$O(N^2d + Nd^2).$$
- 长序列时，$N^2d$ 主导（注意力矩阵瓶颈）。
- 序列较短时，$Nd^2$ 更显著（投影与 FFN）。
