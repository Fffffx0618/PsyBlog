# Chapter 1. Mathematical Preliminaries
## 1.2 Roundoff Errors and Computer Arithmetic
**Discussion**: Approximate $\int_0^1 e^{-x^2} dx$.
使用泰勒展开式表示 $e^{-x^2}$，因此：
$$
\begin{align}
\int_0^1 e^{-x^2} dx & = \int_0^1 (1 - x^2 + \dfrac{x^4}{2!} - \dfrac{x^6}{3!} + \dfrac{x^8}{4!} - \dots) dx \notag \\
& = \underbrace{1 - \dfrac{1}{3} + \dfrac{1}{2!} \times \dfrac{1}{5} - \dfrac{1}{3!} \times \dfrac{1}{7}}_{S_4} + \underbrace{\dfrac{1}{4!} \times \dfrac{1}{9} - \dots}_{R_4/*Remainer*/} \notag
\end{align}
$$
    $|R_4| = |\dfrac{1}{4!} \times \dfrac{1}{9} - \dfrac{1}{5!} \times \dfrac{1}{11} + \dots| < \dfrac{1}{4!} \times \dfrac{1}{9} < 0.005$，所以误差 < 0.005.
综上：
- 舍入误差 < 0.0005 * 2 = 0.001
- 截断误差 < 0.005
- |总误差| < 0.006
---
### 1.2.1 Truncation Error and Roundoff Error
- **Truncation Error 截断误差**: 使用截断的(或者说有限的)求和来近似无穷级数的和产生的误差
	- 理论：$e = \sum_{n=0}^\infty \dfrac{1}{n!}$
	- 计算机: $e = \sum_{n=0}^N \dfrac{1}{n!}$
- **Roundoff Error 舍入误差**: 计算机执行实数计算时产生的误差。这是因为计算机中的算术运算涉及到的数字只有==有限位数==
	- 理论：$0.33333\dots$
	- 计算机: $0.33333$
---
### 1.2.2 Chopping and Rounding
> 使用舍入法或截断法产生的误差都叫做**舍入误差**
- Chopping: $0.1119 \rightarrow 0.111$，直接截断
- Rounding: $0.1119 \rightarrow 0.112$，四舍五入

**Normalized decimal floating-point form of a real number**
$$
\pm0.d_1d_2\dots d_k \times 10^n,\text{where }1\le d_1 \le9 \text{ and } 0\le d_i \le 9(i=2,\dots,k)
$$
函数表示：
$$
fl(y) = \begin{cases}0.d_1 d_2 \dots d_k \times 10^n & \text{/*Chopping*/} \\ chop(y + 5 \times 10^{n - (k+1)}) = 0.\delta_1 \delta_2 \dots \delta_k \times 10^n & \text{/*Rounding*/}\end{cases}
$$
---
### 1.2.3 Absolute error and relative error
Denote $p^{*}$ as the approximation of $p$.
- ==Absolute error 绝对误差==: $|p^*-p|$
- ==Relative error 相对误差==: $|\dfrac{p^*-p}{p}|$
如果 $t$ 是满足下面关系的最大非负整数，那么称 $p^*$ 是 $p$ 保留至 $t$ 位**有效数字**(significant digits) 的近似形式
$$
\dfrac{|p - p^*|}{p} < 5 \times 10^{-t}
$$
- **截断**(chopping)
    - $k-1$ 位有效数字 
$$
\begin{align}
\Big|\dfrac{p - p^*}{p}\Big| & = \Big| \dfrac{0.d_1 d_2 \dots d_k d_{k+1} \dots \times 10^n - 0.d_1 d_2 \dots d_k \times 10^n}{0.d_1 d_2 \dots d_k d_{k+1} \dots \times 10^n} \Big| \notag \\
& = \Big|\dfrac{0.d_{k+1} d_{k+2} \dots}{0.d_1 d_2 \dots}\Big| \times 10^{-k} \le \dfrac{1}{0.1} \times 10^{-k} = 10^{-k+1} \notag
\end{align}
$$
- **舍入**(rounding)
    - $k$ 位有效数字 
