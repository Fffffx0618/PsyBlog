# Chapter8.The Disjoint Set ADT

## 1. Equivalence Relations

**[Definition]** A **relation R** is defined on a set $S$ if for every pair of elements $(a, b),  a, b \in S ,  a \space R \space b$ is either true or false. If $a\space R\space b$ is true, then we say that $a$  is related to $b$.

**[Definition]** A relation, $\sim$ , over a set, $S$, is said to be an equivalence relation over $S$ iff it is **symmetric**, **reflexive**, and **transitive** over $S$.

- ***symmetric 自反性***：$∀a∈S, a \space R\space a$

- ***reflexive 对称性***：$a\space R\space b↔b\space R\space a$

- ***transitive 传递性***：$(a\space R\space b)∧(b\space R\space c)→a\space R\space c$

**[Definition]** Two members $x$ and $y$ of a set $S$ are said to be in the same **equivalence class** iff $x∼y$.

  > 等价类相当于 S 内的**分区 (partition)**，S 内的每个元素仅出现在一个等价类中

## 2. The Dynamic Equivalence Problem

<div style="text-align: center"><img src="images/image-20250402143716453.png" width="70%"></div>

- **Dynamic (on - line)**  动态的在线算法

~~~ c
Algorithm: (Union / Find)
{   
    // step 1: read the relations in
    Initialize N disjoint sets;
    While (read in a~b)
    {
        If (! (Find (a) == Find (b)))
            Union the two sets;
    } // end-while
    // step 2: decide if a~b
    While (read in a and b)
        If (Find (a) == Find (b))
            Output (true);
        Else
            Output (false);
}
~~~

- **ELements** of the sets : $1,2,3,\dots, N$
- **Sets** : $S_1, S_2,\dots$，如果满足 $S_i∩S_j=∅(if \space i≠j)$ ——**不相交 (disjoint)**
- **Operations**
    - `Union (i, j)` ： 用 $S=Si∪Sj$ 取代 $S_i$ 和 $S_j$
    - `Find (i)` ：找到包含元素 $i$ 的集合 $S_k$

## 3. Basic Data Structure

### 3.1 Union (i, j)

`S[element] = the element's parent`

Note: `S[root] = 0` and `set name = root index`

- **Before**

<div style="text-align: center"><img src="images/image-20250402150154939.png" width="70%"></div>


- **After**

<div style="text-align: center"><img src="images/image-20250402150203165.png" width="70%"></div>


~~~c
Void SetUnion (DisSet S, SetType Rt 1, SetType Rt 2)
{ S[Rt 2] = Rt 1; }
~~~

### 3.2 Find (i)

```c
SetType Find (ElementType X, DisSet S){
    For (; S[X] > 0; X = S[X]);
    Return X;
}
```

###  3.3 Analysis

因为 `union ()` 和 `find ()` 操作往往是成对出现的，因此要分析该算法的复杂度，需要考虑执行一系列的 `union () + find ()` 运算

```c
Algorithm using union-find operations
{  Initialize S[i] = {i} for i = 1,..., 12;
   For (k = 1; k <= Size; k++){
       If (Find (i) != Find (j))
           SetUnion (Find (i), Find (j)); 
      }
}
```

------

**the worst situation**：

`union (2, 1), find (1); union (3, 2), find (2); ...... Union (N, N - 1), find (1);`

**Time complexity :  $Θ(N^2)$**

<div style="text-align: center"><img src="images/Quicker_20240410_170917.png" width="40%"></div>



## 4. Smart Union Algorithms

#### 4.1 Union-by-Size

> 总是将规模小的树合并到规模大的树上

* `S[Root] = -size; /*initialized to be -1*/`

**[Lemma]** Let $T$ be a tree created by union-by-size with $N$ nodes, then $height (T)≤⌊log⁡_2 N⌋+1$

* The time complexity of `Find ()` is $O (log⁡N)$

**Time complexity** of $N$ Union and $M$ Find Operations is now $O (N+Mlog⁡N)$

```c
Void SetUnion (DisjSet S, SetType Root 1, SetType Root 2)
{
    If (Root 1 == Root 2)
        Return;
    if (S[Root 2] < S[Root1]){ // the size of Root2 > Root 1
        S[Root 2] += S[Root 1];
        S[Root 1] = Root 2;
    }else{
        S[Root 1] += S[Root 2];// the size of Root 1 > Root 2
        S[Root 2] = Root 1;
    }
}
```

#### 4.2 Union-by-Height (rank)

> 总是将矮的那棵树合并到高的那棵树上

```c
Void SetUnion (DisjSet S, SetType Root 1, SetType Root 2)
{
    If (S[Root 2] < S[Root 1])
        S[Root 1] = Root 2;
    Else{
        If (S[Root 1] == S[Root 2])
            S[Root 1]--;
        S[Root 2] = Root 1;
    }
}
```

## 5. Path Compression

<div style="text-align: center"><img src="images/Quicker_20240421_170311.png" width="55%"></div>



>- 该方法与 union-by-height 的方法不兼容，因为树的高度发生改变。所以推荐使用 **union-by-size**

```c
SetType Find ( ElementType X, DisjSet S )
{
    If ( S[ X ] <= 0 ) return X;
    Else return S[ X ] = Find ( S[ X ], S );
}
```

``` c
SetType Find ( ElementType X, DisjSet S )
{
    ElementType root, trail, lead;
    For ( root = X; S[root] > 0; root = S[root] ); /* find the root */
    For ( trail = X; trail != root; trail = lead ) {
        Lead = S[trail];
        S[ trail ] = root;
    } /* collapsing */
    Return root;
}
```

### 6. Worst Case for Union-by-Rank and Path Compression

> 考试不做要求

**[Lemma (Tarjan)]** Let $T (M, N)$ be the maximum time required to process an intermixed sequence of $M \geq N$ finds and $N-1$ unions. 

Then:

$k_1 M \alpha (M, N) \leq T (M, N) \leq k_2 M \alpha (M, N)$  for some positive constants $k_1$ and $k_2$

* Ackermann’s Function and $\alpha (M, N)$

$$
A (i, j) = \begin{cases} 
2^j & i = 1 \text{ and } j \geq 1 \\
A (i-1, 2) & i \geq 2 \text{ and } j = 1 \\
A (i-1, A (i, j-1)) & i \geq 2 \text{ and } j \geq 2 
\end{cases}
$$

- $\alpha (M, N) = \min\{ i \geq 1 | A (i, \lfloor M/N \rfloor) > \log N \}$
