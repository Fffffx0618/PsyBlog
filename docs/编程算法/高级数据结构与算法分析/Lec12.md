# Local Search
## 12.1 Introduction
**局部搜索**(local search)实际上是近似算法的一大门类
- 它的大致思路是：通过**局部最优解**获得**全局近似解**
> [!note]
> 局部搜索算法的设计需要考虑好「局部」的范围：
> <div style="text-align: center"><img src="images/lec12/4.png" width="30%"></div>
> 
> - 局部范围过小：算法可能就会误以为“小坑”是最优解，而不会继续搜索下去
> - 局部范围过大：算法可能跳过了最优解，最坏的情况下算法可能陷入死循环，因为算法始终无法确定是否不存在更低的点（比如在最低点两边来回跳，就是找不到最低点）

局部搜索的框架结构：
- **局部**(local)：
    - 在一个可行的集合内定义**邻居**(neighborhoods)
    - **局部最优解**(local optimum)是邻居范围内的最优解
- **搜索**(search)：
    - 从一个可行解 $FS$ 开始，在邻居范围内找到一个更好的解
    - 如果没有改进空间，则将当前的局部最优解视为整个问题的“最优解”（不一定是全局最优）

**邻居关系**(neighbor relation)
- $S \sim S'$：$S'$是$S$的邻居解(neighboring solution)，它来自于对原集合$S$的较小修改
- $N(S)$：$S$的邻居，即集合$\{S': S \sim S'\}$（包含所有可能的邻居解）

