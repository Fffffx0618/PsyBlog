# APPENDIX：Storage, Networks and Other Peripherals
## A.1 Introduction
I/O Designers must consider many factors 
- expandability 
- reliability
- performance
	- Assessing I/O system performance is very difficult. In different situations, needs use different measurements. 
	- Performance of I/O system depends on: 
		- Connection between devices and the system 
		- The memory hierarchy 
		- The operating system

**Typical I/O Devices**
<div text-align="center"><img src="image-161.png" width="70%"></div>

**Three Characters of I/O** 
- Behavior：输入（仅读一次）、输出（仅写一次，不可读）或存储（可重读或重写）
- Partner：I/O 设备的另一端可以是机器，也可以是人类
- Data rate：比如 I/O 设备与主存或处理器之间传输数据时的**峰值速率**

**I/O Performance Depends on the Application** 
- Throughput(吞吐量)：
	<u>I/O bandwidth(带宽)</u> can be measured in two ways: 
	1. How much data can be transferred in a certain time
	2. How many I/O operations can be performed per unit time
- Response time (e.g., workstation and PC) 
- Both throughput and response time (e.g., booking systems)

### Amdahl's Law
- **Sequential part** (串行) can limit speedup
> [!example] 100 processors, 90× speedup?
> $$\begin{align} T_{\text{new}} &=T_{\text{parallelizable}}/100+T_{\text{sequential}}\\ 
> \text{Speedup} &= \dfrac{1}{(1-F_\text{parallelizable})+F_{\text{parallelizable}}/100} =90 \\
> \text{Solving:  }&  F_{\text{parallelizable}} = 0.999
> \end{align}
> $$
> - Need sequential part to be 0.1% of original time

---
## A.2 Disk Storage and Dependability 
> [!note] disk & drive?
> - Disk（磁盘）
> 	- 指**实际的硬件存储设备本身**，即用于存储数据的物理媒介
> 	- Hard Disk, Solid-State Disk, Optical Disk
> - Drive（驱动器）
> 	- 指**用于读取和写入磁盘的设备或接口系统**，有时也指操作系统中的**逻辑卷**（如 C: 盘）
> 	- 可以是**物理装置**（如硬盘驱动器），也可以是**逻辑抽象**（如虚拟驱动器、光驱）
> 	- 包含控制电路、接口（如 SATA、NVMe）、固件等，负责与磁盘通信

### The Organization of Hard Disk
- **platters 盘片**: disk consists of a collection of platters, each of which has two recordable disk surfaces 
- **tracks 磁道**: each disk surface is divided into concentric circles 
- **sectors 扇区**: each track is in turn divided into sectors, which is the smallest unit that can be read or written
<div text-align="center"><img src="image-162.png" width="70%"></div>
### To access data of disk
- **Seek**: position read/write head over the proper track  
    数据不一定刚好在圈上，需要找到数据对应的圈
- **Rotational latency**: wait for desired sector  
    找到圈后，等待旋转到数据起点（<u>转 1/2 圈需要的时间</u>）
- **Transfer**: time to transfer a sector (1 KB/sector) function of rotation speed
    把硬盘数据搬到内存
- **Disk controller**: control the transfer between the disk and the memory
> [!example] 硬盘读取时间
> <div text-align="center"><img src="image-164.png" width="90%"></div>
> 
> - Seek Time + Rotational latency（转半圈的时间）+ Transfer Time（1 个 sector 的数据大小除以传输速率）+ Control Time

### Flash Storage
Nonvolatile semiconductor storage
- 100× – 1000× faster than disk
- Smaller, lower power, more robust
- But more $/GB (between disk and DRAM)
**Flash Types** 
- **NOR flash**: bit cell like a NOR gate 
	- Random read/write access 
	- Used for <u>instruction memory</u> in embedded systems 
