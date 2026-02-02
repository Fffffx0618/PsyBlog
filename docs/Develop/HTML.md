# HTML

## 1. 基本结构

每个HTML文档都遵循一个基本的结构，以确保浏览器能够正确解析和显示页面内容。这个结构由几个关键的标签组成。

### `<!DOCTYPE html>`：文档类型声明

`<!DOCTYPE html>` 声明必须是HTML文档的第一行 。它告知浏览器该文档使用的是HTML5标准。虽然在HTML早期版本中，DOCTYPE声明更为复杂，用于链接到特定的HTML规则集，但在HTML5中，它被大大简化，主要作用是确保浏览器以标准模式渲染页面。

### `<html>`

HTML文档的根元素，包裹了页面上的所有其他内容。它通常包含一个 lang 属性，用于指定文档的主要语言，例如 `<html lang="zh-CN">` 表示中文。

### `<head>`：文档元数据

包含了关于HTML文档的元数据（meta-information），这些信息不会直接显示在页面上，但对浏览器、搜索引擎和其他Web服务非常重要。

- `<meta charset="UTF-8">`: 指定文档的字符编码。UTF-8 是一种通用的字符集，支持几乎所有语言的字符，强烈推荐使用。
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`: 控制页面在移动设备上的视口（viewport）设置，是实现响应式网页设计的关键。`width=device-width` 将视口宽度设置为设备宽度，`initial-scale=1.0` 设置初始缩放级别。
- `<title>`: 定义浏览器标签页或窗口标题栏中显示的文档标题。

### `<body>`：可见页面内容

包含了HTML文档中所有用户可见的内容，如文本、图片、链接、视频、列表、表格等。大部分HTML标签都将放置在 `<body>` 标签内部。

###  一个基本的HTML页面结构示例：

下面是一个最基础的HTML页面结构：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的第一个网页</title>
</head>
<body>
    </body>
</html>
```

## 2. 元素、标签和属性

理解HTML元素、标签和属性之间的关系是掌握HTML的关键。

###  HTML元素 (Elements)

HTML文档由HTML元素构成。一个HTML元素通常由一个**开始标签 (start tag)**、**内容 (content)** 和一个**结束标签 (end tag)** 组成。
例如，一个段落元素由 <u>`<p>`（开始标签）、段落文本（内容）和 `</p>`（结束标签）</u>组成。元素是网页的基本构建块，用于表示不同类型的内容。

### HTML标签 (Tags)

标签是用来标记HTML元素开始和结束的关键词，用尖括号 `< >` 包围。

- **开始标签 (Opening Tag):** 标记元素的开始，如 `<p>`、`<h1>`。
- **结束标签 (Closing Tag):** 标记元素的结束，与开始标签类似，但在元素名前加一个正斜杠 `/`，如 `</p>`、`</h1>`。
  * 标签名不区分大小写，但在XHTML等更严格的文档类型中强制使用小写。保持一致的小写风格有助于提高代码的可读性和一致性。

### 内容 (Content)

内容是位于开始标签和结束标签之间的实际信息，例如段落中的文本、列表中的项目等。

- **空元素 (Void Elements / Empty Elements)**

  有些HTML元素没有内容，因此**只有一个开始标签，没有结束标签**，这些被称为***空元素或虚元素***。它们通常用于在文档中插入某些内容或执行特定功能。

  - **示例:** `<img>` (图像), `<br>` (换行), `<hr>` (水平线), `<input>` (输入字段), `<meta>` (元数据)。
  - 在HTML5中，空元素可以自闭合（例如 `<img src="image.jpg" alt="描述">`），也可以不自闭合。但在XHTML中，它们必须自闭合（例如 `<img src="image.jpg" alt="描述" />`） 13。

- **嵌套元素 (Nested Elements)**

  HTML元素可以嵌套在其他元素内部，形成层级结构。例如，`<body>` 元素嵌套在 `<html>` 元素内，而 `<p>` 元素可以嵌套在 `<body>` 元素内。

  * 内部元素必须在外部元素关闭之前关闭。

