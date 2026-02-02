# 登录与鉴权

##  1. 原始登录流程 (Strawman Example) 

### 流程

1. 用户在客户端（注册/登录界面）输入用户名和密码。
2. 客户端将用户名和密码发送给服务端。
3. 服务端查询数据库：
   - 注册：检查用户名是否存在，不存在则存入数据库。
   - 登录：验证用户名和密码是否匹配。

### **问题**

- 安全问题1 (传输安全)：

  - **问题：** 明文密码传输易被抓包泄露。
  - **朴素解决：** 非对称加密密码。但这无法防止中间人攻击（攻击者直接重放请求）。
  - **根本解决：** 使用HTTPS协议。HTTPS能确认发送者身份，防止中间人攻击，保障传输过程安全。

- 安全问题2 (凭证传递与体验)：

  - **问题：** 每次权限操作都需传递密码，用户体验差；客户端缓存密码不安全；频繁传输密码增加泄露风险。
  - **解决思路：** 将权限验证分为登录（Login）和认证（Authentication）。登录后，后续请求通过其他机制（如Cookie）证明用户已登录。

- 安全问题3 (服务端存储安全)：

  - **问题：** 数据库直接存储用户密码，一旦泄露，密码即暴露。

  - 解决： 存储加盐哈希（Salted Hash）后的密码。

    - 验证时，将用户输入密码用相同盐和哈希算法处理，再与数据库中存储的哈希值对比。

    - 好处：即使数据库泄露，也难以直接获取用户原始密码；服务端也不知道用户真实密码。

    - Go示例 (bcrypt)：

      ```go
      import "golang.org/x/crypto/bcrypt"
      
      // 哈希加密
      func HashPassword(password string) (string, error) {
          hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
          return string(hashedPassword), err
      }
      
      // 验证密码
      func CheckPassword(hashedPassword, password string) bool {
          err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
          return err == nil
      }
      ```

    - **工业级：** 通常使用基于SHA256的加盐PBKDF2，每个用户salt不同，迭代次数高（如1000+）。

## **2. Cookie**

### **原理**

- 用户首次登录成功后，服务器创建一些信息（Cookie）并通过HTTP响应头（`Set-Cookie`）发送给浏览器。
- 浏览器按域名保存这些Cookie。
- 后续用户访问该域名下的资源时，浏览器会自动在HTTP请求头（`Cookie`）中携带这些Cookie。
- 服务器通过读取Cookie来识别用户状态（如是否已登录）。
- 大小有限（KB级别），键值对形式。

### **属性**

- 生命周期 (Lifecycle)：
  - `Permanent cookie`：通过 `Expires` (绝对时间) 或 `MaxAge` (相对时长，秒为单位) 设置。`MaxAge` 优先。若 `MaxAge` 为非正数，浏览器立即删除该Cookie。
  - `Session cookie`：若不设置 `Expires` 或 `MaxAge`，则为会话Cookie，浏览器关闭后通常会删除（具体行为取决于浏览器对 "session" 的定义）。
- 访问限制 (Access Restrictions)：
  - `HttpOnly`：若设置，则Cookie不能通过JavaScript的 `document.cookie` API访问，只能在HTTP请求中传输。有助于缓解XSS攻击窃取Cookie。 (注意：仍有其他方式可能获取，非绝对安全)
  - `Secure`：若设置，则Cookie只在HTTPS请求中传输，防止在HTTP连接中被窃听。
- 作用范围 (Scope)：
  - `Domain`：指定Cookie所属的域名。默认情况下，会匹配所有子域名 (如 `domain=example.com` 匹配 `sub.example.com`)。若不设置，则默认为当前请求的域名，且不匹配子域名（更严格）。
  - `Path`：指定Cookie在哪个路径下生效。默认为 `/` (根路径)，匹配所有子路径 (如 `/` 匹配 `/docs`)。
  - Cookie的唯一性由 `name + domain + path` 确定。

**Go (Gin) 中操作Cookie示例：**

```go
r.GET("/cookie", func(c *gin.Context) {
    cookie, err := c.Cookie("key_cookie") // 获取Cookie
    if err != nil {
        cookie = "NotSet"
        // 设置Cookie: 名称, 值, MaxAge(秒), 路径, 域名, Secure, HttpOnly
        c.SetCookie("key_cookie", "value_cookie", 60, "/", "localhost", false, true)
    }
    fmt.Printf("cookie的值是： %s\n", cookie)
})
```

## 3. Session

1. **为什么需要Session？**

   - Cookie大小有限，不适合存储大量信息（如购物车、复杂表单数据）。这些信息应由服务端存储。
   - 仅靠浏览器存储信息，服务端无法完全确认请求者身份的真实性和状态。Session允许服务端维护用户状态。

