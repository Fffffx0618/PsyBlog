# 自然语言处理

!!! info

    课程：【自然语言处理导论】
    教师：汤斯亮
    时间：25-26春夏 - 周二345
    教室：玉泉教1-234
    网站：ftp://dl4nlp2026:nlp2026@10.214.112.254

| Markdown 文件                                            | 对应主题                         | 笔记标题                                                       |
| ------------------------------------------------------ | ---------------------------- | ---------------------------------------------------------- |
| [WordEmbedding.md](WordEmbedding.md)                   | 词嵌入                          | Word Embedding                                             |
| [RNN.md](RNN.md)                                       | 循环神经网络                       | Recurrent Neural Networks                                  |
| [NLG_and_NMT.md](NLG_and_NMT.md)                       | 自然语言生成与神经机器翻译                | Natural Language Generation and Neural Machine Translation |
| [Reinforcement_Learning.md](Reinforcement_Learning.md) | 深度强化学习                       | Deep Reinforcement Learning                                |
| [Transformers.md](Transformers.md)                     | Transformer 与预训练模型           | Transformers                                               |
| [TrainLLM.md](TrainLLM.md)                             | 如何训练大模型                      | How to train your LLM                                      |
| [Model_Compression.md](Model_Compression.md)           | 模型压缩与数据高效微调                  | Model Compression and Data-Efficient Fine-tuning           |
| [GPTs.md](GPTs.md)                                     | GPTs：ChatGPT, GPT-4, and etc | GPTs: ChatGPT, GPT-4, and etc                              |

---

#### 词嵌入

[Word Embedding](WordEmbedding.md)

- **主要内容**：
    - **词表示的演进**：
      从流形假设、离散表示和 One-hot 的局限出发，引入“通过上下文理解词义”的分布式表示思想。
    - ==Word2Vec==：
      介绍 CBOW 与 Skip-gram 两种主流架构，以及如何通过上下文窗口学习词向量。
    - **训练技巧**：

      **Hierarchical Softmax** 和 **Negative Sampling**：缓解大词表 Softmax 计算开销过大的问题。

    - **应用与局限**：
      包括词类比、下游任务初始化，以及静态词向量难以处理一词多义、序列信息和可解释性的问题。

#### 循环神经网络

[Recurrent Neural Networks](RNN.md)

- **主要内容**：
    - **序列数据建模**：
      介绍朴素 RNN 如何通过隐藏状态在时间步之间传递信息，以及展开（Unrolling in Time）后的训练方式。
    - ==LSTM & GRU==：
      讲解 LSTM 的输入门、遗忘门、输出门、细胞状态与窥视孔连接，并对比简化后的 GRU 结构。
    - **NLP 应用**：
      讨论长距离依赖、Encoder-Decoder 框架，以及 LSTM 可以从序列中学习到的语言结构。
    - **注意力机制**：
      从基础注意力得分计算出发，说明注意力如何缓解固定长度向量瓶颈，并为后续 Transformer 铺垫。

#### 自然语言生成与神经机器翻译

[Natural Language Generation and Neural Machine Translation](NLG_and_NMT.md)

- **主要内容**：
    - **生成模型基础**：
      定义 NLG、RNN-LM 与条件语言模型，并介绍训练生成模型时常用的 **Teacher Forcing**。
    - **解码（Decoding）策略**：
      对比 Greedy Decoding、采样式解码、Beam Search 与 Softmax Temperature 等生成阶段的搜索策略。
    - **机器翻译发展与评估**：
      回顾从 SMT 到 NMT 的发展，并介绍人工评估、BLEU、METEOR 和困惑度（Perplexity）。
    - **NMT 架构迭代**：
      从 Seq2Seq 编码器-解码器，到注意力机制、双向编码器、深层网络、并行化与残差连接。

#### Transformer 与预训练模型

[Transformers](Transformers.md)

- **主要内容**：
    - **Self-attention 与 Multi-head Attention**：
      通过 Query、Key、Value 和 Scaled Dot-Product Attention 解释自注意力计算，并说明多头机制如何并行关注不同关系。
    - **Transformer 架构**：
      介绍 Encoder-Decoder 结构、Masked Self-attention、Cross-attention、Position-wise FFN、残差连接与 Layer Norm。
    - **位置编码**：
      从原始 Positional Encoding 讲到 RoPE，强调相对位置感知与长序列外推能力。
    - **后续优化与变体**：
      包括无归一化 Transformer、MLP-Mixer、Linear Attention、RetNet 与门控记忆机制。
    - **BERT 及其变体**：
      总结预训练 / 微调范式、上下文化词表示、输入输出格式、全量微调、Adapter、特征加权与预训练目标。

