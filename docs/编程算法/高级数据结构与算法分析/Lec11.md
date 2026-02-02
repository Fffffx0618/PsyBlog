# Approximation
## 11.1 Introduction
Three aspects to be considered
- Optimality: 算法能找到确切的**最优解**
- Efficiency: 算法能**高效**（通常是多项式时间）运行
- All instances: 算法是通用的，能够解决**全部问题**

Researchers are working on
- O+A：针对全部实例的精确算法
- O+E：对于特殊情况的精确且快速的算法
- E+A：**近似算法**

【Definition】一般通过**近似比**(approximation ratio) $\rho(n)$ 来衡量近似算法的好坏，称这样的近似算法为 $\rho(n)$ -近似算法。它的意义是：对于任意规模为 $n$ 的输入，算法得到一个解所花的成本 $C$ 不会超过得到最优解所花成本 $C^*$ 的 $\rho(n)$ 倍，即：
$$
\max(\dfrac{C}{C^*}, \dfrac{C^*}{C}) \le \rho(n)
$$
【Definition】**近似方案**(approximation scheme) 是关于优化问题的一种近似算法，满足对于给定的输入实例，$\forall \varepsilon > 0$，它是一个 $(1 + \varepsilon)$ 近似算法。

- **polynomial-time approximation scheme, PTAS**
	- 对于任意固定的值 $\varepsilon > 0$，当输入实例规模为 $n$ 时，该方案能在多项式时间内完成计算
	- 时间复杂度可记为 $O(f(n,\varepsilon))$, 其中 $f(n,\varepsilon)$ 关于 $n$ 是多项式
- **fully polynomial-time approximation scheme, FPTAS**
	- 在PTAS的基础上，要求该方案的运行时间关于 $n$ 和 $\varepsilon$ 都是多项式级的
	- 时间复杂度可记为 $O(f(n,\varepsilon))$, 其中 $f(n,\varepsilon)$ 关于 $n$ 和 $\dfrac{1}{\varepsilon}$ 是多项式

---
## 11.2 Bin Packing
> [!question]
> 给定 $N$ 个大小分别为 $S_1, S_2, \dots, S_N$ 的物品，满足 $\forall\ 1 \le i \le N, 0 < S_i \le 1$，并假设有若干个容量为 1 的桶。现在请你求出能够装下所有物品的最小桶数。

这个看似简单的问题实际上是一个**NP困难问题**
> [!tip]- 从 Partition Problem 归约
> - 假设有一个 Partition 实例：$a_1​,a_2​,\dots,a_n$ ​，总和为 $T$，判断是否能分成两个和为 $T/2$ 的子集
> 
> 可以构造一个 Bin Packing 实例如下：
> - 每个物品大小为 $s_i​=a_i​/T$，$s_i < 1$
> - 总共有 n 个物品
> - 问题：**能否用 2 个箱子装下所有物品？**
- 该问题的变种（决策版本）：给定$K$个桶，我们能否装下$N$个物品——**NPC问题**

下面给出几种解决该问题的近似算法。
### Online Algorithms
#### 1. Next Fit
```c
Void NextFit () {
    Read item 1;
    While (read item 2) {
        If (item 2 can be packed in the same bin as item 1)
            Place item 2 in the bin;
        Else
            Create a new bin for item 2;
        Item 1 = item 2;
    } // end-while
}
```

- 按输入顺序放物品，如果当前物品能够放在与上个物品相同的桶内，放入；否则放在新的桶内

> [!Theorem] 定理
> 令 $M$ 为装下这些物品的最优解桶数，那么该方法所得桶数不超过 $2M - 1$，并且存在某种输入使得桶数正好为 $2M - 1$。因此该算法是一个 2-近似算法。
>> [!proof]-
>> **等价命题**：如果该算法能得到 $2M$ 或 $2M + 1$ 个桶，那么最优解至少是 $M + 1$ 个桶，证明如下：
>> 令$S(B_i)$为第$i$个桶所装物品的大小，那么可以得到：
>> $$\begin{align}
>>             S(B_1) + S(B_2) & > 1 \notag \\
>>             S(B_3) + S(B_4) & > 1 \notag \\
>>             \dots \notag \\
>>             S(B_{2M - 1}) + S(B_{2M}) & > 1 \notag
>>             \end{align}
>>             $$
>>累加得：$\sum\limits_{i = 1}^{2M} S(B_i) > M$
>> 最优解至少需要 $\lceil \sum\limits_{i = 1}^{2M} S(B_i)\rceil$ 个桶
>> 因此最终得到：$\lceil \sum\limits_{i = 1}^{2M} S(B_i) \rceil \ge M + 1$，即该命题是正确的，得证。

