# AVL Trees, Splay Trees and Amortized Analysis
> [!caution]
> - 不论是 AVL树，还是 Splay 树，它们的原型还是**二叉查找树**，具备二叉查找树的所有性质。
## 1. AVL Trees
### 1.1 Definitions
[Definition]
- 空的二叉树是**height balanced** ($\text{height}= -1$)
- 如果树 $T$ 有左右子树 $T_L$ 和 $T_R$，那么满足下列条件的树 $T$ 才是**height balanced：
    - $T_L$ 和 $T_R$ 是**height balanced**
    - $|h_L - h_R| \le 1$，其中 $h_L$ 和 $h_R$ 分别是 $T_L$ 和 $T_R$ 的高度
[Definition]
- AVL树的每个节点都有一个**平衡因子**(==balance factor==)  
  - $BF(node) = h_L - h_R$。
  - 根据上面的定义知，它的取值仅有-1, 0或1。
[Definition]
AVL 树在每次插入或删除一个节点后会检查自身的平衡性，
- 如果没有被破坏，那么不做处理
- 如果被破坏（以插入操作为例）：
    - 找到离**插入节点**（==trouble maker==）**最近**的**异常节点** $tf$ (==trouble finder==)
    - 然后通过**旋转**(rotate) 的方法，将 $tf$ 旋转到合适的位置，使得原来以 $tf$ 为根节点的子树继续保持 AVL 树的性质（此时这棵子树不一定以 $tf$ 为根节点）
---
### 1.2 Rotations
> [!caution]
>  - 如果有多个 trouble finder，仅需要关注离 trouble maker 最近的节点，因为只要当以它为根节点的子树恢复为一棵 AVL 树，以它的祖先节点为根节点的树自然也变回 AVL 树。
>  - 在介绍 AVL 树的旋转操作时，主要对<u>插入操作</u>带来的平衡破坏展开讨论

旋转的操作与插入节点 (trouble maker) 的位置有关，分为两种：
- **单旋**(single rotation)
  - LL：插入的位置位于 trouble finder 的左孩子的左子树上
  - RR：插入的位置位于 trouble finder 的右孩子的右子树上
- **双旋**(double rotation)
  - LR：插入的位置位于 trouble finder 的左孩子的右子树上
  - RL：插入的位置位于 trouble finder 的右孩子的左子树上
#### LL & RR
> 旋转的是 **trouble finder** 和它的**儿子节点**
- 以 LL 为例

| **"初始状态"**                                                                                    | **"旋转"**                                                                                      | **"结果"**                                                                                       |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| <div style="text-align: center"><br><img src="images/lec1/1_light.png" width="90%"><br></div> | <div style="text-align: center"><br><img src="images/lec1/2_light.png" width="90%"><br></div> | <div style="text-align: center"><br><img src="images/lec1/3_light.png" width="100%"><br></div> |
PPT 给出的**左旋**示意图
<div style="text-align: center">
<img src="images/lec1/26.png" width="80%">
</div>
PPT 给出的**右旋**示意图
<div style="text-align: center">
<img src="images/lec1/4.png" width="80%">
</div>
一句话总结：==LL 用左旋，RR 用右旋==

#### LR & RL
> 双旋需要关注三个节点（**trouble finder**、trouble finder 的**儿子节点**和**孙子节点**），而单旋不需要关注孙子节点。下面将以 LR 为例介绍双旋的过程：

##### 过程演示

| **"初始状态"**                                                                                    | **"先「右旋」"**                                                                                   |                                                                                               |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| <div style="text-align: center"><br><img src="images/lec1/5_light.png" width="80%"><br></div> | <div style="text-align: center"><br><img src="images/lec1/6_light.png" width="80%"><br></div> |                                                                                               |
| Trouble maker 的具体位置并不重要                                                                       | 首先，通过右旋交换孙子节点（黄色）和它的父亲（橙色）的位置                                                                 |                                                                                               |
| **"中间结果"**                                                                                    | **"后「左旋」"**                                                                                   | **"最终结果"**                                                                                    |
| <div style="text-align: center"><br><img src="images/lec1/7_light.png" width="80%"><br></div> | <div style="text-align: center"><br><img src="images/lec1/8_light.png" width="80%"><br></div> | <div style="text-align: center"><br><img src="images/lec1/9_light.png" width="80%"><br></div> |
|                                                                                               | 然后，通过左旋交换黄色节点与 trouble maker（红色）的位置。                                                          |                                                                                               |

