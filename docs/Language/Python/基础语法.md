# Python 

## 一. 变量
- 给一个内容绑定一个标签即变量名（注意请不要认为变量类似一个“盒子”）
- 通过 = 来定义变量，变量名 = 内容
- 动态类型，不需要规定类型（可以通过 ==变量名: 类型 = 内容== 来进行类型标注）
- 变量名
  - 只能包含**字母、数字、下划线**
  - 只能以字母、下划线开头，不能以数字开头，而且**大小写敏感**
  - 不能用关键字（例如 `if`、 `def` 等）作为变量名，不推荐使用内置函数名作为变量名
## 二. 数据类型
>  注释

```python
>  a = 10
>  # 这是单行注释
>  print(a)
>  """
>  这是多行注释，
>  支持换行
>  """
```

`int, float, str, bool, Nonetype`

~~~ python
type(a) #返回a的数据类型
~~~

### 2.1 数字
- 1 是整数，1. 是浮点数

#### 1. 强制转换
  - `int( )`：向 0 舍入
  - `round( )`：向偶舍入（四舍六入**五凑偶**，``round(4.5) = 4`，`round(5.5) = 6`）
  - `math.floor( )`、`math.ceil( )`  ：下取整、上取整（需要 `import math`）
  - `str( )`：转换成字符串类型
  - 
#### 2. 运算

|      运算符       | 作用                                             |
| :------------: | ---------------------------------------------- |
|    \+  -  *    | 加减乘，左右都是整数结果也是**整数**，<u>有浮点数结果就是浮点数</u>        |
|       /        | 除法，结果是**浮点数**（即使可以整除）                          |
|       //       | 结果是**整数**，<u>向下取整</u>                          |
|       %        | 取模                                             |
|       **       | **可以是浮点数**，比如 a ** 0.5 表示开根号                   |
| pow(a, b, mod) | 乘方，mod 可以省略，如果有 mod 则对结果取模，如果 mod 为 -1 则计算乘法逆元 |

#### 3. 复数

- python 中内置了复数类型，``1+2j`形式就表示一个复数，其中 j 即虚数单位 i
- 也可以使用 **complex( 实部 , 虚部 )** 形式定义复数
- 属性与方法
  - `c.real`：实部
  - `c.imag`：虚部
  - `c.conjugate( )`：返回共轭复数

### 2.2 字符串

> * **字符串无法修改**

#### 1. 定义方式

1. 单引号定义：`name = 'ZhangSan'`
2. 双引号定义：`name = "ZhangSan"`
3. 三引号定义：`name = """ZhangSan"""`（支持换行）

#### 2. 转义字符

| 转义字符 |  作用  |
| :------: | :----: |
|   `\n`   |  换行  |
|   `\t`   | 制表符 |
|   `\r`   |  回车  |
|   `\'`   | 单引号 |
|   `\"`   | 双引号 |
|   `\\`   |  斜杠  |

#### 3. 常用操作

```python
# 拼接：直接将字符串“相加”  
a = name + “said“ + sentence

# 查找：查找元素或字符串
value = list.index("str") 

# 替换：把 str1 替换为 str2
str = str.replace(str1, str2)

# 分割：按指定的分隔符字符串划分，存入列表对象中(分隔符不被存储)
my_str = "Hello My Name Is Bob"
my_list = my_str.split("a")

# 规整
s = "ab32432dewwba"
s.strip() # 删除字符串首尾空白（包含空格和换行符）
s.strip("ab") # 删除字符串首尾的a和b(保证首尾不会出现a或b)
s.upper( ) # 把s的内容转为全大写
s.lower( ) # 把s的内容转为全小写
s.title( ) # 单词首字母大写
```

#### 4. 字符串格式化
* 占位符