- **NAND flash**: bit cell like a NAND gate  
	- Denser (bits/area), but <u>block-at-a-time</u> access 
	- Cheaper per GB 
	- Used for USB keys, media storage, ... 
Flash bits wears out after 10000’s of accesses 
- Not suitable for direct RAM or disk replacement 
- Wear leveling: remap data to less used blocks

### Dependability, Reliability, Availability
Computer system **dependability** is the quality of delivered service such that reliance can justifiably be placed on this service. 
- *MTTF* (Mean Time to Failure) 
	每一次从开始使用到发生故障的平均时间
- *MTTR* (Mean Time to Repair) 
	每一次发生故障后修理所花费的平均时间
- *MTBF* (Mean Time Between Failures) = MTTF+ MTTR 
- *Availability*：$\text{Availability}= \dfrac{\text{MTTF}}{\text{MTTF}+\text{MTTR}}$

Three Ways to Improve MTTF
- **Fault avoidance**: 
	preventing fault occurrence by construction 
- **Fault tolerance**: 
	using redundancy to allow the service to comply with the service specification despite faults occurring, which applies primarily to hardware faults 
- **Fault forecasting**: 
	predicting the presence and creation of faults, which applies to hardware and software faults

### Use Arrays of Small Disks
- $\text{Reliability of N disks} = \text{Reliability of 1 Disk} \div  N$
	50,000 Hours ÷ 70 disks = **700 hours** 
	365 x 24 = 8,760 hours per year 
	50,000 / 8,760 = **6 years** 
	Disk system MTTF: <u>Drops from 6 years to 1 month!</u>
- $\text{AFR (annual failure rate)} = \text{percentage of devices to fail per year}$
> [!note] Array Reliability
> - 采用 $9$ 的数量来测量 reliability
> <div text-align="center"><img src="image-165.png" width="80%"></div>

Arrays (without redundancy) too unreliable to be useful，因此我们引入了 ==RAID==

### Redundant Arrays of (Inexpensive) Disks
- Files are "striped 条带化" across multiple disks 
- Redundancy yields high data availability 
	- **Availability** : service still provided to user, even if some components failed 
- Disks will still fail 
- Contents reconstructed from data redundantly stored in the array 
	- <u>Capacity penalty</u> to store redundant info（牺牲空间换取可靠性）
	- <u>Bandwidth penalty</u> to update redundant info（牺牲读写效率换取可靠性）
> [!example] A disk arrays replace larger disk
> <div text-align="center"><img src="image-166.png" width="85%"></div>
> 
> - 不同的 RAID 模式
> <div text-align="center"><img src="image-167.png" width="85%"></div>

#### RAID 0: No Redundancy
> 常见于各种个人使用的终端设备（如手机，电脑等）
- Data is striped across a disk array but there is no redundancy to tolerate disk failure. 
- It also improves performance for large accesses, since many disks can operate at once. 
- RAID 0 something of a misnomer as there is no Redundancy

#### RAID 1: Disk Mirroring/Shadowing
> [!tip]
> - 一对一的进行复制备份
>   <div text-align="center"><img src="image-168.png" width="80%"></div>

- Each disk is fully duplicated复制 onto its "mirror" 
	Very high availability can be achieved 
- Bandwidth sacrifice on write: 
	Logical write = two physical writes  
	- Reads may be optimized 
- Most expensive solution: 100% capacity overhead
- <font color="#ff0000">(RAID 2 not interesting, so skip)</font>

#### RAID 3: Bit-Interleaved Parity Disk
采用**奇偶校验**，某一个盘中的数据丢失可以通过另外三块盘找回
<div text-align="center"><img src="image-169.png" width="65%"></div>

**Inspiration for RAID 4**
- RAID 3 relies on <font color="#ff0000">parity disk</font> to discover errors on Read
- But every sector has an error detection field 
	- Rely on **error detection field** to catch errors on read, not on the parity disk 

