---
title: "LLM VS GR"
slug: "gr-iii-llm-vs-gr"
subtitle: ""
description: "从策略、奖励、状态、数据等维度对比 LLM 与生成式推荐。"
date: 2026-03-14T22:34:00+08:00
lastmod: 2026-03-14T22:34:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 推荐系统
- LLM
- 生成式推荐

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

- 🎯 **目标读者**：希望比较 LLM 与生成式推荐范式差异的读者
- ⏱️ **阅读时间**：约 8 分钟
- 📚 **知识要点**：策略分布、奖励稀疏性、状态转移、MDP 设定、数据与解释性差异

# General Recommender System

## LLM VS GR

### 对比维度
1. 策略分布
2. 奖励信号
3. 状态转移函数
4. MDP 设定
5. 行为概率分布
6. 数据形态
7. 解释性
8. 安全问题

### 关键结论
- LLM 更偏语言序列建模；GR 更偏用户-物品交互系统建模。
- GR 的奖励设计和业务约束更复杂，不能简单照搬 LLM 的 RL 经验。
