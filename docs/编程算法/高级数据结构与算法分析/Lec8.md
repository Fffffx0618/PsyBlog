# Dynamic Programming
## 8.1 Theory Background
> [!info] 动态规划的概念
> **动态规划**（dynamic programming, DP）是一个重要的算法范式，它将一个问题分解为一系列更小的子问题，并通过存储子问题的解来避免重复计算，从而大幅提升时间效率。

动态规划的问题特性：
- **重叠子问题**：动态规划的子问题是相互依赖的（分治算法处理的是独立的子问题）
- **最优子结构**：原问题的最优解是从子问题的最优解构建得来的
- **无后效性**：给定一个确定的状态，它的未来发展只与当前状态有关，而与过去经历的所有状态无关（否则难以用动态规划解决）

**动态规划**的基本思想：
- 每个子问题仅解决一次，将得到的解存入一张表中（数组/散列表）
- 如果某个子问题需要其他子问题的解，可先查表，看是否已经求过解，若是则直接用，否则再计算
- “以空间换时间”——**记忆化搜索**

> [! note] 动态规划的解题步骤
> 1. 用符号化或数学化的语言描述问题的**一个**最优解，即定义状态
> 	- 可能是最难的部分
> 2. 递归地定义最优解的值
> 	- 得到一个递推关系式（或者称为**状态转移方程**）、base case和其他边界条件
> 3. 确定好计算的顺序
> 	- 自底向上/自顶向下
> 	- **迭代**计算，得到一张状态表
> 4. （可选）重构解决问题的策略
> 	- 有些题目可能要求画出最优解情况的方案，比如画出一棵树或一条路径等，这就需要我们在计算最优解的时候时刻记录计算的过程

---
## 8.2 Examples
### 1. Fibonacci Number
$$F(0)=1,F(1)=1,F_i = F_{i - 1} + F_{i - 2}$$
- 要得到$F_N$，只需知道$F_{N-1}$和$F_{N-2}$的值
- 在计算过程中保留这两个值，即上一次和上上次计算的结果，将它们相加即可得到本次计算的结果，无需存储所有$F_i$的值（空间复杂度$O(N) \rightarrow O(1)$）
- 更新上一次和上上次的值，进入下一轮的计算（$F(N+1)$）
- 所这种方法是**自底向上**计算的，而递归算法是自顶向下计算的

> [!code] 代码实现
> ```cpp
> int Fibonacci(int N) {
>     int i, Last, NextToLast, Answer;
>     if (N <= 1)
>         return 1;
>     Last = NextToLast = 1;    // F(0) = F(1) = 1
> 
>     for (i = 2; i <= N; i++) {
>         Answer = Last + NextToLast;    // F(i) = F(i - 1) + F(i - 2)
>         NextToLast = Last;    // update F(i - 1) and F(i - 2)
>         Last = Answer;
>     }    // end-for
> 
>     return Answer;
> }
> ```
- 时间复杂度：$T(N) = O(N)$

### 2. Ordering Matrix Multiplications
> [!question]
> 对于多个矩阵的乘法，乘法的顺序相当关键，如果顺序选择不当，会让计算次数变多。
> <div style="text-align: center"><img src="images/lec8/1.png" width="70%"></div>
> 
> 问题：对于一个给定的多矩阵乘法，请找出最优的乘法顺序。

#### 穷举法 
- 令 $b_n$ 为计算矩阵乘法 $\mathbf{M}_1 \cdot \mathbf{M}_2 \cdot \dots \cdot \mathbf{M}_n$ 的顺序数，易知 $b_2 = 1, b_3 = 2, b_4 = 5, \dots$
- 令 $\mathbf{M}_{ij} = \mathbf{M}_i \cdot \dots \cdot \mathbf{M}_j$，那么 $\mathbf{M}_{1n} = \mathbf{M}_1 \cdot \dots \cdot \mathbf{M}_n = \mathbf{M}_{1i} \cdot \mathbf{M}_{i+1\ n}$
- 令 $b_n$ 为 $\mathbf{M}_{1n}$ 的乘法顺序数，$b_i$ 为 $\mathbf{M}_{1i}$ 的乘法顺序数，$b_{n - i}$ 为 $\mathbf{M}_{i + 1\ n}$ 的乘法顺序数$$\Rightarrow b_n = \sum\limits_{i = 1}^{n - 1}b_i b_{n - i}，\text{其中 } n > 1 \text{ 且 } b_1 = 1$$经计算，$b_n = O(\dfrac{4^n}{n\sqrt{n}})$，且 $b_n$ 是一个**卡特兰数 (Catalan number)**
#### DP
> [!solution]
> 假设计算 $n$ 个矩阵的乘法为 $\mathbf{M}_1 \cdot \dots \cdot \mathbf{M}_n$，其中 $\mathbf{M}_i$ 是规模为 $r_{i-1} \times r_i$ 的矩阵。令计算矩阵乘法 $\mathbf{M}_i \cdot \dots \cdot \mathbf{M}_j$ 的最优成本为 $m_{ij}$，可以得到以下递推关系式：
> $$
> m_{ij} = \begin{cases}0 & \text{if}\ i = j \\ \min\limits_{i \le l < j}\{m_{il} + m_{l+1\ j} + r_{i-1}r_lr_j\} & \text{if}\ j > i\end{cases}
> $$
> > 此处是将 $m_{ij}$ 分割为 $m_{il},M_l,M_{l+1\space j}$，再将三者相乘

