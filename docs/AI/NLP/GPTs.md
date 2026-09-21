# GPTs: ChatGPT, GPT-4, and etc

!!! tip

    - GPT 系列真正改变 NLP 的地方，不只是参数变大，而是把**语言建模、指令遵循、对齐、推理时计算、多模态和智能体**接到了一条连续的技术路线里。
    - 一个可用的 ChatGPT 类模型通常不是单靠预训练得到的，而是经历：
        - **Pre-training $\rightarrow$ Supervised Fine-tuning $\rightarrow$ RLHF / RL $\rightarrow$ Alignment**

---

## 1. From Turing Test to GPT

### 1.1 Turing Test

图灵测试关注的问题是：**如果测试者无法稳定区分机器和人，那么机器是否可以被认为具有智能？** 

- 图灵提出的设想中，人类通过文本向被测试对象提问；
- 如果机器的回答足以混淆测试者，就可以被认为通过了测试。

!!! info

    图灵测试本身并不等价于“真正理解”，但它把人工智能问题转化成了一个可观察的行为问题：**机器能否在语言交互中表现出足够像人的智能行为**。

### 1.2 2013-2023: From Word Vectors to GPT

GPT 的出现不是凭空跳出来的，它接在前面几代 NLP 技术之后：

1. **Word Embedding**
    - 用连续向量表示词义，典型方法包括 CBOW 和 Skip-gram
    - 核心思想来自分布式假设：一个词的含义由它出现的上下文决定
2. **RNN / LSTM**
    - 用隐藏状态处理序列，能根据前文更新当前表示
    - 但长距离依赖和并行训练效率仍然受限
3. **Transformer**
    - 用 Self-attention 替代递归计算，使大规模并行训练成为可能
    - 后续分化出 BERT 和 GPT 两条重要路线

### 1.3 BERT vs GPT

Transformer 出现后，NLP 中出现了两个很有代表性的“游戏”：

| 路线 | 训练任务 | 架构倾向 | 应用范式 | 典型能力 |
| ---- | ---- | ---- | ---- | ---- |
| **BERT** | 填词游戏 | Encoder-only | 预训练后微调 | 句子理解、分类、抽取 |
| **GPT** | 接龙游戏 | Decoder-only | 语境学习 / 生成 | 文本生成、对话、推理 |

<div style="text-align: center"><img src="images/image-126.png" width="85%"></div>

GPT 的语言模型目标可以写成：

$$
P(x_1, x_2, \dots, x_T)=\prod_{t=1}^{T}P(x_t|x_{<t})
$$

- 目标看起来简单，但当模型规模、数据规模和计算规模足够大时，会出现非常强的通用生成能力

### 1.4 In-context Learning

不更新模型的参数，只通过 prompt 中的上下文和示例来适应任务。

<div style="text-align: center"><img src="images/image-127.png" width="85%"></div>

- **Zero-shot Learning**：不给示例，直接描述任务
- **One-shot Learning**：给一个示例
- **Few-shot Learning**：给少量示例

GPT-3 的重要意义在于：它展示了大模型可以通过上下文示例临时“学会”任务，而不一定需要为每个任务重新训练。

### 1.5 Scaling Laws and Emergent Ability

- ==Scaling Laws（伸缩法则）==：
  模型性能通常会随着参数量、训练数据和计算量增加而提升。
- ==Emergent Ability（涌现能力）==：
  当模型参数、数据规模、计算开销增大到一定规模时，模型的特定能力（例如，举一反三、数学证明、跨域迁移的能力） 出现显著增强

!!! warning

    涌现能力并不意味着模型已经具备人类意义上的理解。更保守的理解是：足够大的模型在足够多数据上训练后，某些行为能力开始在评测中显著出现。

---

## 2. LLM Training Pipeline