#### RAID 4: Block-Interleaved Parity
我们希望每块盘有自己的 error detection, 不需要校验盘来检验正确性，盘与盘之间相互独立
- RAID 4 对于每一条带的数据（分布在前四块磁盘上），都会计算出一个奇偶校验值，并将这个值存在第五块磁盘（奇偶校验盘）上
<div text-align="center"><img src="image-170.png" width="70%"></div>
- **Small read**：只需访问两个不同磁盘上的单个块，支持并行读取
- **Large write**：同时需要更新对应条带的奇偶校验块
> [!note] Write Penalty
> <div text-align="center"><img src="image-171.png" width="65%"></div>

**Inspiration for RAID 5** 
- RAID 4 works well for small reads 
- Small writes (write to one disk): 
	- Option 1: read other data disks, create new sum and write to Parity Disk 
	- Option 2: since P has old sum, compare old data to new data, add the difference to P 
- <u>Small writes are limited by Parity Disk</u>: Write to D0, D5 both also write to P disk

#### RAID 5: High I/O Rate Interleaved Parity
所有磁盘上都同时存放**数据块**和**奇偶校验块**，但它们是**交错分布**的
<div text-align="center"><img src="image-172.png" width="70%"></div>
- 在 RAID 4 中，所有写操作都要访问**同一个奇偶校验盘**，导致该盘成为性能瓶颈
- 在 RAID 5 中，由于奇偶校验块分布在不同磁盘上，所以：
    - 写入不同条带时，可以使用不同的磁盘来更新奇偶校验
    - 多个写请求可以并行处理，**避免单点瓶颈**

#### RAID 6: P+Q Redundancy
使用两组独立的校验信息（P 和 Q）来保护数据，允许同时容忍最多两块硬盘故障
- When a single failure correction is not sufficient, Parity can be generalized to have a <u>second calculation</u> over data and anther check disk of information.

#### Summary: RAID Techniques
- Disk Mirroring, Shadowing (RAID 1) 
	Each disk is fully duplicated onto its "shadow" 
	Logical write = two physical writes 
	100% capacity overhead
- Parity Data Bandwidth Array (RAID 3) 
	Parity computed horizontally 
	Logically a single high data bw disk
- High I/O Rate Parity Array (RAID 5)
	Interleaved parity blocks 
	Independent reads and writes 
	Logical write = 2 reads + 2 writes

---
## A.4 Buses and Other Connections between Processors Memory, and I/O Devices
<div text-align="center"><img src="image-173.png" width="60%"></div>

> [!note]
> **Bus**: Shared communication link (one or more wires) 
> 
> Difficult Design: 
> - may be bottleneck 
> - Physical constraints – limited speed 
> 	- length of the bus 
> 	- number of devices  
> - tradeoffs (fast bus accesses and high bandwidth) 
> - support for many different devices (different response time and data rate) 
> - cost

### 1. Bus Basics
- A bus contains two types of lines 
	- **Control lines 控制线路**: signal requests and acknowledgments, and to indicate what types of information is on the data lines. 
	- **Data lines 数据线路**: carry information (e.g., data, addresses, and complex commands) between the source and the destination. 
- Bus transaction 总线事务 
	- two parts: (1) <u>sending the address</u> and (2) <u>receiving or sending the data</u> 
	- Two operations 
		- input: receiving data from the device to memory 
		- output: sending data to a device from memory
> [!note]- Two operations 
> - input: receiving data from the device to memory 
> <div text-align="center"><img src="image-174.png" width="80%"></div>
> 
> - output: sending data to a device from memory
> <div text-align="center"><img src="image-175.png" width="80%"></div>

**Types of Buses**
- Processor-memory : short high speed, custom design) 
- Backplane 底板: high speed, often standardized, e.g., PCI) 
- I/O : lengthy, different devices, standardized, e.g., SCSI)

<div text-align="center"><img src="image-176.png" width="80%"></div>
<div text-align="center"><img src="image-177.png" width="80%"></div>

