# Chap5.Memory Hierarchy
## 5.1 Memory Technologies
- ==SRAM== (Static Random Access Memory)
	- value is stored on a pair of inverting gates
	- very fast but takes up more space than DRAM
	- 断电后会丢失数据，用于CPU 的高速缓存（L1/L2/L3 Cache）
- ==DRAM== (Dynamic Random Access Memory) 
	- Value is stored as a charge on capacitor 
	- Very small but slower than SRAM (factor of 5 to 10) 
	- Must periodically be refreshed 
	- Read contents and write back (destructive read)
	- 多用于内存条，以及图形显存
- ==Flash==
    - NAND Flash：用于 SSD、U 盘、手机存储（高密度、低成本）
    - NOR Flash：用于固件存储（如 BIOS），支持随机访问，但密度低
- ==Disk==
## 5.2 Memory Hierarchy Introduction
Programs access <u>a small proportion</u> of their address space at any time 
- **Temporal locality** 时间局部性 
	- Items accessed recently are likely to be accessed again soon 
- **Spatial locality** 空间局部性 
	- Items near those accessed recently are likely to be accessed soon

Taking advantage of locality
- Memory hierarchy 
- Store everything on disk 
	- 磁盘是最底层的存储设备，容量最大，但访问速度最慢
- Copy recently accessed (and nearby) items from disk to smaller <u>DRAM memory</u> 
	- DRAM 是 **Main memory**，读取速度快，但容量小价格贵
- Copy more recently accessed (and nearby) items from DRAM to smaller SRAM memory 
	- SRAM 是 **CPU 缓存（Cache memory）**，直接连接到 CPU，访问速度极快

> [!info] Memory Hierarchy Levels
> <div text-align="center"><img src="image-114.png" width="75%"></div>

- **Block** (aka **line**): unit of copying  
    数据传输的最小单位（可能有很多个字）
- **Hit**: The CPU accesses the upper level and succeeds
    命中：所访问的数据在上层存在
    - hit ratio: hits/accesses
    - hit time：访问上层存储的时间（包含了判断是 hit 还是 miss 的时间）
- **Miss**: The CPU accesses the upper level and fails
    未命中：所访问的数据不在上层存储中
    - miss penalty：指处理一次 miss 所需的时间开销
	    - 将下层中对应的块替换到上层 + 将该块传送给处理器 所需的时间
    - miss rate：<u>misses/accessed</u> or <u>1 - hit ratio</u>
    - 最后会把 block 加载到上层

<div text-align="center"><img src="image-115.png" width="80%"></div>设计内存层级时，需要考虑的两个重要问题是内存访问**速度**(speed) 以及内存空间**大小**(size)，因此我们有了**高速缓存**(cache) 和**虚拟内存**(virtual memory) 的概念。

---
## 5.3 The basics of Cache
- For each item of data at the lower level, there is exactly one location in the cache where it might be.
	- lots of items at the lower level **share locations** in the upper level
### 1. Direct Mapped Cache
<div text-align="center"><img src="image-116.png" width="80%"></div>
- Direct-mapping algorithm：
$$\text{(Block address) modulo (Number of blocks in the cache)}$$
- Store block address as well as the data 
	我们需要知道 cache 放的是哪个块
    - Actually, only need the <u>high-order bits</u>
    - Called the **tag**
- Valid bit: 1 = present, 0 = not present  
    我们需要知道 cache 里是否有放有效的块
<div text-align="center"><img src="image-117.png" width="70%"></div>
- Tag：用于标识该块来自主存的哪个区域 (from where)
- Index：确定该数据应存放在缓存中的哪一行 (to where)
- Byte Offset：在缓存块内定位具体字节
> [!example]-
> <div text-align="center"><img src="image-118.png" width="60%"></div>
> ---
> <div text-align="center"><img src="image-119.png" width="60%"></div>
> ---
> <div text-align="center"><img src="image-120.png" width="60%"></div>
> ---
> <div text-align="center"><img src="image-121.png" width="60%"></div>

### 2. Direct Mapped Cache Construction
<div text-align="center"><img src="image-122.png" width="70%"></div>

