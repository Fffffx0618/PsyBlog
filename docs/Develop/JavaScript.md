# JavaScript

## 1. 变量声明

| 特性             | `var`                          | `let`                        | `const`                       |
| ---------------- | ------------------------------ | ---------------------------- | ----------------------------- |
| **引入版本**     | JavaScript 早期                | ES6 (2015)                   | ES6 (2015)                    |
| **作用域**       | 函数作用域或全局作用域         | 块级作用域 `{}`              | 块级作用域 `{}`               |
| **提升行为**     | 声明提升，初始化为 `undefined` | 声明提升，进入 TDZ，未初始化 | 声明提升，进入 TDZ，未初始化  |
| **重复声明**     | 同一作用域内允许               | 同一作用域内不允许           | 同一作用域内不允许            |
| **重新赋值**     | 允许                           | 允许                         | 不允许（对象/数组内容可修改） |
| **声明时初始化** | 可选                           | 可选                         | 必须                          |

### 示例代码

#### `var`
```javascript
console.log(x); // 输出: undefined
var x = 5;
console.log(x); // 输出: 5
```

#### `let`
```javascript
console.log(y); // ReferenceError: TDZ
let y = 10;
console.log(y); // 输出: 10

if (true) {
  let z = 20;
  console.log(z); // 输出: 20
}
console.log(z); // ReferenceError
```

#### `const`
```javascript
const PI = 3.14159;
PI = 3.14; // TypeError

const MY_OBJECT = { key: "value" };
MY_OBJECT.key = "newValue"; // 允许
console.log(MY_OBJECT.key); // 输出: newValue
MY_OBJECT = { otherKey: "anotherValue" }; // TypeError
```

---

## 2. 数据类型

### 2.1 原始类型
- **Number**: 整数和浮点数（`Infinity`, `-Infinity`, `NaN`）
- **String**: 单引号、双引号或反引号（模板字符串）
- **Boolean**: `true` 和 `false`
- **Null**: 表示“空”或“无”
- **Undefined**: 未赋值变量
- **Symbol**（ES6）: 唯一标识符（`Symbol("key")`）
- **BigInt**（ES2020）: 任意精度整数（`123n`）

### 2.2 对象类型（Object Type）
- 键值对集合（`{ key: value }`）
- 特殊对象：数组（`[]`）、函数（`function`）、Map、Set 等

### 2.3 `typeof` 运算符
```javascript
typeof 42;          // "number"
typeof "hello";     // "string"
typeof true;        // "boolean"
typeof undefined;   // "undefined"
typeof { a: 1 };    // "object"
typeof [];          // "object"
typeof function() {}; // "function"
typeof null;        // "object"（历史遗留 bug）
typeof Symbol();    // "symbol"
typeof 123n;        // "bigint"
```

---

## 3. 运算符

### 算术运算符
- `+`, `-`, `*`, `/`, `%`, `**`, `++`, `--`
- `1 / 0` → `Infinity`；`0 / 0` → `NaN`

### 赋值运算符
- `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `**=`

### 比较运算符
- `==`（宽松相等，类型转换） vs `===`（严格相等，推荐）
- `!=`（宽松不等） vs `!==`（严格不等，推荐）
- `>`, `>=`, `<`, `<=`

### 逻辑运算符
- `&&`（逻辑与）、`||`（逻辑或）、`!`（逻辑非）
- **短路行为**：返回决定结果的操作数的值（非布尔值）
```javascript
const result = 0 || 10; // 返回 10
```

### 位运算符
- `&`, `|`, `^`, `~`, `<<`, `>>`, `>>>`（无符号右移）

### 三元运算符
```javascript
const value = condition ? exprIfTrue : exprIfFalse;
```

### `instanceof` 运算符
```javascript
const arr = [];
arr instanceof Array; // true
```

---

## 4. 控制流程

### 4.1 条件语句

#### `if...else`
```javascript
let accessLevel = "user";
let isLoggedIn = true;