!!! abstract "Three Stages"

    大模型训练可以粗略分为三个阶段：

    | 阶段                                | 输入输出形式                                 | 目标                | 得到的模型                 |
    | --------------------------------- | -------------------------------------- | ----------------- | --------------------- |
    | **Pre-training**                  | `人工智` $\rightarrow$ `能`                | 学习语言规律和世界知识       | Base Model            |
    | **Instruction Fine-tuning / SFT** | `USER: 你是谁? AI:` $\rightarrow$ `我是...` | 学会按指令回答           | Instruct / Chat Model |
    | **RLHF / RL**                     | 多个候选回答排序或打分                            | 更符合人类偏好、任务目标和安全规范 | Aligned Model         |

### 2.1 Pre-training

预训练阶段的核心任务是：用海量无标注文本训练 next-token prediction

- 以盘古大模型为例，预训练要同时解决四类问题：

<div style="text-align: center"><img src="images/image-128.png" width="80%"></div>

#### 2.1.1 Data Cleaning

常见清洗步骤：

- 删除中文比例过低的文章；删除过短文本；过滤特殊符号和广告；去重；繁体转简体；去除网页导航、菜单、标题等噪声；敏感词和敏感内容过滤；用小模型对数据质量做批量验证

!!! tip

    数据清洗不是预处理的小配角。对于 LLM 来说，训练数据本身就是“教材”；教材里噪声越多，模型越容易学到奇怪的格式、偏见和无意义模式。

#### 2.1.2 Distributed Training Challenges

超大模型训练会遇到四堵墙：

1. **内存墙**
    - 参数、梯度、优化器状态和激活值都会占显存
    - 200B 级参数模型训练可能需要 TB 级显存
2. **性能墙**
    - 模型切分到集群后，通信成为主要瓶颈
3. **效率墙**
    - 分布式并行代码复杂，难以手工维护
4. **调优墙**
    - 千卡训练要处理故障、性能波动、通信拓扑和 checkpoint

常见解决方向：

- 多维混合并行：数据并行、模型并行、流水线并行、优化器并行
- 重计算：牺牲一部分计算换取更低激活显存
- 通信融合：减少同步次数
- 快速故障恢复：定期保存 checkpoint，故障后重调度资源

!!! bug "Pretrained Models Are Not Enough"

    - 预训练模型只学会了“接着写”，并不保证能当助手。
    - 例如:
        - 用户问：`USER: 你是谁?`
        - Base model 可能只是继续生成类似网页、问答数据或乱码风格的文本；
        - Chat model 则需要回答：`AI: 我是一个人工智能助手...`
    - 差别来自 post-training

---

### 2.2 Supervised Fine-tuning

#### 2.2.1 Post-training (SFT)

==Supervised Fine-tuning (SFT)== ：

- 使用人工或模型生成的指令数据，让模型学习“看到问题后应该如何回答”。
- SFT 的目标不是重新教模型语言，而是把 base model 的语言能力组织成更适合交互的形式。

<div style="text-align: center"><img src="images/image-129.png" width="80%"></div>

#### 2.2.2 Quality Is All You Need

指令微调中，数据质量往往比数据数量更关键
一些代表性观点：

- **LIMA**：<u>Less Is More for Alignment</u>，少量高质量样本也能显著提升对齐效果
- **LLaMA2**：<u>Quality is all you need</u>，强调高质量 SFT 和偏好数据
- **Ruozhiba (弱智吧) 数据**：用非常规问答训练模型处理反直觉、脑筋急转弯式问题

#### 2.2.3 How to prepare your SFT data

==Knowledge Distillation==：很多开源指令模型会用更强的模型生成训练数据

<div style="text-align: center"><img src="images/image-130.png" width="70%"></div>

| 模型 / 数据 | Student              | Teacher | 数据量 | 成本      |
| ------- | -------------------- | ------- | --- | ------- |
| Alpaca  | LLaMA1-7B-base       | ChatGPT | 52k | 约 \$100 |
| Vicuna  | LLaMA1-7B-base       | ChatGPT | 70k | 约 \$140 |
| Sky-T1  | Qwen2.5-32B-Instruct | QwQ     | 17k | 约 \$450 |
| s1      | Qwen2.5-32B-Instruct | Gemini  | 1k  | 小于 \$50 |
SFT 数据不仅需要答案，还需要**问题来源**。

