# B+ 树索引文件

!!! abstract

    B+ 树索引是一种最常用的数据库索引结构。它通过**平衡树**结构，在数据不断插入、删除时仍然保持较好的查找、顺序扫描、插入和删除性能。

    本节重点理解：B+ 树为什么比 index-sequential file organization 更适合动态更新的数据文件，以及 B+ 树的 leaf node、nonleaf node、fanout、平衡性和重复 search key 的处理方式。

## 1. 基本性质

B+ 树是一棵 ==balanced tree==。它最重要的结构性质是：

> 从 root 到任意 leaf 的路径长度都相同。

这意味着所有叶子节点处在同一层，查找任何 search key 需要经过的树高相同，因此查找性能稳定。

设一棵 B+ 树的阶数参数为 $n$：

- 每个 **nonleaf node** 最多有 $n$ 个 children；
- 除 root 以外，每个 nonleaf node 至少有 $\lceil n/2\rceil$ 个 children；
- root 至少有 $2$ 个 children，最多有 $n$ 个 children；
- 如果整棵树只有一个节点，那么 root 可以同时也是 leaf。

B+ 树相比简单索引结构会带来一些额外开销：

- 插入和删除时可能需要 split、merge 或 redistribution；
- 节点可能最多接近半空，因此存在一定空间浪费；
- 维护树结构需要额外的指针和内部节点。

但是这些开销是可以接受的，因为 B+ 树避免了频繁的文件重组，并且能长期保持较好的查询性能。

---

## 2. 节点结构

### 2.1 节点中的键与指针

一个典型的 B+ 树节点最多包含：

- $n-1$ 个 search-key values：$K_1, K_2, \dots, K_{n-1}$；
- $n$ 个 pointers：$P_1, P_2, \dots, P_n$。

节点内部的 search-key values 按升序排列：

$$
i<j \Rightarrow K_i<K_j
$$

如果允许重复 search key，这个条件会相应放宽为：

$$
i<j \Rightarrow K_i\le K_j
$$

!!! note

    B+ 树节点中的 key 主要用于导航；真正的数据记录指针通常都在 leaf node 中。Nonleaf node 起到多级索引的作用。

### 3.2 叶子节点

叶子节点保存实际的 search-key values，并指向数据文件中的记录。

对于 $i=1,2,\dots,n-1$：

- $K_i$ 是某个 search key；
- $P_i$ 指向 search-key value 为 $K_i$ 的文件记录；
- $P_n$ 不指向记录，而是用于连接下一个 leaf node。

叶子节点最多可以保存 $n-1$ 个 search-key values，最少可以保存：

$$
\left\lceil \frac{n-1}{2} \right\rceil
$$

个 search-key values。

!!! example "当 n=4 时"

    - 每个叶子节点最多保存 $3$ 个 search-key values；
    - 每个叶子节点至少保存：$\left\lceil \dfrac{4-1}{2} \right\rceil=\lceil 1.5\rceil=2$ 个 search-key values。

#### 叶子节点的顺序性

叶子节点按 search key 的大小从左到右排列。若 $L_i$ 在 $L_j$ 左边，且 $i<j$，那么：

$$
\text{任意 }v_i\in L_i,\ v_j\in L_j,\quad v_i<v_j
$$

也就是说，左边叶子中的所有 search key 都小于右边叶子中的所有 search key。

#### 叶子节点链接

由于叶子节点本身已经按照 search key 排好序，因此 B+ 树用最后一个指针 $P_n$ 把所有叶子节点串成一个链表。

这样做的好处是：

- 查找某个 key 时，可以从 root 走到对应 leaf；
- 顺序扫描时，只需要沿着 leaf-level linked list 向右移动；
- 范围查询（range query）可以高效地从起点 leaf 扫到终点 leaf。

!!! example "叶子节点的图示含义"

    如果 $n=4$，一个叶子节点可以有最多 $3$ 个 key 和 $4$ 个 pointer。其中前三个 pointer 指向实际记录，最后一个 pointer 指向下一个叶子节点。

### 3.3 Dense Index 中的叶子节点

如果 B+ 树索引用作 ==dense index==，那么每一个 search-key value 都必须出现在某个 leaf node 中。

这点和 nonleaf node 不同：

- 叶子节点保存完整的 search-key entries；
- 非叶子节点只保存用于导航的 separator keys。

因此，B+ 树的真实数据访问入口在 leaf 层。

---

## 4. 非叶子节点

非叶子节点构成了叶子节点之上的多级稀疏索引（multilevel sparse index）。它们的结构和叶子节点类似，也包含 key 和 pointer，但 pointer 的含义不同：

- 在叶子节点中，pointer 指向文件记录或下一个叶子节点；
- 在非叶子节点中，pointer 指向下一层 tree node。

### 4.1 Fanout

一个 nonleaf node 最多有 $n$ 个 pointers，除 root 外至少有：

$$
\lceil n/2\rceil
$$

个 pointers。

一个节点中 pointer 的数量称为该节点的 ==fanout==。Fanout 越大，树越矮；树越矮，查找时需要访问的节点层数越少。

### 4.2 非叶子节点的导航规则

设某个非叶子节点中有 $m$ 个 pointers，且 $m\le n$。它的结构可以理解为：

```text
P1  K1  P2  K2  P3  ...  K(m-1)  Pm
```

各个 pointer 指向的子树范围如下：

