# Backtracking
## 6.1 Introduction
回溯法的大致思路：
- 假设已经得到部分解$(x_1, \dots, x_i)$，其中$x_k \in S_k, 1 \le k \le i < n$
- 首先将一种可能情况为$x_{i+1} \in S_{i+1}$加到这个部分解中，并检查新的部分解$(x_1, \dots, x_i, x_{i+1})$是否满足限制条件
- 如果满足条件，继续添加下一种情况到部分解中（重复上一步）
- 但如果$S_{i+1}$中没有满足要求的选择，那么表示沿$x_i$往下走是走不通的，那么就删掉$x_i$，并且**回溯**到上一个部分解$(x_1, \dots, x_{i-1})$，然后从$S_i$中挑选另外的可能情况$x_i'$，以此类推

### Template
```cpp
bool Backtracking (int i) {
	Found = false;
    if (i > N)
    	return true;  // solved with (x1, ..., xN)
    for (each xi in Si) {
        // check if satisfies the restriction R
    	OK = Check((x1, ..., xi), R);  // pruning
        if (OK) {
        	Count xi in;
            Found = Backtracking(i + 1);
            if (!Found)
	            Undo(i);  // recover to (x1, ..., x{i-1})
        }
        if (Found) break; 
    }
    return Found;
 }
```

---
## 6.2 Examples

### 1. Eight Queens
#### Description
将8个皇后放在$8 \times 8$的棋盘上，保证任何两个皇后之间不会相互攻击。其中皇后的攻击条件为：两个皇后位于同一行、同一列或同一对角线上。

 > [! info] 可行解
 > <div style="text-align: center"><img src="images/lec6/1.png" width="80%"></div>

用数学化的语言描述问题：
- 令$Q_i$为棋盘上第$i$行的皇后，$x_i$为$Q_i$的列索引，$S_i$为$x_i$可取值的集合
- 限制条件为：
    - $S_i = \{1, 2, 3, 4, 5, 6, 7, 8\}$，其中$1 \le i \le 8$
        - 一共有$8^8$种可能解
    - 当$i \ne j$时，$x_i \ne x_j$
        - 每个解是$1, 2, \dots, 8$的排列，所以可能解的个数降到$8!$个
    - $\dfrac{x_i - x_j}{i - j} \ne \pm 1$
        - 用于确保“不在同一对角线”的限制条件
#### Method
1. 构建一棵**博弈树**(game tree)

    <div style="text-align: center">
        <img src="images/lec6/2.png" width="80%">
    </div>

    - 每一条从根节点到叶子节点的路径即为一种可能的解
    - 节点内的数字表示搜索的顺序(post-order-traversal)，深度为 $i$ 的节点表示第 $i$ 行上的皇后
2. 通过执行**深度优先搜索**(depth-first search)（后序遍历）来检验每一条可能的路径

### 2. Turnpike Reconstruction
#### Description
> [!question] 问题描述
> 给定 $N$ 个在x轴上的点，它们的坐标满足 $x_1 < x_2 < \dots x_N$，并假设 $x_1 = 0$。在所有点中任取两点，一共有 $\dfrac{N(N-1)}{2}$ 种取法，对应有 $\dfrac{N(N-1)}{2}$ 不同的路径。
> **问题**：给定$\dfrac{N(N-1)}{2}$条路径，如何重新构造(reconstruct)一个点集？

#### Method
> [! example] 
> 根据距离集 $D = \{1, 2, 2, 2, 3, 3, 3, 4, 5, 5, 5, 6, 7, 8, 10\}$ 构造点集
> - 解方程$\dfrac{N(N-1)}{2} = 15$，解得$N = 6$，即一共有6个点

- 已知$x_1 = 0$且最长的距离为10，可以推断最远的点的坐标$x_6 = 10$
- 继续检查下一个**最大的距离**，找出当前所有可行点的位置，使用回溯法往下搜索，直到找出正确的解

> [!question] 问题：为什么不是找“下一个**最小的**距离”
> 相较于找最小的距离，找最大的距离所产生的可能性更少（或者解空间更小）（通常只有两种情况，分别在靠近两端的位置上），可以提升查找效率；而最小距离对应的点的位置很难确定，会加大查找的难度。

