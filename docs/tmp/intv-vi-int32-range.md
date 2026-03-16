---
title: "为什么32位二进制的最小值是$-2^{31}$,最大值是$2^{31}-1$"
slug: "intv-vi-int32-range"
subtitle: ""
description: "32 位有符号整数范围的补码解释。"
date: 2026-03-14T22:44:00+08:00
lastmod: 2026-03-14T22:44:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 面试
- 计算机基础

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

- 🎯 **目标读者**：想理解补码与整数范围基础的读者
- ⏱️ **阅读时间**：约 2 分钟
- 📚 **知识要点**：32 位补码、符号位、为何范围不对称

# Interview

## 为什么32位二进制的最小值是$-2^{31}$,最大值是$2^{31}-1$

### 补码视角解释
- 最高位为符号位（0 正、1 负）。
- 正数可表示到 $2^{31}-1$。
- 负数可表示到 $-2^{31}$。
- 因为 0 只有一种编码，所以范围在绝对值上不对称。
