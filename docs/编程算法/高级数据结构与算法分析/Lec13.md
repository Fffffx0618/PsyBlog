# Randomized Algorithms
## 13.1 Introduction
What to Randomize?
- **数据**的随机化：传统的算法可根据随机生成的输入数据得到结果
    - 由于数据是随机的（可以理解为数据是等概率分布的），因此对这种算法的分析称为**平均情况分析**(average-case analysis)
- **算法**的随机化：算法在处理最坏情况的输入时会做出**随机的决策**
    - 这样的算法被称为**随机化算法**(randomized algorithm)

Why Randomize？
- 可以将那些始终能够得到正确答案的、高效可确定(efficient deterministic)的算法（就是传统意义上的算法）视为随机化算法的一种**特殊情况**
- 随机化算法的分类：
    - 高效性：efficient randomized algorithms that only need to yield the correct answer with *high probability*
	    只需在**较高概率**下得到正确解的**高效**随机化算法
    - 确定性：randomized algorithms that are always correct, and run efficiently *in expectation*
	    只需在**预期**效率内始终得到**正确解**的随机化算法
> [!example]
> 在分布式的系统中，对所有进程进行**对称分解**(symmetry-breaking)这一随机化算法，实现整个系统的负载均衡(load balance)，这种方法相对比较简单。

**A quick review**:
- $Pr[A]$：事件$A$发生的**概率**
- $\overline{A}$：事件$A$的**补**(complement)，可以得到：$Pr[A] + Pr[\overline{A}] = 1$
- $E[X]$：随机变量$X$的**期望**(expectation)
    - $E[X] = \sum\limits_{j = 0}^{\infty} j \cdot Pr[X = j]$

---
## 13.2 Hiring Problems
> [!question]
> - Hire an office assistant from headhunter 
> - Interview <u>a different applicant per day</u> for $N$ days
> - $\text{Interviewing Cost} = C_i  <<  \text{Hiring Cost} = C_h$
> - Analyze <u>interview & hiring cost</u> instead of running time
> 
> Assume $M$ people are hired, Total Cost: $O(NC_i+MC_h)$

> [!failure] Naive Solution
> ```c
> int Hiring(EventType C[], int N) {
>     // candidate 0 is the least-qualified dummy candidate
>     int Best = 0;
>     int BestQ = the quality of candidate 0;
>     for (i = 0; i <= N; i++) {
>         Qi = interview(i);    // Ci
>         if (Qi > BestQ) {
>             BestQ = Qi;
>             Best = i;
>             hire(i);          
>             // Ch
>         }
>     }
>     return Best;
> }
> ```
> - 采取的策略：每次能被雇佣的候选者的能力需要**高于**已被雇佣的候选者
> - Worst Case：候选者根据能力大小按顺序进行面试，那么每个人都会被雇佣，因此时间复杂度为 $O(NC_h)$（由于 $C_i$ 很小，直接忽略掉）

### 13.2.1 Offline Algorithm
<font color="#245bdb">Randomness assumption</font>: 
- any of first $i$ candidates is *equally* likely to be best-qualified so far

Assume candidates arrive in *random* order： 
- 令$X$为雇佣人数，那么$E(X) = \sum\limits_{j=1}^N j \cdot Pr[X = j]$，接下来需要确定$Pr[X = j]$的值
- 令$X_i = \begin{cases}1 & \text{if candidate } i \text{ is hired} \\ 0 & \text{if candidate } i \text{ is NOT hired}\end{cases}$，那么$E[X_i] = Pr[\text{candidate } i \text{ is hired}] = \dfrac{1}{i}$
- 那么$E[X] = E[\sum\limits_{i=1}^N X_i] = \sum\limits_{i=1}^N E[X_i] = \sum\limits_{i=1}^N \dfrac{1}{i} = \ln N + O(1)$
- 所以总成本为 $O(C_h \ln N + NC_i)$

#### Randomized Algorithm
```c
int Hiring(EventType C[], int N) {
    // candidate 0 is the least-qualified dummy candidate
    int Best = 0;
    int BestQ = the quality of candidate 0;

    randomly permute the list of candidates; 

    for (i = 1; i <= N; i++) {
        Qi = interview(i);    // Ci
        if (Qi > BestQ) {
            BestQ = Qi;
            Best = i;
            hire(i);          
            // Ch
        }
    }
    return Best;
}
```
- 在处理数据前先对数据进行**随机排列**(permute)，即可得到随机排序的数据（而不再是一个假设），从而避免了最坏情况；但缺点在于随机排列数据需要额外的时间成本

#### Randomized Permutation Algorithm
Idea: Assign each element A\[i\] a *random priority* P\[i\], and sort
```c
void PermuteBySorting (ElemType A[], int N) {
	for (i = 1; i <= N; i++) {
    	A[i].P = 1 + rand() % (N * N * N);
    	// makes it more likely that all priorities are unique
    }
    Sort A, using P as the sort keys;
}
```
- Claim：假定数组元素的优先级都是唯一的，那么该算法能够产生一个基于原输入数据的**均匀随机排列(uniform random permutation)**（即等可能地从所有可能的排列中选取其中一种排列）