- 常见来源：人工编写任务指令、真实用户日志、公开 QA 数据集、从网页或文档中抽取问题、非指令式文本改造成续写或问答、让模型自生成问题，再由强模型回答
- ==Non-instructional Fine-tuning==：不一定非要显式指令，<u>普通文本续写</u>也可以帮助模型适应某种领域或风格

<div style="text-align: center"><img src="images/image-131.png" width="60%"></div>

---

### 2.3 RLHF

**RLHF: Reinforcement Learning from Human Feedback**

!!! info "Why ChatGPT Became a Product"

    <div style="text-align: center"><img src="images/image-132.png" width="70%"></div>

    ChatGPT 成为现象级产品，不只是因为语言模型强，还因为它经过了指令微调和人类反馈强化学习

#### 2.3.1 RLHF Pipeline

<div style="text-align: center"><img src="images/image-133.png" width="70%"></div>

**RLHF (Reinforcement Learning from Human Feedback)** 通常包含三步：

1. **SFT**：用人工标注的指令数据训练初始助手模型
2. **Reward Model**
    - 给同一个问题生成多个候选回答
    - 人类比较这些回答的好坏
    - 训练一个奖励模型预测人类偏好
3. **RL Optimization**
    - 用 PPO 等强化学习算法更新语言模型
    - 目标是最大化 reward，同时避免偏离原模型太远

#### 2.3.2 Policy Gradient

强化学习中策略 $\pi_\theta(a|s)$ 代表在状态 $s$ 下选择动作 $a$ 的概率，语言模型也可以进行类比：

- **状态**：当前 prompt 和已生成 token
- **动作**：下一个 token
- **轨迹**：完整回答
- **奖励**：人类偏好 / reward model 分数

**策略梯度目标**：

$$
J(\theta)=\mathbb{E}_{\tau \sim \pi_\theta}[R(\tau)]
$$

- 更新方向大致是<u>让高奖励回答的生成概率上升，低奖励回答的生成概率下降</u>。

!!! bug "Problem of Policy Gradient"

    1. **样本效率低**
        - 每次策略变化后，旧轨迹很快变得不适用
        - 一次更新后，旧数据就要被丢弃，训练速度慢，成本高
    2. **更新不稳定**
        - 步子太大可能让策略突然变差
        - 下一批数据又来自坏策略，会继续恶化

#### 2.3.3 PPO

==PPO (Proximal Policy Optimization)== 是 RLHF 中常见的优化算法

- 目标：**在有限的数据下实现高效利用，并保证学习性能的稳定**
- 解决思路：
    1. **Mini-batch training**：使用 mini-batch 重复利用数据（<font color="#ff0000">On-policy -> Off-policy</font>）
    2. **Regularization KL**：加入 KL 正则，限制新旧策略差异
    3. **Clip Objective**：使用 clip objective，避免单步更新过大

<div style="text-align: center"><img src="images/image-134.png" width="90%"></div>

##### Mini-batch training

PPO 的核心思想是：**用旧策略 $\theta_{old}$ 收集的数据，去估计新策略 $\theta$ 的性能**

- 具体来说，PPO 在目标函数中引入了一个**概率比值（Probability Ratio）**：

$$
r_t(\theta) = \frac{\pi_\theta(a_t | s_t)}{\pi_{\theta_{old}}(a_t | s_t)}
$$

- $\pi_{\theta_{old}}(a_t | s_t)$：旧策略选择动作 $a_t$ 的概率（常量，因为数据已经采出来了）
- $\pi_\theta(a_t | s_t)$：当前正在更新的新策略选择动作 $a_t$ 的概率（变量）

**Training Procedure**：

1. 大步采样（Rollout Phase）
    - 让当前的策略网络在环境中跑很多步，收集包含状态 $s$、动作 $a$、奖励 $r$、旧策略对应的概率 $\pi_{old}(a|s)$ ，称这个大集合为 **Buffer（数据缓存）**
2. 打乱与切分（Shuffle & Batching）
    - 把数据彻底打乱（Shuffle），然后切分成若干个较小的 **Mini-batch**
