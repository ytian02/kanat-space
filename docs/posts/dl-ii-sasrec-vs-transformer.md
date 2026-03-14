---
title: "SASRec和Transformer Encoder/Decoder-only Transformer的区别?"
slug: "dl-ii-sasrec-vs-transformer"
subtitle: ""
description: "SASRec 与 Transformer 结构差异对比。"
date: 2026-03-14T22:27:00+08:00
lastmod: 2026-03-14T22:27:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 深度学习
- 推荐系统
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

- 🎯 **目标读者**：关注序列推荐与 Transformer 架构差异的读者
- ⏱️ **阅读时间**：约 4 分钟
- 📚 **知识要点**：因果掩码、双向注意力、交叉注意力、SASRec 结构定位

# Deep Learning

## SASRec和Transformer Encoder/Decoder-only Transformer的区别?

### 1. 注意力机制
- Transformer Encoder 通常是双向注意力。
- SASRec 与 Decoder-only Transformer 使用因果掩码，避免未来信息泄露。

### 2. 交叉注意力层
- SASRec 没有跨源序列的交叉注意力层。
- 标准 Seq2Seq Decoder 含交叉注意力；标准 Decoder-only（如 GPT）通常不含。

### 注
SASRec 的共享 item embedding 使输入与输出打分共享表示，在参数效率和表达能力之间取得平衡。
