---
title: "常见的损失函数"
slug: "ml-i-common-loss-functions"
subtitle: ""
description: "回归、分类、度量学习与对比学习常见损失函数。"
date: 2026-03-14T22:22:00+08:00
lastmod: 2026-03-14T22:22:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 机器学习
- 损失函数

categories:
- 基础知识

collections:
- Machine Learning

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

- 🎯 **目标读者**：想系统梳理机器学习常见损失函数的读者
- ⏱️ **阅读时间**：约 8 分钟
- 📚 **知识要点**：回归/分类损失、度量学习损失、NCE 与 InfoNCE

# Machine Learning

## 常见的损失函数

### 一、回归任务 (Regression)
- MSE：
  $$L_{MSE}=\frac{1}{N}\sum_{i=1}^N(y_i-\hat y_i)^2$$
- MAE：
  $$L_{MAE}=\frac{1}{N}\sum_{i=1}^N|y_i-\hat y_i|$$
- Huber / Smooth L1：小误差近似 MSE，大误差近似 MAE。

### 二、分类任务 (Classification)
- NLL：$L_{NLL}=-\sum_i\log p(y_i\mid x_i)$。
- CE：
  $$L_{CE}=-\sum_x p(x)\log q(x)$$
- KL 散度：
  $$D_{KL}(P\Vert Q)=\sum_x P(x)\log\frac{P(x)}{Q(x)}$$
  且 $CE=H(P)+D_{KL}(P\Vert Q)$。

### 三、相似度与度量学习 (Similarity & Metric Learning)
- Cosine Embedding Loss：优化向量方向相似性。
- Triplet Loss：
  $$L=\max(d(A,P)-d(A,N)+\text{margin},0).$$

### 四、对比学习与自监督学习 (Contrastive Learning)
- NCE：将多分类近似为真样本与噪声样本的二分类。
- InfoNCE：
  $$L_{InfoNCE}=-\log\frac{\exp(\text{sim}(q,k_+)/\tau)}{\sum_{i=0}^{K}\exp(\text{sim}(q,k_i)/\tau)}.$$
