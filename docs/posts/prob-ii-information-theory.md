---
title: "信息论"
slug: "prob-ii-information-theory"
subtitle: ""
description: "熵、交叉熵、KL 散度与互信息。"
date: 2026-03-14T22:21:00+08:00
lastmod: 2026-03-14T22:21:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 信息论
- 熵
- KL散度

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

- 🎯 **目标读者**：想快速建立信息论基础概念框架的读者
- ⏱️ **阅读时间**：约 6 分钟
- 📚 **知识要点**：熵、交叉熵、KL 散度、互信息及其关系

# Probability

## 信息论

### 1. 熵(Entropy) & 交叉熵(Cross Entropy) & KL散度(KL Divergence)
- **熵**：
  $$H(X)=-\sum_{x\in\mathcal X}p(x)\log p(x),\quad 0\log0=0.$$
  熵度量随机变量不确定性，且 $H(X)\ge 0$。
- **联合熵与条件熵**：
  $$H(X,Y)=-\sum_{x,y}p(x,y)\log p(x,y),$$
  $$H(Y\mid X)=-\sum_{x,y}p(x,y)\log p(y\mid x).$$
  链式法则：$H(X,Y)=H(X)+H(Y\mid X)$。
- **KL 散度**：
  $$D_{KL}(p\Vert q)=\sum_x p(x)\log\frac{p(x)}{q(x)}\ge 0.$$
  当且仅当 $p=q$ 时取 0。
- **互信息**：
  $$I(X;Y)=D_{KL}(p(x,y)\Vert p(x)p(y))$$
  并有
  $$I(X;Y)=H(X)-H(X\mid Y)=H(Y)-H(Y\mid X).$$
- **信息量**：$f(X=x)=-\log p(x)$。
- **交叉熵**：
  $$H(p,q)=-\sum_x p(x)\log q(x).$$

> [待插入图片：互信息示意图（原文 `Pasted image 20251208123304.png`）]