#### 2. First Fit
```c
void FirstFit() {
    while (read item) {
        scan for the first bin that is large enough for item;
        if (found)
            place item in that bin;
        else
            create a new bin for item;
    } // end-while
}
```
        
- 对于当前物品，找到第一个现存的能够容得下它的桶，如果不存在这样的桶再添加新的桶
- 时间复杂度：$O(N\log N)$（循环内扫描桶的时间复杂度优化至$O(\log N)$）

> [!info] Theorem 
> 令 $M$ 为装下这些物品的最优解桶数，那么 first fit 所得桶数不超过 $\dfrac{17 M}{10}$，并且存在某种输入使得桶数正好为 $\dfrac{17(M - 1)}{10}$。因此该算法是一个1.7-近似算法。

#### 3. Best Fit
- 将当前物品放入现存的、容得下它的、且放入该物品后剩余空间是最小的桶内，如果不存在这样的桶再添加新的桶。
- 时间复杂度：$O(N \log N)$
- 与First Fit类似，它也是一个**1.7-近似算法**
---

上述的三种近似算法均为**在线算法**(online algorithm)
- 在处理下一个物品前就要放好当前物品，且**不能改变**当前的决策
> [!note] Theorem
> 由于在线算法无法得知输入何时结束，因此始终无法得到最优解。具体来说，有以下定理：
> - 对于本题的所有近似算法，得到的近似解桶数**至少**是最优解桶数 $\dfrac{5}{3}$ 倍。

### Offline Algorithms
- 在得到答案前需要检查所有的物品
- 先找到trouble maker：尺寸较大的物品
- 解决方案——**first/best fit decreasing**：先将物品按大小的<u>非递增顺序排序</u>，然后应用 first fit 或 best fit 求解。该方法用到了**贪心算法**的思想。

<div style="text-align: center">
<img src="images/lec11/3.gif" width="60%">
</div>

> [!info] Theorem
> 令$M$为装下这些物品的最优解桶数，那么该方法（first fit decreasing）所得桶数不超过$\dfrac{11 M}{9} + \dfrac{6}{9}$，并且存在某种输入使得桶数正好为$\dfrac{11 M}{9} + \dfrac{6}{9}$。

### Conclusions
> [!note] 一些结论
> $FFD(L)$ 表示的是对于物品组 $L$，用first fit decreasing算法得到的桶数
> - $FFD(L) \le \dfrac{3}{2} OPT(L)$
> - 如果能够证明 P=NP，就可以确定 $\dfrac{3}{2}$ 是最小的因数（近似比）
> 
>>[!proof] Conclusion 1
>> - 已知 $\forall\ L, FFD(L) \le \dfrac{11}{9}OPT(L) + 1$（此处使用更宽松的条件）
>> - 可以先计算 $\dfrac{11}{9}OPT(L) + 1 \le \dfrac{3}{2} OPT(L)$，解得 $OPT \ge 4$，所以接下来只需考虑 $OPT = 1, 2, 3$ 的情况即可
>> 	- $OPT = 1$：$FFD = 1$，显然成立
>> 	- $OPT = 2$：根据定理可得 $FFD \le \dfrac{11}{9} \times 2 + 1 = \dfrac{31}{9}$，解得 $FFD \le 3$，结论成立
>> 	- $OPT = 3$：根据定理可得 $FFD \le \dfrac{11}{9} \times 3 + 1 = \dfrac{42}{9}$，解得 $FFD \le 4$，结论成立
>> - 综上所示，结论1成立
>   
>> [!proof] Conclusion 2
>> 考虑该问题的某个判定版本：若存在一种近似算法 $A$，满足 $A < \dfrac{3}{2}OPT$，使用该算法放置物品时，能否用两个桶装下所有的物品？（这是一个NPC问题）
>> - 如果可以，那么$A \le 2$，显然$OPT \le 2$，即最优解也不会超过两个桶，也是OK的
>> - 如果不行，那么$A \ge 3$，$OPT \ge \dfrac{2}{3}A > 2$，即最优解也需要两个以上的桶，也是不行的
>> 
>> 不难发现 $\dfrac{3}{2}$ 是一个临界点。如果能够在多项式时间内能够判定 $A$ 的大小，即解决这个NPC问题，那么此时P=NP

