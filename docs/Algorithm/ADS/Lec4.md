# Leftist Heaps and Skew Heaps
> [!Heaps]
> - Almost complete binary tree
> - Max/Min heap

## 4.1 Leftist Heaps
> Target: Speed up merging in $O(N)$.
### 4.1.1 Definition
==Leftist heaps 左偏堆==
- Order Property : the same
- Structure Property : binary tree, but *unbalanced*

==Null path length 零路径==，记作 $\mathrm{Npl}(X)$，指从节点 $X$ 到**没有两个孩子的节点**（即叶节点或度为1的节点）的最短距离
- Define $\mathrm{Npl}(\text{NULL}) = -1$
- 空指针路径长度的递推关系式为：
$$
\mathrm{Npl}(X) = \min \{\mathrm{Npl}(C) + 1\ \mathrm{for\ all}\ C\ \mathrm{as\ children\ of}\ X\}
 $$
==左偏堆的性质==：对于堆上的每个节点，它的左孩子的 $\mathrm{Npl}$**不小于**它的右孩子的 $\mathrm{Npl}$，即左子树的深度更深一些
- 因此，空指针路径长度往往是**自底向上**计算的

> [!Theorem]
> 对于一个左偏堆，如果它右侧的路径上有 $r$ 个节点（即根节点的空指针路径长度为 $r-1$），那么它至少有 $2^r - 1$ 个节点。

> [!Proof]
> - 当 $r = 1$ 时，显然成立  
> - 假设当 $r \le k$ 时定理成立
> 	- 当 $r = k + 1$ 时
>     - 右子树的右侧路径上有 $k$ 个节点，那么根据假设，右子树的节点数至少为 $2^k - 1$
>     - 再根据左偏树的定义，左孩子的空指针路径长度不小于它的右孩子的空指针路径长度，因此左子树的节点数至少为 $2^k - 1$
>     - 整个堆的节点数至少为 $1 + 2 \times (2^k - 1) = 2^{k + 1} - 1$，得证

推论：对于一个有 $N$ 个节点的Leftist heap，它的右侧路径上至多有 $\lfloor \log (N + 1) \rfloor$ 个节点
- 想要减小合并操作所花的时间，需要让该操作尽可能地在堆的右侧来完成
- 右侧的堆高为 $O(\log N)$，合并的速度能接近 $O(\log N)$ 

### 4.1.2 Operations
左偏堆声明如下：
```c
    #ifndef _LeafHeap_H

    struct TreeNode;
    typedef struct TreeNode * PriorityQueue;

    // Minimal set of priority queue operations
    // Note that nodes will be shared among several
    // leftist heaps after a merge; the use must
    // make sure to not use the old leftist heaps

    PriorityQueue Initialize(void);
    ElementType FindMin(PriorityQueue H);
    int IsEmpty(PriorityQueue H);
    PriorityQueue Merge(PriorityQueue H1, PriorityQueue H2);

    #define Insert(X, H) ( H = Insert1((x), H) )
    // DeleteMin macro is omitted

    PriorityQueue Insert1(ElementType X, PriorityQueue H);
    PriorityQueue DeleteMin1(PriorityQueue H);

    #endif

    // Place in implementation file
    struct TreeNode {
        ElementType   Element;
        PriorityQueue Left;
        PriorityQueue Right;
        int           Npl;
    };
```

#### 1. Merge
##### **Recursive Version**
合并这两个左偏堆：
<div style="text-align: center">
<img src="images/lec4/5.png" width="50%">
</div>

合并操作流程如下：

