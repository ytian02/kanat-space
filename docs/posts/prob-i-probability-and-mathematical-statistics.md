---
title: "概率论与数理统计"
slug: "prob-i-probability-and-mathematical-statistics"
subtitle: ""
description: "概率论与数理统计常见公式与充分统计量梳理。"
date: 2026-03-14T22:20:00+08:00
lastmod: 2026-03-14T22:20:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 概率论
- 数理统计

categories:
- 基础知识

collections:
- Probability

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

- 🎯 **目标读者**：需要复习概率论与数理统计核心概念的读者
- ⏱️ **阅读时间**：约 8 分钟
- 📚 **知识要点**：常见概率公式、条件概率与贝叶斯、充分统计量定义与因子分解定理

# Probability

## 概率论与数理统计

### 1. 常见的概率公式
- 加法公式：$P(A\cup B)=P(A)+P(B)-P(A\cap B)$。
- 条件概率：$P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}$（$P(B)>0$）。
- 乘法公式：$P(A\cap B)=P(A\mid B)P(B)$。
- 全概率公式：若 $\{B_i\}$ 构成完备事件组，则
  $$P(A)=\sum_i P(A\mid B_i)P(B_i).$$
- 贝叶斯公式：
  $$P(B_i\mid A)=\frac{P(A\mid B_i)P(B_i)}{\sum_j P(A\mid B_j)P(B_j)}.$$
- 期望与方差：
  $$\mathbb{E}[X]=\sum_x xP(X=x),\qquad \mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2.$$
- 全期望公式：$\mathbb{E}[X]=\mathbb{E}[\mathbb{E}(X\mid Y)]$。
- 全方差公式：
  $$\mathrm{Var}(X)=\mathbb{E}[\mathrm{Var}(X\mid Y)]+\mathrm{Var}(\mathbb{E}[X\mid Y]).$$

### 2. 充分统计量
- **定义**：设样本 $X=(X_1,\ldots,X_n)$ 来自分布族 $f(x\mid\theta)$。若给定统计量 $T(X)$ 后，条件分布 $P(X\mid T(X),\theta)$ 与 $\theta$ 无关，则称 $T(X)$ 是参数 $\theta$ 的充分统计量。
- **因子分解定理（Neyman-Fisher）**：若
  $$f(x\mid\theta)=g(T(x),\theta)h(x),$$
  则 $T(X)$ 对 $\theta$ 充分。
- **常见例子**：
  - $X_i\sim\text{Bernoulli}(p)$：$T(X)=\sum_i X_i$ 对 $p$ 充分。
  - $X_i\sim\mathcal{N}(\mu,\sigma^2)$（$\sigma^2$ 已知）：$\bar X$ 对 $\mu$ 充分。
  - $X_i\sim\mathcal{N}(\mu,\sigma^2)$（均未知）：$(\sum_i X_i,\sum_i X_i^2)$ 充分。
