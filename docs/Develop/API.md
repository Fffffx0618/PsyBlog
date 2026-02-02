# API

## 一、API 的基本概念

### 1. 什么是 API？
API（Application Programming Interface，应用程序编程接口）是**前端和后端进行通信和交换数据的规范**。  
它定义了：
- 请求路径（URL）
- 请求方法（GET/POST 等）
- 请求参数
- 响应格式

### 2. HTTP 工作原理回顾
HTTP 是客户端（client）向服务器（server）发送请求（request），服务器返回响应（response）的过程。

**示例：**
当你访问 CC98 论坛时，它会通过一个 GET 请求获取你的个人信息：
```
GET https://api.cc98.com/me
```

开发者工具中可以查看这个请求的 response 数据。

### 3. API 在项目中的作用

在我们的评论区功能中，前端需要通过一个 **POST 请求** 获取评论列表。而后端返回的数据结构如下：

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "total": 121,
        "comments": [
            {
                "id": 1,
                "name": "张三",
                "content": "这是一条评论"
            }
        ]
    }
}
```

- `code`: 表示请求是否成功（0 成功，非 0 失败）
- `msg`: 错误信息或提示
- `data`: 实际返回的数据内容

这种结构便于前后端统一处理错误逻辑，避免因某个字段缺失导致程序崩溃。

---

## 二、API 设计规范

### 1. URL 结构设计

#### 示例：
```
https://api.example.com/PROG/user/get
```

- `https://`：协议，保证安全性
- `api.example.com`：域名
- `/PROG/`：项目前缀，用于划分不同业务线
- `/user/get`：具体路由路径，表示用户模块下的“获取”操作

> ✅ 建议：将基础 URL 提取为常量，避免硬编码拼接字符串。

---

### 2. HTTP 方法选择

| 方法   | 描述               |
| ------ | ------------------ |
| GET    | 获取资源（幂等）   |
| POST   | 创建资源（不幂等） |
| PUT    | 更新资源（幂等）   |
| DELETE | 删除资源（幂等）   |

> 📌 本项目主要使用 GET 和 POST 方法。

---

### 3. 参数传递方式

#### (1) GET 请求传参
- **查询字符串（Query String）**：最常见
  ```
  /api/user?id=123&name=xyz
  ```

- **路径参数（URL Parameter）**
  ```
  /user/getById/abc123
  // 后端路由写法: /user/getById/:id
  ```

- **参数数组 / 对象**
  ```url
  /api/user?filter[]=admin&filter[]=active
  /api/user?filter={"role":"admin", "status":"active"}
  ```

#### (2) POST 请求传参
- **JSON 格式（推荐）**
  ```ts
  async function sendJsonData(url: string, data: any) {
      const response = await fetch(url, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      });
      return await response.json();
  }
  ```

- **表单数据（Form Data）**
  - Content-Type: `application/x-www-form-urlencoded`

- **文件上传**
  - Content-Type: `multipart/form-data`

---

## 三、统一响应格式

我们约定所有 API 返回都采用如下结构：

```json
{
    "code": 0,
    "msg": "success",
    "data": {}
}
```

### 后端封装建议：
```ts
// 成功
resp.Ok(data) => { code: 0, msg: "", data }

// 失败
resp.Err(code, reason) => { code, reason, data: null }
```

### 前端处理逻辑：
```ts
function handleResponse(res) {
    if (res.code !== 0) {
        alert(`错误：${res.msg}`);
        return null;
    }
    return res.data;
}
```

---

## 四、状态码分类

| 类型 | 范围    | 含义                                       |
| ---- | ------- | ------------------------------------------ |
| 1xx  | 100-199 | 信息性状态码（接收请求正在处理）           |
| 2xx  | 200-299 | 成功（如 200 OK）                          |
| 3xx  | 300-399 | 重定向                                     |
| 4xx  | 400-499 | 客户端错误（如 404 Not Found）             |
| 5xx  | 500-599 | 服务端错误（如 500 Internal Server Error） |

> ⚠️ 注意：即使业务逻辑出错，也建议返回 200 状态码 + 自定义 `code` 字段来区分错误类型。