### 13.2.2 Online Algorithm
该算法的大致思路：
- 先面试前 $k$ 个候选者，找到他们中最高的能力值并以它为阈值，但全部不雇佣；
- 然后面试后面的候选者，如果出现某位高于这个阈值的候选者，就雇佣这个人并停止面试
```c
int OnlineHiring(EventType C[], int N, int k) {
    int Best = N;
    int BestQ = -Infinity;

    for (i = 1; i <= k; i++) {
        Qi = interview(i);
        if (Qi > BestQ) BestQ = Qi;
    }

    for (i = k + 1; i <= N; i++) {
        Qi = interview(i);
        if (Qi > BestQ) {
            Best = i;
            break;
        }
    }

    return Best;
}
```
Two questions：
1. 对于给定的 $k$，我们能雇佣到能力最高的候选者的概率是多少？
    - $S_i:=\text{the ith applicant is the best}$ 
    - 如何让事件 $S_i$ 是 TRUE 的（$A$ 和 $B$ 事件是**独立**的）：  $$
      \{A:=\text{the best one is at position i} \}\cap \{B:=\text{no one at positions from k+1 to i-1 are hired}\}
      $$
    - 计算概率：$$
        \begin{align}
        Pr[S_i] & = Pr[A \cap B] = \underbrace{Pr[A]}_{\frac{1}{N}} \cdot \underbrace{Pr[B]}_{\frac{k}{i - 1}} = \dfrac{k}{N(i - 1)} \notag \\
        Pr[S] & = \sum\limits_{i=k+1}^N Pr[S_i] = \sum\limits_{i=k+1}^N \dfrac{k}{N(i-1)} = \dfrac{k}{N} \sum\limits_{i=k}^{N-1}\dfrac{1}{i} \notag
        \end{align}
        $$
    - 根据不等式$\int_k^N \dfrac{1}{x} \text{d}x \le \sum\limits_{i=k}^{N-1} \dfrac{1}{i} \le \int_{k-1}^{N-1} \dfrac{1}{x}\text{d}x$，最终可得：$$
    \dfrac{k}{N} \ln(\dfrac{N}{k}) \le Pr[S] \le \dfrac{k}{N} \ln (\dfrac{N - 1}{k - 1})
    $$
2. 最佳的 $k$ 值（即能够得到最大的概率）是多少？
    - 问题可以被转化为：求函数 $f(k) = \dfrac{k}{N} \ln (\dfrac{N}{k})$ 的最大值下对应的 $k$ 值
    - 对该函数求导，得 $\dfrac{\text{d}}{\text{d}k}[\dfrac{k}{N} \ln (\dfrac{N}{k})] = \dfrac{1}{N} (\ln N - \ln k - 1) = 0$，解得 $k = \dfrac{N}{e}$
    - 结论：上述算法雇佣到**能力最佳**的候选者的概率**至少**为$\dfrac{1}{e}$
> [!bug]
> 如果能力最佳的候选者出现在前$k$个人里面，那么这种在线算法就无法得到正确结果，因此该算法**无法保证**总是能够找到正确解。

---
## 13.3 Randomized Quicksort
**确定性的快速排序**(deterministic quicksort)的时间复杂度为：
- $\Theta(N^2)$：最坏情况下的运行时间
- $\Theta(N \log N)$：平均情况下的运行时间（假设各情况出现的概率相等）

确定性的快排是基于<u>每种输入排列是等可能分布</u>的假设，它没有很好地处理最坏情况。要想避免最坏情况，可以用**随机化算法**来解决。
> [!info] Idea 
> 通过随机选择并保证每次划分都有足够平衡（中心分离点），我们可以使快速排序的期望时间复杂度稳定在 $O(N\log{N})$，且每步只需常数次尝试即可找到合适 pivot

**随机化快排**的关键在于<u>随机且均匀地挑选支点(pivot)</u>，挑选原则为：
- ==中心分离点(Central splitter)==：the **pivot** that divides the set so that each side contains *at least n/4*
    - 这样就可以消除支点出现在数据两端（相当于没有分）的最坏情况
    <div style="text-align: center">
        <img src="images/lec13/1.png" width="40%">
    </div>
    
- ==修改后的快速排序(Modified Quicksort)==：在递归前始终能够选出一个中心分离点
结论：寻找中心分离点的**迭代次数的期望值**至多为 $2$
- 解释：Pr\[find a central splitter\] = 1/2， $E = \sum_{i=1}^\infty i \cdot \dfrac{1}{2^i} = 2$

**时间复杂度分析**：
**Type j**：the subproblem $S$ is of **type j** if $N(\dfrac{3}{4})^{j+1} \le |S| \le N(\dfrac{3}{4})^j$
- $\dfrac{3}{4}$ 表示选择了处于边界的中心分离点，此时数据被分为了 $\dfrac{1}{4}N$ 和 $\dfrac{3}{4}N$ 两部分，我们更关心每此快排后最大的子问题 $S$
**Claim**：类型 $j$ 至多有 $(\dfrac{4}{3})^{j+1}$ 个子问题
- 解释：根据上述不等式，对于第 $j$ 趟快排，最大子问题的最小规模为 $N(\dfrac{3}{4})^{j+1}$，因此最多有 $\dfrac{N}{N(\frac{3}{4})^{j+1}} = (\dfrac{4}{3})^{j+1}$ 个子问题
1. $E[T_{\text{type } j}] = O(N(\dfrac{3}{4})^j) \times (\dfrac{4}{3})^{j+1} = O(N)\Rightarrow$ 每一类 type j 的总处理时间是 $O(N)$
2. Number of different types =  $\log_{\frac{4}{3}}N = O(\log N)$
- 上面两条的结果相乘，可见随机化快排的时间复杂度为稳定的 $O(N \log N)$




