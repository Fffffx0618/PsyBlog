# Chap 7: Iterative Techniques in Matrix Algebra
> [!Target] 
> Solve $A\vec{x}=\vec{b}$

> [!Ideas]
> 类似求解 $f(x) = 0$ 的不动点迭代：
> - 先将 $A \vec{x} = \vec{b}$ 转化为等价的 $\vec{x} = T\vec{x} + \vec{c}$ 的形式
> - 然后从初始猜测值 $\vec{x}^{(0)}$ 开始 $\vec{x}^{(k+1)} = T\vec{x}^{(k)} + \vec{c}$ 的迭代，得到（收敛的）序列 $\{\vec{x}^{(k)}\}$

## 7.1 Norms of Vectors and Matrices
### 1. Vector Norms
**Definition**：
在 $R^n$ 上的==向量范数(vector norm)==是一个 $R^n \rightarrow R$ 的函数 $\| \cdot \|$，对于所有 $\vec{x}, \vec{y} \in R^n, \alpha \in C$，它满足以下性质：
- **正定**(positive definite)：$\| \vec{x} \| \ge 0;\ \| \vec{x} \| = 0 \Leftrightarrow \vec{x} = \vec{0}$
- **齐次**(homogeneous)：$\| \alpha \vec{x} \| = |\alpha| \cdot \| \vec{x} \|$
- **三角不等式**(triangle inequality)：$\| \vec{x} + \vec{y}\| \le \| \vec{x} \| + \| \vec{y} \|$

对于向量 $x=(x_1,x_2,\dots,x_n)^T$，**一些常用的范数**：
1. $\| \vec{x} \|_1 = \sum\limits_{i=1}^n |x_i|$
2. $\| \vec{x} \|_2 = \sqrt{\sum\limits_{i=1}^n |x_i|^2}$（**欧几里得范数**，即我们熟知的**模长**）
3. $\| \vec{x} \|_p = \Big( \sum\limits_{i=1}^n |x_i|^p \Big)^{\frac{1}{p}}$（**$p$ 范数**）
4. $\| \vec{x} \|_\infty = \max\limits_{1 \le i \le n} |x_i|$（**无穷范数**）
Note：$\lim\limits_{p \rightarrow \infty} \| \vec{x} \|_p = \| \vec{x} \|_{\infty}$
#### 一些定义和定理
**向量的收敛性**
Definition：
- 若 $\forall \varepsilon > 0$，$\exists N(\varepsilon) \in N$，对于所有 $k \geq N(\varepsilon)$，能使 $\|\vec{x}^{(k)} - \vec{x}\| < \varepsilon$ 恒成立，那么在 $R^n$ 上的向量序列 $\{ \vec{x}^{(k)} \}_{k=1}^{\infty}$ 关于范数 $\| \cdot \|$ 收敛到 $\vec{x}$
Theorem:
- 当且仅当 $\lim\limits_{k \rightarrow \infty} x_i^{(k)} = x_i\ (i = 1, 2, \dots, n)$ 时，在 $R^n$ 上的向量序列 $\{\vec{x}\}_{k=1}^{\infty}$ 关于范数 $\| \cdot \|_{\infty}$ 收敛到 $\vec{x}$

**范数的等价性**    
Definition:
- 若存在正常数 $C_1, C_2$，使得 $C_1 \|\vec{x}\|_B \le \|\vec{x}\|_A \le C_2 \| \vec{x} \|_B$，那么 $\| \cdot \|_A$ 和 $\| \cdot \|_B$ 是等价(equivalent)的
Theorem:
- 所有在 $R^n$ 上的向量范数都是等价(equivalent)的

### 2. Matrix Norms
对于所有规模为 $n \times n$ 的矩阵，**矩阵范数**(matrix norms)是一个实数值函数 $\| \cdot \|$，对于所有规模为 $n \times n$ 的矩阵 $A, B$ 以及所有的 $\alpha \in C$，它满足以下性质：
- **正定**(positive definite)：$\| A \| \ge 0;\ \| A \| = 0 \Leftrightarrow A = O$
- **齐次**(homogeneous)：$\| \alpha A \| = |\alpha| \cdot \| A \|$
- **三角不等式**(triangle inequality)：$\| A + B \| \le \| A \| + \| B \|$
- **\*一致性**(consistency)：$\| AB \| \le \| A \| \cdot \| B \|$