- 需要计算的$m_{ij}$有$O(N^2)$个（$i, j$的范围在$[1, n]$之间）
- 采用**自底向上**计算：先算最小规模的 $m_{ij}$（$i = j$），再计算更大规模的 $m_{ij}$，这样规模较大的子问题可以利用规模较小的子问题的解直接计算，而无需重复计算
<div style="text-align: center">
    <img src="images/lec8/2.png" width="60%">
</div>

```cpp
// r contains numbers of columns for each of the N matrices
// r[0] is the number of rows in matrix 1
// Minimum number of multiplications is left in M[1][N]
void OptMatrix(const long r[], int N, TwoDimArray) {
    int i, j, l, L;
    long ThisM;

    for (i = 1; i <= N; i++){
    	M[i][i] = 0;
    }
    for (k = 1; k < N; k++)    // k = j - i
        for (i = 1; i <= N - k; i++) {    // For each position
            j = i + k;
            M[i][j] = Infinity;
            for (L = i; L < j; L++) {
                ThisM = M[i][L] + M[L + 1][j] + r[i - 1] * r[L] * r[j];
                if (ThisM < M[i][j])    // Update min
                    M[i][j] = ThisM;
            }    // end for-L
        }    // end for-Left
}
```

- 循环顺序是==先循环 k 再循环 i ==
	- 如果先循环 `i`，当 `i` 很小，`k` 很大时，`j` 的取值也可以很大，那么在计算 `M[i][j]` 时，`M[L + 1][j]` 这项还没有算出来（`L + 1 > i`），因此无法得到正确结果。

> [!question] 如何保存乘法的顺序？
> ```cpp
> // Compute optimal ordering of matrix multiplication
> // c contains number of columns for each of the n matrices
> // c[0] is the number of rows in matrix 1 
> // Minimum number of multiplications is left in M[1][n] 
> // Actual ordering can be computed via 
> // another procedure using last_change 
> // M and last_change are indexed starting at 1, instead of zero 
> 
> void opt_matrix(int c[], unsigned int n, two_d_array M, two_d_array last_change) {
>     int i, k, Left, Right, this_M;
> 
>     for (Left = 1; Left <= n; Left++)
>         M[Left][Left] = 0;
>     for (k = 1; k < n; k++)    // k is Right-Left 
>         for (Left = 1; Left <= n - k; Left++) {    // for each position 
>             Right = Left + k;
>             M[Left][Right] = INT_MAX;
>             for (i = Left; i < Right; i++) {
>                 this_M = M[Left][i] + M[i+1][Right]
>                             + c[Left-1] * c[i] * c[Right];
>                 if(this_M < M[Left][Right]) {    // Update min
>                     M[Left][Right] = this_M;
>                     last_change[Left][Right] = i;
>                 }
>             }
>         }
> }
>```
> 时间复杂度：$T(N) = O(N^3)$

---
### 3. Optimal Binary Search Trees
**最优二叉查找树**(optimal binary search trees, OBST)：一种在二叉查找树上完成静态查找(static search)操作的最优方法。

> [!question]
> 给定 $N$ 个单词，满足词典序 $w_1 < w_2 < \dots < w_N$，且每个词 $w_i$ 出现的概率为 $p_i$。现在要求将这些词排列在一个二叉查找树上，使得所有单词的预期查找时间（$T(N) = \sum\limits_{i=1}^N p_i \cdot (1 + d_i)$，其中 $d_i$ 为 $w_i$ 在树中的深度）尽可能小，即构造一棵OBST。
>  - 下面给出一个程序用到的关键词以及对应的词频：
>  <div style="text-align: center"><img src="images/lec8/3.png" width="90%"></div>

