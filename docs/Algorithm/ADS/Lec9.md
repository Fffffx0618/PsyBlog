# Greedy Algorithms
## 9.1 Introduction
**优化问题**(optimization problem)：
- 给定一组**限制条件**(constraints)和**优化函数**(optimization function)，称满足限制条件的解为**可行解**(feasible solutions)。如果一个可行解在优化函数中取得最佳值，则称该解为**最优解**(optimal solution)。

**贪心法**(greedy method)：
- 根据预先设定的贪心标准，在每个阶段中作出最佳决策 
- 当前作出的决策不允许在后面改变，所以要确保作出的每个决策都是可行的
- 只有当“**局部最优 = 全局最优**”时，贪心算法才是可行的
- 贪心算法**不保证**得到最优解，但它能够产生与最优解相当接近的解，因此当直接找最优解耗时太长时，贪心算法可能更加适合。

**贪心算法的范式**：
- 优化问题 -> 做出一个选择后，剩下一个有待继续解决的子问题
- 需要证明：对于原问题，贪心选择总能保证得到**最优解**
- 证明问题具备**最优子结构**(optimal substructure)——做出贪心选择后，剩余的子问题具备这样的性质：子问题的最优解 + 做出的贪心选择 = 原问题的最优解
---

## 9.2 Examples
### 1. Activity Selection
> [!question]
> - 给定一组活动集 $S = \{a_1, a_2, \dots, a_n\}$，这些活动均在一个房间开展，活动 $a_i$ 的进行时间为 $[s_i, f_i)$
> - 如果 $a_i$ 和 $a_j$ 满足 $s_i \ge f_j$ 或 $s_j \ge f_i$（即两个活动的时间不重叠），称这两个活动是**兼容的**(compatible)
> - 为了解题方便，预先将这些活动根据结束时间的先后排好序，即保证 $f_1 \le f_2 \le \dots f_{n-1} \le f_n$
> 
> <div style="text-align: center"><img src="images/lec9/1.png" width="70%"></div>
> 
> 问题：请求出最大的、活动之间相互兼容的子集，即求在不发生冲突的前提下能安排的最多活动的方案

> [! hint] 答案
> 最优解为最多安排4个活动，但有多个最优解，如下所示（用红色或绿色标出的区间）：
> 
> <div style="text-align: center"><img src="images/lec9/2.png" width="70%"></div>
> ---
><div style="text-align: center"><img src="images/lec9/3.png" width="70%"></div>    

#### DP Algorithms
- 规定：$a_1\ a_2 \dots \underbrace{a_i \dots a_k \dots a_j}_{S_{ij}} \dots a_n$，注意 $a_i$ 和 $a_j$ 不在 $S_{ij}$ 内，即 $S_{ij}$ 是一个开区间
- 令$c_{ij}$为活动$a_i$和$a_j$之间最多的活动数，则得到状态转移方程        $$
        c_{ij} = \begin{cases}0 & \text{if}\ S_{ij} = \emptyset \\ \max\limits_{a_k \in S_{ij}} \{c_{ik} + c_{kj} + 1\} & \text{if}\ S_{ij} \ne \emptyset\end{cases}
        $$其中在$S_{ij} \ne \emptyset$的情况用到了分治算法的思想：根据中间的某个活动$a_k$，将整个区间分为左右两半，分而治之，最后再算上$a_k$（$+1$）
#### Greedy Algorithms
- 贪心策略（假设红色区间表示最优解）：
    - 策略1：挑选**最早开始**的活动
        - 反例：
            <div style="text-align: center">
                <img src="images/lec9/4.png" width="70%">
            </div>
            
	        先挑选最早开始且时间最长的区间，那么剩余的三个区间都无法选择，因此该策略不可行
    - 策略2：挑选**时间最短**的活动
        - 反例：
            <div style="text-align: center">
                <img src="images/lec9/5.png" width="60%">
            </div> 

            先挑选最短且和剩余两个区间都冲突的区间，这样的话剩余的两个相互不冲突区间就没得选了，因此该策略不可行
    - 策略3：挑选**冲突最少**的活动
        - 反例：
            <div style="text-align: center">
                <img src="images/lec9/6.png" width="65%">
            </div> 

            冲突最少的区间，如果选择它的话，与它冲突的两个区间就不能选了，这样最多只能选择3个区间，而不是最优解的4个区间，因此该策略不可行
    - 策略4：挑选**最早结束**的活动
        - 这种策略可以解决上面给出的所有反例
        - 接下来验证这种策略的正确性：
            - 贪心选择性质：考虑任意非空子问题 $S_k$，令 $a_m$ 为 $S_k$ 中最早结束的活动，那么 $a_m$ 一定被包含在 $S_k$ 中的**某些**满足活动相互兼容的最大子集中
