# Git入门

## 0. 指令大全

当然，下面是根据Git命令的用途进行分类后的输出：

### 初始化和克隆
```bash
git init# 初始化一个新的Git仓库
git clone <repo_url># 从远程仓库克隆项目到本地
```

### 基本操作（添加、提交）                                   
```bash
git add <file># 将文件添加到暂存区，准备提交
git commit -m "commit message"# 提交暂存区的更改到本地仓库，并附上说明信息
```

### 查看状态和历史
```bash
git status# 显示工作目录和暂存区的状态，查看哪些文件被修改了
git log# 显示提交历史，便于查看项目的变更记录
git diff# 显示未暂存的更改，对比文件的不同之处
```

### 分支管理
```
git branch# 列出所有本地分支，当前所在分支前会有一个星号(*)标记
git branch <branch_name># 创建一个新分支
git checkout <branch_name># 切换到指定分支
git checkout -b <branch_name># 创建并切换到新分支
git merge <branch_name># 将指定分支的更改合并到当前分支
```

### 远程操作
```bash
git push origin <branch_name># 将本地分支的更新推送到远程仓库
git pull# 从远程仓库获取最新更改并与本地代码合并
git fetch# 获取远程仓库的更新但不自动合并
git remote add origin <repo_url># 关联远程仓库
```

### 标签管理
```bash
git tag <tag_name># 给当前分支的最新commit打标签
```

### 撤销与恢复
```bash
git reset <file># 从暂存区移除文件，但保留在工作目录中
git rm <file># 从工作目录和暂存区删除文件
git stash# 暂存当前工作目录的更改，以便你可以切换分支或进行其他操作
```

### 其他
```bash
git show# 显示某次提交的详细信息或者某个文件在特定提交中的内容
git reflog# 记录所有的操作，包括那些没有被任何分支或标签引用的提交
```

## 1. 建立本地版本库

- **定义**：***版本库Repository***是一个被Git管理的目录，可以跟踪文件的修改、删除等操作，以便追踪历史或恢复到以前的状态。

### 1.1 创建Git版本库

1. **创建空目录**：
   
   ```bash
   $ mkdir <repo_name>
   $ cd <repo_name>
   ```
2. **初始化仓库**：
   ```bash
   $ git init
   ```
   - 这会在当前目录下创建一个隐藏的`.git`目录，用于Git管理版本库（用`ls -ah`可以看见）。

### 1.2 添加文件到Git仓库

1. **将文件放入版本库目录**。
2. **添加文件到暂存区**：
   
   ```bash
   $ git add <file>
   ```
3. **提交文件到仓库**：
   ```bash
   $ git commit -m "<message>"
   ```

- **文本 vs 二进制文件**：Git能详细跟踪文本文件的变化，但对二进制文件只能记录<u>整体变化</u>。

- **编码建议**：推荐使用UTF-8编码保存文本文件，避免不同平台间的编码冲突。

## 2. 工作区与暂存区

- **工作区（Working Directory）**：指的是你在电脑上看到的项目目录，例如 `learngit` 文件夹。在这个目录下，你可以进行文件的创建、编辑和删除等操作。

- **版本库（Repository）**：在每个工作区中，都有一个隐藏的 `.git` 目录，这就是Git的版本库。它存储了所有Git管理的数据，包括但不限于：
  - **暂存区（Stage 或 Index）**：用于存放准备提交到仓库的修改。
  - **分支（Branch）**：如默认的 `master` 分支。
  - **HEAD指针**：指向当前所在的分支或特定的commit。

### Git 提交流程

1. **使用 `git add` 命令添加修改至暂存区**：
   - 每当你对工作区中的文件进行了修改后，可以使用 `git add <file>` 将这些修改添加到暂存区。这一步骤允许你选择性地将哪些改动包含在下一个提交中。

2. **通过 `git commit` 提交更改到当前分支**：
   - 执行 `git commit -m "提交说明"` 可以将暂存区的所有内容一次性提交到当前分支。这意味着一旦提交完成，暂存区会被清空，而你的修改则被安全地保存到了版本历史中。

### 状态检查

- 提交完成后，再次运行 `git status`，如果没有任何新的修改，Git会告诉你“没有需要提交的内容，工作区干净”。

## 3. 版本管理

### 3.1 查看提交记录

- **查看所有提交记录**：
  
  ```bash
  $ git log
  ```
  - 显示从最近到最远的提交日志，包括commit ID、作者、日期和提交说明。
  
- **简化输出格式**：
  
  ```bash
  $ git log --pretty=oneline
  ```
  - 每条记录只显示commit ID和提交说明，便于快速浏览。

### 3.2 版本回退

- **回退到上一个版本**：
  
  ```bash
  $ git reset --hard HEAD^
  ```
  - `HEAD` 表示当前版本，`HEAD^` 表示上一个版本，`HEAD^^`表示上上一个版本。更多可用 `HEAD~n`（n代表回退多少个版本）。
  
- **回退到特定版本**：
  ```bash
  $ git reset --hard <commit_id>
  ```
  - `<commit_id>` 是目标版本的commit ID，可以是<u>完整的ID或前几位字符</u>。

