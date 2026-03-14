# 简历
## 1. 自我介绍
面试官你好！我是田熠，现就读于西安交通大学管理学院管理科学与工程专业，现在是硕士二年级。本科毕业于西安交通大学数学与应用数学专业，并修读了大数据管理与应用的双学位。

我的研究方向主要集中在**用户行为**和**强化学习**。

在科研方面，我曾研究如何使用强化学习优化短视频推荐策略以优化用户长期参与，并结合注意力机制输出关于用户留存的可解释性见解。我还做过有关图像解耦相关的工作，利用标签数据的先验信息增强基于VAE的图像解耦方法中隐层表示的可解释性。

在项目方面，我曾使用强化学习解决NPS修复问题，结合用户行为数据输出推荐修复措施，并结合注意力机制分析用户潜在的不满原因。此外，还使用多智能体强化学习方法优化气井开关策略。

我熟悉pytorch框架，掌握经典RL和offline RL方法，以及推荐系统的传统方法，也对RL在大模型和生成式推荐中的应用有所了解。

以上是我的自我介绍。
## 2. 考虑用户长期参与的短视频推荐方法
### 2.1 问题场景
在短视频推荐中，短期参与度指标（点击/观看时长）不能反映用户长期参与（返回时间），比如标题党的内容可能会损害用户对于平台的信任，低质量内容可能会让用户感到懊悔和没有自我提升。而长期参与（比如用户的回访行为-返回时间）更能衡量用户的持续使用意愿。基于此，我们想研究一种直接优化用户长期参与的短视频推荐方法。
### 2.2 问题挑战
1. 策略空间维数灾难：考虑到一次会话中的用户观看体验是连贯的，推荐系统应该优化的是一个推荐序列，但是每个item的候选池可能非常大，而策略空间会随着推荐序列的尺寸指数增长，从而面临策略空间的维数灾难问题；
2. 用户过去的内容消费历史存在复杂的跨期影响：短视频这种内容消费场景中，用户可以重复访问同一个/同一类item，在当前请求给用户推荐视频时需要考虑到用户过去的内容消费历史，而用户过去的行为对于当前状态的影响存在复杂的跨期影响，且随时间动态演变（可以举健身爱好者的例子）；
3. 延迟的长期参与信号：在短视频场景中，通常以用户的回访行为（返回时间）衡量用户的长期参与，但是只有在下一次会话开始时，才能知道上一会话的返回时间，传统的机器学习方法不能有效处理这种延迟信号
### 2.3 研究方法
1. 将用户与平台交互的过程建模为MDP，学习一个根据用户消费行为调整的动态推荐策略；
2. 使用GRU将高维的交互特征转化为低维嵌入向量，并使用一个时间衰减注意力机制查询相关的内容消费历史，并削弱距离很远的消费行为的影响；
3. 使用强化学习算法训练策略，此外，考虑到这是一种特殊的稀疏奖励问题，在会话中并没有来自奖励的监督信号，使用了用户的即时反馈行为作为监督信号，有效塑造状态表征
### 2.4 实验
1. 数据集和实验环境
   KuaiRand数据集和KuaiSim模拟器
	- 细节：
		- KuaiSim模拟器包括三个模块：用户反馈模块（提供用户的即时反馈）、用户离开模块（预测是否准备结束会话）、用户留存模块（预测用户的返回时间）
		- 用户反馈模块：会根据item_enc和user_state先计算候选item中用户多行为的评分(B, nums, n_feedback)，然后输出的动作向量(B, n_feedback)会跟sigmoid(多行为评分)计算内积得到item的评分(B, nums)，然后选topk个item，根据这topk item的sigmoid(多行为评分)通过Bernoulli分布抽样得到用户反馈；
		- 用户离开模块：通过用户即时反馈计算即时奖励，用户耐心减去即时奖励，如果低于一定水平，用户离开
		- 用户留存模块：通过用户状态给出用户每一天的返回分数（设置为10天），通过softmax得到概率值，然后从类别分布中抽样得到用户返回天数
2. 对比方法
	- CEM：采用随机高斯策略，每次从经验回放池中抽样经验，然后选择topk奖励的action更新随机高斯分布的参数
	- SASRec：使用sigmoid(actor)和即时反馈的BCEloss训练模型
	- TD3：ActionTransformer+TD3
	- RLUR：2023年WWW
	- AURO：2025年WWW
	- 细节：
		- ActionTransformer：行为序列同时考虑item id、item feature、user id、user feature、feedback type
		  具体来说，
		- RLUR提到了状态的新颖性，鼓励探索；
		- AURO提到了状态的变化，用于提醒模型；
3. 实验结果
   在平均返回时间、次日留存率、留存奖励三个指标上表现良好
   且通过计算不同留存组的影视综艺类别视频的平均注意力权重，得到前20个最相关的视频，发现高质量视频更能促进长期留存

细节：
- **last-n**：max_hist_seq_len 50
- 更新过程：
	- **feedback loss**：buffer中存储的feedback是历史上采取s_t,a_t之后的y_t
	- **buffer**：next_policy_output是现算的，但是policy_output是存储的真实action
	- **critic loss**：TD3算法policy_output存的是$(s_t,a_t)$，但是next_policy_output使用$x_{t+1}$算出来的，所以其实$s_{t+1}$不是历史经验，因此TD target的输入本应该都是带梯度的，但是因为是target网络输出的next_policy_output和target_critic_output，所以其实没有梯度，所以TD更新时只会更新critic网络
	- **actor loss**：在计算actor_loss时，policy_output由$x_t$重新计算，critic_output和policy_output都是有梯度的，但是只会更新状态表征网络和actor网络
	- 总结来说，TD算法更新critic网络，最大化Q值更新actor的状态表征和action_module
