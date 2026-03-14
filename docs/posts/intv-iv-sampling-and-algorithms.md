---
title: "第四类：数据采样与算法结合"
slug: "intv-iv-sampling-and-algorithms"
subtitle: ""
description: "蓄水池采样与随机函数构造问题。"
date: 2026-03-14T22:42:00+08:00
lastmod: 2026-03-14T22:42:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 面试
- 采样
- 算法

categories:
- 面试

collections:
- Interview

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

- 🎯 **目标读者**：准备随机算法与采样题的读者
- ⏱️ **阅读时间**：约 5 分钟
- 📚 **知识要点**：蓄水池采样、拒绝采样、Rand5 到 Rand7 构造

# Interview

## 第四类：数据采样与算法结合

### 9. 蓄水池采样 (Reservoir Sampling)
未知总数数据流中，保持每个元素以相同概率进入大小为 $k$ 的样本池。

### 10. Rand5() 实现 Rand7()
通过拒绝采样在 1~25 的均匀空间中截取 1~21，再映射到 1~7。
