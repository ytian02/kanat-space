---
title: "常用指标"
slug: "gr-iv-common-metrics"
subtitle: ""
description: "推荐系统常见评估指标与场景化建议。"
date: 2026-03-14T22:35:00+08:00
lastmod: 2026-03-14T22:35:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 推荐系统
- 评估指标

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

- 🎯 **目标读者**：需要快速选型推荐评估指标的读者
- ⏱️ **阅读时间**：约 4 分钟
- 📚 **知识要点**：RMSE/MAE、Recall/NDCG/AUC、不同业务场景指标重点

# General Recommender System

## 常用指标

### 常见指标
1. 评分预测：RMSE、MAE
2. Top-N 排序：Precision@K、Recall@K、MAP、NDCG、MRR
3. 非精度指标：Coverage、Diversity、Novelty

### 场景建议
- 电商/短视频：重点关注 Recall + NDCG。
- CTR 预估：重点关注 AUC + LogLoss。
- 研究报告：通常同时汇报 Precision/Recall/NDCG@K。
