# Parallel Algorithms
## 14.1 Introduction
**并行**(parallelism)：<u>每一步能够同时完成多个操作</u>。有以下几类并行方式：
- ##### Machine Parallelism
	- Pipelining：将一条指令的执行过程分解为多个阶段，每个阶段由不同的硬件单元负责
	- Very-Long Instruction Word, VLIW：每条指令包含多个操作，在同一周期内并行执行
	- Processor parallelism：使用多个处理器核心（或多个CPU）协同工作来完成任务
- ##### Parallel Algorithm
	- 从**软件/算法设计**角度研究如何利用并行性解决问题的方法
为了描述 parallel algorithm，引入==Parallel Random Access Machine（PRAM, 并行随机存取机）==
### 1. Parallel Random Access Machine
<div style="text-align: center">
    <img src="images/lec14/1.png" width="40%">
</div>

- $P_1, \dots, P_n$表示$n$个处理器，它们同时访问一块共享内存
- 处理器与共享内存间的双向箭头表示**单位时间内对内存的访问**（包括读、写、计算等操作）
    - 向上的箭头表示读取，向下的箭头表示写入
> [!example]
> Example 1：处理器i执行操作：`c := a + b`
> - 读取 $a$ 和 $b$ 的值，计算 $a+b$ 后写入 $c$
>  <div style="text-align: center"><img src="images/lec14/2.png" width="40%"></div>
>  
>  Example 2：将每个处理器的结果写入到内存对应位置上
>  
>  ```c
>  for P_i, 1 <= i <= n pardo
> 	 A(i) := B(i)
> // pardo: do parallelly，即并行执行循环；因此实际上执行这个循环所需时间为 O(1)
>  ```
>  <div style="text-align: center"><img src="images/lec14/3.png" width="40%"></div> 

**To slove access conflicts**:
1. <u>Exclusive-Read Exclusive-Write</u>（EREW，专一读取-专一写入）
	- 同一时间内不允许多个处理器访问（读/写）同一块内存
2. <u>Concurrent-Read Exclusive-Write</u>（CREW，并发读取-专一写入）
3. <u>Concurrent-Read Concurrent-Write</u>（CRCW，并发读取--并发写入），有三种写入规则：
    - Arbitrary rule：**任意选择**一个处理器进行写入操作
    - Priority rule：选择**编号最小**的处理器（规定编号越小优先级越高）进行写入操作
    - Common rule：只有当所有处理器的写入数据是**一致**的时候，才会执行写入操作

> [!example] The summation problem
> - Input：$A(1), A(2), \dots, A(n)$
> - Output：$A(1) + A(2) + \dots + A(n)$
>   <div style="text-align: center"><img src="images/lec14/4.png" width="75%"></div>
>    
>  - 最底层表示初始情况，每层表示并行算法的每个步骤；每层都有8个处理器，空白圆圈表示空闲的处理器；整个过程中所有工作的处理器构成了一棵**满二叉树**
> 	 - 因此层数为 $\log n$，即算法在 $\log n$ 时间内完成
>  - $B(h, i)$表示第$h$步中第$i$个处理器的计算结果
> 	 - 有以下关系式成立：$B(h, i) = B(h - 1, 2i - 1) + B(h - 1, 2i)$
> ```c
> for P_i, 1 <= i <= n pardo
>     B(0, i) := A(i)
>     for h = 1 to log(n) do
>         if i <= n / 2^h:
>             B(h, i) := B(h - 1, 2 * i - 1) + B(h - 1, 2 * i)
>         else
>             stay idle
>     if i = 1:
>         output B(log(n), 1)
>     else:
>         stay idle
> ```
> - 上层的节点需要知道下层的两个节点值才能计算。由于外层循环是并行计算的，说明这棵树上<u>同一层的节点是**同时**算出来的</u>
> - 时间复杂度：$T(n) = \log n + 2$
>   
> **操作数量和时间**之间的关系如下图：
> <div style="text-align: center"><img src="images/lec14/5.png" width="35%"></div> 
> 
> - 横轴上的最大值为$p$，等于用到过的处理器的最大数量
> - 纵轴上的最大值为$t$，表示总的运行时间
> - 每个横条表示一个阶段（单位时间），蓝色部分表示工作的处理器，灰色部分表示空闲的处理器

