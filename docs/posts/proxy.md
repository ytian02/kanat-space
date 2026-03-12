---
title: "Proxy"
slug: "Proxy"
# 副标题
subtitle: ""
# 文章描述，是搜索引擎呈现在搜索结果链接下方的网页简介，建议设置
description: ""
date: 2026-01-19T15:21:54+08:00
lastmod: 2026-01-19T15:21:54+08:00
# 文章过期提醒
outdatedInfoWarning: true
draft: false

# 文章的标签
tags:
- Network

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

🎯 目标读者: 需要在 Linux/Windows 上快速配置代理（含 Git 代理）的读者
⏱️ 阅读时间: 约 6 分钟
📚 知识要点: Clash for Linux 安装与启动、临时环境变量代理、Git Bash 全局代理设置与取消

## Clash for Linux
### 下载和安装
```sh
wget https://github.com/doreamon-design/clash/releases/download/v2.0.24/clash_2.0.24_linux_amd64.tar.gz  # 下载clash
tar zxvf clash_2.0.24_linux_amd64.tar.gz  # 解压
chmod +x clash
sudo mv clash /usr/local/bin/clash  # 移动
clash -v  # clash版本
sudo mkdir /etc/clash  # 创建目录
cd /etc/clash
sudo wget -O config.yaml https://  # 导入订阅
sudo mv /home/ubuntu/Country.mmdb /etc/clash/  #  GeoIP功能
```
### 启动
```sh
sudo clash -d /etc/clash  # 启动
```
启动后可使用 http://clash.razord.top/ 调整节点
### 临时代理
临时代理仅在临时窗口生效
```sh
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
curl ipinfo.io  # 测试代理

env | grep -i proxy  # 查看代理设置
unset http_proxy  # 删除代理设置
unset https_proxy  # 删除代理设置

sudo lsof -i :9090
sudo kill -9 pid  # 删除存在的进程
```

## Git Bash for windows
```sh
# 取消旧代理
git config --global --unset http.proxy
git config --global --unset https.proxy

# 设置代理
# 请将 7890 替换为您实际的代理端口
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```