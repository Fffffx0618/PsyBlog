# CHAPTER 5. Hashing

## 1. General Idea
**==Symbol Table ( = Dictionary ) ::= {<name, attribute>}==**

**Symbol Table (简单表) ADT** :   
* **Objects**: A set of name - attribute pairs, where the names are unique   
* **Operations**:  
  * `SymTab Create (TableSize)   `
  * `Boolean IsIn (symtab, name) ` 
  * `Attribute Find (symtab, name)  `
  * `SymTab Insert (symtab, name, attr)  `
  * `SymTab Delete (symtab, name)`

**Hash Tables (散列表)**
<img src="数据结构基础.assets/image-20250524161808278.png" alt="image-20250524161808278" style="zoom:67%;" />

* **标识符密度 (identifier density)** $= \frac{n}{T}$ 
* **加载密度 (loading density)** $λ=\frac{n}{s⋅b}$

**Problem** :
* A **collision 冲突** occurs when we hash two nonidentical identifiers in to the same bucket, i.e. $f (i_1)=f (i_2)$ when $i_1 \neq i_2$.
* An **overflow 溢出** occurs when we hash a new identifier into a full bucket.

**Without overflow, $T_{search}=T_{insert}=T_{delete}=O (1)$**

## 2. Hash Function
Properties of $f$: 
1.  $f (x)$ must be **easy** to compute and **minimizes** the number of collisions. 
2.  $f (x)$ should be unbiased. That is, for any $ x $ and any $ i $, we have that Probability $(  f (x) = i  ) = 1 / b$. Such kind of a hash function is called a ***uniform hash function 统一散列函数***.  
### Some Hash Function
$$ f (x) = x \% \text{TableSize}; \quad /* \text{if } x \text{ is an integer} */  $$
>  What if TableSize = $10$ and $ x $'s are all end in zero? ---- bad
>  TableSize = **prime** number ---- good for random integer keys
$$ f (x) = (\sum x[i] )\% \text{TableSize}; \quad /* \text{if } x \text{ is a string} */  $$
$$f (x)=(x[0]+x[1]∗27+x[2]∗27^2) \% \text{TableSize}f (x)=(∑x[N−i−1]∗32^i) \% TableSize$$

```c
> Index Hash 3 (const char *x, int TableSize)
> {
> Unsigned int HashVal = 0;
> While (*x != '\0')
>   HashVal = (HashVal << 5) + *x++;
> Return HashVal % TableSize;
> }
> ```
* If $x$ is too long, the early characters will be left-shifted out of place.

## 3. Seperate Chaining
* keep a list of all keys that hash to the same value
### 3.1 Initialize

```c
Struct ListNode;
Typedef struct ListNode * Position;
Struct HashTbl;
Typedef struct HashTbl * HashTable;

Struct ListNode
{
    ElementType Element;
    Position Next;
};
Typedef Position List;

/* List *TheList will be an array of lists, allocated later */ 
/* The lists use headers (for simplicity), */ 
/* though this wastes space */ 
Struct HashTbl
{
    Int TableSize;
    List * TheLists;
};
```

### 3.2 Create an empty table
<img src="数据结构基础.assets/image-20250524165112663.png" alt="image-20250524165112663" style="zoom: 100%;" />

```c
HashTable InitializeTable (int TableSize)
{
    HashTable H;
    Int i;
    If (TableSize < MinTableSize)
    {
        Error ("Table size too small");
        Return NULL;
    }
    H = (HashTable) malloc (sizeof (struct HashTbl)); // Allocate table
    If (H == NULL) 
        FatalError ("Out of Space!!!");
    H->TableSize = NextPrime (TableSize);  // Better be prime
    H->TheLists = malloc (sizeof (List) * H->TableSize);  // Array of lists
    If (H->TheLists == NULL)   
        FatalError ("Out of space!!!"); 
    for (i = 0; i < H->TableSize; i++) 
    {   // Allocate list headers
        H->TheLists[i] = malloc (sizeof (struct ListNode)); // Slow! 
        If ( H->TheLists[i] == NULL )  
            FatalError ("Out of space!!!"); 
        Else    
            H->TheLists[i]->Next = NULL;
    } 
    Return H; 
}
```

### 3.3 Find a key from a hash table
```c
Position Find (ElementType Key, HashTable H)
{
    Position P;
    List L;

    L = H->TheLists[Hash (Key, H->TableSize)];

    P = L->Next;
    // Identical to the code to perform a Find for List ADT
    While (P != NULL && P->Element != Key) // Probably need strcmp
        P = P->Next;
    Return P;
}
```