### 属性 (Attributes)

  属性为HTML元素提供附加信息或配置选项。

  - 属性总是写在**开始标签**中。
  - 属性通常以**名称/值对**的形式出现，如 `name="value"`。
  - 属性值应该用引号（单引号或双引号）括起来，尤其当属性值包含空格时，引号是必需的。。
  - **示例:** 在 `<a href="https://www.example.com">访问示例网站</a>` 中，`href` 是 `<a>` 元素的属性名，`"https://www.example.com"` 是属性值。在 `<img src="image.jpg" alt="描述图片">` 中，`src` 和 `alt` 都是属性。

- **全局属性 (Global Attributes)**

  全局属性是可以应用于所有HTML元素的通用属性。它们为元素提供了通用的功能和标识。

  **常见的全局HTML属性**

| **属性名** | **描述/用途**                                                | **示例用法**                                            |
| ---------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| `id`       | 为元素定义一个唯一的标识符。在整个文档中必须是唯一的。       | `<p id="intro">这是介绍段落。</p>`                      |
| `class`    | 为元素指定一个或多个类名（用空格分隔）。多个元素可以共享同一个类名。 | `<p class="highlight important">重要高亮文本。</p>`     |
| `style`    | 用于向元素应用内联CSS样式。                                  | `<p style="color:blue; font-size:16px;">蓝色文本。</p>` |
| `title`    | 提供关于元素的额外信息，通常在鼠标悬停时显示为工具提示。     | `<abbr title="超文本标记语言">HTML</abbr>`              |
| `lang`     | 指定元素内容的语言代码。                                     | `<p lang="en">Hello world!</p>`                         |

## 3. 构建模块

掌握了HTML的基本结构和核心概念后，接下来我们将学习用于构建实际网页内容的各种基本HTML标签。

### 标题 (`<h1>` 到 `<h6>`)

HTML提供了六个级别的标题标签，用于定义内容的层级结构 。

- 通常，每个页面只应包含一个 `<h1>` 标签，用于页面的主要标题 。
- 应按逻辑顺序使用标题级别，不要跳级。

- 代码示例:

  ```html
  <h1>我的主页标题</h1>
  <h2>主要章节标题</h2>
  <h3>章节内小节标题</h3>
  ```

#### 段落 (`<p>`)：组织文本内容

`<p>` 标签用于定义一个段落的文本。浏览器通常会在段落前后添加一些空白（外边距），以区分不同的段落。


- 代码示例:

  ```html
  <p>这是一个简单的文本段落。它包含了关于某个主题的一些信息。</p>
  ```

### 创建链接 (`<a>`)

`<a>` 标签（anchor，锚点）用于创建超链接，使用户能够从一个页面跳转到另一个页面，或跳转到同一页面内的不同位置。

- **`href` 属性:** 这是 `<a>` 标签最重要的属性，用于指定链接的目标URL（统一资源定位符）。URL可以是绝对路径（指向其他网站的完整地址）或相对路径（指向同一网站内的文件或位置）。

- **链接文本:** 位于 `<a>` 和 `</a>` 标签之间的内容将成为用户可以点击的链接文本。

- `target` 属性:

   控制链接如何在浏览器中打开。常见的值有：

  - `_self`: (默认值) 在当前窗口或标签页中打开链接。
  - `_blank`: 在新的窗口或标签页中打开链接。

- **`title` 属性:** 提供关于链接的额外信息，通常在鼠标悬停在链接上时以工具提示的形式显示 。

- **页面内锚点链接:** 可以使用 `href="#idName"` 的形式链接到同一页面内具有特定 `id` 的元素。

- **可访问性:** 应使用具有描述性的链接文本，避免使用像“点击这里”这样的通用短语，以帮助用户（尤其是使用屏幕阅读器的用户）理解链接的目的 。

- 代码示例:

  ```html
  <a href="https://www.mozilla.org" target="_blank" rel="noopener noreferrer" title="访问 MDN Web Docs">访问 MDN 学习 HTML</a>
  <a href="#section2">跳转到第二节</a>
  ```