##### PPT 流程演示
**"来自 PPT 的 LR 过程"**
<div style="text-align: center">
<img src="images/lec1/10.png" width="70%">
</div>

**RL 的旋转方法与之类似，只要做一个镜像变换即可**
<div style="text-align: center">
<img src="images/lec1/11.png" width="70%">
</div>

> 时间复杂度：$O(\log N)$，其中 $N$ 为节点数，即与**树的高度**成正比
> （最坏情况是从叶子节点开始，一直调整到根节点）
#### 总结
- 记住两类旋转的具体步骤（**增加/删除边**和**变换节点的祖先-后代关系**），而不是所谓的左右旋转
- 在“旋转”前后，节点的**水平相对位置**并没有发生改变，变的只是它们的**竖直方向**上的相对位置（保证树始终是一棵二叉搜索树）
#### 关于删除
- 先按照 BST 的方法进行删除
- 若子树的高度发生变化， AVL 树的平衡被破坏，则要旋转调整（可能旋转多次）
- 时间复杂度：$O(\log{N})$
---
### 1.3 The height of AVL Trees
一棵高为$h$时节点数最小的平衡树的形状如下所示： 

<div style="text-align: center">
    <img src="images/lec1/14.png" width="40%">
</div>

由定义易得关于 AVL 的最小节点数 $n_h$ 和树高 $h$ 相关的递推关系式（类似斐波那契数列）：
    $$
    n_h = \begin{cases}n_{h - 1} + n_{h - 2} + 1 & \mathrm{if}\ h > 1\\ 2 & \mathrm{if}\ h = 1\\ 1 & \mathrm{if}\ h = 0\end{cases}
    $$

事实上，$n_h = F_{h + 3} - 1(h \ge -1, F_0 = 0, F_1 = 1)$。而斐波那契数 $F_h \approx \dfrac{1}{\sqrt{5}}(\dfrac{1 + \sqrt{5}}{2})^i$，所以：
$$
n_h  \approx \dfrac{1}{\sqrt{5}}(\dfrac{1 + \sqrt{5}}{2})^{h+3} - 1    
$$
因而高度 $h = O(\log n)$

---
## 2. Splay Trees
AVL树虽然能始终保持平衡，但需要维护每个节点的高度/平衡因子，而Splay 树（伸展树）更加简洁:
- 不维护节点的高度/平衡因子字段(无法保障树的平衡)
- **核心操作**：访问某个节点时，将该节点通过**旋转**将其调到**根节点**的位置上
- 能够保证 $M$ 次操作（增删查改）的**摊还(amortized)复杂度**为 $O(M \log N)$
---
### 2.1 Rotation
#### Wrong solution
单纯的左旋或右旋**无法降低**下面这棵树的复杂度
- 某些节点复杂度降低，但另外一些节点的复杂度增加了
<div style="text-align: center">
<img src="images/lec1/15.gif" width="60%">
</div>
如果按升序插入节点之后（树退化成链表）再按升序访问每个节点，时间复杂度为$O(N)$
        <div style="text-align: center">
        <img src="images/lec1/16.gif" width="60%">
        </div>  
#### Right solution
分为3种情况（其中被访问的非根节点记作 $X$，它的父亲和祖父分别记作 $P$ 和 $G$）
- Case 1：$P$ 是根节点 -> 旋转 $X$ 和 $P$ 即可（AVL树的单旋）
- Case 2：$P$ 是非根节点
    - Case 2-1：==Zig-zag==（$X, P, G$ 不在一条直线）-> $X$ 节点转两次
    - 相当于 *LR 和 RL*，*从下往上*旋转
    <div style="text-align: center">
    <img src="images/lec1/17.png" width="70%">
    </div> 

    - Case 2-2：==Zig-zig==（$X, P, G$ 三者在一条直线上）-> 先转 $P$ 节点，后转 $X$ 节点
    - 相当于*从上往下*旋转
    <div style="text-align: center">
    <img src="images/lec1/18.png" width="70%">
    </div>
    