### 2. Synchronous vs. Asynchronous
- **Synchronous bus 同步总线**: use a clock and a fixed protocol, fast and small but every device must operate at same rate and clock skew requires the bus to be short 
- **Asynchronous bus 异步总线**: don’t use a clock and instead use *handshaking* 
	- **Handshaking protocol 握手协议**: A serial of steps used to coordinate asynchronous bus transfers.

> [!example] Asynchronous Example
> <div text-align="center"><img src="image-178.png" width="85%"></div>
> 
> 1. 当 `ReadReq` 处于高电平时，内存从数据总线中读取地址，执行读操作，然后抬高 `Ack` 的电平，告诉设备它看到了 `ReadReq` 信号
> 2. I/O 设备看到 `Ack` 处于高电平后，将 `ReadReq` 置于低电平状态
> 3. 内存看到 `ReadReq` 处于低电平后，将 `Ack` 置于低电平状态
> 4. 当内存完成数据读取后，它将数据放在数据线路上，并抬高 `DataRdy` 的电平
> 5. I/O 设备看到 `DataRdy` 处于高电平后，将从总线中读取数据，然后抬高 `Ack` 电平来表明 I/O 设备完成对数据的读取
> 6. 内存看到 `Ack` 处于高电平后，将 `DataRdy` 置于低电平状态
> 7. I/O 设备看到`DataRdy`处于低电平后，将`Ack`置于低电平状态，表明完成了整个传输过

### 3. Bus Arbitration
总线上有很多设备，多个设备要访问同一个内存时，需要**总线仲裁**，获得总线的所有权。
- A **bus master 总线主控器** is needed. Bus masters initiate and control all bus requests.
	e.g., processor is always a bus master. 

<div text-align="center"><img src="image-179.png" width="80%"></div>
<div text-align="center"><img src="image-180.png" width="80%"></div>

Deciding which bus master gets to use the bus next. 
- **Four bus arbitration schemes**: 
	- daisy chain arbitration (not very fair) 
	- centralized, parallel arbitration (requires an arbiter), e.g., PCI 
	- self selection, e.g., NuBus used in Macintosh 
	- collision detection, e.g., Ethernet 
- **Two factors** in choosing which device to grant the bus: 
	- bus priority（给不同设备分配不同的优先级）
	- fairness（避免某个设备长时间占用）

### 4. Performance analysis of Synchronous versus Asynchronous buses
评价总线的性能 - ==带宽 bandwidth==
> [!example]
> <div text-align="center"><img src="image-181.png" width="75%"></div>
> 
> <div text-align="center"><img src="image-182.png" width="75%"></div>

**Increasing the Bus Bandwidth** 
- Increasing data bus width 
- Use separate address and data lines 
- Transfer multiple words
> [!example]- Increasing the Bus Bandwidth
> <div text-align="center"><img src="image-183.png" width="80%"></div>
> 
> - the 4-word Block Transfers
> <div text-align="center"><img src="image-184.png" width="80%"></div>
> 
> <div text-align="center"><img src="image-185.png" width="75%"></div>
> 
> - the 16-word Block Transfers
> <div text-align="center"><img src="image-186.png" width="75%"></div>
> 
> <div text-align="center"><img src="image-187.png" width="75%"></div>
> 
> <div text-align="center"><img src="image-188.png" width="75%"></div>

---
## A.5 Interfacing I/O Devices to the Memory, Processor, and Operating System
- **Three characteristics of I/O systems** 
	- *shared* by multiple programs using the processor. 
	- often use *interrupts* to communicate information about I/O operations. 
	- The low-level control of an I/O devices is *complex* 
- **Three types of communication are required** 
	- The OS must be able to give *commands* to the I/O devices. 
	- The device must be able to *notify* the OS, when I/O device *completed* an operation or has encountered an *error*. 
	- Data must be transferred between memory and an I/O device