2. **原理：**

   - 用户访问网站时，服务器创建一个Session对象（存储在服务器内存、数据库或缓存中）。
   - 服务器为该Session生成一个唯一的Session ID。
   - Session ID通过Cookie（通常名为 `session_id` 或类似）发送给浏览器。
   - 浏览器后续请求会自动带上这个包含Session ID的Cookie。
   - 服务器通过接收到的Session ID找到对应的Session数据，从而识别用户并恢复其状态。
   - ==**核心：Session是基于Cookie（用于传递Session ID）实现的。**==

3. **Go (Gin + gorilla/sessions) 示例：**

   ```go
   import (
       "net/http"
       "github.com/gin-gonic/gin"
       "github.com/gorilla/sessions"
   )
   
   var store = sessions.NewCookieStore([]byte("Your-Secret-Key")) // 密钥用于签名和加密session cookie
   
   func main() {
       r := gin.Default()
       store.Options.MaxAge = 30 // Session过期时间 (秒)
   
       r.GET("/login", func(c *gin.Context) {
           session, _ := store.Get(c.Request, "Your-Session-Name") // 获取或创建Session
           session.Values["authenticated"] = true
           session.Values["username"] = "Username from your frontend"
           session.Save(c.Request, c.Writer) // 保存Session，会设置相应的Cookie
           c.String(http.StatusOK, "Login success")
       })
   
       r.GET("/home", func(c *gin.Context) {
           session, _ := store.Get(c.Request, "Your-Session-Name")
           if auth, ok := session.Values["authenticated"].(bool); ok && auth {
               username := session.Values["username"].(string)
               c.String(http.StatusOK, "Welcome "+username)
               // 可选：活动用户刷新过期时间
               session.Options.MaxAge = 30
               session.Save(c.Request, c.Writer)
           } else {
               c.String(http.StatusUnauthorized, "Please login first")
           }
       })
   
       r.GET("/logout", func(c *gin.Context) {
           session, _ := store.Get(c.Request, "Your-Session-Name")
           session.Options.MaxAge = -1 // 设置MaxAge为负数，立即销毁Session (删除Cookie)
           session.Save(c.Request, c.Writer)
           c.String(http.StatusOK, "Logout success")
       })
       r.Run(":8000")
   }
   ```

## 4. Cookie的问题

1. **CSRF原理：**

   * 攻击者诱导已登录某网站（如A网站）的用户访问一个恶意页面或点击恶意链接。

   - 该恶意页面包含向A网站发起特定操作（如转账、修改密码）的请求。
   - 由于浏览器会自动携带A网站的Cookie（包含用户的登录凭证，如Session ID）到A网站，A网站服务器会认为这是用户的合法操作并执行。

2. **防御CSRF：**

   - **验证码：** 对高危操作要求用户输入验证码，但影响用户体验。
   - 限制Cookie的携带 (`SameSite`属性)：
     - `Site` (站点)：通常由顶级域名+二级域名（eTLD+1）定义，如 `example.com`。
     - `Origin` (源)：由 `schema` (协议) + `host` (主机名) + `port` (端口号) 组成。
     - `SameSite`属性值：
       - `Strict`：最严格，禁止所有跨站请求携带Cookie。即使从 `a.com` 点击链接到 `b.com`，也不会携带 `b.com` 的Cookie。
       - `Lax`：允许部分“安全”的顶层导航跨站请求携带Cookie（如通过 `<a>` 标签GET请求跳转）。是许多浏览器逐步采用的默认值。
       - `None`：允许所有跨站请求携带Cookie。**必须同时设置 `Secure` 属性** (即Cookie只能通过HTTPS传输)。
   - **校验请求来源 (Referer Check)：** 检查HTTP请求头中的 `Referer` 字段，判断请求是否来自合法的源。但 `Referer` 可被伪造或为空。
   - Token (Anti-CSRF Token)：
     - 用户访问表单页面时，服务器生成一个随机Token，嵌入表单中（如隐藏字段）。
     - 用户提交表单时，该Token随表单一并发送。
     - 服务器验证该Token是否与之前生成并存储在用户Session中的Token一致。攻击者无法获取此Token。
   - CORS (Cross-Origin Resource Sharing)：
     - 本身不是直接防御CSRF的机制，而是用于控制**跨域资源访问**的策略。
     - CORS通过HTTP头部协商，允许一个源（Origin）的Web应用访问另一个源的资源。
     - 流程简介 (Non-simple request)：
       1. **Preflight Request (预检请求):** 浏览器自动发送 `OPTIONS` 请求到目标服务器，携带 `Origin`, `Access-Control-Request-Method`, `Access-Control-Request-Headers`。
       2. **Server Response:** 服务器响应，包含 `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`, `Access-Control-Allow-Credentials`, `Access-Control-Max-Age`。
       3. **Actual Request:** 若预检通过，浏览器发送实际请求（如POST），携带 `Origin`。
       4. **Server Response:** 服务器正常响应，也可能包含 `Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`, `Access-Control-Expose-Headers`。
     - `Access-Control-Allow-Origin: *` 与 `Access-Control-Allow-Credentials: true` 不可同时使用（若为`*`，`Credentials` 会被视为`false`）。
     - 客户端发起带凭证的跨域请求 (如 `Workspace`) 需设置 `credentials: 'include'`。