局部搜索算法的伪代码如下：
```c
Solution Type Gradient_descent() {
    Start from a feasible solution S in FS;    // randomly
    // FS: the feasible solution set(for initialization)
    MinCost = cost(S);
    while (1) {
        S` = Search(N(S));     // find the best S' in N(S)
        CurrentCost = cost(S`);
        if (CurrentCost < MinCost) {
            MinCost = CurrentCost;
            S = S`;
        }
        else break;
    } 

    return S;
}
```

- 该算法称为“**梯度下降法**”(gradient descent)
---

## 12.2 Examples
### 1. Vertex Cover Problem
> [!question]
> - 给定一个无向图 $G = (V, E)$，请找到一个最小的子集 $S \subseteq V$，使得 $E$ 中的任意一边 $(u, v)$，$u$ 和 $v$ 至少有一个属于 $S$

**先定义一些量**：
- 可行解集$FS$：所有的顶点覆盖
- $cost(S) = |S|$
- $S \sim S'$：每个顶点覆盖$S$至多有$|V|$个邻居
**搜索步骤**：
- 从$S = V$开始
- 删除或增加一个节点得到新的顶点覆盖$S'$
- 检查$S'$的成本是否更低
> [!bug] 几种tricky的情况
> - **Case 0**
> <div style="text-align: center"><img src="images/lec12/5.png" width="40%"></div>
> 
> 可以看到，这张图只有顶点没有边，因此最优解就是去掉所有顶点，即 $S = \emptyset$。显然，用前面介绍过的梯度下降法能够解决此类情况。
> - **Case 1**
> <div style="text-align: center"><img src="images/lec12/8.png" width="40%"></div>
> 
> 这道题答案相当简单：只需要保留中间那个点，去掉所有其他的点即可。然而，如果算法一开始选择删除的是中间的点，就会出现问题——梯度下降法不具备撤销操作，如果该点被删除，最终无法得到最优解。
> 
> - **Case 2**
> 
>   <div style="text-align: center"><img src="images/lec12/12.png" width="65%"></div>
> 
> 这次给出的图形是一条链，不难得到以下的最优解（红色点表示保留下来的点）：
> <div style="text-align: center"><img src="images/lec12/13.png" width="60%"></div>
> 
> 然而，若算法在执行过程中一不小心删掉了这三个红点中的任意一个，则无法得到最优解，而会得到各种各样的错误：
> <div style="text-align: center"><img src="images/lec12/14.png" width="60%"></div>
> 

**Metropolis算法**
```c
SolutionType Metropolis() {
    Define constants k and T;
    Start from a feasible solution S in FS;
    MinCost = cost(S);
    while (1) {
        S` = Randomly chosen from N(S);
        CurrentCost = cost(S`);
        if (CurrentCost < MinCost) {
            MinCost = CurrentCost;
            S = S`;
        } else {
            With a probability exp(-(CurrentCost - MinCost) / (k * T)), let S = S`;
            otherwise break;
        }
    }

    return S;
}
```
- 再来看前面给出的例子：
    - 对于Case 1，该算法有一定概率可以跳出局部最优，得到正确解
    - 对于Case 0，有可能在+1和-1之间无限振荡

- 这一算法与梯度下降法的不同之处：如果新的顶点覆盖$S'$的成本更大，它不会马上就被抛弃掉，而是通过概率$e^{-\frac{\Delta \text{cost}}{kT}}$来决定是否保留
    - 这一假设被称为[玻尔兹曼分布](https://en.wikipedia.org/wiki/Boltzmann_distribution)
    - 因此，$S'$既可以来自删掉任意一点后的$S$，也可以来自增加任意一点后的$S$（可视为**撤销**操作）
    - 算法中的$T$表示温度
        - 当$T \rightarrow +\infty$时，概率$e^{-\frac{\Delta \text{cost}}{kT}} \rightarrow 1$，容易引起底部振荡（也就是说无论在何种情况下，$S'$会不断更新）
        - 当$T \rightarrow 0$，概率$e^{-\frac{\Delta \text{cost}}{kT}} \rightarrow 0$，此时该算法接近原始的梯度下降法
- 设计该算法的难点在于寻找合适的温度值——这里采用**模拟退火**(simulated annealing)的算法。该算法的名称来自于冶金学术语“退火”：让材料从很高的温度开始**慢慢**冷却，使我们有充足的时间在一系列不断减小的中间温度值$T = \{T_1, T_2, \dots\}(T_1 \ge T_2 \ge \dots)$中找到平衡点(equilibrium)（即最优解）
---

### 2. Hopfield Neural Networks
> [!question]
> 给定一张图 $G = (V, E)$，每条边都有一个整数（不论正负）的权重 $w$，其绝对值 $|w|$ 称为需求强度(strength of requirement)；每个顶点的取值（称为状态(state)）$s$ 为 $\pm 1$
> 
> 对于边$e = (u, v)$：
> - 如果 $w_e < 0$，那么 $u$ 和 $v$ 具备相同的状态（都为 $-1$ 或都为 $1$）
> - 如果 $w_e > 0$，那么 $u$ 和 $v$ 具备不同的状态（一个为 $-1$，另一个为 $1$）
> 
> 题目的输出为：网络的一种布局(configuration) $S$ ——所有顶点的状态集合，每个顶点 $u$ 都被赋予一个状态 $s_u$

需要注意的是：可能不存在能够满足所有边的需求的布局，比如这张图：
<div style="text-align: center">
 <img src="images/lec12/16.png" width="30%">
</div>
因此需要找到一种**足够好**(sufficiently good)的布局：
**【Definition】**
1. 在一种布局中，如果 $w_e s_u s_v < 0$，称边 $e = (u, v)$ 是一条**好边**，否则称其为一条**坏边**
2. 在一种布局中，如果一个顶点的关联(incident)（即该点作为某条边的端点）好边的总权重不小于关联坏边的总权重，称这个点为==满意(satisfied)点==，即满足：
$$\sum\limits_{v:e=(u, v) \in E}w_e s_u s_v \le 0$$
- 如果一张图的所有顶点都是满意点，那么称这个布局是==稳定的(stable)==

> [!example]
> Q：根据给定边的权重，请找出一个稳定的布局
> 
>  <div style="text-align: center"><img src="images/lec12/17.png" width="30%"></div>
>  
> A：这里给出其中一种可能的稳定布局：
>  <div style="text-align: center"><img src="images/lec12/18.png" width="30%"></div>
>  
>  通过计算发现坏边的两个端点的总权重均小于0，满足定义，因此所有点都是满意点，这种布局是稳定的。

下面给出一种寻找稳定布局的算法——**状态翻转**(state-flipping)算法：
```c
ConfigType State_flipping() {
    Start from an arbitrary configuration S;
    while (!IsStable(S)) {
        u = GetUnsatisfied(S);
        s_u = -s_u;
    }

    return S;
}
```

整体思路：
- 只要布局不是稳定的，算法就会找出不满意点并翻转它的状态，这样就能使其变成满意点，直到所有的点都是满意点为止。
Claim：
- 该算法在至多 $W = \sum_e|w_e|$ 次迭代后终止
> [!proof]
> 令势能函数 $\Phi(S) = \sum_{e \text{ is good}}|w_e|$，当顶点 $u$ 翻转状态时（$S$ 会变成 $S'$）
> - 所有与 $u$ 关联的好边都变成了坏边
> - 所有与 $u$ 关联的坏边都变成了好边
> - 其他边保持不变

因此：
$$\Phi(S') = \Phi(S) - \sum\limits_{e:e=(u,v) \in E \atop e \text{ is bad}}|w_e| + \sum\limits_{e:e=(u,v) \in E \atop e \text{ is good}}|w_e|$$
由于每次翻转的是不满意点，因此翻转之后，好边的权重绝对值之和是**严格递增**的。在最坏的情况下，一个布局的所有边都是坏边，最后都变成了好边，那么所需要的迭代次数就是 $W$ 了。
- 因此可以得到 $0 \le \Phi(S) \le W$

下面从【**局部搜索**】算法的角度重新审视这道题：
- 问题：找到最大的$\Phi$
- 可行解集$FS$：某种布局
- $S \sim S'$：$S'$ 可通过对 $S$ 的某个顶点的状态翻转后得到

**结论**：
- 任意一种在状态翻转算法中得到的**局部最大**的 $\Phi$ 的最优布局是一种**稳定的布局**
- 局部最优 $\rightarrow$ 全局最优

这不是一个多项式时间的算法，因为时间复杂度与**边的绝对值权重和**相关，而权重的绝对值可以很大
- 至今还未找到多项式时间下构建稳定布局的算法
---

### 3. Maximum Cut Problem
> [!question]
> **最大割问题**(maximum cut problem)：给定一张无向图$G = (V, E)$，每条边都有一个**正整数权重**$w_e$，请找到一种顶点划分(node partition)$(A, B)$（即对于所有顶点，要么属于集合$A$，要么属于集合$B$），使得割之间的所有边的权重和$w(A, B) = \sum\limits_{u \in A, v \in B} w_{uv}$最大。

现在从局部搜索的角度审视此题：
- 问题：使$w(A, B)$尽可能大
- 可行解集$FS$：任意划分$(A, B)$
- $S \sim S'$：通过将$S$中的某个顶点从划分$A$移动到划分$B$，或从划分$B$移动到划分$A$来得到$S'$

这道题和 Hopfield 问题十分相似：所有边权重非负，此时分成 $A, B$ 集合就相当于给每个点 $-1$ 或 $1$ 的状态，此时希望好边（两端点状态不同的边）权重和最大。依然使用翻转法，因为已经证明翻转过程中好边的绝对值不断增大。最终状态终止于所有点都是稳定点。

然而，这种算法终止情况是<u>不存在不稳定点</u>，只是一个对最优解的近似：
- 局部最优解有多好？
    - **结论**：令 $(A, B)$ 为一种局部最优的划分，$(A^*, B^*)$ 为一种全局最优的划分，那么 $w(A, B) \ge \dfrac{1}{2}w(A^*, B^*)$
	- 换句话说，局部最优解得到的最大割至少是全局最优解的一半
> [!proof]
> 因为$(A, B)$是局部最优划分，所以$\forall u \in A$，可以得到：
> $$\sum\limits_{v \in A} w_{uv} \le \sum\limits_{v \in B} w_{uv}$$
> 将所有的顶点$u \in A$累加起来，得到：
> $$\begin{align}2 \sum\limits_{ \{u, v\} \subseteq A} w_{uv} = \sum\limits_{u \in A} \sum\limits_{v \in A} w_{uv} \le \sum\limits_{u \in A} \sum\limits_{v \in B} w_{uv} = w(A, B)\tag{1} \end{align}$$
> 同理得：
> $$\begin{align}2 \sum\limits_{ \{u, v\} \subseteq B} w_{uv} \le w(A, B)\tag{2}\end{align}$$
> $(1) + (2)$并化简，得到：
> $$w(A^*, B^*) \le W \le \sum\limits_{ \{u, v\} \subseteq A} w_{uv} + \sum\limits_{ \{u, v\} \subseteq B} w_{uv} + w(A, B) \le 2w(A, B)$$
> - 所以，状态翻转算法在本题是一种**2-近似算法**

- 能否在多项式时间内得到结果？
    - **大提升翻转**(big-improvement-flip)：该只挑选能够提升至少 $\dfrac{2\varepsilon}{|V|}w(A, B)$ 割值的顶点来翻转，如果找不到满足提升的解，就终止迭代
    - 相关结论：
        - 算法结束后得到的割集 $(A, B)$，满足：$(2 + \varepsilon)w(A, B) \ge w(A^*, B^*)$，因此该算法是一个 $(2 + \varepsilon)$ -近似算法
> [!proof]
> - 根据条件，对于 $u \in A$，我们可以得到不等式：
>   $$\sum\limits_{v \in A} w_{uv} \le \sum\limits_{v \in B} w_{uv} + \dfrac{\varepsilon}{n}w(A, B)$$
>   后续证明过程与前一个证明类似，故不再展开叙述。
>   
> 最终得到
> $$
> w(A^*, B^*) \le W \le \sum\limits_{ \{u, v\} \subseteq A} w_{uv} + \sum\limits_{ \{u, v\} \subseteq B} w_{uv} + w(A, B) \le \frac{\varepsilon}{2}w(A, B)+\frac{\varepsilon}{2}w(A, B)+w(A, B)
> $$

- 该算法能够在至多$O(\dfrac{n}{\varepsilon} \log W)$次翻转后终止，其中$W = \sum w$
> [!proof ]
> - 根据前面的证明知，每次翻转后，$w(A, B)$会提升$(1 + \dfrac{\varepsilon}{n})$倍
> - 由不等式$(1 + \dfrac{1}{x})^x \ge 2, \forall x \ge 1$知，$(1 + \dfrac{\varepsilon}{n})^{\frac{n}{\varepsilon}} \ge 2, \forall \dfrac{\varepsilon}{n} \ge 1$
> - 我们的目标是最大化$w(A, B)$，即令$w(A, B) \rightarrow W$，那么由上面的不等式知，要使$w(A, B)$从最低值1出发提升$W$倍，就需要翻转$O(\dfrac{n}{\varepsilon} \log W)$。得证。

- 是否存在一种更好的「局部」？
    - 一个好的「局部」需要满足：
        - 解的邻居需要足够大，使得算法不会陷入局部最优解而“出不来”
        - 但解的邻居也不能太大，因为我们希望能够在有限的步数内，在邻居集中高效地寻找最优解
    - 要想寻找一个更好的局部解，一个简单的想法是使用前面介绍过的状态翻转算法来翻转$k$个顶点，这样得到了一个$k$翻转的邻居关系，
        - 若$(A, B)$和$(A', B')$是$k$翻转的邻居关系，则对于$k' > k$，$(A, B)$和$(A', B')$也是$k'$翻转的邻居关系。所以我们可以通过不断增大$k$找到更好的邻居关系，从而减小近似比
        - 但是该方法的搜索空间为$\Theta(n^k)$，当$k$稍微变大时时间复杂度就会变得很大，不太令人满意
    - **K-L启发式算法**(K-L heuristic)，执行步骤如下：
        - 第1步：make 1-flip as good as we can -> 得到最优解 $(A_1, B_1)$，被翻转的顶点记为 $v_1$
            - 时间复杂度：$O(n)$
        - 第k步：make 1-flip of an *unmarked* node as good as we can -> 得到最优解 $(A_k, B_k)$，被翻转的顶点为 $v_1, \dots, v_k$
            - 时间复杂度：$O(n - k + 1)$
        - 第n步：$(A_n, b_n) = (B, A)$
        - 因此，划分$(A, B)$的邻居集为$\{(A_1, B_1), \dots, (A_{n - 1}, B_{n - 1})\}$，时间复杂度为$O(n^2)$