**Giving Commands to I/O Devices - Two methods used to address the device**
1. memory-mapped I/O（内存映射）: 
	- portions of the memory address space are assigned to I/O devices, and `lw` and `sw` instructions can be used to access the I/O port. 
2. special I/O instructions（专用I/O指令）
	- exp: x86 中 `in al,port out port,al.` RISC-V 中没有
3. command port & data port（命令端口 & 数据端口）
	- The Status register (a done bit, an error bit……) 
	- The Data register, The command register

### Communication with the Processor
#### 1. Polling
- **轮询**：处理器定期检查I/O设备的状态位，以判断是否需要执行下一个I/O操作
> [!bug]
> 即使设备没有数据要传、也没有准备好，CPU 仍不断重复查询。这种“忙等”行为浪费了大量宝贵的 CPU 时间。尤其在低速设备或长时间等待时，效率极低。

#### 2. Interrupt
- **中断**：当I/O设备完成某个操作或需要处理时，主动向处理器发送一个信号（中断），通知它来处理
> [!info] Interrupt-Driven I/O Mode
> - Advantage: concurrent operation 
> 	- 主要优点是实现“**并发操作**”— CPU 和 I/O 设备可以同时工作，提高效率
> 	  
> <div text-align="center"><img src="image-189.png" width="80%"></div>
> 
> - 当打印机在打印时，CPU 可以继续运行其他程序；只有当打印机需要数据时，才打断 CPU

#### 3. DMA（Direct Memory Access）
- **直接内存访问**：由设备控制器直接在内存和I/O设备之间传输数据，无需CPU参与
> [!info] DMA Transfer Mode
> <div text-align="center"><img src="image-190.png" width="75%"></div>
> 
> A DMA transfer need three steps:
> 1. 处理器初始化 DMA
> 	- CPU 首先向 **DMA 控制器** 提供必要的信息，包括：
> 	  - 设备身份（identity of the device，操作类型（operation），内存地址（memory address），传输字节数（number of bytes to transfer）
> 2. DMA 执行数据传输
>     - DMA 控制器根据 CPU 提供的信息，开始执行数据传输
>       - 它会 **请求总线控制权**（arbitrates for the bus），暂时“接管”系统总线
>     - 如果需要多次传输（如连续传输多个字节）：
>       - DMA 单元会自动**生成下一个内存地址**；并发起下一次传输，无需 CPU 干预
> 3. 传输完成后通知 CPU
>    - 当所有数据都成功传输完毕，DMA 控制器会：
>      - 释放总线控制权；向 CPU 发送 **中断信号（interrupt）**
>    - CPU 收到中断后，暂停当前任务，进入中断服务程序（ISR）：
>      - 检查是否发生错误；更新状态或继续后续操作

> [!tip] Compare polling, interrupts, DMA
> - polling 的坏处是浪费了大量的 CPU 的时间，CPU 定期轮询 IO 设备可能没有请求或者没有准备好
> - 如果 IO 操作是中断驱动的，OS 可以在数据从设备读取或写入时处理其他任务
> - DMA 不需要 CPU 控制，不会消耗 CPU 时间。但 DMA 只是搬运数据时有用，和 polling、interrupt 不对立
### Calculate Overhead
- 计算各种策略的开销（Overhead）
#### 1. Overhead of Polling in an I/O System
> [!Question]
> <div text-align="center"><img src="image-191.png" width="80%"></div>

**Answer**
$$
 \text{CPU 时间占比} = \frac{\text{每次轮询耗时} \times \text{每秒轮询次数}}{\text{每秒总时钟周期数}}
$$
- 每次轮询耗时 = $400 \text{ clocks}$
- 每秒总时钟周期数 = $500 \text{ MHz}$ = $5 \times 10^8 \text{ clock/s}$ 
##### Mouse
 - 每秒轮询次数：$30$；每次轮询耗时：$400 \text{ clocks}$
 - 总耗时/秒：$30 \times 400 = 12,000 \text{ clocks}$ 
 - CPU 占比：$\dfrac{12,000}{500,000,000} = 0.000024 = 0.0024\%$