- tag 位宽由总的地址位宽减掉其他位决定
$$
\text{tag bits}= \text{address bits}-(\text{index bits}+\text{block offset bits}+\text{byte offset bits})
$$
	- Index 位宽由 cache size / num of blocks  决定
		- 如果缓存共有 $2^n$ 行 (对应 $2^n$ 个 block) $\rightarrow$ Index 需要 $n$ 位
	- Block offset 位宽由一个 block 中 word 的个数决定
		- 如果 $1$ 个 block 有 $B$ 个 word，则 block offset 需要 $\log_2{B}$ 位
	- Byte offset 位宽由 word 的位数决定
		- 如果 word size 为 $B$ byte，则 byte offset 需要 $\log_2{B}$ 位

> [!example] Bits in Cache
> How many total bits are required for a direct-mapped cache 16KB of data and 4-word blocks, assuming a 32-bit address?
> <div text-align="center"><img src="image-123.png" width="80%"></div>
> 
> - 每个 block 包含：
> 	- Data: 128 bits
> 	- Tag: 18 bits
> 	- Valid bit: 1 bit

> [!example] Mapping an Address to Multiword Cache Block
> <div text-align="center"><img src="image-124.png" width="85%"></div>
> 
> - 字节地址 1200 属于第 75 号内存块（block），映射到缓存中的第 11 号块

### 3. Handling Cache reads hit and Misses
- Read hits
- Read misses—two kinds of misses
    - data cache miss
    - instruction cache miss  
        Stall the CPU, fetch block from memory, deliver to cache, restart CPU read  
        1. Send the original PC value (current PC-4) to the memory.  
	        - 因为 PC 取值完就变成 +4 了，所以当前执行的其实是 PC-4 
        2. Instruct main memory to perform a read and wait for the memory to complete its access.  
        3. Write the cache entry, putting the data from memory in the data portion of the entry, writing the upper bits of the address (from the ALU) into the tag field, and turning the valid bit on.  
			- 此时，该指令已成功载入缓存
        4. Restart the instruction execution at the first step, which will refetch the instruction again, this time finding it in the cache.
- Write hits
    - **write-back**: Cause Inconsistent  
        仅将数据写入缓存，不立即写入主内存；
        等待后续（如该缓存块被替换出去时），再把数据写回主内存
    - **write-through**: Ensuring Consistent  
        既把数据写到 cache 中又写到内存中 
        Slower! -- write buffer
- Write misses  
    read the entire block into the cache, then write the word

> [!info] 衡量失效的 3C 模型
> - **强制失效**(compulsory misses)（或称为冷启动失效 (cold-start misses)）：首次访问不存在于高速缓存的数据块（**初始化**时高速缓存为空，自然就失效了）
> - **容量失效**(capacity misses)：在**全相联**的置放方案中，高速缓存无法保存所有数据块，因此可能出现检索已被替代的高速缓存块的情况
> - **冲突失效**(conflict/collision misses)：在**组相联**与**直接映射**的置放方案中，可能会遇到多个块在同一个集内竞争的情况
>   
>   <div text-align="center"><img src="image-197.png" width="70%"></div>
>   
>   Solution
><div text-align="center"><img src="image-198.png" width="90%"></div>


### 4. Deep concept in Cache
- Q1: Where can a block be placed in the upper level? (Block placement)
- Q2: How is a block found if it is in the upper level? (Block identification)
- Q3: Which block should be replaced on a miss? (Block replacement)
- Q4: What happens on a write? (Write strategy)
#### Q1: Block Placement
**Direct mapped** 
- Block can only go in <u>one place</u> in the cache 
	- Usually address MOD Number of blocks in cache 
**Fully associative** 全相联映射
- Block can go <u>anywhere</u> in cache. 
**Set associative** 组相联映射
- Block can go in one of <u>a set of places</u> in the cache. 
- A set is a group of blocks in the cache. Block address MOD Number of sets in the cache 
- If sets have $n$ blocks, the cache is said to be <u>n-way set associative</u>.
> [!note]
> Direct mapped is the same as 1-way set associative, and fully associative is m-way set-associative (for a cache with m blocks).
><div text-align="center"><img src="image-125.png" width="80%"></div>

#### Q2: Block Identification
##### Tag
- Every block has an <u>address tag</u> that stores the main memory address of the data stored in the block.
	tag 存储了该块所对应的数据在主内存中的**起始地址的高位部分**