> [!bug] PRAM模型的缺陷"
> - 该模型无法揭示算法和实际使用的处理器个数之间的关系
> - 对于上个例子，假如有100个处理器，但实际上只用了8个处理器，所以更多的处理器并不能使执行速度进一步加快
> - 该模型需要指定哪个处理器处理哪部分的指令，这时就需要知道更多的细节

### 2. Word & Depth Model
```c
//A Parallel Algorithm for the Summation Problem
For i, i<=i<=n pardo
	B(0,i) := A(i)
	
for h = 1 to log(n)
	for i, i<=i<=n/2^h pardo
		B(h, i) := B(h-1, 2i-1) + B(h-1, 2i)

output B(log(n), 1)
```
令 $T_p$ 为此算法在 $p$ 个处理器上的运行时间
- $T_1 = \Theta (n),\quad T_{\infty} = \log (n)$

> [!question] What about $T_p$ for arbitrary $p$? 
> - An accurate analysis can be tedious. (should specify the allocation of instructions to processors) 
> - Unrealistic to go through all possible $p$

> [!info] Bounding $T_p$ ​ using work and depth
> For a parallel algorithm,
> - Its *work* $W$ is the total amount of unit-time operations required to complete this algorithm
> $$W=T_1$$ 
> - Its *depth* $D$ is the length of the longest chain of sequential dependencies. (Intuitively, depth measures how parallel this algorithm is)
>  $$D=T_{\infty}$$
>  代入到上述算法，得到 $W=\Theta (n)$, $D=\Theta(\log n)$，因此
>  $$\Theta(\frac{n}{p})\leq T_p \leq \Theta(\frac{n}{p}+\log n)$$

>[!tip] Brent’s Theorem
>  $$\dfrac{W}{p} \leq T_p \leq \dfrac{W}{p}+D$$
#### Work-Depth (WD) Presentation
```c
for P_i, 1 <= i <= n pardo
    B(0, i) := A(i)
for h = 1 to log(n) do
    for P_i, i <= n / 2^h pardo
        B(h, i) := B(h - 1, 2 * i - 1) + B(h - 1, 2 * i)
for i = 1 pardo
    output B(log(n), 1)
```
- 这里用到的是并行处理的方式（`pardo`），而且不再显式指出不工作的处理器

因此对应的操作数量和时间之间的关系图变成了：
<div style="text-align: center">
    <img src="images/lec14/6.png" width="30%">
</div> 

由于没有了那些灰色区域（不工作的处理器），因此这张图更清楚地反映了真实情况下各个时间段内的用到的处理器数量。对于更一般的情况，如下所示：
<div style="text-align: center">
    <img src="images/lec14/7.png" width="30%">
</div> 

- 每个时间段处于工作状态的处理器数量，即工作量是不一样的，且没有任何规律可言。

### 3. Measurement
衡量 PRAM 模型下并行算法的性能的一些指标：
- $W(n)$：**工作量**(workload)，即运行并行算法所需的总操作数目
- $T(n)$：最坏情况下的运行**时间**（准确说是**处理器数量无穷多时**所需的运行时间）
- $P(n)=\dfrac{W(n)}{T(n)}$：所需处理器的数量
- 当所需处理器数量 $p≤\frac{W(n)}{T(n)}$ 时，所需时间为 $\dfrac{W(n)}{p}$
- 使用任意数量为 $p$ 的处理器时，所需时间为 $\dfrac{W(n)}{p}+T(n)$
后面那三个指标是**渐进等价的**(asymptotically equivalent)，即对于任意大的 $n$，这三者位于同一复杂度下

---
## 14.2 Prefix-Sums
> [!question]
> - Input：$A(1), A(2), \dots, A(n)$
> - Output：$\sum\limits_{i=1}^1A(i), \sum\limits_{i=1}^2A(i), \dots, \sum\limits_{i=1}^nA(i)$

<div style="text-align: center">
    <img src="images/lec14/8.png" width="50%">
</div> 
规定**前缀和**$C(h, i) = \sum\limits_{k=1}^\alpha A(k)$，其中$(0, \alpha)$表示二叉树的节点$(h, i)$最右侧路径上的叶子节点的位置
### 1. Case1
<div style="text-align: center">
    <img src="images/lec14/10.png" width="50%">
</div> 
计算**最左边路径**上的节点：
```c
if (i == 1)
    C(h, i) := B(h, i)
```
### 2. Case2
<div style="text-align: center">
        <img src="images/lec14/11.png" width="50%">
    </div>