**一些常用的范数**：
1. **弗罗贝尼乌斯范数**(Frobenius norm)：$\| A \|_F = \sqrt{\sum\limits_{i=1}^n \sum\limits_{j=1}^n |a_{ij}|^2}$
2. **自然范数**(natural norm)
	- **算子范数**(operator norm)（和向量范数 $\| \cdot \|$ 关联，所以也可称为 **$p$ 范数**）$$
    \| A \|_p = \max\limits_{\vec{x} \ne \vec{0}} \dfrac{\| A \vec{x} \|_p}{\| \vec{x} \|_p} = \max\limits_{\| \vec{x} \|_p = 1} \| A\vec{x} \|_p
    $$
    - **无穷范数**：$\| A \|_{\infty} = \max\limits_{1 \le i \le n} \sum\limits_{j=1}^n |a_{ij}|$（最大行）
	    - **1-范数**：$\| A \|_1 = \max\limits_{1 \le j \le n} \sum\limits_{i=1}^n |a_{ij}|$ （最大列）
	    - **2-范数**（又称**谱范数**(spectral norm)）：$\| A \|_2 = \sqrt{\lambda_{\max} (A^T A)}$

> [!Proof]
> 证明 $\|A \|_{\infty} = \max\limits_{1 \le i \le n} \sum\limits_{j=1}^n |a_{ij}|$
> 
> 1. 证明 $\| A \|_{\infty} = \max\limits_{\| \vec{x} \|_{\infty} = 1} \| A \vec{x} \|_{\infty} \le \max\limits_{1 \le i \le n} \sum\limits_{j=1}^n |a_{ij}|$
> $$\| A \vec{x} \|_{\infty} = \max\limits_{1 \le i \le n} |(A \vec{x})_i| = \max\limits_{1 \le i \le n} |\sum\limits_{j=1}^n a_{ij} x_j| \le \max\limits_{1 \le i \le n} \sum\limits_{j=1}^n |a_{ij}| \cdot \max\limits_{1 \le i \le n} |x_j|$$
> 2. 证明 $\| A \|_{\infty} = \max\limits_{\| \vec{x} \|_{\infty} = 1} \| A\vec{x} \|_{\infty} \ge \max\limits_{1 \le i \le n} \sum\limits_{j=1}^n |a_{ij}|$
> - 令第 $p$ 行为最大行，即满足 $\sum\limits_{j=1}^n |a_{pj}| = \max\limits_{1 \le i \le n} \sum\limits_{j=1}^n |a_{ij}|$
> - 取一个特殊的单位向量 $\vec{x}$ 使得 $x_j = \begin{cases} 1, & \text{if } a_{pj} \ge 0 \\ -1, & \text{if } a_{pj} < 0 \end{cases}$
> $$\| A \vec{x} \|_{\infty} = \max\limits_{1 \le i \le n} \Big| \sum\limits_{j=1}^n a_{ij} x_j\Big| \ge \Big| \sum\limits_{j=1}^n a_{pj} x_j \Big| = \Big| \sum\limits_{j=1}^n |a_{pj}| \Big| = \max\limits_{1 \le i \le n} \sum\limits_{j=1}^n |a_{ij}|$$

> [!推论]
> 对于任意向量 $\vec{z} \ne 0$，矩阵 $A$ 以及任意自然范数 $\| \cdot \|$，我们有：
> $$\| A \vec{z} \| \le \| A \| \cdot \| \vec{z} \|$$
> 成立。

## 7.2 Eigenvalues and Eigenvectors
> [!info] 特征值和特征向量
> - 矩阵 $A$ 的**特征多项式**(characteristic polynomial)为 $p(\lambda) = \det (A - \lambda I)$
>     - 特征方程 $p(\lambda) = 0$ 的解就是矩阵 $A$ 的**特征值**(eigenvalues)
>     - 若存在特征值 $\lambda$ 和向量 $\vec{x} \ne \vec{0}$，满足 $(A - \lambda I) \vec{x} = \vec{0}$，那么 $\vec{x}$ 就是 $A$ 的**特征向量**(eigenvector)

