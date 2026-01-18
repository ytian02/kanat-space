---
title: "III Policy Based RL"
slug: "III Policy Based RL"
# 副标题
subtitle: ""
# 文章描述，是搜索引擎呈现在搜索结果链接下方的网页简介，建议设置
description: "本文梳理了基于策略的强化学习算法。"
date: 2026-01-15T21:25:46+08:00
lastmod: 2026-01-15T21:25:46+08:00
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
weight: 4

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
策略学习方法关注如何近似最优策略，优化目标是$J(\theta)=\mathbb{E}_S\left[V^\pi(S)\right]$，其中$\theta$是策略$\pi$的参数。

## 策略梯度公式 
$$\dfrac{\partial J(\theta)}{\partial\theta}=\mathbb{E}_{S}\left[\mathbb{E}_{A\sim\pi(\cdot\vert S;\theta)}\left[\dfrac{\partial\log\pi(A\vert S;\theta)}{\partial\theta}\cdot Q^\pi(S,A)\right]\right].$$事实上，对状态的期望前面应该还有系数$\dfrac{1-\gamma^n}{1-\gamma}$，但在实际应用中，该系数可以忽略，这是因为在做梯度上升时，系数会被学习率吸收。此外，策略梯度定理只有在状态$S$服从马尔可夫链的稳态分布$d(\cdot)$时成立。**注：其实有点像使用Q值加权策略的梯度上升过程。**

## 广义优势估计(Generalized Advantage Estimation, GAE)
参考[六、GAE 广义优势估计 - 知乎](https://zhuanlan.zhihu.com/p/549145459)整理

### 背景
在Policy-based RL中，经常引入baseline $V^\pi(s)$ 来计算优势值函数 $$A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)=\mathbb{E}_{s^\prime \sim P(s^\prime\vert s,a)}\left(r(s,a)+\gamma V^\pi(s^\prime)-V^\pi(s)\right),$$由于使用神经网络$V_\theta(s)$近似值函数时存在偏差，因此在使用损失函数$\mathbb{E}_{s,a,s^\prime}\left[r(s,a)+\gamma V_\theta(s^\prime)-V_\theta(s)\right]^2$（TD方法）优化优势值估计是一种**高偏差、低方差**（只涉及单步值估计）的方法，考虑到状态价值函数的定义$$V^\pi(s_t)=\mathbb{E}_\pi[\sum\limits_{k=0}^n\gamma^kR_{t+k}\vert S=s],$$也可以考虑一局游戏结束后使用$\sum\limits_{k=0}^n\gamma^k r_{t+k}$对状态价值函数进行近似（MC方法），进而求解优势值，这是一种**低偏差、高方差**（涉及多步奖励）的方法。为了结合TD和MC的特性，**n步TD方法**考虑了n步回报$$G_{t\colon t+n}=R_t+\gamma R_{t+1}+\cdots+\gamma^{n-1}R_{t+n-1}+\gamma^nV^\pi(S_{t+n}),$$**λ-return方法**进行了加权平均，平衡了偏差和方差，考虑有限步$T$结束游戏，$$G^\lambda_t=(1-\lambda)\sum\limits_{n=1}^{T-t-1}\lambda^{n-1}G_{t\colon t+n}+\lambda^{T-t-1}G_{t},$$其中$G_t$是折扣回报。当$\lambda=0$时，退化为n步TD方法；当$\lambda=1$时，退化为MC方法。对于无限步，则有$$G_t^\lambda=(1-\lambda)\sum\limits_{n=1}^\infty\lambda^{n-1}G_{t:t+n}.$$
### GAE
GAE借鉴了λ-return方法的思想，考虑优势函数的定义，有
$$\begin{align}&\hat{A}_t^1=r_t+\gamma V(s_{t+1})-V(s_t)=\delta_t\\&\hat{A}_t^2=r_{t}+\gamma r_{t+1}+\gamma^2 V(s_{t+2})-V(s_t)=\delta_t+\gamma\delta_{t+1}\\&\cdots\\&\hat{A}_t^n=r_{t}+\gamma r_{t+1}+\cdots+\gamma^{n-1}r_{t+n-1}+\gamma^n V(s_{t+n})-V(s_t)=\sum\limits_{k=1}^n\gamma^{k-1}\delta_{t+k-1}\\&\cdots\\&\hat{A}_t^\infty=\sum\limits_{l=0}^\infty\gamma^{l}r_{t+l}-V(s_t)=\sum\limits_{l=0}^\infty\gamma^l\delta_{t+l}\end{align}$$参考λ-return方法，考虑无限步的推导，有
$$\begin{align}\hat{A}_t^{\text{GAE}(\lambda,\gamma)}&=(1-\lambda)\sum\limits_{n=1}^{\infty}\lambda^{n-1}\hat{A}_t^n\\&=\sum\limits_{l=0}^\infty(\gamma\lambda)^l\delta_{t+l}\\&=\sum\limits_{l=1}^\infty(\gamma\lambda)^l\delta_{t+l}+\delta_t\\&=\gamma\lambda\hat{A}_{t+1}^{\text{GAE}(\lambda,\gamma)}+\delta_{t}\end{align}$$

