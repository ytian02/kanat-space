---
title: "RL4LLM"
slug: "RL4LLM"
# 副标题
subtitle: ""
# 文章描述，是搜索引擎呈现在搜索结果链接下方的网页简介，建议设置
description: ""
date: 2026-01-19T19:12:19+08:00
lastmod: 2026-01-19T19:12:19+08:00
# 文章过期提醒
outdatedInfoWarning: true
draft: false

# 文章的标签
tags:
- LLM
- RL

# 文章所属的类别
categories:
- Algorithms

# 文章所属的合集
collections:
- LLM

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

## 本文概览

- 🎯 **目标读者**：了解基础 RL / policy gradient，想入门 RLHF/LLM 对齐中 PPO/GRPO 思路的读者
- ⏱️ **阅读时间**：约 20 分钟
- 📚 **知识要点**：PPO-Clip 目标函数、ratio/clip 直觉、优势函数的作用、实现要点、与 GRPO 的关系与参考资料

## 前言
这篇笔记把 PPO-Clip 的关键公式与代码实现放在一起看：先理解目标函数每一项在“约束更新幅度”上的作用，再去对照实现细节（log prob、ratio、优势估计等）会更顺。

## PPO
本节主要梳理PPO-Clip算法原理和代码实现。引用[GRPO](https://arxiv.org/abs/2402.03300)论文中的记法，有PPO的优化目标
$$\mathcal{J}_\text{PPO}(\theta)=\mathbb{E}_{q\sim P(Q)}\mathbb{E}_{o\sim\pi_{\theta_\text{old}}(O\vert q)}\dfrac{1}{\vert o\vert}\sum\limits_{i=1}^{\vert o\vert}\min\left\{\dfrac{\pi(o_t\vert q,o_{<t})}{\pi_{\theta_\text{old}}(o_t\vert q,o_{<t})}A_t,\text{clip}\left(\dfrac{\pi(o_t\vert q,o_{<t})}{\pi_{\theta_\text{old}}(o_t\vert q,o_{<t})},1-\epsilon,1+\epsilon\right)A_t\right\},$$其中$\text{clip}(x,l,r)\coloneqq\max\left\{\min\left\{x,r\right\},l\right\}$，$\epsilon>0$是一个超参数，**当优势大于0时，说明动作价值高于平均，最大化这个式子会增大比值，但不会超过$1+\epsilon$；当优势小于0时，说明动作价值低于平均，则最大化u这个式子会缩小比值，但不会低于$1-\epsilon$。**

在稠密奖励的环境中，PPO的实现如下所示（引用[动手学强化学习 - PPO算法](https://hrl.boyuai.com/chapter/2/ppo%E7%AE%97%E6%B3%95/)的实现）
```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# Actor网络，用于近似策略分布
class Actor(nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim):
        super().__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.act = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, action_dim)
    
    def forward(self, state):
        X = self.act(self.fc1(state))
        return torch.softmax(self.fc2(X), dim=-1)
    
# Critic网络，用于近似价值函数
class VCritic(nn.Module):
    def __init__(self, state_dim, hidden_dim):
        super().__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.act = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, 1)

    def forward(self, state):
        X = self.act(self.fc1(state))
        return self.fc2(X)
    

    
class PPO:
    def __init__(self, state_dim, hidden_dim, action_dim, 
                 critic_lr, actor_lr, epochs, 
                 lmbda, gamma, eps):
        self.actor = Actor(state_dim, hidden_dim, action_dim)
        self.critic = VCritic(state_dim, hidden_dim)
        self.actor_opt = torch.optim.Adam(self.actor.parameters(), lr=actor_lr)
        self.critic_opt = torch.optim.Adam(self.critic.parameters(), lr=critic_lr)

        self.epochs = epochs
        self.lmbda = lmbda
        self.gamma = gamma
        self.eps = eps
    
    def take_action(self, state):
        probs = self.actor(state)
        action_dist = torch.distributions.Categorical(probs)
        action = action_dist.sample()
        return action.item()
    
    def update(self, transition_dict):
        # (L, state_dim)
        states = torch.tensor(transition_dict['state'], dtype=torch.float)
        # (L, 1)
        actions = torch.tensor(transition_dict['actions'], dtype=torch.float)
        # (L, 1)
        rewards = torch.tensor(transition_dict['rewards'], dtype=torch.float)
        # (L, state_dim)
        next_states = torch.tensor(transition_dict['next_state'], dtype=torch.float)
        # (L, 1)
        dones = torch.tensor(transition_dict['done'], dtype=torch.float)
        # (L, 1)
        td_target = rewards + self.critic(next_states) * (1-dones)
        # (L, 1)
        td_delta = td_target - self.critic(states)
        # (L, 1)
        advs = compute_advantages(td_delta, self.lmbda, self.gamma)
        # (L, action_dim)
        old_log_probs = torch.log(self.actor(states)).gather(1, actions).detach()

        for _ in range(self.epochs):
            # (L, 1)
            log_probs = torch.log(self.actor(states)).gather(1, actions)
            # (L, 1)
            ratio = torch.exp(log_probs - old_log_probs)
            # (L, 1)
            surr1 = ratio * advs
            # (L, 1)
            surr2 = torch.clamp(ratio, 1-self.eps, 1+self.eps) * advs
            # (L, 1)
            actor_loss = torch.mean(-torch.min(surr1, surr2))
            critic_loss = torch.mean(F.mse_loss(self.critic(states), td_target.detach()))

            self.actor_opt.zero_grad()
            self.critic_opt.zero_grad()
            actor_loss.backward()
            critic_loss.backward()
            self.actor_opt.step()
            self.critic_opt.step()


def compute_advantages(td_delta: torch.Tensor, lmbda, gamma):  # (L, 1)
    td_delta = td_delta.squeeze(1).detach().numpy()
    advantages = []
    advantage = 0
    for delta in td_delta[::-1]:
        advantage = advantage * gamma * lmbda + delta
        advantages.append(advantage)
    advantages.reverse()
    return torch.tensor(advantages, dtype=torch.float)
```
## GRPO
[Hands-On-Large-Language-Models-CN - Agentic RAG](https://github.com/bbruceyuan/Hands-On-Large-Language-Models-CN/blob/master/chapter08/agentic-rag/rl-based.py)

[Transformer Reinforcement Learning (TRL)](https://huggingface.co/docs/trl/index)

## 未完待续
后续会整理DPO、GRPO、Tree-GRPO、GTPO、DAPO、$\lambda$-GRPO、GSPO、GDPO的原理和代码实现（如果有开源实现）。