- **参数选项**：
  
   | 模式      | 暂存区 | 工作区 | 操作                         |
   | --------- | ------ | ------ | ---------------------------- |
   | `--hard`  | 清空   | 清空   | 回到指定版本**已提交**状态   |
   | `--soft`  | 保留   | 保留   | 回到指定版本**未commit**状态 |
   | `--mixed` | 清空   | 保留   | 回到指定版本**未add**状态    |


- **找回已删除的提交记录**：
  
  ```bash
  $ git reflog
  ```
  - 显示所有操作命令的历史记录，包括已被回退掉的提交，帮助你找到想恢复的commit ID。

### 3.4 查看差异

* **查看工作区与最新版本库之间的差异：**

```bash
git diff HEAD -- <file>
```

可以查看工作区和版本库里最新版本的区别

### 3.5 撤销修改

#### 1. **撤销工作区的修改**

```bash
git checkout -- <file>
```

作用：**把文件在工作区的修改全部撤销；**

- 文件未add则回到版本库的状态，文件已add则回到刚add时的状态
- 文件回到**最近一次 git commit 或 git add** 时的状态

#### **2. 撤销已添加到暂存区的修改**

1. 将暂存区的修改“撤回”到工作区：
   ```bash
   git reset HEAD <file>
   ```

2. 再使用 `git checkout -- <file>` 撤销工作区的修改。

**说明：**
- `git reset HEAD <file>` 可以将文件从暂存区移回工作区，不删除内容；
- 之后可选择是否彻底丢弃修改。

#### 3. 撤销已经提交到版本库的修改

```bash
git reset --hard HEAD^
```

| 场景             | 操作                   | 命令                                               |
| ---------------- | ---------------------- | -------------------------------------------------- |
| 修改仅在工作区   | 直接丢弃修改           | `git checkout -- <file>`                           |
| 修改已加入暂存区 | 先取消暂存，再丢弃修改 | `git reset HEAD <file>` + `git checkout -- <file>` |
| 已提交到本地仓库 | 回退版本               | `git reset --hard HEAD^`                           |

### 3.6 删除文件 

* Git 把**删除文件**也视为一种“修改”，和添加、修改内容一样，都会被版本控制系统跟踪。

1. **手动删除文件（或使用 `rm` 命令）**
   
   ```bash
   $ rm test.txt
   ```
   
3. **从Git中移除该文件（即提交删除操作）：**
   
   ```bash
   $ git rm test.txt
   ```
   
4. **提交删除：**
   
   ```bash
   $ git commit -m "remove test.txt"
   ```

*  只有执行了 `git rm` 和 `git commit`，文件才会真正从版本库中删除。

**误删文件**

* 如果只是**误删了文件**，但之前已经提交到Git仓库，可以轻松恢复：

```bash
$ git checkout -- test.txt
```

这个命令的作用是：
- 用版本库中的最新版本替换工作区的内容；
- 无论是修改还是删除，都可以还原。

| 操作                       | 命令                                         |
| -------------------------- | -------------------------------------------- |
| 删除文件并提交             | `rm <file>` → `git rm <file>` → `git commit` |
| 恢复误删文件               | `git checkout -- <file>`                     |
| 仅删除工作区文件（不提交） | 直接 `rm <file>`                             |
| 仅删除暂存区文件（不解绑） | `git rm --cached <file>`                     |

## 4. 远程仓库

### 4.1添加远程仓库 

#### 关联远程仓库

1. **在GitHub上创建新仓库**：
   
   - 登录 GitHub；
   - 点击右上角 `+` → `New repository`；
   - 输入仓库名（如：`learngit`）；
   - 其他保持默认，点击创建。
   
2. **将本地仓库与远程仓库关联**：
   ```bash
   git remote add origin git@github.com:<你的用户名>/learngit.git
   ```
   - `origin` 是远程仓库的默认名称（可自定义）；
   - 请替换 `<你的用户名>` 为你的 GitHub 账号。

#### 推送内容到远程仓库

1. **首次推送（需绑定分支）**：
   
   ```bash
   git push -u origin master
   ```
   - `-u` 参数会将本地 `master` 分支与远程 `master` 分支关联；

2. **后续提交只需简单命令即可**：
   ```bash
   git push origin master
   ```

### 4.2  删除远程仓库关联

1. **查看当前远程库信息**：
   
   ```bash
   git remote -v
   ```
   
2. **删除远程库关联（解除绑定）**：
   ```bash
   git remote rm origin
   ```
   - 此操作仅解除本地和远程的绑定关系；
   - 不会删除远程仓库本身

| 操作               | 命令                               |
| ------------------ | ---------------------------------- |
| 添加远程仓库       | `git remote add origin <仓库地址>` |
| 首次推送并绑定分支 | `git push -u origin master`        |
| 后续推送           | `git push origin master`           |
| 查看远程仓库信息   | `git remote -v`                    |
| 删除远程仓库绑定   | `git remote rm origin`             |

### 4.3 从远程库克隆 Git 仓库

#### 创建远程仓库

