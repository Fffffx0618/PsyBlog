# Chap 9: Approximating Eigenvalues
## 9.1 The Power Method
**幂法**(power method) 是一种用于计算矩阵的**主特征值**(dominant eigenvalue)（矩阵中模长最大的特征值，即**谱半径** $\rho(\lambda)$）以及对应的特征向量的技术。
### 1. The Original Method
假设 $A$ 是一个 $n \times n$ 的矩阵，满足 $|\textcolor{red}{\lambda_1}| \textcolor{red}{>} |\lambda_2| \ge \dots \ge |\lambda_n| \ge 0$，且这些特征值对应 $n$ 个线性独立的特征向量。

思路：从任意 $x^{(0)} \ne 0$ 以及 $(x^{0}, v_1)$ 出发
$$
\begin{align}
x^{(0)} & = \sum\limits_{j=1}^n \beta_j v_j, \beta_1 \ne 0 \notag \\
x^{(1)} & = Ax^{(0)} = \sum\limits_{j=1}^n \beta_j \lambda_j v_j \notag \\
x^{(2)} & = Ax^{(1)} = \sum\limits_{j=1}^n \beta_j \lambda_j^2 v_j \notag \\
& \quad \quad \quad \dots \notag \\
x^{(k)} & = A x^{(k-1)} = \sum\limits_{j=1}^n \beta_j \lambda_j^k v_j \notag \\
& = \lambda_1^k \sum\limits_{j=1}^n \Big(\dfrac{\lambda_j}{\lambda_1}\Big)^k v_j \notag
\end{align}
$$

当 $k$ 足够大时，有：
$$
x^{(k)} \approx \lambda_1^k \beta_1 v_1, x^{(k-1)} \approx \lambda_1^{k-1} \beta_1 v_1 \Rightarrow \dfrac{(x^{(k)})_i}{(x^{(k-1)})_i} \approx \lambda_i
$$
### 1.2 Normalization
**归一化**(normalization) 的目的是确保在每一步满足 $\| x \|_{\infty} = 1$，以确保稳定性。

令 $\| x^{(k)} \|_{\infty} = |x_{p_k}^{(k)}|$，那么 $u^{(k-1)} = \dfrac{x^{(k-1)}}{x^{(k-1)_{p_{k-1}}}}$ 且 $x^{(k)} = A u^{(k-1)}$。因而得到：

$$
u^{(k)} = \dfrac{x^{(k)}}{|x^{(k)}_{p_k}|} \rightarrow v_1 \quad \text{and} \quad \lambda_1 \approx \dfrac{x_i^{(k)}}{u_i^{(k-1)}} = x^{(k)_{p_{k-1}}}
$$

> [!code] "算法：幂法"
> 从非零初始向量开始，近似求解规模为 $n \times n$ 的矩阵 $A$ 的主特征值及其特征向量。
> 
> - 输入：维度 $n$，矩阵 $a[][]$，初始向量 $x0[]$，容忍值 $TOL$，最大迭代次数 $N_{max}$
> - 输出：近似特征值 $\lambda$，近似（规范化的）特征向量
> 
> ```c
> Step 1  Set k = 1;
> Step 2  Find index such that [x0[index]] = norm_infty(x0);
> Step 3  Set x0[] = x0[] / x0[index];    // normalize x0
> Step 4  while (k <= N_max) do steps 5-11
>         Step 5  x[] = A * x0[];
>         Step 6  lambda = x[index]
>         Step 7  Find index such that [x[index]] = norm_infty(x);
>         Step 8  if x[index] == 0 then
>                     Output("A has the eigenvalue 0", x[0]);
>                     STOP.
>                 // the matrix is singular and user should try a new x0
>         Step 9  err = norm_infty(x0 - x / x[index]);
>                 x0[] = x[] / x[index]      // computer u^k
>         Step 10 if (err < TOL) then
>                     Output(lambda, x0[]);
>                     STOP.
>         Step 11 Set k++;
> Step 12 Output(Maximum number of iterations exceeded);
>         STOP.    // unsucessful
> ```