矩阵的==谱半径(spectral radius)== $\rho(A) = \max{| \lambda |}$，其中 $\lambda$ 是 $A$ 的特征值（复数范围， $|\lambda|$ 表示特征值的**模长**）
<div style="text-align: center"><img src="images/image-12.png" width="50%"></div>
> [!theorem] 定理
> 如果 $A$ 是一个 $n \times n$ 的矩阵，那么对于所有的自然范数 $\| \cdot \|$，$\rho(A) \le \| A \|$ 恒成立
>     
>> [!proof] 证明
>> 对于 $A$ 的任何特征值 $\lambda$ 以及特征向量 $\| \vec{x} \|$，且 $\| \vec{x} \| = 1$，有：
>> $$|\lambda| \cdot \| \vec{x} \| = \| \lambda \vec{x} \| = \| A\vec{x} \| \le \| A \| \cdot \| \vec{x} \|$$

若 $\forall i, j = 1, 2, \dots, n$，有 $\lim\limits_{k \rightarrow \infty} (A^k)_{ij} = 0$，那么称规模为 $n \times n$ 的矩阵 $A$ 是**收敛**的

## 7.3 Iterative Techniques for Solving Linear Systems

### 1. Jacobi Iterative Method
对于线性方程组 $\begin{cases}a_{11}x_1 + a_{12}x_2 + \dots + a_{1n}x_n = b_1 \\ a_{21}x_1 + a_{22}x_2 + \dots + a_{2n}x_n = b_2 \\ \dots \\ a_{n1}x_1 + a_{n2}x_2 + \dots + a_{nn}x_n = b_n\end{cases}$，当 $a_{ii} \ne 0$ 时，不难得到：

$$
\begin{cases}
x_1 = \dfrac{1}{a_{11}}(-a_{12}x_2 - \dots - a_{1n}x_n + b_1) \\ x_2 = \dfrac{1}{a_{22}}(-a_{21}x_1 - \dots - a_{2n}x_n + b_1) \\ x_n = \dfrac{1}{a_{nn}}(-a_{n1}x_1 - \dots - a_{1n, n-1}x_{n-1} + b_n) 
\end{cases}
$$

用矩阵形式表示上述线形方程组，并转化为以下形式：
![[image-11.png|149x114]]
那么：
$$
\begin{align}
A\vec{x} = \vec{b} & \Leftrightarrow (D - L - U)\vec{x} = \vec{b} \notag \\
& \Leftrightarrow D\vec{x} = (L + U) \vec{x} + \vec{b} \notag \\
& \Leftrightarrow \vec{x} = \underbrace{D^{-1} (L + U)}_{T_j} \vec{x} + \underbrace{D^{-1} \vec{b}}_{\vec{c_j}} \notag
\end{align}
$$

可得递推公式为：$\vec{x}^{(k)} = T_j \vec{x}^{(k-1)} + \vec{c_j}$，其中 $T_j$ 被称为**雅可比迭代矩阵**(Jacobi iterative matrix)