3. 多轮循环训练（Multiple Epochs）
    - **Each Epoch**：模型会历遍所有的 Mini-batch
    - **Each Mini-batch**：计算比值 $r_t(\theta)$ 和优势函数，计算 Clip 损失，然后更新网络参数 $\theta$

##### Regularization KL

==KL 散度==（通常写为 $D_{KL}(P \parallel Q)$）用来**衡量两个概率分布之间的差异程度**。

- 如果两个分布完全一模一样，KL 散度就等于 $0$；两个分布差异越大，KL 散度就越大
- **注意**：它不是一个距离，因为它是非对称的（即 $D_{KL}(P \parallel Q) \neq D_{KL}(Q \parallel P)$），但在强化学习里，只用它来量化 **“新策略的输出分布”偏离“旧策略的输出分布”有多远**。

为了不让新策略跑得太远，PPO 将 KL 散度作为**惩罚项（Regularization）** 加入到损失函数里。它的目标函数（Objective）如下：

$$
L^{KLPEN}(\theta) = \hat{\mathbb{E}}_t \left[ \frac{\pi_\theta(a_t | s_t)}{\pi_{\theta_{old}}(a_t | s_t)} \hat{A}_t \right] - \beta \, D_{KL}(\pi_{\theta_{old}}(\cdot | s_t) \parallel \pi_\theta(\cdot | s_t))
$$

我们可以把这个公式拆成两部分来看：

- **前半部分（优势回报）**：$\frac{\pi_\theta}{\pi_{\theta_{old}}} \hat{A}_t$，这部分鼓励模型去最大化奖励。如果一个动作的优势 $\hat{A}_t$ 是正的，模型就会努力**提高新策略 $\pi_\theta$ 选这个动作的概率。
- **后半部分（KL 惩罚项）**：$- \beta \, D_{KL}(\dots)$，防止新策略 $\pi_\theta$ 偏离旧策略太远，导致 KL 散度变大
    - 这里的 $\beta$ 是一个控制惩罚力度的系数
    - OpenAI 在设计 PPO 时引入了**动态自适应 KL 散度（Adaptive KL Coefficient）** 机制。在每一轮迭代结束时，算法会检查实际的 KL 散度大小并做出调整

##### Clip Objective

PPO-Clip 的目标函数如下：

$$
L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta)\hat{A}_t, \, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t \right) \right]
$$

我们来拆解里面的每一个符号：

- **新旧策略的概率比值**：$r_t(\theta) = \frac{\pi_\theta(a_t | s_t)}{\pi_{\theta_{old}}(a_t | s_t)}$
  如果 $r_t > 1$，说明新策略选这个动作的概率比旧策略大；$r_t < 1$ 则相反
- **优势函数（Advantage Function）**：$\hat{A}_t$
  用来衡量在状态 $s_t$ 下采取动作 $a_t$ 是比平均表现好（$\hat{A}_t > 0$）还是差（$\hat{A}_t < 0$）
- **裁剪超参数**：$\epsilon$，通常设为 $0.2$
  这意味着安全区间被限制在 $[0.8, 1.2]$ 之间
- **裁剪函数**：$\text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)$
  如果 $r_t$ 跑出了 $[0.8, 1.2]$ 的范围，就强行把它拉回到边界值。
- $\min(\dots)$：**取极小值**，这是最关键的安全锁

!!! abstract

    比起普通的策略梯度或者前面讲的 KL 正则化，Clip Objective 有三个优势：

    1. **极度贪婪但又极度克制**：
       它允许算法在安全线内尽情地压榨数据的价值。但只要一过线，梯度立刻归零（或只允许往回修正），提供了硬性的安全保障。
    2. **计算极其高效**：
       KL 散度需要算两个复杂概率分布的积分/期望，而 Clip 只需要做一次简单的判断。
    3. **悲观主义原则（Pessimistic Bound）**：
       通过 min 操作，PPO 始终在对策略的改善做最坏、最保守的打算。保证强化学习在多轮 Mini-batch 训练中不崩盘。

---

## 3. Problems in Alignment