> [!Note] 注
> - 该方法在有**多重特征值**（即存在 $\lambda_1 = \lambda_2 = \dots = \lambda_r$）的情况下也能生效，因为：
> $$
>         x^{(k)} = \lambda_1^k \Big[ \sum\limits_{j=1}^r \beta_j v_j + \sum\limits_{j=r+1}^n \beta_j \Big(\dfrac{\lambda_j}{\lambda_1}\Big)^k v_j \Big] \approx \lambda_1^k \Big( \sum\limits_{j=1}^r \beta_j v_j \Big)
>         $$
> - 若存在类似 $\lambda_1 = -\lambda_2$ 的情况，那么该方法就会失效。
> - 因为我们无法确保对于任意初始近似向量 $\bm{x^{(0)}}$，$\beta_1 \ne 0$，所以在这种情况下的迭代结果可能就不是 $\bm{v_1}$，而时第一个满足 $(\bm{x^{(0)}}, \bm{v_m}) \ne 0$，关联的特征值为 $\lambda_m$。

### 1.3 Rate of Convergence
在前面的计算中得到：
$$x^{(k)} = Ax^{(k-1)} = \lambda_1^k \sum\limits_{j=1}^n \Big(\dfrac{\lambda_j}{\lambda_1}\Big)^k v_j$$
现在，我们的目标是使 $\Big| \dfrac{\lambda_2}{\lambda_1} \Big|$ 的值尽可能小，以加快收敛速度。

假设 $\lambda_1 > \lambda_2 \ge \dots \lambda_n$，且 $|\lambda_2| > |\lambda_n|$
<div style="text-align: center">
    <img src="image-33.png" width=90%/>
</div>

思路：令 $B = A - pI$，那么 $|\lambda I - A| = |\lambda I - (B + pI)| = |(\lambda - p) I - B|$，这样可以得到 $\lambda_A - p = \lambda_B$。因为 $\dfrac{\lambda_2 - p}{\lambda_1 - p} < \dfrac{|\lambda_2|}{|\lambda_1|}$，寻找 $B$ 的特征值的迭代收敛速度快于关于 $A$ 的迭代
### 1.4 Inverse Power Method
**反幂法**(inverse power method) 是幂法的一种改进方法，相比幂法能够更快地收敛。下面给出具体计算过程：

如果 $A$ 有特征值 $|\lambda_1| \ge |\lambda_2| \ge \dots \textcolor{red}{> |\lambda_n|}$，那么对于 $A^{-1}$ 满足：

$$
\textcolor{red}{\Big|\dfrac{1}{\lambda_n}\Big| > } \Big|\dfrac{1}{\lambda_{n-1}}\Big| \ge \dots \ge \Big| \dfrac{1}{\lambda_1} \Big|
$$

并且这些特征值对应于相同的特征向量。

$A^{-1}$ 的主特征值 $\Leftrightarrow$ $A$ 的特征值中的最小值

要想迭代计算 $x^{(k+1)} = A^{-1} x^{(k)}$，就得在每次迭代步骤中求解线性方程组 $A x^{(k+1)} = x^{(k)}$，其中 $A$ 需要被分解 (factorized)

思路：如果我们知道 $A$ 的一个特征值 $\lambda_i$ 最接近一个指定值 $p$，那么对于任意的 $j \ne i$，我们有 $|\lambda_i - p| << |\lambda_j - p|$。并且，如果存在 $(A - pI)^{-1}$，那么逆幂法能以更快的收敛速度寻找到 $(A - pI)^{-1}$ 的主特征值 $\dfrac{1}{\lambda_i - p}$

> [!Code] 算法：反幂法
> 从非零初始向量开始，近似求解规模为 $n \times n$ 的矩阵 $A$ 的主特征值及其特征向量。
> - 输入：维度 $n$，矩阵 $a[][]$，初始向量 $x0[]$，容忍值 $TOL$，最大迭代次数 $N_{max}$
> - 输出：近似特征值 $\lambda$，近似（规范化的）特征向量
> ```c
> Step 1  Set q = (x[]^T · A · x[]) / (x^T · x[]);
> Step 2  Set k = 1;
> Step 3  Find the smallest integer p with 1 <= p <= n and |x_p| = norm_infty(x);
> Step 4  Set x[] = x[] / x_p
> Step 5  while (k <= N_max) do steps 6-12
>         Step 6  Solve the linear system (A - qI)y = x;
>         Step 7  if the system does not have a unique solution, then
>                     Output("q is an eigenvalue", q);
>                     STOP.
>         Step 8  set lambda = y_p;
>         Step 9  Find the smallest integer p with 1 <= p <= n and |y_p| = norm_infty(y);
>         Step 10  err = norm_infty(x[] - y[] / y_p);
>                  x[] = y[] / y_p;
>         Step 11 if (err < TOL) then
>                     Output(lambda, x[]);
>                     STOP.
>         Step 12 Set k++;
> Step 13 Output(Maximum number of iterations exceeded);
>         STOP.
> ```