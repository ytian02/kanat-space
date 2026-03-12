---
title: "II Value-Based RL"
slug: "II Value-Based RL"
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
## 基本概念
价值学习方法关注如何近似最优价值函数$Q^\ast(s,a)$，使用$\pi(a\vert s)=\arg\max\limits_{a}Q^\ast(s,a)$作为最优策略。
## 常见算法
### DQN
通过最优贝尔曼方程和（期望的）蒙特卡洛近似推导出TD算法训练。

[Playing Atari with Deep Reinforcement Learning (DeepMind, 2013)](https://arxiv.org/pdf/1312.05602)[[Code]](https://hrl.boyuai.com/chapter/2/dqn%E7%AE%97%E6%B3%95)
### Double DQN 
在DQN的基础上引入目标网络缓解（由max操作和自举导致的）高估问题。

[Deep Reinforcement Learning with Double Q-learning (DeepMind, AAAI, 2016)](https://ojs.aaai.org/index.php/AAAI/article/view/10295)[[Code]](https://hrl.boyuai.com/chapter/2/dqn%E6%94%B9%E8%BF%9B%E7%AE%97%E6%B3%95)
### Dueling DQN 
通过优势头$A(s,a;\omega^A)$和状态价值头$V(s;\omega^V)$近似最优价值函数，也可以使用目标网络的技术缓解高估问题

[Dueling Network Architectures for Deep Reinforcement Learning (Google, ICLR, 2016)](https://proceedings.mlr.press/v48/wangf16.html)
[[Code]](https://hrl.boyuai.com/chapter/2/dqn%E6%94%B9%E8%BF%9B%E7%AE%97%E6%B3%95)