| **合并**：`Merge(H1->Right, H2)`                                                                    | **附加**：`Attach(H2, H1->Right)`                                                                   | 如有必要，**交换**左右子树：`Swap(H1->Right, H1->Left)`                                                      |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| <div style="text-align: center"><br>    <img src="images/lec4/6.png" width="100%"><br>    </div> | <div style="text-align: center"><br>    <img src="images/lec4/7.png" width="100%"><br>    </div> | <div style="text-align: center"><br>    <img src="images/lec4/8.png" width="100%"><br>    </div> |
| 由于 $H_1$ 的根节点更小，所以将 $H_1$ 的右子树与 $H_2$ 进行递归地合并                                                    | 将合并好的堆附加到 $H_1$ 右子树的位置                                                                           | 根据具体情况决定                                                                                         |
**Code implement**
```c
PriorityQueue Merge(PriorityQueue H1, PriorityQueue H2) {
    // If one heap is empty, then return another heap
    if (H1 == NULL) {  
        return H2;
    }
    if (H2 == NULL) {
        return H1;
    }
    // Assure that the left parameter is the heap with smaller root
    if (H1->Element < H2->Element) {
        return Merge1(H1, H2);
    } else {
        return Merge1(H2, H1);
    }
}

static PriorityQueue Merge1(PriorityQueue H1, PriorityQueue H2) {
    if (H1->Left == NULL) {     // single node
        H1->Left = H2;          /* H1->Right is already NULL
                                and H1->Npl is already 0*/
    } else {
        H1->Right = Merge(H1->Right, H2);  // Step 1 & 2
        if (H1->Left->Npl < H1->Right->Npl) {
            SwapChildren(H1);              // Step 3
        }
        H1->Npl = H1->Right->Npl + 1;      // Important!
    }
    return H1;
}
```
##### **Iterative Version**
在不改变左孩子的情况下，根据两个堆的右子树进行合并：
- 将根节点较小的堆作为合并的**目标堆**，然后将目标堆的右子树“拆出来”，作为**待比较堆A**，另一个堆作为**待比较堆B**
- 比较两个待比较堆，将**根节点更小的待比较堆去掉右子树后**附加到目标堆的最右侧，更新目标堆   
- 而被抛下的右子树作为新的待比较堆，与另一个待比较堆继续比较
 - 重复进行上述的比较、附加操作，直到只剩下一个目标堆为止

**初始状态**
<div style="text-align: center">
            <img src="images/lec4/5.png" width="40%">
            </div>
- 将 $H_1$ 作为**目标堆**，它的右子树作为待比较堆A，$H_2$ 作为待比较堆B

| Step 1                                                                                                          | Step 2                                                                                                            | Step 3                                                                                                            | Step 4                                                                                                            |
| --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| <div style="text-align: center"><br>            <img src="images/lec4/9.png" width="90%"><br>            </div> | <div style="text-align: center"><br>            <img src="images/lec4/10.png" width="100%"><br>            </div> | <div style="text-align: center"><br>            <img src="images/lec4/11.png" width="100%"><br>            </div> | <div style="text-align: center"><br>            <img src="images/lec4/12.png" width="100%"><br>            </div> |
| $H_2$ 的根节点更小，将 $H_2$ 的**根节点及其左子树**附加在 $H_1$ 的右子树，作为新的目标堆；而 $H_1$ 原来的右子树与 $H_2$ 原来的右子树作为新的一组待比较堆                 | $H_2$ 原来右子树上的根节点更小，将它的**根节点及其左子树**附加在目标堆最右侧的位置上；原 $H_1$ 右子树和 $H_2$ 右子树的右子树作为新的待比较堆                                | $H_1$ 原来右子树上的根节点更小，因此将它的**根节点及其左子树**附加在目标堆最右侧；此时仅剩下原 $H_2$ 右子树的右子树                                                | 将剩余的堆附加在目标堆的最右侧，合并操作完成                                                                                            |
> [!Note]
> 左子树空指针路径长度更小时，交换合并后的堆的两个子树
> <div style="text-align: center"><img src="images/lec4/8.png" width="30%"></div>
> 
> - 只要出现堆中右子树比左子树规模更大的情况，就应该调整，因此可能需要**交换多次**

Pros and Cons：
- 递归实现的难度较小，代码写起来较为容易，但是不易理解合并的过程
- 迭代实现更为清晰地展现了合并的过程，但是代码编写较为困难
两者时间复杂度均为 $T_P = O(\log N)$

#### 2. Insert
- 插入是一种特殊的合并操作，可以理解为<u>只有一个节点的堆与另一个堆进行合并</u>

#### 3. DeleteMin
可以利用合并操作来删除最小节点：
1. 删除根节点，此时会将原来的堆拆作两个子堆
2. 合并两个子堆
时间复杂度：$T_P = O(\log N)$
---

## 4.2 Skew Heaps
### 4.2.1 Definition
**斜堆**(skew heaps)是左偏堆的一种简单形式，它删除了 `Npl` 字段，但能保证在 $M$ 次连续操作消耗至多 $O(M \log N)$ 的时间

> [!操作过程]
> **合并操作**：
> - 由于斜堆不维护 `Npl`，因此**即将被附加的待比较堆**（包括最开始的目标堆）在拆开右子树后，需要把待比较堆的左子树换到右子树的位置上，然后再加到目标堆上。也就是每一次的附加都要一次交换操作
> 
> - 斜堆的优势：不用维护 `Npl`，节省了存储空间，同时也不需要根据 `Npl` 判断是否交换堆的两个孩子