| `%s` |         字符串的格式化，也是最常用的，又称作“通配符”         |
| :--: | :----------------------------------------------------------: |
| `%d` |                    格式化整数，也比较常用                    |
| `%c` |                     格式化字符及ASCII码                      |
| `%f` | 格式化浮点数，可以指定精度，默认是小数点6位（`%m.nf`：宽度m，保留n位小数） |
| `%o` |                     格式化无符号八进制数                     |
| `%x` |                    格式化无符号十六进制数                    |
| `%e` |                将整数、浮点数转换成科学计数法                |
| `%%` |     字符串中存在格式化标志时，需要用 `%%`表示一个百分号      |

* 输出格式
  ```python
  name = '小明'
  hello = '你好'
  a = “%s我的名字叫%-4s！“ %(hello, name)
  print(a)# 左对应
  character=56
  print("%d在ASCII码中表示字母%c" %(character, character))
  # 由于在python中只有字符串这种类型，使用在这里%c只能表示ASCII码，并不能表示字符
  ```

* `format`方式
  ``` python
  name = "{2}在{0}学了一天的{1}"
  data = name.format("ZJU","Python","Jason",)
  print(data)
  ```

#### 5. 快速格式化

- **r-string**：引号中**不进行转义**，即代表斜杠字符本身
- **f-string**：**格式化**字符串
- **b-string**：将字符串转为 bytes，**只能包含 ASCII 字符**

 **f-string**

~~~ python
name = "Bob", math_score = "124"
message_content = f"I am {name}, I got {math_score} in the math test."
~~~

### 2.3 数据输入
* `input( )`语句，默认读取格式为字符串
* 需要手动转换所需的数据类型

  ```python
  a = int(input("Please input your password."))
  ```

### 2.4 字节类型
- 类似字符串，但存储的是字节的值，更像列表，显示为 `b"..."` 只是更加易读而已
- `b"..."` 则表示字节类型，其中只能包含 ASCII 字符和 `\x..` 表示的十六进制数
- 与字符串转换
  - `"...".encode(encoding)` 根据 encoding 编码字符串，默认 UTF-8
  - `bytes_obj.decode(encoding)` 根据 encoding 解码字节序列，解码失败会报错
  - `bytes("...", encoding) ` 也是根据 encoding 编码字符串
  - 不要使用 `str(b"...") ` 来将字节序列转为字符串

