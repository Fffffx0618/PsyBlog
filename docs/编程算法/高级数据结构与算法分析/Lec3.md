# Inverted File Index
---
## 3.1 Concept
> 搜索引擎是如何根据搜索框内输入的内容来找到符合要求的网页呢？
> - 建立==词汇-文档关联矩阵 (term-document incidence matrix)==

**Definition**：
- ==索引（Index）==是一种用于在文本中定位特定术语的机制
- ==倒排文件（Inverted file）==包含一系列指针（例如页面编号），指向该术语在文本中所有出现的位置

> [!Note]
> 假设现在有一份文档集
> - 可以将所有词汇整理为一张词汇-文档关联表【又称==倒排索引(inverted file index)==】：
> 
> <div style="text-align: center"><img src="image-8.png" width="90%"></div>
> 
> 关于表格的后两列信息：
> - 前者被称为**词典**(term dictionary)，收集文档中出现过的所有词汇
> - 后者被称为**倒排列表**(posting list)，记录了每个词汇的出现次数（或**频率**）以及出现**位置**（哪个文档；文档中的具体位置）
>     - 对于一个包含**多个关键词**的搜索语句，搜索引擎**优先搜索出现次数最少的网页**，这样可以提升搜索速度

一个简单的索引生成器（Index Generator）：
```c
while (read a document D) {
    while (read a term T in D) {
        if (Find(Dictionary, T) == false) 
            Insert(Dictionary, T);
        Get T's posting list;
        Insert a node to T's posting list;
    }
}
Write the inverted index to disk;
```

以下是搜索引擎的几个重要模块 (module)：
- 词元分析器 (token analyzer)、停用词过滤器 (stop filter) 
- 词汇扫描器 (vocabulary scanner)
- 词汇插入器 (vocabulary insertor) 
- 内存管理系统 (memeory management)

---
## 3.2 Modules
### 1. Word Stemming

> Process a word so that only its stem or root form is left.

<div style="text-align: center">
    <img src="images/lec3/5.png" width="80%">
    </div>

- 合并形式各异但词干相同的词汇&合并某个单词的错误拼写
### 2. Stop Words
有些词汇过于常见，如"a" "the" "it"（这些词被称为**停用词**(stop words)），因为它们通常不具备特殊的含义，因此可以预先将它们从原始文本中去掉，然后再进行倒序索引的匹配。
### 3. Term Access
通常使用以下数据结构来存储倒排索引：
- **Search Trees**（B+树、字典树(Tries)等）
- **Hashing**
    - 优点：查找单个词汇的速度非常快（$O(1)$）
    - 缺点：查找多个词汇的速度较慢
	    - 多个词汇在 Hashing的位置是不确定的
	    - Search Trees可能会按联系程度的紧密来确定这些词汇的相对位置
### 4. Memory Management
- 将填满的内存放入磁盘的一个存储块内，然后释放内存
> [!伪代码实现]
> ```c
> BlockCnt = 0;
> while (read a document D) {
>     while (read a term T in D) {
>          if (out of memory) {
>             Write BlockIndex[BlockCnt] to disk;
>             BlockCnt++;
>             FreeMemory;
>         }
> 
>         if (Find(Dictionary, T) == false) 
>             Insert(Dictionary, T);
>         Get T's posting list;
>         Insert a node to T's posting list;
>     }
> }
> ```

---
## 3.3 Techniques
### 1. Distributed Indexing
通常会将倒排索引放在多台计算机内，他们合称为**集群**(cluster)，其中的一台计算机被称为**节点**(node)，每个节点会存储所有倒排索引的一个子集。

- 法1：按**词汇**划分索引
<div style="text-align: center">
<img src="images/lec3/6.png" width="60%">
</div>
- 法2：按**文档**划分索引 (*更常用*)
<div style="text-align: center">
<img src="images/lec3/7.png" width="60%">
</div>
### 2. Dynamic Indexing
**Problem**:
- Docs come in over time
- Docs get deleted

**Solution**：
<div style="text-align: center">
<img src="images/lec3/8.png" width="70%">
</div>

- 原来存储索引的地方为**主索引**(main index)
- 新增一个**辅助索引**(auxiliary index), 用于存储的少量索引（可理解为cache）
- 新插入文档的索引会暂时存放在辅助索引内
- 搜索时，搜索引擎会同时在主索引和辅助索引内查找对应的索引，查找辅助索引的速度更快一些
- 在适当的时候合并归档，随后清空辅助索引，继续用于存放新插入的文档
### 3. Compression
-  先去除 Stop Words
-  然后将所有的词汇放在同一个存储块内，词汇之间没有任何间隔
- 为了区分词汇，还需要另一张表来记录每个词汇的**开头的位置**
- 这样可以将一个很大的数组压缩成两张相对较小的表

Example:
![[image-9.png|580x264]]
    
- 关于索引
    - 如果有大量的文档，索引值可能会非常大，甚至无法直接表示
    - 此时可以记录某个词汇所在的两个最近的文档的间距，即基于绝对序号的**差分(difference)序列**。根据实际经验，大多数的间距值不会超过20 bit
### 4. Threshold
- **Document**：只检索根据权重排名前x个文档
    - 对于 **Boolean queries 布尔查询**，可能会错过一些有意义的文档
    - 比如 `Computer & Science`，搜索引擎只会搜与这两者交集相关的文档，可能会忽略与 `Computer` 相关或与 `Science` 相关的文档
- **Query**：将查询中的词汇按它们出现的频率升序排序
    - 只会根据出现频率相对较少的词汇搜索（在倒排索引中，词汇对应的倒排列表的长度越长，蕴含的意义可能更少）
    - 根据实际情况确定阈值的大小：如果对于不同的阈值，搜索的准确度差不多，那么就取较小的阈值，否则取更大的阈值
    <div style="text-align: center">
    <img src="images/lec3/11.png" width="80%">
    </div>
## 3.4 Measurement
可以从以下角度来衡量搜索引擎的性能：

- 排索引的速度：每小时处理的文档数
- 搜索的速度
    - 时延(latency)：等待搜索结果出现的时间
    - 将时延看作关于索引大小的一个函数，在此基础上做比较
- 查询语句的可表达性(expressiveness)
	- 即能够表达复杂信息的能力
	- 比较搜索引擎在这类复杂查询下的搜索速度
- 用户满意度：
    - **数据**检索性能评估(data retrieval performance evaluation)
	    - 响应时间、索引占用空间等指标
    - **信息**检索性能评估(information retrieval performance evaluation)
	    - 回答的相关程度等

*Relevance* measurement requires 3 elements:
 - A benchmark **document collection（文档集）**
 - A benchmark **suite of queries（查询语句）**
 - A **binary assessment** of either Relevant or Irrelevant for each query-doc pair
其中，<u>对于查询-文档对的二维的相关性评估表</u>如下图所示：
 <div style="text-align: center">
 <img src="images/lec3/12.png" width="80%">
    </div>

- **Precision**：所有检索到的文档中，有多少是有意义的（考虑表格第一行）
    - $P = \dfrac{R_R}{R_R + I_R}$
- **Recall**：所有有意义的文档中，有多少是被检索到的（考虑表格第一列）
    - $R = \dfrac{R_R}{R_R + R_N}$

 理想情况是同时具备较高的精确度和召回率，但实际应用中可能无法同时兼顾两者，需要做好权衡


