---
title: "II Value-Based RL"
slug: "II Value-Based RL"
# 副标题
subtitle: ""
# 文章描述，是搜索引擎呈现在搜索结果链接下方的网页简介，建议设置
description: "本文梳理了基于价值的强化学习算法。"
date: 2026-01-10T19:36:47+08:00
lastmod: 2026-01-10T19:37:47+08:00
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

## AI 含量说明

本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。

## 本文概览

- 🎯 **目标读者**：已了解 MDP/贝尔曼方程，想快速建立 value-based RL 全景的读者
- ⏱️ **阅读时间**：约 10 分钟
- 📚 **知识要点**：Q-learning 思想、DQN 训练套路（回放池/目标网络）、高估偏差、Double DQN、Dueling 结构

价值学习（value-based RL）的核心目标是学习（或近似）最优动作价值函数 $Q^*(s,a)$，再用贪心策略从 $Q$ 中导出动作选择。与 policy gradient 直接优化策略不同，value-based 方法往往把“策略改进”隐含在 $\arg\max$ 里。

## 基本概念
价值学习方法关注如何近似最优价值函数$Q^\ast(s,a)$，使用$\pi(a\vert s)=\arg\max\limits_{a}Q^\ast(s,a)$作为最优策略。

一个直观理解是：只要我们能对“在状态 $s$ 下做动作 $a$ 值不值”给出足够准确的评分（$Q$ 值），就可以通过“选分数最高的动作”来得到一个很强的策略。

## 常见算法
### DQN
DQN 可以理解为把 **tabular Q-learning** 的更新（对 $Q(s,a)$ 做自举 bootstrapping）推广到深度网络函数逼近：用一个神经网络 $Q(s,a;\theta)$ 来近似动作价值函数。

在最常见的实现里，DQN 的训练目标是让网络输出的 $Q(s_t,a_t;\theta)$ 拟合 TD target：

$$
 y_t = r_t + \gamma \max_{a'} Q(s_{t+1}, a'; \theta^-) ,
$$

并最小化均方误差损失：

$$
 \mathcal{L}(\theta)=\mathbb{E}\left[\left(Q(s_t,a_t;\theta)-y_t\right)^2\right].
$$

让 DQN “能跑起来且比较稳定”的关键经验通常有三条：

- **Experience Replay（回放池）**：打乱样本相关性、提升样本复用率。
- **Target Network（目标网络）**：用延迟参数 $\theta^-$ 计算 target，降低自举目标随训练剧烈漂移带来的不稳定。
- **Exploration（探索）**：最常见是 $\epsilon$-greedy，用一定概率随机选动作，避免过早陷入局部最优。

[Playing Atari with Deep Reinforcement Learning (DeepMind, 2013)](https://arxiv.org/pdf/1312.05602) [[Code]](https://hrl.boyuai.com/chapter/2/dqn%E7%AE%97%E6%B3%95)

### Double DQN
DQN 的一个经典问题是 **高估偏差（overestimation）**：由于 target 中的 $\max$ 同时承担“选动作”和“评估动作”的角色，在有噪声/函数逼近误差时往往会系统性偏大。

Double DQN 的核心思想是把“选择”和“评估”解耦：

- 用在线网络选动作：$a^* = \arg\max_{a'} Q(s_{t+1}, a'; \theta)$
- 用目标网络评估：$y_t = r_t + \gamma Q(s_{t+1}, a^*; \theta^-)$

这通常能明显缓解高估问题，同时几乎不增加实现复杂度。

[Deep Reinforcement Learning with Double Q-learning (DeepMind, AAAI, 2016)](https://ojs.aaai.org/index.php/AAAI/article/view/10295) [[Code]](https://hrl.boyuai.com/chapter/2/dqn%E6%94%B9%E8%BF%9B%E7%AE%97%E6%B3%95)

### Dueling DQN
Dueling 结构更关注表示学习：在很多状态下，“各个动作之间差别不大”，但“这个状态整体好不好”很关键。

因此它把 $Q(s,a)$ 拆成两部分来建模：

- 状态价值（state value）：$V(s)$，表示状态本身好坏
- 优势（advantage）：$A(s,a)$，表示相对该状态下平均水平，动作 $a$ 额外带来的增益

常见写法是：

$$
Q(s,a)=V(s)+\left(A(s,a)-\frac{1}{\lvert\mathcal{A}\rvert}\sum_{a'}A(s,a')\right),
$$

通过减去均值来消除 $V$ 和 $A$ 的不唯一性问题。Dueling 结构通常能提升学习效率与泛化（尤其在动作很多、但大部分动作在当前状态意义不大的场景）。

[Dueling Network Architectures for Deep Reinforcement Learning (Google, ICLR, 2016)](https://proceedings.mlr.press/v48/wangf16.html) [[Code]](https://hrl.boyuai.com/chapter/2/dqn%E6%94%B9%E8%BF%9B%E7%AE%97%E6%B3%95)

### 小结
如果把 value-based RL 当作“学评分函数 $Q$”的路线，那么：

- DQN 给了一个可扩展到高维状态的基础训练框架（replay + target + TD loss）。
- Double DQN 主要修复了 $\max$ 带来的系统性高估偏差。
- Dueling DQN 更像是对网络结构的归纳偏置（inductive bias），让表示更贴近问题本身。