### 3.4 Insert a key into a hash table
```c
Void Insert (ElementType Key, HashTable H)
{
    Position Pos, NewWell;
    List L;
    Pos = Find (Key, H);
    If (Pos == NULL) // Key is not found, then insert
    {
        NewCell = (Position) malloc (sizeof (struct ListNode));
        If (NewCell == NULL)
            FatalError ("Out of space!!!");
        Else
        {
            L = H->TheLists[Hash (Key, H->TableSize)];
            NewCell->Next = L->Next;
            NewCell->Element = Key; // Probably need strcpy
            L->Next = NewCell;
        }
    }
}
```

* Make the TableSize about as large as the number of keys expected (i.e. to make the loading density factor $\lambda ≈ 1$)

## 4. Opening Addressing
* find another empty cell to solve collision (avoiding pointers)
  ```c
  Algorithm: insert key into an array of hash table
  {
      If (table is full) ERROR ("No space left");
      Initalize i = 0; /*the counter of probing*/
      Do{
          Index = ( hash (key) + f (i) )%TableSize;
          ++i;
      }while ( collision at index );
      Insert key at index;
  }
  ```
  * $f (i)$ is collision resolving function. $f (0)=0$

### 4.1 Linear Probing
线性探测 $f (i)=i$
<img src="数据结构基础.assets/image-20250524191127740.png" alt="image-20250524191127740" style="zoom:80%;" />

**Analysis：**

$$ p =  \begin{cases}  \frac{1}{2}\left (1 + \frac{1}{(1-\lambda)^2}\right) & \text{for insertions and unsuccessful searches} \\ \frac{1}{2}\left (1 + \frac{1}{1-\lambda}\right) & \text{for successful searches} \end{cases} $$

### 4.2 Quadratic Probing

==二次探测 $f (i)=i^2$ /* a quadratic function */==

> * **【Theorem】** If quadratic probing is used, and the table size is **prime**, then a new element can always be inserted if the table is **at least half empty**.
>
> * Note: If the table size is a prime of the form $4 k+3$, then the quadratic probing $f (i)=±i^2$ can probe the **entire** table.

**Proof:** Just prove that the first $⌊TableSize/2⌋$ alternative locations are all distinct. That is, for any $0 ≤ i ≠ j ≤ ⌊TableSize/2⌋$, we have $(h (x) + i²) \% TableSize ≠ (h (x) + j²) \% TableSize$ 

Suppose:    $h (x) + i² = h (x) + j² (mod TableSize)$ 
Then:          $i² = j² (mod TableSize)$
                  $  (i + j)(i - j) = 0 (mod TableSize)$

TableSize is prime ➞ either $(i + j)$ or $(i - j)$ is divisible by $TableSize$ 

**Contradiction!** 

For any $x$, it has $⌊TableSize/2⌋$ distinct locations into which it can go. If **at most** $⌊TableSize/2⌋ $ positions are taken, then an empty spot can always be found.

#### Find Position  
* using $F (i)=F (i-1)+2 i-1$ 
```c
Position Find (ElementType Key, HashTable H)
{
    Position CurrentPos;
    Int CollisionNum = 0;
    CurrentPos = Hash (Key, H->TableSize);
    While (H->TheCells[CurrentPos]. Info != Empty && 
            H->TheCells[CurrentPos]. Element != Key) 
    {
        CurrentPos += 2 * ++CollisionNum - 1;  // 1
        If (CurrentPos >= H->TableSize)        // 2
            CurrentPos -= H->TableSize;      
    }
    Return CurrentPos;  // 3
}
```

#### Insert ELement
* 每个元素有三种状态：`Empty`, `Legitimate`, `Deleted`
```c
Void Insert (ElementType Key, HashTable H)
{
    Position Pos;
    Pos = Find (Key, H);
    If (H->TheCells[Pos]. Info != Legitimate)  // Ok to insert here
    {
        H->TheCells[Pos]. Info = Legitimate;
        H->TheCells[Pos]. Element = Key; // Probably need strcpy
    }
}
```

**Note:**  
1.  Insertion will be seriously slowed down if there are too many deletions intermixed with insertions.
2.  Although primary clustering is solved, secondary clustering occurs – that is, keys that hash to the same position will probe the same alternative cells.

### 4.3 Double Hashing
 $f (i)=i * hash_2 (x);$ // $hash_2 (x)$ is the $2_{nd}$ hash function 
* $hash_2 (x)\neq 0$
* make sure that all cells can be probed
Tip: $hash_2 (x)=R-(x\% R)$ with $R$ a prime smaller than Tablesize, will work well.

**Note:** 
1.  If double hashing is correctly implemented, simulations imply that the **expected** number of probes is almost the same as for a **random** collision resolution strategy. 
2.  Quadratic probing does not require the use of a second hash function and is thus likely to be **simpler and faster** in practice.

## 5. Rehashing
* Build another table whose size is a **prime** and **at least as twice as big**
* Scan down the entire original hash table for non-deleted elements
* Use a **new function** to hash those elements into the new table
If there are $N$ keys in the table, then $T (N)=O (N)$
