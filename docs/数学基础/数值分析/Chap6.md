# Chapter 6. Direct Methods for Solving Linear Systems
> [!Target] 
> Solve $A\vec{x}=\vec{b}$
## 6.1 Linear Systems of Equations
### 1. Gaussian Elimination
 ==高斯消元法==：
- First reduce $A$ into an **upper-triangular 上三角** matrix
- Then solve the unknowns by a **backward-substitution 回代** process
<div text-align="center"><img src="image-7.png" width="40%"></div>
**消元**(elimination) 的实现：先令 $A^{(1)} = A = (a_{ij}^{(1)})_{n \times n}, b^{(1)} = b = \begin{bmatrix}b_1^{(1)} \\ \vdots \\ b_n^{(1)}\end{bmatrix}$

- 第 1 步：
    - 如果 $a_{11}^{(1)} \ne 0$，计算 $m_{i1} = \dfrac{a_{i1}^{(1)}}{a_{11}^{(1)}}, (i = 2, \dots, n)$
    - 那么增广矩阵 (augmented matrix) 的第 $i$ 行 $\text{row}_i$ 为：$m_{i1} \times \text{row}_1$，得到$$
        \left[
        \begin{array}{cccc|c}
        a_{11}^{(1)} & a_{12}^{(1)} & \cdots & a_{1n}^{(1)} & b_1^{(1)} \\
        0 & & A^{(2)} & & b^{(2)} \\
        \end{array}
        \right]
        $$
    其中 $\begin{cases}a_{ij}^{(2)} = a_{ij}^{(1)} - m_{i1} a_{1j}^{1} \\ b_i^{(2)} = b_i^{(1)} - m_{i1} b_1^{(1)}\end{cases}, (i, j = 2, \dots, n)$
- 第 k 步：
    - 如果 $a_{kk}^{(k)} \ne 0$，计算 $m_{ik} = \dfrac{a_{ik}^{(k)}}{a_{kk}^{(k)}}, (i = k+1, \dots, n)$
	    - $\begin{cases}a_{ij}^{(k+1)} = a_{ij}^{(k)} - m_{ik} a_{kj}^{k} \\ b_i^{(k+1)} = b_i^{(k)} - m_{ik} b_k^{(k)}\end{cases}, (i, j = k+1, \dots, n)$
	- 如果 $a_{kk}^{(k)} = 0$，找到最小的整数 $i \ge k$ 且 $a_{ik}^{(k)} \ne 0$，然后交换第 $k$ 行和第 $i$ 行
- 最终可得到 $A$ 的**增广矩阵**：$$ \begin{bmatrix} a_{11}^{(1)} & a_{12}^{(1)} & \cdots & a_{1n}^{(1)} \\ &a_{22}^{(2)} & \cdots  & a_{2n}^{(2)} \\ && \cdots  & \vdots \\ && & a_{nn}^{(n)} \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix} = \begin{bmatrix} b_1^{(1)} \\ b_2^{(2)} \\ \vdots \\ b_n^{(n)} \end{bmatrix} $$
**回代**的实现（从 $n$ 到 $1$）：
- $x_n = \dfrac{b_n^{(n)}}{a_{nn}^{(n)}}$
- $x_i = \dfrac{b_i^{(i)} - \sum\limits_{j=i+1}^n a_{ij}^{(i)} x_j}{a_{ii}^{(i)}}, (i = n - 1, \dots, 1)$

> [!Code implement]
> 求解 $n\times n$ 线性方程组
> ```c
> Step 1  for i = 1, ..., n - 1 do Steps 2-4:
>     Step 2  Let p be the smallest integer with i <= p <= n and a[p][i] != 0;
>             if no integer p can be found
>                 then Output('no unique solution exists');
>                 STOP;
>             // row exchange
>     Step 3  if p != i then perform (E[p]) <-> (E[i]);
>             // elimination
>     Step 4  for j = i + 1, ..., n do Step 5 and 6:
>         Step 5  Set m[j][i] = a[j][i] / a[i][i]
>         Step 6  Perform (E[j] - m[j][i] * E[i]) -> (E[i])
>     Step 7  if a[n][n] = 0 then Output('no unique solution exists');
>                 STOP;
>             // backward substitution
>     Step 8  Set x_n = a[n][n+1] / a[n][n]
>     Step 9  for i = n - 1, ..., 1 set x[i] = [a[i][n+1] - sum(j=i+1, n, a[i][j] * x[j])] / a[i][i];
>     Step 10 Output(x[1], ..., x[n]);
>             STOP;    // success
> ```

### 2. Amount of Computation
统计计算量，此处仅考虑**乘法**和**除法**