### 3.1 Catastrophic Forgetting

**Catastrophic Forgetting**：模型在 post-training 中学会了新任务，却忘掉了原本能力。

- 模型的大小和遗忘的程度无关，和微调的程度有关

<div style="text-align: center"><img src="images/image-135.png" width="80%"></div>

### 3.2 Safety Degradation

**对齐模型继续微调后，可能失去安全性**。

- 原因是 SFT 数据通常只告诉模型“怎么完成任务”，不一定保留原来的拒答边界。

<div style="text-align: center"><img src="images/image-136.png" width="80%"></div>

### 3.3 LoRA Learns Less and Forgets Less

LoRA 只训练低秩增量参数，冻结原模型大部分权重

- 学到的新任务可能没有全量微调那么彻底，但原能力也更不容易被覆盖

<div style="text-align: center"><img src="images/image-137.png" width="70%"></div>

因此 LoRA 在很多场景中既是省显存方法，也是**缓解遗忘**的方法。

### 3.4 Experience Replay

缓解遗忘的经典方法是 **Experience Replay**：

1. 新任务训练时混入少量旧任务数据
2. 让模型同时保持旧能力和学习新能力
3. 即使旧数据比例很小，也可能显著降低遗忘

<div style="text-align: center"><img src="images/image-138.png" width="70%"></div>

如果真实旧数据不可用，可以使用：

- **Pseudo Experience Replay**：用模型生成旧任务样本
- **Paraphrase**：让模型把旧样本换一种说法
- **Self-output**：让 foundation model 对旧输入生成输出，再用于训练

### 3.5 Synthetic Data - Magpie

==Magpie（喜鹊）==：一种用于生成高质量合成数据（Synthetic Data）的方法

- 它的核心突破在于：**不需要编写**任何初始 Prompt，**直接**利用对话模型（这里以 Llama-3-Instruct 为例）的预设模板，让大模型“自导自演”，**同时生成 Instruction 和 Response**

<div style="text-align: center"><img src="images/image-139.png" width="70%"></div>

- 像 Llama-3-Instruct 这样的对齐模型，在训练时被强行灌输了特殊的**模板标签（Special Tokens）**，比如 `< |start_header_id| >user< |end_header_id| >`
- 模型在看到这个标签后，它的下一个 Token 预测机制会**本能地、高概率地**去续写一个“人类用户会说的话”。Magpie 正是利用了这种自回归模型的续写特性。
- 通过这种方式，可以获得一条包含 **[Instruction, Response]** 的完整高质量对话数据。重复这个过程，就能得到 **MAGPIE-Raw** 原始合成数据集。

### 3.6 Solutions of Catastrophic Forgetting

1. **(Pseudo) Experience Replay（伪经验回放）**
    - 训练时，不仅输入新数据，还会让基座模型生成一些它以前擅长的数据
    - 把这些老数据混进训练集里，一起训练得到新模型
    - **目的**：通过“新老混练”，强行让模型在拉近新知识的同时，复习旧知识。
2. **Paraphrase（改写 / 用自己的话换句话说）**
    - 输入新知识的同时将这些信息喂给原基座模型，让它把信息“换种说法”（Paraphrase），将其转化为它原本更熟悉的表达方式或相关的老知识（old）。
    - **目的**：把新知识和模型已有的知识网络连接起来。用模型“听得懂的老话”去理解新概念，从而保护旧有的认知结构不被新知识粗暴地覆盖。
3. **Self-output（自输出）**
    - 给定一个可能包含新意图的输入，先不做任何限制，直接喂给原基座模型
    - 模型会根据它原有的逻辑输出一个结果（output: old）。
    - 策略提示：**“If it is correct, use this.”（如果这个输出是对的，就用它。）**        
    - **目的**：如果模型用旧知识就能把新问题答对，那就直接沿用，不强行用新数据去纠偏，以此减少对模型的无谓修改。
前面提到的三点（Experience Replay, Paraphrase, Self-output）通常是用在监督微调（SFT）阶段的数据操纵手段。**如果换成基于强化学习（如 PPO、DPO）的后训练，情况可能会更好**

