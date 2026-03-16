---
title: "常用的Linux指令"
slug: "intv-v-common-linux-commands"
subtitle: ""
description: "面试和实战中的常见 Linux 命令。"
date: 2026-03-14T22:43:00+08:00
lastmod: 2026-03-15T10:00:00+08:00
outdatedInfoWarning: true
draft: false

tags:
- 面试
- Linux

categories:
- 面试

collections:
- Interview

math: false
collectionList: true
collectionNavigation: true

hiddenFromHomePage: false
hiddenFromSearch: false

featuredImage: ""
featuredImagePreview: ""
---

## AI 含量说明

本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。

## 本文概览

- 🎯 **目标读者**：希望在工作中高频使用 Linux 命令处理数据和排查问题的读者
- ⏱️ **阅读时间**：约 8 分钟
- 📚 **知识要点**：JSON/JSONL 查询、命令行改脚本、`breakpoint()` 调试命令

# Interview

## 常用的Linux指令

下面以实际工作场景组织命令，默认你在 Linux shell（`bash`/`zsh`）中执行。

### 0. 先说两个原则

- 优先使用 `jq` 处理 JSON/JSONL，少写一次性 Python 脚本。
- 对大文件先看规模（行数/大小）再查询，避免直接 `cat` 卡终端。

可先安装常用工具：

```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y jq ripgrep

# CentOS/RHEL
sudo yum install -y jq ripgrep
```

### 1. 文件规模与基础探查

```bash
# 文件大小（人类可读）
ls -lh data.json data.jsonl

# 行数（JSONL 常用，等价于数据条数）
wc -l data.jsonl

# 只看前几行/后几行
head -n 5 data.jsonl
tail -n 5 data.jsonl

# 实时看日志/数据追加
tail -f data.jsonl
```

### 2. JSON（list of dict）常见操作

假设 `data.json` 内容是一个数组：`[{...}, {...}]`。

```bash
# 格式化查看
jq '.' data.json

# 数据量（数组长度）
jq 'length' data.json

# 看第 1 条记录
jq '.[0]' data.json

# 查看某个 key 在前几条里的值
jq '.[0:5] | map(.user_id)' data.json

# 列出所有顶层 key（适合初步看字典结构）
jq '.[0] | keys' data.json
```

筛选指定 key 等于某个 value：

```bash
# 找 status == "ok" 的记录
jq '[.[] | select(.status == "ok")]' data.json

# 只输出 id 和 score 字段
jq '[.[] | select(.status == "ok") | {id, score}]' data.json

# 统计匹配数量
jq '[.[] | select(.status == "ok")] | length' data.json
```

### 3. JSONL（dict lines）常见操作

假设 `data.jsonl` 每行一个 JSON 对象。

```bash
# 总条数
wc -l data.jsonl

# 抽样看结构（前 3 行）
head -n 3 data.jsonl | jq '.'

# 看 key 集合（抽样前 1000 行，避免全量太慢）
head -n 1000 data.jsonl | jq -r 'keys[]' | sort -u
```

筛选 key/value：

```bash
# 过滤出 status == "ok" 的行（仍是 JSON）
jq -c 'select(.status == "ok")' data.jsonl

# 过滤并只取部分字段
jq -c 'select(.status == "ok") | {id, status, ts}' data.jsonl

# 统计匹配条数
jq -c 'select(.status == "ok")' data.jsonl | wc -l
```

### 4. 高亮查询结果（排查很实用）

```bash
# 用 grep 高亮关键字（--color=always 强制高亮）
grep --color=always -n '"status":"ok"' data.jsonl | head

# 同时查多个关键词并高亮
grep --color=always -nE '"status":"ok"|"error_code":500' data.jsonl | head -n 20

# 用 rg（ripgrep）更快
rg --color=always -n '"status":"ok"' data.jsonl | head
```

如果想分页查看并保留颜色：

```bash
rg --color=always -n '"status":"ok"' data.jsonl | less -R
```

### 5. 一行命令快速改脚本

#### 5.1 定位与替换

```bash
# 查找项目中包含某字符串的文件
rg -n 'old_func_name' .

# 批量替换（先预览，再执行）
rg -l 'old_func_name' .
rg -l 'old_func_name' . | xargs sed -i 's/old_func_name/new_func_name/g'
```

注意：`sed -i` 会直接改文件，建议先 `git diff` 检查。

#### 5.2 命令行编辑器

```bash
# 用 vim 打开
vim train.py

# 用 nano 打开（更易上手）
nano train.py
```

#### 5.3 查看改动

```bash
git status
git diff
```

### 6. Python `breakpoint()` 调试常用命令

在代码里打断点：

```python
def train_step(batch):
    loss = model(batch)
    breakpoint()
    return loss
```

运行到 `breakpoint()` 后，会进入 `pdb`，常用命令如下：

- `n`：下一行（不进入函数内部）
- `s`：进入当前行调用的函数
- `c`：继续运行到下一个断点
- `l`：查看当前代码片段
- `p var`：打印变量，如 `p loss`
- `pp var`：更友好的打印（pretty print）
- `where` 或 `bt`：查看调用栈
- `u` / `d`：在调用栈中上移/下移
- `q`：退出调试

补充几个高频技巧：

```bash
# 直接用 pdb 运行脚本
python -m pdb train.py

# 查看异常后自动进入调试（脚本内）
# import pdb; pdb.set_trace() 也可用，但更推荐 breakpoint()
```

### 7. 其他高频实战命令

```bash
# 看 GPU 使用情况
watch -n 0.5 nvidia-smi

# 后台运行脚本并记录日志
nohup python train.py > train.log 2>&1 &

# 查看进程
ps -ef | grep train.py

# 杀进程
kill -9 <pid>

# 实时看日志并高亮 error
tail -f train.log | grep --color=always -i 'error\|warn'
```

### 8. 一套常用组合拳（建议记住）

当你拿到一个陌生 JSONL 文件时，可以按这个顺序：

```bash
ls -lh data.jsonl
wc -l data.jsonl
head -n 3 data.jsonl | jq '.'
head -n 1000 data.jsonl | jq -r 'keys[]' | sort -u
jq -c 'select(.status == "ok")' data.jsonl | wc -l
rg --color=always -n '"status":"ok"' data.jsonl | head
```

这 6 步通常就能完成「规模评估 -> 结构摸底 -> 条件过滤 -> 结果抽查」。