Elimination：
$$
\sum_{k=1}^{n-1}(n-k)(n-k+2)=\frac{n^3}{3}+\frac{n^2}{2}-\frac{5}{6}n
$$
Backward-subtitution:
$$
1+\sum_{i=1}^{n-1}(n-i+1)=\frac{n^2}{2}+\frac{n}{2}
$$
因此，高斯消元法的算法复杂度为 $O (N^3)$
## 6.2 Pivoting Strategies
> Problem: Small ==pivot 主元== element may cause trouble
> 除非有特殊说明，以下的 k 指的是第 k 次高斯消元

### 1. Partial Pivoting
==部分主元法==：找到最小的 $p$，使得 $|a_{pk}^{(p)}|=\max_{k\leq i \leq n}|a_{ik}^{(k)}|$，然后交换第 $p$ 行和第 $k$ 行
> [!缺陷]
> - 有时根据部分主元法，解方程时无需交换行，但某一行内各个元素的量级可能相差巨大，而另一行的元素量级相近，这会导致较大的误差

### 2. Scaled Partial Pivoting
==缩放主元法==：首先让每一行的元素都除以该行的最大元素的绝对值，然后进行部分主元选取，再对原方程组部分进行行交换，从而选取主元。
- Step 1
	- 定义每行的缩放因子（scale factor）$s_i=\max_{1 \leq j \leq n}|a_{ij}|$ （每行绝对值最大的元素）
- Step 2
	- 找到最小的 $p$，使得 $\dfrac{|a_{pk}^{(k)}|}{s_p}=\max_{k\leq i \leq n}\dfrac{|a_{ik}^{(k)}|}{s_i}$，然后交换第 $p$ 行和第 $k$ 行 
### 3. Complete Pivoting
==完全主元法==（或称最大主元法 maximal pivoting）：搜索所有的元素 $a_{ij}(i,j=k,…,n)$，找出其中的最大元素。通过**互换**(interchange) 行和列，使得该元素来到主元的位置上。
### 4. Amount of Computation
- 部分主元法：需要 $O(n^2)$ 次**比较**
- 缩放部分主元法：需要 $O(n^2)$ 次**比较**，以及 $O(n^2)$ 次**除法**
	- 新的缩放因子在行交换的时候才被确定，则需要 $O(n^3)$ 次额外的**比较**，以及 $O(n^2)$ 次**除法**
- 完全主元法：需要 $O(n^3/3)$ 次**比较**
## 6.5 Matrix Factorization
Matrix Factorization (矩阵分解) 是高斯消元法的改进方法
注：下式中 $A^{(1)}$ 表示原矩阵，$A^{(k)}$ 表示第 $k-1$ 次消元后得到的矩阵
### LU 分解
- Step 1
	- $m_{i1}=\dfrac{a_{i1}}{a_{11}} (a_{11}\ne 0)$
	- Let $M_1 = \begin{bmatrix} 1 & & & \\ -m_{21} & 1 & & \\ \vdots & & \ddots & \\ -m_{n1} & & & 1 \end{bmatrix}$ （**第一高斯变换矩阵**first Gaussian transformation matrix），那么 $M_1[A^{(1)} \quad \boldsymbol{b}^{(1)}] = \begin{bmatrix} a_{11}^{(1)} & \cdots & a_{1n}^{(1)} & b_1^{(1)} \\ O & & A^{(2)} & \boldsymbol{b}^{(2)} \end{bmatrix}$
	- 这一步完成了**第一列的消元**
- Step k
	-  **第 $k$ 高斯变换矩阵**（$k_{th}$ Gaussian transformation matrix） $M_k = \begin{bmatrix} 1 & & & & \\ & \ddots & & & \\ & & 1 & & \\ & & -m_{k+1,k} & & & \\&&\vdots&\ddots\\ & & -m_{n,k} & & 1   \end{bmatrix} \quad \text{(空的地方都是 0)}$
	- $m_{ik}=\dfrac{a_{ik}^{(k)}}{a_{kk}^{(k)}}(a_{kk}^{(k)}\ne 0)$
- Step n-1: 
	-  $M_{n-1} M_{n-2} \dots M_1 [A \quad \boldsymbol{b}] = \begin{bmatrix} a_{11}^{(1)} & a_{12}^{(1)} & \cdots & a_{1n}^{(1)} & b_1^{(1)} \\ & a_{22}^{(2)} & \cdots & a_{2n}^{(2)} & b_2^{(2)} \\ & & \ddots & \vdots & \vdots \\ & & & a_{nn}^{(n)} & b_n^{(n)} \end{bmatrix}$