if (accessLevel === "admin") {
  console.log("完全访问权限");
} else if (accessLevel === "user" && isLoggedIn) {
  console.log("受限访问权限");
} else {
  console.log("未知访问级别");
}
```

#### `switch`
```javascript
let dayOfWeek = 3;
let dayName;

switch (dayOfWeek) {
  case 1:
    dayName = "星期一";
    break;
  case 3:
    dayName = "星期三";
    break;
  default:
    dayName = "无效日期";
}
console.log(dayName); // 输出: 星期三
```

### 4.2 循环结构

#### `for`
```javascript
for (let i = 0; i < 3; i++) {
  console.log(`迭代: ${i}`);
}
```

#### `while`
```javascript
let count = 0;
while (count < 2) {
  console.log(`While 计数: ${count}`);
  count++;
}
```

#### `do...while`
```javascript
let num = 5;
do {
  console.log(`Do...while, num = ${num}`);
  num++;
} while (num < 5); // 执行一次
```

#### `break` 和 `continue`
```javascript
for (let i = 0; i < 10; i++) {
  if (i % 2 === 0) continue;
  if (i > 5) break;
  console.log(i); // 输出: 1, 3, 5
}
```

### 4.3 特有循环

#### `for...in`（遍历对象键）
```javascript
const car = { make: "Toyota", model: "Camry" };
for (const prop in car) {
  if (Object.hasOwn(car, prop)) {
    console.log(`${prop}: ${car[prop]}`);
  }
}
// 输出:
// make: Toyota
// model: Camry
```

#### `for...of`（遍历可迭代值）
```javascript
const colors = ["red", "green", "blue"];
for (const color of colors) {
  console.log(color); // red, green, blue
}

const message = "Hi";
for (const char of message) {
  console.log(char); // H, i
}
```

---

## 5. 函数

### 5.1 定义函数

#### 函数声明
```javascript
function add(a, b) {
  return a + b;
}
```

#### 函数表达式
```javascript
const multiply = function(a, b) {
  return a * b;
};
```

#### 箭头函数
```javascript
const subtract = (a, b) => a - b;
const greet = name => `Hello, ${name}!`;

const complexCalculation = (a, b) => {
  const temp = a + b;
  return temp * 2;
};
```

### 5.2 调用函数
```javascript
function logMessage(message, level = "INFO") {
  console.log(`[${level}] ${message}`);
}
logMessage("User logged in."); // [INFO] User logged in.
```

### 5.3 返回值
- `return value;`（无 `return` 或 `return;` 则返回 `undefined`）

### 5.4 作用域与闭包
```javascript
function createCounter() {
  let count = 0;
  return function increment() {
    count++;
    return count;
  };
}
const counterA = createCounter();
console.log(counterA()); // 1
console.log(counterA()); // 2
```

---

## 6. 使用对象

### 6.1 创建对象

#### 对象字面量
```javascript
const person = {
  firstName: "John",
  lastName: "Doe",
  age: 30,
  greet() {
    console.log(`Hello, my name is ${this.firstName}`);
  }
};
```

#### 构造函数
```javascript
function Car(make, model, year) {
  this.make = make;
  this.model = model;
  this.year = year;
}
const myCar = new Car("Ford", "Mustang", 1969);
```

#### ES6 `class` 语法
```javascript
class Vehicle {
  constructor(type, wheels) {
    this.type = type;
    this.wheels = wheels;
  }
  startEngine() {
    console.log(`${this.type} engine started.`);
  }
}
const truck = new Vehicle("Truck", 6);
```

#### `Object.create()`
```javascript
const animalPrototype = {
  makeSound() { console.log("Generic sound"); }
};
const dog = Object.create(animalPrototype);
dog.breed = "Labrador";
dog.makeSound(); // Generic sound
```

### 6.2 访问与修改属性
```javascript
console.log(person.firstName); // John
person.age = 31;
let prop = "lastName";
console.log(person[prop]); // Doe
person["country"] = "USA";
delete person.age;
```

---

## 7. JavaScript 数组

### 7.1 创建数组
```javascript
const numbers = [1, 2, 3, 4, 5];
const mixedArray = [10, "hello", true];