### 2.5 布尔类型
- `True` 和 `False`，记住**首字母大写**
- 将变量转换为``bool`类型
  * `bool(a)`，如果是a是数字，则非零都是 True，如果a是字符串,则非空都是 True

## 三. 数据容器
### 3.1 列表
```python
list = [value1, value2, value3]
```

- 可存储**不同类型**的元素（可嵌套使用`list[ [1,2,3], "abc", [2,4,6] ]`）

#### 1. 索引

- 从 0 开始计数，`list[n]` 即表示访问第 n+1 个元素
- 可以是负数，负数即表示倒数，`list[-2] `表示倒数第二个元素

#### 2. 切片

```python
list[start_index:end_index:step]
```

Example

```python
list[1:5:2] # 从1取到4，步长为2
list[1:10] # 省略步长
list[::-1] # 省略起始位置和终止位置
list[:10:1] # 省略起始位置
list[1::1] # 省略终止位置
```

* 第一个冒号**不能省略**

#### 3. 列表操作

* 获取索引

  ```python
  list = ["Hello", 24, "ZJU", 67656]
  a = list.index("ZJU")
  b = list.index(24) 
  ```

- 修改元素

  * 直接通过索引查找元素，然后等号赋值

- 插入

  ```python
  list.insert(index, x) # 在索引 index 的位置插入 x，后面依次后移
  ```

- 栈的功能

  ```python
  # 入栈
  list.append(a) # 在列表末尾加入元素 a
  list.extend(a) # 把一个列表 a 接到当前列表后面
  
  # 出栈
  list.pop( ) # 弹出列表末尾元素并返回
  list.pop(index) # 弹出索引 index 位置的元素，后面依次前移
  ```

- 删除元素

  ```python
  del list[index] # 删除list[index]
  list.remove(value) # 删除第一个值为 value 的元素
  list.clear( ) # 清空列表
  ```

- 统计元素

  ```python
  list.count(x) # 统计 list 中值为 x 的元素个数
  len(list) # 统计 list 中的元素个数
  max(list) # 得到列表中的最大值
  min(list) # 得到列表中的最小值
  ```

- 排序

  ```python
  list.sort(reverse = False) # 永久排序（即排序后赋值给当前列表）
  sorted(list, reverse = False) # 返回排序好的新列表，未实际改变链表
  # 省略 reverse 则默认升序，如果传入 reverse = True 则按降序
  ```

- 反转列表

  ```python
  list.reverse() # 永久反转
  list[\:\:-1] # 返回反转的列表（利用切片）
  ```

### 3.2 元组

```python
tuple_name = (value1, value2, value3) # 定义元组变量
tuple_name = () # 定义空元组
tuple_name = tuple() # 定义空元组
```

- 定义后元素**无法修改**，可包含**不同类型**的元素
- 元组只有一个元素写成`tuple = (a,)` 而不是 `(a)`（后者表示单个值）
- 可以使用 `tuple(name)` 来将可迭代对象（列表、字符串等）转为元组
- 元组并**不能保证**元素完全不可变，避免在元组中存放可变元素

### 3.3 集合

```python
set_name = {element1, element2, element3} # 定义集合变量
set_name = set() # 定义空集合
```

- 自动**去重**，内部数据**无序**（不支持下标索引访问）
- 可用 `set(name)` 来将可迭代对象转为元组，自动去重
- 集合中不能包含列表等不可 hash 化的元素

#### 修改

* ```python
  s = {123,"Hello",67656,"ZJU"}
  s.add("ZJU") # 来加入一个元素，自动去重
  a = s.pop() # 随机弹出一个元素
  s.remove("ZJU") # 删除一个元素，如果没有会抛出异常
  s.discard("ZJU") # 来删除一个元素，如果没有则忽略
  s.clear() # 清空集合
  ```

#### 运算

* ```python
  s1 = {1, 2, 3, 4, 5}
  s2 = {1, 3, 6, 7, 8}
  set3 = s1 - s2 # 取差集
  set4 = s1 & s2 # 取交集
  set5 = s1 | s2 # 取并集
  set6 = s1 ^ s2 # 取对称差集
  ```

### 3.4 字典

```python
dictionary = {key1: value1, key2: value2, key3: value3} # 定义字典变量
dictionary = {} # 定义空字典
dictionary = dict() # 定义空字典
```

- 存储键值对，键的类型必须是**不可变**的

- 用 `d[key]` 来访问字典中 `key` 对应的值，可读取、修改

- key 和 value 可以为任意数据类型（key 不能为字典）

  * 字典是可以**嵌套**的

- ```python
  d[key] = value # key不存在则添加键值对，存在则修改key的值
  get_value = d.pop(key) # 弹出key对应的value，并删去键值对
  del d[key] # 删除指定的键值对（key不存在会报错）
  d.clear() # 清空字典
  keys = d.keys() # 获得所有的key
  ```

- 判断字典时候存在某键：`key in dictionary`（返回`bool`值）

### 3.5 类型注释

* 协助第三方IDE工具对代码进行类型推断，协助做代码提示
* 帮助开发者自身对变量进行类型注释（备注）
* 仅仅是**提示性**的，并非决定性

#### 1. 变量类型注释

1. **方法1**：`变量:类型`

* 基础数据类型注释

  ```python
  var_1: int = 1 # 定义了int型变量var_1，值为1
  ```

* 类对象类型注释

  ```python
  class Student:
      pass
  stu: Student = Student()
  ```

* 数据容器类型注释

  ```python
  my_dir: dict = {name: "Bob", age: 18}
  # 以下是详细注释
  my_list: list[int] = [1, 2, 3] 
  my_tuple: tuple[str, int, bool] = ("Hello", 24, True)
  my_set: set[int] = {1, 2, 3}
  my_dir: dict[str, int] = {"height": 170, "age": 18}
  ```

2. **方法2**：`# type:类型`

   ```python
   var_1 = 1 # type: int为变量设置类型注释
   ```