构造OBST与计算矩阵乘法的最优顺序类似：
- $T_{ij}$：由单词$w_i \dots w_j(i < j)$构成的OBST
- $c_{ij}$：$T_{ij}$的成本
- $r_{ij}$：$T_{ij}$的根节点
- $w_{ij}$：$T_{ij}$的权重，等于$\sum\limits_{k = i}^j p_k$（$w_{ii} = p_i$）
如果令$w_k = r_{ij}$，那么$T_{ij}$的结构如下所示：
<div style="text-align: center">
    <img src="images/lec8/5.png" width="60%">
</div>  
这棵树的成本为：
$$
\begin{align}
c_{ij} & = p_k + \text{cost}(L) + \text{cost}(R) + \text{weight}(L) + \text{weight}(R) \notag \\
& = p_k + c_{i, k - 1} + c_{k + 1, j} + w_{i, k - 1} + w_{k + 1, j} \notag \\
& = w_{ij} + c_{i, k - 1} + c_{k + 1, j} \notag
\end{align}
$$
若 $T_{ij}$ 是最优的，那么需要满足 $c_{ij} = w_{ij} + \min\limits_{i < l \le j}\{c_{i, l - 1} + c_{l + 1, j}\}$

<div style="text-align: center">
<img src="images/lec8/12.png" width="90%">
</div>

- 得到完整的表后，先将位于表格最后一行的单词插入树内，作为根节点
- 根据词典序将剩余的单词划分为左右两半，按照**中序遍历**的顺序逐一插入
  <div style="text-align: center">
    <img src="images/lec8/19.png" width="90%">
    </div>

可以看到OBST可以确保词频较大的单词的深度尽可能小，从而有效降低了总的查找时间。
- 时间复杂度：$T(N) = O(N^3)$

### 4. ALl-Pairs Shortest Path
> [!info] 
> <u>单源最短路(single-source)算法【Dijkstra算法】</u>的时间复杂度为 $O(|V|^2)$（$|V|$ 为图的顶点数），因此通过该算法计算任意两点间的最短路需要 $O(|V|^3)$ 的复杂度（每个点都需要用一次该算法）。这种算法在稀疏图上运行较快，对于**稠密图**而言，更快的算法是**Floyd算法**

定义：
- $D^k[i][j] = \min\{\text{length of path}\ i \rightarrow \{l \le k\} \rightarrow j\}$，其中 $l\leq k$ 表示路径上可以经过任何编号不大于 $k$ 的节点（$k \in [0, N - 1]$，共 $N$ 个待判断的点）
	- 表示在只允许使用前 $k$ 个顶点（即索引为 $0∼k$）作为中间节点时，从 $i$ 到 $j$ 的最短路径长度
- $D^{-1}[i][j] = \text{Cost}[i][j]$（$k = -1$表示$i, j$之间没有任何节点，即初始状态）
则从顶点$i$到顶点$j$之间的最短路径长度为$D^{N-1}[i][j]$

**Floyd算法的思路**
从$D^{-1}$开始，连续得到$D^0, D^1, \dots, D^{N-1}$。如果已经解决了$D^{k-1}$，则此时有两种可能的情况：
- 第$k$个节点并不在最短路内，即$D^k = D^{k - 1}$
- 第$k$个节点在最短路内，那么满足$D^k[i][j] = D^{k-1}[i][k] + D^{k-1}[k][j]$
因此有递推关系：$$D^k[i][j] = \min\{D^{k-1}[i][j], D^{k-1}[i][k] + D^{k-1}[k][j]\}, k \ge 0$$
**代码实现**
```c
// A[] contains the adjacency matric with A[i][i] = 0
// D[] contains the values of the shortest path
// N is the number of vertices
// A negative cycle exists iff D[i][i] < 0

void AllPairs(TwoDimArray A, TwoDimArray D, int N) {
    int i, j, k;
    for (i = 0; i < N; i++)    // initialize D
        for (j = 0; j < N; j++)
            D[i][j] = A[i][j];

    for (k = 0; k < N; k++)      // add the kth vertex into the path
        for (i = 0; i < N; i++)
            for (j = 0; j < N; j++)
                if (D[i][k] + D[k][j] < D[i][j])    // update shortest path
                    D[i][j] = D[i][k] + D[k][j];
}
```
- 该算法适用于负权边，但不适用于负权环
- 可以看到，上述函数仅计算了任意两点间的最短路径长度，并没有记住最短路径是什么样子的，读者可以尝试着添加这个功能。