计算每一层偶数位上的节点：
```c
if (i % 2 == 0)
    C(h, i) := C(h + 1, i / 2)
```
### 3. Case3
<div style="text-align: center">
    <img src="images/lec14/12.png" width="50%">
</div>
计算除最左边路径外每一层奇数位上的节点：
```c
if (i % 2 == 1 && i != 1)
    C(h, i) := C(h + 1, (i - 1) / 2) + B(h, i)
```
- 计算 $C(h, i)$ 时没有利用与它同一级上的节点，这是因为每层都是**并行计算**的，只能利用上一级的计算值以及自身的值。
### 4. Code Implement
- 先**自底向上**计算求和问题，然后根据求和问题的结果**自顶向下**计算前缀和问题
- 这两趟计算都用到了==并行算法==
```c
// Same as summation problem
for P_i, 1 <= i <= n pardo
    B(0, i) := A(i)
for h = 1 to log(n)
    for i, 1 <= i <= n / 2^h pardo
        B(h, i) := B(h - 1, 2 * i - 1) + B(h - 1, 2 * i)

// Now calculate the prefix sum problem
for h = log(n) to 0
    for i even, 1 <= i <= n / 2^h pardo
        C(h, i) := C(h + 1, i / 2)
    for i = 1 pardo
        C(h, 1) := B(h, 1)
    for i odd, 3 <= i <= n / 2^h pardo
        C(h, i) := C(h + 1, (i - 1) / 2) + B(h, i)
for P_i, 1 <= i <= n pardo
    Output C(0, i)
```
- 时间复杂度：$T(n) = O(\log n)$
- 工作量：$W(n) = O(n)$

---
## 14.3 Merging
> [!question]
> 合并两个**非递减**的数组 $A(1), A(2), \dots, A(n)$ 和数组 $B(1), B(2), \dots, B(m)$ 至另一个**非递减**的数组 $C(1), C(2), \dots, C(n + m)$

为了简化后面的分析，做如下假设：
- 数组 $A, B$ 中的元素互不相同
- 令 $n = m$
- $\log n, \dfrac{n}{\log n}$ 的结果均为整数

**划分范式**(Partitioning Paradigm)
- partitioning：将输入数据划分为 $p$ 个独立的小任务，每个小任务的规模大致为 $\dfrac{n}{p}$
- actual work：并发执行这些小任务，对于每个小任务使用（顺序）算法来解决

可以将问题转化为**排行**问题(ranking)，规定数组$B$中第$j$个元素在数组$A$中的排行为：
$$
\text{RANK}(j, A) = \begin{cases}i & \text{if } A(i) < B(j) < A(i + 1), \text{for } 1 \le i < n \\ 0 & \text{if } B(j) < A(1) \\ n & \text{if } B(j) > A(n)\end{cases}
$$

那么排行问题，也就是 $\text{RANK}(A, B)$，需要计算的东西为：
1. $\text{RANK}(i, B)$ for every $\forall 1 \le i \le n$, and
2. $\text{RANK}(i, A)$ for every $\forall 1 \le i \le n$

伪代码如下所示：
```c
for P_i, 1 <= i <= n pardo
    C(i + RANK(i, B)) := A(i)
for P_i, 1 <= i <= n pardo
    C(i + RANK(i, A)) := B(i)
```
结论：根据排行问题给出的解，**合并问题**可以在 $O(1)$ 时间内得到结果，且工作量为 $O(n + m)$。该算法的速度非常快，但是工作量没有得到优化。

> [!example]
> - 对以下两个数组，先分别给出它们的排行，然后合并这两个数组。
> <div style="text-align: center"><img src="images/lec14/13.png" width="50%"></div>
> 
> - 答案
> <div style="text-align: center"><img src="images/lec14/14.png" width="50%"></div>