> [!code] 算法：雅可比迭代方法
> 对于给定的初始近似解 $\vec{x}^{(0)}$，求解 $A\vec{x} = \vec{b}$
> - 输入：方程和未知数的个数 $n$，矩阵元素 $a[\space][\space]$，常数项 $b[\space]$，初始近似解 $X0[\space]$，容忍值 $TOL$，最大迭代次数 $N_{max}$
> - 输出：近似解 $X[\space]$ 或错误信息
> 
> ```c 
> Step 1  Set k = 1;
> Step 2  while (k <= N_max) do step 3-6
>         Step 3  for i = 1, ..., n
>                     Set X[i] = (b[i] - sum(j=1, j!=i, j<=n, a[i][j] * X[0][j])) / a[i][i];  // compute x^k
>         Step 4  if norm(X - X0)_infty = max(1<=i<=n, X[i] - X0[i]) < TOL then Output(X[]);
>                 STOP;    // successful
>         Step 5  for i = 1, ..., n  Set X0[] = X[];  // update X0
>         Step 6  Set k++;
> Step 7  Output (Maximum number of iterations exceeded);
>         STOP.    // unsuccessful
> ```
> 
> - 第 4 行：`a[i][i]` 可能为 0，可以在计算前为矩阵元素**重新排序**，以保证 `a[i][i] != 0`，如果无法通过重排避免这一问题，那么矩阵 $A$ 就是**奇异的** 
> - 第 7 行：$X^{(k+1)}$ 必须等到 $X^{(k)}$ 的项全部算出来，因此要用两个向量来存储结果。但这样会浪费空间了，因为最后只会用到一个向量
### 2. Gauss-Seidel Iterative Method
$$
\begin{align}
x_2^{(k)} & = \dfrac{1}{a_{22}}(\textcolor{red}{-a_{21}x_1^{(k)}} - a_{23}x_3^{(k-1)} - a_{24}x_4^{(k-1)} - \dots - a_{2n}x_n^{k-1} + b_2) \notag \\ 
x_3^{(k)} & = \dfrac{1}{a_{33}}(\textcolor{red}{-a_{31}x_1^{(k)} - a_{32}x_2^{(k)}} - a_{34}x_4^{(k-1)} - \dots - a_{3n}x_n^{k-1} + b_3) \notag \\ 
\dots \notag \\ 
x_n^{(k)} & = \dfrac{1}{a_{nn}}(\textcolor{red}{-a_{n1}x_1^{(k)} -a_{n2}x_2^{(k)} -a_{n3}x_3^{(k)} - \dots - a_{n, n-1}x_{n-1}^{k}} + b_n) \notag
\end{align}
$$
用矩阵形式表述为：
$$
\begin{align}
& \vec{x}^{(k)} = D^{-1} (L\vec{x}^{(k)} + U\vec{x}^{(k-1)}) + D^{-1} \vec{b} \notag \\
\Leftrightarrow & (D - L)\vec{x}^{(k)} = U\vec{x}^{(k-1)} + \vec{b} \notag \\
\Leftrightarrow & \vec{x}^{(k)} = \underbrace{(D - L)^{-1} U }_{T_g} \vec{x}^{(k-1)} + \underbrace{(D - L)^{-1}}_{\vec{c}_g} \vec{b} \notag
\end{align}
$$

递推公式为：$\vec{x}^{(k)} = T_g \vec{x}^{(k-1)} + c_g \vec{b}$，其中 $T_g$ 为**高斯-塞德尔迭代矩阵**(Gauss-Seidel iterative matrix)。

> [!code] 算法：高斯-塞德尔迭代方法
> 对于给定的初始近似解 $\vec{x}^{(0)}$，求解 $A\vec{x} = \vec{b}$
>     
>   - 输入：方程和未知数的个数 $n$，矩阵元素 $a[\quad][\quad]$，常数项 $b[\quad]$，初始近似解 $X0[\quad]$，容忍值 $TOL$，最大迭代次数 $N_{max}$
>   - 输出：近似解 $X[\quad]$ 或错误信息
>     
> ```c
> Step 1  Set k = 1;
> Step 2  while (k <= N_max) do step 3-6
>         Step 3  for i = 1, ..., n
>                     Set X[i] = (-sum(j=1, i-1, a[i][j] * x[j]) - sum(j=i+1, n, a[i][j] * X0[j]) + b[i]) / a[i][i];  // compute x^k
>         Step 4  if norm(X - X0)_infty = max(1<=i<=n, X[i] - X0[i]) < TOL then Output(X[]);
>                 STOP;    // successful
>         Step 5  for i = 1, ..., n  Set X0[] = X[];  // update X0
>         Step 6  Set k++;
> Step 7  Output (Maximum number of iterations exceeded);
>         STOP.    // unsuccessful
> ```

- 上述两种迭代方法**不总是收敛的**。并且存在雅可比迭代法失败，但高斯-塞德尔迭代法成功的情况，反之亦然。

### 3. Convergence of Iterative Method
> 考察迭代法 $\vec{x}^{(k)} = T\vec{x}^{(k-1)} + \vec{c}$ 的收敛性。

以下语句是等价的：
- $A$ 是一个收敛矩阵
- 对于<u>某些</u>自然范数，$\lim\limits_{n \rightarrow \infty} \| A^n \| = 0$
- 对于<u>所有</u>自然范数，$\lim\limits_{n \rightarrow \infty} \| A^n \| = 0$
- $\textcolor{red}{\rho(A) < 1}$（比较常用）
- $\forall \vec{x},\ \lim\limits_{n \rightarrow \infty} A^n \vec{x} = \vec{0}$