##### Floppy Disk
 - 数据以 $16\text{-bit}$（$2\text{-byte}$） 传输；数据速率：$50 \text{ KB/sec}$；每次传输不能遗漏
- 每秒传输 $50 KB = 50 \times 1024 = 51,200\text{ byte}$ 
- 每次轮询需处理 2 字节 → 每秒需要轮询次数：$\dfrac{51,200}{2} = 25,600 \text{ 次/秒}$
- 总耗时/秒：$25,600 \times 400 = 10,240,000$ 周期
- CPU 占比：$\dfrac{10,240,000}{500,000,000} = 0.02048 = 2.048\%$
##### Hard Disk
- 以四个字（four-word chunks）为单位传输；传输速率为 $4 \text{ MB/sec}$；每次传输不能遗漏
- 四个字 = $4 \times 4 = 16$ 字节
- 每秒传输 $4 \text{ MB} = 4 \times 1024 \times 1024 = 4,194,304\text{ byte}$ 
- 每次轮询处理 16 字节 → 每秒轮询次数：$\dfrac{4,194,304}{16} = 262,144 \text{ 次/秒}$
- 总耗时/秒：$262,144 \times 400 = 104,857,600$ 周期
- CPU 占比：$\dfrac{104,857,600}{500,000,000} = 0.2097152 = 20.97\%$
#### 2. Overhead of Interrupt-Driven I/O
**No CPU time is needed when an interrupt-driven I/O device is not actually transferring.**
> [!Question]
> Suppose we have the same hard disk and processor we used in the former example, but we used **interrupt-driven I/O**. The overhead for each transfer, including the interrupt, is $500 \text{ clock cycles}$. Find the fraction of the processor consumed if the hard disk is only transferring data $5\%$ of the time.

假设硬盘 $100\%$ 时间都在传输数据
1. 由 Polling 中可以得到，每秒轮询次数为 $\dfrac{4,194,304}{16} = 262,144 \text{ 次/秒}$
2. 每次传输对应一次中断，所以总周期数 $250K\times 500=125\times 10^{6}\text{ cycles per second}$
	- 将 $262,144 \approx 250K$
3. CPU 占比：$\dfrac{125,000,000}{500,000,000} = 25\%$
假设硬盘 $5\%$ 时间都在传输数据，那么CPU 占比变为 $25\% \times 5\%=1.25\%$
#### 3. Overhead of I/O Using DMA
> [!Question]
> Suppose we have the same hard disk and processor we used in the former example.
> - Assume that the initial setup of a DMA transfer takes $1000\text{ clock cycles}$ for the processor, and assume the handling of the interrupt at DMA completion requires $500$ clock cycles for the processor. 
> - The hard disk has a transfer rate of $4\text{ MB/sec}$ and uses DMA. The average transfer from disk is $8 \text{ KB}$. Assume the disk is actively transferring $100\%$ of the time. 
> 
> Please find what fraction of the processor time is consumed.

每次 8KB 传输所需时间：
$$
\text{Time per transfer}=\frac{8\text{KB}​}{4\text{MB/sec}}=\frac{8×1024\text{ B}}{4\times1024\times1024\text{ B/sec}​}=\frac{8}{4096}​=\frac{1}{512}\approx 0.002\text{ ​seconds}
$$
总开销：
$$
\frac{\text{每次传输需要的CPU周期个数}}{\text{每秒传输的次数}}=\frac{(1000+500)\frac{\text{cycles}}{\text{transfer}}}{0.002\frac{\text{seconds}}{\text{transfer}}}=＝750\times 10^3 \frac{\text{clock cycles}}{\text{second}}
$$
CPU 占比：$\dfrac{750\times 10^3}{500\times 10^6} = 0.2\%$

