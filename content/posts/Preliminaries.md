---
title: "Preliminaries"
slug: "Preliminaries"
# 副标题
subtitle: ""
# 文章描述，是搜索引擎呈现在搜索结果链接下方的网页简介，建议设置
description: "本文主要梳理马尔可夫决策过程中的基本概念和贝尔曼方程。"
date: 2026-01-10T17:09:18+08:00
lastmod: 2026-01-10T17:09:18+08:00
# 文章过期提醒
outdatedInfoWarning: true
draft: false

# 文章的标签
tags: 
- RL

# 文章所属的类别
categories:
- Basic

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

**折扣回报(discounted return):** 

定义了从当前时刻的状态开始到终止状态结束时所有奖励的之和，考虑到未来奖励的不确定性，引入了折扣因子$\gamma$$$U_t=R_t+\gamma R_{t+1}+\gamma^2 R_{t+2}+\cdots=\sum\limits_{k=0}\gamma^kR_{t+k},$$注意$U_t$是一个随机变量，依赖于未来的状态和动作。

**状态价值函数(state value function)和动作价值函数(state-action value function):** 

状态价值函数衡量在策略$\pi$下，当前状态的期望回报(衡量状态的好坏)$$V^\pi(s)=\mathbb{E}_\pi\left[U_t\vert S_t=s\right].$$动作价值函数衡量在策略$\pi$下，当前状态下采取某种动作的期望回报(衡量动作的好坏)$$Q^\pi(s,a)=\mathbb{E}_\pi\left[U_t\vert S_t=s,A_t=a\right].$$不难发现状态价值函数和动作价值函数存在如下关系
$$\begin{align}&V^\pi(s)=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)Q^\pi(s,a),\\&Q^\pi(s,a)=r(s,a)+\gamma\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)V^\pi(s^\prime),\end{align}$$其中$r(s,a)$是环境的奖励函数，$P(s^\prime\vert s,a)$是环境的状态转移函数，共同构成了环境动态。

**贝尔曼方程(Bellman equation):** 

不难推导出两个价值函数的贝尔曼方程

$$\begin{align}&V^\pi(s)=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\left[r(s,a)+\gamma\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)V^\pi(s^\prime)\right],\\&Q^\pi(s,a)=r(s,a)+\gamma\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\sum\limits_{a^\prime\in\mathcal{A}}\pi(a^\prime\vert s^\prime)Q^\pi(s^\prime,a^\prime),\end{align}$$为了和TD learning对应，贝尔曼方程可以改写为如下形式

$$\begin{align}&V^\pi(s)=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\left[\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\left[r(s,a)+\gamma V^\pi(s^\prime)\right]\right],\\&Q^\pi(s,a)=\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\left[r(s,a)+\gamma\sum\limits_{a^\prime\in\mathcal{A}}\pi(a^\prime\vert s^\prime)Q^\pi(s^\prime,a^\prime)\right],\end{align}$$

**最优状态价值函数和最优动作价值函数:** 

考虑策略空间$\Pi$中的偏序关系: 当且仅当对于任意状态$s\in\mathcal{S}$都有$V^\pi(s)\geq V^{\pi^\prime}(s)$，记$\pi\succ\pi^\prime$。假设存在最优策略（比其他所有策略都好或者不差于其他所有策略），记为$\pi^\ast$，定义最优价值函数$$V^\ast(s)=\max\limits_{\pi}V^\pi(s),$$以及最优动作价值函数$$Q^\ast(s,a)=\max\limits_{\pi}Q^\pi(s,a).$$考虑到为了使得$Q^\pi(s,a)$最大需要在$(s,a)$之后都执行最优策略,由最优策略的定义可得$$Q^\ast(s,a)=r(s,a)+\gamma\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)V^\ast(s^\prime),$$这与普通策略下的动作价值函数和状态价值函数之间的关系是一样的，此外考虑到最优策略需要在任意状态都需要执行，因此有$$V^\ast(s)=\max\limits_{a}Q^\ast(s,a).$$

**贝尔曼最优方程(Bellman optimality equation):** 

由上述最优状态价值函数和最优动作价值函数的关系，不难得到贝尔曼最优方程
$$\begin{align}&V^\ast(s)=\max\limits_{a\in\mathcal{A}}\left(r(s,a)+\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)V^\ast(s^\prime)\right)\\&Q^\ast(s,a)=r(s,a)+\gamma\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\max\limits_{a\in\mathcal{A}}Q^\ast(s^\prime,a^\prime)\end{align}$$
为了和TD learning对应，贝尔曼最优方程可以改写为如下形式
$$\begin{align}
&V^\ast(s)=\max\limits_{a\in\mathcal{A}}\left[\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\left[r(s,a)+V^\ast(s^\prime)\right]\right]\\&Q^\ast(s,a)=\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\left[r(s,a)+\gamma\max\limits_{a\in\mathcal{A}}Q^\ast(s^\prime,a^\prime)\right]
\end{align}$$

**注:** 以上最优策略的定义是定义在finit MDP中的，详见Sutton《Reinforcement learning: an introduction》- 3.6 Optimal Policies and Optimal Value Functions.