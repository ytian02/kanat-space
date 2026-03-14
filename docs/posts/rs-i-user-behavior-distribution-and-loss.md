---
title: "用户的行为分别服从什么概率分布,又能推导出什么损失?"
slug: "gr-i-user-behavior-distribution-and-loss"
subtitle: ""
description: "推荐系统中行为分布建模与损失设计。"
date: 2026-03-14T22:32:00+08:00
lastmod: 2026-03-14T22:32:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 推荐系统
- 概率建模
- 损失函数

categories:
- 基础知识

collections:
- General Recommender System

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

- 🎯 **目标读者**：想从概率建模角度理解推荐行为建模的读者
- ⏱️ **阅读时间**：约 8 分钟
- 📚 **知识要点**：二分类/连续/计数行为分布、BCE/Focal Loss、过离散建模

# General Recommender System

## 用户的行为分别服从什么概率分布,又能推导出什么损失?

### 1. 二分类行为
- 适用：点击、点赞、收藏、关注、转发、点踩。
- 分布：伯努利分布
  $$P(x;p)=p^x(1-p)^{1-x}.$$
- 实践：稀疏正样本常配样本加权或 Focal Loss。

### 2. 连续行为
- 适用：观看时长、完播率。
- 绝对时长常见长尾，可用对数正态或对数变换后 MSE。
- 完播率 $x\in[0,1]$ 可用 Beta 分布：
  $$f(x;a,b)=\frac{1}{B(a,b)}x^{a-1}(1-x)^{b-1}.$$

### 3. 计数型行为
- 适用：评论数、循环播放次数。
- 泊松分布：
  $$P(X=k)=\frac{\lambda^k}{k!}e^{-\lambda}.$$
- 过离散时更常用负二项分布：
  $$P(X=k)=\frac{\Gamma(k+r)}{k!\Gamma(r)}(1-p)^rp^k.$$