---

## 4. DeepSeek and Reasoning Models

!!! info "DeepSeek V3 vs R1"

    | 维度   | V3               | R 1            |
    | ---- | ----------------- | -------------- |
    | 模型类型 | 非推理模型             | 推理模型           |
    | 结果倾向 | 确定性高、路径明确         | 开放性高、多路径探索     |
    | 适合任务 | 规范流程、结构化生成        | 数学、代码、复杂推理     |
    | 提示方式 | 需要清晰角色、技能、约束、输出格式 | 更适合给目标，让模型展开思考 |
    | 风险特征 | 稳定可控              | 不确定性更高         |

<div style="text-align: center"><img src="images/image-140.png" width="70%"></div>

### 4.1 DeepSeek V3 Technology

DeepSeek V3 的几个关键技术点：

#### Architecture Design

1. **DeepSeekMoE**
    - 使用 MoE 架构，每层包含共享专家和路由专家
    - 671B 总参数中，每个 token 只激活一部分专家，实际激活约 37B 参数
2. **Multi-Head Latent Attention (MLA)**
    - 将 QKV 压缩到 latent space 存入 cache
    - 降低 KV Cache 存储压力，有利于长上下文推理加速
3. **Multi-Token Prediction (MTP)**
    - 不只预测下一个 token，也预测后续多个 token，让训练信号更密集

#### Quantitative Training

1. **FP8 Training**
    - 大规模使用 FP8 量化训练，降低显存需求并提升训练效率
    - 使用分组量化和更高精度累加缓解 outlier 问题
2. 混合精度细粒度量化（减缓 outlier 的影响，提高模型精度） 
    - 激活采用 1\*128 Tile 条形分组量化方式，权重采用 128\*128 Block 块分组方式
    - 增加累加精度（FP 32）、增加尾数量，以及在线量化策略 
    - 优化并改进了 CUDA Kernal 的调用方式

#### Parallel Training

- 采用 $16$ 路流水线并行+ $64$ 路专家并行（跨 $8$ 个物理节点）+数据并行（ZeRO-1），并未采用通讯开销较大的张量并行，极大改善了并行训练中的通信和计算冲突问题，解决了调度瓶颈。
- DualPipe：双向流水线，减少流水线气泡
- Warp Specialization：分配 GPU SM 数量，让通信和计算尽量重叠
- 内存优化：使用 CPU 内存，重计算

### 4.2 What Is a Reasoning Model?

==Reasoning Model== 通常指会在回答前生成较长推理过程的模型。

它的典型行为：

- Verification：检查答案是否合理
- Planning：先规划解题步骤
- Explore：尝试不同解法
- Reflection：发现错误后自我修正

!!! warning

    “推理模型”是一个工程分类，不等价于模型真的具有人类推理能力。更准确地说，它们把更多计算放到了测试阶段，通过更长的中间过程提高最终答案质量。

#### Test-Time Compute

- 传统模型主要依赖 training-time compute：训练时花大量计算，推理时尽快给答案。
- 推理模型强调 ==Test-Time Compute==：推理时多花计算，多试几条路径，提升最终正确率。

可以理解为：

$$
\text{Answer Quality} \approx f(\text{Model Capability}, \text{Test-Time Compute})
$$

“**深度不够，长度来凑**”描述的就是这种现象：

- 模型本身能力有限时，可以通过更长的推理链、多次采样或验证器选择来提升结果。

#### Chain-of-Thought

Chain-of-Thought (CoT)：让模型显式生成中间推理步骤

- **Few-shot CoT**：在 prompt 中给带推理过程的示例
- **Zero-shot CoT**：直接要求模型逐步思考
- **Long CoT**：推理模型生成很长的内部推理过程
- **Short CoT**：控制推理过程更短、更可读
CoT 的作用不是保证每一步都正确，而是给模型更多中间状态来组织计算。

#### Majority Vote and Self-consistency

如果同一个问题采样多次，可以得到多个候选答案
==Majority Vote / Self-consistency==：