> [!theorem]  定理
> $\forall \vec{x^{(0)}} \in R^n$，由 $\vec{x}^{(k)} = T\vec{x}^{(k-1)} + \vec{c}\ (k \ge 1)$ 定义的序列 $\{ \vec{x^{(k)}} \}_{k=0}^\infty$，当且仅当 $\textcolor{red}{\rho(T) < 1}$ 时，会收敛到 $\vec{x} = T\vec{x} + \vec{c}$ 的唯一解
> 
> 
>> [!proof] 证明
>> - 假如 $\rho(T) < 1$，那么
>>  
>>    $$
>>          \begin{align}
>>          \vec{x}^{(k)} & = T\vec{x}^{(k-1)} + \vec{c} = T(T\vec{x}^{(k-2)} + \vec{c}) + \vec{c} = T^2 \vec{x^{(k-2)}} + (T + I)\vec{c} \notag \\
>>          & = \dots = \cancel{T^k\vec{x^{(0)}}} + (\textcolor{red}{T^{k-1} + \dots + T + I})\vec{c} \notag
>>          \end{align}$$
>>  
>>    又因为 $\rho(T) < 1 \Rightarrow (I - T)^{-1} = \sum\limits_{j=0}^{\infty} T^j$，所以：
>>  
>>    $$
>>         \lim\limits_{k \rightarrow \infty} \vec{x}^{(k)} = \lim\limits_{k \rightarrow \infty} T^k\vec{x^{(0)}} + \lim\limits_{k \rightarrow \infty} (T^{k-1} + \dots + T + I)\vec{c} = (I - T)^{-1} \vec{c}
>>         $$
>> 
>> - $\lim\limits_{k \rightarrow \infty} \vec{e}^{(k)} \rightarrow \vec{0}\ \Rightarrow\ \lim\limits_{k \rightarrow \infty} T^k \vec{e^{(0)}} = \vec{0} \text{ for any } \vec{e^{0}}$，所以 $\rho(T) < 1$

> [! theorem] 定理
> 对于任意满足 $\|T\| < 1$ 的自然矩阵以及给定的向量 $\vec{c}$，那么 $\forall \vec{x^{(0)}} \in R^n$，由 $\vec{x}^{(k)} = T\vec{x}^{(k-1)} + \vec{c}$ 定义的序列 $\{ \vec{x^{(k)}} \}_{k=0}^\infty$ 会收敛到向量 $\vec{x} \in R^n$，误差边界如下：
>     
>   - $\| \vec{x} - \vec{x^{(k)}}\| \le \|T\|^k \| \vec{x} - \vec{x^{0}}\|$
>         - $\| \vec{x} - \vec{x^{(k)}}\| \approx \rho(T)^k \| \vec{x} - \vec{x^{0}}\|$。因此，**谱半径越小，迭代法的收敛速度越快**
>     
>   - $\| \vec{x} - \vec{x^{(k)}}\| \le \dfrac{\|T\|^k}{1 - \|T\|} \| \vec{x^{(1)}} - \vec{x^{0}}\|$
>     

> [!theorem]  定理
> 如果 $A$ 是一个严格对角占优矩阵，那么对于任意选择的初始近似解 $\vec{x^{(0)}}$，无论使用雅可比方法还是高斯-塞德尔方法，都可以让序列 $\{ \vec{x^{(k)}} \}_{k=0}^\infty$ 收敛到 $A\vec{x} = \vec{b}$ 的唯一解

### 4. Relaxation Methods
- 假设 $\widetilde{\vec{x}} \in \mathbb{R}^n$ 是线性方程组 $A \vec{x} = \vec{b}$ 的近似解，那么线性方程组的 $\widetilde{\vec{x}}$ 的**残差向量**(residual vector)为 $\vec{r} = \vec{b} - A \widetilde{\vec{x}}$

对于高斯-塞德尔方法：
$$
\begin{align}
x_i^{(k)} & = \dfrac{1}{a_{ii}} \Big[ b_i - \sum\limits_{j=1}^{i-1} a_{ij} x_i^{(k)} - \sum\limits_{j=i+1}^n a_{ij} x_j^{(k-1)} \Big] \notag \\
& = x_i^{(k-1)} + \dfrac{r_i^{(k)}}{a_{ii}} \quad \text{ where } r_i^{(k)} = b_i - \sum\limits_{j < i} a_{ij} x_j^{(k)} - \sum\limits_{j \ge i} a_{ij} x_j^{(k-1)} \notag
\end{align}
$$
令 $x_i^{(k)} = x_i^{(k-1)} + \textcolor{red}{\omega} \dfrac{r_i^{(k)}}{a_{ii}}$，选取合适的正数 $\omega$ 能够得到更快的收敛，这样的方法称为**松弛法**(relaxation methods)。根据 $\omega$ 的大小，有以下几类松弛法：
- $0 < \omega < 1$：**欠松弛法**(under-relaxation methods)
- $\omega = 1$：**高斯-塞德尔方法**
- $\omega > 1$：**逐次超松弛法**(successive over-relaxation methods, **SOR**)
  - 通常能加速收敛，“超前”地调整了更新方向，使得迭代步长更大，更快地逼近真实解