$$
\Big|\dfrac{p - p^*}{p}\Big| \le \dfrac{0.5}{0.1} \times 10^{-k} = 0.5 \times 10^{-k+1}
$$
---
**舍入误差**对计算结果的影响：

**两个近乎相等的数字相减，会导致有效位数的抵消**
-  $a_1 = 0.1234\textcolor{red}{5}, a_2 = 0.1234\textcolor{red}{6}$  都有 5 位有效数字，但是 $a_2 - a_1 = 0.0000\textcolor{red}{1}$ 只有 1 位有效数字。

**用一个很小的数去除（或用很大的数去乘）另一个数，会导致误差的扩大**
- 取 $p$ 和 $q$，令 $a = \dfrac{p}{q}$，其近似结果为 $a^* = \dfrac{p + \varepsilon_p}{q + \varepsilon_q}$。那么：
   - 绝对误差 $e_{\text{abs}} = |a^* - a|$
   - 相对误差 $e_{\text{rel}} = \dfrac{e_{\text{abs}}}{a}$
把 $e_{\text{abs}}$ 看作是 $q$ 关于 $\dfrac{p}{q}$ 的函数，对它求导，我们就能观察绝对误差的变化率。所以：
$$
e_{\text{abs}}'(q)  = \dfrac{d\frac{p}{q}}{dq} \notag = -\dfrac{p}{q^2} \notag
$$ 如果 $q$ 足够小，它的微小变化会使绝对误差产生很大的变化

---
启示：在让计算机计算数学公式前，要先对公式化简，以降低对精度的影响。

> [!example]
> Evaluate $f(x) = x^3 - 6.1x^2 + 3.2x + 1.5$ at $x = 4.71$ using 3-digit arithmetic(3位有效数字)
> ![[image.png]]
> - Exact value: $f(4.71) = 104.487111 - 135.32301 + 15.072 + 1.5 = -14.263899$ 
> - Chopping: $f(4.71) = 104 - 134 + 15.0 + 1.5 = -13.5$ 
>     - Relative error: $\dfrac{|-14.263899 + 13.5|}{|-14.263899|} \approx 5.35\%$ 
> - Rounding: $f(4.71) = 105 - 135 + 15.1 + 1.5 = -13.4$ 
>     - Relative error: $\dfrac{|-14.263899 + 13.4|}{|-14.263899|} \approx 6.06\%$ 
> 可见，有时候舍入误差比截断误差更大。
> 
> 下面介绍一种使近似结果更为精确的方法——[秦九韶算法]（又称 Horner's Method），它可以将多项式转化为：
> $$
>         \begin{align}
>         & a_0 + a_1 x + a_2 x^2 + a_3 x^3 + \dots + a_n x^n \notag \\
>         = & a_0 + x(a_1 + x(a_2 + x(a_3 + \dots + x(a_{n-1} + xa_n) \dots ))) \notag
>         \end{align}
>         $$
> 利用这一公式，我们可以将原函数转换为：
> $$
> f(x) = x^3 - 6.1x^2 + 3.2x + 1.5 = ((x - 6.1)x + 3.2)x + 1.5
> $$
> **Chopping**: 
> $$\begin{aligned} &((4.71 - 6.1)4.71 + 3.2)4.71 + 1.5 \\ = &(-1.39 * 4.71 + 3.2)4.71 + 1.5 \\ = &(-6.54 + 3.2)4.71 + 1.5 \\ = &-3.34 * 4.71 + 1.5 \\ = &-15.7 + 1.5 \\ = &-14.2 \end{aligned} $$
> - Relative error: $\dfrac{|-14.263899 + 14.2|}{|-14.263899|} \approx 0.44\%$ 
> **Rounding**: 
> $$\begin{aligned} &((4.71 - 6.1)4.71 + 3.2)4.71 + 1.5 \\ = &(-1.39 * 4.71 + 3.2)4.71 + 1.5 \\ =& (-6.55 + 3.2)4.71 + 1.5 \\ =& -3.35 * 4.71 + 1.5 \\ =& -15.8 + 1.5 \\ =& -14.3 \end{aligned} $$
> - Relative error: $\dfrac{|-14.263899 + 14.3|}{|-14.263899|} \approx 0.25\%$ 
> 可见，此时误差明显减小了。