**Case 2-2 过程演示**

| 初始状态                                                                                                           | 中间结果                                                                                                           | 最终结果                                                                                                           |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| <figure style=" width: 70%" markdown="span"><br>            ![](images/lec1/19_light.png)<br>        </figure> | <figure style=" width: 80%" markdown="span"><br>            ![](images/lec1/21_light.png)<br>        </figure> | <figure style=" width: 80%" markdown="span"><br>            ![](images/lec1/23_light.png)<br>        </figure> |
#### Application
> [!caution]
>  - 在调整的过程中不要和 AVL 树搞混：AVL 树通过检测**树高或平衡因子**来决定是否要继续旋转；而 Splay 树是要旋转**被访问的节点**，直到它位于根节点为止
>  - 在节点数足够多的理想情况下，把被访问的节点移到根节点上之后，路径上大多数节点的高度降至原来的**一半**左右

<div style="text-align: center">
        <img src="images/lec1/24.png" width="60%">
</div> 

---
### 2.2 Operations
#### Insertion
1. $\text{Insert} X$
2. $\text{Find}X$
#### Deletion
1. Find $X$
2. Remove $X$
3. $\text{FindMax}(T_L)$ 或者 $\text{FindMin}(T_R)$
4. Make $T_R$ the right child of the root of $T_L$ or Make $T_L$ the left child of the root of $T_R$
---
## 3. Amortized Analysis
==「amortized 摊还」==：
- 保证在 $N$ 个数据上的 $M$ 次连续操作的总体复杂度最多为 $O(M \log N)$
- 考虑全局耗时，允许某些运算耗时久一些，可用在另一些数据上耗时较短的运算来弥补损失
- 区分**最坏复杂度**，**摊还复杂度**和**平均复杂度**
    - **最坏**：保证单个运算以及整体运算的复杂度不超过某一边界（考虑最极端的情况）
    - **摊还**：保证<u>整体的运算复杂度</u>不超过某一边界，但允许某几次运算超过边界（考虑真实情况）
    - **平均**：在给定**数据分布平均**的情况下（理想假设），保证整体运算的复杂度不超过某一边界
<div style="text-align: center" markdown="1">
$$\text{worst-case bound} \ge \text{amortized-case bound} \ge \text{average-case bound}$$
> 注：只有平均复杂度考虑数据分布，前两者并不考虑数据的分布。

常见的摊还分析方法有：
- **聚合法**(aggregate method)
- **核算法**(accounting method)
- **势能法**(potential method)
---
### 3.1 Aggregate Method
> [!idea]
> 摊还复杂度 = 所有操作的总时间 / 操作次数，即 $T_{amortized} = \dfrac{\sum\limits^nT_i}{n}$

**Example**
Stack with `MultiPop(int k, Stack S)`：依次弹出栈内 $\min\{\text{sizeof}(S),k\}$ 个元素
``` c
Algorithm {
    while (!isEmpty(S) && k > 0) {
        Pop(S);
        k--;
    }
}
```
 易知 $\text{size}(S) \le n$（$n$ 为数据总数），所以摊还复杂度 $T_{amortized} = \dfrac{O(n)}{n} = O(1)$ 
 
---
### 3.2 Accounting Method
> [!idea]
> 当我们的 **amortized cost** $\hat{c}_i$ 高于 **Actual cost** $c_i$ 时，多余部分转化为**credit**。如果之后的摊还成本小于实际成本时，可以用之前攒的积分抵消实际的成本
> > 注意：必须满足 $\sum\limits^n\hat{c}_i \ge \sum\limits^nc_i$，公式为：$T_{amortized} = \dfrac{\sum\limits^n\hat{c}_i}{n}$

#### Example
接着 MultiPop 的例子
- $c_i$ for `Push`：$1$，`Pop`：$1$，`MultiPop`：$\min(\text{sizeof}(S), k)$
- $\hat{c}_i$ for `Push`：$2$，`Pop`：$0$，`MultiPop`：$0$
Credits
- $\text{credits}$ for `Push`：$+1$，`Pop`：$-1$，`MultiPop`：$\min(\text{sizeof}(S), k)$
因此
$$
    \text{sizeof}(S) \ge 0 \Rightarrow Credits \ge 0 \Rightarrow O(n) = \sum\limits^n\hat{c}_i \ge \sum\limits^n\hat{c}_i \Rightarrow T_{amortized} = \dfrac{O(n)}{n} = O(1)
    $$