- When checking the cache, the processor will compare the requested memory address to the cache tag -- if the two are equal, then there is a <u>cache hit</u> and the data is present in the cache 
##### Valid bit 
- Often, each cache block also has a <u>valid bit</u> that tells if the contents of the cache block are valid

##### The Format of the Physical Address
The **Index** field selects 
- The set, in case of a set-associative cache 
- The block, in case of a direct-mapped cache 
- Has as many bits as $\log_2{ (\text{sets}) }$ for set-associative caches, or $\log_2{ (\text{blocks}) }$ for direct-mapped caches 
The **Byte Offset** field selects 
- The byte within the block 
- Has as many bits as $\log_2(\text{size of block})$
The **Tag** is used to find the matching block within a set or in the cache 
- Has as many bits as `Address_size – Index_size – Byte_Offset_Size `
<div text-align="center"><img src="image-126.png" width="80%"></div>

> [!example]-
> <div text-align="center"><img src="image-127.png" width="80%"></div>
> 
> <div text-align="center"><img src="image-128.png" width="80%"></div>
> 
> <div text-align="center"><img src="image-128.png" width="80%"></div>
> 
>  <div text-align="center"><img src="image-131.png" width="80%"></div>

#### Q3: Block Replacement
- In a direct-mapped cache, there is **only one block** that can be replaced 
- In set-associative and fully-associative caches, there are **N blocks** (where N is the degree of associativity)
##### Strategy of Block Replacement
Several different replacement policies can be used 
- **Random replacement** - randomly pick any block 
	- Easy to implement in hardware, just requires a random number generator 
	- Spreads allocation uniformly across cache 
	- May evict a block that is about to be accessed 
- **Least-recently used (LRU)** - pick the block in the set which was least recently accessed 
	- Assumed more recently accessed blocks more likely to be referenced again 
	- This requires <u>extra bits</u> in the cache to keep track of accesses. 
- **First in,first out(FIFO)** - Choose a block from the set which was first came into the cache

#### Q4: Write Strategy
When data is written into the cache (on a store), is the data also written to main memory? 
- If the data is written to memory, the cache is called a ==write-through== cache
	- Can always discard cached data 
		- most up-to-date data is in **memory** 
	- Cache control bit: only a *valid bit* 
	- memory (or other processors) always have latest data 
- If the data is NOT written to memory, the cache is called a ==write-back== cache 
	- Can’t just discard cached data 
		- may have to write it back to memory 
	- Cache control bits: both *valid and dirty bits* 
		- **Valid bit**：表示数据是否有效
		- **Dirty bit**：表示数据是否被修改（若为 1，则写回时必须更新主内存）
	- much lower bandwidth, since data often overwritten multiple times p
- Write-through: 
	- Read misses don't result in writes, memory hierarchy is consistent and it is simple to implement. 
- Write-back: 
	- Writes occur at speed of cache and main memory bandwidth is smaller when multiple writes occur to the same block.
##### Write stall 
- When the CPU must wait for writes to complete during <u>write through</u>
##### Write buffers 
- A small cache that can hold a few values waiting to go to main memory. 
- To avoid stalling on writes, many CPUs use a write buffer. 
	- 当 CPU 执行写操作时：
		1. 数据先写入 **write buffer**
		2. CPU 立即继续执行下一条指令（无需等待）
		3. 后台由专门的硬件将 buffer 中的数据逐个写入主内存。
<div text-align="center"><img src="image-132.png" width="60%"></div>
- This buffer helps when writes are clustered. 
- It does not entirely eliminate stalls since it is possible for the buffer to fill if the burst is larger than the buffer.
##### Write misses 
If a miss occurs on a write (the block is not present), there are two options. 
- **Write allocate** 
	- The block is loaded into the cache on a miss before anything else occurs. 
- **Write around** (no write allocate) 
	- The block is only written to main memory 
	- It is not stored in the cache.
In general, <u>write-back caches use write-allocate</u>, and <u>write-through caches use write-around</u> .

> [!info] Larger Blocks Exploit Spatial Locality
> <div text-align="center"><img src="image-133.png" width="80%"></div>

### 5. Designing the Memory system to Support Cache
#### Performance basic memory organization
<div text-align="center"><img src="image-134.png" width="80%"></div>
现代 DRAM 支持“突发传输”（burst mode）
- 一旦地址被发送，可以连续传输多个字，无需重复发送地址。