---
## 1.3 Algorithms and Convergence
### 1.3.1 Stability
若算法满足：对初始数据的微小改动对最终结果的影响不大，那么称这样的算法是**稳定的**(stable)，否则就是**不稳定的**(unstable)。如果算法仅对某些特定的初始数据改动是稳定的，那么称这种算法是**条件稳定的**(conditionally stable)。
### 1.3.2 The growth of errors
假设 $E_0 > 0$ 是初始误差(initial error)，$E_n$ 是 $n$ 步操作后的误差
- 如果 $E_n \approx CnE_0$，则称为==线性增长(linear growth)==
    线性增长的误差通常是**无法避免**的，当 $C$ 和 $E_0$ 都很小的时候，结果通常**可以接受**
- 如果 $E_n \approx C^nE_0$，则称为==指数增长(exponential growth)==
    指数增长的误差**应该避免**，因为即使 $E_0$ 很小，$C^n$ 也会变得很大。这会导致**不可接受**的不准确性
> [!examples]
> 计算 $I_n = \dfrac{1}{e} \int_0^1 x^n e^x dx, n = 0, 1, 2, \dots$
> #### Method 1
> 通过分部积分，可得：$I_n = 1 - nI_{n-1}$
> - $I_0 = \dfrac{1}{e} \int_0^1 e^x dx = 1 - \dfrac{1}{e} \approx 0.63212056 = I_0^*$，对应的绝对误差 $|E_0| = |I_0 - I_0^*| < 0.5 \times 10^{-8}$
> - 由 $\dfrac{1}{e} \int_0^1 x^n e^0 dx < I_n < \dfrac{1}{e} \int_0^1 x^n e^1 dx$ 可得 $\dfrac{1}{e(n+1)} \le I_n \le \dfrac{1}{n+1}$
> 
> 然而，借助第 1 步的等式和第 2 步的近似结果，继续计算后面的结果，发现：
> $$
> \begin{align} I_{1}^{*} &= 1 - 1 \cdot I_{0}^{*} = 0.36787944 \\ \ldots &\ldots \ldots \\ I_{10}^{*} &= 1 - 10 \cdot I_{9}^{*} = 0.08812800 \\ I_{11}^{*} &= 1 - 11 \cdot I_{10}^{*} = 0.03059200 \\ I_{12}^{*} &= 1 - 12 \cdot I_{11}^{*} = 0.63289600 \quad ? \\ I_{13}^{*} &= 1 - 13 \cdot I_{12}^{*} = -7.2276480 \quad ?? \\ I_{14}^{*} &= 1 - 14 \cdot I_{13}^{*} = 94.959424 \quad ?! \\ I_{15}^{*} &= 1 - 15 \cdot I_{14}^{*} = -1423.3914 \quad !! \end{align}
> $$
> 误差越来越大，明显超出第 3 步得到的不等式范围
> 
> > 出现上述情况的原因？
> > 绝对误差 $|E_n| = |I_n - I_n^*| = |(1 - nI_{n-1}) - (1 - nI_{n-1}^*)| = n|E_{n-1}| = \dots = n!|E_0|$
> > 误差以**阶乘速度**增长的，比指数级别的增长还要快得多
> 
> #### Method 2
> 在法1基础上，将等式 $I_n = 1 - nI_{n-1}$ 转换为等价形式 $I_{n-1} = \dfrac{1}{n} (1 - I_n)$
> - 根据法1得到的不等式，取中间值作为 $I_n$ 的近似值，即令 $I_n^* = \dfrac{1}{2} \Big[\dfrac{1}{e(N+1)} + \dfrac{1}{N+1}\Big] \approx I_n$
>     - 此时的绝对误差：$|E_n| = |I_n - I_n^*| \rightarrow 0\text{ as } n \rightarrow +\infty$
>     - 现在得到的计算结果如下所示：
> $$
> \begin{align*} \text{Take } I_{15}^{*} &= \frac{1}{2}\left[\frac{1}{e \cdot 16} + \frac{1}{16}\right] \approx 0.042746233 \\ &\Rightarrow I_{14}^{*} = \frac{1}{15}(1 - I_{15}^{*}) \approx 0.063816918 \\ I_{13}^{*} &= \frac{1}{14}(1 - I_{14}^{*}) \approx 0.066870220 \\ I_{12}^{*} &= \frac{1}{13}(1 - I_{13}^{*}) \approx 0.071779214 \\ I_{11}^{*} &= \frac{1}{12}(1 - I_{12}^{*}) \approx 0.077351732 \\ I_{10}^{*} &= \frac{1}{11}(1 - I_{11}^{*}) \approx 0.083877115 \\ &\ldots \ldots \ldots \ldots \\ I_{1}^{*} &= \frac{1}{2}(1 - I_{2}^{*}) \approx 0.36787944 \\ I_{0}^{*} &= \frac{1}{1}(1 - I_{1}^{*}) \approx 0.63212056 \end{align*}
> $$
>     可以看到，计算结果的误差变得很小了，到达可以被接受的程度
>     
> 这种转换之所以可行，是因为 $|E_{n-1}| = \Big| \dfrac{1}{n} (1 - I_n) - \dfrac{1}{n} (1 - I_n^*) \Big| = \dfrac{1}{n}|E_n|$，从而 $|E_n| = \dfrac{1}{N(N-1)\dots(n+1)} |E_N|$，也就是说即使当 $n$ 变得很大，误差还是很小，是稳定的误差

