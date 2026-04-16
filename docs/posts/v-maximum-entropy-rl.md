---
title: "V Maximum Entropy RL"
description: ""
date: 2026-01-19T20:34:49+08:00
draft: false
tags:
  - RL
categories:
  - Algorithms
collections:
  - Reinforcement Learning
math: true
---


## AI 含量说明

本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。

## 本文概览

- 🎯 **目标读者**：已了解基本 RL/actor-critic，想理解 SAC 背后“最大熵”动机的读者
- ⏱️ **阅读时间**：约 12 分钟
- 📚 **知识要点**：熵正则的直觉、soft value 的形式、Boltzmann 策略、温度系数 $\alpha$、与 SAC 的关系

## 前言
最大熵强化学习（Maximum Entropy RL）可以看作是在“最大化期望回报”的目标上，额外加入“鼓励策略保持随机性”的约束/正则。直觉上，它更偏向“既要拿到高回报，也要尽量保持多样的可选动作”，从而提升探索能力与鲁棒性。

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