const arr1 = new Array(3); // [empty × 3]
const arr2 = new Array("a", "b", "c"); // ["a", "b", "c"]
```

### 7.2 访问与修改
```javascript
const colors = ["red", "green", "blue"];
colors[1] = "yellow"; // ["red", "yellow", "blue"]
colors[3] = "purple"; // ["red", "yellow", "blue", "purple"]

colors.length = 2; // 截断为 ["red", "yellow"]
```

### 7.3 常用数组方法

#### 修改原数组
- `push()`, `pop()`, `shift()`, `unshift()`, `splice()`, `sort()`, `reverse()`

#### 不修改原数组
- `slice()`, `concat()`, `join()`, `indexOf()`, `lastIndexOf()`, `includes()`

#### 迭代方法
- `forEach()`, `map()`, `filter()`, `reduce()`

---

## 8. DOM 与事件

### 8.1 选择元素
```javascript
const introP = document.getElementById('intro');
const firstLink = document.querySelector('a');
const allLinks = document.querySelectorAll('a');
```

### 8.2 修改元素
```javascript
// 内容
introP.textContent = "New text";
introP.innerHTML = "<strong>New HTML</strong>";

// 属性
firstLink.href = "https://example.com";
firstLink.setAttribute('target', '_blank');

// 样式
introP.style.color = 'blue';
introP.classList.add('highlight');
```

### 8.3 事件处理
```javascript
const btn = document.getElementById('myButton');

btn.addEventListener('click', (event) => {
  console.log('Button clicked!', event.target);
});
```

---

## 9. 异步特性

### 9.1 事件循环
- 单线程模型，通过事件循环实现非阻塞异步
- 调用栈 → 回调队列 → 事件循环调度

### 9.2 异步机制

#### 回调函数
```javascript
console.log("Start");
setTimeout(() => {
  console.log("Timeout callback (after 1s)");
}, 1000);
console.log("End (this runs before callback)");
```

#### Promise
```javascript
fetch('https://api.example.com/data')
  .then(response => response.json())
  .then(data => console.log("Data:", data))
  .catch(error => console.error("Error:", error));
```

#### `async/await`
```javascript
async function fetchData() {
  try {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    console.log("Data (async/await):", data);
  } catch (error) {
    console.error("Error (async/await):", error);
  }
}
fetchData();
```

# 开发

## 1. 文档对象模型（DOM）脚本

- **文档对象模型（DOM）**：一种API，用于表示和操作HTML或XML文档。它允许开发者通过编程方式访问和修改文档结构、样式和内容。
- **JavaScript与CSS交互**：
  - JavaScript中的CSS属性名采用小驼峰命名法（如`backgroundColor`），而CSS中则使用连字符分隔（如`background-color`）。
  - 使用`Element.setAttribute()`方法动态地为元素设置类名以应用预定义的CSS样式。
- **实际用途示例**：
  - 动态创建并操作页面元素，例如构建一个购物清单应用，允许用户添加或删除列表项。
  - 不建议用JavaScript来创建静态内容，因为这会增加复杂性，并可能带来SEO方面的问题。

创建并添加段落

```javascript
// 获取section元素的引用
const sect = document.querySelector("section");

// 创建一个新的段落元素
const para = document.createElement("p");
para.textContent = "We hope you enjoyed the ride.";

// 将新创建的段落追加到section中
sect.appendChild(para);