---
### 3.3 Potential Method
> [!idea]
> 将 Accounting Method 中的「credit」转化为「势能差」，即 $\hat{c}_i - c_i = \Phi(D_i) - \Phi(D_{i-1})$，其中 $D_i$ 表示经历了 i 次运算后的数据结构，$\Phi(D_i)$ 表示该数据结构的**势能函数**(potential function)。经过一些转化，可以得到：
>  $$\begin{align}\sum\limits_{i = 1}^n\hat{c}_i= & \sum\limits_{i=1}^n(c_i + \Phi(D_i) - \Phi(D_{i-1})) \notag \\= & (\sum\limits_{i=1}^nc_i) + \Phi(D_n) - \Phi(D_0) \notag\end{align}$$
>  因此只需考虑始末势能之差，确保它们的势能差 $\Phi(D_n) - \Phi(D_0) \ge 0$ 即可（通常会令 $\Phi(D_0) = 0$），关键在于设计一个合理的势能函数。

**Example**
还是接着 MultiPop 的例子，
假定 $D_i$ 为经过 $i$ 次操作后的栈，$\Phi(D_i)$ 表示栈的元素个数，易知 $\Phi(D_i) \ge 0 = \Phi(D_0)$
- `Push`：$\Phi(D_i) - \Phi(D_{i-1}) = (sizeof(S) + 1) - sizeof(S) = 1$
        $\Rightarrow \hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1}) = 1 + 1 = 2$
        
- `Pop`：$\Phi(D_i) - \Phi(D_{i-1}) = (sizeof(S) - 1) - sizeof(S) = -1$
        $\Rightarrow \hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1}) = 1 - 1 = 0$
        
- `MultiPop`：$\Phi(D_i) - \Phi(D_{i-1}) = (sizeof(S) - k') - sizeof(S) = -k'$
        $\Rightarrow \hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1}) = k' - k' = 0$
    $$\therefore \sum\limits_{i = 1}^n\hat{c}_i = \sum\limits_{i = 1}^nO(1) = O(n) \ge \sum\limits_{i=1}^nc_i \Rightarrow T_{amortized} = \dfrac{O(n)}{n} = 1$$
---
### 3.4 Analysis for Splay Tree
> 结论：Splay 树的摊还复杂度为 $T_{amortized} = O(\log N)$

下面我们用**势能法**来进行势能分析。
#### Analysis
假定：
- $D_i$ = 以被访问的节点为根节点（经过变换后）的新树
- $c_i$ = 转换过程中所需的实际成本
    - zig：$c_i = 1$
    - zig-zag & zig-zig：$c_i = 2$
- $\Phi(T) = \sum\limits_{i \in T} \log S(i) = \sum\limits_{i \in T} R(i)$
	- 其中 $i$ 是 $T$ 的后代，$S(i)$ 是以 $i$ 为根节点的子树的节点数
    - 取 $S (i)$ 对数就是 $i$ 的**秩(rank)** $R(i)$,  $R(i) \approx H(i)$（$H(i)$ 为树的高度）

下面我们就具体分析 Splay 树的三种情况（记$R_k(X)$为第$k$次操作后节点$X$的秩）：
##### 1. zig
<img src="images/lec1/25.png" width="70%"/>

- 显然，在旋转前后，以 $P$ 为根节点的子树的大小变小了，因此 $R_{k+1}(P) - R_k(P) < 0$
$$\begin{align}\hat{c}_i = & 1 + (R_{k+1}(X) - R_k(X)) + (R_{k+1}(P) - R_k(P)) \notag \\ \le & 1 + R_{k+1}(X) - R_k(X) \notag\end{align}
$$
##### 2. zig-zag
**引理**
如果 $a + b \le c$，且$a, b$都是正整数，则$\log a + \log b \le 2 \log c - 2$
    <div style="text-align: center">
        <img src="images/lec1/17.png" width="70%"/>