用矩阵形式可以表述为：
$$
\begin{align}
x_i^{(k)} & = x_i^{(k-1)} + \omega \dfrac{r_i^{(k)}}{a_{ii}} = (1 - \omega)x_i^{(k-1)} + \dfrac{\omega}{a_{ii}} \Big[ -\sum\limits_{j<i} a_{ij} x_j^{(k)} - \sum\limits_{j>i} a_{ij} x_j^{k-1} + b_i \Big] \notag \\
& \Rightarrow\ \vec{x^{(k)}} = (1 - \omega) \vec{x^{(k-1)}} + \omega D^{-1} [L \vec{x^{(k)}} + U \vec{x^{(k-1)}} + \vec{b}] \notag \\
& \Rightarrow\ \underbrace{(D - \omega L)^{-1} [(1 - \omega) D + \omega U]}_{T_{\omega}} \vec{x}^{(k-1)} + \underbrace{(D - \omega L)^{-1} \omega}_{\vec{c_\omega}} \vec{b} \notag
\end{align}
$$
也就是说，SOR 迭代法的递推公式为：$\vec{x}^{(k)} = T_\omega \vec{x}^{(k-1)} + \vec{c}_\omega \vec{b}$。


> [!theorem]  一些定理
> 定理1
>- **Kahan 定理**：若 $a_{ii} \ne 0\ (i = 1, 2, \dots, n)$，那么 $\rho(T_\omega) \ge |\omega - 1|$，这也就意味着 SOR 方法仅在 $0 < \omega < 2$ 时收敛。
> 
>  定理2
> - **Ostrowski-Reich 定理**：若 $A$ 是**正定**矩阵且 $0 < \omega < 2$，那么 SOR 方法对于任意初始近似解均能收敛。
>     
>  定理3
>  - 如果 $A$ 是**正定**的**三对角线**矩阵，那么 $\rho(T_g) = |\rho(T_j)|^2 < 1$，且 SOR 方法中 $\omega$ 的最优选择是 $\omega = \dfrac{2}{1 + \sqrt{1 - |[\rho(T_j)]^2|}}$，此时 $\rho(T_\omega) = \omega - 1$。

## 7.4 Error Bounds and Iterative Refinement
假设 $A$ 是准确的，$\vec{b}$ 有误差 $\delta \vec{b}$，那么带有误差的解可以写成 $\vec{x} + \delta \vec{x}$，可以得到：
$$
A (\vec{x} + \delta \vec{x}) = \vec{b} + \delta \vec{b} \Rightarrow \dfrac{\| \delta \vec{x} \|}{\| \vec{x} \|} \le \| A \| \cdot \| A^{-1} \| \cdot \dfrac{\| \delta \vec{b} \|}{\| \vec{b} \|}
$$
其中 $\| A \| \cdot \| A^{-1} \|$ 被称为**相对放大因子**(relative amplification factor)。

> [!proof]  证明
由 $\vec{b} = A\vec{x}$，可得 $\|\vec{b}\| \le \|A\| \cdot \|\vec{x}\|$，因此 $\dfrac{1}{\|\vec{x}\|} \le \dfrac{\|A\|}{\|\vec{b}\|}$。所以：
> $$\dfrac{\| \delta \vec{x} \|}{\| \vec{x} \|} \le \dfrac{\| A \| \cdot \| A^{-1} \|}{\| \vec{b} \|} \cdot \| \delta \vec{b} \|$$

> [!theorem] 定理
> 如果矩阵 $B$ 在某些自然范数上满足 $\| B \| < 1$，那么：
> -  $I \pm B$ 是非奇异的
> - $\| (I \pm B)^{-1} \| \le \dfrac{1}{1 - \| B \|}$