#### 如何训练大模型

[How to train your LLM](TrainLLM.md)

- **主要内容**：
    - **训练显存构成**：
      分析参数、梯度、优化器状态和激活值的显存占用，说明训练为什么比推理更吃资源。
    - **ZeRO 系列优化**：
      从 ZeRO-1 到 ZeRO-3 逐步切分优化器状态、梯度和模型参数，并讨论通信与显存的权衡。
    - **Offload 策略**：
      将优化器状态、梯度或模型参数迁移到 CPU 内存，以牺牲速度换取更低 GPU 显存占用。
    - **激活与算子优化**：
      介绍 Kernel、Flash Attention 和 Liger Kernel 如何降低 Attention 训练中的内存访问成本
    - **量化基础**：
      通过有损压缩、量化与反量化理解低精度表示如何减少模型存储和显存压力。

#### 模型压缩与数据高效微调

[Model Compression and Data-Efficient Fine-tuning](Model_Compression.md)

- **主要内容**：
    - **模型压缩总览**：
      围绕降低存储、显存、计算和推理延迟，介绍量化、剪枝和蒸馏三类核心方法。
        1. **Quantization**：包括 Post-Training Quantization、INT8 量化、GOBO、LLM.int8、QAT、ZeroQuant 与 QLoRA
        2. **Pruning**：对比非结构化与结构化剪枝，介绍 Magnitude Pruning、Lottery Ticket Hypothesis、Wanda、CoFi 和 Bonsai
        3. **Distillation**：讨论 Hard / Soft Targets、Sequence-Level Distillation、DistilBERT、Self-Instruct 与 Prompt2Model
    - **数据高效微调**：
      总结 Adapter、LoRA、Prefix / Prompt Tuning、Prompt Tuning、Early Exit、PET 与 prompting 方法选择。

#### 深度强化学习

[Deep Reinforcement Learning](Reinforcement_Learning.md)

- **主要内容**：
    - **RL 基础概念**：
      介绍 Agent、Environment、Action、Observation、Reward、Experience 与 State，并区分 Model-based / Model-free、Value-based / Policy-based 方法。
    - **Value-based RL**：
      从 Q-function、Bellman Equation 和 Value Iteration 出发，解释 Q-Learning 如何通过估计长期回报选择行动。
    - ==DQN==：
      用深度神经网络近似 Q-value，重点整理 Experience Replay、Target Q-network、Reward Clipping 等稳定训练技巧。
    - **Policy Gradient**：
      直接优化策略网络，用 trajectory 的累计回报调整 action probability，并解释为什么要关注长期 reward。
    - **Actor-Critic / A 3 C**：
      用 Critic 估计 Value / Advantage 来降低策略梯度方差，并介绍异步 worker 的并行采样与更新机制。

#### GPTs：ChatGPT, GPT-4, and etc

[GPTs: ChatGPT, GPT-4, and etc](GPTs.md)

- **主要内容**：
    - **GPT 技术脉络**：
      从图灵测试、Word Embedding、RNN 和 Transformer 出发，对比 BERT 的填词范式与 GPT 的接龙式语言建模，并介绍 In-context Learning、Scaling Laws 与 Emergent Ability。
    - **大模型训练与对齐**：
      梳理 Pre-training、Instruction Fine-tuning / SFT、RLHF / PPO 的完整流程，解释为什么 Base Model 不能直接作为 ChatBot 使用。
    - **Post-training 风险**：
      总结 Catastrophic Forgetting、安全性退化、LoRA、Experience Replay、Pseudo Replay 与 Self-output 等缓解方法。
    - ==DeepSeek 与推理模型==：
      对比 DeepSeek V3 / R1，整理 MoE、MLA、FP8、DualPipe、Test-Time Compute、CoT、Self-consistency、Best-of-N、Verifier、Distillation 与 RL。
    - **大模型发展趋势**：
      覆盖领域模型、算力芯片、多模态模型、语音与视觉统一、Agent、HuggingGPT、具身智能、世界模型，以及认知系统与感知系统的关系。
