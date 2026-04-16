---
title: "Recommender Systems with Generative Retrieval"
description: "TIGER 将 sequential recommendation 改写为 Semantic ID 的生成式检索问题。"
date: 2026-04-16
draft: true
summary: "TIGER 用 RQ-VAE 生成 Semantic ID，并用 seq2seq Transformer 自回归预测下一个 item 的 Semantic ID，在多个 Amazon benchmark 上优于传统 sequential recommender baseline。"
authors:
  - Shashank Rajput
  - Nikhil Mehta
  - Anima Singh
  - Raghunandan Keshavan
  - Trung Vu
  - Lukasz Heldt
  - Lichan Hong
  - Yi Tay
  - Vinh Q. Tran
  - Jonah Samost
  - Maciej Kula
  - Ed H. Chi
  - Maheswaran Sathiamoorthy
institutions:
  - Google DeepMind
  - Google
  - University of Wisconsin-Madison
venue: NeurIPS
year: 2023
source: "https://arxiv.org/pdf/2305.05065.pdf"
pdf: "https://arxiv.org/pdf/2305.05065.pdf"
arxiv: "https://arxiv.org/abs/2305.05065"
reading_status: 速读
tags:
  - paper
  - recommender-system
  - generative-retrieval
  - semantic-id
categories:
  - Papers
collections:
  - Paper Notes
math: true
---

<PaperMeta />

# Recommender Systems with Generative Retrieval

## 一句话总结

这篇论文提出 `TIGER`，把 sequential recommendation 中“检索下一个 item”改写成“生成下一个 item 的 Semantic ID”，并在公开 benchmark 上展示了优于多种传统 baseline 的 Recall / NDCG 表现。

## 完整 Abstract

Modern recommender systems perform large-scale retrieval by embedding queries and item candidates in the same unified space, followed by approximate nearest neighbor search to select top candidates given a query embedding. In this paper, we propose a novel generative retrieval approach, where the retrieval model autoregressively decodes the identifiers of the target candidates. To that end, we create semantically meaningful tuple of codewords to serve as a Semantic ID for each item. Given Semantic IDs for items in a user session, a Transformer-based sequence-to-sequence model is trained to predict the Semantic ID of the next item that the user will interact with. We show that recommender systems trained with the proposed paradigm significantly outperform the current SOTA models on various datasets. In addition, we show that incorporating Semantic IDs into the sequence-to-sequence model enhances its ability to generalize, as evidenced by the improved retrieval performance observed for items with no prior interaction history.

## 核心问题

传统推荐检索通常采用 dual-encoder + ANN 的范式：用户和 item 各自编码到同一向量空间，再通过 nearest neighbor search 找候选。这一做法在 item 数量很大时需要维护庞大的 embedding table 和索引结构，而且随机 atomic ID 对新 item 或低频 item 的泛化能力有限。

这篇论文试图回答的问题是：是否可以像 generative retrieval in IR 那样，把推荐检索直接改写成“生成目标 item 标识”的任务，并借助有语义结构的 item ID 改善泛化与冷启动能力。

## 主要贡献

- 提出 `TIGER (Transformer Index for GEnerative Recommenders)`，将 sequential recommendation 改写为生成式检索任务。
- 使用 `RQ-VAE` 基于 item content embedding 构造 `Semantic ID`，让相似 item 共享部分离散 token。
- 在 Amazon Beauty、Sports and Outdoors、Toys and Games 三个 benchmark 上优于多种 sequential recommendation baseline。
- 展示了该范式在 cold-start recommendation 和 recommendation diversity 上的额外能力。

## 方法概览

论文方法分为两步：

1. `Semantic ID generation`
   先用文本编码器得到 item 的内容 embedding，再用 `RQ-VAE` 把 embedding 量化成若干 codeword。这个 codeword tuple 就是 item 的 `Semantic ID`。

2. `Generative recommendation`
   把用户历史交互 item 的 `Semantic ID` 序列输入到 Transformer encoder-decoder 中，自回归生成下一个 item 的 `Semantic ID`。

和传统的 dual-encoder 检索相比，TIGER 不是先学 user/item embedding 再做 ANN，而是直接生成目标 item 的离散标识。论文强调，这种表示让模型可以在相似 item 之间共享知识，也让 Transformer 参数本身承担了一部分“索引”的作用。

## 代表性图表

### 候选模型图页

下面先保留自动导出的候选页图。后续如果确认需要更干净的局部图，可以再从同一页裁剪出单独的模型图。

![TIGER 候选模型图页](/papers/2023-google-tiger/pages/page-1.png)

### 候选主结果表页

这一页包含 Table 1 与主结果比较，后续可进一步转写为 Markdown 表格。

![TIGER 候选主结果表页](/papers/2023-google-tiger/pages/page-6.png)

## 实验设置

- 数据集：Amazon Product Reviews 的 `Beauty`、`Sports and Outdoors`、`Toys and Games`
- Baseline：`GRU4Rec`、`Caser`、`HGN`、`SASRec`、`BERT4Rec`、`FDSA`、`S3-Rec`、`P5`
- 指标：`Recall@5`、`Recall@10`、`NDCG@5`、`NDCG@10`
- 关键结果：
  - TIGER 在三个 benchmark 上整体优于 baseline
  - 在 `Beauty` 上，文中报告相对最强 baseline 有约 `29%` 的 `NDCG@5` 提升
  - 在 `Toys and Games` 上，`NDCG@5` 和 `NDCG@10` 提升约 `21%` 与 `15%`

## 结论

论文的核心结论是：`Semantic ID + seq2seq generative retrieval` 可以作为 recommender retrieval 的一个替代范式，不仅在公开数据上获得更好的排序指标，还能更自然地支持冷启动 item 和多样性控制。

## 局限与边界

- 结果主要来自公开 benchmark，和超大规模工业在线系统之间仍有距离。
- 论文强调“不需要传统 ANN index”，但 serving 复杂度并没有消失，只是转移到了生成式检索与离散 ID 设计上。
- 冷启动能力强依赖 item content embedding 的质量；如果内容特征不足，Semantic ID 的优势会下降。

## 可复用想法

- 把 item ID 从“随机主键”转成“带语义结构的离散表示”，这一思路对推荐和检索都很有启发。
- 用 `RQ-VAE` 生成分层 codeword，使 coarse-to-fine 的语义结构显式化。
- 在读后续 Semantic ID 相关工作时，可以把这篇当作 generative recommendation 的起点论文。

## 我的问题

- `Semantic ID` 的 token 长度、codebook 规模和唯一性约束之间到底怎么平衡？
- 这种方法在 item 内容特征很弱、甚至几乎没有文本描述时还能否稳定成立？
- 如果把这个范式搬到工业场景，生成式延迟和召回覆盖率要如何权衡？

## 讨论后更新的理解

- 当前版本还是速读草稿，已经保留了完整 abstract、来源信息和候选图表页。
- 下一轮适合继续深挖的部分是：`RQ-VAE` 的层次化量化细节、cold-start 实验设置，以及表 1 / 表 2 的精确转写。