---
### 1.3.3 Convergence rate
- 使用 $O$ 符号来表示==收敛速度==
假设 $\lim_{h \to 0} F(h) = L$，$\lim_{h \to 0} G(h) = 0$。如果存在正常数 $K$ 使得
$$
|F(h) - L| \leq K|G(h)|
$$
对于足够小的 $h$ 成立，则记为 $F(h) = L + O(G(h))$
- 我们通常取 $G(h) = h^p, (p > 0)$，并对**最大的 $p$ 值**感兴趣
**Example**
$F(h)=\dfrac{\sin h}{h}, \lim_{h\rightarrow 0}\frac{\sin h}{h} = 1$
- 解: $F(h) - L = \frac{\sin h}{h} - 1 = \frac{\sin h - h}{h} \sim \frac{h - \frac{h^3}{6} + o(h^3) - h}{h} \sim -\frac{h^2}{6} \leq K|h^2|$
- 所以收敛速度为 $O(h^2)$
---
## 1.4 IEEE 754 Floating Point Representation
![[image-8.png]]
$$
x = (-1)^s \times (1+\text{Fraction}) \times 2^{\text{Exponent-Bias}}
$$
- $S$ (1 bit)代表==符号位(sign bit)==, $0$ 为表示非负数, $1$ 为表示负数
- 有效位数($\text{Significand}=1+\text{Fraction}$)中 $1$ 是默认的，只存储小数点后面的位数(即Fraction)
-  **Fraction** 代表==尾数==部分(也称作**mantissa**)
    - Single: 23 bits
    - Double: 52 bits
-  **Exponent** 表示==指数==部分(也称作**characteristic**)
    - Single: 8 bits
    - Double: 11 bits
    - **excess representation**(偏移表示法)$= \text{actual exponent} -\text{bias}$，其中：
        - Single:  bias = 127 bits
        - Double:  bias = 1023 bits
        - $\text{Exponent}=\text{实际的指数}+\text{bias}$
    - 指数为全 $0$ 和全 $1$ 时用作**特殊值**处理
        - 全 $0$：零或非规约数（Subnormal/Denormalized）
        - 全 $1$：无穷大或 $\text{NaN}$（Not a Number）

**Example**

| Value                       | Type   | S   | Exponent | Fraction                |
| --------------------------- | ------ | --- | -------- | ----------------------- |
| $5.0= 1.01_2\times 2^2$     | Single | 0   | 10000001 | 01000000000000000000000 |
| $-0.75=-1.1_2\times 2^{-2}$ | Single | 1   | 01111110 | 10000000000000000000000 |

