# External Sorting
## 15.1 Introduction
==Internal Sorting==: 在**主存 (main memory)** 运行的内部排序
- 运行的前提条件：主存能够容纳**所有**待排序的数据
==External Sorting==：使用**磁盘**空间和**主存**进行的外部排序
- 排序的适用情景：数据量很大，主存**无法容下**所有待排序数据

访问数组的某个元素 `a[i]` 所需的时间：
- 主存：$O(1)$（用索引寻找，随机访问）
- 磁盘：找到元素所在的迹(track) -> 找到对应的区(sector) -> 找到 `a[i]` 并传输数据
    - 这一过程的快慢取决于设备的性能
    - 要想提升访问速度，应尽可能让磁盘读写头沿同一方向移动，以避免磁盘频繁的旋转

**Definition**
- 存储数据的容器称为**磁带**(tape)，里面的元素只能顺序访问（符合磁盘读写头的特性）
- 至少需要使用 3 个磁带（ 2 个子序列合并成 1 个更大的序列）
- 在主存中排好序的一组数据块称为**顺串**(run)
- **趟**(pass)：在归并排序中指的是对所有数据进行一趟遍历、排序、合并的过程

> [!question]
> 假设主存一次最多只能处理 $M = 3$ 条记录，请通过外部排序算法（归并排序）来实现对以下序列的排序：
> <div style="text-align: center"><img src="images/lec15/1.png" width="70%"></div> 

> [!info] Answer
> Pass 1
> - 将原序列分为 3 条记录一组，每组分别进行排序（排序算法任意）
> - 为了将小的顺串合并成一个大的顺串，这里规定相邻的两个顺串放在不同的磁带内
> 
> Pass 2
> - 开始<u>合并 + 排序</u>，注意还是要放在两个不同的磁带里（可以利用原有的空闲磁带） 
> 
> Pass 3
> - 进一步的<u>合并 + 排序</u>，离排序完成仅差一步
> <div style="text-align: center"><img src="image-13.png" width="80%"></div> 

**结论**：若要对 $N$ 条记录进行外部排序，且主存最多对 $M$ 条记录进行排序，那么需要的**趟数**(number of passes)为 $1 + \lceil \log_2 \dfrac{N}{M}\rceil$

---
## 15.2 Pass Reduction
### 1. k-way Merge
通过增大对数函数的底数 $k$ 来减少趟数，也就是**增加子序列的个数**
> [!example]
> <div style="text-align: center"><img src="image-14.png" width="80%"></div> 
> 
> Pass 1
> - 由于多出一路子序列，所以需要更多的磁带（下面还会用到其他额外的磁带）
> 
> Pass 2
> 
> - 由于需要同时比较三个数据，这里用到了**最小堆**，便于随时取出最小的数据，并加快比较速度；剩余部分的合并与之类似，故不再展示其详细过程。
> - 本例中，第3个子序列为空，但为了一般性的解释，为第3个子序列预留了一个磁带。

> [!abstract] 总结
> - 时间复杂度：
> 	- 不用最小堆（也就是对k个子序列进行顺序比较）：$O(kN \log_k N)$
> 	- 解释：关键点在于系数 $k$（其他部分应该比较好理解），因为单次比较所需时间为 $O(k)$，这是不可忽视的一个参数，需要算在时间复杂度内
> 	- $k$ 不是越大越好，因为当 $k \rightarrow N$ 时，时间复杂度退化为 $\rightarrow O(N^2)$
> - 使用最小堆：$O(N \log_2 N)$
> 	- 解释：比较所需的时间降至 $\log k$，因此时间复杂度为 $O(\log k N \log_k N) = O(\log k N \dfrac{\log N}{\log k}) = O(N \log N)$
> 	- 所以堆的大小不影响时间复杂度
> 	- 但即便如此，$k$ 也不是越大越好，因为 $k$ 的增大会增加I/O时间
> - 趟数降至 $1 + \lceil \log_k \dfrac{N}{M} \rceil$
> - 但所需的磁带数升至$2k$个，因此这种改进方法不太令人满意