### 嵌入图像 (`<img>`)

`<img>` 标签用于在HTML文档中嵌入图像 。这是一个空元素，意味着它只有开始标签，没有结束标签。

- **`src` 属性 (source):** 必需属性，指定图像文件的路径或URL。

- **`alt` 属性 (alternative text):** 必需属性，为图像提供替代文本。当图像无法显示（例如，路径错误、网络问题）或用户使用屏幕阅读器时，将显示或读出 `alt` 文本。良好的 `alt` 文本应简洁地描述图像的内容和功能。

- **`width` 和 `height` 属性:** 指定图像的宽度和高度（通常以像素为单位）。在图像加载之前，浏览器可以根据这些尺寸预留空间，从而防止页面布局在图像加载过程中发生跳动。

- 代码示例:

  ```html
  <img src="images/logo.png" alt="网站Logo" width="150" height="50">
  ```

### 列表（`<ul>`）

列表用于将相关项目组合在一起显示。HTML主要支持两种类型的列表：

- **无序列表** (`<ul>`): 用于列出顺序不重要的项目，通常以项目符号（如圆点）显示 4。

- **有序列表** (`<ol>`):用于列出顺序很重要的项目，通常以数字或字母（如 1, 2, 3 或 A, B, C）显示。

   - `start`: 指定列表项开始的数字（例如 `start="5"` 使列表从5开始计数）。
- `reversed`: 使列表项倒序排列。
  - `type`: 指定编号类型（如 `type="A"` 表示大写字母，`type="i"` 表示小写罗马数字）。

- **列表项 (`<li>` ):** 定义 `<ul>` 或 `<ol>` 中的每一个列表项 4。

- **嵌套列表:** 列表可以嵌套在其他列表项中，形成多级列表。

- 代码示例:

  ```html
  <p>我喜欢的水果：</p>
  <ul>
    <li>苹果</li>
    <li>香蕉</li>
    <li>橙子</li>
  </ul>
  
  <p>制作三明治的步骤：</p>
  <ol type="1" start="1">
    <li>准备两片面包。</li>
    <li>在面包上涂抹黄油。</li>
    <li>加入你喜欢的馅料。
      <ul>
        <li>生菜</li>
        <li>番茄</li>
        <li>火腿</li>
      </ul>
    </li>
    <li>盖上另一片面包。</li>
  </ol>
  ```

### 表格 (`<table>`) 

用于创建表格，以行和列的形式展示数据。


- `<table>`: 表格的容器。
- `<tr>` (Table Row): 定义表格中的一行。
- `<th>` (Table Header): 定义表头单元格，通常用于列标题或行标题。其内容默认会加粗并居中显示。为了增强可访问性，应配合使用 `scope` 属性，如 `scope="col"` (表示该表头对应一列) 或 `scope="row"` (表示该表头对应一行)。
- `<td>` (Table Data): 定义表格中的一个数据单元格。
- `<caption>`: 为表格提供一个标题，描述表格的内容。
- `<thead>`, `<tbody>`, `<tfoot>`: 分别用于对表头、表主体和表注脚内容进行分组，有助于组织大型表格的结构，并允许独立滚动表体。
- `colspan` 和 `rowspan` 属性: 分别用于让单元格横跨多列或多行 28。

- 代码示例:

  ```html
  <table border="1"> <caption>每月销售额</caption>
    <thead>
      <tr>
        <th scope="col">月份</th>
        <th scope="col">销售额 (元)</th>
        <th scope="col">备注</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th scope="row">一月</th>
        <td>10,000</td>
        <td>新年促销</td>
      </tr>
      <tr>
        <th scope="row">二月</th>
        <td>12,000</td>
        <td rowspan="2">春节活动</td> </tr>
      <tr>
        <th scope="row">三月</th>
        <td>15,000</td>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <td colspan="2">总计 (第一季度)</td> <td>37,000</td>
      </tr>
    </tfoot>
  </table>
  ```

### 使用表单 (`<form>`) 进行用户输入

