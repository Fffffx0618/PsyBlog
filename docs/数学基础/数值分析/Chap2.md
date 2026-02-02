# Chapter 2. Solutions of Equations in One Variable
## 2.1 The Bisection Method
> **二分法**(bisection method) 是利用**介值定理**(intermediate value theorem) ，通过二分不断逼近真正的根。

- 如果 $f\in C[a, b]$，且 $K$ 是介于 $f(a)$ 和 $f(b)$ 之间的任意值，那么存在一个数 $p \in (a, b)$，使得 $f(p)=K$
<div text-align="center"><img src="image-5.png" width="50%"></div>
> [!note] **迭代何时结束**
> 以下几种条件都可作为停止迭代的根据：
> - 绝对误差：$|p_N - p_{N-1}| < \varepsilon$
> - 相对误差：$\dfrac{|p_N - p_{N-1}|}{|p_N|} < \varepsilon$ 
> - 函数值：$|f(p_N)| < \varepsilon$ 
> 
> 使用误差作为依据的时候要当心：存在序列 $\{p_N\}$ 发散的情况，这个时候不应该将误差作为判断依据

**Theorem**
假设 $f \in C[a, b]$ 且满足 $f(a) \cdot f(b) < 0$，那么二分法将产生一个序列 $\{p_n\} (n = 1, 2, \dots)$，用于逼近 $f$ 的一个零点 $p$，并满足：
$$ |p_n - p| \le \dfrac{b - a}{2^n} \quad \text{when } n \ge 1 $$
> [!代码实现]
> ```c
> Step 1  Set i = 1;
>             FA = f(a);
> Step 2  while (i <= N_max) do steps 3-6
>         Step 3  Set p = a + (b - a) / 2;  // computer p_i
>                 FP = f(p);
>         Step 4  if (FP == 0) or (b - a) / 2 < TOL then Output(p);
>                 STOP;  // successful
>         Step 5  Set i++;
>         Step 6  if sign(FA) * sign(FP) > 0 then Set a = p; FA = FP;
>                 else set b = p;  // update a_i, b_i
> Step 7  Output(Method failed after N_max iterations);  // unsuccessful
>         Stop.
> ```
> - `p = a + (b - a) / 2`：可以减小误差
> - `sign(FA) * sign(FP) > 0`：防止数据溢出（overflow）

---
## 2.2 Fixed-Point Iteration
将 $f(x)$ 的根看作 $g(x)$ 的不动点（ $g(x)=f(x)+x$ ），即：$$f(x)=0 \stackrel{equivalent} \Leftrightarrow x = g(x)$$
- 从初始的近似值 $p_0$ 开始，通过 $p_n = g(p_{n-1})$（其中 $n \ge 1$），产生序列 $\{p_n\}_{n=0}^\infty$。如果该序列能收敛到 $p$，且 $g$ 是一个连续函数，那么：
$$
p = \lim\limits_{n \rightarrow \infty} p_n = \lim\limits_{n \rightarrow \infty} g(p_{n-1}) = g(\lim\limits_{n \rightarrow \infty} p_{n-1}) = g(p) 
$$
> [!Note] 如下图，并非所有的 $g (x)$ 可以使用迭代法
> - 蛛网模型
> <img src='image-1.png'>
> 

**Theorem（不动点定理）**
- 令 $g \in C[a, b]$，且 $g(x) \in [a, b],\forall x \in [a, b]$。并且一阶导函数 $g'$ 存在于区间 $(a, b)$，且满足 $\forall x \in (a, b)$，$\exists$ 常数 $k \in (0, 1)$ 使得 $|g'(x)| \le k$ 成立。那么 $\forall p_0 \in [a, b]$，由 $p_n = g(p_{n-1}), n \ge 1$ 定义的序列会收敛到位于区间 $[a, b]$ 上的唯一不动点。