#### 2. 函数类型注释

~~~python
def func(data: int, name: str) -> int:
    return data
~~~

#### 3. Union类型

* `my_list: list[int]`表示列表中的元素属性均为`int`

* 如果想要表示有多种类型的元素则需要使用`Union[类型,...,类型]`标记

* ```python
  my_list: list[Union[int,str]] = ["CS", "ZJU", 3] 
  my_dir: dict[str, Union[str,int]] = {"name": "Bob", "height": 170, "age": 18}
  
  def func(data: Union[int, str], name: str) -> Union[int, str]:
      return data
  ```



## 四. 条件分支

### 4.1 布尔表达式

**比较运算符**

* `== != > < >= <=`，类比C语言

- 使用 `not`、`and`、`or` （按优先级排序）来进行布尔运算，必要时加括号保证优先级

  > C语言中用的是`&&`和`||`，注意区分

  - 用 `&`和` | `来表示**与**和**或**（不会短路）
  - 用 `and` `or` `not` 进行**与**/**或**/**非**运算（会短路）

- 判断元素是否在列表中

  - `value in lst`：如果在则值为 True
  - `value not in lst`：如果在则为 False

- 判断键是否在字典中

  - `key in d`、``key not in d` 与列表同理

### 4.2 条件语句

```python
if condition1:
    ...
elif condition2:
    ...
else:
    ...
```

- 条件不需要加括号（**加了也没问题**）

- 注意**缩进**!!!

- **三目运算符**写法 `a if condition else b`

  ```python
  a = 25 if b > c else 10
  ```

### 4.3 缩进

- **缩进**在 python 中非常重要，python 通过缩进来得到代码结构
- 缩进可以使用空格或制表符
- 处于同一层缩进下的代码属于同一个代码块
- 同一个代码块的缩进要统一
  - 区好空格与制表符
  - 4 个空格与一个显示宽度为 4 的制表符并**不是**同一缩进
- 一般使用 **4 空格**缩进，或者 **1 制表符**缩进
- 缩进有误的报错为 `IndentationError`

### 4.4 循环

#### 1. while 循环

- 条件检查，如果为 True 则继续运行，直到 False 停止

```python
while condition:
    ...