- 旋转前 $G$ 的大小和旋转后 $X$ 的大小相等，所以 $R_{k+1}(X) = R_{k}(G)$
- 旋转后，$S(X) \ge S(P) + S(G)$，根据引理知，$\log S(P) + \log S(G) \le 2 \log S(X) - 2$，即 $R_{k+1}(P) + R_{k+1}(G)\le 2 R_{k+1}(X) - 2$
- 旋转前，$P$ 是 $X$ 的父节点，因此 $R_k(P) \ge R_k(X)$
- 通过上述的转换和抵消，可以得到最终的不等式$$
        \begin{align}
        \hat{c}_i = & 2 + (R_{k+1}(X) - R_k(X)) + (R_{k+1}(P) - R_k(P)) + (R_{k+1}(G) - R_k(G))\notag \\
        = & (2 +R_{k+1}(P) + R_{k+1}(G))+ (R_{k+1}(X) - R_{k}(G))-(R_k(X) + R_k(P))
        \\
        \le & 2(R_{k+1}(X) - R_k(X)) \notag
        \end{align}$$
##### 3. zig-zig
  <img src="images/lec1/18.png" width="70%"/>
- 旋转后的 $X$ 的大小 = 旋转前的 $G$ 的大小，所以 $R_{k+1}(X) = R_k(G)$
- 观察旋转前的 X 子树和旋转后的 G 子树，不难发现它们加起来的大小 $\le$ 旋转后的 X 树的大小，所以用上面的引理，可得 $R_{k+1}(G) + R_k(X) \le 2R_{k+1}(X) - 2$
- 由图可知 $R_{k+1}(P) \le R_{k+1}(X), R_k(P) \ge R_k(X)$
-  最终我们得到了正确的不等式
$$
        \begin{align}
        \hat{c}_i & = 2 + (R_{k+1}(X) - R_k (X)) + (R_{k+1}(P) - R_k (P)) + (R_{k+1}(G) - R_k (G))\notag \\
        & = 2 + (R_{k+1}(X) - R_k (G)) + (R_{k+1}(G) + R_k (X)) + R_{k+1}(P) - 2 R_k (X) - R_k (P) \notag \\
        & \le 2 R_{k+1}(X) + R_{k+1}(X) - 2 R_k (X) - R_k (X)\notag \\
        & \le 3 (R_{k+1}(X) - R_k (X)) \notag
        \end{align}
$$
##### 4. Sum
将这三部分并起来，得到最终的摊还成本。但在此之前，我们需要进一步的放缩，便于后续计算：
$$
    \begin{align}
    \hat{c}_{zig} & \le 1 + 3(R_{k+1}(X) - R_k(X)) \notag \\
    \hat{c}_{zig-zag} & \le 2(R_{k+1}(X) - R_k(X)) \le 3(R_{k+1}(X) - R_k(X)) \notag \\
    \hat{c}_{zig-zig} & \le 3(R_{k+1}(X) - R_k(X)) \notag
    \end{align}
    $$
在最终计算之前，还得先确定这3种操作的总次数$k$，不难得到：$$k = \begin{cases}\dfrac{H(X)}{2} & H(X) \text{ is even} \\ \dfrac{H(X) - 1}{2} + 1 & H(X) \text{ is odd}\end{cases}$$
- 当 $k$ 为偶数时，每次操作要么是zig-zig，要么是zig-zag
- 当 $k$ 为奇数时，前 $k-1$ 次操作是zig-zig或zig-zag，最后一次操作是zig
    将所有旋转操作对应的摊还成本加起来：
$$
    \begin{align}
    \sum\limits_{i=1}^{k+1}\widehat{c_i} & = \hat{c}_{zig} + \sum \hat{c}_{zig-zag} + \sum \hat{c}_{zig-zig} \notag \\
    & = 1 + 3(R_{k+1}(X) - R_k(X)) + \sum\limits_{i=1}^k3(R_i(X) - R_{i-1}(X)) \notag \\
    & = O(1) + 3(R_{k+1}(X) - R_0(X)) \notag \\
    & = O(\log N) \notag
    \end{align}
    $$
    这样，我们成功证明了 Splay 树的摊还复杂度。