### 2. Polyphase Merge
我们希望在降低趟数的同时能够尽可能避免磁带数的提升，因此尝试在保持子序列个数不变的情况下减少所需磁带数，下面以 $k=2$，磁带数 $= 3$ 为例进行分析：
> [!example]
> 已知 $k=2$，磁带数=3，且原序列的情况如下：
> 
> <div style="text-align: center"><img src="images/lec15/8.png" width="50%"></div>
> 
> - 34 runs 意味着原序列由34组内部已排好序的子序列构成
> 
> Pass 1
> 
> <div style="text-align: center"><img src="images/lec15/9.png" width="50%"></div>  
> 
> - 将 34 个顺串均分为包含 17 个顺串的两个子序列，然后进行合并，形成一个 17 个顺串的完整序列，此时每个顺串会包含更多排好序的记录。
> 
> Copy 1
> <div style="text-align: center"><img src="images/lec15/10.png" width="50%"></div>
> 
> - 为了继续合并，需要将所有的顺串一分为二。在进入下一趟操作前，将 $T_1$ 的一半顺串拷贝到另一个空磁带 $T_2$ 上。
> 
> - 磁盘拷贝所需的成本有些大，如果这样简单地减少磁带数量，可能会带来更大的成本损耗

**多相合并**(polymerge sort)：在起始步的时候，对原序列进行**不均等的分割**，形成大小不一的子序列
- 可以确保在每一趟结束后，（除了最后阶段外）始终会有多个包含记录的子序列，无需额外高昂的拷贝操作
> [!example]
> Split
> <div style="text-align: center"><img src="images/lec15/11.png" width="60%"></div>
>   
> 现将原序列划分为大小不一的两个子序列（34 -> 21 + 13）
> 
> Pass 1
> <div style="text-align: center"><img src="images/lec15/12.png" width="60%"></div>  
> 
> 合并两个子序列后，还会剩下两个子序列，
> - 其中一个是刚合并好的结果序列，其数量为原来**更小的子序列**的顺串的数量
> - 另一个是剩下未进行合并的子序列
>   
> Pass 2
> <div style="text-align: center"><img src="images/lec15/13.png" width="60%"></div>  
> 
> Pass 3
> <div style="text-align: center"><img src="images/lec15/14.png" width="60%"></div>  
> 
> Pass 4
> <div style="text-align: center"><img src="images/lec15/15.png" width="60%"></div>  
> 
> Pass 5
> <div style="text-align: center"><img src="images/lec15/16.png" width="60%"></div>  
> 
> Pass 6
> <div style="text-align: center">
> <img src="images/lec15/17.png" width="60%"></div>  
> 
> Pass 7
> <div style="text-align: center"><img src="images/lec15/18.png" width="60%"></div>  

如何分割才能得到以上效果？
- Claim：对于**两路归并排序**，如果序列中顺串的数量是一个**斐波那契数**$F_N$，那么最好的分割情况是将它分成 $F_{N-1}$ 和 $F_{N-2}$ 个顺串。
    - 如果初始顺串的数量不是一个斐波那契数，只需找到最接近该数的斐波那契数，然后按照该数的递推式将其分成两个子序列
- Claim：对于 $k$ 路归并排序，$F_N^{(k)} = F_{N-1}^{(k)} + \dots + F_{N-k}^{(k)}$，其中 $F_N^{(k)} = 0(0 \le N \le k - 2), F_{k-1}^{(k)} = 1$
    - 对于 $k$ 路归并排序，只需要 $k+1$ 个磁带
    - 可能很难将顺串的数量划分为多个斐波那契数，但应确保有尽可能多的斐波那契数
> [!tip]
> 这个序列 $F_N^{(k)}$ 是一个**k阶斐波那契数列**
> - 它的递推关系是：每一项等于前 $k$ 项之和。
> - 初始条件为：
>   - 当 $N < k-1$ 时，$F_N^{(k)} = 0$
>   - $F_{k-1}^{(k)} = 1$
>   - 之后按递推计算
> 
> **例子**：若 $k=3$，则：
> - $F_0^{(3)} = F_1^{(3)} = 0$
> - $F_2^{(3)} = 1$
> - $F_3^{(3)} = F_2^{(3)} + F_1^{(3)} + F_0^{(3)} = 1+0+0 = 1$
> - $F_4^{(3)} = F_3^{(3)} + F_2^{(3)} + F_1^{(3)} = 1+1+0 = 2$
> - $F_5^{(3)} = F_4^{(3)} + F_3^{(3)} + F_2^{(3)} = 2+1+1 = 4$

### 3. Replacement Selection
**置换选择**(replacement selection)：通过生成**更长的顺串**来减小趟数
> [!question] 
> 请基于下面给出的原序列生成较长的顺串：
> <div style="text-align: center"><img src="images/lec15/24.png" width="60%"></div>  

