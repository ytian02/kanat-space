---
title: "L1和L2正则化"
slug: "ml-ii-l1-and-l2-regularization"
subtitle: ""
description: "L1/L2 正则化的特点、几何解释与概率解释。"
date: 2026-03-14T22:23:00+08:00
lastmod: 2026-03-14T22:23:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 机器学习
- 正则化

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

- 🎯 **目标读者**：想理解 L1/L2 正则化差异与直觉的读者
- ⏱️ **阅读时间**：约 5 分钟
- 📚 **知识要点**：L1/L2 特点对比、几何解释、梯度解释、MAP 概率解释

# Machine Learning

## L1和L2正则化

### 1. 特点
- L1 正则化倾向于产生稀疏解（部分参数变 0），常用于特征选择。
- L2 正则化倾向于整体缩小参数，通常不为 0，可抑制过拟合。

### 2. 几何解释
- L1 约束域是菱形，更容易在坐标轴处取到最优点。
- L2 约束域是圆形，更倾向平滑收缩。

### 3. 导数解释
- L1：梯度近似 $\text{sign}(w)$，对小权重仍有明显收缩作用。
- L2：梯度为 $2w$，权重越小梯度越小。

### 4. 概率解释
从 MAP 角度看，L1 对应 Laplace 先验，L2 对应 Gaussian 先验。