HTML表单用于收集用户的输入信息。

- `<form>`: 表单的容器元素。关键属性包括：
  
  - `action`: 指定当表单提交时，数据发送到的服务器端URL。
  - `method`: 指定提交表单数据时使用的HTTP方法，通常是 `GET` 或 `POST` 22。
  
- `<input>`: 最通用的表单元素，可以通过`type`属性创建多种不同类型的输入控件,常见的值包括：
  
  - `text`: 单行文本输入框。
  - `password`: 密码输入框（输入内容通常被隐藏）。
  - `email`: 邮箱地址输入框（通常带有基本的格式验证）。
  - `number`: 数字输入框。
  - `checkbox`: 复选框（允许用户选择一个或多个选项）。
  - `radio`: 单选按钮（允许用户从一组选项中选择一个）。
  - `submit`: 提交按钮，用于提交表单数据。
  - `file`: 文件选择控件，用于上传文件。
  - 其他重要属性: `name` (对于数据提交至关重要，作为键值对的键名), `id` (用于与 `<label>` 关联), `value` (输入控件的初始值或提交值), `placeholder` (输入框中的提示文本), `required` (表示该字段为必填项)。

- `<label>`: 为表单输入控件提供描述性标签。使用 `for` 属性与对应输入控件的 `id` 属性相关联，可以提高表单的可访问性（例如，点击标签可以聚焦到对应的输入框）。

- `<button>`: 创建可点击的按钮。`type` 属性可以设置为 `submit` (提交表单), `reset` (重置表单内容), 或 `button` (通用按钮，通常配合JavaScript使用) 22。

- `<textarea>`: 用于多行文本输入。

- `<select>` 和 `<option>`: 用于创建下拉选择列表。

- 代码示例:

  ```html
  <form action="/submit-feedback" method="post">
    <div>
      <label for="name">姓名:</label>
      <input type="text" id="name" name="user_name" placeholder="请输入您的姓名" required>
    </div>
    <div>
      <label for="email">邮箱:</label>
      <input type="email" id="email" name="user_email" required>
    </div>
    <div>
      <label for="message">留言:</label>
      <textarea id="message" name="user_message" rows="4" cols="50"></textarea>
    </div>
    <div>
      <input type="checkbox" id="subscribe" name="subscribe" value="yes">
      <label for="subscribe">订阅我们的资讯</label>
    </div>
    <div>
      <button type="submit">提交反馈</button>
    </div>
  </form>
  ```

**基本HTML标签总结**

| **标签**      | **用途/描述**                      | **关键属性 (示例)**                                      |
| ------------- | ---------------------------------- | -------------------------------------------------------- |
| `<h1>`-`<h6>` | 定义不同级别的标题，构建文档结构。 | -                                                        |
| `<p>`         | 定义文本段落。                     | -                                                        |
| `<a>`         | 创建超链接。                       | `href`, `target`, `title`, `rel`                         |
| `<img>`       | 嵌入图像。                         | `src`, `alt`, `width`, `height`                          |
| `<ul>`        | 定义无序列表（项目符号）。         | -                                                        |
| `<ol>`        | 定义有序列表（数字/字母）。        | `type`, `start`, `reversed`                              |
| `<li>`        | 定义列表中的一个项目。             | `value` (在 `<ol>` 中)                                   |
| `<table>`     | 定义表格。                         | `border` (不推荐, 用CSS代替)                             |
| `<tr>`        | 定义表格中的行。                   | -                                                        |
| `<th>`        | 定义表头单元格。                   | `scope`, `colspan`, `rowspan`                            |
| `<td>`        | 定义表格数据单元格。               | `colspan`, `rowspan`                                     |
| `<form>`      | 定义HTML表单，用于收集用户输入。   | `action`, `method`                                       |
| `<input>`     | 定义表单输入控件。                 | `type`, `name`, `id`, `value`, `placeholder`, `required` |
| `<button>`    | 定义可点击的按钮。                 | `type`, `name`, `value`                                  |
| `<label>`     | 为表单控件定义标签。               | `for`                                                    |