> [!Proof]
> 对于上述定理，我们需要证明三个点：
> - “存在”：令 $f(x) = g(x) - x$，因为 $a \le g(x) \le b$，所以 $f(a) = g(a) - a \ge 0$ 且 $f(b) = g(b) - b \le 0$。由**介值定理**，$f$ 在 $[a, b]$ 上一定有根，==因此 $g$ 在 $[a,b]$ 上存在不动点==
> - “唯一”：（用**反证法**证明）
>     - 假设 $p, q$ 都是 $g$ 在区间 $[a, b]$ 上的两个不同的不动点
>     - 根据**均值定理**(mean value theorem)，存在一个位于 $p, q$ 的数 $\xi$，满足 $g(p) - g(q) = g'(\xi)(p - q)$
>     - 因为 $g(p) = p, g(q) = q$，所以可以得到 $(1 - g'(\xi))(p - q) = 0$，和已知条件矛盾，因此假设不成立，即“==不动点是唯一的==”成立
> 
> - “收敛”：即证明 $\lim\limits_{n \rightarrow \infty} |p_n - p| = 0$
>     - 因为 $\forall x \in [a, b]$，$g(x) \in [a, b]$，所以 $\forall n \ge 0$，$p_n$ 都是有定义的
>     - 因此：
> 
>         $$
>         \begin{align}
>         |p_n - p| & = |g(p_{n-1}) - g(p)| = |g'(\xi)||p_{n-1} - p| \le k|p_{n-1} - p| \notag \\
>         & \le k^2 |p_{n-2} - p| \le \dots \le k^n|p_0 - p| \notag
>         \end{align}
>         $$
> 
>     - 根据条件，$k \in (0, 1)$，所以 $k^n \rightarrow 0$，==因此 $\lim\limits_{n \rightarrow \infty} |p_n - p| = 0$ 成立==

**Corollary**
- 如果 $g$ 满足不动点定理的假设，那么用 $p_n$（$\forall n \ge 1$）近似表示 $p$ 所产生的误差边界为： 
$$ |p_n - p| \le \dfrac{1}{1 - k}|p_{n+1} - p_n| \quad \text{and} \quad |p_n - p| \le \dfrac{k^n}{1 - k} |p_1 - p_0|$$
- 左式可用于控制精度，右式可知 $k$ 越小收敛速度越快
**Proof**
-  $|p_{n+1} - p_n| \ge |p_n - p| - |p_{n+1} - p| \ge |p_n - p| - k|p_n - p|=(1-k)|p_n-p|$
-  $|p_{n+1} - p_n| = |g(x_n) - g(x_{n-1})| = |g'(\xi_n)(p_n - p_{n-1})| \le k|p_n - p_{n-1}| \le \dots \le k^n |p_1 - p_0|$
---
## 2.3 Newton's Method
> 牛顿法实际上也是一种不动点迭代，使用**泰勒展开式**(Taylor's expansion) 来线性化一个非线性的函数，通过迭代 $p_n=g(p_{n-1})$ 逼近 $g$ 的不动点
   
令 $p_0 \in [a, b]$ 为 $p$ 的一个近似值，满足 $f'(p) \ne 0$，考虑以下 $f(x)$ 关于 $p_0$ 的泰勒多项式：
$$
f(x) = f(p_0) + f'(p_0)(x - p_0) + \dfrac{f''(\xi_x)}{2!} (x - p_0)^2 \quad \text{where } \xi_x \text{ lies between } p_0 \text{ and } x
$$
假设 $|p - p_0|$ 很小，那么 $(p - p_0)^2$ 会更小（可近似忽略），那么：
$$
0  = f(p) \approx f(p_0) + f'(p_0) (p - p_0) \Rightarrow p \approx p_0 - \dfrac{f(p_0)}{f'(p_0)}
$$
过程如下图，
![[image-4.png|256x166]]
从上述过程中，我们不难得到以下递推关系式：
$$
p_n = p_{n-1} - \dfrac{f(p_{n-1})}{f'(p_{n-1})} \quad \text{for } n \ge 1
$$
> [!Theorem]
> - 令 $f \in C^2[a, b]$（即函数具有二阶连续导数）。如果 $p \in [a, b]$ 满足 $f(p) = 0$ 且 $f'(p) \ne 0$，那么存在一个 $\delta > 0$，使得牛顿法产生一个序列 $\{p_n\} (n = 1, 2, \dots)$，对任意近似值 $p_0 \in [p - \delta, p + \delta]$，该序列收敛于 $p$

> [!Code implement]
> 给定一个初始近似值 $p_0$ ​，找到 $f(x)=0$ 的一个解。
> - 输入：初始近似值 $p_0$ ​；容忍值 $TOL$；最大迭代次数 $N_{max}$
> - 输出：近似解 $p$ 或错误信息
> ```c
> Step 1  Set i = 1;
> Step 2  while (i <= N_max) do steps 3-6
>         Step 3  Set p = p_0 - f(p_0) / f'(p_0);  // compute p_i
>         Step 4  if |p - p_0| < TOL then Output(p);  // successful
>             STOP;
>         Step 5  Set i++;
>         Step 6  Set p_0 = p;  // update p_0
> Step 7  Output(The method failed after N_max iterations);  // unsuccessful
> ```

---
## 2.4 Error Analysis for Iterative Methods
**Definition**
假设 $\{p_n\} (n = 0, 1, 2, \dots)$ 是一个收敛到 $p$ 的序列，且 $\forall n, p_n \ne p$。若存在正常数 $\alpha, \lambda$，使得：
$$
    \lim\limits_{n \rightarrow \infty} \dfrac{|p_{n+1} - p|}{|p_n - p|^\alpha} = \lambda
    $$
那么 $\{p_n\} (n = 0, 1, 2, \dots)$ 以阶数 (order) $\alpha$ 收敛到 $p$，且渐进误差常量(asymptotic error constant)为 $\lambda$。
- 若 $\alpha = 1$，那么序列是**线性(linearly)收敛**的
	- 迭代法（$g'(p)\ne 0$）：
	- $$\lim\limits_{n \rightarrow \infty} \dfrac{|p_{n+1} - p|}{|p_n - p|} = \lim\limits_{n \rightarrow \infty} \dfrac{g'(\xi_{n})|p_{n} - p|}{|p_n - p|}=|g'(p)|$$ 
- 若 $\alpha = 2$，那么序列是**二次(quadratically)收敛**的
	- 牛顿法：$$ p = p_n - \underbrace{\frac{f(p_n)}{f'(p_n)}}_{p_{n+1}} - \frac{f''(\xi_n)}{2!f'(p_n)}(p - p_n)^2 \Rightarrow \frac{|p_{n+1} - p|}{|p_n - p|^2} = \frac{f''(\xi_n)}{2f'(p_n)} $$
	- 只要 $f' (p)\neq 0$，牛顿法至少是**二次收敛**的
所以， $\alpha$ *越大*，收敛速度*越快*。

> [!Theorem]
> 令 $p$ 是 $g(x)$ 的不动点。如果存在一些常量 $\alpha \geq 2$，使得 $g \in C^\alpha[p - \delta, p + \delta]$，$g'(p) = \cdots = g^{(\alpha-1)}(p) = 0$ 且 $g^{(\alpha)}(p) \neq 0$，那么关于 $p_n = g(p_{n-1})$，$n \geq 1$ 的迭代是 $\alpha$ 阶收敛的。
> 
>  **Proof**
> 根据泰勒展开的结果易证 $$ p_{n+1} = g(p_n) = \underbrace{g(p)}_{=p} + g'(p)(p_n - p) + \cdots + \underbrace{\frac{g^{(\alpha)}(\xi_n)}{\alpha!}}_{=\lambda \text{ (when } n \to \infty)} (p_n - p)^\alpha $$

**Multiple roots 重根**
假设 $p$ 是 $f$ 中的一个根，且重数为 $m$，那么 $f(x)=(x-p)^mq(x)$ 且 $q(x)\ne 0$。
根据牛顿法：
$$
p_n = g(p_{n-1}) \quad \text{for } n \ge 1 \quad \text{with} \quad g(x) = x - \frac{f(x)}{f'(x)}
$$
可以推导出：
$$
g'(p) = \left| 1 - \frac{f'(p)^2 - f(p)f''(p)}{f'(p)^2} \right| = 1 - \frac{1}{m} < 1
$$

所以此时牛顿法收敛，但不是二次收敛。
> [!加快收敛速度的方法]
> 令 $\mu (x)=\dfrac{f(x)}{f'(x)}=\dfrac{(x-p)q(x)}{mq(x)+q'(x)(x-p)}$，易知 $p$ 是 $\mu (x)$ 的单根，
> 因此可以使用**牛顿迭代法**处理：
> $$ \begin{aligned} p_{n+1} &= g(p_n) = p_n - \frac{\mu(p_n)}{\mu'(p_n)} \\ &= p_n - \frac{\frac{f(p_n)}{f'(p_n)}}{\frac{f'(p_n)f'(p_n) - f(p_n)f''(p_n)}{(f'(p_n))^2}} \\ &= p_n - \frac{f(p_n)f'(p_n)}{[f'(p_n)]^2 - f(p_n)f''(p_n)} \end{aligned} $$
> - 优点：二次收敛
> - 缺点：
> 	- 需要额外计算 $f''(x)$
> 	- 分母是两个都接近于 $0$ 的数的差
## 2.5 Accelerating Convergence
### 1. Aitken's $\Delta^2$ Method
> [!Definition]
> 对数列 ${p_n}(n=1,2,\dots)$，==前向差（forward difference）==定义为 $\Delta p_n = p_{n+1}-p_n(n\geq 0)$，更高次的幂 $\Delta ^k p_n$ 可以被递归定义为 $\Delta ^k p_n = \Delta (\Delta ^{k-1}p_n)(k \geq 2)$
> 注：$\Delta^2p_n=\Delta p_{n+1}-\Delta p_n=p_{n+2} - 2p_{n+1} + p_n$

假设 $\{p_n\}_{n=0}^{\infty}$ 是线性收敛的，其极限为 $p$
为了便于构造比 $\{p_n\}_{n=0}^{\infty}$ 收敛更快的序列 $\{\hat{p}_n\}_{n=0}^{\infty}$，我们假设 $p_n - p, p_{n+1} - p, p_{n+2} - p$ 的符号一致，又假设 $n$ 足够大，有 
$$ \frac{p_{n+1} - p}{p_n - p} \approx \frac{p_{n+2} - p}{p_{n+1} - p} $$ 从而 
$$ p_{n+1}^2 - 2p_{n+1}p + p^2 \approx p_{n+2}p_n - (p_n + p_{n+2})p + p^2 $$ 解出 $p$，得到 $$ p \approx \frac{p_{n+2}p_n - p_{n+1}^2}{p_{n+2} - 2p_{n+1} + p_n} \approx p_n - \frac{(p_{n+1} - p_n)^2}{p_{n+2} - 2p_{n+1} + p_n} $$ 于是，我们可以构造序列 $\{\hat{p}_n\}_{n=0}^{\infty}$，其中 $$ \hat{p}_n = \{\Delta^2\}(p_n)=p_n - \frac{(p_{n+1} - p_n)^2}{p_{n+2} - 2p_{n+1} + p_n} = p_n - \frac{(\Delta p_n)^2}{\Delta^2 p_n} $$
这样定义序列的方法就是AITKEN $\Delta^2$ 法
> [!Theorem]
> 假设序列 $\{p_n\}(n = 1,2,\ldots)$ 线性收敛到极限 $p$，且对于所有充分大的数 $n$，有 $(p_n - p)(p_{n+1} - p) > 0$。那么序列 $\{\hat{p}_n\}(n = 1,2,\ldots)$ 收敛到 $p$ 的速度快于 $\{p_n\}(n = 1,2,\ldots)$，即： $$ \lim_{n \to \infty} \frac{\hat{p}_n - p}{p_n - p} = 0 $$
> 构造按如下顺序：
> $$p_0,p_1=g(p_0),p_2=g(p_1),\hat{p_0}=\{\Delta^2\}(p_0),p_3=g(p_2),\hat{p_1}=\{\Delta^2\}(p_1),\dots$$

### 2. Steffensen's Method
- Steffensen's Method 在 Aitken's $\Delta^2$ 方法的基础上稍作修改，通过多轮迭代，可以得到用于加速**二次收敛**的技术。
给 $p=g(p)$ 寻找一个根的近似值 $p_0$，用这种方法构造出来的序列如下所示： 
$$ \begin{aligned} &p_0^{(0)},\;  p_1^{(0)} = g(p_0^{(0)}),\; p_2^{(0)} = g(p_1^{(0)}) \\ &p_0^{(1)} = \{\Delta^2\}(p_0^{(0)}),\;  p_1^{(1)} = \{\Delta^2\}(p_0^{(1)}),\; p_2^{(1)} = \{\Delta^2\}(p_1^{(1)}) \\ &p_0^{(2)} = \{\Delta^2\}(p_0^{(1)}),\;  \ldots \end{aligned} $$
> [!Code]
> - 输入：初始近似值 $p_0$ ​；容忍值 $TOL$；最大迭代次数 $N_{max}$ Nmax$​
> - 输出：近似解 $x$ 或失败信息
> ```c
> Step 1  Set i = 1;
> Step 2  while (i <= N_max) do steps 3-6
>         Step 3  Set p_1 = g(p_0);
>                     p_2 = g(p_1);
>                     p = p_0 - (p_1 - p_0)^2 / (p_2 - 2 * p_1 + p_0);
>         Step 4  if |p - p_0| < TOL then Output(p);  // successful
>             STOP;
>         Step 5  Set i++;
>         Step 6  Set p_0 = p;  // update p_0
> Step 7  Output(The method failed after N_max iterations);  // unsuccessful
> ```