1. 同一个 input 生成多个 output
2. 提取最终答案
3. 选择出现次数最多的答案

这种方法适合答案空间较明确的任务，例如数学题、选择题、代码输出。

#### Best-of-N and Verifier

==Best-of-N== 使用 verifier 从多个候选中选最好的。
流程：

1. 模型生成 $N$ 个候选答案
2. Verifier 给每个答案打分
3. 选择分数最高的答案
Verifier 本身也可以是语言模型。它不一定负责生成答案，而是负责判断答案质量。

#### Distillation and RL for Reasoning

训练推理模型的常见方法：

1. **Knowledge Distillation**
    - 强推理模型生成 reasoning process 和 answer
    - 小模型学习这些过程
    - Sky-T1、s1 等属于这种路线
2. **Reinforcement Learning**
    - 不要求推理过程完全模仿人类
    - 只要最终答案正确，就给 reward
    - DeepSeek-R1-Zero 使用 accuracy as reward 展示了这种路线

<div style="text-align: center"><img src="images/image-141.png" width="70%"></div>

DeepSeek-R1-Zero 的意义：

- 模型可能在没有人工标注推理过程的情况下，通过 RL 自发学出反思、验证等行为。

DeepSeek-R1 则进一步加入：

- 少量 cold-start reasoning data
- RL 训练
- 过滤混合语言、过长段落、代码块等低质量 CoT
- 通用任务上的 SFT 和偏好优化
- Safety / Helpfulness verifier

---

## 5. Trends of Large Models

### 5.1 Open Models and Domain Models

大模型发展出现两个方向：

1. **通用模型**
    - 头部公司主导
    - 能力趋于全面
    - 训练和推理成本很高
2. **垂直领域模型**
    - 面向司法、教育、金融、医疗等领域
    - 更强调专业知识、可解释性、私有化部署和数据合规

!!! abstract

    通用大模型解决“广度”，领域大模型解决“落地”。后者不一定参数更大，但需要更高质量的领域数据、更强的知识溯源和更严格的安全合规。

### 5.2 Compute Trend

大模型能力高度依赖算力。

课件中列举的算力趋势：

- GPU 性能继续提升，例如 Blackwell / Blackwell Ultra
- 专用推理芯片开始发力，例如 Groq LPU
- TPU 继续扩展 HBM 容量、带宽和集群规模
- 存算一体、类脑芯片可能成为长期方向

算力提升的意义：

- 支持更大模型
- 支持更长上下文
- 支持更低延迟推理
- 支持 test-time compute 和多候选搜索

### 7.3 Multimodal Models

随着 ChatGPT 成功，多模态成为下一阶段重点。

多模态能力包括：

- 图像理解
- 图表理解与数据推理
- 图像 / 文本内容生成
- 视频理解
- 语音识别和语音合成
- 跨模态检索与交互

#### Cheetah / 联觉

联觉多模态大模型强调复杂图文交错指令理解。

特点：

- 支持多种多模态任务
- 使用可控知识注入机制
- 构造大规模图文交错复杂指令数据集
- 能理解多张图片之间的关系

#### Momentor

==Momentor== 是视频大语言模型，目标是细粒度视频理解。

核心问题：

- 普通视频模型只理解短视频或整体内容
- 未裁剪视频很长，包含多个语义片段
- 用户可能需要指定时间段或让模型定位事件时间

关键模块：

- **Temporal Perception Module**：注入精确时间信息
- **Grounded Event-Sequence Modeling**：对齐视频特征序列和事件语义序列
- **Moment-10M**：细粒度指令微调数据集

#### NaturalSpeech 3 and GPT-4o

语音大模型方向关注：

- 零样本语音合成
- 音色、语速、韵律控制
- 实时语音对话
- 实时翻译
- 语音识别和语音合成一体化

GPT-4o 展示了多模态模型向实时语音交互发展的趋势。

#### Auto-Encoding Morph-Tokens

视觉理解和视觉生成有冲突目标：

| 任务 | 需要的信息 | 倾向 |
| ---- | ---- | ---- |
| 视觉理解 | 抽象语义 | 可以丢弃部分细节 |
| 视觉生成 | 完整视觉细节 | 需要尽量保留图像信息 |