---
## 11.3 Knapsack Problems
### Fractional Version
> [!question] 问题描述
>> [!info] 注
>> 这里的“背包问题(knapsack problem)”是==分数版本==的0-1背包问题，不是在DP那一讲中提到的那几种简单类型
> 
>令背包容量为$M$，给定$N$类物品，每类物品$i$的重量为$w_i$，价值为$p_i$，被放进背包的比例为$x_i \in [0, 1]$（因此该类物品的总价值为$p_i x_i$）。
> 很明显，该问题的最优解即为背包所装物品的最大价值。也就是说，在满足$\sum\limits_{i=1}^n w_i x_i \le M$的限制条件下，令$\sum\limits_{i=1}^np_ix_i$最大。

- 在每个阶段中，我们需要将一类物品放入背包内
- **贪心法**：按**价值密度**(profit density)大小$\dfrac{p_i}{w_i}$的降序挑选物品，直到背包被填满为止
> [!example]
> **题目**:已知 $n = 3, M = 20, (p_1, p_2, p_3) = (25, 24, 15), (w_1, w_2, w_3) = (18, 15, 10)$，计算背包的最大价值
> **答案**: $(x_1, x_2, x_3) = (0, 1, \dfrac{1}{2})$，此时最大价值 $P = 31.5$

### 0-1 Version
在上面一类背包问题的基础上多了一条限制：$x_i = 0 \text{ or } 1$，事实上，这个看似简单的问题是一个NP困难问题
> [!example]
> **题目**
> - 已知 $n = 5, M = 11, (p_1, p_2, p_3, p_4, p_5) = (1, 6, 18, 22, 28), (w_1, w_2, w_3, w_4, w_5) = (1, 2, 5, 6, 7)$，计算背包的最大价值。
> 
> **答案**
> - 最优解：$(0, 0, 1, 1, 0), P = 40$
> - 贪心解：$(1, 1, 0, 0, 1), P = 35$
> 
> 对于本例，无论是采取选最大价值密度的策略，还是采取选最大价值的策略，结果都是一样的
    
贪心法在0-1背包问题中是一个**2-近似算法**，证明如下：
> [!proof]
> 通过已知条件，可以得到下列不等式：
> $$
>     \begin{align}
>     p_{\text{max}} & \le P_{\text{opt}} \le P_{\text{frac}} \notag \\
>     p_{\text{max}} & \le P_{\text{greedy}} \notag \\
>     P_{\text{opt}} & \le P_{\text{greedy}} + p_{\text{max}} \notag
>     \end{align}
>     $$
> 其中，$p_{\text{max}} = \max\limits_{1 \le i \le n}\{p_i\}$，$P_{\text{opt}}$ 表示本题的最优解，$P_{\text{frac}}$ 表示分数背包问题的解，$P_{\text{greedy}}$ 表示本题的贪心解。
> - 第一个不等式：左边不等号显然成立，右边不等号是因为分数背包问题可以取部分物品，那么它一定能够在0-1背包的基础上，通过塞入部分物品将背包塞满
> - 第二个不等式也是显然成立的
> - 第三个不等式：不等号两边同时减去$P_{\text{greedy}}$，即最优解与贪心解之差一定不超过最大价值
>   - 在小数解中，其实**只有一个物品会被拆分放入**（因为价值大的剩余位置够用时肯定装满价值大的），因此贪心解和分数解的差值就是没有被拆分放入背包的物品的价值
>   - 将被拆分的物品价值 $p$ 替换为价值最大的物品 $p_{max}$，这时 $P_{greedy} + p_{max} \ge P_{frac} = P_{greedy} + p \ge P_{opt}$
>     
> 根据这三个不等式，可以推出：
> $$
>     \dfrac{P_{\text{opt}}}{P_{\text{greedy}}} \le 1 + \dfrac{p_{\text{max}}}{P_{\text{greedy}}} \le 2
>     $$
> 根据近似比的定义，便可得到近似比为2。

**A Dynamic Programming Solution**：
- 令$W_{i, p}$为物品1到物品$i$之间的最小质量，而这些物品的总价值为$p = \sum\limits_{k = 1}^i p_k$
- 分类讨论：
    - 取物品$i$：$W_{i, p} = w_i + W_{i - 1, p - p_i}$
    - 不取物品$i$：$W_{i, p} = W_{i - 1, p}$
    - 不可能得到价值$p$：$W_{i, p} = \infty$