### Ranking Problem
#### Binary Search
```c
for P_i, 1 <= i <= n pardo
    RANK(i, B) := BS(A(i), B)
    RANK(i, A) := BS(B(i), A)
```
- 时间复杂度：$T(n) = O(\log n)$
- 工作量：$W(n) = O(n \log n)$
- 用到的处理器数：$p = n$
#### Serial Ranking
```c
i = j = 0
while (i <= n || j <= m){
    if (A(i + 1) < B(j + 1))
        RANK(++i, B) = j;
    else 
        RANK(++j, A) = i;
}
```
- 时间复杂度：$T(n) = O(n + m)$
- 工作量：$W(n) = O(n + m)$
- 用到的处理器数：$p = 1$
#### Parallel Ranking
- 假设 $n = m$，且确保 $A(n + 1), B(n + 1)$ 比 $A(n), B(n)$ 都要大
- Stage1: **Partitioning**，令处理器数量 $p = \dfrac{n}{\log n}$，对 $1 \le i \le p$，有：
    - $A_{\text{Select}}(i) = A(1 + (i - 1)\log n)$
    - $B_{\text{Select}}(i) = B(1 + (i - 1)\log n)$
    - 计算被选中的元素的 RANK
- Stage2: **Actual Ranking**
    - 划分以后，整个问题被分为**至多**有 $2p$ 个规模为 $O(\log n)$ 的子问题
    - $T=O (\log{n}),W=O(n)$

> [!example]-
> 原数组
> <div style="text-align: center"><img src="images/lec14/15.png" width="60%"></div>
> 
> 选中元素
> <div style="text-align: center"><img src="images/lec14/16.png" width="60%"></div>
> 
> 对这些元素进行排行
> <div style="text-align: center"><img src="images/lec14/17.png" width="60%"></div>
> 
> 得到子问题
> <div style="text-align: center"><img src="images/lec14/18.png" width="60%"></div>
> 绿色部分表示一个个的子问题

> [!tip] Analysis
> - Partitioning：
> 	- 时间：$T = O(\log n)$
> 	- 工作量：$W = O(p \log n) = O(n)$
> - Actual ranking：
> 	- 时间：$T = O(\log n)$
> 	- 工作量：$W = O(p \log n) = O(n)$
> - Conclusion：
> 	- 时间：$T = O(\log n)$
> 	- 工作量：$W = O(p \log n) = O(n)$

---
## 14.4 Maximum Finding
> [!question]
> $n$个元素中找到最大值
### 1. Naive Ideas
#### Replace "+" by "max" in the summation algorithm
- 时间：$T(n) = O(\log n)$
- 工作量：$W(n) = O(n)$
#### Compare all pairs    
```c
for P_i, 1 <=i<= n pardo
	B(i) := 0
for i and j, 1<=i, j<=n pardo
    if (A(i) < A(j) || A(i) == A(j) && i<j)
        B(i) = 1
    else
        B(j) = 1
for P_i, 1 <=i<= n pardo
    if B(i) == 0
    	A(i) is a maximum in A
```
- 时间：$T(n) = O(1)$
- 工作量：$W(n) = O(n^2)$
> [!bug] How to resolve access conflits?
> - 由于是并行比较 $O(n^2)$ 对元素，因此不可避免地会出现多个处理器访问相同元素的冲突。
> - 解决方案：<u>PRAM模型-CRCW策略-共同规则</u>（当所有处理器写入相同的数据时才能进行写入操作）

### 2. A Doubly-Logarithmic Paradigm
**原始策略**：
将问题划分为 $\sqrt{n}$ 个规模为 $\sqrt{n}$ 的子问题：
$$
\begin{align}
A_1 &= A(1), \dots, A(\sqrt{n}) \quad \Rightarrow M_1 \\
A_2 &= A(\sqrt{n} + 1), \dots, A(2 \sqrt{n}) \quad \Rightarrow M_2 \\
&\cdots\\
A_{\sqrt{n}} &= A(n - \sqrt{n} + 1), \dots, A(n) \quad \Rightarrow M_{\sqrt{n}}
\end{align}
$$
最后从每个子问题得到的最大值 $M_1, M_2, \dots M_{\sqrt{n}}$ 中选取最大值为 $A_{max}$
> [!tip] Analysis
> - 对于每个子问题，采用**顺序算法**找最大值，所需时间为$T(\sqrt{n})$，工作量为$W(\sqrt{n})$
> - 采用两两比较从子问题的最大值中寻找整个问题的最大值，所需时间为 $T(1)$，工作量为 $W((\sqrt{n})^2) = O(n)$
> - 由于是并行解决 $\sqrt{n}$ 个子问题，因此对于总问题而言，有以下递推式成立：
> 	- $T(n) \le T(\sqrt{n}) + c_1$（$c_1 = O(1)$）
> 	- $W(n) \le \sqrt{n}W(\sqrt{n}) + c_2 n$（$c_2 = O(n)$）
> - 根据递推式，最终解得：
> 	- 时间：$T(n) = O(\log \log n)$
> 	- 工作量：$W(n) = O(n \log \log n)$
> 
> 可以看到，虽然工作量下降了，但是所需时间却变多了。