根据上式，令 $L_k=(M_k)^{-1} = \begin{bmatrix} 1 & & & & \\ & \ddots & & & \\ & & 1 & & \\ & & m_{k+1,k} & & & \\&&\vdots&\ddots\\ & & m_{n,k} & & 1   \end{bmatrix} \quad$，可以得到如下的定理：
> [!Theorem]
> 若高斯消元法能够在**不使用行互换**的基础上求解线性方程组 $A\vec{x}=\vec{b}$，那么矩阵 $A$ 可以被因式分解为一个下三角矩阵 (lower -triangular matrix) $L$ 和上三角矩阵 (upper -triangular matrix)  $U$ 的乘积，
> 即：
> $$A=LU$$
> 其中：
> $$U = \begin{bmatrix} a_{11}^{(1)} & a_{12}^{(1)} & \cdots & a_{1n}^{(1)} \\ 0 & a_{22}^{(2)} & \cdots & a_{2n}^{(2)} \\ \vdots & \vdots & \ddots & \vdots \\ 0 & \cdots & \cdots & a_{nn}^{(n)} \end{bmatrix}, L = \begin{bmatrix} 1 & 0 & \cdots & 0 \\  m_{21} & 1 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ m_{n1} & \cdots & m_{n,n-1} & 1 \end{bmatrix},m_{ji}=\frac{a_{ji}^{(i)}}{a_{ii}^{(i)}}$$
> 如果矩阵 $L$ 是**单位的**(unitary)（即主对角线元素都是 $1$），那么得到的矩阵分解是**唯一的**
> 注：$L=(M_{n-1} M_{n-2} \cdots M_1)^{-1}=L_1 L_2 \dots L_{n-1}$

> [!唯一性证明]
> 反证法
> 如果 $\mathbf{A} = \mathbf{L}_1\mathbf{U}_1 = \mathbf{L}_2\mathbf{U}_2$，其中 $\mathbf{L}_1$ 和 $\mathbf{L}_2$ 是单位下三角矩阵，$\mathbf{U}_1$ 和 $\mathbf{U}_2$ 是上三角矩阵。则有 $$\mathbf{U}_1\mathbf{U}_2^{-1} = \mathbf{L}_1^{-1}\mathbf{L}_2$$ 因为**上三角阵的逆依然是上三角阵，下三角阵同理**。所以等式左右分别为上三角阵和下三角阵。又因为 $\mathbf{L}_1^{-1}\mathbf{L}_2$ 的对角线上的元素均为 1，所以两式相等当且仅当 $$ \mathbf{U}_1\mathbf{U}_2^{-1} = \mathbf{L}_1^{-1}\mathbf{L}_2 = \mathbf{I} $$ 即 $\mathbf{U}_1 = \mathbf{U}_2$，$\mathbf{L}_1 = \mathbf{L}_2$。所以这个分解是==唯一的==

Note：如果 $U$ 也是**单位的**，那么这种分解就称为 **Crout 分解**。可通过对 $A^T$ 的 $LU$ 分解来实现 Crout 分解。也就是说，找到 $A^T=LU$，那么 $A=U^TL^T$ 就是 $A$ 的 ==Crout 分解==

## 6.6 Special Types of Matrices
### 1. Strictly Diagonally Dominant Matrix
**严格对角占优矩阵**(strictly diagonally dominant matrix) 满足：
$$
|a_{ii}|\geq \sum_{j=1,j\ne i}^{n}|a_{ij}|,\text{for each }i=1,\dots,n.
$$
> [!Theorem]
> - 严格对角占优矩阵 $A$ 是**非奇异的**(nonsigular)（即行列式不为 0，且存在逆矩阵）
> - 在这种矩阵上使用高斯消元法**无需**行或列的**互换**
> - 并且计算将相对于舍入误差的增长保持**稳定**
> **Proof**
> - $A$ 是非奇异的——反证法证明
> - 高斯消元法无需行或列的互换——归纳法证明：通过高斯消元法得到的每一个矩阵 $A^{(2)},A^{(3)},\dots,A^{(n)}$ 都是严格对角占优的

### 2. Choleski's Method for Positive Definite Matrix
【Definition】：对于一个矩阵 $A$，如果它是**对称的**，且 $∀\vec{x}≠0,\vec{x}^TA\vec{x}>0$ 成立，那么称该矩阵是**正定**(positive definite) 
> [!Review] 
>   正定矩阵 $A$ 的性质：
> - $A^{−1}$ 也是正定的, $a_{ii}>0$
> - $\max∣a_{ij}∣\leq \max⁡∣a_{kk}∣;(a_{ij})^2 < a_{ii}a_{jj} \text{ for each }i\ne j$
> - $A$ 的每个**前导主子矩阵**(leading principal submatrices) $A_k$ 的行列式 (determinant) 都是正的
> 	- $A_{k} = \begin{bmatrix} a_{11} & a_{12} & \cdots & a_{1k} \\  a_{21} & a_{22} & \cdots & a_{2k} \\ \vdots & \vdots & \ddots & \vdots \\ a_{k1} & a_{k2} & \cdots & a_{kk} \end{bmatrix},1\leq k \leq n$