---
## A.6 I/O Performance Measures: Examples from Disk and File Systems
- Supercomputer I/O Benchmarks
- Transaction Processing I/O Benchmarks
	- I/O rate: the number of disk access per second, as opposed to data rate.
- File System I/O Benchmarks
	- MakeDir, Copy, ScanDir, ReadAll, Make

---
## A.7 Designing an I/O system
**The general approaches to designing I/O system**
- Find the *weakest link* in the I/O system, which is the component in the I/O path that will constrain the design. Both the <u>workload</u>**工作负载** and <u>configuration limits</u>**硬件配置** may dictate where the weakest link is located.
- Configure this component to sustain the required **bandwidth**.
- Determine the requirements for the rest of the system and configure them to support this bandwidth.
> [!question]
> Consider the following computer system:
> 1. A CPU sustains <u>3 billion instructions per second</u> and it takes average <u>100,000 instructions</u> in the operating system per I/O operation.
> 2. A memory backplane bus is capable of sustaining a transfer rate of <u>1000 MB/sec</u>.
> 3. SCSI-Ultra320 controllers with a transfer rate of <u>320 MB/sec</u> and accommodating up to <u>7 disks</u>.
> 4. Disk drives with a read/write bandwidth of <u>75 MB/sec</u> and an average seek plus rotational latency of <u>6 ms</u>.
> 
> If the workload consists of 64-KB reads (assuming the data block is sequential on a track), and the user program need 200,000 instructions per I/O operation, please find the maximum sustainable I/O rate and the number of disks and SCSI controllers required.

- CPU 的最大 I/O 速率
$$
\begin{align}
\text{Maximum I/O rate of CPU}&=\frac{\text{Instruction execution rate}}{\text{Instructions per I/O}}\\
&=\frac{3\times 10^9}{(200+100)\times 10^3}=10000\frac{{\text{I/Os}}}{{\text{seconds}}}
\end{align}​
$$
- 内存总线的最大 I/O 速率
$$
\text{Maximum I/O rate of bus} = \frac{\text{Bus bandwidth}}{\text{Bytes per I/O}}=\frac{1000\times 10^6}{64\times 10^3}=15625\frac{{\text{I/Os}}}{{\text{seconds}}}
$$
- **最大 I/O 速率**
	- CPU 是**瓶颈**，因为它只能处理 10,000 $\frac{{\text{I/Os}}}{{\text{seconds}}}$，而总线可以支持 15,625 $\frac{{\text{I/Os}}}{{\text{seconds}}}$
	- 系统最大可持续 I/O 速率由 CPU 决定：**10,000 I/Os/秒**
- **计算所需磁盘数量**
	- 单次 I/O 时间（Disk Time）
$$
\begin{align}
\text{Time per I/O at disk} &= \text{Seek/rotational time} + \text{Transfer time}\\
&= 6 \text{ms} ＋ \frac{\text{64KB}}{\text{75MB/sec}} = 6.9 \text{ms}
\end{align}
$$
	- This means each disk can complete <u>1000ms/6.9ms = 146 I/Os per second</u>. To saturate the bus, the system need <u>10000/146 ≈ 69 disks</u>.
- **计算所需 SCSI 控制器数量**
$$
\text{Number of controllers}=⌈ \frac{69}{7} ⌉=10
$$
	- 每块磁盘的平均传输速率
$$
\text{Transfer rate}=\frac{\text{Transfer size}}{\text{Transfer time}}​=\frac{6.9 \text{ms}}{64\text{KB}}​​\approx9.56 \text{MB/s}
$$
	- 7 块磁盘的总传输速率
$$7\times9.56 \text{MB/s}\approx 66.92 \text{MB/s}<320 \text{MB/s}$$
	- 说明即使有 7 块磁盘共享一个控制器，不会导致带宽饱和