> [!prove]-
> #### 求解 $T (n)$
> 1. 变量代换
> 令 $n = 2^{2^k} \Rightarrow  \sqrt{n} = 2^{2^{k-1}}$
> 设 $S(k) = T(2^{2^k})=T(n)$, 那么原递推可变为 $S(k) \leq S(k-1) + O(1)$
> 2. 求解递推
> 求解得到 $S(k) = O(k)$，回代 $k$，可以得到 $T(n) = S(k) = O(k) = O(\log \log n)$
> 
> #### 求解 $W (n)$
> 1. 变量代换
> 令 $n = 2^k$ ，那么 $\sqrt{n} = n^{1/2} = (2^k)^{1/2} = 2^{k/2}$
> 设 $S(k) = W(2^k) = W(n)$，递推式 $W(n) = \sqrt{n} W(\sqrt{n}) + n$ 代入新变量得：
> $$ S(k) = 2^{k/2} S(k/2) + 2^k $$
> 2. 简化方程
> $$ \frac{S(k)}{2^k} = \frac{S(k/2)}{2^{k/2}} + 1 $$
> 3. 再次换元
> 令 $A(k) = \frac{S(k)}{2^k}$，上式变为：$A(k) = A(k/2) + 1$
> 
> 4. 求解递推
> $$ A(k) = A(k/2) + 1 = A(k/4) + 1 + 1 = \dots = O(\log k) $$
> 因为 $A(k) = \frac{S(k)}{2^k}$，所以：
> $$ \frac{S(k)}{2^k} = O(\log k) \implies S(k) = O(2^k \log k) $$
> 将 $k = \log n$ 和 $2^k = n$ 代回：
> $$ W(n) = S(k) = O(n \log {\log{ n}}) $$

**双对数范式**(doubly-logarithmic paradigm)
假设 $h = \log \log n$ 为整数，此时 $n = 2^{2^h}$。现在将问题划分为 $\dfrac{n}{h}$ 个规模为 $h$ 的子问题：
$$
\begin{align}
A_1 &= A(1), \dots, A(h) \quad \Rightarrow M_1 \\
A_2 &= A(h + 1), \dots, A(2 h) \quad \Rightarrow M_2 \\
&\cdots\\
A_{\frac{n}{h}} &= A(n - h + 1), \dots, A(n) \quad \Rightarrow M_{\frac{n}{h}}
\end{align}
$$
最后从每个子问题得到的最大值 $M_1, M_2, \dots M_{\frac{n}{h}}$ 中选取最大值为 $A_{max}$
> [!tip] Analysis
> - 对于每个子问题，所需时间为 $T(h)$，工作量为 $W(h)$
> - 根据对之前划分的分析，最终解得：
> 	- 时间：$T(n) = O(h + \log \log \dfrac{n}{h}) = O(\log \log n)$
> 	- 工作量：$W(n) = O(h \cdot \dfrac{n}{h} + \dfrac{n}{h} \log \log \dfrac{n}{h}) = O(n)$
> 
> 这次将工作量压到了线性复杂度，但是没能保住原来常数级的时间。