**记录路径的版本**
```c
// Compute All-Shortest Paths 
// A[] contains the adjacency matrix 
// with A[i][i] presumed to be zero 
// D[] contains the values of shortest path 
// |V| is the number of vertices 
// A negative cycle exists iff 
// d[i][j] is set to a negative value
// Actual Path can be computed via another procedure using path 
// All arrays are indexed starting at 0 
void all_pairs( two_d_array A, two_d_array D, two_d_array path ) {
    int i, j, k;
    for (i = 0; i < |V|; i++) // Initialize D and path 
        for (j = 0; j < |V|; j++) {
            D[i][j] = A[i][j];
            path[i][j] = NOT_A_VERTEX;
        }
    for (k = 0; k < |V|; k++)
        // Consider each vertex as an intermediate 
        for (i = 0; i < |V|; i++)
            for (j = 0; j < |V|; j++)
                if (d[i][k] + d[k][j] < d[i][j]) {    // update min 
                    d[i][j] = d[i][k] + d[k][j];
                    path[i][j] = k;
                }
}
```

时间复杂度：$T(N) = O(N^3)$，但是在稠密图中表现较好

### 5. Product Assembly
> [!question]
> 产品组装(product assembly)问题，有以下条件
> - 一辆车的生产需要用到两条组装线
>     - 每个阶段会用到不同的工艺（时间，即不同的节点值）
>     - 在各阶段都可以随时切换组装线
> 
>     现在要求求出最短的组装总时间
> 
>     <div style="text-align: center"><img src="images/lec8/20.png" width="90%"></div>

1. 定义状态
    <div style="text-align: center">
        <img src="images/lec8/21.png" width="80%">
    </div>

    - 这张图给出了在*stage*阶段时的最优解（绿点 + 蓝线）
    - 红色虚线表示虽然有一条同样能在*stage*阶段到达同一个点的路径，但这条路径所花的时间更长，因此被pass掉了

2. 递归地定义最优解的值
    <div style="text-align: center">
        <img src="images/lec8/22.png" width="40%">
    </div>

    - 在*stage*阶段时，我们有两种到达对应点的路径：要么来自第一条组装线，要么来自第二条组装线
    - 因此，我们不难得出以下递推关系式：
$$
    \begin{align}
    f[line][stage] & = \min\{f[line][stage - 1] + t_{process}[line][stage - 1]， \notag \\ 
    &  f[1 - line][stage - 1] + t_{transit}[1 - line][stage - 1]\} \notag 
    \end{align}
    $$

    其中$f[line][stage]$表示在*stage*阶段时，在第*line*条组装线上的最优时间，$t_{process}[line][stage]$表示在同一条组装线上进入*stage*阶段所需的时间，$t_{transit}[line][stage]$表示从不同组装线上进入*stage*阶段所需的时间。

3. 确定好计算的顺序
```c
// Initialization
f[0][0] = 0; 
f[1][0] = 0;
// Outer loop: start from the first stage, end with the last stage
for (stage = 1; stage <= n; stage++) {
    // Inner loop: test each line and find the minimum path
    for (line = 0; line <= 1; line++) {
        f[line][stage] = min(f[line][stage - 1] + t_process[line][stage - 1], 
                                f[1 - line][stage - 1] + t_transit[1 - line][stage - 1]);
    }
}
// The solution comes from the last stage of two lines
Solution = min(f[0][n], f[1][n]);
```

4. 重构解决问题的策略。这里要求输出最短时间的组装顺序，代码如下所示：
```c
f[0][0] = 0; 
f[1][0] = 0;

// L[line][stage]: record the source of the stage, either 0 or 1(the number of assembly lines) 
L[0][0] = 0;
L[1][0] = 0;

for (stage = 1; stage <= n; stage++) {
    for (line = 0; line <= 1; line++) {
        f_stay = f[line][stage - 1] + t_process[line][stage - 1];
        f_move = f[1 - line][stage - 1] + t_transit[1 - line][stage - 1];
        if (f_stay < f_move) {
            f[line][stage] = f_stay;
            L[line][stage] = line;
        } else {
            f[line][stage] = f_move;
            L[line][stage] = 1 - line;       
        }
    }
}

// save the optimal path in plan[]
line = f[0][n] < f[1][n] ? 0 : 1;
for (stage = n; stage > 0; stage--) {
    plan[stage] = line;
    line = L[line][stage];
}
```

时间复杂度：$T = O(N)$