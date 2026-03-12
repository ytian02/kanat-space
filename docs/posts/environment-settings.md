---
title: "Environment Settings"
slug: "Environment Settings"
# 副标题
subtitle: ""
# 文章描述，是搜索引擎呈现在搜索结果链接下方的网页简介，建议设置
description: ""
date: 2026-01-19T15:09:15+08:00
lastmod: 2026-01-19T15:09:15+08:00
# 文章过期提醒
outdatedInfoWarning: true
draft: false

# 文章的标签
tags:
- python

# 文章所属的类别
categories:
- Others

# 文章所属的合集
collections:
- Quick Start

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