==Morph-Tokens== 的思路是区分：

- **Pre-MLLM tokens**：包含抽象主体语义，用于理解
- **Post-MLLM tokens**：包含完整视觉语义，用于重建和生成

这样可以缓解理解和生成目标之间的冲突。

### 7.4 Agents

智能体方向关注让大模型从“回答问题”走向“完成任务”。

典型能力：

- 调用工具
- 角色扮演
- 任务规划
- 多步决策
- 访问外部模型或 API
- 操作 GUI
- 形成短期和长期记忆

#### Toolformer

Toolformer 的思想是让语言模型学会在生成过程中调用外部工具，例如计算器、搜索或 API。

#### HuggingGPT

==HuggingGPT== 使用大模型作为任务规划和调度中心，调用 Hugging Face 上的专用模型完成跨媒体任务。

可以理解为：

1. 用户提出复杂任务
2. LLM 拆解任务
3. LLM 选择合适小模型
4. 小模型执行视觉、语音、文本等子任务
5. LLM 汇总结果并回复

!!! info

    Agent 的关键不是模型自己会所有事情，而是模型能够**知道何时调用外部能力，并把多个工具的结果组织成可用方案**。

### 7.5 Embodied AI and World Models

具身智能把大模型接到真实或模拟环境中。

相关方向：

- GUI agent：把屏幕图像作为输入，把鼠标键盘操作作为动作
- 推荐系统 agent：结合用户历史行为、短期记忆、长期记忆和事件预测
- VLA 模型：Vision-Language-Action，用视觉和语言指导动作
- 世界模型：预测环境变化，用于规划和控制

例子：

- Helix: 面向通用人形机器人控制的 VLA 模型
- Nvidia Cosmos: 世界模型方向

---

## 8. Cognition, Perception and Future

### 8.1 System 1 and System 2

《思考，快与慢》中把人的思维粗略分成两类：

| 系统 | 特点 | 类比到 AI |
| ---- | ---- | ---- |
| **System 1** | 快速、直觉、感知驱动 | 深度学习、模式识别 |
| **System 2** | 慢速、计划、逻辑推理 | 符号推理、程序、数据库 |

AI 早期更偏 System 2：编程语言、算法、数据库。
深度学习兴起后更偏 System 1：图像、语音、语言等感知任务。

### 8.2 Why Deep Learning Works

机器学习成功的核心方式是：

1. 收集大量输入和输出
2. 不手写解决问题的具体规则
3. 把问题转化为学习一个映射函数

也就是从：

```text
人工写规则
```

转向：

```text
数据 + 模型 + 优化
```

### 8.3 Current Limitations

当我们试图用 System 1 的方法解决 System 2 的问题时，会出现很多问题：

- 不能稳定举一反三
- 缺乏常识
- 不具备解释性
- 容易受到攻击
- 细节看起来合理，但全局结构荒诞

!!! warning

    LLM 很擅长生成局部合理的语言片段，但不总是能保证全局正确性、因果一致性和可验证性。这也是为什么工具调用、检索增强、验证器和 agent 规划会变得重要。

### 8.4 Future Direction

课件中对未来的设想是：大的认知模型控制小的感知模型，形成自我扩展的系统。

可能路径：

- 系统 2 模型自动编写系统 1 模型代码
- 自动生成高质量语料和图像训练感知模型
- 自动生成训练脚本和评估流程
- 通过自我问答提升推理能力
- 用多个模型协作完成大型工程

### 8.5 Concerns

生成式 AI 带来的担忧包括：

- 大量岗位任务被自动化
- 初级岗位减少，新人入行更困难
- 高学历、高收入岗位也会受到影响
- 工作内容被重组，而不是简单替代某一个职业

!!! abstract

    GPT 时代的核心变化是：语言模型不再只是 NLP 组件，而正在变成知识接口、推理引擎、工具调度器和多模态交互入口。它的能力来自规模，也来自 post-training、test-time compute、外部工具和真实场景反馈。