---

假如 $\vec{b}$ 是准确的，$A$ 有误差 $\delta A$，那么带有误差的解可以写成 $\vec{x} + \delta \vec{x}$，可以得到：
$$
\begin{align}
& (A + \delta A) (\vec{x} + \delta \vec{x}) = \vec{b} \notag \\
\Rightarrow & \dfrac{\| \delta \vec{x} \|}{\| \vec{x} \|} \le \dfrac{\| A^{-1} \| \cdot \| \delta A \|}{1 - \| A^{-1} \| \cdot \| \delta A \|} = \dfrac{\| A^{-1} \| \cdot \| A \| \cdot \frac{\| \delta A \|}{\| A \|}}{1 - \| A^{-1} \| \cdot \| A \| \cdot \frac{\| \delta A \|}{\| A \|}} \notag
\end{align}
$$
其中 $\| A \| \cdot \| A^{-1} \|$ 是误差放大的关键因子，被称为**条件数**(condition number)，记作 $K(A)$
- 如果 $K(A)$ 接近1，那么矩阵 $A$ 是**良态的**(well-conditioned)
- 如果 $K(A)$ 比远大于1，那么矩阵 $A$ 是**病态的**(ill-conditioned)

> [!theorem] 定理
> 假设 $A$ 是非奇异的，且 $\| \delta A \| < \dfrac{1}{\| A^{-1} \|}$。那么 $(A + \delta A) (\vec{x} + \delta \vec{x}) = \vec{b} + \delta \vec{b}$ 的解 $\vec{x} + \delta \vec{x}$ 近似于 $A \vec{x} = \vec{b}$ 的解 $\vec{x}$，（相对）误差为：
> $$\dfrac{\| \delta \vec{x} \|}{\| \vec{x} \|} \le \dfrac{K(A)}{1 - K(A) \frac{\| \delta A\|}{\| A \|}} \Big(\dfrac{\| \delta A \|}{\| A \|} + \dfrac{\| \delta \vec{b} \|}{\| \vec{b} \|} \Big)$$

> [!note] 注
>条件数 $K(A)_i$ 的下标 $i$ 表示所使用的[矩阵范数](#matrix-norms)的类型（比如 $i=2$ 表示的就是 2-范数）
>- 如果 $A$ 是**对称的**，那么 $K(A)_2 = \dfrac{\max |\lambda|}{\min |\lambda|}$
> -   对于所有自然范数 $\| \cdot \|_p$，$K(A)_p \ge 1$
> - $\forall\ \alpha \in R, K(\alpha A) = K(A)$
> - 如果 $A$ 是正交的（即 $A^{-1} = A^T$），那么 $K(A)_2 = 1$
> - 对于所有正交矩阵 $R$，$K(RA)_2 = K(AR)_2 = K(A)_2$

### Iterative Refinement
**Theorem**
- 假设 $\vec{x}^*$ 是 $A \vec{x} = \vec{b}$ 的近似解，$A$ 是一个非奇异矩阵，$\vec{r} = \vec{b} - A\vec{x}$ 是 $\vec{x}^*$ 的残差向量。那么对于任意自然范数，$\| \vec{x} - \vec{x}^* \| \le \| \vec{r} \| \cdot \| A^{-1} \|$。且如果 $\vec{x} \ne \vec{0}, \vec{b} \ne \vec{0}$，那么：
$$
    \dfrac{\| \vec{x} - \vec{x}^* \|}{\| \vec{x} \|} \le K(A) \dfrac{\| \vec{r} \|}{\| \vec{b} \|}
    $$
**迭代优化**(iterative refinement)的步骤为：
1. $A \vec{x} = \vec{b} \Rightarrow$ 近似解 $\vec{x}_1$
2. $\vec{r}_1 = \vec{b} - A \vec{x}_1$
3. $A \vec{d}_1 = \vec{r}_1 \Rightarrow \vec{d}_1$
   - 如果 $\vec{d}_1$ 是精确的，那么 $\vec{x}_2 = \vec{x}_1 + A^{-1} (\vec{b} - A\vec{x}_1) = A^{-1} \vec{b}$，$\vec{x}_2$ 也是精确的。
4. $\vec{x}_2 = \vec{x}_1 + \vec{d}_1$
之后重复 2-4 步。