- 状态转移方程为：
$$
W_{i, p} = \begin{cases}\infty & i = 0 \\ W_{i - 1, p} & p_i > p \\ \min\{W_{i - 1, p}, w_i + W_{i - 1, p - p_i}\} & \text{otherwise}\end{cases}
$$
- 其中，$i = 1, \dots, n, p = 1, \dots, np_{\text{max}}$，因此时间复杂度为$O(n^2 p_{\text{max}})$

> [!question]
> **问题1**：Why NP-hard?
> - 上面给出的时间复杂度中包含 $p_{max}$，它与数据规模 $n$ 独立，因此这个数可以很大很大，超出 $n$ 的指数级倍。因此，无法保证dp解法能够在多项式时间内产生解。
> 
> **问题2**：假定 $w_i \le N^2$，那么0-1背包问题是否还是 NP-hard？
> - 不难得到 $M = \sum\limits_{i = 1}^N N \cdot w_i \le N \cdot N^2 \le N^3$，那么总的时间复杂度就是 $O(N^4)$，因此此时0-1背包问题就不是 NP-hard了。

---
## 11.4 K-center Problems
**聚类**(clustering)问题：把相似的对象通过静态分类的方法分成不同的组别或者更多的子集，使得同一子集中的成员对象都有一些相似属性的一种操作，常应用于数据挖掘、机器学习等领域。下面介绍一类聚类问题——**K-中心问题**(K-center problem)。
> [!question]
> 给定 $n$ 个地址 $s_1, \dots, s_n$，在地图上选择 $K$ 个中心点 $c$，使任意地址到离它距离最近的中心点之间的距离中的最大值最小化。

<div style="text-align: center">
<img src="images/lec11/6.png" width="60%">
</div>  
**符号化的定义**：
- $dist(s_i, C) = \min\limits_{c \in C} \{dist(s_i, c)\}$，即$s_i$到最近中心点间的距离
- $r(C) = \max\limits_{i} \{dist(s_i, C)\}$，即所有中心点中最大的最小覆盖半径，换句话说，就是以中心点为圆心的最小覆盖圆中，最大的那个圆的半径
**目标**：
- 找到一组中心点集 $C$，使得 $r(C)$ 最小化，且保证 $|C| = K$（$K$ 为常数）

### Naive Greedy
- 让第一个中心点作为所有地址的**中点**（就好像只能放一个中心点）
- 随后加入的中心点满足能够减少$r(C)$值的条件
<div style="text-align: center">
    <img src="images/lec11/7.png" width="60%">
</div>  

> [!failure]
> 如图所示，假设整个点集包括两个相距很远的子集，且$K = 2$。此时第一个中心点就会被放在两个子集的中间，但最优解应该是中心点位于子集的中间位置的时候，所以贪心策略失效了
> 
> <div style="text-align: center"><img src="images/lec11/8.png" width="80%"></div>  

