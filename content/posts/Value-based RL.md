---
title: "Value Based RL"
slug: "Value-Based RL"
# 副标题
subtitle: ""
# 文章描述，是搜索引擎呈现在搜索结果链接下方的网页简介，建议设置
description: "本文梳理了基于价值的强化学习算法。"
date: 2026-01-10T19:36:47+08:00
lastmod: 2026-01-10T19:36:47+08:00
# 文章过期提醒
outdatedInfoWarning: true
draft: false

# 文章的标签
tags: 
- RL

# 文章所属的类别
categories:
- Algorithms

# 文章所属的合集
collections:
- Reinforcement Learning

# [重要] 开启本页面的数学公式支持
math: true

# 是否在侧边栏开启合集
collectionList: true
# 是否在帖子末尾启用合集
collectionNavigation: true

# 如果设为 true, 这篇文章将不会显示在主页上
hiddenFromHomePage: false
# 如果设为 true, 这篇文章将不会显示在搜索结果中
hiddenFromSearch: false

# 文章的特色图片
featuredImage: ""
# 用在主页预览的文章特色图片
featuredImagePreview: ""

---
价值学习方法关注如何近似最优价值函数$Q^\ast(s,a)$，使用$\pi(a\vert s)=\arg\max\limits_{a}Q^\ast(s,a)$作为最优策略。
- **DQN:** 通过最优贝尔曼方程和（期望的）蒙特卡洛近似推导出TD算法训练
- **Double DQN:** 在DQN的基础上引入目标网络缓解（由max操作和自举导致的）高估问题
- **Dueling DQN:** 通过优势头$A(s,a;\omega^A)$和状态价值头$V(s;\omega^V)$近似最优价值函数，也可以使用目标网络的技术缓解高估问题