1. 登录 GitHub。
2. 点击页面右上角的 `+` 号，选择 `New repository`。
3. 在 Repository name 中输入仓库名（如：`gitskills`）。
4. 勾选 `Initialize this repository with a README`，这样 GitHub 会自动为你创建一个 `README.md` 文件。
5. 完成创建后，你可以在 GitHub 页面看到新创建的 `README.md` 文件。

#### 克隆远程仓库到本地

1. **获取仓库地址**：
   
   - 在仓库主页找到并复制仓库的 SSH 或 HTTPS 地址。对于使用 SSH 密钥认证的用户，推荐使用 SSH 地址，例如：`git@github.com:michaelliao/gitskills.git`。
   
2. **执行克隆命令**：
   ```bash
   git clone git@github.com:michaelliao/gitskills.git
   ```
   - 这个命令会在当前目录下创建一个与远程仓库同名的文件夹，并将远程仓库的内容下载到这个文件夹中。

3. **进入项目目录**：
   ```bash
   cd gitskills
   ls
   ```
   - 使用 `ls` 查看目录内容，你应该能看到 `README.md` 文件。

## 5. 分支管理

### 5.1 创建与合并分支

#### 1. 创建与切换分支

1. 使用 `git checkout` 命令

- **创建并切换到新分支**：
  
  ```bash
  git checkout -b dev
  ```
  这相当于以下两条命令的组合：
  ```bash
  git branch dev
  git checkout dev
  ```

2. 使用更新的 `git switch` 命令（推荐）

- **创建并切换到新分支**：
  ```bash
  git switch -c dev
  ```
- **直接切换到已有分支**：
  ```bash
  git switch master
  ```

查看当前所有分支

```bash
git branch
```
- 当前所在分支前会有一个星号(*)标记。

仅创建一个新分支而不立即切换过去：

```bash
git branch <branch-name>
```

#### 2. 合并分支

要将指定分支的更改合并到当前分支中：

```bash
git merge <branch-name>
```

- 如果合并过程是“快进模式”(Fast-forward)，意味着目标分支的所有提交都直接添加到当前分支的历史记录中。
- 若无法进行快进合并，则Git会尝试自动合并，若存在冲突则需要手动解决。

#### 3. 删除分支

当你确定不再需要某个分支时，可以将其删除：

```bash
git branch -d <branch-name>
```

- `-d` 选项用于安全删除，即只有当分支已完全合并时才允许删除。如果想强制删除未合并的分支，可以使用 `-D`。

| 操作                 | 命令                                               |
| -------------------- | -------------------------------------------------- |
| 查看所有分支         | `git branch`                                       |
| 创建分支             | `git branch <name>`                                |
| 切换分支             | `git checkout <name>` 或 `git switch <name>`       |
| 创建+切换分支        | `git checkout -b <name>` 或 `git switch -c <name>` |
| 合并某分支到当前分支 | `git merge <name>`                                 |
| 删除分支             | `git branch -d <name>`                             |

### 5.2 解决冲突

**示例情境**

假设我们有两个分支：`master` 和 `feature1`，它们分别对同一个文件（如 `readme.txt`）进行了不同的修改。当我们尝试将 `feature1` 合并到 `master` 时，Git 无法自动合并这些更改，从而导致了冲突。

#### 1. 创建与修改分支

- 在 `feature1` 分支上，我们将 `readme.txt` 文件的最后一行改为：
  ```
  Creating a new branch is quick AND simple.
  ```
- 切换回 `master` 分支，并将同一文件的最后一行改为：
  ```
  Creating a new branch is quick & simple.
  ```

#### 2. 尝试合并

执行合并命令：

```bash
git merge feature1
```

此时，Git 会报告一个冲突，因为它不知道应该保留哪个版本的更改。

---

#### 3. 解决冲突

* **打开产生冲突的文件（本例中为 `readme.txt`），你会看到类似以下内容：**

```txt
Creating a new branch is quick <<<<<<< HEAD
& simple
=======
AND simple
>>>>>>> feature1
```

这里，`<<<<<<< HEAD` 到 `=======` 表示当前分支（`HEAD`，即 `master`）的内容，而 `=======` 到 `>>>>>>> feature1` 则表示 `feature1` 分支的内容。

* **编辑文件解决冲突**

根据需要编辑文件以解决冲突。例如，我们可以选择其中一个版本或结合两者的信息：

```txt
Creating a new branch is quick and simple.
```

* **标记冲突已解决**

保存文件后，使用 `git add` 命令标记冲突已解决：

```bash
git add readme.txt
```

然后提交解决方案：

```bash
git commit -m "resolve conflict in readme.txt"
```

---

#### 4. 检查合并历史

为了查看合并的历史记录和分支图，可以使用如下命令：

```bash
git log --graph --pretty=oneline --abbrev-commit
```

这将展示一个简洁的分支合并图，帮助你理解项目的分支结构和合并历史。

#### 5. 删除已合并分支

一旦确认合并无误且不需要再保留该分支，可以通过以下命令删除它：

```bash
git branch -d feature1
```

注意，如果分支尚未完全合并，Git 将阻止其被删除，除非使用 `-D` 强制删除git