```

#### 2. for 循环

~~~ python
for value in list:
for value in range(a, b, c):
~~~

- python 中 for 循环是遍历一个可迭代对象
- for 循环会产生一个用于循环的变量，这个变量在循环结束后并不会删除，而是保留最后一次的值
- 可以使用 `range` 来生成一串数字用来循环
  - `range(a, b, c)` 以 c 为步长生成从 a 到 b-1 的连续整数
  - range 得到的并不是列表，如果要生成列表要用 `list(range(...))`

#### 3. 控制循环

- `break` 立刻结束循环
- `continue` 立刻进行下一轮循环

#### 4. 技巧

##### 1. 遍历字典

```python
for key in dictionary.keys( ): # 遍历所有键
for value in dictionary.values( ): # 遍历所有值
for item in dictionary.items( ): # 遍历键值对（需要解包）item是一个元组，对应dictionary中的一个键值对
for item_key, item_value in dictionary.items( ): # 把key赋给item_key，value赋给item_value
```

##### 2. 元素解包

- 赋值时等号左侧可以是<u>用逗号分隔的多个值</u>，这时会将右侧解包分别赋值给左侧的各个变量

- 右侧也可以是多个值（只要出现逗号就会视为一个元组）

  - 可以通过 a, b = b, a 实现元素交换

  ```python
  t = (1, 2, 3)
  a, b, c = t # a = 1, b = 2, c = 3
  t = (1, 2, (3, 4))
  a, b, (c, d) = t # c = 3, d = 4
  ```

- 星号表达式

  - 用来在可迭代对象内部**解包**，也可用来**标记**一个变量包含多个值

    ```python
    l = [1, 2, *[3, 4]] # [3, 4] 被解包, l = [1, 2, 3, 4]
    a, *b = [1, 2, 3, 4] # a = 1, b = [2, 3, 4]
    ```

- for 循环可以解包

  ```python
  lst = [[1, 2], [3, 4]]
  for a, b in lst:
      # 第一次循环 a, b 为 1, 2
      # 第二次循环 a, b 为 3, 4
  ```

##### 3. for 循环技巧


- **enumerate** 计数

  - 可以指定初始值

  ```python
  for i, value in enumerate(lst): # i 依次为 0，1，2，……
  for i, value in enumerate(lst, 1): # i 依次为 1，2，3，……
  ```

- **zip** 同时循环多个可迭代对象

  - 循环次数为**最短的对象的长度**

  ```python
  for a, b in zip(lst1, lst2): # a 在 lst1 中循环，b 在 lst2 中循环
  ```

##### 4. 列表推导

```python
列表 = [表达式 for 变量 in 可迭代对象]
列表 = [表达式 for 变量 in 可迭代对象 if 条件]
列表 = [表达式 for 变量1 in 可迭代对象1 for 变量2 in 可迭代对象2]
```

- 列表中包含循环，逐次记录循环前表达式的值

  ```python
  lst = []
  for i in range(1, 10):
      lst.append(i**2)
  # 等价于
  lst = [i**2 for i in range(1, 10)]
  ```

- 多重循环，即生成笛卡尔积

  ```python
  l1 = [1, 2, 3]
  l2 = [3, 4, 7]
  for x in l1:
      for y in l2:
          lst1.append(x * y)
  # 等价于
  lst = [x*y for x in l1 for y in l2]
  ```

- 包含条件，即在条件成立时才记录值

  ```python
  lst2 = [i ** 2 for i in range(1, 10) if i % 2 == 0]
  ```

##### 5/ 生成元组/字典

> 与列表推导类似

- 生成元组要用 `tuple( )`

  - `( )` 只是生成器表达式

  ```python
  tuple(i**2 for i in range(1, 10))
  (i**2 for i in range(1, 10))
  ```

- 生成字典时循环前用 `:`将键值隔开

  ```python
  {a: b for a in ... for b in ... }
  ```

## 五. 函数

### 5.1 函数定义

~~~python
def function_name(arg):
    function
    return value
~~~

### 5.2 函数的参数

```python
def func(arg1, arg2): 
    # 括号中要列出参数名，供函数体内使用
def func(arg1, arg2 = "...", "..."): 
    # 可赋默认值  
def func(arg, *args, **kwargs): 
    # *args 接收任意多参数（元组）, **kwargs 接收任意多关键字参数（字典）
