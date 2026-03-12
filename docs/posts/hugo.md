---
title: "Hugo"
slug: "Hugo"
# 副标题
subtitle: ""
# 文章描述，是搜索引擎呈现在搜索结果链接下方的网页简介，建议设置
description: ""
date: 2026-01-19T15:31:27+08:00
lastmod: 2026-01-19T15:31:27+08:00
# 文章过期提醒
outdatedInfoWarning: true
draft: false

# 文章的标签
# 文章的标签
tags:
- Website

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

## 本文概览

- 🎯 **目标读者**：想在 Windows 上用 Hugo + GitHub Pages 搭建博客的读者
- ⏱️ **阅读时间**：约 8 分钟
- 📚 **知识要点**：Hugo 建站流程、主题安装、常用命令、发布到 GitHub Pages、自动化部署

## Hugo for Windows
原教程[Windows下使用hugo和Github Pages配置博客](https://www.haoyep.com/posts/windows-hugo-blog-github/)，写得非常详细，这里只是粗略地总结了整体的步骤和常用命令。

### 安装和配置
假设在D:/personal_websites存储个人网站相关内容
```sh
# Git Bash Here，运行下面命令创建“blog”
hugo new site blog
# 安装Fixlt主题
cd blog
git init
git submodule add https://github.com/hugo-fixit/FixIt.git themes/FixIt
# 基础配置
# 修改hugo.toml文件
# 覆盖archetypes/default.md 以及 archetypes/posts.md文件
# 创建文章测试实例
hugo new posts/test.md
# 本地调试
hugo serve -D --disableFastRender
# 创建blog仓库
git branch -m master main  # 重命名分支，可能会用到
git add . 
git commit -m "init blog files"
git remote add origin https://github.com/ytian02/blog.git
git pull origin main --allow-unrelated-histories  # 拉取远程更改并合并，可能会用到
git push -u origin main
# 创建 Github Pages 公开仓库
# 上传页面
hugo
cd public
git init
git remote add origin https://github.com/ytian02/ytian02.github.io.git # 将本地目录链接到远程服务器的代码仓库
git add .
git commit -m "[介绍，随便写点什么，比如日期]"
git push -u origin master
# Github Action 自动发布
cd ../
mkdir .github
mkdir .github/workflows
touch .github/workflows/deploy.yml
git add .
git commit -m "add action config"
git push
```

### 创建新blog并上传
```sh
# 在站点目录下，打开Git Bash
hugo new posts/文章名.md  # 站点目录下，新建文章
hugo serve -D --disableFastRender  # 使用VScode编辑文章内容或修改，包括修改主题之类的。在本地进行调试
hugo  # 修改完成，确定要上传到 GitHub 上后，站点目录下执行
# 进行编译，没错误的话修改的内容就顺利同步到public下了，然后执行提交命令
git add .
git commit -m "随便写点提交信息"
git push
```

### 常用命令
```sh
# 重命名分支
git branch -m master main

# 或者 
git push -u origin master

# 合并远程文件（推荐，更安全）
git pull origin main --allow-unrelated-histories

# 删除远程分支
git push origin --delete master
```
