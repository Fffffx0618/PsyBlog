# Chapter3.Lists, Stacks, and Queues

## 1. Abstract Data Type

[Definition] $\text{Data Type = {Objects}} \cup\text{{Operations}}$

- 数据类型 = 数据**对象集** + 数据集合相关联的**操作集**

- 抽象：描述数据类型的方法不依赖于具体实现
    - 与存放数据的机器无关
    - 与数据存储的物理结构无关
    - 与实现操作的算法和编程语言无关 

## 2. The List ADT
### 1. Simple Array Implementation of Lists 

>  内部存储连续

- Advantage: `Find_Kth` takes $O(1)$ time.
- Disadvantage
    - MaxSize has to be estimated. 
    - `Insertion` and `Delete` not only takes $O(N)$ time, but also involves a lot of data movements.

### 2. Linked Lists

> 注：除非作特殊说明，FDS 中所有链表的实现默认将虚拟节点作为头指针

**Note : ==<u>dummy head !!!</u>==**

- Advantage : `Insertion` and `Delete` takes $O(1)$ time.
- Disadvantage : `Find_Kth` takes $O(N)$ time

### 3. Doubly Linked Circular Lists

<div style="text-align: center"><img src="images/image-20250619222511917.png" width="60%"></div>


~~~c
typedef struct node*node_ptr;
typedef struct node{
    node_ptr llink;
    element item;
    node_ptr rlink;
}
~~~

- `ptr = ptr->llink->rlink=ptr->rlink->llink`

### 4. Cursor Implementation of Linked Lists

<div style="text-align: center"><img src="images/image-20250305142445525.png" width="65%"></div>

- **声明**

    ```c
    typedef unsigned int node_ptr;
    struct node
    {
       element_type element;
        node_ptr next;
    };
    typedef node_ptr LIST;
    typedef node_ptr position;
    struct node CURSOR_SPACE[SPACE_SIZE];
    ```

- **Operations**

    ```c
    //malloc:
    p = CursorSpace[0].Next;
    CursorSpace[0].Next = CursorSpace[p].Next;
    //free(p)
    CursorSpace[p].Next = CursorSpace[0].Next ;
    CursorSpace[0].Next = p;
    ```

### 5. Multilists

> 实现起来较复杂，此处略过

<div style="text-align: center"><img src="images/image-20250619222912693.png" width="50%"></div>



## 3. The Stack ADT
### 1. ADT
A **stack** is a **Last-In-First-Out (LIFO)** list, insertions and deletions are made at the **top** only.

**Operations:**

~~~ c
int IsEmpty(Stack S);
Stack CreateStack(void);
void DisposeStack(Stack S);
void MakeEmpty(Stack S);
void Push(ElementType X, Stack S);
ElementType Top(Stack S);
void Pop(Stack S);
~~~

**Note :**

- A `Pop` (or `Top`) on an **empty** stack is an error in the **stack ADT**.

- `Push` on a **full** stack is an **implementation error** but not an ADT error.

### 2. Implementation

~~~c
struct StackRecord{
    int capacity;
    int TopOfStack;
    ELementType *Aray;
}
~~~

#### Linked List Implementation
- **Push**

    ```c
    TmpCell->Next = S->Next;
    S->Next = TmpCell;
    ```

- **Top**

    ```c
    return S->Next->Element;
    ```

- **Pop**

    ```c
    FirstCell = S->Next;
    S->Next = S->Next->Next;
    free(FIrstCell);
    ```

> **Note**: 
>
> - The stack model must be well **encapsulated**(封装).
> - Error check must be done before Push or Pop.

### 3. Applications

- Balancing Symbols
- Postfix Evaluation
- Function Calls - System Stack

#### 3.1 Postfix Evaluation

- 遇到**操作数**，将其压入栈中

- 遇到**运算符** $opt$，弹出栈最顶上两个元素 $a, b$，其中 $top=a$，然后计算 $c=b \space opt\space a$，最后将 $c$ 压入栈中

- 遍历完后缀表达式后，栈中应当剩下一个元素，该元素即为最终结果

#### 3.2 Infix to Postfix Conversation

1. 初始化一个空栈 (存储算子) 和一个空输出列表。
2. 从左到右扫描中缀表达式。
3. 如果扫描到**操作数**（如 a, b, c 等）：直接将其加入输出列表。
4. 如果扫描到**运算符**（如 $+, -, *, /$等)
    1. 若**当前运算符的优先级 $>$ 栈顶运算符的优先级**，则将当前运算符压入栈中
    2. 若**当前运算符的优先级 $\leq$ 栈顶运算符的优先级**，则<u>将栈顶运算符弹出</u>直到满足条件 (1)，将运算符压入栈
    3. 如果扫描到**左括号" ( "**，则直接**进栈**（<u>压入前优先级最高，压入后优先级最低</u>）
    4. 如果扫描到**右括号" ) "**，则不断**弹出**栈顶运算符并输出，遇到左括号**" ( "**停止，弹出左括号并丢弃括号
5. **扫描完表达式后**，将栈中剩余的运算符依次弹出并加入输出列表。

## 4. The Queue ADT

### 1. ADT
A queue is a **First-In-First-Out (FIFO)** list, insertions take place at one end and deletions are take place at the oppose end.

**Operations:**

~~~ c
Int IsEmpty ( Queue Q );//是否是空
Queue CreateQueue ( void );//申请内存，返回 queue
Void DisposeQueue ( Queue Q );//消除一个 queue
Void MakeEmpty ( Queue Q );//清除元素，保留 queue

Void Enqueue ( ElementType X, Queue Q );//把 X 加入到 Q 中
ElementType Front ( Queue Q );//获取顶端元素的值
Void Dequeue ( Queue Q );//删除底部端元素
~~~

### 2. Implementation

~~~c
Struct QueueRecord{
    Int Capacity;/* max size of queue */
    Int Front;/* the front pointer */
    Int Rear;/* the rear pointer */
    Int Size;/* Optional - the current size of queue */
    ELementType *Arra;
}
~~~

#### Circular Queue

对于循环队列，区分空队列和满队列有 2 种做法：

- 空出一块空间
- 增加一个 `Size` 的字段，用来实时统计队列元素个数，这样无需浪费空间

  > 如果用 `front` 表示队首元素，`size` 表示当前队伍大小，`m` 表示队伍最大大小，则队尾元素 `rear = (front + size - 1) % m`
  

<div style="text-align: center"><img src="images/image-20250305154604454.png" width="35%"></div>