**Step 1**
<div style="text-align: center"><img src="images/lec15/25.png" width="50%"></div>  
- 借助**最小堆**（大小为3）来生成顺串。先取出堆中最小的元素出来，作为第一个顺串的元素。
**Step 2**
<div style="text-align: center"><img src="images/lec15/26.png" width="50%"></div>  
每次从堆中删除元素时，需要比较这个被删除的元素与下一个进入堆的元素：
- 如果前者更小，说明后者将会与前者处于同一个顺串内（本阶段符合这一情况）
- 否则的话，后者要放在与前者不同的顺串内，且它不会参与堆排序
**Step 3**
<div style="text-align: center">
<img src="images/lec15/27.png" width="50%">
</div>
- 特殊情况：12 < 81，因此12要放入新的顺串内，且它目前不会参与堆排序
**Step 4**
<div style="text-align: center">
<img src="images/lec15/28.png" width="50%">
</div>  
- 还是特殊的情况
**Step 4.5**
<div style="text-align: center">
<img src="images/lec15/29.png" width="20%">
</div>  
第一个顺串内的所有元素都从堆中出来了，此时堆中剩下的元素将会进入下一个顺串
**Step 5**
<div style="text-align: center">
<img src="images/lec15/30.png" width="50%">
</div>  
**Step 6~n-1**
<div style="text-align: center"><img src="images/lec15/31.gif" width="50%"></div>  
**Step n**
<div style="text-align: center"><img src="images/lec15/32.png" width="50%"></div>  
- 由于最后读进去的15比当时被删除的堆元素小，因此它会被放入第3个顺串内。

> [!info] 结论
> - 用这种算法生成得到的顺串的**平均长度**$L_{\text{avg}} = 2M$
> - 当序列的数据处于接近排好序的状态时，这种算法的表现就很不错

## 15.3 Buffer Handling
How to handle the buffers for parallel opetation?
> [! Question]
> 对一个包含3250份记录的文件排序，限制条件为：
> - 用于排序的计算机的主存最多能容纳750份记录
> - 单个的输入文件是一个包含250份记录的记录块
>   <div style="text-align: center"><img src="images/lec15/19.png" width="60%"></div>  

- 首先，将主存划分为**输入缓存**和**输出缓存**两个部分（此时内部排序应为归并排序）
<div style="text-align: center"><img src="images/lec15/20.png" width="55%"></div>  
- 然后从两个子序列中分别读出一个记录块到输入缓存中，开始进行内部排序。
<div style="text-align: center"><img src="images/lec15/21.png" width="55%"></div>  
- 对于输入缓存的记录，我们需要逐条记录地进行比较和排序。
<div style="text-align: center"><img src="images/lec15/22.gif" width="50%"></div>  
- 由于输出缓存的空间有限，所以排序还未结束时，输出缓存的空间就会满。因此需要先暂停排序，将输出缓存排好序的部分记录块丢给空闲的磁带，然后清空缓存
<div style="text-align: center"><img src="images/lec15/23.png" width="60%"></div>  

### Parallel Handling
- 修改**输出缓存**：
    - 将输出缓存**一分为二**：当其中一个输出缓存爆满，需要清空时，另一个闲置的输出缓存可以接替后续的排序任务，即两个输出缓存轮流保存排序结果，确保排序不间断进行
- 修改**输入缓存**：
    - 对于 $k$ 路归并排序，将输入缓存划分为 $2k$ 个子空间：其中 $k$ 个子空间用于容纳正在进行排序的记录，而另外 $k$ 个子空间用于读取子序列的记录块
$$k \uparrow\  \Rightarrow \text{number of input buffers} \uparrow\ \Rightarrow \text{buffer size} \downarrow\ \Rightarrow \text{block size on disk} \downarrow\ \Rightarrow \text{seek time} \uparrow$$（即I/O时间的增加），这种划分方法对于更大的 $k$ 而言效果可能不是特别好。为了取得最佳效果，我们需要综合磁盘参数和用于缓存的主存空间容量来选择合适的 $k$ 值。

## 15.4 Minimizing the Merge Time
适用哈夫曼树（Huffman Tree）来缩短合并的时间
> [!example]
> **题目**：假设我们有4个顺串，长度分别为2, 4, 5, 15。请计算最小的合并时长
> 
> **分析**：
> <div style="text-align: center"><img src="images/lec15/33.png" width="40%"></div> 
> 
> 最小时间 = $2 * 3 + 4 * 3 + 5 * 2 + 15 * 1 = 43$

结论：最小合并时间 = $O(\text{the weighted external path length})$（哈夫曼树的带权路径和）