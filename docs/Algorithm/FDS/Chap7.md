# Chapter7.Sorting

## 1. Preliminaries
`void X_sort (ElementType A[], int N)`

* N must be a legal integer
* Assume integer array for the sake of simplicity
* ***comparison-based sorting 基于比较的排序*** : '>' and '<' operators exist and are the only operations allowed on the input data
* Consider ***internal sorting 内部排序*** only (即整个排序能在主内存中完成）

## 2. Insertion Sort

> 重复 $N - 1$ 趟排序，从 $P = 1$ 到 $P = N - 1$ 。排序前已知 $0$~$P-1$ 位置上的元素是有序的。对于第 $P$ 趟排序，我们将位置 $P$ 上的元素向前 $P$ 个元素移动，直到发现正确的位置。这样保证每趟排序结束后位置在 $0$ ~ $P$ 上的元素是有序的。

```c
Void InsertionSort (ElementType A[], int N)
{
    Int j, P;
    ElementType Tmp;

    For (P = 1; P < N; P++)
    {
        Tmp = A[P] // the next coming card
        For (j = P; j > 0 && A[j - 1] > Tmp; j--)
            A[j] = A[j - 1];
        // shift sorted cards to provide a position for the new coming card
        A[j] = Tmp; // place the new card at the proper position
    } // end for-P-loop
}
```

* The worst case : Input A[ ] is in reverse order. $T (N)=O (N^2)$.
* The best case : Input A[ ] is in sorted order. $T (N)=O (N)$.

## 3. A Lower Bound for Simple Sorting Algorithms
【Definition】An ***inversion 逆序*** in an array of numbers is any ordered pair $(i, j)$ having the property that $i < j$ but $A[i] > A[j]$.

* Swapping two adjacent elements that are out of place removes **exactly one** inversion.
* $T (N, I) = O (I + N)$ where $I$ is the number of inversions in the original array.
    * Fast if the list is almost sorted.

【Theorem】The average number of inversions in an array of $N$ distinct numbers is $\frac{1}{4} N (N-1)$

【Theorem】Any algorithm that sorts by exchanging adjacent elements requires $\Omega (N^2)$ time on average.

## 4. Shellsort


<div style="text-align: center"><img src="images/image-20250507142708116.png" width="55%"></div>

* Define an ***increment sequence 增量序列*** $h_1<h_2<\dots<h_t (h_1=1)$
* Define an $h_k-sort$ at each phase for $k = t, t-1,\dots, 1$
    * An $h_k-sorted$ file that is then $h_{k-1}sorted$ reamains $h_k-sorted$

### 4.1 Shell's increment sequence
$$
H_t=⌊ \frac{N}{2}⌋, h_k=⌊ \frac{h_{k+1}}{2}⌋
$$

```c
Void Shellsort (ElementType A[], int N)
{
    Int i, j, increment;
    ElementType Tmp;
    For (increment = N / 2; increment > 0; increment /= 2)
        // h sequence
        For (i = increment; i < N; i++)
        { // insertion sort
            Tmp = A[i];
            For (j = i; j >= increment; j -= increment)
                If (Tmp < A[j - increment])
                    A[j] = A[j - increment];
                Else
                    Break;
                A[j] = Tmp;
        } // end for-l and for-increment loop
}
```

**[Theorem]**: The worst-case running time of Shellsort, using Shell's increments, is $\Theta (N^2)$

### 4.2 Hibbard's increment sequence
> Improved

$$
H_k=2^k-1
$$

**[Theorem]**: The worst-case running time of Shellsort, using Shell's increments, is $\Theta (N^{3/2})$

#### Conjectures

* $T_{avg-Hibbard}(N)=O (N^{5/4})$
* Sedgewick's best sequence is {1, 5, 19, 41, 109,…}, which the terms are either of the form $9×4^i−9×2^i+1$ or $4^i−3×2^i+1$
    - $T_{avg}(N)=O (N^{7/6})$
    - $T_{worst}(N)=O (N^{4/3})$
* **In-place**：
    - 算法**不需要额外的空间**来执行操作，或者只需要固定数量的额外空间（比如 $O (1)$ 复杂度的空间）。这意味着该算法主要使用输入的数据结构本身来进行计算。
* **Stable**：
    - 算法保持**相等元素之间的相对顺序**不变。即在排序前出现在相同值前面的元素，在排序后仍然会保持在这些相同值的前面。这对于处理具有多个键的数据非常重要。

## 5. Heapsort

**Algorithm 1**
  $T (N)=O (NlogN)$, but **not in-place**

  ```c
  Algorithm 1:
  {
      BuildHeap (H);  // O (N)
      For (i = 0; i < N; i++)
          TmpH[i] = DeleteMin (H);  // O (log N)
      For (i = 0; i < N; i++)
          H[i] = TmpH[i];  // O (1)
  }
  ```

**Algorithm 2**

**[Theorem]**: The average number of comparisons used to heapsort a random permutation of $N$ distinct items is $2 N\log N-O (N\log\log N)$

  ```c
  // 这里的 PercDown 函数与 Chap 6 给出的稍有不同（索引的标注发生变化）
  #define LeftChild (i) (2 * (i) + 1)
  
  Void PercDown (ElementType A[], int i, int N)
  {
      Int Child;
      ElementType Tmp;
  
      For (Tmp = A[i]; LeftChild (i) < N; i = Child)
      {
          Child = LeftChild (i);
          If (Child != N - 1 && A[Child + 1] > A[Child])
              Child++;
          If (Tmp < A[Child])
              A[i] = A[Child];
          Else
              Break;
      }
      A[i] = Tmp;
  }
  
  Void Heapsort (ElementType A[], int N)
  {
      Int i;
      For (i = N / 2; i >= 0; i--)  // BuildHeap
          PercDown (A, i, N);
      For (i = N - 1; i > 0; i--)   // DeleteMax
      {
          Swap (&A[0], &A[i]);
          PercDown (A, 0, i);
      }
  }
  ```

## 6. Mergesort
#### Merge two sorted lists

* $T (N)=O (N)$

<div style="text-align: center"><img src="images/image-20250507152213200.png" width="60%"></div>

#### Mergesort
* 体现了分治 (divide-and-conquer)思想

  ```c
  Void MergeSort (ElementType A[], int N)
  {
      ElementType *TmpArray;
      TmpArray = (ElementType *) malloc (N * sizeof (ElementType));
      If (TmpArray != NULL)
      {
          MSort (A, TmpArray, 0, N - 1);
          Free (TmpArray);
      }
      Else FatalError ("No space for tmp array!!!");
  }
  
  Void MSort (ElementType A[], ElementType TmpArray[], int Left, int Right)
  {
      Int Center;
      If (Left < Right)
      {
          Center = (Left + Right) / 2;
          MSort (A, TmpArray, Left, Center);
          MSort (A, TmpArray, Center + 1, Right);
          Merge (A, TmpArray, Left, Center + 1, Right);
      }
  }
  
  // Lpos = start of left half, Rpos = start of right half
  Void Merge (ElementType A[], ElementType TmpArray[], int Lpos, int Rpos, int RightEnd)
  {
      Int i, LeftEnd, NumElements, TmpPos;
      LeftEnd = Rpos - 1;
      TmpPos = Lpos;
      NumElements = RightEnd - Lpos + 1;
      While (Lpos <= LeftEnd && Rpos <= RightEnd) // main loop
          If (A[Lpos] <= A[Rpos])
              TmpArray[TmpPos++] = A[Lpos++];
          Else
              TmpArray[TmpPos++] = A[Rpos++];
      While (Lpos <= LeftEnd) // Copy rest of first half
          TmpArray[TmpPos++] = A[Lpos++];
      While (Rpos <= RightEnd) // Copy rest of second half
          TmpArray[TmpPos++] = A[Rpos++];
      For (i = 0; i < NumElements; i++, RightEnd--)
          // Copy TmpArray back
          A[RightEnd] = TmpArray[RightEnd];
  }
  ```

#### Analysis

$$
\begin{align}
T (1)&=1\\
T (N)&=2 T (N/2)+O (N)\\
&=O (N+NlogN)
\end{align}
$$

|           | in-place | stable |
| :-------- | :------: | :----: |
| insertion |    1     |   1    |
| shell     |    1     |   0    |
| heap      |    1     |   0    |
| merge     |    0     |   1    |

## 7. Quicksort
### 7.1 The Algorithm

```c
Void Quicksort (ElementType A[], int N)
{
    If (N < 2) return;
    Pivot = pick any element in A[];
    Partition S = { A[] \ pivot } into two dijoint sets:  
        A 1 = {a in S | a <= pivot} and A2 = {a in S | a >= pivot}
    A = Quicksort (A 1, N 1) + {pivot} + Quicksort (A 2, N 2);
}
```

- The best average case : $O (N\log{N})$

### 7.2 Picking the Pivot

Median-of-Three Partitoning:`Pivot=median (left, center, right)`

- Eliminates the bad case for sorted input and actually reduces the running time by about $5\%$

### 7.3 Partitioning Strategy

- 初始状态：将 `Pivot` 与最后一个元素交换，即把 `Pivot` 放入最后；`i` 从第一个元素开始，`j` 从倒数第二个元素开始
- 当 `i < j` 时，
    - 若 `i` 所指元素比 `Pivot` 小，`i++`，否则停止
    - 若 `j` 所指元素比 `Pivot` 大，`j--`，否则停止
    - 当 `i` 和 `j` 都停止，交换 `i, j` 所指元素
  这样，数组中比 `Pivot` 小的元素在左边，比 `Pivot` 大的元素在右边
- 最后 `i >= j` 时，`i` 位置上的元素和 `pivot` 互换，让 `pivot` 重新回到中间


<div style="text-align: center"><img src="images/image-20250514144928822.png" width="60%"></div>

* `key == pivot` 时, 同时停止 `i` 和 `j`：
- 较坏的情况：1, 1, 1, ……, 这时快排就会进行许多无意义的交换
    - 然而，这确保整个序列能够被划分均匀
- 时间复杂度：$T (N)=O (Nlog⁡N)$

### 7.4 Small Arrays

Problem: 

- Quicksort is **slower** than insertion sort for small $N (\leq 20)$.

Solution: 

- Cutoff when $N$ gets small (e.g. $N=10$) and use other efficient algorithms (such as insertion sort).

### 7.5 Implementation
```c
Void Quicksort (ElementType A[], int N)
{
    Qsort (A, 0, N - 1);
    // A: the array
    // 0: Left index
    // N - 1: Right index
    // Return median of Left, Center, and Right
    // Order these and hide the pivot
}
```

```c
Void Qsort (ElementType A[], int Left, int Right)
{
    Int i, j;
    ElementType Pivot;

    If (Left + Cutoff <= Right) // if the sequence is not too short
    {
        Pivot = Median 3 (A, Left, Right);  // select pivot
        I = Left;                         // (1)
        J = Right - 1;                    // (2)
        For (;;)
        {
            While (A[++i] < Pivot) {}     // scan from left
            While (A[--j] > Pivot) {}     // scan from right
            If (i < j)
                Swap (&A[i], &A[j]);       // adjust partition
            Else break;                   // partition done
        }
        Swap (&A[i], &A[Right - 1]);       // restore pivot
        Qsort (A, Left, i - 1);            // recursively sort left part   
        Qsort (A, i + 1, Right);           // recursively sort right part  
    }  // end if - the sequence subarray
    Else
        InsertionSort (A + Left, Right - Left + 1);
}
```

```c
ElementType Median 3 (ElementType A[], int Left, int Right)
{
    Int Center = (Left + Right) / 2;
    If (A[Left] > A[Center])
        Swap (&A[Left], &A[Center]);
    If (A[Left] > A[Right])
        Swap (&A[Left], &A[Right]);
    If (A[Center] > A[Right])
        Swap (&A[Center], &A[Right]);
    // Invariant: A[Left] <= A[Center] <= A[Right]
    Swap (&A[Center], &A[Right - 1]);
    // only need to sort A[Left + 1] .. A[Right - 2]
    // 因为我们已经知道 A[Left] 比 pivot 小，A[Right] 比 pivot 大
    // 所以回到 Qsort 函数后，我们无需改变 A[Left] 和 A[Right] 的顺序
    Return A[Right - 1]; // Return pivot
}
```

### 7.6 Analysis

$T (N)=T (i)+T (N-i-1)+cN$

* The worst case: $T (N)=T (N-1)+cN \rightarrow T (N)=O (N^2)$
* The best case: $T (N)=2 T (N/2)+cN \rightarrow T (N)=O (NlogN)$
* The average case: Assume the average value of $T (i)$ for any $i$ is $\frac{1}{N}[\sum_{j=0}^{N-1}T (j)]$

    $\rightarrow T (N)=O (NlogN)$

## 8. Sorting Large Structures（Table Sort）

* Problem: Swapping large structures can be very much expensive
* Solution: Add a pointer field to the structure and swap pointers instead - ***indirect pointing***. Physically rearrange the structures at last if it is really necessary.

* 如何输出排好序的列表：`list[table[0]], list[table[1]], ..., list[table[n-1]]`


<div style="text-align: center"><img src="images/image-20250514192913570.png" width="30%"></div>


The worst case: there are $⌊N/2⌋$ cycles and requires $⌊3 N/2⌋$ record moves

* $T=O (mN)$ where $m$ is the size of a structure

## 9. A General Lower Bound for Sorting

***Decision Tree 决策树***

<div style="text-align: center"><img src="images/image-20250514193814214.png" width="40%"></div>


【Theorem】Any algorithm that sorts by comparisons only must have a worst case computing time of $Ω( N \log{N} )$.

## 10. Bucket Sort and Radix Sort
### 10.1 Bucket Sort

```c
Algorithm
{
    Initialize count[];
    While (read in a student's record)
        Insert to list count[stdnt. Grade];
    For (i = 0; i < M; i++)
    {
        If (count[i])
            Output list count[i];
    }
}
```

- $T (N, M)=O (M+N)$

### 10.2 Radix Sort

* When $M>>N$,

<div style="text-align: center"><img src="images/image-20250514194034014.png" width="50%"></div>


Suppose that the record $R_i$ has $r$ keys.  

* $K_i^j :=$ the $j$ -th key of record $R_i$ -
* $K_i^0 :=$ the most significant key of record $R_i$ 
* $K_i^{r-1} :=$ the least significant key of record $R_i$ 
* A list of records $R_0, \ldots, R_{n-1}$ is lexically sorted with respect to the keys $K^0, K^1, \ldots, K^{r-1}$ iff 
 
    $$ (K_i^0, K_i^1, \ldots, K_i^{r-1}) \leq (K_{i+1}^0, K_{i+1}^1, \ldots, K_{i+1}^{r-1}), \quad 0 \leq i < n-1. $$

    That is, $K_i^0 = K_{i+1}^0$, ..., $K_i^l = K_{i+1}^l$, $K_i^{l+1} < K_{i+1}^{l+1}$ for some $l < r-1$.