> [!prove]-
> ##### 时间复杂度证明 $T(n)$
> - Step 1：组内顺序处理
> 	- 由于每组有 $h$ 个元素，且各组是并行进行的，所以时间取决于单组的处理时间。使用顺序比较法，处理 $h$ 个元素需要的时间为线性时间：$T_1 = O(h)$
> - Step 2：代表元素并行归约
> 	- 输入规模变成了 $M = \dfrac{n}{h}$
> 	- 采用上述的方法进行 $\sqrt(M)$ 划分，所需时间为 $O(\log \log M)$，即 $T_2 = O(\log \log \dfrac{n}{h})$
> - Step 3：总时间合并
> $$ T(n) = T_1 + T_2 = O(h + \log \log \frac{n}{h}) $$
> 将 $h = \log \log n$ 代入公式：
> 	1.  第一项：$O(\log \log n)$
> 	2.  第二项：
>     $$ \begin{aligned} \log \log (\frac{n}{h}) &= \log \log (\frac{n}{\log \log n}) \\ &= \log (\log n - \log (\log \log n)) \end{aligned} $$
>     当 $n$ 很大时，$\log \log \log n$ 远小于 $\log n$，因此 $O(\log \log \dfrac{n}{h}) \approx O(\log \log n)$
> 
> **最终结果：**
> $$ T(n) = O(\log \log n) + O(\log \log n) = \mathbf{O(\log \log n)} $$
> 
> ---
> 
> ##### 工作量证明 $W(n)$
> 
> Step 1：组内处理工作量
> - 每个组的工作量是 $O(h)$（顺序扫描）
> - 一共有 $\dfrac{n}{h}$ 个组
> $$ W_1 = (\text{组数}) \times (\text{单组工作量}) = \frac{n}{h} \times h = O(n) $$
> 
> Step 2：代表元素归约工作量
> - 输入规模为 $M = \frac{n}{h}$。
> - 根据上述结论，规模为 $M$ 时的总工作量是 $O(M \log \log M)$。
> $$ W_2 = O\left( \frac{n}{h} \log \log \frac{n}{h} \right) $$
> 
> Step 3： 总工作量合并与化简
> $$ W(n) = W_1 + W_2 = O(n) + O\left( \frac{n}{h} \log \log \frac{n}{h} \right) $$
> 
> 我们将 $h = \log \log n$ 代入第二项进行验证：
> $$ \begin{aligned} W_2 &= \frac{n}{\log \log n} \times \log \log \left( \frac{n}{\log \log n} \right) \\ &\approx \frac{n}{\log \log n} \times \log \log n \quad (\text{因为 } \log\log\frac{n}{h} \approx \log\log n) \\ &= O(n) \end{aligned} $$
> 
> **最终结果：**
> $$ W(n) = O(n) + O(n) = \mathbf{O(n)} $$

## 14.5 Random Sampling
- With very high probability, on an **Arbitrary CRCW PRAM**

其具体步骤如下：
1. 先从数组 $A$ 中的 $n$ 个元素中挑选 $n^{\frac{7}{8}}$ 个元素出来，形成数组 $B$
<div style="text-align: center">
    <img src="images/lec14/19.png" width="50%">
</div>
- 时间：$T=O(1)$    
- 工作量：$W=O(n^{7/8})$

2. 将数组 $B$ 划分成大小为 $n^{\frac{1}{8}}$ 的小块，因此这样的小块有 $n^{\frac{3}{4}}$ 个。然后对每个小块求出最大值，通过两两比较的方式得到了 $n^{\frac{3}{4}}$ 个局部最大值
<div style="text-align: center">
    <img src="images/lec14/20.png" width="50%">
</div>
在 **CRCW-PRAM** 模型中，若支持并发写入最大值，则可以实现 $O(1)$ 时间求最大值
- 时间：$M_i^{(1)} \sim T = O(1) \Rightarrow T(n) = O(1)$
- 工作量：$W_i = O((n^{\frac{1}{8}})^2) = O(n^{\frac{1}{4}}) \Rightarrow W(n) = O(n)$

3. 将这些最大值划分为 $n^{\frac{1}{2}}$ 个大小为 $n^{\frac{1}{4}}$ 的小块，然后对每个小块求出最大值，进而通过两两比较的方式得到所有 $n^{\frac{7}{8}}$ 个元素的最大值
<div style="text-align: center">
    <img src="images/lec14/21.png" width="50%">
</div>
- 时间：$M_i^{(2)} \sim T = O(1) \Rightarrow T(n) = O(1)$
- 工作量：$W_i = O((n^{\frac{1}{4}})^2) = O(n^{\frac{1}{2}}) \Rightarrow W(n) = O(n)$
**Conclusion**：
```c
while (there is an element larger than M) {
    for (each element larger than M)
        Throw it into random place in new B(n^{7/8})
    Compute a new M;
}
```
- 时间：$M(n^{\frac{7}{8}}) \sim T = O(1)$
- 工作量：$W = O(n)$

> [!warning]
> 由于是随机挑选的，因此这个算法不能保证始终得到正确结果，但是得到正确结果的概率相当大（失败概率为 $O(\dfrac{1}{n^c})$，其中 $c$ 为正常数；或者也可以记作 $O(n^c)$，但此时 $c$ 为负常数）。