### 2r Greedy
贪心法需要进一步的改进，先给出伪代码：
```c
Centers Greedy-2r(Sites S[], int n, int K, double r) {
    Sites S`[] = S[];  // S` is the set of the remaining sites
    Centers C[] = NULL;
    while (S`[] != NULL) {
        Select any s form S` and add it to C;
        Delete all s` from S` that are at dist(s`, s) <= 2r;
    } // end-while
    if (|C| <= K) 
        return C;
    else
        ERROR("No set of K centers with covering radius at most r");
}
```

1. 预备知识：在改进的贪心算法中，我们直接挑选某个地址作为中心点。
	- 这种做法之所以可行，是因为某个中心点覆盖半径为 $r$ 的区域，可以近似为以（接近）区域边界上一点 $s$ 为新的中心点，$2r$ 为半径的区域。这个区域明显比原区域大，同时也能保证覆盖原区域所能覆盖的点。
	- 这样的话我们就不必通过繁琐的计算算出中心点，而是从原有的地址中选择中心点。下图说明了这一点：
<div style="text-align: center">
    <img src="images/lec11/10_light.png" width="40%">
</div>  
2. 关于参数 $r$（$C^*$ 为最优中心点集，令 $r(C^*) \le r$）：
	假如我们知道了最大半径 $r_{\text{max}}$，此时由于 $r$ 的范围是已知的（$0 < r \le r_{\text{max}}$）我们可以使用**二分查找**来找到 $r$ 的值，具体来说：
    - 先令$r = \dfrac{0 + r_{\max}}{2}$
    - 如果能够在这个 $r$ 下面找到满足要求的 $K$ 个中心点，说明这个界还是比较宽松的，需要减小 $r$；否则的话增加 $r$（都是用二分法改变 $r$ 值）
    - 时间复杂度：$O(\log r_{\max})$

3. 回到贪心算法上：
    - 从输入点集中随机选取第一个点作为中心，然后删除**以该点为中心，$2r$ 为半径的圆**内部的所有点
    - 然后在剩余点中随机选择第二个中心，以此类推
    - 如果该 $r$ 值确实是最优解，那么这一算法在 $K$ 步之内必然停止，且得到的解是最优解的2倍，即该算法是一个**2-近似算法**
    - 定理：假设该算法选择的中心点数超过 $K$，那么对于任意规模至多为 $K$ 的中心点集 $C^*$，覆盖半径为 $r(C^*) > r$

### Smarter Greedy
```c
Centers Greedy-Kcenter(Sites S[], int n, int K) {
    Centers C[] = NULL;
    Select any s from S and add it to C;
    while (|C| < K) {
        Select s from S with maximum dist(s, C);
        Add s to C;
    }  // end-while
    return C;
}
```

- 这里的贪心法策略是：
    - 第一个点还是任意取的
    - 之后<u>选择离中心点集中的点尽可能远的点</u>作为新的中心点
    - 循环$K$遍结束循环
- 定理：该算法返回包含规模为$K$的中心点集$C$，使得$r(C) \le 2r(C^*)$，其中$C^*$表示最优中心点集
	- 本质上依旧是一个2-近似算法。

## 11.5 Appendix
> [!info] 一些常见问题的近似解
> - **绝对近似比**（Absolute Approximation Ratio）：对所有输入实例 $I$ ， $\text{result}\le \rho \cdot OPT(I)$
> - **渐近近似比**（Asymptotic Approximation Ratio）：存在常数 $c$ ，使得对所有 $I$，$\text{result}\le \rho \cdot OPT(I) + c$
>   
> 

| 问题                        | 最优近似结果（多项式时间）                                                                                      | 结论（复杂性含义）                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 0-1 背包                    | 存在 FPTAS：对任意  $\varepsilon ﹥ 0$ ，可在 $\text{poly}(n, 1/\varepsilon)$ 时间内得到 $(1+\varepsilon)$ -近似解   | ✅ 可任意精度近似；是少数容易近似的 NP-hard                               |
| K-center                  | 存在 2-近似算法，且对所有实例满足  $R \leq 2 \cdot \text{OPT}$                                                    | ❌ 除非 P = NP，否则不存在  $(2 - \varepsilon)$ -近似算法；2 是紧的绝对近似比  |
| Bin Packing               | 不存在多项式时间算法满足$\text{ALG} \leq (3/2 - \varepsilon) \cdot \text{OPT}$                                 | ⚠️ 1.5 是绝对近似比的下界；实际算法在渐近意义下优于 1.5，但无法保证对所有实例 ≤ 1.5 × OPT |
| Vertex Cover Problem      | 存在 2-近似算法，且对所有实例满足  $R \leq 2 \cdot \text{OPT}$                                                    |                                                          |
| Set Cover                 | 贪心算法达到  $H_n \approx \ln n + 1$  近似<br>对任意  $\varepsilon ﹥ 0$ ，不存在  $(1 - \varepsilon)\ln n$ -近似算法 | ❌ 无法做到常数近似； $\Theta(\ln n)$  是紧的近似界                      |
| 广义 TSP                    | 对任意常数 $\rho$ ，不存在 $\rho$ -近似算法（除非 P = NP）；甚至对某些版本，近似比需为指数级                                         | 🚫 完全不可近似（无常数因子近似算法）                                     |
| Maximum Clique            | 最好已知近似比约为  $O(n / \log^2 n)$ <br>对任意 $\varepsilon ﹥ 0$，不存在  $n^{1 - \varepsilon}$ -近似算法（除非 P = NP） | 🧱 几乎无法近似；近似比必须随 $n$ 多项式增长                               |
| Multiprocessor Scheduling | List Scheduling 算法的近似比 $\dfrac{C_{LS}}{C_{OPT}}\le 2-\dfrac{1}{m}$                                 |                                                          |

