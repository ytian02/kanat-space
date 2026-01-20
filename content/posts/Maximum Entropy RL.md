---
title: "V Maximum Entropy RL"
slug: "V Maximum Entropy RL"
# 副标题
subtitle: ""
# 文章描述，是搜索引擎呈现在搜索结果链接下方的网页简介，建议设置
description: ""
date: 2026-01-19T20:34:49+08:00
lastmod: 2026-01-19T20:34:49+08:00
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
最大熵强化学习在标准RL的基础上引入了熵正则项，以鼓励策略网络的输出更具多样性。
## 目标
在最大熵强化学习中，学习目标被定义为
$$J(\theta)=\mathbb{E}_S\left[V^\pi(S)+\alpha H(S;\theta)\right],$$
其中$H(s;\theta)=-\sum\limits_{a\in\mathcal{A}}\pi(a\vert s;\theta)\log\pi(a\vert s;\theta)$。
## 常见算法
Soft Q-learning, SAC
## 软价值函数
在标准的Q-learning中，状态价值函数$V(s)=\max\limits_{a\in\mathcal{A}}Q(s,a)$，而最大化操作是一种硬操作，而在最大熵强化学习的框架下，状态价值函数变成
$$V_\text{soft}(s)=\alpha\log\left(\sum\limits_{a}\exp\left(\dfrac{Q_\text{soft}(s,a)}{\alpha}\right)\right),$$其中$\alpha$是温度系数，控制熵正则项的重要性。
## 详细推导
给定状态$s$，最大熵强化学习的优化目标为$$\max\limits_{\pi}V_\text{soft}(s)=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)Q(s,a)-\alpha\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\log\pi(a\vert s),\quad \text{s.t. }\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)=1.$$利用拉格朗日乘子法引入乘子$\lambda$构建拉格朗日函数$\mathcal{L}$$$\mathcal{L}(\pi,\lambda)=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\left(Q(s,a)-\alpha\log\pi(a\vert s)\right)-\lambda(\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)-1),$$通过对$\pi(a\vert s)$求偏导可得$$\dfrac{\partial\mathcal{L}(\pi,\lambda)}{\partial\pi(a\vert s)}=Q(s,a)-\alpha-\alpha\log\pi(a\vert s)-\lambda=0,$$求解可得$$\pi(a\vert s)=\exp\left(\dfrac{Q(s,a)}{\alpha}\right)\cdot\left(-\dfrac{\lambda}{\alpha}-1\right),$$由于$\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)=1$，可以通过归一化来消除常数项，进而得到最优策略$$\pi(a\vert s)=\dfrac{\exp\left(\dfrac{Q(s,a)}{\alpha}\right)}{\sum\limits_{a^\prime\in\mathcal{A}}\exp\left(\dfrac{Q(s,a^\prime)}{\alpha}\right)}$$这是一个关于Q值的Boltzmann分布，将最优策略代入优化目标可得$$\begin{align}
V_\text{soft}(s)&=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\cdot \left[Q(s,a)-\alpha\log \dfrac{\exp\left(\dfrac{Q(s,a)}{\alpha}\right)}{Z}\right],\\
&=\alpha\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\log Z,\\
&=\alpha\log\sum\limits_{a^\prime\in\mathcal{A}}\exp\left(\dfrac{Q(s,a^\prime)}{\alpha}\right),
\end{align}$$这也就是软价值函数的定义。

## 未完待续
后续会整理SAC的原理和实现。