#### Performance in Wider Main Memory
<div text-align="center"><img src="image-135.png" width="80%"></div>

#### Performance in Four-way interleaved memory
<div text-align="center"><img src="image-136.png" width="80%"></div>

## 5.4 Measuring and improving cache performance
- How to measure cache performance?
- How to improve performance?
    - Reducing cache misses by more flexible placement of blocks
    - Reducing the miss penalty using multilevel caches
$$
\begin{align}
\text{Average Memory Assess Time(AMAT)}&=\text{hit time}+\text{miss time}\\
&=\text{hit time}+\text{miss rate}\times\text{miss penalty}
\end{align}
$$
### 1. Measuring cache performance
CPU 运行时间计算：
$$
\text{CPU time} = \text{CPU execution clock cycles} + \text{Memory-stall clock cycles}
$$
其中，
$$
\begin{align}
\text{Memory-stall clock cycles} &= \text{instructions}\times \text{miss ratio}\times \text{miss penalty} \\ &= \text{Read-stall cycles} + \text{Write-stall cycles}
\end{align}
$$
- For Read-stall
    包括取指和数据加载
$$
\text{Read-stall cycles}=\frac{\text{Read}}{\text{Program}}\times\text{Read miss rate}\times \text{Read miss penalty}
$$
- For a write-through plus write buffer scheme   $$
    \begin{align}
\text{Write-stall cycles}=&( \frac{\text{Write}}{\text{Program}}\times \text{Write miss rate} \times \text{Write miss penalty}) \\ &+ \text{Write buffer stalls}
\end{align}
$$
- If the write buffer stalls are small, we can safely ignore them.  
	一般来说 buffer 不会溢出
- If the cache block size is one word, the write miss penalty is 0.  
    大小是一个 word, 替换出去就直接写了
把读写结合起来：
- In most write-through cache organizations, the read and write miss penalties are the same (question?) 
	- If we neglect the write buffer stalls, we get the following equation: 
$$
\text{Memory-stall clock cycles} ＝ \frac{\text{Memory accesses}}{\text{Program}}\times \text{Miss rate}\times \text{Miss penalty}
$$
	Or
$$
\text{Memory-stall clock cycles} ＝ \frac{\text{Instructions}}{\text{Program}}\times \frac{\text{Misses}}{\text{Instructions}}\times \text{Miss penalty}
$$
> [!example]- Calculating Cache Performance
> <div text-align="center"><img src="image-137.png" width="80%"></div>
> 可见内存导致了性能瓶颈
> <div text-align="center"><img src="image-138.png" width="80%"></div>
> 加快时钟频率可以提高性能
> <div text-align="center"><img src="image-139.png" width="80%"></div>
### 2. Improving
#### 1. Reducing cache misses by more flexible placement of blocks
> [!info]- The disadvantage of a direct-mapped cache
> <div text-align="center"><img src="image-140.png" width="80%"></div>

An eight-block cache configured as variety-way
<div text-align="center"><img src="image-141.png" width="65%"></div>
- A **set-associative** cache is divided into some sets. A set contains several blocks.
	- If a set has only <u>one block</u>, this set-associative cache is actually a **direct-mapped** cache. 
	- If a set-associative cache has only <u>one set</u>, this set-associative cache is called a **fully-associative** cache.
> [!example]- Miss rate versus set-associativity — 8 Blocks
> <div text-align="center"><img src="image-142.png" width="80%"></div>
> 
> - set-associated cache 
> 
> <div text-align="center"><img src="image-143.png" width="80%"></div>
> 
> - 最终结果，可见 data miss rate 逐渐下降
>  <div text-align="center"><img src="image-144.png" width="80%"></div>

**Locating a block in the set-associative cache**
<div text-align="center"><img src="image-145.png" width="80%"></div>
- 根据 index 读取四个 set 中对应的 block
- 读取 tag 和 data，并合需要访问的 tag 和 data 比较
- 通过 4-1 mux 选择指定的 cache，并返回 hit / miss

> [!example]- Size of tags versus set associativity
> 注意 block addr 是忽略了地位的 byte offset 的
> <div text-align="center"><img src="image-146.png" width="80%"></div>
> 
> <div text-align="center"><img src="image-147.png" width="80%"></div>

**Choose which block to replace**
- The most commonly used scheme is ==least recently used (LRU)==. 
	- In an LRU scheme, the block replaced is the one that has been unused for the longest time. 