Consider the $LU$ factorization of a *positive definite* $A$:
- $U$ 进一步拆分成对角矩阵 $D$ 和单位上三角矩阵 $\widetilde{U}$
<div text-align="center"><img src="image-10.png" width="70%"></div>
- $A = A^T \Rightarrow LU = LD \widetilde{U} = \widetilde{U}^T DL^T \Rightarrow L = \widetilde{U}^T \Rightarrow A = LDL^T$
这样我们得到了另一种矩阵分解—— $LDL^T$ 分解
---

令 $D^{\frac{1}{2}} = \begin{bmatrix}\sqrt{u_{11}} & & & \\ & \sqrt{u_{22}} & & \\ & & & & \\ & & & \sqrt{u_{nn}}\end{bmatrix}$，$\widetilde{L}=LD^{\frac{1}{2}}$ 仍然是一个下三角矩阵，因此 $A=\widetilde{L}\widetilde{L}^T$

> [!Theorem]
> 若 $A$ 是**正定矩阵**，那么：
> - 当 $L$ 是一个对角线元素均为 $1$ 的下三角矩阵，并且 $D$ 是一个对角项均为正数的对角矩阵时，$A$ 可被分解为 $LDL^T$
> - 当 $L$ 是一个对角线上均为非零元素的下三角矩阵时，$A$ 可被分解为 $LL^T$

### 3. Crout Reduction for Tridiagonal Linear System
> 对于一个 $n \times n$ 的矩阵，如果有整数 $p, q$，满足 $1 < p, q < n$，当 $i + p \le j$ 或 $j + q \le i$ 时，有 $a_{ij} = 0$，那么称该矩阵为==带状矩阵(band matrix)==，其**带宽**(bandwidth)为 $w = p + q - 1$

当 $p=q=2$ 时，$w=3$，此时的矩阵称为**三对角矩阵**(tridiagonal matrix)，形式如下：
$$
 \begin{bmatrix}b_{1} & c_{1} & 0 &  \dots & 0 \\ a_{2} & b_{2} & c_{2} & \dots  & \vdots  \\ \vdots & \ddots & \ddots & \ddots  & 0 \\ 0 & 0 & a_{n-1} & b_{n-1} & c_{n-1}  \\ 0 & \dots & \dots & a_n & b_n \end{bmatrix}
 \begin{bmatrix}
 x_1 \\x_2 \\ \vdots \\ \vdots \\ x_n
 \end{bmatrix}
 =
  \begin{bmatrix}
 f_1 \\f_2 \\ \vdots \\ \vdots \\ f_n
 \end{bmatrix}
$$
对于上述形式的线性方程组，我们采用一种特殊的 $LU$ 分解，称为 ==Crout 分解==
Steps：
1. 寻找矩阵 $A$ 的 Crout 分解：$$
A = 
\begin{bmatrix}
\alpha_1 &        &        &        \\
\gamma_2 & \ddots &        &        \\
        & \ddots & \ddots &        \\
        &        & \gamma_n & \alpha_n
\end{bmatrix}
\begin{bmatrix}
1 & \beta_1 &        &        \\
   & \ddots & \ddots &        \\
   &        & \ddots & \beta_{n-1} \\
   &        &        & 1
\end{bmatrix}
$$
2. 求解 $L\vec{y} = \vec{f} \Rightarrow y_1 = \dfrac{f_1}{\alpha_1}, \quad y_i = \dfrac{f_i - \gamma_i y_{i-1}}{\alpha_i} \quad (i = 2, \ldots, n)$
3. 求解 $Ux = y \Rightarrow x_n = y_n, \quad x_i = y_i - \beta_i x_{i+1} \quad (i = n-1, \ldots, 1)$

> [!Theorem]
> 如果 $A$ 是三对角(tridiagonal)矩阵，且是对角线占优(diagonally dominant)的，并满足 $|b_1| > |c_1| > 0, |b_n| >|a_n| > 0, a_i \ne 0, c_i \ne 0$，那么 $A$ 是非奇异的，并且其对应的线性方程组有解

Note:
- 如果 $A$ 是严格对角占优(strictly diagonally dominant)，那么没有必要让所有的 $a_i, b_i, c_i$ 都是非零的
- 该方法是稳定的，因为所有从计算过程中获得的值会被约束在原有元素的范围内
- 计算量为 $O(n)$