>[!prove]
> - 令 $A_k$ 为最优解集，$a_{ef}$ 为 $A_k$ 中最早结束的活动
> - 如果 $a_m = a_{ef}$，那么定理成立；否则的话需要用 $a_m$ 替代 $a_{ef}$，得到 $A_k'$
> - 因为 $f_m \le f_{ef}$（由条件知），因此 $A_k'$ 是另一个最优解，得证。
> 
> 这种证明方法称为**交换参数法**：假设存在一个最优选择，其中的某些元素不在贪心选择中，此时可以通过交换贪心选择和最优选择的元素来构造一个不可能变差的解。
>> 另一种思路与此对称，即不断选取**最后开始的事件**

---
**最优子结构**：在活动选择问题中，用贪心策略选择 $a_k$ 之后得到子问题 $S_k$，那么 $a_k$ + 子问题 $S_k$ 的最优解一定可以得到原问题的一个最优解
- 实现步骤：
	- 选择首先结束的活动，递归解决剩余的活动子集
	- 由于这是一个尾递归，因此可以用迭代方法替代
	- 时间复杂度：$O(N \log N)$，解释如下：
		- 先将活动按照结束时间升序排序（$O(N \log N)$）
		- 然后遍历每个活动，按照贪心策略得到最优解（$O(N)$）
	- 对应地，也可以采取<u>“选择最晚开始的活动”</u>这一策略

- 得到正确的贪心算法后，修改DP的状态转移方程：$$
    c_{1, j} = \begin{cases}1 & \text{if}\ j = 1 \\ \max \{c_{1, j - 1}, c_{1, k(j)} + 1\} & \text{if}\ j > 1\end{cases}
    $$
	-  其中 $c_{1, j}$ 是 $a_1$ 到 $a_j$ 之间的最优解，$a_{k(j)}$ 是 $a_1$ 到 $a_j$ 之间最晚结束的，且与 $a_j$ 不冲突的活动，即 $1 \le k(j) \le j,\ f_{k(j)} \le s_j$
	- 此时只需要两层循环，因此时间复杂度为 $O(N^2)$

**加权活动选择问题**：现在考虑权重尽可能大的活动，此时一般的贪心算法会失效，但可以用动态规划来解决本问题，状态转移方程为：$$
    c_{1, j} = \begin{cases}w_j & \text{if}\ j = 1 \\ \max \{c_{1, j - 1}, c_{1, k(j)} + w_j\} & \text{if}\ j > 1\end{cases}
    $$---
### 2. Huffman Codes
> [!example]
> 假设给出一段长为1000个字符的字符串文本，仅包含字符a, u, x和z。因为一个字符占1字节空间，因此如果直接存储字符，就需要1000字节，即8000位的空间。
> - 如果预先进行编码：a = 00, u = 01, x = 10, z = 11，那么每个字符仅占2位空间，整个字符串的大小降为2000位（以及额外的一些空格）。不难得到：如果有 $C$ 个字符，那么每个字符的编码长度为 $\lfloor \log C \rfloor$ 位。
> 
> 更高效的编码方式——**根据字符出现的频率编码**
> - 假如给定字符串<span style="color: blue">aaa</span><span style="color: green">x</span><span style="color: red">u</span><span style="color: blue">a</span><span style="color: green">x</span><span style="color: purple">z</span>，那么频率为$f(a) = 4, f(u) = 1, f(x) = 2, f(z) = 1$
>   - 如果用前面那种定长字符编码，得到的结果为：<span style="color: blue">000000</span><span style="color: green">10</span><span style="color: red">01</span><span style="color: blue">00</span><span style="color: green">10</span><span style="color: purple">11</span>（长16位）
>   - 而用基于频率的编码方法（令a = 0, u = 110, x = 10, z = 111），得到的结果为：<span style="color: blue">000</span><span style="color: green">10</span><span style="color: red">110</span><span style="color: blue">0</span><span style="color: green">10</span><span style="color: purple">111</span>（长14位）
>   - 但如果遇到所有字符出现频率相等的情况，这种方法便起不到任何优化效果