- ActionTransformer细节：先由get_item_encoding得到历史item序列的encoding，再加上pos_emb经过dropout和layer norm，然后由get_response_embedding得到历史feedback序列的encoding，并和前面的encoding拼起来，输出transformer得到output_seq，取最后一个作为hist_enc，最后再由get_user_encoding得到user_enc，经过dropout和layer norm后与hist_enc拼起来得到user state
- 精排or重排：AURO和RLUR论文中直接提到actor输出排序权重，用于加权评分函数输出的多反馈预测分数![[Pasted image 20260104181045.png#center|]]
- RLUR VS CEM：请注意，在短视频平台上，用户留存率提高0.01%和日活跃用户（DAU）提高0.1%在统计上是显著的。这意味着RLUR的表现相当显著。请注意，DAU和留存率持续增加。![[Pasted image 20260104182120.png#center|]]
- AURO![[Pasted image 20260104182606.png]]AURO在所有指标上都有了提升，特别地，在点踩率上有了显著提升，这可能是模型的状态抽象网络的作用。
## 3. 基于属性标签先验的变分自编码器重构与解耦平衡研究
### 3.1 问题场景
1. 概念：解耦表征学习旨在学习一个能够可分离的观测特征背后潜在的生成因子的模型
2. 研究背景：基于VAE的图像解耦表征研究使用VAE解耦图像背后的生成因子
### 3.2 问题挑战
现有基于VAE的方法生成图像质量差，且生成的隐层表示可解释性差（人类看不懂）
### 3.3 研究方法
1. 对于生成图像质量差的问题，假设条件生成分布符合像素级别的laplace分布，推导得到l1损失
2. 对于隐层表示可解释性差的问题，利用属性标签（40个人脸属性，都是0-1变量）构造了个体先验和群体先验
	- 个体先验：假设z->x且z->y
	- 群体先验：使用p(z) = N(0,Σ)，其中Σ是标签的协方差矩阵，存储了属性之间的相关关系
### 3.4 实验
在CelebA数据集上进行了实验，取得了生成质量和解耦质量的平衡
评价指标：重构损失、PSNR、SSIM、互信息、MISJED、RMIG、JEMMIG
## 4. NPS 推荐及修复建模
### 4.1 问题场景
在电信运营商场景中，NPS（净推荐值），NPS（净推荐值）是一个衡量客户忠诚度和满意度的标准指标
- NPS分数=(推荐者人数-批评者人数)/总人数   注：0-6为批评者，7-8为中立者，9-10为推荐者
### 4.2 问题挑战
现有方法多为基于规则针对用户做出单次修复，没有考虑到过去的交互历史，而最大化单次满意度可能不能反映用户的长期满意度（或者说治标不治本）
### 4.3 研究方法
- 概要：将用户与运营商交互的历史建模为POMDP，使用DRQN+Attention的方式优化修复策略，目标是最大化用户的长期满意度
- 概念：状态-用户潜在状态，动作-修复措施，奖励-修复后评分
- 细节：GRU得到用户历史Emb，和用户静态特征emb结合起来作为query，尺寸为(B, 1, attn_dim)，然后对用户的情境特征（当月特征）做one-hot encoding，尺寸为(B, contextual_dim, 1)，映射为key，尺寸为(B, contextual_dim, attn_dim)，复制为value，尺寸为(B, contextual_dim, 1)，使用点积注意力机制得到答案后和query拼接再接线性层得到user_state
- 训练：使用Dueling Network优化
### 4.4 实验
在真实的用户月活数据和修复数据上进行了实验
DRQN+Attention在Fixed-M PERS指标上表现良好
Fixed-M PERS简单介绍：
1. 给定H，计算episode长度为H的M值，其中pi_b, pi_e, T(s,a,s')都是根据历史记录计算的，M值表示从状态s开始episode的重要性比值
2. 然后执行拒绝采样，对于历史数据，以状态s为初始状态，计算episode的折扣回报和重要性比值，如果这个重要性比值和M的比值很高，表示这段episode和历史很像，从[0, 1]均匀分布抽样得到mu，如果mu小于等于比值接受折扣回报
简单来说，就是采样和历史策略能够产生相似episode的记录的折扣回报
![[Pasted image 20251229204123.png]]
## 5. 天然气气井开关策略优化
### 5.1 问题场景
在天然气气井场景中，需要合理开关气井以实现产能最大化
### 5.2 问题挑战
现有生产模式基于规则开关井，忽略了同一个井场不同气井之间的复杂影响
### 5.3 研究方法
1. 循环神经网络训练环境模型，学习状态转移函数和奖励函数
2. 使用多智能体算法训练开关井策略
3. 细节：
	- MDP：POMDP，单个气井只能观测到自己的状态，状态-套压/油压，动作-开/关，奖励-瞬时流量
	- 方法：IQL-单个气井训练自己的开关策略，VDN使用单个智能体的Q函数的加和近似整体的Q函数，QMIX使用超网络学习环境全局状态的信息，然后使用混合网络以每个Q函数和超网络的输出为输入，计算Q值
### 5.4 实验
在环境模拟器上可实现约20%的产量提升
## 6. 反问环节
1. 项目组的业务
2. 发论文
3. 实习生能否训练模型，训练模型能否上线
4. GPU资源（小厂）

# 概率论、数理统计、信息论
## 概率论与数理统计
### 1. 常见的概率公式

### 2. 充分统计量


## 信息论
### 1. 熵(Entropy) & 交叉熵(Cross Entropy) & KL散度(KL Divergence)
(以下内容均来自于《信息论基础》Thomas M. Cover 第二版)
- **熵:** 是随机变量不确定性的度量,记随机变量$X$的概率密度为$p(x)$,其中$x\in\mathcal{X}$,随机变量$X$的熵为$$H(X)=- \sum\limits_{x\in\mathcal{X}}p(x)\log p(x),$$其中对数的底一般取2,熵的单位用**比特**(bit)表示,例如抛硬币(均匀)这一事件的熵为1比特.由于当$x\to 0$时,$x\log x\to 0$,约定$0\log 0=0$,因为加上零概率的项不改变熵的值.
	- 此外,记以b为底的熵为$H_b(X)$,特别地,当使用对数底时,熵的单位为**奈特**(nat).
	- 注意,熵是随机变量的**泛函**,不依赖于随机变量的具体取值,仅依赖于其概率分布.
	- $H(X)\geqslant 0$
- **联合熵和条件熵:** 由熵的定义可以引出联合熵和条件熵的概念.
  联合熵$$H(X,Y)=
-\sum\limits_{x\in\mathcal{X}}\sum\limits_{y\in\mathcal{Y}}p(x,y)\log p(x,y).$$条件熵$$H(Y\vert X)=-\sum\limits_{x\in\mathcal{X}}p(x)H(Y\vert X=x)=-\sum\limits_{x\in\mathcal{X}}\sum\limits_{y\in\mathcal{Y}}p(x,y)\log p(y\vert x).$$链式法则$$H(X,Y)=H(Y)+H(Y\vert X).$$
- **KL散度:** 也叫相对熵,是两个概率分布之间距离的度量,$D_\text{KL}(p\Vert q)$度量真实分布为$p$时假设分布为$q$的无效性$$D_{KL}(p\Vert q)=-\sum\limits_{x\in\mathcal{X}} p(x)\log\dfrac{q(x)}{p(x)},$$对于上述定义,约定$0\log\dfrac{0}{0}=0,-p\log\dfrac{0}{p}=\infty$.注意$D_{KL}(p\Vert q)\geqslant 0$恒成立,当且仅当$p(x)=q(x)$时等号成立,由[Gibbs' inequality - Wikipedia](https://en.wikipedia.org/wiki/Gibbs'_inequality)保证.
- **互信息:** 是一个随机变量包含另一个随机变量的信息量的度量,也是在给定另一个随机变量知识的条件下,原随机变量不确定度的缩减量$$I(X;Y)=-\sum\limits_{x\in\mathcal{X}}\sum\limits_{y\in\mathcal{Y}}\log\dfrac{p(x)p(y)}{p(x,y)}=D_\text{KL}\left(p(x,y)\Vert p(x)p(y)\right).$$熵与互信息的关系$$I(X;Y)=H(X)-H(X\vert Y)=H(Y)-H(Y\vert X)=H(X)+H(Y)-H(X,Y)=I(Y;X).$$特别地,$I(X;X)=H(x)$.
  ![[Pasted image 20251208123304.png#center|]]
(补充)
- **信息量:** 衡量事件从不确定到达确定的难度,定义如下$$f(X=x)=-\log p(x)$$以2为底的信息量的单位称为bit(比特).
- **交叉熵:** 衡量两个概率分布的差异,真实分布为$p$,假设分布为$q$,定义为$$H(p,q)=-\sum\limits_{x\in\mathcal{X}}p(x)\log q(x),$$交叉熵被广泛应用于分类任务.


# 机器学习
## 1. 常见的损失函数
(以下内容来自Gemini3.0Pro)
### **一、 回归任务 (Regression)**
用于预测连续数值（如房价预测、坐标回归）。
#### **1. MSE (Mean Squared Error / L2 Loss)**
最常用的回归损失函数。$$L_{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$
- **特点**：对异常值（Outliers）非常敏感，因为误差被平方放大了。
- **适用**：绝大多数常规回归任务。
#### **2. MAE (Mean Absolute Error / L1 Loss)**
计算预测值与真实值绝对误差的平均值。$$L_{MAE} = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i|$$
- **特点**：对异常值具有鲁棒性（Robust），但在 $x=0$ 处不可导（通常使用次梯度）。
- **适用**：数据中噪音较多，或者希望模型具有稀疏性（L1正则化特性）时。
#### **3. Huber Loss / Smooth L1 Loss**
MSE和MAE的结合体。
- **特点**：在误差较小时表现为MSE（可导，收敛快），在误差较大时表现为MAE（对异常值不敏感）。
- **适用**：目标检测（如Faster R-CNN的边界框回归）。
### **二、 分类任务 (Classification)**
用于预测离散类别（如图像分类、情感分析）。
#### **1. NLL (Negative Log-Likelihood)**
负对数似然损失$$L_{NLL} = - \sum_{i=1}^{N} \log(p(y_i|x_i))$$
- **特点**：它通常不包含Softmax操作，直接接受概率值（或者Log概率）进行计算。
- **注意**：在PyTorch中，`NLLLoss` 期望输入是经过 `LogSoftmax` 处理后的值。
#### **2. CE (Cross-Entropy Loss)**
交叉熵损失，衡量两个概率分布之间的差异。$$L_{CE} = - \sum_{x} p(x) \log q(x)$$其中 $p(x)$ 是真实分布（One-hot），$q(x)$ 是预测分布。
- **关系**：**CrossEntropyLoss = Softmax + Log + NLLLoss**。
- **二元交叉熵 (BCE)**：用于二分类，公式为 $-(y\log(\hat{y}) + (1-y)\log(1-\hat{y}))$。
- **适用**：几乎所有的多分类和二分类任务。
#### **3. KL Divergence (Kullback-Leibler Divergence)**
相对熵，衡量预测分布 $Q$ 与真实分布 $P$ 的差异。$$D_{KL}(P || Q) = \sum P(x) \log \frac{P(x)}{Q(x)}$$
- **关系**：$CE = Entropy(P) + D_{KL}(P||Q)$。**如果 $P$ 是固定的（如One-hot），最小化CE等价于最小化KL散度**。
- **适用**：知识蒸馏（Knowledge Distillation）、变分自编码器（VAE）。
### **三、 相似度与度量学习 (Similarity & Metric Learning)**
用于学习向量表示，使得相似样本距离近，不相似样本距离远。
#### **1. Cosine Similarity Loss (Cosine Embedding Loss)**
直接优化两个向量之间的余弦相似度。$$L_{cos} = \begin{cases} 1 - \cos(x_1, x_2), & \text{if } y=1 \text{ (相似)} \\ \max(0, \cos(x_1, x_2) - \text{margin}), & \text{if } y=-1 \text{ (不相似)} \end{cases}$$
- **特点**：关注向量的方向而非模长。注意当$\vert x_1\vert=\vert x_2\vert=1$时，最大化余弦相似度相当于最小化MSE。
- **适用**：语义匹配、文本相似度。
#### **2. Triplet Loss**
输入是一个三元组：Anchor ($A$)，Positive ($P$)，Negative ($N$)。$$L = \max(d(A, P) - d(A, N) + \text{margin}, 0)$$
- **目标**：拉近 $(A, P)$，推远 $(A, N)$。
- **适用**：人脸识别（FaceNet）、细粒度图像检索。
### **四、 对比学习与自监督学习 (Contrastive Learning)**
这是你提到的NCE系列的核心领域，常用于处理大规模类别或自监督预训练。
#### **1. NCE (Noise Contrastive Estimation)**
噪音对比估计。
- **背景**：在NLP中，如果词表巨大（如10万+），计算Softmax的分母（归一化项）非常耗时。
- **核心思想**：将“从N个类别中预测正确类别”的多分类问题，转化为“区分真实样本与噪音样本”的二分类问题。
- **操作**：对于每一个真实样本，采样 $k$ 个噪音样本（来自噪声分布 $P_n$），训练一个二分类器（Logistic Regression）。
- 公式：$$J(\theta) = \dfrac{1}{K+1}\left[\log\sigma(u(x))+\sum\limits_{k=1}^K\log(1-\sigma(u(x_j)))\right]$$(其中 $u(x)$ 是未归一化的模型得分，$x$是正样本，$x_j$是采样的负样本)
  注意当K越大，NCE损失越接近极大似然估计的结果，详细的推导过程见[NCE和InfoNCE的理解与应用 - 知乎](https://zhuanlan.zhihu.com/p/684512415)
- **适用**：Word2Vec (Negative Sampling 是 NCE 的简化版)、大规模语言模型早期训练。
#### **2. InfoNCE (Information Noise Contrastive Estimation)**
NCE 的泛化版本，是目前**对比学习（Contrastive Learning）**（如 SimCLR, MoCo, CLIP）的标配损失函数。
- **核心思想**：最大化输入 $x$ 与其正样本 $x^+$ 之间的**互信息（Mutual Information）下界**，详细的推导过程见[NCE和InfoNCE的理解与应用 - 知乎](https://zhuanlan.zhihu.com/p/684512415)
- **操作**：在一个Batch中，有一个正样本对 $(q, k_+)$ 和 $K$ 个负样本对 $(q, k_-)$。它本质上是一个**带温度系数的 Softmax Cross-Entropy**。
- 公式：$$L_{InfoNCE} = - \log \frac{\exp(\text{sim}(q, k_+) / \tau)}{\sum_{i=0}^{K} \exp(\text{sim}(q, k_i) / \tau)}$$
    - $\text{sim}(\cdot)$：通常是余弦相似度。
    - $\tau$ (Temperature)：温度系数，控制模型对困难负样本的关注程度。
- **直观理解**：分子是正样本的得分，分母是（正样本+所有负样本）的得分总和。我们要让正样本在所有样本中“脱颖而出”。
- **适用**：自监督学习、多模态预训练（CLIP）。

简要版本：NCE考虑到将问题建模为类别分布时，softmax的分布计算耗时的问题，将原问题转化成二分类问题，（假设样本来自真实分布的概率为$1/(K+1)$），对于每个真实样本，采样K个负样本，利用NCE损失训练一个二分类器。而InfoNCE是从数据集中抽取一个正样本和K个负样本，然后建模为多分类问题优化负对数似然，本质上是带温度系数的Softmax。
## 2. L1和L2正则化
1. 特点
	- L1正则化倾向于产生**稀疏权重矩阵**（即很多 $w_i$ 变为 0），常用于**特征选择**（Feature Selection）
	- L2正则化倾向于让权重参数 $\mathbf{w}$ 变小且分布均匀，接近于 0 但通常**不等于 0**，防止过拟合，处理特征多重共线性（Multicollinearity）。
2. 几何解释
   考虑原损失函数的等高线和正则化的等高线，最优解一般出现在两者相切的地方
	- L1正则化：约束区域是一个菱形，导致切点井场落到坐标轴上
	- L2正则化：约束区域是一个圆形，切点不容易落到坐标轴上
3. 导数解释
	- L1正则化：L1的导数是$\text{sign}(w)$，无论$w$的大小，都会以恒定的速度推向0，直到变成0，0处使用次梯度，pytorch中规定$\text{sign}(0)=0$
	- L2正则化：L2的导数是$2w$，当权重很小时，梯度也很小
4. 概率解释
   从最大后验估计的角度来看$$\log P(w\vert\mathcal{D})\propto\log P(\mathcal{D}\vert w)+\log P(w)$$分母是归一化因子，其实和权重没有关系可以省略，代入Laplace分布（均值为0，尺度参数为b）可以得到L1正则化，高斯分布（均值为0，方差确定）可以得到L2正则化，Laplace分布在0处是一个尖峰，高斯分布在0处平滑。
## 3. L2正则化和权重衰减
在标准的SGD中，两者在数学上是等价的。但是在Adam中，是不等价的。直接修改损失函数加 L2 正则化（L2 Regularization），和直接在参数更新步骤中减去 $\lambda w$（Weight Decay），效果是不同的。现在的主流库（如 PyTorch 的 `AdamW`）提倡将 Weight Decay 与梯度更新解耦。
# 深度学习
## 1. 为什么自注意力机制不直接使用输入向量$X$作为QKV?
引入三个可学习的权重矩阵$W^Q,W^K,W^V$,可以从以下几个方面考虑:
1. **打破对称性,实现非对称关注**
   如果直接使用$X$,那么在计算缩放点积注意力机制时,注意力分数为$XX^\top$,此时第$i$个单词对第$j$个单词的分数和第$j$个单词对第$i$个单词的分数都是$x_i\cdot x_j$,这意味着:如果"苹果"觉得"好吃"很重要,那么"好吃"也必须觉得"苹果"同样重要.而引入权重矩阵$W^Q,W^K$可以实现注意力分数的非对称性.
2. **语义空间的转换与角色分离**
   在注意力机制中,需要输入向量$X$扮演三种不同的角色,以图书馆搜索为例,$X$是一本实体书,$W^Q$(投影为Query)可以理解为去图书馆填写的"索书号"或"关键词"(比如:"找一本关于历史的书");$W^K$ (投影为Key)可以理解为书脊上印的分类标签(比如:"历史类-编号001");$W^V$(投影为Value)可以理解为书里面的实际内容.
3. **多头注意力机制的基础**
   多头注意力正是引入多组不同的$W^Q_i,W^K_i,W^V_i$,不同的头可能分别学会了关注语法结构、指代关系、长距离依赖等等.
4. **调整维度的灵活性**
   虽然标准Transformer通常保持输入输出维度一致(例如$d_{model}=512$),但在计算注意力内部,我们经常会将向量投影到不同的维度$d_k=d_{model}/h$,如果没有$W$矩阵,我们就无法灵活地在低维空间进行高效的注意力计算,计算量会随着$d_{model}$的平方增长,且容易造成参数冗余. (这一点说服力不强,因为在推荐系统中输入向量可能是嵌入向量连接后再经过一个MLP得到)
## 2. SASRec和Transformer Encoder/Decoder-only Transformer的区别?
从架构本质上来说,SASRec是一个Decoder-only Transformer的结构,而不是Transformer Encoder,以下是详细对比:
1. **注意力机制**
   Transformer Encoder使用了双向注意力(Bidirectional Attention),如果使用seq2seq的方式做next item prediction任务,则会面临"未来信息泄露"的问题.而SASRec和Decoder-only Transformer都使用了因果编码(Causal Mask),注意力矩阵是一个下三角矩阵上三角部分被置为$-\infty$(softmax后变为0).
2. **交叉注意力层**
   在SASRec中,没有交叉注意力层,这是因为SASRec没有"源语言"和"目标语言"之分,只有用户的行为流.Transformer Decoder有一个交叉注意力层,用于"看"翻译任务中的源语言句子(Encoder的输出).此外,标准的Decoder-only Transformer(如 GPT 系列、Llama)中,是没有交叉注意力层的,但是在多模态模型或者一些变体中可能有特例.
注: SASRec的Shared Item Embedding指的是输入层的item embedding被用于输出层计算点积分数,在传统的方法(如FPMC)中内积可能无法处理不对称的item转换,但是SASRec学习了非线性变换,前馈网络可以轻松地通过相同的item嵌入实现不对称.
## 3. Transformer
### 3.1 模型结构
- Encoder: 
	- (输入) 结合位置编码的source token embedding
	- (Layer) 多头注意力机制(自注意力) -> 注意力的输出残差连接后接层归一化 -> 前馈网络 -> 前馈网络的输出残差连接后经过层归一化
- Decoder: 
	- (输入) 结合位置编码的target token embedding + Encoder的输出
	- (Layer) (因果)掩码多头注意力机制(自注意力) -> 注意力的输出残差连接后接层归一化 -> 多头注意力机制(Query来自Decoder的掩码多头注意力机制,Key和Value来自Encoder的输出) -> 注意力的输出残差连接后接层归一化 -> 前馈网络 -> 前馈网络的输出残差连接后经过层归一化
	- (输出) 通过线性层和softmax得到尺寸为(bs, seq_len, target_vocab_size)的输出概率
![[Pasted image 20251217193941.png#center|]]
### 3.2 为什么不用循环神经网络？
1. **并行计算:** 循环神经网络只能根据上一时刻的隐藏状态来输出当前的隐藏状态，在训练时无法并行计算，而自注意力机制可以同时处理整个序列![[Pasted image 20251217195345.png]]
2. **信息传递与长距离依赖:** 循环神经网络所有历史信息压缩进一个固定大小的隐藏状态中，随着序列变长，早期信息的信号会逐渐衰减；自注意力机制允许序列中的每一个 token 直接与序列中的其他所有 token 交互。
### 3.3 为什么使用点积注意力而不是加性注意力？
因为点积注意力更快更节省空间![[Pasted image 20251217200235.png]]
### 3.4 为什么使用缩放点积注意力而不是标准的点积注意力？
1. **简单解释:** 如果不使用缩放点积注意力机制，随着向量维度$d_k$的增加，点积的结果会越来越大，导致softmax函数进入“饱和区”（softmax的值非常接近1或0），梯度变得接近于0
2. **数学解释:** 考虑Query和Key的每个元素都是独立的随机变量，均值为0，方差为1，则点积的均值为0，方差为$\sqrt{d_k}$，所以需要除以缩放因子以降低方差
![[Pasted image 20251217200352.png]]
### 3.5 嵌入层与softmax
**(以下解释来自于Gemini3 Pro)**
1. **共享权重:** Transformer在Encoder的Embedding层，Decoder的Embedding层和Decoder的logits层共享了权重系数。这样做的好处是不需要维护三个巨大的矩阵，可以减少模型参数量和保证训练稳定性。比如，输入的“猫”的向量表示，和输出时预测“猫”所用的权重向量，逻辑上应该是同源的。共享权重强制模型在输入和输出端学习一致的语义表示。
2. **缩放权重:** 在两个Embedding层，将权重乘以$\sqrt{d_{model}}$，这是因为Embedding 层的权重初始化通常很小如 Xavier 初始化，方差约为 $1/d_{model}$），而位置编码（和嵌入向量维度相同）的数值范围在$[-1, 1]$之间，乘以$\sqrt{d_{model}}$之后，Embedding 的数值变大，与位置编码处于同一个量级，模型就能同时有效地利用语义信息和位置信息。
![[Pasted image 20251217203636.png]]

### 3.6 位置编码
1. **引入位置编码的原因:** 自注意力机制不像RNN和CNN一样，没有token的位置信息，因此需要向token序列中加入相对或绝对位置信息。
2. **定义:** 位置编码的定义如下$$\begin{aligned} \text{PE}_{(pos, 2i)} &= \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right) \\ \text{PE}_{(pos, 2i+1)} &= \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right) \end{aligned},$$注意$i\in\{1,\cdots,d_{model}\}$。
3. **好处:** **(以下解释来自于Gemini3 Pro)**
	- **相对位置:** 考虑三角公式$$\sin(\alpha+\beta)=\sin(\alpha)\cos(\beta)+\sin(\beta)\cos(\alpha),$$可以发现对于任意位置$pos$和偏移量$k$，$pos+k$的位置编码都可以由$pos$的为位置编码通过一个线性变换(旋转矩阵)得到，这让 Attention 机制很容易通过线性投影来学习到词与词之间的相对距离。
	- **可泛化性:** 正弦和余弦函数对于任意长度的序列都能计算位置编码
	- **数值稳定性:** 正弦和余弦值位于$[-1,1]$之间，这与 Word Embedding 的数值范围比较匹配，相加后不会破坏原始 Embedding 的分布，也不会像整数编码那样随着序列变长数值爆炸。
### 3.7 为什么使用Layernorm不用BatchNorm?
1. 变长序列
   batch_norm对(B,L,C)的(B,L)求均值和方差，但是填充的0值会影响到均值和方差的计算
   layer_norm对C求均值和方差，
2. batch size
   Batch Norm的效果依赖于batch size，layer norm适用于小批量数据
### 3.8 Transformer的时间复杂度
(以下内容来自Gemini3.0 Pro)
计算 Transformer 模型的时间复杂度通常是指 **单层（Per Layer）** 的计算量。
简而言之，标准 Transformer 单层的时间复杂度为：$$O(N^2 d + N d^2)$$其中：
- $N$：序列长度（Sequence Length）
- $d$：隐藏层维度（Hidden Dimension, or Embedding Size）
以下是详细的推导过程，分为 **自注意力机制 (Self-Attention)** 和 **前馈神经网络 (Feed-Forward Network)** 两部分来计算。
#### 1. 符号定义
为了清晰描述矩阵运算，我们定义以下符号：
- **$N$**: 输入序列的长度（Token 数量）。
- **$d$**: 模型的隐藏层维度（Hidden size）。
- **$h$**: 多头注意力的头数（Heads）。通常每个头的维度 $d_k = d/h$。
#### 2. 自注意力机制 (Self-Attention) 的复杂度
自注意力机制的计算包含三个主要步骤：线性投影、注意力分数计算、加权求和。
##### Step 1: 生成 Q, K, V (线性投影)
输入矩阵 $X$ 的形状为 $(N, d)$。我们需要将其乘以权重矩阵 $W^Q, W^K, W^V$（形状均为 $(d, d)$）来得到 Query、Key 和 Value。
- 计算：$X \times W$
- 矩阵运算：$(N, d) \times (d, d) \rightarrow (N, d)$
- 复杂度：$O(N \cdot d^2)$
- 由于有 Q, K, V 三个，总是 $3 \cdot O(N \cdot d^2)$，即 **$O(N d^2)$**。
##### Step 2: 计算注意力分数矩阵 (Attention Matrix)
计算 $Q$ 和 $K^T$ 的点积。
- 计算：$Q \times K^T$
- 矩阵运算：$(N, d) \times (d, N) \rightarrow (N, N)$
- **复杂度：$O(N^2 d)$**
- _注意：这一步是导致 Transformer 在长序列下计算量爆炸的主要原因。_
##### Step 3: 加权求和 (Context Mapping)
将 Softmax 后的注意力矩阵（形状 $(N, N)$）与 $V$（形状 $(N, d)$）相乘。
- 计算：$A \times V$
- 矩阵运算：$(N, N) \times (N, d) \rightarrow (N, d)$
- **复杂度：$O(N^2 d)$**
自注意力部分总复杂度：$$O(N^2 d + N d^2)$$
#### 3. 前馈神经网络 (Feed-Forward Network) 的复杂度
FFN 通常包含两个线性层，中间夹一个激活函数。标准 Transformer 中，中间层的维度通常扩展为 $4d$。
##### Step 1: 第一层线性变换 (扩维)
- 计算：$X \times W_1$
- 矩阵运算：$(N, d) \times (d, 4d) \rightarrow (N, 4d)$
- 复杂度：$O(N \cdot d \cdot 4d) = O(4 N d^2)$
##### Step 2: 第二层线性变换 (降维)
- 计算：$H \times W_2$
- 矩阵运算：$(N, 4d) \times (4d, d) \rightarrow (N, d)$
- 复杂度：$O(N \cdot 4d \cdot d) = O(4 N d^2)$
FFN 部分总复杂度：$$O(N d^2)$$(常数项通常忽略，但在具体算力估算时约为 $8 N d^2$)
#### 4. 总结与对比
将上述两部分相加，单层的总时间复杂度为：$$O(N^2 d + N d^2)$$
#### 关键结论：
1. **当序列较短时 ($N < d$)**：$O(N d^2)$ 占主导。此时 Transformer 的计算量主要由模型宽度（参数量）决定。
2. **当序列较长时 ($N > d$)**：$O(N^2 d)$ 占主导。此时 **$N^2$** 成为瓶颈。这就是为什么处理超长文本（如 100k tokens）非常昂贵的原因，也是 FlashAttention 或 Linear Attention 等优化技术试图解决的核心问题。
## 4. Transformer -> Bert -> GPT
Transformer是Encoder-Decoder架构，主要应对翻译任务
Bert是Encoder-only架构，重在语言理解
GPT是Decoder-only架构，重在语言生成
## 5. Scaling law
(以下内容来自Gemini3.0Pro)
**LLM Scaling Laws（大语言模型缩放定律）** 指的是在深度学习领域（尤其是大语言模型中），模型性能与计算资源、数据量和参数量之间存在的**可预测的数学关系**。
简单来说，Scaling Law 告诉我们：只要按照特定的比例增加算力、数据和模型大小，模型的智能水平（通常以 Loss 损失函数下降来衡量）就会呈现出规律性的提升。这被认为是 AI 领域的“摩尔定律”。
以下是关于 Scaling Law 的详细演变与核心内容：
### 1. 核心三要素
Scaling Law 主要研究以下三个变量与模型性能（Loss）之间的**幂律（Power Law）**关系：
- **N (Number of Parameters)：** 模型参数量（模型“脑容量”有多大）。
- **D (Dataset Size)：** 训练数据量（模型“读”了多少书）。
- **C (Compute)：** 训练所用的计算量（训练花费了多少算力，通常用 FLOPs 衡量）。
数学形式通常表现为：$$L(N, D) \approx \frac{A}{N^\alpha} + \frac{B}{D^\beta} + L_{min}$$（Loss 随着 N 和 D 的增加而呈指数级下降，存在边际效应但趋势稳定。）
### 2. 演变阶段一：Kaplan 定律 (OpenAI, 2020)
论文： Scaling Laws for Neural Language Models
核心观点： “模型越大越好”
OpenAI 的研究人员（Kaplan 等人）最早系统化地提出了这一概念。他们得出的结论是：
- **参数量 (N) 是最重要的因素。**
- 为了获得最佳性能，应该优先把算力分配给**增加模型参数**，而不是增加训练数据。
- **比例建议：** 即使数据量不怎么增加，只要把模型做大，效果就会显著提升。
- **影响：** 这一理论直接推动了 GPT-3（1750亿参数）等超大参数模型的诞生，导致了业界在这个阶段疯狂追求“大模型”。
### 3. 演变阶段二：Chinchilla 定律 (DeepMind, 2022)
论文： Training Compute-Optimal Large Language Models
核心观点： “数据和参数要平衡”
DeepMind 重新审视了 Kaplan 的结论，发现之前的模型（如 GPT-3）其实**严重训练不足**（Undertrained）。他们提出了修正后的 Scaling Law（通常被称为 Chinchilla Scaling Laws）：
- **平衡至上：** 在给定的算力预算下，**模型参数量 (N) 和训练数据量 (D) 应该等比例增加**。
- **黄金比例：** **20:1**。即每增加 1 个参数，大约需要 20 个 token 的训练数据。
- **结论：** 以前的模型太大了但读的书不够。如果把 GPT-3 做小一点（比如 700亿参数），但多读几倍的数据，效果会比原来的 GPT-3 更好且推理成本更低。
- **影响：** 这终结了盲目追求“万亿参数”的时代，催生了 Llama 系列等“小参数、大数据”的高性能模型。
### 4. 演变阶段三：Inference Scaling (OpenAI o1, 2024 - 至今)
**新趋势：** **“推理侧缩放”**
随着预训练 Scaling Law 逐渐遭遇数据枯竭的瓶颈，新的 Scaling Law 开始受到关注，即 **Test-time Compute（测试时计算）**。
- **核心逻辑：** 除了在**训练**时堆算力，我们在**推理**（思考）时给模型更多的时间和算力（例如让它通过“思维链”反复思考、自我修正），其智能表现也会呈现规律性提升。
- **代表模型：** OpenAI o1。它证明了通过强化学习和思维链，推理侧的算力投入可以换取解决复杂数学/代码问题的能力。
### 总结：为什么它很重要？
Scaling Law 的最大意义在于把炼丹变成了科学。
在 Scaling Law 出现之前，训练一个大模型像是在赌博；有了 Scaling Law，研究人员可以在训练之前，通过小规模实验精准预测出一个千亿参数模型在训练完之后的 Loss 是多少，从而极大地降低了高昂的试错成本
# 强化学习
## 1. 强化学习做推荐系统和其他模型做next item prediction有什么区别?
优化负对数似然和优化奖励的区别
## 2. 贝尔曼方程
- **折扣回报(discounted return):** 定义了从当前时刻的状态开始到终止状态结束时所有奖励的之和，考虑到未来奖励的不确定性，引入了折扣因子$\gamma$$$U_t=R_t+\gamma R_{t+1}+\gamma^2 R_{t+2}+\cdots=\sum\limits_{k=0}\gamma^kR_{t+k},$$注意$U_t$是一个随机变量，依赖于未来的状态和动作。
- **状态价值函数(state value function)和动作价值函数(state-action value function):** 状态价值函数衡量在策略$\pi$下，当前状态的期望回报(衡量状态的好坏)$$V^\pi(s)=\mathbb{E}_\pi\left[U_t\vert S_t=s\right].$$动作价值函数衡量在策略$\pi$下，当前状态下采取某种动作的期望回报(衡量动作的好坏)$$Q^\pi(s,a)=\mathbb{E}_\pi\left[U_t\vert S_t=s,A_t=a\right].$$不难发现状态价值函数和动作价值函数存在如下关系$$\begin{align}&V^\pi(s)=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)Q^\pi(s,a),\\&Q^\pi(s,a)=r(s,a)+\gamma\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)V^\pi(s^\prime),\end{align}$$其中$r(s,a)$是环境的奖励函数，$P(s^\prime\vert s,a)$是环境的状态转移函数，共同构成了环境动态。
- **贝尔曼方程(Bellman equation):** 不难推导出两个价值函数的贝尔曼方程$$\begin{align}&V^\pi(s)=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\left[r(s,a)+\gamma\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)V^\pi(s^\prime)\right],\\&Q^\pi(s,a)=r(s,a)+\gamma\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\sum\limits_{a^\prime\in\mathcal{A}}\pi(a^\prime\vert s^\prime)Q^\pi(s^\prime,a^\prime),\end{align}$$为了和TD learning对应，贝尔曼方程可以改写为如下形式$$\begin{align}&V^\pi(s)=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\left[\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\left[r(s,a)+\gamma V^\pi(s^\prime)\right]\right],\\&Q^\pi(s,a)=\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\left[r(s,a)+\gamma\sum\limits_{a^\prime\in\mathcal{A}}\pi(a^\prime\vert s^\prime)Q^\pi(s^\prime,a^\prime)\right],\end{align}$$
- **最优状态价值函数和最优动作价值函数:** 考虑策略空间$\Pi$中的偏序关系: 当且仅当对于任意状态$s\in\mathcal{S}$都有$V^\pi(s)\geq V^{\pi^\prime}(s)$，记$\pi\succ\pi^\prime$。假设存在最优策略（比其他所有策略都好或者不差于其他所有策略），记为$\pi^\ast$，定义最优价值函数$$V^\ast(s)=\max\limits_{\pi}V^\pi(s),$$以及最优动作价值函数$$Q^\ast(s,a)=\max\limits_{\pi}Q^\pi(s,a).$$考虑到为了使得$Q^\pi(s,a)$最大需要在$(s,a)$之后都执行最优策略,由最优策略的定义可得$$Q^\ast(s,a)=r(s,a)+\gamma\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)V^\ast(s^\prime),$$这与普通策略下的动作价值函数和状态价值函数之间的关系是一样的，此外考虑到最优策略需要在任意状态都需要执行，因此有$$V^\ast(s)=\max\limits_{a}Q^\ast(s,a).$$
- **贝尔曼最优方程(Bellman optimality equation):** 由上述最优状态价值函数和最优动作价值函数的关系，不难得到贝尔曼最优方程$$\begin{align}&V^\ast(s)=\max\limits_{a\in\mathcal{A}}\left(r(s,a)+\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)V^\ast(s^\prime)\right)\\&Q^\ast(s,a)=r(s,a)+\gamma\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\max\limits_{a\in\mathcal{A}}Q^\ast(s^\prime,a^\prime)\end{align}$$为了和TD learning对应，贝尔曼最优方程可以改写为如下形式$$\begin{align}
&V^\ast(s)=\max\limits_{a\in\mathcal{A}}\left[\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\left[r(s,a)+V^\ast(s^\prime)\right]\right]\\&Q^\ast(s,a)=\sum\limits_{s^\prime\in\mathcal{S}}P(s^\prime\vert s,a)\left[r(s,a)+\gamma\max\limits_{a\in\mathcal{A}}Q^\ast(s^\prime,a^\prime)\right]
\end{align}$$
- **注:** 以上最优策略的定义是定义在finit MDP中的，详见Sutton《Reinforcement learning: an introduction》- 3.6 Optimal Policies and Optimal Value Functions.
## 3. 常见的RL算法
### 3.1 价值学习(value-based)与策略(policy-based)学习  
(以下内容参考王树森《深度强化学习》，值得一提的是，书中对于策略梯度等公式给出了严谨的数学证明)
1. **概念:** 价值学习方法关注如何近似最优价值函数$Q^\ast(s,a)$，使用$\pi(a\vert s)=\arg\max\limits_{a}Q^\ast(s,a)$作为最优策略，策略学习方法关注如何近似最优策略，优化目标是$J(\theta)=\mathbb{E}_S\left[V^\pi(S)\right]$，其中$\theta$是策略$\pi$的参数。
2. **TD算法(Temporal Difference):** (原理) 使用当前的预测值近似真实值和未来的预测值的加和  (推导) 贝尔曼方程/最优贝尔曼方程
3. **策略梯度公式:** $$\dfrac{\partial J(\theta)}{\partial\theta}=\mathbb{E}_{S}\left[\mathbb{E}_{A\sim\pi(\cdot\vert S;\theta)}\left[\dfrac{\partial\log\pi(A\vert S;\theta)}{\partial\theta}\cdot Q^\pi(S,A)\right]\right].$$事实上，对状态的期望前面应该还有系数$\dfrac{1-\gamma^n}{1-\gamma}$，但在实际应用中，该系数可以忽略，这是因为在做梯度上升时，系数会被学习率吸收。此外，策略梯度定理只有在状态$S$服从马尔可夫链的稳态分布$d(\cdot)$时成立。**注：其实有点像使用Q值加权策略的梯度上升过程。** 
4. **广义优势估计(Generalized Advantage Estimation, GAE):** 参考[六、GAE 广义优势估计 - 知乎](https://zhuanlan.zhihu.com/p/549145459)整理，做了细微修改（作者非常厉害）
	- **背景:** 在Policy-based RL中，经常引入baseline $V^\pi(s)$ 来计算优势值函数 $$A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)=\mathbb{E}_{s^\prime \sim P(s^\prime\vert s,a)}\left(r(s,a)+\gamma V^\pi(s^\prime)-V^\pi(s)\right),$$由于使用神经网络$V_\theta(s)$近似值函数时存在偏差，因此在使用损失函数$\mathbb{E}_{s,a,s^\prime}\left[r(s,a)+\gamma V_\theta(s^\prime)-V_\theta(s)\right]^2$（TD方法）优化优势值估计是一种**高偏差、低方差**（只涉及单步值估计）的方法，考虑到状态价值函数的定义$$V^\pi(s_t)=\mathbb{E}_\pi[\sum\limits_{k=0}^n\gamma^kR_{t+k}\vert S=s],$$也可以考虑一局游戏结束后使用$\sum\limits_{k=0}^n\gamma^k r_{t+k}$对状态价值函数进行近似（MC方法），进而求解优势值，这是一种**低偏差、高方差**（涉及多步奖励）的方法。为了结合TD和MC的特性，**n步TD方法**考虑了n步回报$$G_{t\colon t+n}=R_t+\gamma R_{t+1}+\cdots+\gamma^{n-1}R_{t+n-1}+\gamma^nV^\pi(S_{t+n}),$$**λ-return方法**进行了加权平均，平衡了偏差和方差，考虑有限步$T$结束游戏，$$G^\lambda_t=(1-\lambda)\sum\limits_{n=1}^{T-t-1}\lambda^{n-1}G_{t\colon t+n}+\lambda^{T-t-1}G_{t},$$其中$G_t$是折扣回报。当$\lambda=0$时，退化为n步TD方法；当$\lambda=1$时，退化为MC方法。对于无限步，则有$$G_t^\lambda=(1-\lambda)\sum\limits_{n=1}^\infty\lambda^{n-1}G_{t:t+n}.$$
	- **GAE:** GAE借鉴了λ-return方法的思想，考虑优势函数的定义，有$$\begin{align}&\hat{A}_t^1=r_t+\gamma V(s_{t+1})-V(s_t)=\delta_t\\&\hat{A}_t^2=r_{t}+\gamma r_{t+1}+\gamma^2 V(s_{t+2})-V(s_t)=\delta_t+\gamma\delta_{t+1}\\&\cdots\\&\hat{A}_t^n=r_{t}+\gamma r_{t+1}+\cdots+\gamma^{n-1}r_{t+n-1}+\gamma^n V(s_{t+n})-V(s_t)=\sum\limits_{k=1}^n\gamma^{k-1}\delta_{t+k-1}\\&\cdots\\&\hat{A}_t^\infty=\sum\limits_{l=0}^\infty\gamma^{l}r_{t+l}-V(s_t)=\sum\limits_{l=0}^\infty\gamma^l\delta_{t+l}\end{align}$$参考λ-return方法，考虑无限步的推导，有$$\begin{align}\hat{A}_t^{\text{GAE}(\lambda,\gamma)}&=(1-\lambda)\sum\limits_{n=1}^{\infty}\lambda^{n-1}\hat{A}_t^n\\&=\sum\limits_{l=0}^\infty(\gamma\lambda)^l\delta_{t+l}\\&=\sum\limits_{l=1}^\infty(\gamma\lambda)^l\delta_{t+l}+\delta_t\\&=\gamma\lambda\hat{A}_{t+1}^{\text{GAE}(\lambda,\gamma)}+\delta_{t}\end{align}$$
	- **GAE实现:** 以PPO为例，会存储所有时间步的TD error，然后在游戏结束后，按照如下方式计算优势值![[Pasted image 20251223162615.png#center|]]
5. **常见方法:** 
	- **价值学习:** 
		- **DQN:** 通过最优贝尔曼方程和（期望的）蒙特卡洛近似推导出TD算法训练
		- **Double DQN:** 在DQN的基础上引入目标网络缓解（由max操作和自举导致的）高估问题
		- **Dueling DQN:** 通过优势头$A(s,a;\omega^A)$和状态价值头$V(s;\omega^V)$近似最优价值函数，也可以使用目标网络的技术缓解高估问题
	- 策略学习: 
		- **Reinforce:** 通过策略梯度和（回报的）蒙特卡洛近似$u_t$直接优化策略网络$\pi(a\vert s;\theta)$
		- **Reinforce with baseline:** 引入了状态价值网络$v(s;\omega)$作为基线，状态价值网络使用$u_t$作为监督信号来训练
		- **Actor-Critic:** 使用策略梯度优化策略网络$\pi(a\vert s;\theta)$(actor)，TD算法优化动作价值网络$q_\omega(s,a;\omega)$(critic)
		- **A2C (Advantage Actor-Critic):** 引入状态价值网络$v(s;\omega)$作为基线，使用TD算法更新$v(s;\omega)$，并根据$v(s;\omega)$计算的TD误差和策略梯度更新策略网络$\pi(a\vert s;\theta)$
		- **TRPO (Trust Region Policy Optimization):** (置信域算法的思想) 找一个在当前参数$\theta_\text{now}$的邻域上距离复杂的目标函数$J(\theta)$很近的简单函数$L(\theta\vert\theta_\text{now})$，在邻域中寻找$\theta$的值最大化$L(\theta\vert\theta_\text{now})$并更新参数。(TRPO中的置信域算法) $$L(\theta\vert\theta_\text{now})=\mathbb{E}_S\left[\mathbb{E}_{A\sim\pi(\cdot\vert s;\theta_\text{now})}\left[\dfrac{\pi(A\vert S;\theta)}{\pi(A\vert S;\theta_\text{now})}\cdot Q^\pi(s,A)\right]\right],$$并进一步使用蒙特卡洛模拟(两步近似$Q^\pi\to Q^{\pi_\text{now}}\to u_t$)转化成$$\tilde{L}(\theta\vert\theta_\text{now})=\dfrac{1}{n}\sum\limits_{t=1}^n\dfrac{\pi(s_t,a_t;\theta)}{\pi(s_t,a_t;\theta_\text{now})}\cdot u_t.$$在最大化时，可以选择欧几里得距离选取置信域，也可以用KL散度$$\max\limits_{\theta}\tilde{L}(\theta\vert\theta_\text{now}),\quad \text{s.t. }\dfrac{1}{n}\sum\limits_{t=1}^nD_\text{KL}\left(\pi(\cdot\vert s_t;\theta_\text{now})\Vert\pi(\cdot\vert s_t;\theta)\right)\leq\Delta,$$这是一个约束优化问题，代码实现较为复杂。一些文献使用优势函数$A^\pi(S,A)=Q^\pi(S,A)-V^\pi(S)$替换$Q^\pi(s,a)$，注意有$A^\pi(s,a)=\mathbb{E}_{s^\prime}(r(s,a)+\gamma V^\pi(s^\prime)-V^\pi(s))$。
		- **PPO (Proximal Policy Optimization):** TRPO的改进版，有两种形式
			- PPO-Penalty: 用拉格朗日乘子法将TRPO中的KL散度约束放进了目标函数中，并在迭代的过程中不断更新KL散度的系数$$\arg\max\limits_{\theta}\mathbb{E}_S\mathbb{E}_{A\sim\pi(\cdot\vert S;\theta_\text{now})}\left[\dfrac{\pi(A\vert S;\theta)}{\pi(A\vert S;\theta_\text{now})}A^\pi(S,A)-\beta D_\text{KL}\left(\pi(\cdot\vert S;\theta_\text{now})\Vert\pi(\cdot\vert S;\theta)\right)\right].$$当KL散度项小于$\delta/1.5$时令$\beta$缩小一半，当大于$\delta/1.5$时增大一倍，等于时维持现状。
			- PPO-Clip: $$\arg\max\limits_{\theta}\mathbb{E}_S\mathbb{E}_{A\sim\pi(\cdot\vert S;\theta_\text{now})}\left[\min\left\{\dfrac{\pi(A\vert S;\theta)}{\pi(A\vert S;\theta_\text{now})}A^\pi(S,A),\text{clip}\left(\dfrac{\pi(A\vert S;\theta)}{\pi(A\vert S;\theta_\text{now})},1-\epsilon,1+\epsilon\right)A^\pi(S,A)\right\}\right],$$其中$\text{clip}(x,l,r)\coloneqq\max\left\{\min\left\{x,r\right\},l\right\}$，$\epsilon>0$是一个超参数，当优势大于0时，说明动作价值高于平均，最大化这个式子会增大比值，但不会超过$1+\epsilon$；当优势小于0时，说明动作价值低于平均，则最大化u这个式子会缩小比值，但不会低于$1-\epsilon$。
			- 大量的实验表明PPO-Clip比PPO-Penalty更好，PPO-Clip的实现见[PPO 算法](https://hrl.boyuai.com/chapter/2/ppo%E7%AE%97%E6%B3%95)，注意优势值的计算使用了广义优势估计(Generalized Advantage Estimation, GAE)实现。
			- 简单来说，PPO-Clip可以理解为对于好动作（优势值大于0），提升策略生成动作的概率，但是不能偏离基准策略太远；对于坏动作（优势值小于0），降低策略生成动作的概率，但是不能偏离基准策略太远。
		- **DDPG (Deep Deterministic Policy Gradient):** 使用（确定性）策略网络$\mu(s;\theta)$学习最优策略，目标定义为$$J(\theta)=\mathbb{E}_S\left[q(S,\mu(S;\theta);\omega)\right],$$其中价值网络使用TD算法进行更新，策略网络通过最大化当前的价值网络进行更新。注意DDPG的价值网络近似动作价值函数而非最优动作价值函数；在选择动作时，一般会加一个噪声$\epsilon$。DDPG中也存在最大化（当前的价值网络）和自举造成的高估问题。
		- **TD3(Twin Delayed Deep Deterministic Gradient):**  针对DDPG的高估问题，使用两个价值网络和一个策略网络，对应三个目标网络$q(s,a;\omega_1^-),q(s,a;\omega_2^-),\mu(s;\theta^-)$，在计算TD target时，策略目标网络输出动作向量，然后取两个价值目标网络输出的较小值作为TD target。此外，TD3还有一些细节: **(动作噪声)** 在计算TD target的输出动作步骤中，加入各元素从截断正态分布$\mathcal{CN}(0,\sigma^2,-c,c)$(防止噪声过大)中采样的噪声向量；**(更新频率)** 减小更新策略网络和目标网络的频率。
		- **随机高斯策略:** 用两个神经网络分别近似高斯分布的均值和对数方差，然后利用重参数化技巧进行动作采样，并用策略梯度更新两个神经网络的参数。
		- **SAC(Soft Actor-Critic):** SAC的前身是Soft Q-learning，都属于最大熵强化学习，Soft Q-learning 不存在一个显式的策略函数，而是使用一个函数的波尔兹曼分布，在连续空间下求解非常麻烦。于是 SAC 提出使用一个 Actor 表示策略函数，从而解决这个问题。SAC使用了两个Critic网络和对应的目标网络，在计算计算TD目标和策略更新时都取两个网络的最小值。由于在学习目标中加入了熵正则项，因此TD目标和策略更新都多了一个log pi(s\vert a)项。注意SAC输出的是随机高斯策略。 
6. **连续控制问题:** 在连续动作向量的问题中，一个自然的想法是通过离散化动作空间然后训练DQN或者策略网络，但是随着自由度的增大，离散后的动作空间的大小指数增长，会造成维数灾难，DQN和策略网络的训练都变得异常困难。在真实的环境中，虽然动作空间可能是离散的，但是可能动作空间非常庞大（比如推荐系统的item数量），往往会输出连续动作向量再映射到有效动作空间（比如item列表），DDPG、TD3就是处理连续动作空间的有效办法。
7. **同策略(On-Policy)和异策略(Off-Policy):** 
	- **定义:** 首先引入行为策略(behavior policy)和目标策略(target policy)的概念，行为策略是与环境交互收集经验的策略，训练时的策略称为目标策略，如果行为策略和目标策略相同，称为同策略，如果不同则称为异策略。
	- **常见算法分类:** 常见的同策略方法包括Reinforce(收集$u_t$和用于训练的策略是同一策略)、Reinforce with baseline(同理)、Actor-Critic(使用SARSA算法训练，且策略梯度是根据目标策略计算的)、A2C(没有经验回放池)、TRPO(与A2C同理)；常见的异策略方法包括DQN及其变体(使用经验回放数组)、DDPG(同理)、TD3(同理)、SAC
8. **代码实现细节:** 
	- **目标网络:** 通常目标网络的参数不加入优化器，而是定期根据价值网络或策略网络进行优化；
	- **随机策略:** 在策略梯度的算法中，如果使用的是随机策略，一般用神经网络输出logits再经过softmax得到每个动作的概率，在选择动作时使用一个类别分布进行抽样得到动作
### 3.2 离线强化学习(Offline RL)
1. **概念:** 区别于在线(同策略)强化学习和异策略强化学习方法，离线强化学习从离线的经验回放数组中直接学习一个策略用于和环境交互。![[Pasted image 20251220144005.png]]Cited from "Offline Reinforcement Learning: Tutorial, Review, and Perspectives on Open Problems" (2023)
2. **挑战:** **(策略分布偏移)** 策略的改进往往需要探索新的动作，但是离线数据集并没有真实动作的反事实估计，因此在对未知动作的较高的值估计会导致策略分布偏移真实动作空间。
3. **现有范式:** 现有的Offline RL有两个范式，以权衡策略改进和策略分布偏移(Liu et al. 2023)
	- Behavior Constrained Policy Optimization: 显式地使用目标策略和行为策略之间的散度作为正则化；
	- Conservative Methods: 惩罚超出分布（out-of-distribution, OOD）的动作的价值估计，以避免高估目标策略价值的错误
	Cited from "Offline reinforcement learning with closed-form policy improvement operators" (2023 ICLR)
4. **经典方法:** 
	- **BCQ (Batch-Constrained deep Q-learning):** 使用条件变分自编码器生成与离线数据集中出现过的动作相似的候选动作，并在一定的范围内进行扰动以确保动作的多样性，通过类似q-learning的方式来学习最优策略。算法流程: 批量样本抽样->VAE编码$(s,a)$再解码出$\tilde{a}$->计算重构误差和KL散度以优化VAE的参数->从VAE中抽样得到状态$s^\prime$的n个候选动作并加上扰动->计算TD target并更新动作价值网络。![[Pasted image 20251220150324.png#center|]]![[Pasted image 20251220150535.png#center|]]Cited from "Off-policy deep reinforcement learning without exploration" (2019 ICML)
	  注意BCQ使用的是CVAE (Conditional VAE)，CVAE建模的是条件生成分布，在训练时，编码器以数据和条件作为输入输出近似后验分布的参数，解码器以抽样得到的隐变量和条件作为输入输出重建数据；在推理时，根据抽样得到的隐变量和条件生成新的数据，以数字9为例，条件是9，通过调整隐变量可以生成各种风格的数字9。
	- **CQL (Constrained Q-Learning):** 在标准的贝尔曼误差（TD误差）前加上了CQL正则项，惩罚了分布外动作的Q值，奖励服从离线数据集中动作分布的Q值$$\hat{Q}^{k+1}\leftarrow\arg\min\limits_{Q}\alpha\cdot\left(\mathbb{E}_{s\sim\mathcal{D},a\sim\mu(a\vert s)}\left[Q(s,a)\right]-\textcolor{red}{\mathbb{E}_{s\sim\mathcal{D},a\sim\hat{\pi}_\beta(a\vert s)}\left[Q(s,a)\right]}\right)+\dfrac{1}{2}\mathbb{E}_{s,a,s^\prime\sim\mathcal{D}}\left[\left(Q(s,a)-\hat{\mathcal{B}}^\pi\hat{Q}^k(s,a)\right)^2\right].$$![[Pasted image 20251220161212.png]]其中$\mathcal{B}^\pi$是贝尔曼算子(Bellman operator)，$\hat{\mathcal{B}}^\pi\hat{Q}^k(s,a)$其实就是TD target。上式进一步可以改写为$$\min\limits_{Q}\textcolor{red}{\max\limits_\mu}\alpha\cdot\left(\mathbb{E}_{s\sim\mathcal{D},a\sim\textcolor{red}{\mu(a\vert s)}}\left[Q(s,a)\right]-\textcolor{red}{\mathbb{E}_{s\sim\mathcal{D},a\sim\hat{\pi}_\beta(a\vert s)}\left[Q(s,a)\right]}\right)+\dfrac{1}{2}\mathbb{E}_{s,a,s^\prime\sim\mathcal{D}}\left[\left(Q(s,a)-\hat{\mathcal{B}}^\pi\hat{Q}^k(s,a)\right)^2\right]+\textcolor{red}{\mathcal{R}(\mu)}\quad(\text{CQL}(\mathcal{R})).$$![[Pasted image 20251220162004.png]]其中$\mathcal{R}(\mu)$是一个正则化器。令$\mathcal{R}(\mu)=-D_\text{KL}(\mu\Vert\rho)$，其中$\rho(a\vert s)$是先验分布，推导出$\mu(a\vert s)\propto\rho(a\vert s)\cdot\exp(Q(s,a))$，当$\rho=\text{Unif}(a)$时，可以推导出如下变体，记为$\text{CQL}(\mathcal{H})$$$\min\limits_{Q}\alpha\mathbb{E}_{s\sim\mathcal{D}}\left[\log\sum\limits_{a\in\mathcal{A}}\exp(Q(s,a))-{\mathbb{E}_{a\sim\hat{\pi}_\beta(a\vert s)}\left[Q(s,a)\right]}\right]+\dfrac{1}{2}\mathbb{E}_{s,a,s^\prime\sim\mathcal{D}}\left[\left(Q(s,a)-\hat{\mathcal{B}}^\pi\hat{Q}^k(s,a)\right)^2\right].$$![[Pasted image 20251220162732.png]]如果$\rho=\hat{\pi}^{k-1}$，则(4)的第一项被$\hat{\pi}^{k-1}$选中的动作的Q值的指数加权平均替代。注意到(4)式的更新不包括策略，可以直接令$\mu^\ast$为策略；如果使用Actor-Critic的方式，需要借助SAC算法额外训练Actor。一些额外的资料[离线强化学习(Offline RL)系列3: (算法篇) CQL 算法详解与实现 - 知乎](https://zhuanlan.zhihu.com/p/496103195)[CQL算法logsumexp公式推导 - 知乎](https://zhuanlan.zhihu.com/p/546193376)[Conservative Q Learning(保守强化学习)傻瓜级讲解和落地教程 - 知乎](https://zhuanlan.zhihu.com/p/603691759)
	  Cited from "Conservative q-learning for offline reinforcement learning" (2020 NeurIPS)
	- **TD3+BC (Twin Delayed Deep Deterministic Gradiant with Behavior Cloning):** 在TD3算法中的更新策略步骤添加了行为克隆损失项![[Pasted image 20251220154505.png]]Cited from "A Minimalist Approach to Ofﬂine Reinforcement Learning" (2021 NeurIPS)
### 3.3 最大熵强化学习 (Maximum Entropy RL)
1. **概念:** 最大熵强化学习在标准RL的基础上引入了熵正则项，以鼓励策略网络的输出更具多样性。
2. **目标:** 在最大熵强化学习中，学习目标被定义为$$J(\theta)=\mathbb{E}_S\left[V^\pi(S)+\alpha H(S;\theta)\right],$$其中$H(s;\theta)=-\sum\limits_{a\in\mathcal{A}}\pi(a\vert s;\theta)\log\pi(a\vert s;\theta)$。
3. **常见算法:** Soft Q-learning, SAC
4. **软价值函数:** 在标准的Q-learning中，状态价值函数$V(s)=\max\limits_{a\in\mathcal{A}}Q(s,a)$，而最大化操作是一种硬操作，而在最大熵强化学习的框架下，状态价值函数变成$$V_\text{soft}(s)=\alpha\log\left(\sum\limits_{a}\exp\left(\dfrac{Q_\text{soft}(s,a)}{\alpha}\right)\right),$$其中$\alpha$是温度系数，控制熵正则项的重要性。
5. **详细推导:** 给定状态$s$，最大熵强化学习的优化目标为$$\max\limits_{\pi}V_\text{soft}(s)=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)Q(s,a)-\alpha\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\log\pi(a\vert s),\quad \text{s.t. }\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)=1.$$利用拉格朗日乘子法引入乘子$\lambda$构建拉格朗日函数$\mathcal{L}$$$\mathcal{L}(\pi,\lambda)=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\left(Q(s,a)-\alpha\log\pi(a\vert s)\right)-\lambda(\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)-1),$$通过对$\pi(a\vert s)$求偏导可得$$\dfrac{\partial\mathcal{L}(\pi,\lambda)}{\partial\pi(a\vert s)}=Q(s,a)-\alpha-\alpha\log\pi(a\vert s)-\lambda=0,$$求解可得$$\pi(a\vert s)=\exp\left(\dfrac{Q(s,a)}{\alpha}\right)\cdot\left(-\dfrac{\lambda}{\alpha}-1\right),$$由于$\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)=1$，可以通过归一化来消除常数项，进而得到最优策略$$\pi(a\vert s)=\dfrac{\exp\left(\dfrac{Q(s,a)}{\alpha}\right)}{\sum\limits_{a^\prime\in\mathcal{A}}\exp\left(\dfrac{Q(s,a^\prime)}{\alpha}\right)}$$这是一个关于Q值的Boltzmann分布，将最优策略代入优化目标可得$$\begin{align}
V_\text{soft}(s)&=\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\cdot \left[Q(s,a)-\alpha\log \dfrac{\exp\left(\dfrac{Q(s,a)}{\alpha}\right)}{Z}\right],\\
&=\alpha\sum\limits_{a\in\mathcal{A}}\pi(a\vert s)\log Z,\\
&=\alpha\log\sum\limits_{a^\prime\in\mathcal{A}}\exp\left(\dfrac{Q(s,a^\prime)}{\alpha}\right),
\end{align}$$这也就是软价值函数的定义。
## 4. DPO
### 4.1 RLHF
![[rlhf.png]]RLHF分为三个步骤:
(1) 通过有监督微调(Supervised Fine-tuning, SFT)让模型学会生成prompt的response；
(2) 通过人类偏好数据训练奖励模型；
(3) 基于奖励模型，使用强化学习算法(如PPO)训练生成response的策略

具体来说，记SFT之后的生成策略为 $\pi^\text{SFT}$，给定prompt $x$，可以生成问题对 $(y_1,y_2)\sim\pi^\text{SFT}(y\vert x)$，提供给人类labelers，标注后得到偏好 $y_w\succ y_l\vert x$。假设偏好由一个潜在的奖励函数 $r^\ast(y,x)$ 根据Bradley-Terry模型生成$$p^\ast(y_w\succ y_l\vert x)=\dfrac{\exp(r^\ast(x,y_w))}{\exp(r^\ast(x,y_w))+\exp(r^\ast(x,y_l))}=\sigma(r^\ast(x,y_w)-r^\ast(x,y_l)) \tag{1}$$而 $\mathcal{D}=\{x^{(i)},y_w^{(i)},y_l^{(i)}\}_{i=1}^N$ 是从 $p^\ast$ 中采样得到的离线数据集。
在奖励建模阶段，我们可以通过优化负的对数似然函数损失来优化参数化奖励模型$r_\phi(x,y)$$$\mathcal{L}_R(r_\phi,\mathcal{D})=-\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\log\sigma(r_\phi(x,y_w)-r_\phi(x,y_l))\tag{2}$$通常，为了保证奖励函数的方差较小，需要先对奖励进行归一化，使得 $\mathbb{E}_{x,y\sim\mathcal{D}}\left[r_\phi(x,y)\right]=0$。
在强化学习阶段，使用学习到的奖励函数 $r_\phi(x,y)$ 来优化生成策略$$\max\limits_{\pi_\theta}\mathbb{E}_{x\sim\mathcal{D},y\sim\pi_\theta(y\vert x)}\left[r_\phi(x,y)\right]-\beta D_{\text{KL}}\left[\pi_\theta(y\vert x)\Vert\pi_{\text{ref}}(y\vert x)\right]\tag{3}$$其中 $\pi_\text{ref}=\pi^\text{SFT}$，在实际应用中，生成策略 $\pi_\theta$ 也被初始化为 $\pi^\text{SFT}$。由于语言生成的离散性(从策略网络输出的softmax概率分布中抽样得到token)，因此这个目标是不可微的，通常使用强化学习来优化。标准的方法是构造奖励函数$$r(x,y)=r_\phi(x,y)-\beta(\log\pi_\theta(y\vert x)-\log\pi_{\text{ref}}(y\vert x))$$然后使用PPO来优化。（注意这个奖励函数其实是把KL散度拆开后和前项合并得到的）
### 4.2 RLHF VS DPO
![[Pasted image 20251220182457.png]]
DPO不显式使用奖励模型，不使用强化学习算法，而是直接从人类偏好数据（通常为成对比较）中直接学习最优策略。
### 4.3 DPO细节
1. 推导DPO目标
   回顾RLHF的优化目标$$\max\limits_{\pi_\theta}\mathbb{E}_{x\sim\mathcal{D},y\sim\pi_\theta(y\vert x)}\left[r_\phi(x,y)-\beta(\log\pi_\theta(y\vert x)-\log\pi_{\text{ref}}(y\vert x))\right],\quad\text{s.t. }\sum\limits_{y\in\mathcal{Y}}\pi_\theta(y\vert x)=1.$$可以通过推导（KL散度法）$$\begin{align}
&\max\limits_{\pi_\theta}\mathbb{E}_{x\sim\mathcal{D},y\sim\pi_\theta(y\vert x)}\left[r_\phi(x,y)-\beta(\log\pi_\theta(y\vert x)-\log\pi_{\text{ref}}(y\vert x))\right]\\=&\min\limits_{\pi_\theta}\mathbb{E}_{x\sim\mathcal{D},y\sim\pi_\theta(y\vert x)}\left[\log\dfrac{\pi_\theta(y\vert x)}{\pi_{\text{ref}}(y\vert x)}-\dfrac{1}{\beta}r(x,y)\right]\\=&\min\limits_{\pi_\theta}\mathbb{E}_{x\sim\mathcal{D},y\sim\pi_\theta(y\vert x)}\left[\log\dfrac{\pi_\theta(y\vert x)}{\frac{1}{Z(x)}\pi_{\text{ref}}(y\vert x)\exp\{\frac{1}{\beta}r(x,y)\}}-\log Z(x)\right]\\=&\min\limits_{\pi_\theta}\mathbb{E}_{x\in\mathcal{D}}\left[D_{\text{KL}}\left[\pi_\theta(y\vert x)\Vert\dfrac{1}{Z(x)}\pi_{\text{ref}}(y\vert x)\exp\{\dfrac{1}{\beta}r(x,y)\}\right]-\log Z(x)\right]
\end{align}$$得到最优解$$\pi_r(y\vert x)=\dfrac{1}{Z(x)}\pi_{\text{ref}}(y\vert x)\exp\left(\dfrac{1}{\beta}r(x,y)\right),\tag{4}$$其中$Z(x)=\sum\limits_{y\in\mathcal{Y}}\pi_\text{ref}(y\vert x)\exp\left(\dfrac{1}{\beta}r(x,y)\right)$，注意也可以用拉格朗日乘子法进行推导（更通用）。通过重写(4)式可以得到$$r(x,y)=\beta\log Z(x)+\beta\log\dfrac{\pi_r(y\vert x)}{\pi_\text{ref}(y\vert x)}.$$假设这里学到的是最优奖励函数$r^\ast$和对应的$\pi^\ast$，代回(1)式(Bradley-Terry模型)可以得到$$p^\ast(y_w\succ y_l\vert x)=\sigma\left(\beta\log\dfrac{\pi^\ast(y_w\vert x)}{\pi_\text{ref}(y_w\vert x)}-\beta\log\dfrac{\pi^\ast(y_l\vert x)}{\pi_\text{ref}(y_l\vert x)}\right).\tag{6}$$进而重写(2)式(奖励建模的损失函数)得到DPO的损失函数$$\mathcal{L}_{\text{DPO}}(\pi_\theta;\pi_\text{ref})=\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left[\log\sigma\left(\beta\log\dfrac{\pi_\theta(y_w\vert x)}{\pi_\text{ref}(y_w\vert x)}-\beta\log\dfrac{\pi_\theta(y_l\vert x)}{\pi_\text{ref}(y_l\vert x)}\right)\right].\tag{7}$$
2. DPO更新的内在机理
   对DPO更新的梯度进行分析$$    \begin{align}
      &\nabla_\theta\mathcal{L}_{\text{DPO}}(\pi_\theta;\pi_\text{ref})\\
      =&-\beta\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\Bigg[\underbrace{\sigma\left(\hat{r}_\theta(x,y_l)-\hat{r}_\theta(x,y_w)\right)}_{\text{higher weight when reward estimate is wrong}}\cdot\bigg[\underbrace{\nabla_\theta\log\pi(y_w\vert x)}_\text{increase likelihood of $y_w$}-\underbrace{\nabla_\theta\log\pi(y_l\vert x)}_\text{decrease likelihood of $y_l$}\bigg]\Bigg],
      \end{align}\tag{8}$$其中$\hat{r}_\theta(x,y)=\beta\log\dfrac{\pi_\theta(y\vert x)}{\pi_\text{ref}(y\vert x)}$。梯度公式告诉我们，DPO的更新惩罚了错误的奖励估计，并提升$y_w$的似然，降低$y_l$的似然，注意奖励函数是由参数化策略和参考策略隐式定义的。
3. DPO流程![[Pasted image 20251221192644.png#center|]]注意DPO优化参数化策略$\pi_\theta$，等价于通过(2)式优化奖励函数$\hat{r}_\theta(x,y)=\beta\log\dfrac{\pi_\theta(y\vert x)}{\pi_\text{ref}(y\vert x)}$。
4. 理论分析
	- **语言模型其实是一个奖励模型:** 
	  DPO可以绕过显式奖励拟合和通过强化学习（RL）来学习策略的过程，而是使用单一的最大似然目标进行优化。事实上，(5)式展示的DPO目标等价于优化以$\hat{r}^\ast(x,y)=\beta\log\dfrac{\pi^\ast(y\vert x)}{\pi_\text{ref}(y\vert x)}$为奖励函数的Bradley-Terry模型。下面将证明它不会限制所学习的奖励模型的类别，并允许精确恢复最优策略。
	  首先引入奖励函数的等价类的概念![[Pasted image 20251221193755.png#center|]]根据上述概念陈述如下两个引理以及展示对应的证明![[Pasted image 20251221193855.png#center|]]引理1和引理2告诉我们属于同一个等价类的奖励模型不会影响用户的偏好分布，且会在RL阶段训练出相同的最优策略。关于引理1，考虑更一般的Plackett-Luce模型和选项$\{y_k\}_{k=1}^K$，以及属于同一个等价类的奖励函数$r(x,y)$和$r^\prime(x,y)$，则存在某个$f(\cdot)$使得$r^\prime(x,y)=r(x,y)+f(x)$，有$$P(y_k\vert x,\{y_k\}_{k=1}^K)=\dfrac{\exp\{r(x,y_k)\}}{\sum\limits_{l=1}^K\exp\{r(x,y_l)\}},$$因此排序$\tau=\{\tau(1),\cdots,\tau(k)\}$出现的概率为$$\begin{align}
      p_{r^\prime}(\tau\vert x,\{y_k\}_{k=1}^K)&=\prod\limits_{k=1}^K\dfrac{\exp\{r^\prime(x,y_{\tau_{(k)}})\}}{\sum\limits_{j=k}^{K}\exp\{r^\prime(x,y_{\tau_{(j)}})\}}\\
      &=\prod\limits_{k=1}^K\dfrac{\exp\{r(x,y_{\tau_{(k)}})+f(x)\}}{\sum\limits_{j=k}^{K}\exp\{r(x,y_{\tau_{(j)}})+f(x)\}}\\
      &=\prod\limits_{k=1}^K\dfrac{\exp\{r(x,y_{\tau_{(k)}})\}}{\sum\limits_{j=k}^{K}\exp\{r(x,y_{\tau_{(j)}})\}}\\
      &=p_{r}(\tau\vert x,\{y_k\}_{k=1}^K)
      \end{align}$$引理一证毕。关于引理二，沿用上述记号，有$$    \begin{align}
      \pi_{r^\prime}(y\vert x)&=\dfrac{\pi_{\text{ref}}(y\vert x)\exp\left(\frac{1}{\beta}{r^\prime}(x,y)\right)}{\sum\limits_y\pi_{\text{ref}}(y\vert x)\exp\left(\frac{1}{\beta}{r^\prime}(x,y)\right)}\\
      &=\dfrac{\pi_{\text{ref}}(y\vert x)\exp\left(\frac{1}{\beta}{r}(x,y)+\frac{1}{\beta}f(x)\right)}{\sum\limits_y\pi_{\text{ref}}(y\vert x)\exp\left(\frac{1}{\beta}{r}(x,y)+\frac{1}{\beta}f(x)\right)}\\
      &=\dfrac{\pi_{\text{ref}}(y\vert x)\exp\left(\frac{1}{\beta}{r}(x,y)\right)}{\sum\limits_y\pi_{\text{ref}}(y\vert x)\exp\left(\frac{1}{\beta}{r}(x,y)\right)}\\
      &=\pi_{r}(y\vert x)
	      \end{align}$$引理2证毕。由引理1和引理2，可以推导出如下定理![[Pasted image 20251221200028.png#center|]]定理1告诉我们可以使用目标策略和参考策略来表示奖励函数的等价类。证明如下：对于任意奖励函数$r(x,y)$，其推导出的最优策略满足$$r(x,y)=\beta\log\dfrac{\pi_r(y\vert x)}{\pi_{\text{ref}}(y\vert x)}+\beta\log Z(x).$$记$$f(r;\pi_\text{ref},\beta)=r(x,y)-\beta\log Z(x)=\beta\log\dfrac{\pi_r(y\vert x)}{\pi_{\text{ref}}(y\vert x)},$$与$r(x,y)$等价。考虑另一个属于该等价类的奖励函数$r^\prime(x,y)$，由引理2可得$$f(r;\pi_\text{ref},\beta)=f(r^\prime;\pi_\text{ref},\beta),$$定理证毕。注意定理1告诉我们可以考虑一个满足下式的特殊的奖励函数代表整个等价类$$\sum\limits_y\underbrace{\pi_{\text{ref}}(y\vert x)\exp\left(\dfrac{1}{\beta}{r}(x,y)\right)}_{\pi_r(y\vert x)}=1.\tag{9}$$这告诉我们尽管计算(4)式中归一化项很难，但DPO利用人类偏好只取决于两（多）个选择相对好坏而非绝对分数这一特性，只需要关注奖励函数的等价类中特定的奖励函数((9)式)，这样做不仅没有损失模型的表达能力，反而让(4)式中的最优策略对于任意prompt$x$都是解析可解的。
	 - **Actor-Critic 算法的不稳定性:** 假设参数化策略$\pi_\theta$，通过最小化与最优策略$\pi^\ast$的KL散度$D_\text{KL}\left[\pi_\theta(y\vert x)\Vert\pi^\ast(y\vert x)\right]$来学习，$\pi^\ast$通过(7)式得到，则有$$    \begin{align}
      \max\limits_{\pi_\theta}\mathbb{E}_{\pi_\theta(y\vert x)}\bigg[&\underbrace{r_\phi(x,y)-\beta\log\sum\limits_{y}\pi_\text{ref}(y\vert x)\exp\left(\dfrac{1}{\beta}r_\phi(x,y)\right)}_{f(r_\phi,\pi_\text{ref},\beta)}\\
      &-\underbrace{\beta\log\dfrac{\pi_\theta(y\vert x)}{\pi_{\text{ref}}(y\vert x)}}_\text{KL Divergence}\bigg]
    \end{align}\tag{10}$$具体推导如下，考虑奖励函数$r_\phi(x,y)$对应的最优策略$$\pi^\ast(y\vert x)=\dfrac{1}{Z(x)}\pi_{\text{ref}}(y\vert x)\exp\left(\dfrac{1}{\beta}r_\phi(x,y)\right).$$则最小化KL散度$$\begin{align}
      &D_\text{KL}\left[\pi_\theta(y\vert x)\Vert\pi^\ast(y\vert x)\right]\\
      =&\min\limits_{\pi_\theta}\mathbb{E}_{\pi_\theta(y\vert x)}\left[\log\dfrac{\pi_\theta(y\vert x)}{\pi^\ast(y\vert x)}\right]\\
      =&\min\limits_{\pi_\theta}\mathbb{E}_{\pi_\theta(y\vert x)}\left[\log\dfrac{\pi_\theta(y\vert x)}{\pi_\text{ref}(y\vert x)}+\log Z(x)-\dfrac{1}{\beta}r_\phi(x,y)\right]\\
      =&\max\limits_{\pi_\theta}\mathbb{E}_{\pi_\theta(y\vert x)}\left[r_\phi(x,y)-\beta\log Z(x)-\beta\log\dfrac{\pi_\theta(y\vert x)}{\pi_{\text{ref}}(y\vert x)}\right]
    \end{align}$$证毕。注意到这一目标函数与RLHF中RL步骤的目标函数很相似，但是多了一个归一化项，可以理解为参考策略的软价值函数。虽然这一项并不影响最优解，但没有它时，**目标的策略梯度可能会有很高的方差**，从而使学习变得不稳定。我们可以通过使用学习的值函数来对归一化项进行补偿，但这也可能难以优化。另一种选择是使用基于人类完成的基线来归一化奖励，本质上是对归一化项的**单样本蒙特卡罗估计**。相比之下，DPO 的重新参数化产生的奖励函数不需要任何基线。
## 5. GRPO
### 5.1 PPO to GRPO
1. PPO回顾与GRPO概览
   回顾大模型RL微调阶段中PPO的目标函数![[Pasted image 20251222192029.png]]其中$q,o$分别表示问题和大模型的输出，注意输出的长度为$\vert o\vert$。在PPO中，策略网络和价值网络一起训练，且为了减轻奖励模型的过度优化，标准方法是在每个token的奖励中，从参考模型添加**逐token的KL惩罚**![[Pasted image 20251222192801.png#center|]]由于价值网络和策略网络一般规模相当，带来了相当大的**内存和计算负担**。此外，在强化学习训练过程中，价值函数被视为**计算优势以减少方差**的基线。而在大语言模型的上下文中，通常只有最后一个标记会被奖励模型分配奖励分数（**稀疏奖励**），这可能会使在每个标记上都准确的价值函数的训练变得复杂。为此，本文提出了GRPO，与PPO进行额外的值函数近似不同，GRPO利用对同一问题产生的多个输出采样的平均奖励作为基线![[Pasted image 20251222193752.png]]其中$\epsilon,\beta$都是超参数。文中还提到GRPO利用**group relative way**来计算优势值，与奖励模型的**比较特性**高度一致，因为奖励模型通常是在同一问题上的输出之间比较的数据集上进行训练的。注意GRPO将目标策略与参考策略的KL散度加入到损失函数中进行正则化，而不是加到奖励函数中，**以避免将$\hat{A}_{i,t}$的计算复杂化**。而且，GRPO使用了KL散度的无偏估计量![[Pasted image 20251222195011.png]]
2. Outcome Supervision RL with GRPO
   对于每个问题$q$，从旧策略中抽取一组输出$\{o_1,\cdots,o_G\}$，通过奖励函数评分得到一组奖励$\{r_1,\cdots,r_G\}$，然后对每个奖励进行归一化得到优势值估计$\hat{A}_{i,t}=\tilde{r_i}=\dfrac{r_i-\text{mean}(\mathbfit{r})}{\text{std}(\mathbfit{r})}$。
3. Process Supervision RL with GRPO
   考虑到结果监督仅在每个输出的末尾提供奖励，这可能不足以有效地监督复杂数学任务中的策略。本文还探索了过程监督，在每一个推理步骤的末尾提供奖励，有$\hat{A}_{i,t}=\sum\limits_{\text{index}(j)\geq t}\tilde{r_i}^{\text{index}(j)}$。
4. Iterative RL with GRPO
   随着强化学习训练过程的进行，旧的奖励模型可能不足以监督当前的策略模型。因此，我们还探索了与GRPO结合的迭代RL。如算法1所示，在迭代GRPO中，我们基于来自策略模型的采样结果生成新的奖励模型训练集，并通过一种重放机制持续训练旧的奖励模型，该机制包含10%的历史数据。然后，我们将参考模型设置为策略模型，并使用新的奖励模型持续训练策略模型。![[Pasted image 20251222200027.png]]
### 5.2 思考
1. **共享参数:** 为什么LLM的actor和critic不能共享Encoder的参数呢？
2. **比较特性:** 为什么说GRPO的这种group relative way就和奖励函数的比较特性高度一致？
3. **稀疏奖励:** LLM的策略函数是给定问题，生成token，通过自回归的生成过程得到一定长度的答案，这种方式肯定会导致奖励稀疏的问题，因为偏好数据是对于答案而非每一个token定义的
4. **MDP:** 与标准的RL不同，LLM的策略应该是自回归生成一个序列，而非单个token，奖励也只有在序列生成后才被观测，但是策略分布又必须考虑token级别的生成，因此对于LLM来说：MDP被描述为，给定问题（初始状态），LLM生成一个token，再根据问题和token（新的状态）生成下一个token，直到整个序列生成，用户（环境）提供奖励，奖励被均分到每一个token。
5. **优势值近似:** 考虑优势函数的定义$$A^\pi(s_t,a_t)=\mathbb{E}_{s_{t+1}\sim P(s_{t+1}\vert s_t,a_t)}\left[r(s_t,a_t)+\gamma V^\pi(s_{t+1})-V^\pi(s_t)\right],$$对于LLM来说，状态转移函数是确定的（旧序列+新token=新状态），且奖励函数满足$$r(s_t,a_t)=\dfrac{1}{T}r(s_T,a_T),\quad\forall t\in[1,\cdots,T],$$其中$T$是序列的长度，则有$$V^\pi(s_t)=\sum\limits_{k=0}^{T-t}\gamma^kr_{t+k}=\dfrac{1-\gamma^{T-t+1}}{1-\gamma}\dfrac{1}{T}r(s_T,a_T),$$因此优势值等于$$A^\pi(s_t,a_t)=\dfrac{1}{T}r(s_T,a_T)\cdot\left[1+\gamma\cdot\dfrac{1-\gamma^{T-t}}{1-\gamma}-\dfrac{1-\gamma^{T-t+1}}{1-\gamma}\right]=\dfrac{1}{T}r(s_T,a_T)\cdot\left[1+\dfrac{\gamma-1}{1-\gamma}\right]=0???$$事实上，可以从稀疏奖励的角度来看，奖励函数满足$$r(s_t,a_t)=\left\{\begin{align}&0,\quad\text{t<T}\\&R,\quad{t=T}\end{align}\right.$$则有状态价值函数$$V^\pi(s_t)=\gamma^{T-t}R,$$则优势值满足$$A^\pi(s_t,a_t)=\left\{\begin{align}&\gamma V^\pi(s_{t+1})-V^\pi(s,a)=0,\quad t<T,\\&R-V^\pi(s_T)=0,\quad t=T\end{align}\right.$$感觉有点怪，考虑不引入baseline，则有$$V^\pi(s_t)=\gamma^{T-t}R=\gamma V^\pi(s_{t+1})$$如果是站在优化$$J(\theta)=\mathbb{E}_{s_1\sim\mathcal{S}}V^\pi(s_1),$$按照梯度上升时，系数$\gamma^{T-t}$会被学习率吸收的说法，其实就可以用奖励近似状态价值。
## 6. RL的训练
(以下内容来自Gemini3.0 Pro)
1. 为什么 RL 的训练会不稳定？
	- **非平稳的训练目标 (Non-stationary Targets/Bootstrapping):** 在监督学习中，标签（Label）是固定的。但在 RL（特别是基于值的方法，如 DQN）中，我们通常使用“自举”（Bootstrapping）的方式更新网络。也就是说，更新当前网络的 $Q(s,a)$ 时，目标值往往依赖于同一个（或稍旧的）网络计算出的 $\max Q(s', a')$，导致训练像是在追逐一个移动的靶子，极易产生震荡。
	- **数据非独立同分布 (Non-i.i.d. Data):** 监督学习假设数据是独立同分布的（i.i.d.）。而在 RL 中，智能体产生的数据是**序列相关**的（当前的 $s_{t+1}$ 强依赖于 $s_t$ 和 $a_t$）。
	- (这种解释感觉最靠谱)
	  **高方差的梯度 (High Variance in Gradients):** 特别是在策略梯度（Policy Gradient）算法中，由于环境本身是随机的（Stochastic），且策略也是随机的，导致即使在相同的状态下，采样得到的 Reward 差异也可能巨大。**蒙特卡洛采样**带来的高方差会导致梯度估计非常嘈杂，更新方向忽左忽右，难以收敛。
	- **探索与利用的矛盾 (Exploration vs. Exploitation):** 如果探索不够，模型会陷入局部最优；如果探索过多，模型无法稳定在最优策略上。这种平衡非常微妙，稍有偏差就会导致训练崩盘。
2. 什么情况下 RL 的策略会坍缩到几个 Action 上？
	- **Q值高估 (Overestimation Bias) - 针对 Value-based:** DQN 等算法中使用了 $\max$ 操作符。如果初期由于噪声，某个动作 $a$ 偶然获得了一个被高估的 Q 值，算法会倾向于反复选择它。
	- **熵过低 (Low Entropy) - 针对 Policy-based:** 在 Actor-Critic 或 PPO 中，如果奖励信号（Reward）过于稀疏或某些动作的早期回报稍微高一点，策略网络会迅速增加该动作的概率。如果没有足够的**熵正则化 (Entropy Regularization)**，分布 $\pi(a|s)$ 会迅速变成 Dirac 分布（尖峰），失去随机性。
	- **奖励设计的漏洞 (Reward Hacking):** 如果环境存在某个“安全但平庸”的动作（例如：为了不扣分而原地不动），而探索新动作的惩罚（Penalty）过大，智能体为了规避风险，会迅速坍缩到这个安全动作上，不再进行任何有意义的尝试。
	- **灾难性干扰 (Catastrophic Interference):** 在使用神经网络逼近函数时，更新某个状态的策略可能会意外地大幅改变其他状态的策略输出，导致在某些状态下所有动作的概率分布被破坏，最终坍缩。
3. 有哪些方法来稳定训练？
	- **针对数据与目标 (Data & Targets)**: 经验回放 (Experience Replay)、目标网络 (Target Network)、Double Q-learning
	- **针对策略更新 (Policy Updates)**: 限制更新步长 (Trust Region / Clipping)、熵正则化 (Entropy Regularization)
	- **针对方差与结构 (Variance & Architecture)**: Actor-Critic 架构、优势函数 (Advantage Function)与广义优势估计（GAE）、奖励归一化与裁剪 (Reward Normalization/Clipping)
# 推荐系统
## 1. 用户的行为分别服从什么概率分布,又能推导出什么损失?
1. 二分类行为
	- 适用行为: 点击 (Click)、点赞 (Like)、收藏 (Favorite)、关注 (Follow)、转发 (Share)、点踩 (Dislike/Not Interested)
	- 概率分布: 伯努利分布(Bernoulli Distribution)$$P(x;p)=p^x(1-p)^{1-x}.$$
	- 注意: 对于“转发”或“收藏”这类极其稀疏的行为（正样本极少），虽然本质也是伯努利分布，但在工程上常需要通过**样本加权**（Sample Weighting）或**Focal Loss**来处理类别不平衡问题。
	- 引申: 
	  (样本加权) 通过给正样本赋高权重，可以是逆频率加权，也可以是业务加权 
	  (Focal Loss) 在标准的BCE loss上增加了两个系数$$\mathcal{L}_\text{FL}= - \alpha (1-p)^\gamma \cdot x \log(p) + (1-\alpha) p^\gamma \cdot (1-x) \log(1-p),$$其中平衡因子 $\alpha$ 用来调节正负样本本身的比例不平衡（例如 0.75），$\gamma$ (Gamma) 是一个超参数，通常取 2.0，那些模型已经学得很好的简单样本，其 Loss 贡献几乎归零；模型会被迫去学习那些预测不准的“困难样本”。其实就是对于样本为正样本的概率$p$，计算$$-\alpha(1-p)^\gamma\log p$$如果正样本已经学得很好了，那么$(1-p)^\gamma$会比较小，用来抑制学得好的样本。
2. 连续行为
	- 适用行为: 观看时长
	- 特点: 长数据的分布通常是**长尾（Long-tail）** 且非负的
	- 建模方式: 
		- 绝对时长: $x \in [0, +\infty)$，且呈现明显的右偏分布（大部分人看很短，少数人看很久），一般用对数正态分布$z = \log(x + \epsilon)\sim\mathcal{N}(\mu,\sigma^2)$，概率密度函数为$$f(x;\mu,\sigma^2)=\dfrac{1}{\sqrt{2\pi}\sigma x}\exp\left\{-\frac{(\log (x+\epsilon)-\mu)^2}{2\sigma^2}\right\},$$然后优化对数时间的MSE损失。进一步地，可以使用**Weibull 分布** 或 **Gamma 分布**：这两个分布专门用于描述“生存时间”或“等待时间”，在学术界应用较多，能更好地拟合长尾。
		- 完播率: 定义为观看时长除以总时长，通常截断在$[0,1]$，定义为$x\in[0, 1]$，一般使用Beta分布建模，可以模拟“两头高中间低”（很多0%和100%的用户）或“单峰”分布，概率密度函数为$$f(x;a,b)=\dfrac{1}{B(a,b)}x^{a-1}(1-x)^{b-1},\quad x\in(0,1),$$其中$B(a,b)$是Beta函数，注意在优化Beta分布的参数时需要对$x$进行截断，然后优化$x$的对数似然
3. 计数型行为
	- 适用行为: 评论数 (Number of Comments)、循环播放次数 (Loop Counts)、页面进入次数。
	- 概率分布: 
		- **泊松分布 (Poisson Distribution)：** 最基础的计数分布，概率质量函数为$$P(x=k)=\dfrac{\lambda^k}{x!}e^{-\lambda},$$注意泊松分布的均值等于方差，$\lambda$衡量事件发生的速率。
		- **负二项分布 (Negative Binomial Distribution, NBD)：** **（更推荐）**
		  在推荐场景中，计数数据往往存在过离散（Over-dispersion）现象（即方差远大于均值，例如大部分人评论0次，极少数人评论100次）。泊松分布无法很好地拟合这种情况，而负二项分布引入了额外的参数来适应这种高方差。概率质量函数为$$P(x=k)=\dfrac{\Gamma(k+r)}{k!\Gamma(r)}(1-p)^rp^k,$$其中$\Gamma(\cdot)$是Gamma函数，参数 $r$ (离散参数) 和 $p$ (成功概率)，负二项分布的均值和方差分别为$E[X] = \mu$和$Var(X) = \mu + \frac{\mu^2}{r}$。在推荐系统中，不要把 NBD 理解为“失败 r 次前的成功次数”，而应该理解为：**每个用户的活跃度 $\lambda$ 是不同的，且 $\lambda$ 本身服从伽马分布 (Gamma Distribution)。**
## 2. DIN和DIEN在工业级推荐系统中应用存在哪些难点?
(DIN)![[Pasted image 20251208175626.png#center|]]翻译: 在线服务工业深度网络并不是一项容易的工作，每天有数亿用户访问我们的系统。更糟糕的是，在流量高峰期，我们的系统每秒钟要服务超过100万用户。需要以高吞吐量和低延迟进行实时CTR预测。例如，在我们的实际系统中，我们需要在不到10毫秒的时间内为每位访客预测数百个广告。在我们的实践中，采用了几种重要技术来加速CPU-GPU架构下工业深度网络的在线服务：i) 请求批处理，将相邻请求合并以充分利用GPU的计算能力，ii) GPU内存优化，改善访问模式以减少GPU内存中的无效事务，iii) 并行内核计算，允许多个CUDA内核同时处理矩阵计算。总的来说，这些技术的优化实际上使单台机器的QPS（每秒查询数）能力翻倍。在线服务DIN也受益于此。
(DIEN)![[Pasted image 20251208175831.png#center|]]![[Pasted image 20251208175850.png#center|]]翻译: 值得注意的是，DIEN的在线服务对商业系统来说是一个巨大的挑战。在线系统在我们的展示广告系统中承载着非常高的流量，在流量峰值时，每秒为超过100万用户提供服务。为了保持低延迟和高吞吐量，我们部署了几种重要技术来提高服务性能：i) 元素并行 GRU 和内核融合（Wang, Lin, and Yi 2010），我们融合尽可能多的独立内核。此外，GRU的隐藏状态的每个元素都可以并行计算。ii) 批处理：来自不同用户的相邻请求合并为一个批次，以利用GPU的优势。iii) 使用火箭发射法模型压缩（Zhou et al. 2018b）：我们使用（Zhou et al. 2018b, DIN）中提出的方法来训练一个轻量级网络，该网络体积较小，但性能接近更深层和更复杂的网络。例如，借助火箭发射法，可以将GRU隐藏状态的维度从108压缩到32。在这些技术的帮助下，DIEN服务的延迟可以从38.2毫秒减少到6.6毫秒，每个工作节点的QPS（每秒查询数）容量可以提高到360。
## 3. LLM VS GR
本问题旨在理解如何用LLM的方式理解生成式推荐，而非局限于现有的GR范式
1. 策略分布
	- LLM: 以现有token序列为状态，预测下一个token的概率（输出每个token的logits值然后softmax得到概率值，再使用categorical distribution抽样）
	- GR: 以过去的交互序列为状态，预测下一个/下一组item（输出每个/每组item的logits值然后softmax得到概率值，再使用categorical distribution抽样）
	- 对比: 可以看到，对于GR来说，如果只是预测下一个item，似乎可以模仿LLM的方式，但是对于预测一组item（slate recommendation），那么action space将是非常庞大的离散空间，就算是精排之后拿到几千或者几百个item，它们的组合也是不可估量的，一些RL的工作采用hyper action的方式，输出连续的hyper action向量，再通过scoring function映射为effective action
2. 奖励信号
	- LLM: 以问答场景为例，给定问题，需要自回归生成整个回答才能得到用户提供的奖励，这本质上是一个稀疏奖励的问题，可以理解为中间的token奖励为0，最后一个token奖励赋值；或者理解为每个token的奖励是答案奖励的平均（奖励除以答案序列的长度）
	- GR: 无论是single recommendation还是slate recommendation，都会在输出一个/一组token之后立刻获得来自用户的反馈（在特定的优化目标中可以理解为奖励），当然也存在一些延迟反馈（比如下一次会话开始才能得到的用户返回时间）
	- 对比: 可以看到，LLM的RL步骤需要考虑一种特殊的稀疏奖励的情况，而且对于具体的token对于最终奖励的贡献（信用分配问题），还有很多可以改进的空间；而GR的奖励信号看似是非常稠密的，但是存在多种反馈信号，对于不同的业务目标，可能对应非常复杂的奖励设计，如果要使用RL学习GR的策略函数，不太能参考LLM的经验，更应该关注奖励函数的设计以及RL本身
3. 状态转移函数
	- LLM: 以问答场景为例，状态转移函数是确定的，由现有的token和模型预测的token组成下一时刻的状态
	- GR: 不能完全使用用户点击的序列作为序列数据，点击数据不能作为用户状态，而且状态转移函数是不确定的
4. MDP
	- LLM: 以生成一个完整的回答为一个episode
	- GR: 不太好定义episode的结束，如果利用会话结束作为done信号，也不好使用GAE估计优势值
5. 行为的概率分布
	- LLM: LLM中的用户行为其实只考虑了用户对于答案的反馈（奖励信号），通常使用奖励模型进行刻画
	- GR: GR中的用户行为种类繁多，从时间的角度可以分为即时的和延迟，从随机变量的角度可以分为二分类、连续、计数等
	- 对比: GR如果要用统一的奖励函数去评估，则需要非常复杂的奖励设计
6. 数据
	- LLM: LLM的数据包括符合语法的语料以及用户的反馈
	- GR: GR的数据包括用户特征、item特征和用户与item的交互历史
	- 对比: LLM的数据更多是符合句法规范的序列数据，但是GR的数据（尤其是交互历史数据）可能混杂了很多噪声，比如一个用户是否点击一个商品可能是因为感兴趣（内生），也可能是受到了外界因素的影响（外生），因此GR的序列建模可能不仅仅是Transformer架构就能解决的问题
7. 解释性
	- LLM: LLM的输出是language，是可以被人类理解的序列
	- GR: GR的输出是一个/一组item，尽管可以从多样性、用户的兴趣等角度分析推荐策略，但是对于推荐结果，其实很难像LLM的输出那样能够直接比较不同的输出
	- 对比: GR的可解释性比LLM更难，只能从用户对于推荐item的反馈上评估推荐的好坏
8. 安全问题
	- LLM: 人类会诱导LLM产生不安全的回答(比如让grandma提供炸弹制作方法)
	- GR: 对于推荐系统来说，会不会在引入生成式范式之后也会存在这种问题呢？
## 4. 常用指标
可以看[生成式推荐中的常见评估指标 - 小红书](https://www.xiaohongshu.com/explore/687e34c1000000000d01890a?app_platform=android&ignoreEngage=true&app_version=9.13.1&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CBkjWXK6v6wRhNuafiuLrHYZQhTvSFIzrGUnu3FIVJPtg=&author_share=1&xhsshare=&shareRedId=ODw1Q0hKNTk2NzUyOTgwNjY6OTc4PUk5&apptime=1766656828&share_id=81248cb269a448a5987d23a04900a6a5&share_channel=wechat)[【基础】推荐系统常用评价指标Recall、NDCG、AUC、GAUC-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/2111158)[算法面经系列：手撕AUC和损失函数 - 知乎](https://zhuanlan.zhihu.com/p/845511711)
(以下内容来自Gemini 3.0 Pro)
1. **评分预测指标:** RMSE, MAE
2. **Top-N排序指标:** Precision@K, Recall@K, MAP (Mean Average Precision), NDCG (Normalized Discounted Cumulative Gain), MRR (Mean Reciprocal Rank)
3. **非精度指标:** 覆盖率 (Coverage), 多样性 (Diversity), 新颖性 (Novelty)
建议: 
- 如果是**电商/短视频**场景：**NDCG** 和 **Recall** 是最重要的，前者看重排序，后者看重召回能力。
- 如果是**广告 CTR 预估**：**AUC** (Area Under Curve) 和 **LogLoss** 是绝对核心。
- 如果是**做研究**：通常需要同时汇报 Precision, Recall, NDCG (at K=10, 20等)。
## 5. DIN & DIEN & SIM
### 5.1 适用阶段
注意DIN、DIEN和SIM都需要候选item，但是双塔模型（召回）、三塔模型（粗排）中的用户塔没有候选item的信息，需要根据候选item实时加权last-n作为新的用户特征。DIN计算复杂度高，适用于精排阶段，可以用于用户特征提取层。
### 5.2 损失函数
由于是点击率预测的场景，因此最后接MLP输出点击率预测，适用二元交叉熵损失。
## 6. 不同的推荐场景
主要有短视频、电商、种草社区、长视频
1. 短视频关注用户留存，只有持续的使用行为才能给平台带来稳定的收益，用户行为数据分为显式反馈和隐式反馈，更受用户兴趣驱动，收益来自广告、直播
2. 电商关注购物旅程，用户行为数据涵盖整个购物旅程的曝光-点击-加购-下单-支付-评价等，比起其他平台，在电商场景中用户的查询具有强烈的意图，是一种非常重要的信息，收益来自商品交易
3. 种草社区关注社区氛围，用户行为数据中的收藏/保存代表用户有强烈意向或作为工具书使用，收益来自广告
4. 长视频关注用户观看体验，用户行为数据往往不会像短视频一样有特别长的观看序列，但是有更多观看活动的细节（如拖拽进度条），收益来自订阅制服务和PGC（购买版权的内容）。

(以下内容来自Gemini 3.0 Pro)
### 1. 短视频场景 (如：抖音/TikTok, 快手)
这是目前流量最大、交互最高频的场景，其核心逻辑是“杀时间”与“沉浸式消费”**。
- **用户行为数据 (User Behavior Data):**
    - **隐式反馈（极其重要）：** 完播率（Completion Rate）、播放时长占比、复播（Re-watch）、快速滑走（Negative feedback）、停留时长。
    - **显式反馈：** 点赞、关注、转发、评论、下载、进入主页。
    - **特征：** 数据极度稠密，反馈延迟极低（几秒钟就是一个样本）。用户的决策成本极低（不喜欢就滑走）。
- **平台核心指标 (Key Metrics):**
    - **用户增长与留存：** DAU (日活)、**用户留存率 (Retention Rate)**、**人均使用时长 (Time Spent)**。这是基本盘。
    - **变现指标：** 广告加载率 (Ad Load)、广告eCPM、直播打赏金额、直播带货GMV。
    - **体验指标：** 视频首屏加载时间、多样性（防止信息茧房导致用户疲劳）。
**核心逻辑：** 通过最大化用户的**沉浸时长**来创造广告位库存。推荐系统需要平衡“即时满足”（高CTR视频）与“长期留存”（高质量/有价值视频）。
### 2. 电商场景 (如：淘宝/天猫, 亚马逊, 京东)
这是离钱最近的场景，核心逻辑是“流量分发效率”与“成交转化”**。
- **用户行为数据 (User Behavior Data):**
    - **全链路漏斗数据：** 曝光(Impression) -> 点击(Click) -> 加购(Add-to-cart) / 收藏(Favorite) -> 下单(Order) -> 支付(Pay) -> 退货/评价。
    - **搜索数据：** 强意图的Search Query是电商最宝贵的数据。
    - **特征：** 数据相对稀疏（相比短视频，用户不会每天买几十单），决策周期长，决策成本高（涉及金钱）。
- **平台核心指标 (Key Metrics):**
    - **交易指标（北极星）：** **GMV (Gross Merchandise Value)**。
    - **效率指标：** **CVR (转化率)**、CTR (点击率)、UV价值 (每个用户带来的收益)。
    - **生态指标：** 退货率、复购率、客单价 (AOV)。
**核心逻辑：** 推荐不仅仅是让用户点进去，更要预测用户“买得起”且“愿意买”。系统往往需要在CTR（吸引眼球）和CVR（实际购买）之间做多目标平衡（ESMM模型等）。
### 3. 内容分享/种草社区 (如：小红书, Instagram)
这是一个介于“逛街”和“看视频”之间的场景，核心逻辑是**“生活方式认同”与“消费决策辅助”**。
- **用户行为数据 (User Behavior Data):**
    - **收藏/保存 (Save/Collect)：** 这是该场景**最特殊且高价值**的信号，代表用户有强烈意向或作为工具书使用。
    - **搜索与浏览：** “搜索-点击-深度浏览”的链路。
    - **互动：** 评论区的互动往往比点赞更有价值，代表社区氛围。
    - **特征：** 图文与视频混排，用户兼具“杀时间”和“找答案”的双重心理。
- **平台核心指标 (Key Metrics):**
    - **社区粘性：** **互动率 (Engagement Rate)**，特别是收藏率和评论率。
    - **搜索渗透率：** 多少用户会主动搜索（体现工具属性）。
    - **种草转化：** 后链路的搜索行为（看了笔记后去搜商品）或站外溢出价值。
**核心逻辑：** 维持**社区调性**至关重要。如果只推高CTR的标题党内容，会破坏社区氛围导致用户流失。因此，推荐系统往往会引入“内容质量分”和“发布者信誉分”进行打压或扶持。
### 4. 长视频/流媒体 (如：Bilibili, Netflix, 爱奇艺)
核心逻辑是“会员订阅”与“IP消费”。
- **用户行为数据 (User Behavior Data):**
    - **长时间观看：** 这里的播放时长是分钟/小时级的。
    - **拖拽进度条：** 跳过片头、倍速播放、空降（seek）。
    - **追剧行为：** 连续观看同一系列。
    - **特征：** 物品数量（Item）相对较少，但制作成本极高。用户的选择非常慎重。
- **平台核心指标 (Key Metrics):**
    - **会员价值：** **LTV (Life Time Value)**、会员续费率、退订率 (Churn Rate)。
    - **内容利用率：** 独家内容的VV (Video Views)，长尾内容的分发效率（降低版权浪费）。

# 大模型
## 1. 大模型为什么使用PPO进行训练，而不是其他确定性策略的算法(DDPG, TD3)
(以下内容来自Gemini3.0 Pro)
1. 动作空间
   DDPG, TD3等确定性策略方法适合处理连续动作空间，而LLM的动作空间是离散空间，PPO适合处理离散空间，而且这与微调阶段的结构一致
2. 随机性 VS 确定性
   LLM需要随机性策略需要保持一定的多样性
3. 微调的稳定性 (这个感觉说得不太好)
   PPO的核心机制（Clipping）天然就是为了限制策略更新步长，防止策略崩塌（Policy Collapse）。这使得它在微调这种巨型模型时非常稳定。DDPG是 Off-policy 算法，利用 Replay Buffer 极其激进地利用数据。在 LLM 这种高维、稀疏奖励的环境下，Off-policy 算法很容易导致 Q 值估计发散（Overestimation bias），进而导致模型生成乱码。
4. 显存与计算效率
   Off-Policy需要维护巨大的经验回放数组，在 LLM 语境下，一个 Transition $(s, a, r, s')$ 极其巨大。State $s$ 包含了极长的 Context（可能有 4k 或 32k tokens），存储数百万条这样的数据对显存和内存是毁灭性的打击。
## 2. RMSNorm
考虑到Layer Norm需要计算均值和方差，计算量较大，RMSNorm仅使用均方根(root mean square)归一化$$\text{RMS}(x)=\sqrt{\dfrac{1}{d}\sum\limits_{i=1}^dx_i^2}\quad \rightarrow\quad\hat{x}=\dfrac{x}{\text{RMS}(x)+\epsilon}\quad\rightarrow\quad y=\gamma\hat{x}$$其中$\gamma$是和$x$维度相同的可学习的参数向量。
## 3. 束搜索
[束搜索（Beam Search）-CSDN博客](https://blog.csdn.net/u013172930/article/details/145500769)
# 智力题
以下内容来自小红书、Gemini 3.0 pro
### 第一类：概率与统计类 (最核心)
这类题目与算法岗工作最相关，主要考察数学期望和几何概率。
#### 1. 棍子折成三段能组成三角形的概率
题目：一根木棒，将其随机折成3段，这3段能组成一个三角形的概率是多少？
解答：$1/4$
解析：这是一个经典的几何概率问题。
设棍子总长为1，折断点为$x, y$ (假设$x < y$)。三段长度分别为 $x$, $y-x$, $1-y$。
组成三角形的条件是“任意两边之和大于第三边”，即**三段中每一段的长度都必须小于总长的一半**（$0.5$）。
我们在平面直角坐标系画出可行域（总面积为三角形），满足条件的区域面积占总可行域的 $1/4$。
如下图所示，绿色表示$0<x<0.5$，紫色表示$0<y-x<0.5$，青色表示$0<1-y<0.5$![[Pasted image 20260104103356.png#center|]]
#### 2. 两人见面的概率
题目：两人约定在 12:00 到 13:00 之间见面，每个人都会等待 15 分钟，如果对方没来就离开。求两人能见上面的概率。
解答：$7/16$
解析：
这也是几何概型。设两人到达时间分别为 $x$ 和 $y$ ($0 \le x, y \le 60$)。
见面的条件是 $|x - y| \le 15$。
画出 $60 \times 60$ 的正方形，减去两个不能见面的三角形区域（即 $|x-y| > 15$ 的部分），剩下的面积就是能见面的概率。
不能见面的区域是两个边长为 45 的直角三角形。
概率 $= 1 - (\frac{45}{60})^2 = 1 - (\frac{3}{4})^2 = 1 - \frac{9}{16} = \frac{7}{16}$。
以下图为例，绿色表示$\vert x-y\vert \leq 15$，紫色表示$0<x<60$，青色表示$0<y<60$![[Pasted image 20260104103939.png#center|]]
#### 3. 重男轻女村庄的男女比例
题目：一个国家的人都想要男孩。如果生了女孩，就继续生，直到生出男孩为止。假设生男生女概率各为 50%。问长期来看，男女比例是多少？
解答：1:1
解析：
这是一个期望值陷阱题。
- 第一胎：$1/2$ 是男孩（停止），$1/2$ 是女孩（继续）。
- 第二胎：$1/4$ 是男孩，$1/4$ 是女孩。
- ...
    平均每家会生几个男孩？答：肯定只有 1 个（因为生到男孩就停了）。
    平均每家会生几个女孩？期望值 $E = 1 \cdot (1/2) + 1 \cdot (1/4) + 1 \cdot (1/8) ... = \text{lim}_{n\to\infty}\dfrac{1}{2}\dfrac{1-(1/2)^n}{1-1/2}=1$。
    所以平均每户人家：1 男 1 女。比例为 1:1。
#### 4. 硬币问题

### 第二类：逻辑推理与最优解 (常考大厂)
这类题目考察你对复杂流程的优化能力（类似算法复杂度分析）。
#### 4. 64匹马找最快的4匹
题目：有64匹马，8条赛道。没有计时器，只能通过比赛知道名次。问最少赛多少场，能选出最快的4匹马？
解答：11 场
解析：
1. **分组赛 (8场)**：64匹分8组，每组跑一次。淘汰每组后4名（因为每组前4才有可能是总排名前4）。
2. **王中王 (1场)**：取这8组的第一名跑一场。
    - 设第一名为A1组，第二名为B1组...以此类推。
    - 后4名的小组（E1, F1, G1, H1）全员淘汰（因为E1已经是第五快的小组第一了，不可能进前4）。
3. **确定最终名额 (2场)**：
    - 第一名肯定是 A1（不用跑）。
    - 剩下的3个名额在以下马匹中产生：A2, A3, A4, B1, B2, B3, C1, C2, D1（共9匹，加上前面的逻辑剔除，这里需要仔细推导）。（注意A1>B1>C1>D1，所以A组中取3，B组能取3，C组只能取2，D组只能取1）
    - 这步比较复杂，通常策略是挑选最有希望的几匹加赛一场，再视情况加赛一场。总共通常是 8+1+2 = 11场
    - 比如前八匹马决出三匹马，如果三匹马中没有B1和C1，或者B1和C1出现在第三匹马，则D1肯定不在三匹马中
    - 如果正好是B1、C1是前两匹马，那么需要第三匹马和D1比谁速度快
#### 5. 烧绳子计时
题目：有两根粗细不均匀的绳子，烧完每一根都需要1个小时。如何用它们来衡量45分钟？
解答：
1. 点燃绳子 A 的两头，同时点燃绳子 B 的一头。
2. 当绳子 A 烧完时（过去了30分钟），绳子 B 还剩一半（虽然不均匀，但时间剩一半）。
3. 此时立刻点燃绳子 B 的另一头。
4. 绳子 B 剩下的部分会以双倍速度燃烧，即 15 分钟烧完。
5. 30 + 15 = 45 分钟。
#### 6. 称球问题 (经典二分/三分思想)
题目：有8个球，其中1个比其他的重，给一个天平，最少称几次能找出那个球？
解答：2 次
解析：利用三分法（信息量最大化）。
1. 将球分为 3, 3, 2 三组。
2. **第一次**：称量两组 3 个的球。
    - **平**：重的球在剩下的 2 个里。再称一次即可。
    - **不平**：重的球在重的那 3 个里。从这 3 个里任选 2 个称。
        - 如果不平，重的那个就是。
        - 如果平，没称的那个就是。
### 第三类：博弈论 (Game Theory)
推荐系统本质是平台与用户的博弈，这类题目考察逆向思维。
#### 7. 拿硬币/石子游戏
题目：有 100 个石子，你和对手轮流拿，每次最少拿 1 个，最多拿 5 个。最后拿光石子的人获胜。你先手，怎么做才能必胜？
解答：先拿 4 个
解析：
这是一个巴什博弈 (Bash Game) 问题。关键数字是 $1+5=6$。
你想赢，就要把剩下的石子数控制为 6 的倍数，让对手面对绝望。
$100 \mod 6 = 4$。
你先拿 4 个，剩 96 个（6的倍数）。
之后无论对手拿 $x$ 个，你就拿 $6-x$ 个。每一轮你们俩加起来都拿走 6 个，最后肯定是你拿走最后一组。
#### 8. 海盗分金币
题目：5个海盗（A, B, C, D, E，等级由高到低）分100个金币。由等级最高的人提出方案，大家表决。如果同意人数 $\ge 50\%$，方案通过；否则提出者被扔进海里，换下一位提方案。A 应该怎么分，才能使自己收益最大且保命？
解答：A: 97, B: 0, C: 1, D: 2, E: 0 或类似变种。
解析：
使用逆向归纳法（倒着推）。
- 如果只剩 D, E：D 必须给自己 100，E 没得选（D自己就占50%）。E 收益 0。
- 如果是 C, D, E：C 只要给 E 1个金币（比D给他的0多），E 就会支持 C。C 拿 99，D 拿 0，E 拿 1。
- 如果是 B, C, D, E：B 需要 2 票。他给 D 1个金币（比C给的0多），D 会支持。B 拿 99，C 0，D 1，E 0。
- 如果是 A, B, C, D, E：A 需要 3 票（含自己）。
    - C 在 B 的方案里拿 0，A 给 C 1个。
    - E 在 B 的方案里拿 0 (或 D 在 B 的方案里拿 1，A 给 D 2个)。
    - 通常最优是拉拢 C 和 D（或 E）。
    - 方案：A 分 97，C 分 1，D分 2（或者给D 1，E 2 等，取决于细微假设，但核心是利用每个人的“次优解”来压价）。
### 第四类：数据采样与算法结合
这是推荐算法面试特有的“智力题”，其实是算法题。
#### 9. 蓄水池采样 (Reservoir Sampling)
题目：给你一个无限的数据流（不知道总数 $N$），如何从中随机抽取 $k$ 个元素，使得每个元素被选中的概率相等？
解答：
1. 先将前 $k$ 个元素放入“蓄水池”。
2. 对于第 $i$ ($i > k$) 个元素，以 $k/i$ 的概率决定是否把它替换进蓄水池。
3. 如果决定替换，随机从蓄水池的 $k$ 个位置中选一个替换掉。
    证明：每个元素最终保留的概率都是 $k/N$。
详细证明：考虑元素x，第m步考虑是否加入池子，如果m<=k，则加入池子的概率为1，否则为k/m，首先考虑m<=k的情况，那么第k+1步x被留下的概率等于1-(1/k)* (k/(k+1))=k/(k+1)，进一步有k+2步被留下的概率有k/(k+1)* (k+1)/(k+2)，因此有x被留下的概率为$$1\cdot\dfrac{k}{k+1}\cdot\dfrac{k+1}{k+2}\cdots=\dfrac{k}{N},$$再考虑$m>k$的情况，则m步元素加入池子的概率为k/m，m+1步在池子的概率为(k/m) * (m/(m+1))，进而有x被留下的概率为$$\dfrac{k}{m}\cdot\dfrac{m}{m+1}\cdots=\dfrac{k}{N}$$
#### 10. Rand5() 实现 Rand7()
题目：给定一个函数 Rand5() 可以等概率生成 1-5 的整数，请用它实现 Rand7()。
解答：拒绝采样 (Rejection Sampling)
1. $5 \times (\text{Rand5}() - 1) + \text{Rand5}()$ 可以生成 1 到 25 的均匀整数。（假设乘以1，则第一个抽1，第二个抽2，和第一个抽2，第二个抽1对应的都是2）
2. 如果生成的数是 1-21，则返回 $\text{result} \% 7 + 1$。
3. 如果生成的数是 22-25，丢弃重来。
# 其他
## 1. 常用的Linux指令
- watch -n 0.1 nvidia-smi 查看显卡
- screen -S name 创建name窗口 
- screen -ls 列出窗口列表
- screen -r name 进入name窗口
- screen -S name -X quit 删除name窗口
- bash x.sh 运行x.sh脚本

## 2. 为什么32位二进制的最小值是$-2^{31}$,最大值是$2^{31}-1$
由于32位二进制数的最高位用作符号位(0表示正数,1表示负数),考虑到考虑到全0的32位整数表示0,所以正数的最大值是$2^{31}-1$;而最高位为1,其余为0的32位整数表示-1,所以负数的最小值是$-2^{31}$.

# 日常实习-岗位及岗位要求
## 1. 字节跳动
### 1.1 推荐算法实习生-国际电商 (北京)
![[Pasted image 20251206121254.png]]
### 1.2 推荐算法实习生-Data AML (杭州)
![[Pasted image 20251206121731.png]]
### 1.3 推荐算法实习生-Data AML
![[Pasted image 20251206122555.png]]
### 1.4 推荐算法实习生-基础推荐 (北京)
![[Pasted image 20251206121902.png]]
### 1.5 推荐算法实习生-国际化短视频直播 (北京)
![[Pasted image 20251206122502.png]]
## 2. 快手
### 2.1 推荐算法实习生-【电商】(北京)
![[Pasted image 20251206123712.png]]
### 2.2 电商推荐算法实习生 - 流量策略方向 (北京)
![[Pasted image 20251206123822.png]]
### 2.3 广告生态推荐算法实习生 -【商业化】
![[Pasted image 20251206124123.png]]
### 2.4 推荐模型算法实习生-【生活服务】(北京)
![[Pasted image 20251206124501.png]]

### 2.5 推荐算法实习生-【主APP】(北京)
![[Pasted image 20251206124538.png]]
### 2.6 推荐算法实习生-【内容增长算法部】 (北京)
![[Pasted image 20251206124752.png]]

### 2.7 推荐算法实习生-【创新体验中心】(北京)
![[Pasted image 20251206124846.png]]
## 3. 阿里
### 3.1 阿里妈妈-机制策略算法实习生 (淘天/研究型实习生/北京)
![[Pasted image 20251206125302.png]]
### 3.2 研究型实习生-阿里妈妈-多目标推荐算法工程师 (淘天/北京)
![[Pasted image 20251206125449.png]]
### 3.3 研究型实习生-搜推智能产品-认知推荐算法工程师 (淘天/北京)
![[Pasted image 20251206125625.png]]
### 3.4 算法技术-生成式混排-算法工程师实习生 (淘天/研究型实习生/杭州)
![[Pasted image 20251206130053.png]]
### 3.5 算法工程师实习生 (淘天/日常实习生/北京)
![[Pasted image 20251206130246.png]]
## 4. 腾讯
### 4.1 技术研究-机器学习方向
![[Pasted image 20251206213926.png]]![[Pasted image 20251206213938.png]]
### 4.2 技术研究-数据科学方向
![[Pasted image 20251206214124.png]]![[Pasted image 20251206214134.png]]
### 4.3 技术研究-推荐算法方向
![[Pasted image 20251206214223.png]]![[Pasted image 20251206214234.png]]
## 5. 小红书
### 5.1 基础模型算法实习生
![[Pasted image 20251206214656.png]]
### 5.2 广告算法实习生-行业方向
![[Pasted image 20251206215117.png]]
### 5.3 电商广告算法实习生
![[Pasted image 20251206215212.png]]
### 5.4 搜索广告算法实习生
![[Pasted image 20251206215245.png]]
### 5.5 推荐算法实习生-社区技术
![[Pasted image 20251206215402.png]]
## 6. 美团
### 6.1 外卖商品-搜索推荐算法工程师（实习/北京）
![[Pasted image 20251206215742.png]]
### 6.2 美团-首页推荐-算法实习生 (北京)
![[Pasted image 20251206215938.png]]
### 6.3 搜推营销-拼好饭推荐算法实习生
![[Pasted image 20251206220149.png]]
## 7. 京东
### 7.1 算法工程师-机器学习
![[Pasted image 20251206221035.png]]
### 7.2 推荐算法实习生（北京/BOSS直聘）
![[Pasted image 20251215124731.png]]
### 7.3 推荐算法实习生（深圳/BOSS直聘）
![[Pasted image 20251215125651.png]]
## 8. 哔哩哔哩
### 8.1 算法实习生（推荐算法/上海）
![[Pasted image 20251206222232.png]]
## 9. 得物
### 9.1 推荐算法实习生（上海-BOSS直聘）
![[Pasted image 20251215124441.png]]
## 10. 智谱华章
### 10.1 推荐算法实习生（AMiner）
![[Pasted image 20251215124516.png]]
## 11. 小米
### 11.1 生成式搜推大模型算法实习生（北京）
![[Pasted image 20251215125525.png]]


## 其他信息
### 大厂推荐核心团队
![[37ce5772bbd15888db25419095b12d96 1.jpg#center|]]
### 大厂实习薪资待遇
![[ab99fa547acaddca3bf8c7fa8bf0d70f.jpg#center|]]![[0a34af97d49332d642bafcf5a7c17604.jpg#center|]]![[0a34af97d49332d642bafcf5a7c17604 1.jpg#center|]]![[d86033fde1ecc1d8269b4fd74a2ceeee.jpg#center|]]![[8732d31b07e57e20c0b421e739bb587f.jpg#center|]]