```

* 关于`def func(**kwargs)`，在调用时的格式为`func(name = "ZJU", number = 67656)`
  （区别于字典的格式`kwargs = {"name": "ZJU", "number": 67656}`）

### 5.3 函数的返回值

- 没有 return 或 return 后不接参数，返回 `None`
- `return a`：返回a（a的类型不受限制）
- `return a, b, c`：返回多个参数

### 5.4 函数调用

- 直接传参的话要将参数与定义对应上

- 通过**关键字传参**可以打乱顺序

- 带有默认值的参数如果不传则使用**默认值**

  ```python
  def func(a, b, c, d):
      ...
  
  func(1, 2, 3, 4) # 位置参数-默认使用形式
  func(b = 2, c = 3, a = 1, d = 4) # 关键字参数
  func(3, 4, b = 1, a = 2) # 混合使用
  ```

- 如果读任意多关键字参数，则多余的读到字典中

  ```python
  def func2(a, **b):
      ...
  
  func2(a=1, b=2, c=3)
  # a = 1, b = {"b": 2, "c": 3}
  ```

### 5.5 引用变量

- python 中的变量都是==**引用**==的（变量是**标签**而不是盒子，可理解为“**指针**“）

- 用 = 实际上是定义了一个别名

  ```python
  a = [1, 2, 3]
  b = a
  ```

  * 此处`a` 是贴在列表上的一个标签， `b = a` 就是给该列表贴了另一个标签 `b`
  * 修改`a`后，`b`的值也会变化

- 复制操作

  * 使用`[:]`或`copy()`

  ```python
  a = [1, 2, 3]
  b = a[:]  # 创建了一个新的副本
  c = a.copy() # 创建了一个新的副本
  ```

* 对于数字、字符串、布尔值这些“不可变”的类型

  ```python
  x = 5
  y = x
  x = 10
  print(y)  # 输出：5，y 没有跟着变
  ```

  这是因为数字是“不可变”的，无法改变 5 的值，只能让 `x` 指向另一个数

* `==` 和 `is` 的区别

  * `==`比较值的大小，`is`比较内存地址是否相同

  ```python
  a = [1, 2, 3]
  b = [1, 2, 3]
  print(a == b)  # True，值是一样的
  print(a is b)  # False，是两个不同的列表对象
  ```

---

#### 函数参数是“共享引用”

在 Python 中，函数传参本质上是“**共享了同一个引用**”。

* For example：

  ```python
  def change_list(lst):
      lst.append(4)
  
  my_list = [1, 2, 3]
  change_list(my_list)
  print(my_list)  # 输出：[1, 2, 3, 4]
  ```

* 因为 `lst` 和 `my_list` 指向同一个列表

如果不希望函数修改原始数据，可以**传入一个副本**

```python
def change_list(lst):
    lst.append(4)

my_list = [1, 2, 3]
change_list(my_list[:])  # 把副本传进去
print(my_list)  # 输出：[1, 2, 3]，没有被修改
```

### 5.6 匿名函数

```python
lambda 传入参数:函数体
```

- 可以将一个函数赋值给一个变量
- 避免用 lambda 赋值的形式定义函数
  - 例如 `_name_ `属性不会是函数名，而是 `<lambda>`

## 六. 文件

### 6.1 路径

* 绝对路径
* `home/User/Desktop/Python.txt`
* 相对路径
  * `./User/Desktop/Python.txt` 以当前位置为参考
  * `..` 相对当前位置的上一级文件
  * `.. \ ..` 相对当前位置的上上级文件

### 6.2 文件操作

#### 1. 打开文件

```python
open(name, mode ,encoding)
```

> name：目标文件名的字符串（或具体路径），mode：打开模式，encoding：编码格式

* `f = open("./data.tex", "r", encoding = "utf-8")`
* 打开成功后返回一个**文件对象**

- | 打开模式 | 作用                                                        |
  | :------: | :---------------------------------------------------------- |
  |    r     | 读取（默认）                                                |
  |    w     | 写入（文件已存在则**清空内容** / 文件不存在则**创建**）     |
  |    a     | 添加（文件已存在则**末尾追加内容** / 文件不存在则**创建**） |

#### 2. 读取文件

* `f.read( )` 读取全部内容，`f.read(x)` 读取 x 个字节
* `f.readline( )` 读取一行的内容
* `f.readlines()` 读取所有行，返回一个列表

每次read后会**记录**读到的位置，类比指针

~~~ python
f = open("./data.tex", "r", encoding = "utf-8")
lines = f.readlines()
for line in lines:
    print(line)
~~~

#### 3. 关闭文件

* 使用`f.close( )`关闭打开的文件
* `with` 块
  * with 块开始时自动打开文件，结束自动关闭文件且**保存变量**

```python 
with open("file", "r", encoding="utf-8") as f:
    for line in f:
        print(f"This line is{line}")