## **5. Token**

### 1. 为什么需要Token？

- **分布式系统：** Session存储在单台服务器时，多服务器负载均衡场景下，用户请求可能被分配到不同服务器，导致Session信息不一致。将Session存入共享数据库或缓存会增加其压力。Token是无状态的（或服务器端轻状态）。
- **无状态认证：** 服务器不需要存储用户状态信息（如Session），每次请求都携带Token，服务器验证Token即可。
- **灵活性：** Token可以承载更多信息，没有Cookie的大小和跨域限制（但仍需考虑安全传输和存储）。

### 2. JWT (JSON Web Token) 结构：

由三部分组成，用点 `. `分隔：`Header.Payload.Signature`

#### Header (头部)

 Base64Url编码的JSON对象，包含：

- `typ`: "JWT" (类型)
- `alg`: 签名算法 (如 "HS256", "RS256")

#### Payload (载荷)

 Base64Url编码的JSON对象，包含Claims (声明)：

- **Registered Claims (注册声明，可选，建议使用)：** `iss` (签发者), `sub` (主题), `aud` (受众), `exp` (过期时间戳), `nbf` (生效时间戳), `iat` (签发时间戳), `jti` (JWT ID)。
- **Public Claims (公共声明)：** 自定义，但应避免与注册声明冲突。
- **Private Claims (私有声明)：** 通信双方自定义，用于传递非标准信息 (如 `user_id`, `username`)。

#### Signature (签名)

- 使用Header中指定的算法，对 `base64UrlEncode(Header) + "." + base64UrlEncode(Payload)` 进行签名，再加上一个服务器端持有的`secret`（对于HS256）或私钥（对于RS256）。
- **作用：** 验证Token的完整性和来源，确保Header和Payload未被篡改。
- **注意：** JWT的Payload是Base64Url编码的，不是加密的。敏感信息不应直接放在Payload中，除非整个JWT被加密传输（JWE）。

#### **JWT 工作流程：**

1. 用户使用用户名密码登录。
2. 服务器验证通过，生成JWT（包含用户信息、过期时间等）。
3. 服务器将JWT返回给客户端。
4. 客户端存储JWT（如 `localStorage`, `sessionStorage`，或安全的HttpOnly Cookie）。
5. 客户端每次请求受保护资源时，在HTTP请求头 `Authorization` 中携带JWT：`Authorization: Bearer <token>`。
6. 服务器接收请求，提取JWT。
7. 服务器使用自己的`secret`验证JWT的签名。若验证通过且未过期，则处理请求。

**Go (golang-jwt/jwt) 生成和解析JWT示例：**

```go
package myjwt // Renamed package to avoid conflict with std lib

import (
    "errors"
    "time"
    "github.com/golang-jwt/jwt/v5"
)

const TokenExpireDuration = time.Hour * 2 // 例如2小时过期
var CustomSecret = []byte("your-very-strong-secret-key") // 必须保密

type CustomClaims struct {
    UserID   int64  `json:"user_id"`
    Username string `json:"username"`
    jwt.RegisteredClaims // 内嵌标准声明
}

func GenToken(UserID int64, Username string) (string, error) {
    claims := CustomClaims{
        UserID,
        Username,
        jwt.RegisteredClaims{
            ExpiresAt: jwt.NewNumericDate(time.Now().Add(TokenExpireDuration)),
            Issuer:    "my-app-issuer", // 签发者
        },
    }
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString(CustomSecret)
}

func ParseToken(tokenString string) (*CustomClaims, error) {
    claims := new(CustomClaims)
    token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
        // 校验签名算法是否符合预期
        if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
            return nil, errors.New("unexpected signing method")
        }
        return CustomSecret, nil
    })
    if err != nil {
        return nil, err
    }
    if token.Valid { // token.Valid 会检查 claims 中的 RegisteredClaims (如 ExpiresAt)
        return claims, nil
    }
    return nil, errors.New("invalid token")
}
```

