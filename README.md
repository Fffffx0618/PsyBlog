# PsyBlog

基于 Zensical（classic 外观）的课程笔记。`docs/` 存放网站使用的 Markdown；
`example/` 中的 Obsidian 原稿和 PDF 用于比对，不参与构建。

## 本地预览

使用已有的 Conda 环境：

```sh
conda activate mkdocs-env
python -m pip install -r requirements.txt
zensical serve
```

打开终端显示的本地地址。仅生成静态网页时运行 `zensical build`，产物在 `site/`。

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

网站通过 `mkdocs.yml` 的 `extra_css` 加载唯一的正文主题文件
`docs/stylesheets/blue-topaz.css`。Zensical 继续使用兼容的 YAML 配置。
`about-me.css` 只供独立的 `AboutMe.html` 使用，不加载到笔记页面。

主题选取本地 Blue Topaz `theme.css` 的默认浅色／深色阅读配色，
保留原变量名，并通过 `--md-*` 变量和 `.md-typeset` 选择器映射到 Zensical：

| Blue Topaz | Zensical / Markdown |
| --- | --- |
| `.theme-light` / `.theme-dark` | `default` / `slate` |
| `--background-primary`、`--text-normal`、`--text-muted` | 页面背景、正文、次要文字 |
| `--h1-color` … `--h6-color` | 六级标题；深色模式保留原来的彩色标题 |
| `--accent-strong`、`--accent-em`、`--strong-em-color-*` | 粗体、斜体、粗斜体渐变 |
| `--text-accent`、`--text-selection` | 链接、选中文字 |
| `--text-highlight-bg`、`--bg-color-highlight-*` | 普通、斜体、粗体、粗斜体高亮 |
| `--text-color-code`、`--background-code-2` | 行内代码文字和底色 |
| `code-theme-bt-default`（叠加主题共用代码配色） | Pygments 对应的 `--md-code-hl-*` 语义颜色 |
| 原站引用配色、`--text-normal` | 引用保留灰色文字／边线和透明背景；无序列表标记跟随正文 |
| `--table-*-color` | 表格背景、表头、边框、斑马纹和悬停 |

Obsidian 的 CodeMirror/Prism 与 Zensical 的 Pygments 分词不同，代码颜色按语义对应，
不会保证每一段代码的每个 token 完全相同。提示框沿用 Obsidian 核心的类型配色，
映射为原生 admonition / details，保留图标、折叠和嵌套。
此移植不加载 Obsidian 编辑器、插件界面、背景图片或可选配色方案。
Blue Topaz 的 MIT 许可已保留在样式文件头部。

字号设置集中在文件顶部：根字号 `125%`，正文 `--bt-body-size: .8rem`，
浏览器默认字号为 16 时正文仍为 16；增大浏览器默认字号或页面缩放时同步放大。
标题使用 `rem`（沿用原主题的标题／正文比例），代码、表格等使用 `em` 跟随上下文。
不再按显示器宽度突然切换根字号。正文最大宽度使用 `rem`，图片自适应，
表格和宽公式在窄屏横向滚动。修改整体正文大小时，也可同时调整标题的 `rem` 值。

官方扩展方式与字体变量说明：[自定义样式](https://zensical.org/docs/customization/)、
[字体](https://zensical.org/docs/setup/fonts/)。

迁移脚本测试：

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

同步新增/删除笔记后，更新 `mkdocs.yml` 的导航并运行 `zensical build --clean`，
检查目录和文章链接是否仍指向存在的文件。