> [!code] 代码实现
> ```cpp
> bool Reconstruct(DistType X[], DistSet D, int N, int left, int right) {
>         // X[1]...X[left-1] and X[right+1]...X[N] are solved
>         bool Found = false;
>         if (is_Empty(D))
>             return true;  // solved
>         D_max = Find_Max(D);
>         // option 1: X[right] = D_max
>         // check if |D_max - X[i]| in D is true for all X[i]'s that have been solved
>         OK = Check(D_max, N, left, right);  // pruning
>         if (OK) {  // add X[right] and update D
>             X[right] = D_max;
>             for (i = 1; i < left; i++)
>                 Delete(abs(X[right] - X[i]), D);
>             for (i = right + 1; i <= N; i++)
>                 Delete(abs(X[right] - X[i]), D);
>             Found = Reconstruct(X, D, N, left, right - 1);
>             if (!Found) {  // if does not work, undo
>                 for (i = 1; i < left; i++)
>                     Insert(abs(X[right] - X[i]), D);
>                 for (i = right + 1; i <= N; i++)
>                     Insert(abs(X[right] - X[i]), D);
>             }
>         }
>         // finish checking option 1
> 
>         if (!Found) {  // if option 1 does not work
>             // option 2: X[left] = X[N] - D_max
>             OK = Check(X[N] - D_max, N, left, right); 
>             if (OK) { 
>                 X[left] = X[N] - D_max;
>                 for (i = 1; i < left; i++)
>                     Delete(abs(X[left] - X[i]), D);
>                 for (i = right + 1; i <= N; i++)
>                     Delete(abs(X[left] - X[i]), D);
>                 Found = Reconstruct(X, D, N, left + 1, right);
>                 if (!Found) { 
>                     for (i = 1; i < left; i++)
>                         Insert(abs(X[left] - X[i]), D);
>                     for (i = right + 1; i <= N; i++)
>                         Insert(abs(X[left] - X[i]), D);
>                 }
>             } 
>             // finish checking option 2
>         }  // finish checking all the option
> 
>         return Found;
> }    
> ```

### 3. Games: Tic-tac-toe
#### Description
> [!question] 问题描述
> **井字棋**(tic-tac-toe)：在 $3 \times 3$ 的棋盘上，一位玩家画圈，另一位玩家画叉，轮流下棋。如果某位玩家在棋盘上的所有标记中有3个位于同一行、同一列或同一对角线上，则该玩家获胜。    
> <div style="text-align: center"><img src="images/lec6/14.png" width="40%"></div> 
> 
> - 一共有 $9!$ 种可能的下棋顺序（不考虑当前的棋子是圈还是叉）
> - 一共有$3^9$种可能的棋局（每个格子上有圈、叉、空三种情况，不考虑获胜后停止下

#### Method
> 采用**极小化极大策略**(minimax strategy)来解决井字棋的问题，这一策略对于棋手双方而言都是最佳策略。

- 使用**评估函数**(evaluation function)来量化当前棋局 $P$ 的价值：令 $f(P) = W_{\text{Computer}} - W_{\text{Human}}$，$W$ 表示在当前棋局 $P$ 下可能的获胜情况数
- 假设玩家双方分别是人类和计算机，根据上述评估函数，人类倾向于最小化当前棋局$P$下的**价值**(goodness)，而计算机倾向于最大化$P$下的价值

> [!info] 流程
> 1. 先计算在第二轮结束后所有情况下的评估函数值（红色数字）
> 2. 第二轮是**人类**下棋，因此第一轮的评估函数值为第二轮评估函数中的**最小值**
> 	- 人类在第二轮中应选择第二种情况，因为它的评估函数值最小，获胜的希望更大
> 3. 第一轮是**计算机**下棋，因此第 0 轮的评估函数值为第一轮评估函数中的**最大值**
>  <div style="text-align: center"><img src="images/lec6/18.png" width="70%"></div> 


**$\alpha-\beta$ 剪枝**（pruning）：它结合了 $\alpha$ 剪枝和 $\beta$ 剪枝，能够将博弈树的搜索规模限制在 $O(\sqrt{N})$ 个节点（$N$ 为博弈树的节点数），提升搜索的效率

- $\alpha$ 剪枝：对下列情况，不需要再搜索根节点为 `?` 的子树
    <div style="text-align: center">
        <img src="images/lec6/19.png" width="35%">
    </div> 

    - 若`? >= 40`，第二层的节点`40`不会更新，因为该节点取的是左右孩子的最小值
    - 若 `? < 40`，虽然第二层节点的 `40` 会更新，但是不影响第一层的节点，因为第一层节点取的是左右孩子的最大值，而最大值原来就不是这个更新的节点

- $\beta$剪枝：对于下列情况，我们不需要再搜索根节点为`?`的子树
    <div style="text-align: center">
        <img src="images/lec6/20.png" width="37%">
    </div> 

    - 若`? <= 68`，第二层的节点`68`不会更新，因为该节点取的是左右孩子的最大值
    - 若`? > 68`，虽然第二层节点的`68`会更新，但是不影响第一层的节点，因为第一层节点取的是左右孩子的最小值，而最小值原来就不是这个更新的节点