### 3. **客户端存储和传递Token：**

#### 存储

- `localStorage`: 持久存储，浏览器关闭后仍在。XSS可访问。
- `sessionStorage`: 会话级存储，标签页关闭后清除。XSS可访问。
- `HttpOnly Cookie`: 更安全，防XSS，但有CSRF风险（需配合`SameSite`）。

#### 传递

- HTTP Header: `Authorization: Bearer <token>` (推荐)。
- URL参数: `?token=<token>` (不推荐，URL易暴露)。
- Request Body: (POST请求中)。

- JS示例 (localStorage + Fetch API)：

  ```javascript
  // 存储
  localStorage.setItem('jwtToken', 'your_received_token');
  
  // 读取和使用
  const token = localStorage.getItem('jwtToken');
  fetch("http://localhost:8080/api/data", {
      method: "GET",
      headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
      }
  })
  .then(response => response.json())
  .then(data => console.log(data));
  ```

## 6. JWT的问题与解决方案

### 1. **用户登出 (Token失效)**

- **问题：** JWT一旦签发，在过期前都是有效的。服务器无法主动使其失效。
- **客户端方案：** 删除本地存储的JWT (`localStorage.removeItem("TokenName")`)。但如果JWT已被泄露，攻击者仍可使用。
- 服务端方案：
  - **黑名单机制：** 维护一个已失效Token的列表（如存入Redis）。每次校验Token时先查黑名单。这给无状态服务器增加了一点“状态”。
  - **修改用户密钥：** 每个用户有专属的Token签名密钥。用户登出时，修改其密钥。旧Token因密钥不匹配而失效。
    * 缺点：分布式系统密钥同步问题；多设备登录时，一个设备登出可能导致其他设备也登出。

### 2. **Token续签 (Renewal)**

- **问题：** Session续签简单（更新服务端Session过期时间）。JWT的过期时间是Payload的一部分，修改会使签名失效。
- 解决方案：Access Token + Refresh Token
  - `Access Token`: 短生命周期（如15分钟-2小时），用于访问受保护资源。Payload中可包含权限信息。
  - `Refresh Token`: 长生命周期（如几天或几周），用于获取新的Access Token。Refresh Token本身通常只包含用户标识，不含权限，且存储更安全。
  - 流程：
    1. 用户登录，服务器返回Access Token和Refresh Token。
    2. 客户端使用Access Token访问API。
    3. 若Access Token过期，服务器返回特定错误（如401）。
    4. 客户端检测到此错误，使用Refresh Token向服务器特定端点请求新的Access Token。
    5. 服务器验证Refresh Token的有效性（是否过期、是否在黑名单/白名单中）。
    6. 若Refresh Token有效，服务器签发新的Access Token（有时也会签发新的Refresh Token，实现Refresh Token滚动刷新）。
    7. 若Refresh Token也失效，则要求用户重新登录。

## 7. OAuth

### 1. 概念

- 一个授权框架，允许第三方应用（Client，如Deepseek）在用户授权的前提下，访问用户在某个服务提供商（Resource Server/Authorization Server，如微信）上的受保护资源，而无需将用户的凭证（用户名密码）直接给第三方应用。
- 角色：
  - `Resource Owner`: 用户。
  - `Client`: 第三方应用 (如Deepseek)。
  - `Authorization Server`: 鉴权方，负责验证用户身份并颁发访问令牌 (Access Token)。
  - `Resource Server`: 资源方，存储用户受保护资源，信任Authorization Server颁发的Access Token。

### 2. **常用授权流程 (Authorization Code Grant Type - 授权码模式)：**

1. **用户发起：** 用户在Client应用中点击“使用XX登录”。

2. 重定向到授权服务器：

    Client将用户重定向到Authorization Server的授权页面（`AuthURL`），并携带参数：

   - `client_id`: Client的标识符。
   - `redirect_uri`: 授权成功后，Authorization Server将用户重定向回Client的地址。
   - `response_type=code`: 表明要求返回授权码。
- `scope`: Client申请的权限范围。
   - `state`: Client生成的一个随机字符串，用于防止CSRF攻击，并关联用户在Client的状态。

3. **用户授权：** 用户在Authorization Server上登录并同意授权Client请求的权限。

4. **返回授权码：** Authorization Server将用户重定向回Client提供的 `redirect_uri`，并附带一个短期的 `code` (授权码) 和之前Client发送的 `state` 参数。

