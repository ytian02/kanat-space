---
title: "Basic Knowledge of LLM"
slug: "Basic-Knowledge-of-LLM"
# 副标题
subtitle: ""
# 文章描述，是搜索引擎呈现在搜索结果链接下方的网页简介，建议设置
description: ""
date: 2026-03-14T19:00:00+08:00
lastmod: 2026-03-14T19:00:00+08:00
# 文章过期提醒
outdatedInfoWarning: true
draft: false

# 文章的标签
tags:
- LLM

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

- 🎯 **目标读者**：希望了解LLM基础知识以及训练和推理的参数设置细节的读者。
- ⏱️ **阅读时间**：20-30分钟。
- 📚 **知识要点**：SFT 的核心概念与损失函数（Cross-Entropy、Z-loss）及其适用场景；全参数微调（FFT）常见参数的作用与调参逻辑（模型、方法、数据、训练与分布式设置）；vLLM 离线推理脚本 `vllm_infer.py` 的关键参数含义（采样、并行、多模态、输出评测）；训练与推理阶段的实战注意事项：显存-吞吐权衡、可复现性、评估指标解读。

## 前言
整理本文的初衷在于实际工作中用到LlamaFactory微调、VLLM推理时，发现对一些基础概念的理解不够清晰，导致在使用过程中遇到一些问题。希望通过这篇文章能够系统地梳理一下LLM微调的相关知识点，以及实际工作中遇到的坑，帮助自己和其他读者更好地理解和应用这些技术。本文部分内容来自于**百面大模型-第5章 大模型的垂类微调**。
## Supervised Fine-tuning (SFT)
- **定义**：Supervised Fine-tuning（SFT）是一种基于监督学习的微调方法，主要用于在预训练语言模型的基础上，通过有标签的数据进行进一步训练，以适应特定任务或领域的需求。
- **损失函数**：SFT通常使用交叉熵损失函数（Cross-Entropy Loss）来衡量模型预测与真实标签之间的差距：$$L(\theta) = -\sum_{i=1}^{N} y_i \log(\hat{y}_i)$$其中，$N$是样本数量，$y_i$是真实标签，$\hat{y}_i$是模型预测的概率分布。
    - **拓展**：Z-loss ([Google PaLM](https://arxiv.org/abs/2204.02311))$$\text{z-loss}=10^{-4}\times\log^2(Z)$$其中$Z$是模型最后一层预测出的 logits 的最大值。这种做法使得模型最后一层的输出更加稳定。在进行模型输出超参数微调的时候,这种稳定性可以保证模型在调整过程中维持相对稳定的性能,避免因某些参数的调整导致模型的 logits 波动过大,从而影响模型的整体效果。
- **词表扩充**：在生成式推荐中，需要对模型的词表进行扩充，以适应由单/多模态嵌入使用各种量化方法得到的语义ID。
- **微调方法**：常见的微调方法包括全参数微调（Full Fine-tuning）和参数高效微调（Parameter-Efficient Fine-tuning, PEFT）。全参数微调需要更新模型的所有参数，而PEFT则只更新模型的一部分参数，如Adapter、LoRA等，能够显著减少训练时间和资源消耗。
- **数据格式**：
    - json文件
    ```
    {
    "instruction": "用户的正反馈历史为：${sidList}，基于用户的正反馈历史，为用户推荐可能感兴趣的sid",
    "input": "",
    "output": "${sidLabel}",
    }
    ```
- **训练参数**：以下基于 LlamaFactory 的全参数微调（FFT）配置进行参数详解：
    - **Model (模型)**
        - `model_name_or_path`: 模型文件路径或 HuggingFace Hub 上的模型 ID（如 `Qwen/Qwen3-4B`）。
        - `trust_remote_code`: 是否允许加载模型仓库中的自定义代码（对于某些新模型是必须的，默认为 `true`）。
    - **Method (方法)**
        - `stage`: 训练阶段。`sft` 代表有监督微调（Supervised Fine-Tuning）。
        - `do_train`: 开启训练模式。
        - `finetuning_type`: 微调类型。`full` 为全参数微调，`lora` 为 LoRA 微调。
        - `deepspeed`: DeepSpeed 配置文件路径（如 `ds_z3_config.json`）。ZeRO-3 (z3) 对显存优化最大，但也最慢。
            - **ZeRO-1** (z1)：优化优化器状态，适合显存较小的环境。
            - **ZeRO-2** (z2)：优化优化器状态和梯度，适合中等显存环境。
            - **ZeRO-3** (z3)：优化优化器状态、梯度和模型参数，适合显存较大的环境，但训练速度较慢。
    - **Dataset (数据集)**
        - `dataset`: 使用的数据集标识（如 `identity,alpaca_en_demo`）。
        - `template`: Prompt 模板（如 `qwen3_nothink`），决定了输入数据如何拼接成 prompt。
        - `cutoff_len`: 截断长度（如 `2048`），单条数据的最大 Token 数。
            - cutoff_len 的设置需要根据模型的最大输入长度来调整，过长可能导致显存不足，过短可能丢失重要信息，可以先在数据集上统计样本token长度的分布。
        - `max_samples`: 仅使用部分样本进行调试。
        - `preprocessing_num_workers` / `dataloader_num_workers`: 数据预处理和加载的线程数。
    - **Output (输出)**
        - `output_dir`: 训练结果保存目录。
        - `logging_steps`: 每多少步打印一次日志。
        - `save_steps`: 每多少步保存一次 Checkpoint，需要根据样本数量/有效 Batch Size 来设置。
        - `plot_loss`: 是否绘制 Loss 曲线。
        - `save_only_model`: finish后是否只保留模型权重文件（剔除优化器状态等）。
    - **Train (训练超参)**
        - `per_device_train_batch_size`: 每张显卡的 Batch Size。
        - `gradient_accumulation_steps`: 梯度累积步数。有效 Batch Size = `per_device_train_batch_size` * `gradient_accumulation_steps` * GPU数量。
        - `learning_rate`: 初始学习率（如 `1.0e-5`）。
        - `num_train_epochs`: 训练总轮数 (Epochs)。
        - `lr_scheduler_type`: 学习率调度策略（如 `cosine`）。
        - `warmup_ratio`: 学习率预热比例（如 `0.1`），前 10% 的步数学习率从 0 线性增加。
        - `bf16`: 是否开启 BF16 混合精度（需要 Ampere 架构如 3090/A100 支持，相比 FP16 更稳定）。
            - BF16（Brain Floating Point 16）是一种16位浮点数格式，具有与32位浮点数相同的指数范围，但只有8位的尾数。这使得BF16在保持较大动态范围的同时，能够提供更高的计算效率和更低的内存占用，特别适用于深度学习训练中的大规模模型。
            - FP16（Half Precision Floating Point）也是一种16位浮点数格式，但它的指数范围较小，只有5位的尾数。这可能导致在训练过程中出现数值不稳定的问题，尤其是在处理大规模模型时。因此，BF16通常被认为是更适合深度学习训练的16位浮点数格式。
        - `ddp_timeout`: 分布式训练通信超时时间。
    - **多机多卡训练**
        - `tokenized_path`: 预处理后数据的保存路径，可以先在单卡上完成数据预处理并保存，后续多卡训练时直接加载，避免重复预处理。
        - `packing`: 是否启用 Packing 技术，将多条样本拼接成一条输入以提高显存利用率和训练效率。
- **其他**：
    - **基座模型和聊天模型的区别**：基座模型（Base Model）是指预训练的语言模型，通常没有经过特定任务的微调；而聊天模型（Chat Model）则是在基座模型的基础上，通过SFT等方法进行微调，使其更适合于对话生成等特定任务。基座模型更倾向于执行针对输入的续写任务,而不是专门进行对话任务。

## Inference
- **定义**：Inference是指在模型训练完成后，使用训练好的模型对新的输入数据进行预测或生成的过程。
- **推理引擎**：VLLM是一个高性能的推理引擎，专为大规模语言模型设计，能够显著提升推理效率和吞吐量。
- **数据格式**
    - 输出格式
    ```
    {
        "prompt": "Human: 用户的正反馈历史为：${sidList}，基于用户的正反馈历史，为用户推荐可能感兴趣的sid\nAssistant:", 
        "predict": "${sidPredList}", 
        "label": "${sidLabel}\n"
    }
    ```
- **推理参数**：
    - 以下基于  LlamaFactory 的 `vllm_infer.py` 进行参数详解：
    - **Model & Adapter（模型与适配器）**
        - `model_name_or_path`: 基座模型路径或 HuggingFace 模型 ID。
        - `adapter_name_or_path`: LoRA 适配器路径。为 `None` 时不加载 LoRA；有值时会启用 `enable_lora` 并构造 `LoRARequest`。
    - **Dataset & Prompt（数据与提示模板）**
        - `dataset`: 推理使用的数据集名称（默认 `alpaca_en_demo`）。
        - `dataset_dir`: 数据集目录（默认 `data`）。
        - `template`: 对话/指令模板名称（如 `default`、`qwen3_vl` 等），决定 prompt 拼接格式。
        - `cutoff_len`: 输入截断长度（prompt 最大 token 数）。
        - `max_samples`: 仅取前 N 条样本做快速验证；`None` 表示使用全部样本。
        - `default_system`: 系统提示词（system prompt），用于统一模型行为。
        - `enable_thinking`: 是否启用“思考”相关模板行为（对支持该能力的模板有效）。
    - **vLLM Engine（引擎配置）**
        - `vllm_config`: 额外 vLLM 配置，JSON 字符串形式（如 `{\"gpu_memory_utilization\":0.9}`），会覆盖/补充默认 `engine_args`。
        - `pipeline_parallel_size`: Pipeline Parallel 的并行段数；必须小于等于 GPU 数量。
        - `tensor_parallel_size`: 代码中自动计算为 `GPU数 // pipeline_parallel_size`，用于张量并行。
        - `max_model_len`: 代码中设为 `cutoff_len + max_new_tokens`，确保上下文 + 新生成长度都在模型上限内。
        - `dtype`: 从 `infer_dtype` 自动读取（如 `bf16/fp16/fp32`），影响速度与显存。
        - `trust_remote_code`: 允许加载模型仓库自定义代码（脚本中固定为 `True`）。
    - **Sampling（生成采样参数）**
        - `temperature`: 采样温度，越大越随机，越小越确定。
        - `top_p`: Nucleus Sampling，保留累计概率达到 `p` 的候选token。
        - `top_k`: 每步只在概率最高的 `k` 个 token 中采样。
        - `max_new_tokens`: 单条样本最多生成 token 数。
        - `repetition_penalty`: 重复惩罚系数，`>1` 时抑制重复。
        - `skip_special_tokens`: 解码时是否跳过特殊 token（如 `<eos>`）。
        - `seed`: 随机种子，固定后可提高结果可复现性。
        - `stop_token_ids`: 由模板自动提供的停止 token（代码里通过 `template_obj.get_stop_token_ids(tokenizer)` 获取）。
    - **Multimodal（多模态参数）**
        - `image_max_pixels` / `image_min_pixels`: 图像分辨率约束，防止输入图像过大导致显存和吞吐问题。
        - `video_fps`: 视频抽帧帧率（每秒采样帧数）。
        - `video_maxlen`: 单条视频最多保留帧数。
        - 说明：当模板是 `qwen3_vl` 或 `glm4v` 时，脚本会额外传入视频元信息（如总帧数、采样索引）。
    - **Batch & Throughput（批处理与吞吐）**
        - `batch_size`: 推理批大小。脚本按批循环调用 `llm.generate(...)`，避免一次打开过多文件/样本导致资源问题。
        - 调参建议：增大 `batch_size` 可提升吞吐，但会增加显存占用；需要与 `max_new_tokens`、多模态输入大小一起权衡。
    - **Output & Metrics（输出与评估）**
        - `save_name`: 预测结果保存文件（jsonl），每行包含 `prompt/predict/label`。
        - `matrix_save_name`: 若不为 `None`，会额外计算并保存指标（如 BLEU、ROUGE、runtime、samples_per_second）。
        - 说明：`matrix_save_name` 依赖 `eval_bleu_rouge.compute_metrics`，更适合离线评测场景。
## Online Serving
- **定义**：Online Serving 是指将训练好的模型部署到生产环境中，提供实时的预测或生成服务。
- **压测**：在部署前进行压力测试（Stress Testing）以评估模型在高负载情况下的性能和稳定性。
    - **性能指标**：常见的性能指标包括响应时间（Latency）、吞吐量（Throughput）和资源利用率（Resource Utilization）。

## 大模型补充：PPO、RMSNorm 与束搜索

### 大模型为什么常使用 PPO，而不是 DDPG / TD3 这类确定性策略方法
1. **动作空间匹配**：LLM 的 token 选择是离散动作空间，PPO 更自然地适配离散策略优化流程。
2. **策略随机性需求**：语言生成需要保留一定随机性来维持多样性，确定性策略不占优势。
3. **训练稳定性**：PPO 的 clipping 机制可以约束策略更新步长，降低策略崩塌（Policy Collapse）风险。
4. **资源开销与可扩展性**：Off-policy 方法依赖经验回放，在 LLM 场景中 transition（长上下文 + 高维状态）存储成本极高，工程上更重。

### RMSNorm
LayerNorm 同时使用均值与方差归一化，而 RMSNorm 只使用均方根，计算更轻量：
$$
\text{RMS}(x)=\sqrt{\frac{1}{d}\sum_{i=1}^{d}x_i^2}
\quad\rightarrow\quad
\hat{x}=\frac{x}{\text{RMS}(x)+\epsilon}
\quad\rightarrow\quad
y=\gamma\hat{x}
$$
其中 $\gamma$ 是可学习缩放参数。

### 束搜索（Beam Search）
- 束搜索在每一步保留 top-$k$ 条候选路径（beam），在质量与搜索开销之间做折中。
- 相比贪心解码，束搜索通常能提高序列整体质量；相比全搜索，计算量可控。
- 参考资料：[束搜索（Beam Search）- CSDN](https://blog.csdn.net/u013172930/article/details/145500769)