```

#### 4. 写入文件

* `f.write(string)`：直接写入string（不会自动换行）
* `f.writelines(list)`：传入列表，元素间换行写入
* `f.flush()`：刷新文件，写入数据（`f.close()`内置了刷新功能）

```python 
f = open("filename", "w", encodeing="utf-8")
f.write("Hello ZJU!")
f.writelines(["Hello", "ZJU", 67656])
...
f.close()
```

## 七. 异常

- 产生错误 -> 抛出异常 -> 程序结束
- 异常具有**传递性**

### 捕获异常

- try-except 块

  ```python
  try:
  可成出现错误的代码
  except:
      上述代码出错后执行的代码
  ```

- finally 语句

  - 不管是否有异常**都会**运行

~~~ python
try:
    a = int(input("请输入a："))
    b = int(input("请输入b："))
    rate = a / b
except (NameError, ValueError): # 捕获多个异常
	print("输入有误")
except ZeroDivisionError as e: # 将e作为一个对象
    print("b的值不能为零")
    print(e)
except Exception: # 捕获全部异常
    print("发生错误，请重新输入")
else: # 如果不存在异常则执行
    print("没有异常")
    print("rate = %d" %(rate))
finally:
    print("程序结束")
~~~

## 八. 模块

- 模块可以是一个单独的Python文件，也可以是一个文件夹

  * **包**：包含一个`__init.py__`文件和多个模块文件

  * 调用方式

    1. `package.module4.func3()`（调用`package`文件夹中`module4.py`中的函数`func3`）

    2. ```python
       ## __init__.py
       __all__ = ["my_module2"]
       ```

       ```python
       from my_package import *
       my_module2.func1()
       ```

- 导入方式

  ```python
  [from 模块名] import [模块|类|变量|函数|*] [as 别名]
  ```

- 导入时相当于运行了一遍导入的代码

  ```python
  ## code.py
  def f():
      print("call func in code.py")
  ```

  ```python
  import code 
  code.f() # 模块名.功能名()
  import code as cd 
  cd.f() # 别名.功能名()
  from code import f 
  f() # 单独导入具体功能
  from code import * 
  f() # 导入所有功能
  ```

### 8.1 `__main__`

在 Python 中，每个模块都有一个内置变量 `__name__`，它的值取决于这个模块是如何被使用的：

|      使用方式      |      `__name__` 的值      |        说明        |
| :----------------: | :-----------------------: | :----------------: |
|   直接运行该模块   |       `"__main__"`        | 表示这是程序的入口 |
| 被其他模块导入使用 | 模块的名字（如 `"code"`） |     不是主程序     |

- 防止导入模块时运行模块内的测试代码

  ```python
  ## code.py
  def calculate(a, b):
      return a + b
  if __name__ == "__main__":
      print(calculate(1, 2))
  ```

### 8.2 `__all__`

* ```python
  ## code.py
  __all__ = ['func1']
  def func1(a, b):
      return a + b
  def func2(a, b):
      return a - b
  ```

* ```python
  from code import * # 导入所有功能
  ```

  * 此时仅能导入`func1`函数，`__all__`**仅作用在`*`上**

## 九. 类与对象

* 命名时采用Pascal命名法，**首字母大写**并用大写字母分隔单词

- 类包含**属性**和**方法**

```python
# 创建一个类
class Student:
    name = None
    school = None
# 创建对象并赋值
Bob = Student()
Bob.name = "Bob"
Bob.school = "ZJU"
```

### 9.1 属性

- **构造方法**

  * 创建类对象的时候自动执行
  * 创建类对象时，将传入参数自动传递给`__init__`方法使用（self**不可省略**）

- ```python
  # 创建一个类
  class Student:
      def __init__(self, name, school):
          self.name = name
          self.school = school
  # 创建对象并赋值        
  Bob = Student("Bob", "ZJU") 
  ```

### 9.2 方法

```python
def 方法名(self,形参1 ,形参2 ,..., 形参n):
    方法体