5. **交换授权码获取Token：** Client收到 `code` 后，在后端用 `code`、`client_id`、`client_secret` (Client的密钥)、`redirect_uri` 向Authorization Server的 `TokenURL` 发起请求，交换Access Token (以及可选的Refresh Token)。

6. **访问资源：** Client使用获取到的Access Token向Resource Server请求用户资源。

**Go (golang.org/x/oauth2) 示例片段：**

```go
import (
    "context"
    "fmt"
    "net/http"
    "golang.org/x/oauth2"
)

var oauthConfig = oauth2.Config{
    ClientID:     "YOUR_CLIENT_ID",
    ClientSecret: "YOUR_CLIENT_SECRET",
    RedirectURL:  "http://localhost:8080/callback", // 必须与在服务商处注册的一致
    Scopes:       []string{"scope1", "scope2"},     // 申请的权限
    Endpoint: oauth2.Endpoint{
        AuthURL:  "PROVIDER_AUTH_URL",  // 服务商的授权URL
        TokenURL: "PROVIDER_TOKEN_URL", // 服务商的Token URL
    },
}
var oauthStateString = "random-string-for-csrf-protection" // 应该为每个请求动态生成并验证

func handleLogin(w http.ResponseWriter, r *http.Request) {
    // 实际应用中 oauthStateString 应为每个授权请求生成，并可能存储在session中用于后续验证
    url := oauthConfig.AuthCodeURL(oauthStateString)
    http.Redirect(w, r, url, http.StatusTemporaryRedirect)
}

func handleCallback(w http.ResponseWriter, r *http.Request) {
    // 1. 验证 state 参数防止CSRF
    if r.FormValue("state") != oauthStateString {
        fmt.Println("invalid oauth state")
        http.Redirect(w, r, "/", http.StatusTemporaryRedirect)
        return
    }

    // 2. 获取授权码
    code := r.FormValue("code")

    // 3. 用授权码交换Token
    token, err := oauthConfig.Exchange(context.Background(), code)
    if err != nil {
        fmt.Printf("oauthConfig.Exchange() failed with '%s'\n", err)
        http.Redirect(w, r, "/", http.StatusTemporaryRedirect)
        return
    }

    // 4. token.AccessToken 即为访问令牌
    // 可以用此token去调用服务商的API获取用户信息等
    fmt.Fprintf(w, "OAuth2认证成功! Access Token: %s\n", token.AccessToken)
    if token.RefreshToken != "" {
        fmt.Fprintf(w, "Refresh Token: %s\n", token.RefreshToken)
    }
    // 实际应用中，通常会将 token 存储起来 (如session或数据库) 关联到用户
}
```

- `state` 参数：在 `handleLogin` 时生成并随 `AuthCodeURL` 发出，在 `handleCallback` 时从请求中获取并与之前存储的值（如Session中）比较，一致才继续，否则可能是CSRF。

## 八、总结

| **特性**     | **Cookie**                                 | **Session**                                        | **Token (JWT)**                                              |
| ------------ | ------------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------ |
| **存储位置** | 客户端（浏览器）                           | Session ID在客户端(Cookie)，数据在服务端           | 客户端 (localStorage, sessionStorage, Cookie)                |
| **状态**     | 无状态（但用于维护服务器的有状态会话）     | 有状态（服务器需存储Session数据）                  | 无状态（服务器不需存Token本身，但可能存黑名单/密钥）         |
| **大小**     | 小 (约4KB)                                 | Session ID小，服务端数据可大                       | 可以比Cookie大，但仍需考虑传输效率                           |
| **安全性**   | XSS可窃取 (除非HttpOnly), CSRF风险         | Session ID的Cookie有同样风险。数据在服务端相对安全 | 存储在localStorage/sessionStorage易被XSS窃取。签名防篡改，内容可见（非加密） |
| **跨域**     | 受同源策略限制，可通过`Domain`属性部分放宽 | Session ID通过Cookie传递，同样受限                 | 本身无跨域限制，常用于API认证，但客户端获取和发送仍需CORS配合 |
| **分布式**   | -                                          | 需Session共享机制（如Redis, DB），增加复杂度       | 易于分布式部署，服务器无需共享状态                           |
| **主要用途** | 存储少量数据，跟踪用户，传递Session ID     | 维护用户会话状态，存储购物车等复杂信息             | API认证，无状态认证，单点登录，移动应用认证                  |
| **依赖**     | 无                                         | 通常依赖Cookie传递Session ID                       | 不直接依赖Cookie (但可存入Cookie)                            |

1. - 考虑Refresh Token的吊销/黑名单机制。

------

这份笔记应该能帮助您更好地理解这几个概念及其应用。祝您项目顺利！