// 创建文本节点，并将其添加到段落中
const text = document.createTextNode(" — the premier source for web development knowledge.");
const linkPara = document.querySelector("p");
linkPara.appendChild(text);
```

删除段落

```javascript
// 假设要删除具有内部链接的段落
sect.removeChild(linkPara); // 使用父节点的方法删除
linkPara.remove(); // 直接删除自身
```

## 2. 网络请求与数据处理

- **网络请求的重要性**：传统网页需要重新加载整个页面来更新部分内容，效率低下。现代Web应用通过使用JavaScript API（如Fetch API）仅请求必要的数据来更新页面部分，从而提高效率和用户体验。

- **Fetch API**：用于发起HTTP请求并处理响应的现代化API，支持异步操作。可以通过`.then()`和`.catch()`链式调用来处理成功和错误情况。
  - 示例代码：从服务器获取数据并更新页面。
    ```javascript
    // 定义一个函数 updateDisplay，接收参数 verse（诗句名称）
    function updateDisplay(verse) {
        // 去除字符串中的空格，并将字母全部转为小写，用于构建文件名
        verse = verse.replace(" ", "").toLowerCase();
    
        // 构建请求的 URL，格式为：[处理后的verse值].txt
        const url = `${verse}.txt`;
    
        // 使用 Fetch API 发起 HTTP 请求，获取对应的文本内容
        fetch(url)
            // 第一个 .then() 处理响应对象
            .then((response) => {
                // 检查响应是否成功（状态码 200-299）
                if (!response.ok) {
                    // 如果不成功，抛出错误，包含状态码信息
                    throw new Error(`HTTP error: ${response.status}`);
                }
    
                // 如果成功，返回响应体的文本内容
                return response.text();
            })
            // 第二个 .then() 接收文本内容作为参数
            .then((text) => {
                // 将获取到的文本内容显示在页面上的 <pre> 元素中
                poemDisplay.textContent = text;
            })
            // .catch() 捕获并处理整个过程中可能发生的任何错误
            .catch((error) => console.error(error));
    }
    
    // 获取页面中 <select> 元素（下拉选择框），用于选择诗句
    const verseChoose = document.querySelector("select");
    
    // 获取页面中 <pre> 元素，用于显示获取到的诗句内容
    const poemDisplay = document.querySelector("pre");
    
    // 为下拉框添加 change 事件监听器
    verseChoose.addEventListener("change", () => {
        // 当选项改变时，获取当前选中的值（即诗句名称）
        const verse = verseChoose.value;
    
        // 调用 updateDisplay 函数，传入选中的值，更新显示内容
        updateDisplay(verse);
    });
    ```

1. 用户从 `<select>` 下拉菜单中选择一个诗句名称。
2. `verseChoose.addEventListener("change")` 监听到变化后，获取选中值。
3. 调用 `updateDisplay(verse)` 函数，根据选中值构造 `.txt` 文件路径。
4. 使用 `fetch()` 向服务器发起请求，获取对应文本内容。
5. 成功获取后，将内容插入到 `<pre>` 标签中展示。
6. 若请求失败，则通过 `.catch()` 输出错误信息。

## 3. JSON基础

- **JSON（JavaScript Object Notation）**：JSON 是一个字符串，其格式非常类似于 JavaScript 对象字面量的格式。你可以在 JSON 中包含与标准 JavaScript 对象相同的基本数据类型——字符串、数字、数组、布尔值和其他对象字面量。这使你可以构建一个数据层次结构，如下所示：

  ```json
  {
    "squadName": "Super hero squad",
    "homeTown": "Metro City",
    "formed": 2016,
    "secretBase": "Super tower",
    "active": true,
    "members": [
      {
        "name": "Molecule Man",
        "age": 29,
        "secretIdentity": "Dan Jukes",
        "powers": ["Radiation resistance", "Turning tiny", "Radiation blast"]
      },
      {
        "name": "Madame Uppercut",
        "age": 39,
        "secretIdentity": "Jane Wilson",
        "powers": [
          "Million tonne punch",
          "Damage resistance",
          "Superhuman reflexes"
        ]
      },
      {
        "name": "Eternal Flame",
        "age": 1000000,
        "secretIdentity": "Unknown",
        "powers": [
          "Immortality",
          "Heat Immunity",
          "Inferno",
          "Teleportation",
          "Interdimensional travel"
        ]
      }
    ]
  }
  
  ```

  

- **验证JSON**：确保JSON数据的有效性非常重要，可以使用在线工具如JSONLint来进行验证。

- **利用JSON数据**：在Web开发中，JSON常用于从服务器获取数据并在客户端动态展示这些数据。
  - 示例代码：使用Fetch API获取包含商品信息的JSON文件，并在网页上显示这些商品的信息。
    ```javascript
    fetch('products.json')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    ```

