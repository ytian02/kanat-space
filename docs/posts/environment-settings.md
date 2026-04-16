---
title: "Environment Settings"
description: ""
date: 2026-01-19T15:09:15+08:00
draft: false
tags:
  - python
categories:
  - Others
collections:
  - Quick Start
math: true
---


## 本文概览

- 🎯 **目标读者**：需要快速在本地/服务器搭好实验环境的读者
- ⏱️ **阅读时间**：约 5 分钟
- 📚 **知识要点**：Conda 环境创建、PyTorch CUDA 版本选择、常用依赖、Jupyter kernel 注册


## Hands-on-LLMs
```sh
conda create -n rl4llm python=3.10
conda activate rl4llm
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
pip install transformers
pip install pandas matplotlib scikit-learn tqdm ipykernel 
python -m ipykernel install --user --name rl4llm --display-name "rl4llm"
```

## DRL4Long-termEngagement
```sh
conda create -n DRL4LE python=3.9.13
conda activate DRL4LE
pip install torch==2.3.0 --index-url https://download.pytorch.org/whl/cu121
pip install pandas matplotlib scikit-learn tqdm ipykernel torchtest wordcloud svglib reportlab
python -m ipykernel install --user --name DRL4LE --display-name "DRL4LE"
pip install numpy==1.24.3
```