- For a two-way set associative cache, the LRU can be implemented easily.
	- We could keep **a single bit** in each set. 
	- set the bit whenever a specific block in the set is referenced, and reset the bit whenever another block is referenced. 
- As associativity increases, implementing LRU gets harder.

#### 2. Decreasing miss penalty with multilevel caches
Add a second level cache: 
- often primary cache is on the same chip as the processor 
- use SRAMs to add another cache above primary memory (DRAM) 
- miss penalty goes down if data is in 2nd level cache 

利用==多级缓存==可以有效提高 CPU 速度
> [!example]
> <div text-align="center"><img src="image-148.png" width="85%"></div>
> <div text-align="center"><img src="image-150.png" width="85%"></div>

Using multilevel caches（整体优化思路）: 
- try and optimize the **hit time** on the 1st level cache 
- try and optimize the **miss rate** on the 2nd level cache

<div text-align="center"><img src="image-151.png" width="90%"></div>

## 5.7 Virtual Memory
> Main Memory act as a “Cache” for the secondary storage. 
> **主存（RAM）** 是 **辅助存储（如硬盘、SSD）** 的“缓存”
- Motivation: 
	- Efficient and safe sharing of memory among multiple programs. 
		不同程序有自己的内存空间，我们希望只考虑自己的空间，不在乎其他程序放在哪里。让进程认为是自己独有这块地址空间
	- Remove the programming burdens of a small, limited amount of main memory. 

**Translation of a program’s address space to physical address**
<div text-align="center"><img src="image-152.png" width="85%"></div>

### 1. Pages：virtual memory blocks
虚拟页的数量比物理页多（现在不一定）
**Page faults**: 数据不在 memory 中，去 disk 中获取
- miss penalty 很大, 因此 page 通常设置的很大
- reducing page faults is important (LRU is worth the price) 
- can handle the faults in software instead of hardware 
- using write-through is too expensive so we use **write back**
<div text-align="center"><img src="image-153.png" width="70%"></div>
### 2. Page Tables
1. Page Table : Virtual to physical address 
	页表的作用：将程序使用的虚拟地址映射为实际的物理地址
2. Stored into the memory, indexed by the virtual page number 
	页表本身存储在**物理内存**中，以“虚拟页号”作为索引
3. Each Entry in the table contains the <u>physical page number</u> for that virtual pages if the page is current in memory 
	- 有效位（Valid bit）：表示该虚拟页是否当前在物理内存中
		- 1：页面在内存中，可以使用
		- 0：页面不在内存中，可能在磁盘上
4. <u>Page table, Program counter and the page table register</u>, specifies the state of the program. Each process has one page table. (Process switch? )
	- 每个进程有一个独立的页表：不同进程的虚拟地址空间相互隔离，互不干扰
	- 页表寄存器（Page Table Register）：保存当前运行进程的页表基地址。当发生 Process Switch 时，操作系统会更新这个寄存器指向新进程的页表
	- 程序计数器（Program Counter）：指示当前执行指令的位置（也是虚拟地址），配合页表完成地址转换
<div text-align="center"><img src="image-154.png" width="75%"></div>
Each program has its own page table
- Virtual memory systems use **fully associative mapping** method
<div text-align="center"><img src="image-155.png" width="85%"></div>

### 3. Page Faults
When the OS creates a process, it usually creates the space on disk for **all the pages** of a process.
- When a page fault occurs, the OS will be given control through exception mechanism.
- The OS will find the page in the disk by the page table.
- Next, the OS will bring the requested page into main memory. 
	- If all the pages in main memory are in use, the OS will use **LRU strategy** to choose a page to replace

### 4. How Large is a Page Table?
<div text-align="center"><img src="image-160.png" width="75%"></div>
### 5. Making Address Translation Fast--
- The  (Translation-lookaside Buffer) acts as **Cache** on the page table
- 虚拟地址，先在 TLB 找，找不到再去内存里的页表找
<div text-align="center"><img src="image-157.png" width="75%"></div>

> [!note] FastMATH Memory Hierarchy
> 一种更高效的访问结构
> <div text-align="center"><img src="image-158.png" width="75%"></div>

> [!note] 流程图
> **TLBs and Caches**
> <div text-align="center"><img src="image-159.png" width="80%"></div>

