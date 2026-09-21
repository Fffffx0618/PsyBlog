# PsyBlog

基于 MkDocs Material 的课程笔记。`docs/` 存放网站使用的 Markdown；
`example/` 中的 Obsidian 原稿和 PDF 用于比对，不参与构建。

## 本地预览

使用已有的 Conda 环境：

```sh
conda activate mkdocs-env
python -m pip install -r requirements.txt
mkdocs serve
```

打开终端显示的本地地址。仅生成静态网页时运行 `mkdocs build`，产物在 `site/`。

## 从 Obsidian 迁移笔记

1. 把 Markdown 放到 `docs/` 对应课程目录，附件放在该目录的 `images/` 中。
2. 先查看哪些文件需要转换：

   ```sh
   python scripts/migrate_obsidian.py docs/System/CO/Chapter2.md
   ```

3. 写入转换结果并检查 Git diff：

   ```sh
   python scripts/migrate_obsidian.py docs/System/CO/Chapter2.md --write
   ```

省略文件路径会处理整个 `docs/`。脚本只使用 Python 标准库，重复执行不会重复修改。
这是针对本仓库写法的迁移工具，不是完整的 Obsidian 解析器；块引用嵌入、
插件专用语法和缺失附件需要人工处理。

支持的转换包括：

- `> [!note] 标题` → `!!! note "标题"`，保留嵌套提示框。
- `[!type]-` → `??? type`，`[!type]+` → `???+ type`，保留折叠状态。
- 自定义提示框类型作为标题保留，以 `note` 样式显示。
- `![[图片.png|336x204]]` → 带宽高的图片，优先匹配当前目录和当前课程的 `images/`。
- 修复已有本地附件的相对路径；找不到的 Wiki 附件会报错，不会猜用其他课程的同名图。
- 将 `[[Chapter8|Cycle GAN]]` 转为当前目录内的 Markdown 链接；原深度学习目录的旧路径也会映射到新目录。
- 为列表、标题、提示框、块级公式补充段落边界，统一列表缩进。
- 把紧接正文的 `$$...$$` 拆成独立公式块，保留公式内容。
- 代码围栏中的内容和开头的 YAML 元数据不做语法替换。
- 修正围栏比代码正文缩进更深的情况，保留代码的相对缩进；未闭合围栏会报错，避免吞掉后续章节。

仍需人工检查：列表之后的文字属于列表项还是独立段落、未闭合的代码围栏/HTML、
以及图片宽度是否符合实际内容。提示框内的所有段落、代码块和图片都应缩进 4 个空格。

```markdown
!!! note "Register vs. Memory"

    - Registers are faster to access than memory
    - Operating on memory data requires loads and stores
        - More instructions to be executed

    <div style="text-align: center">
      <img src="images/image-22.png" width="70%" alt="字节序示意图">
    </div>
```

`mkdocs.yml` 已加载公式、高亮、表格和提示框扩展。迁移后使用标准图片引用，
不再启用 roamlinks，避免把 Python 的 `[[1, 2], [3, 4]]` 等代码误当成 Wiki 链接。

代码高亮使用 `pymdownx.highlight` + `pymdownx.superfences`，依赖中固定了验证过的
`pymdown-extensions==12.0.1`。旧环境中的 10.20.1 与 Pygments 2.20 组合会让围栏代码退化为
行内代码，或在处理缩进代码时抛出 `NoneType ... replace` 错误，因此已有环境也需要安装一次依赖。

## 样式与检查

`docs/stylesheets/extra.css` 在 `blueTopaz.css` 后加载，调整标题、列表、浅蓝提示框、
表格和强调色，使正文接近参考 PDF。窄屏保留表头并横向滚动表格。
网页会随屏幕宽度重排，不复刻 PDF 的 A4 分页。

迁移脚本测试：

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

同步新增/删除笔记后，更新 `mkdocs.yml` 的导航并运行 `mkdocs build --strict`，
检查目录和文章链接是否仍指向存在的文件。