GAE详细的推导过程也可以参考[11.6 广义优势估计](https://hrl.boyuai.com/chapter/2/trpo%E7%AE%97%E6%B3%95#116-%E5%B9%BF%E4%B9%89%E4%BC%98%E5%8A%BF%E4%BC%B0%E8%AE%A1)，写得也很清楚。

## Value-based RL
### Reinforce
通过策略梯度和（回报的）蒙特卡洛近似$u_t$直接优化策略网络$\pi(a\vert s;\theta)$

[Simple statistical gradient-following algorithms for connectionist reinforcement learning (Williams, ML, 1992)](https://link.springer.com/article/10.1007/bf00992696)[[Code]](https://hrl.boyuai.com/chapter/2/%E7%AD%96%E7%95%A5%E6%A2%AF%E5%BA%A6%E7%AE%97%E6%B3%95)

### Reinforce with baseline
引入了状态价值网络$v(s;\omega)$作为基线，状态价值网络使用$u_t$作为监督信号来训练。

(论文引用同上)

### Actor-Critic
使用策略梯度优化策略网络$\pi(a\vert s;\theta)$(actor)，TD算法优化动作价值网络$q_\omega(s,a;\omega)$(critic)

[Actor-Critic Algorithms (Konda, NeurIPS, 1999)](https://proceedings.neurips.cc/paper/1999/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html)[[Code]](https://hrl.boyuai.com/chapter/2/actor-critic%E7%AE%97%E6%B3%95)

注: 也有说法认为Actor-Critic方法起源于[Neuronlike adaptive elements that can solve difficult learning control problems (Barto et al., Tos, 1983)](https://psycnet.apa.org/record/1984-13799-001?ref=https:%2F%2Fgithubhelp.com),或[Policy Gradient Methods for Reinforcement Learning with Function Approximation (Sutton et al., NeurIPS, 1999)](https://proceedings.neurips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html)


### A2C (Advantage Actor-Critic)
引入状态价值网络$v(s;\omega)$作为基线，使用TD算法更新$v(\omega)$，并根据$v(s;\omega)$计算的TD误差和策略梯度更新策略网络$\pi(a\vert s;\theta)$

[OpenAI Baselines: ACKTR & A2C (OpenAI, 2017)](https://openai.com/index/openai-baselines-acktr-a2c/)[[Code]](https://github.com/openai/baselines/tree/master/baselines/a2c)

### TRPO (Trust Region Policy Optimization)
**(置信域算法的思想)** 找一个在当前参数$\theta_\text{now}$的邻域上距离复杂的目标函数$J(\theta)$很近的简单函数$L(\theta\vert\theta_\text{now})$，在邻域中寻找$\theta$的值最大化$L(\theta\vert\theta_\text{now})$并更新参数。

**(TRPO中的置信域算法)** $$L(\theta\vert\theta_\text{now})=\mathbb{E}_S\left[\mathbb{E}_{A\sim\pi(\cdot\vert s;\theta_\text{now})}\left[\dfrac{\pi(A\vert S;\theta)}{\pi(A\vert S;\theta_\text{now})}\cdot Q^\pi(s,A)\right]\right],$$并进一步使用蒙特卡洛模拟(两步近似$Q^\pi\to Q^{\pi_\text{now}}\to u_t$)转化成$$\tilde{L}(\theta\vert\theta_\text{now})=\dfrac{1}{n}\sum\limits_{t=1}^n\dfrac{\pi(s_t,a_t;\theta)}{\pi(s_t,a_t;\theta_\text{now})}\cdot u_t.$$在最大化时，可以选择欧几里得距离选取置信域，也可以用KL散度$$\max\limits_{\theta}\tilde{L}(\theta\vert\theta_\text{now}),\quad \text{s.t. }\dfrac{1}{n}\sum\limits_{t=1}^nD_\text{KL}\left(\pi(\cdot\vert s_t;\theta_\text{now})\Vert\pi(\cdot\vert s_t;\theta)\right)\leq\Delta,$$这是一个约束优化问题，**代码实现较为复杂**。一些文献使用优势函数$A^\pi(S,A)=Q^\pi(S,A)-V^\pi(S)$替换$Q^\pi(s,a)$，然后使用GAE计算优势值，注意有$A^\pi(s,a)=\mathbb{E}_{s^\prime}(r(s,a)+\gamma V^\pi(s^\prime)-V^\pi(s))$。

[Trust Region Policy Optimization (Schulman et al., ICML, 2015)](https://proceedings.mlr.press/v37/schulman15.html)[[Code]](https://hrl.boyuai.com/chapter/2/trpo%E7%AE%97%E6%B3%95)

### PPO (Proximal Policy Optimization)
TRPO的改进版，有两种形式

**PPO-Penalty:** 用拉格朗日乘子法将TRPO中的KL散度约束放进了目标函数中，并在迭代的过程中不断更新KL散度的系数$$\arg\max\limits_{\theta}\mathbb{E}_S\mathbb{E}_{A\sim\pi(\cdot\vert S;\theta_\text{now})}\left[\dfrac{\pi(A\vert S;\theta)}{\pi(A\vert S;\theta_\text{now})}A^\pi(S,A)-\beta D_\text{KL}\left(\pi(\cdot\vert S;\theta_\text{now})\Vert\pi(\cdot\vert S;\theta)\right)\right].$$当KL散度项小于$\delta/1.5$时令$\beta$缩小一半，当大于$\delta/1.5$时增大一倍，等于时维持现状。

**PPO-Clip:** $$\arg\max\limits_{\theta}\mathbb{E}_S\mathbb{E}_{A\sim\pi(\cdot\vert S;\theta_\text{now})}\left[\min\left\{\dfrac{\pi(A\vert S;\theta)}{\pi(A\vert S;\theta_\text{now})}A^\pi(S,A),\text{clip}\left(\dfrac{\pi(A\vert S;\theta)}{\pi(A\vert S;\theta_\text{now})},1-\epsilon,1+\epsilon\right)A^\pi(S,A)\right\}\right],$$其中$\text{clip}(x,l,r)\coloneqq\max\left\{\min\left\{x,r\right\},l\right\}$，$\epsilon>0$是一个超参数，**当优势大于0时，说明动作价值高于平均，最大化这个式子会增大比值，但不会超过$1+\epsilon$；当优势小于0时，说明动作价值低于平均，则最大化u这个式子会缩小比值，但不会低于$1-\epsilon$。**

大量的实验表明PPO-Clip比PPO-Penalty更好。简单来说，PPO-Clip可以理解为对于好动作（优势值大于0），提升策略生成动作的概率，但是不能偏离基准策略太远；对于坏动作（优势值小于0），降低策略生成动作的概率，但是不能偏离基准策略太远。

[Proximal Policy Optimization Algorithms (Schulman et al., 2017)](https://arxiv.org/abs/1707.06347)[[Code]](https://hrl.boyuai.com/chapter/2/ppo%E7%AE%97%E6%B3%95)

### DDPG (Deep Deterministic Policy Gradient)
使用（确定性）策略网络$\mu(s;\theta)$学习最优策略，目标定义为$$J(\theta)=\mathbb{E}_S\left[q(S,\mu(S;\theta);\omega)\right],$$其中价值网络使用TD算法进行更新，策略网络通过最大化当前的价值网络进行更新。注意DDPG的价值网络近似动作价值函数而非最优动作价值函数；在选择动作时，一般会加一个噪声$\epsilon$。DDPG中也存在最大化（当前的价值网络）和自举造成的高估问题。

[Continuous control with deep reinforcement learning (DeepMind, 2015)](https://arxiv.org/abs/1509.02971)[[Code]](https://hrl.boyuai.com/chapter/2/ddpg%E7%AE%97%E6%B3%95)

### TD3 (Twin Delayed Deep Deterministic Gradient)
针对DDPG的高估问题，使用两个价值网络和一个策略网络，对应三个目标网络$q(s,a;\omega_1^-),q(s,a;\omega_2^-),\mu(s;\theta^-)$，在计算TD target时，策略目标网络输出动作向量，然后取两个价值目标网络输出的较小值作为TD target。此外，TD3还有一些细节: **(动作噪声)** 在计算TD target的输出动作步骤中，加入各元素从截断正态分布$\mathcal{CN}(0,\sigma^2,-c,c)$(防止噪声过大)中采样的噪声向量；**(更新频率)** 减小更新策略网络和目标网络的频率。

[Addressing Function Approximation Error in Actor-Critic Methods (Fujimoto et al., ICML, 2018)](https://proceedings.mlr.press/v80/fujimoto18a.html)[[Code]](https://github.com/sfujim/TD3)

### 随机高斯策略 (Stochastic Gaussian Policy)
使用两个神经网络分别近似高斯分布的均值和对数方差，利用重参数化技巧进行动作采样，并用策略梯度更新两个神经网络的参数。

随机高斯策略最早出现在Reinforce (Williams, 1992) 的论文中，作为处理连续动作空间（Continuous Action Spaces）的标准方法。Williams 在文中明确推导了当策略网络输出高斯分布的均值（$\mu$）和标准差（$\sigma$）时的梯度更新公式。(Gemini说的,不保真)

### SAC(Soft Actor-Critic)
SAC的前身是Soft Q-learning，都属于最大熵强化学习，Soft Q-learning 不存在一个显式的策略函数，而是使用一个函数的波尔兹曼分布，在连续空间下求解非常麻烦。于是 SAC 提出使用一个 Actor 表示策略函数，从而解决这个问题。SAC使用了两个Critic网络和对应的目标网络，在计算计算TD目标和策略更新时都取两个网络的最小值。由于在学习目标中加入了熵正则项，因此TD目标和策略更新都多了一个log pi(s\vert a)项。注意SAC输出的是随机高斯策略。

[Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor (Haarnoja, ICML, 2018)](https://proceedings.mlr.press/v80/haarnoja18b)[[Code]](https://hrl.boyuai.com/chapter/2/sac%E7%AE%97%E6%B3%95)

## 连续控制问题
在连续动作向量的问题中，一个自然的想法是通过离散化动作空间然后训练DQN或者策略网络，但是随着自由度的增大，离散后的动作空间的大小指数增长，会造成维数灾难，DQN和策略网络的训练都变得异常困难。在真实的环境中，虽然动作空间可能是离散的，但是可能动作空间非常庞大（比如推荐系统的item数量），往往会输出连续动作向量再映射到有效动作空间（比如item列表），DDPG、TD3就是处理连续动作空间的有效办法。

## 同策略(On-Policy)和异策略(Off-Policy) 
**定义:** 首先引入行为策略(behavior policy)和目标策略(target policy)的概念，行为策略是与环境交互收集经验的策略，训练时的策略称为目标策略，如果行为策略和目标策略相同，称为同策略，如果不同则称为异策略。

**常见算法分类:** 常见的同策略方法包括Reinforce(收集$u_t$和用于训练的策略是同一策略)、Reinforce with baseline(同理)、Actor-Critic(使用SARSA算法训练，且策略梯度是根据目标策略计算的)、A2C(没有经验回放池)、TRPO(与A2C同理)；常见的异策略方法包括DQN及其变体(使用经验回放数组)、DDPG(同理)、TD3(同理)、SAC

## 代码实现细节 
**目标网络:** 通常目标网络的参数不加入优化器，而是定期根据价值网络或策略网络的参数进行优化；

**随机策略:** 在策略梯度的算法中，如果使用的是随机策略，一般用神经网络输出logits再经过softmax得到每个动作的概率，在选择动作时使用一个类别分布进行抽样得到动作