```

### 9.3 魔术方法

#### 1. 字符串方法

* 不使用

  ```python
  class Student():
      def __init__(self, name, id):
          self.name = name
          self.id = id   
  Bob = Student("Bob", 3240100000)
  print(Boy) # 返回Boy的内存地址
  print(str(Boy)) # 返回Boy的内存地址
  ```

* 使用后

  ```python
  class Student():
      def __init__(self, name, id):
          self.name = name
          self.id = id   
      def __str__(self):
          return f"Student类对象，姓名为{self.name}，学号为{self.id}"
      
  Bob = Student("Bob", 3240100000)
  
  print(Boy) # 返回：Student类对象，姓名为Bob，学号为3240100000
  print(str(Boy)) # 返回：Student类对象，姓名为Bob，学号为3240100000
  ```

#### 2. 比较方法

* `__lt__`用于小于/大于的比较

  ```python
  class Student():
      def __init__(self, name, age):
          self.name = name
          self.age = age 
      def __lt__(self, other):
          return self.age < other.age
      
  Bob = Student("Bob", 15)
  Alice = Student("Alice", 16)
  
  print(Boy < Alice) # 结果为True
  print(Boy > Alice) # 结果为False
  ```

* `__le__`用于小于等于/大于等于的比较

  ```python
  class Student():
      def __init__(self, name, age):
          self.name = name
          self.age = age 
      def __le__(self, other):
          return self.age <= other.age
      
  Bob = Student("Bob", 15)
  Alice = Student("Alice", 16)
  
  print(Boy <= Alice) # 结果为True
  print(Boy >= Alice) # 结果为False
  ```

* `__eq__`用于等于的比较

  * 未定义默认比较**内存地址**

  ```python
  class Student():
      def __init__(self, name, age):
          self.name = name
          self.age = age 
      def __eq__(self, other):
          return self.age += other.age
      
  Bob = Student("Bob", 15)
  Alice = Student("Alice", 16)
  
  print(Boy == Alice) # 结果为False
  ```

### 9.4 封装

> 将现实事物在类中描述为属性和方法，称为封装

* 私有成员

  * 私有成员变量：变量名以`__`开头

  * 私有方法变量：方法名以`__`开头
* 私有成员**无法**被类对象使用，但是可以被**其他的成员**使用。
* python中类并**没有严格私有的属性**
  * 双下划线开头的属性会被隐藏，不能直接读取
  * 但这种属性可以通过 `_类名__属性` 但方式读取到

```python
class Phone():
    __voltage = 0.6
    def __use_single_core(self):
        print("使用单核运行")
    def call_by_5G(self):
        if self.__voltage >= 1:
            print("5G已开启")
        else:
            self.__use_single_core()
            print("电量不足")
            
iphone = Phone()
iphone.call_by_5G()
print(iphone._Phone__voltage) # 输出0.6
```

### 9.5 继承

* 子类会继承父类的所有属性和方法

```python
class 类名(父类1,父类2,...,父类N):
    类内容体 # 没有内容则写"pass"
```

#### 1. 复写

* 采用和父类相同的成员名/方法名
  * 调用时会调用**复写后的新成员**

#### 2. 子类调用父类

- 使用 `super()`调用
  * `super().变量`，`super().成员方法()`

```python
class Student():
    def __init__(self, name, id):
        self.name = name
        self.id = id
    def print(self):
        print(f"The id of {self.name} is {self.id}")

class Boy(Student):
    def __init__(self, name, id, grade):
        super().__init__(name, id)
        self.grade = grade
        
Bob = Boy("Bob", 3240100000, 67656)
Bob.print()
print(Bob.grade)
```

* 使用父类名调用
  * `父类名.变量`，`父类名.成员方法(self)`

```python
class Boy(Student):
    def __init__(self, name, id, grade):
        Student.__init__(self, name, id)
        self.grade = grade
```

### 9.6 多态

* 多种状态，即完成某个行为时，使用不同的对象会得到不同的状态

抽象类（接口）

* 父类用来确定有哪些方法

* 具体的方法实现由子类来实现

  ```python
  class Animal():
      def speak(self):
          pass
      
  class Dog(Animal):
      def speak(self):
          print("汪汪汪") 
          
  class Cat(Animal):
      def speak(self):
          print("喵喵瞄")
  ```