| Pointer | 指向的 search-key 范围 |
| --- | --- |
| $P_1$ | 小于 $K_1$ 的 search keys |
| $P_i,\ 2\le i\le m-1$ | 大于等于 $K_{i-1}$ 且小于 $K_i$ 的 search keys |
| $P_m$ | 大于等于 $K_{m-1}$ 的 search keys |

也就是说，非叶子节点中的 key 不是直接对应一条数据记录，而是把 search-key space 划分成若干区间。查找时，根据目标 key 落在哪个区间，选择对应 pointer 继续向下走。

!!! info "查找过程"

    从 root 开始，根据 search key 和当前节点中的 separator keys 比较，选择对应 pointer 进入下一层。重复这个过程，直到到达 leaf node。最后在 leaf node 中找到具体 key 对应的记录指针。

### 4.3 根节点的例外

根节点和普通 nonleaf node 的约束略有不同：

- 普通 nonleaf node 至少有 $\lceil n/2\rceil$ 个 pointers；
- 根节点可以少于 $\lceil n/2\rceil$ 个 pointers；
- 但只要整棵树不止一个节点，根节点至少要有 $2$ 个 pointers。

这个例外使得 B+ 树在规模很小时也能合法存在。

---

## 5. B+ 树的高度和平衡性

原文中给了两个 instructor file 上的 B+ 树例子：

- 一个例子取 $n=4$；
- 另一个例子取 $n=6$。

当 $n$ 变大时，每个 nonleaf node 可以有更多 children，也就是 fanout 更大。因此树的高度通常会降低。

可以直观理解为：

$$
\text{fanout 越大}
\Rightarrow
\text{每层覆盖的 key 范围越多}
\Rightarrow
\text{树高越小}
$$

但是，无论 $n=4$ 还是 $n=6$，B+ 树都必须满足同一个平衡条件：

> 从 root 到每一个 leaf node 的路径长度完全相同。

这正是 B+ 树查找、插入、删除性能良好的原因。只要树保持平衡，查找任何 key 都不会退化成线性扫描。

---

## 6. 重复 Search Key 的处理

前面的结构说明默认 search key 是 unique 的，也就是每个 search key 最多出现在一条记录中。但现实数据库中，search key 经常会重复。

例如 `instructor` 关系中，`name` 可能重复；如果用 `name` 建索引，就会出现多个记录具有同一个 search key 的情况。

### 6.1 方法一：重复存储 search key

一种处理方法是在 leaf node 中把同一个 search key 存储多次，每一份都指向一条不同记录。

此时节点内部 key 的有序条件要从：

$$
i<j \Rightarrow K_i<K_j
$$

改为：

$$
i<j \Rightarrow K_i\le K_j
$$

这种方法的问题是：

- internal nodes 中也可能出现重复 search key；
- 插入和删除过程会变得更复杂；
- 维护成本更高。

### 6.2 方法二：为每个 key 存 pointer bucket

另一种方法是每个 search key 只存一次，但为它保存一个 record pointer set / bucket。

例如：

```text
name = "Kim"  ->  {ptr1, ptr2, ptr3, ...}
```

这种方法的问题是：

- bucket 本身需要额外管理；
- 如果某个 key 对应的记录很多，bucket 会变大；
- 访问效率可能下降，尤其是某个 search key 的重复记录非常多时。

### 6.3 实际数据库常用方法：构造唯一复合键

大多数数据库实现会把 nonunique search key 自动扩展成 unique composite search key。

假设关系 $r$ 中希望建立索引的属性是 $a_i$，但 $a_i$ 不唯一。设 $A_p$ 是关系 $r$ 的 primary key，则可以使用复合 search key：

$$
(a_i, A_p)
$$

代替单独的 $a_i$ 来建立索引。

因为 primary key 本身唯一，所以 $(a_i,A_p)$ 一定唯一。

!!! example "对 instructor.name 建索引"

    如果希望在 `instructor` 关系上对 `name` 建索引，而 `name` 可能重复，那么数据库可以实际建立：

    $$
    (\text{name}, \text{ID})
    $$

    作为复合 search key。

    其中 `ID` 是 `instructor` 的 primary key，因此 `(name, ID)` 是唯一的。即使用户只按 `name` 查询，也仍然可以利用这个复合索引高效查找。

!!! abstract "重复 key 的处理"

    - 教材示例中为了简单，常假设 search key 没有重复。
    - 实际数据库通常会在内部自动添加额外属性，使 search key 唯一。
    - 这样既能保持 B+ 树结构规则清晰，也能避免 internal nodes 中大量重复 key 带来的复杂性。

---

## 7. 本节小结

1. Index-sequential file organization 会随着文件增长和更新而性能下降，频繁重组文件代价较高。
2. B+ 树通过 balanced tree 结构，在插入和删除后仍能保持较好的查找性能。
3. B+ 树中所有 root-to-leaf 路径长度相同，这是性能稳定的关键。
4. Leaf node 保存 search-key entries，并通过最后一个 pointer 串成有序链表，支持高效顺序扫描和范围查询。
5. Nonleaf node 是 leaf nodes 上方的 sparse index，pointer 指向子树而不是记录。
6. Fanout 越大，树通常越矮，查找需要访问的层数越少。
7. Root node 有特殊约束：除非整棵树只有一个节点，否则 root 至少有两个 children。
8. 重复 search key 可以通过重复存储、pointer bucket 或复合唯一键处理；实际数据库通常使用复合唯一键。