> [!caution]
> Note: 右侧路径上的**最后一个节点**如果只有*一个孩子*，则不用交换左右子树，其余情况全部需要交换左右子树。
> [可以看这里关于Skew Heap的例题](https://www.yuque.com/xianyuxuan/coding/ads_exam_1#I4vFd)
### 4.2.2 Amortized Analysis
合并操作的摊还复杂度 $T_{\mathrm{amortized}} = O(\log N)$，证明如下：

> [!Proof]
> 采用势能分析法
> 
> 首先确定**势能函数**：令 $D_i$ 为第 $i$ 次操作后的目标堆的根节点，势能函数 $\Phi(D_i)$ 为这个堆上**重节点**的个数
> 
> - 「==重节点==(heavy node)」，指的是满足**右子树的节点个数占整棵树节点个数（包括这个根节点）的一半以上**的节点；对应的，不是重节点的节点被称为「==轻节点==(light node)」
> 
>> [!question] 势能函数为什么不是右子树的节点个数
>> - 斜堆会不停地交换左右子树，右子树的节点个数有可能会增加，这是**不好的情况**；但是在**好的情况**下，右子树的节点个数也不会减少。这导致势能函数<u>只能反映不好情况下堆的变化，而无法体现好的情况</u>，因此记录右子树的节点个数不能满足要求。
>> - 而重节点个数很好地反映了当前斜堆的情况：情况较差时，重节点个数多；情况较好时，重节点个数少，可用于“抵消”情况较差的情况，因而更适合作为势能函数。
> 
> **结论**：<u>合并后轻重状态发生变化的节点一定位于原来堆上的（最）右侧路径</u>
> - 理由：在斜堆的合并过程中，待比较堆的根节点一定是原来两个堆上（最）右侧路径的节点，而其他路上的节点基本维持原有的样子不变
> 
> 在势能分析的时候，更关注右侧路径上的节点。记 $H_i = l_i + h_i(i = 1, 2)$，其中 $H_i$, $l_i$ 和 $h_i$ 分别表示右侧路径的节点数，右侧路径上的轻节点数和重节点数。
> 
> 在最坏情况下，合并所需时间为：
> 
> $$
> T_{\mathrm{worst}}= l_1 + h_1 + l_2 + h_2
> $$
> 
> - 合并前，势能函数$\Phi_i = h_1 + h_2 + h$，其中$h$为两个堆内剩余的重节点数
> - 合并后，势能函数$\Phi_{i+1} \le l_1 + l_2 + h$
>     - 原因：由上面的结论知，两个堆右侧路径的节点的轻重状态可能会发生改变，最坏的情况是：原来两个堆右侧路径上的节点都是轻节点，合并之后都变成了重节点，所以合并后的堆的重节点个数最多为$l_1 + l_2 + h$
> 
> 所以，
> $$
> \begin{align}
> T_{\mathrm{amortized}} & = T_{\mathrm{worst}} + \Phi_{i+1} - \Phi_i \notag \\
> & = 2(l_1 + l_2) \notag
> \end{align} 
> $$
> 由于 $l = O(\log N)$，所以摊还复杂度 $T_{\mathrm{amortized}} = O(\log N)$，证毕。
> 
>> [!Proof] 证明 $l = O(\log N)$
> >注：$l$是堆（最）右侧路径的轻节点数
> 可以先证明：对于右侧路径上带有 $l$ 个轻结点的斜堆，至少有 $2^l - 1$ 个结点。即如果一个堆有 $N$ 个节点，那么它右侧路径上的轻节点个数为 $O(\log N)$，即 $l = O(\log N)$，所以只要证出前者，后者自然成立。
>>  
>> 采用**归纳法**证明：
>> - 当 $l = 1$ 时，显然成立；假设 $l \le n$ 时，该结论成立
>>- 当$l = n + 1$时，先找到右侧路径的第二个轻节点，根据归纳假设知，以该节点为根节点的子树至少有$2^l - 1$个节点
>>- 再找第一个轻节点，由轻节点的定义知，它的左子树节点数一定大于右子树节点数，而上面提到的子树位于它的右子树处，所以以第一个轻节点为根节点的子树至少有$2 \times (2^l - 1) + 1 = 2^{l + 1} - 1$个节点。那么整个堆的节点个数一定大于$2^{l + 1} - 1$，得证

**自调整**(self-adjusting) 的数据结构
- 自调整数据结构是一类在操作过程中会根据访问或修改的历史信息动态调整自身结构，以提高效率的数据结构。这些数据结构没有固定的形态，能通过自适应性调整，在特定情况下优化常用操作的性能。前面介绍过的**伸展树**和**斜堆**均有这种自调整的特性，它们的共同点有：
	1. 节省空间（无需记录额外的平衡信息）
	2. 访问和更新相关的算法易于理解和实现
	3. 不考虑因数的情况下，这类算法的效率与对应的平衡版本的数据结构（AVL 树和左偏堆）是相当的
	4. 局部调整的次数**不小于**对应的平衡版本的数据结构