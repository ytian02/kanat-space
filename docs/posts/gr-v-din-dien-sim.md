---
title: "DIN & DIEN & SIM"
slug: "gr-v-din-dien-sim"
subtitle: ""
description: "DIN/DIEN/SIM 的适用阶段与损失函数。"
date: 2026-03-14T22:36:00+08:00
lastmod: 2026-03-14T22:36:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 推荐系统
- DIN
- DIEN
- SIM

categories:
- 基础知识

collections:
- General Recommender System

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

- 🎯 **目标读者**：想了解 DIN/DIEN/SIM 工程定位的读者
- ⏱️ **阅读时间**：约 3 分钟
- 📚 **知识要点**：适用阶段、候选 item 依赖、CTR 常用损失

# General Recommender System

## DIN & DIEN & SIM

### 5.1 适用阶段
这类模型通常依赖候选 item，计算复杂度较高，更适合精排阶段或深度排序特征层。

### 5.2 损失函数
CTR 场景下常用二元交叉熵损失。