> [! warning]    
> 想要无歧义地对每个字符进行译码，那么在为字符编码的时候需要保证：任意一个编码**不是**其他编码的**前缀**(prefix)。

通常用一棵二叉树(**字典树**(trie))来表示这些字符编码
- 对于字符 $C_i$，它的深度和频率分别为 $d_i$ 和 $f_i$，那么总的 cost 为 $\sum d_i f_i$
- 对于前一种原始的编码方式，得到的字典树如下所示：
    <div style="text-align: center">
        <img src="images/lec9/7.png" width="30%">
    </div>
    $\text{成本} = 2 * 4 + 2 * 1 + 2 * 2 + 2 * 1 = 16$ 

- 而对于后一种优化的编码方式，得到的字典树如下所示：
    <div style="text-align: center">
        <img src="images/lec9/8.png" width="30%">
    </div>  
    $\text{成本} = 1 * 4 + 3 * 1 + 2 * 2 + 3 * 1 = 14$

字典树的特征：**所有的字符位于叶子节点上**，这样可以避免“某个字符的编码是另一个字符的编码的前缀”的问题。像这样的树称为**满树**(full tree)，树上的01编码称为**前缀码**(prefix code)

第二种编码方式便是经典的**哈夫曼编码**(Huffman Codes)

具体步骤为：
- 初始化：将每个字符作为一个二叉树的节点，并将它们放在一个最小堆内
- 循环执行以下步骤（共 $\text{节点数 - 1}$ 次）
	- 从最小堆的根节点取出频率最小的节点，作为新树的左孩子
	- 再取出频率次小的节点，作为新树的右孩子
	- 这棵新树的根节点是两者频率之和，然后将新树重新插回最小堆内
时间复杂度：$T = O(C \log C)$

> [!example]
> 给定以下字符及其频率，请你得到对应的哈夫曼编码，并计算编码的总成本。
> <div style="text-align: center"><img src="images/lec9/9.png" width="70%"></div> 
> ---
> <div style="text-align: center"><img src="images/lec9/18.gif" width="70%"></div> 

**证明算法的正确性**：
- **贪心选择**：令 $C$ 为一张字母表，其中字符 $c \in C$ 的频率为 $c.freq$。令 $x, y$ 为 $C$ 内频率最小的两个字符，那么在 $C$ 中存在一个最优的前缀码，$x$ 和 $y$ 的编码具有相同的长度，且只有最低位不同。
    <div style="text-align: center">
        <img src="images/lec9/19.png" width="40%">
    </div>
    
> [!prove]
> 考虑 $x$ 和 $a$，有 $d_xc_x + d_ac_a-d_ac_x-d_xc_a= (d_a-d_x)(c_a-c_x)\geq0$，$y$ 和 $b$ 同理

- **最优子结构**：（与前一条引理一样的前提条件）令 $C'$ 为加入新字符 $z$ 并移除 $x$ 和 $y$ 后的字母表，满足 $z.freq = x.freq + y.freq$。令 $T'$ 为表示字母表 $C'$ 的最优前缀码的树，那么树 $T$ 可以通过移除树 $T'$ 的叶子节点 $z$，用 $x, y$ 以及一个内部节点构成的子树替代得到，它能够表示字母表 $C$ 的最优前缀码（可用归谬法证明）。

    <div style="text-align: center">
        <img src="images/lec9/20.png" width="40%">
    </div>

> [!prove]
> **假设**：存在一棵比 $T$ 更优的树 $T''$，它表示字母表 C 的最优前缀码，并且**不是**由 $T'$ 替换叶子 $z$ 得来的
> 1. 构造一个新的树 $T'''$：把 $T''$ 中的 $x$ 和 $y$ 所在的子树合并成一个新叶子 $z$，其频率为 $x.freq+y.freq$，得到一棵新的树 $T'''$，对应字母表 $C'$。
> 2. 所以有 $Cost(T''')=Cost(T'')−(x.freq+y.freq) \geq Cost(T')$
> 3. 结合上面两式可得：$Cost(T'')\geq Cost(T')+(x.freq+y.freq) = Cost(T)$
> 4. 这说明 $T''$ 不可能比 $T$ 更优，这与假设矛盾
