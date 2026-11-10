# Keith的学习空间

具身智能学习与研究笔记，关注 **2023 年以来**的 VLM、VLA、具身智能体与世界模型。

[网站](https://keith-814.github.io/Keith-s-EAI-Learning/) · [研究笔记](https://keith-814.github.io/Keith-s-EAI-Learning/research/)

## 当前内容

- **VLA 综述**：转载自 Tingde Liu，保留原作者和来源。
- **世界模型综述**：转载自 Tingde Liu，保留原作者和来源。
- 时间线、学习记录和关于页面的框架已建立，后续内容由阅读逐步补充。

正文和参考图保持来源版本；早期背景未删减。后续个人时间线重点限定为 2023 年以来的工作。

## 首次发布

进入仓库 **Settings → Pages → Build and deployment → Source**，选择 **GitHub Actions**。

向 `main` 推送后，Actions 会安装依赖、构建 Jekyll、检查本地链接与图片并自动发布。首次发布如提示 Pages 未启用，按上一步设置后到 Actions 手动运行该工作流。

项目地址使用 `/Keith-s-EAI-Learning/` 子路径，由 `_config.yml` 的 `baseurl` 管理。不要把资源路径直接写为 `/images/...`，应使用 `{{ '/images/...' | relative_url }}`。

## 日常维护

| 修改目标 | 文件 |
| --- | --- |
| 两篇综述正文 | `_posts/research/*.md` |
| 首页文章列表 | `_includes/home-index.html`、`_includes/file-row.html`（自动读取文章） |
| 研究页分组 | `_data/research_groups.json` |
| 时间线 | `pages/timeline.md` |
| 学习记录入口 | `pages/blog.html` |
| 站点名称与导航 | `_config.yml` |
| 布局与公共组件 | `_layouts/`、`_includes/` |
| 自动发布 | `.github/workflows/deploy.yml` |

新增个人笔记：复制 `templates/paper.md` 到 `_posts/blog/YYYY-MM-DD-title.md`，填写标题、日期和内容。`categories: blog` 会自动进入学习记录列表。

新增研究文章：放入 `_posts/research/`，设 `categories: research`，首页和研究列表会自动收录。需要归入特定研究分组时，在 `_data/research_groups.json` 中添加 slug。

## 发布新的 Markdown 文章

当前发布链路：**新增或修改 `.md` → 提交到 `main` → GitHub Actions 构建并检查 → GitHub Pages 更新网站**。不需要手动转换 HTML，也不要把文章上传到 `_site/`；该目录是构建结果，会在下次构建时重新生成。

### 1. 选择目录和文件名

| 内容类型 | 保存位置 | 头部分类 | 网站入口 |
| --- | --- | --- | --- |
| 个人论文笔记、方法比较、实验记录 | `_posts/blog/YYYY-MM-DD-slug.md` | `categories: blog` | 自动进入“学习记录”和首页列表 |
| 研究综述、主题文章 | `_posts/research/YYYY-MM-DD-slug.md` | `categories: research` | 自动进入“研究”和首页列表；分组配置见第 4 步 |

例如：`_posts/blog/2026-11-10-openvla-notes.md`。文件名必须包含日期前缀，建议使用英文小写 slug，并用连字符连接单词；页面标题仍可用中文。

当前 `_config.yml` 设置 `permalink: /:title/`，默认以文件名去掉日期和扩展名后的 slug 生成地址。上述文件会发布到：

```text
https://keith-814.github.io/Keith-s-EAI-Learning/openvla-notes/
```

`title` 字段决定显示标题，修改它通常不会改变文章地址。不要让两篇文章使用相同 slug，即使分属 `blog`、`research` 目录，也会生成相同地址。已经发布的文件不要随意改 slug，以免原链接失效。

### 2. 添加文章头部

可以复制 `templates/paper.md`，也可以在现有 `.md` 顶部添加以下内容。头部必须放在文件开头，两端的 `---` 都要保留，正文放在第二个 `---` 后面。

```markdown
---
layout: post
title: "OpenVLA 阅读笔记"
date: 2026-11-10
author: Keith
categories: blog
tags: [VLA, Robotics]
toc: true
excerpt: "整理 OpenVLA 的模型结构、训练数据与实验结果。"
---

## 基本信息

- 论文：https://arxiv.org/abs/2406.09246
- 阅读状态：初读

## 研究问题

在这里填写正文。

## 方法

## 实验与局限

## 待核实
```

| 参数 | 用途与填写方式 |
| --- | --- |
| `layout` | 固定填 `post`，使用文章页面模板。 |
| `title` | 网页标题，建议使用双引号，尤其是含冒号时。 |
| `date` | 文章日期，使用 `YYYY-MM-DD`；决定日期显示及当前列表排序。建议与文件名日期一致。 |
| `author` | 作者元数据；个人笔记填 `Keith`。 |
| `categories` | 填 `blog` 或 `research`，决定列表归属；仅放进对应文件夹不足以完成分类。 |
| `tags` | 可选，用方括号填写主题标签，如 `[VLA, Robotics]`。 |
| `toc` | `true` 开启目录，`false` 关闭。目录从正文标题生成。 |
| `excerpt` | 建议填写简短、客观的摘要，用于文章头部；列表只显示标题、分类和日期。 |
| `last_modified_at` | 可选，文章修订日期，如 `2026-11-12`；文章头部优先显示此日期，当前列表仍按 `date` 排序。 |
| `published` | 草稿可加 `published: false`，正常构建不会发布；发布前删除此行或改为 `true`。 |

本站已启用 `future: true`，**未来日期不会阻止文章发布**，请使用 `published: false` 保存草稿。YAML 用空格缩进，不要用 Tab；`true`、`false` 使用英文小写。普通自写笔记无需复制转载文章的 `original_url`、`imported_at`、`source_revision` 或 `vla_survey` 等专用字段。

文章模板已经显示 `title`，正文一般从 `##` 开始，无需重复写一遍 `# 文章标题`。

### 3. 添加图片和站内链接

把图片放到仓库的 `images/` 下，例如：

```text
images/openvla-notes/architecture.webp
```

在 Markdown 中引用：

```markdown
![模型结构示意图]({{ '/images/openvla-notes/architecture.webp' | relative_url }})

[查看 VLA 综述]({{ '/VLA-Survey/' | relative_url }})
```

`relative_url` 会自动加上项目子路径 `/Keith-s-EAI-Learning`。不要使用电脑上的绝对路径、`file://` 地址，也不要直接写 `/images/...`；这些路径在 Pages 网站上无法正确定位。文件名和大小写必须与仓库一致，图片需要和文章一起提交。引用外部论文可直接使用完整 `https://...` 地址。

代码块使用三个反引号并注明语言，例如 `python`。数学公式可用 `$...$` 或 `$$...$$`；Mermaid 图表使用 `mermaid` 代码块。公式和图表增强依赖公共 CDN，发布成功不代表离线环境也能加载这些功能。

### 4. 首页收录与研究分组

首页自动读取所有已发布文章，按 `date` 从新到旧排列，每篇一行显示标题、分类和日期。不需要手动添加首页入口，`_data/home_tree.yml` 是历史首页配置，当前首页不再读取它。

个人笔记设置 `categories: blog`，即可同时进入首页和“学习记录”。研究文章设置 `categories: research`，即可同时进入首页和“研究”。未配置研究分组时，首页分类显示“研究”，研究页归入“其他”。

如果希望文章归入已有研究方向，在 `_data/research_groups.json` 对应分组的 `slugs` 中添加文件名去掉日期和扩展名后的值。例如新增 `_posts/research/2026-11-10-action-models.md`，在 VLA 分组中添加 `action-models`：

```json
{
  "id": "vla",
  "zh": "VLA · 动作策略",
  "en": "VLA",
  "slugs": ["VLA-Survey", "action-models"]
}
```

这是数组内的一个分组对象，不要用它覆盖整个 JSON 文件；保留外层 `[]` 和其他分组，注意逗号。分组的 `zh` 是列表显示的分类名称。新增研究方向时，可在数组中添加具有独立 `id` 的分组对象。

### 5. 提交文件：两种方式任选一种

**方式 A：直接在 GitHub 网页操作，无需安装 Ruby。**

1. 打开仓库，确认分支选择为 `main`。
2. 新建文章时点击 **Add file → Create new file**，文件名填写完整路径，例如 `_posts/blog/2026-11-10-openvla-notes.md`，粘贴含头部的正文。已有 `.md` 文件可先进入 `_posts/blog/` 或 `_posts/research/`，再用 **Add file → Upload files** 上传。
3. 点击 **Commit changes**，填写提交说明，例如 `Add OpenVLA reading notes`。有写权限时可直接提交到 `main`；若选择新分支，则需创建 Pull Request 并合并到 `main` 后才会上线。
4. 有图片时，在相应 `images/` 子目录上传并提交图片；有首页或分组调整时，一并保存相关配置。网页分次提交会触发多次构建，期间缺少图片可能导致检查失败；全部文件提交齐后查看最后一次运行。

**方式 B：在电脑上编辑后提交。**

在仓库根目录执行。以下以个人笔记为例；按实际情况调整文件名和需要提交的文件：

```bash
# 创建目录并复制笔记模板
mkdir -p _posts/blog
cp templates/paper.md _posts/blog/2026-11-10-openvla-notes.md

# 编辑新文件，填写日期、标题、摘要和正文；有配图时将其放入 images/

# 如已安装 Ruby 3.2 和 Bundler，可先运行本地检查
bundle install
bundle exec jekyll build
python3 scripts/check_site.py

# 检查实际修改，再明确选择需要发布的文件
git status --short
git diff
git add _posts/blog/2026-11-10-openvla-notes.md
# 有配图或研究配置修改时，再添加对应文件，例如：
# git add images/openvla-notes/ _data/research_groups.json
git diff --cached

git commit -m "Add OpenVLA reading notes"
git push origin main
```

上述命令假设你正在 `main` 分支，且与远端同步；其他分支应通过 Pull Request 合并。新建且未跟踪的文件不会出现在普通 `git diff` 中，可直接打开检查，添加后再看 `git diff --cached`。不要提交 `_site/`、`vendor/`、`.bundle/` 或本地缓存。没有本地 Ruby 环境也可提交源码，由 Actions 执行相同构建检查。

### 6. 确认网站已更新

1. 进入仓库 **Actions**，打开 **Build and deploy research notes** 的最新运行，确认对应刚才的提交。
2. `build` 会安装依赖、构建 Jekyll、检查站内链接与必要资源，再上传网站产物。
3. `deploy` 依赖 `build` 成功，且仅在 `main` 的非 Pull Request 运行中发布。**Pull Request 的检查通过不等于网站已更新。**
4. 等 `build`、`deploy` 都成功后，从部署环境的链接打开网站，或直接访问文章地址；再确认研究列表、学习记录或首页入口符合预期。
5. 首次使用需在 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。需要手动重试时，在 Actions 中选择该工作流，点 **Run workflow**，分支选 `main`。

网站只会在相关提交成功部署后更新，不需要自行上传 HTML。如果连续推送，工作流会取消同一分支上较早的运行，请以最新提交对应的运行结果为准。

### 7. 常见问题

| 现象 | 排查位置 |
| --- | --- |
| 构建出现红叉 | 打开失败运行的具体步骤和摘要；`Build Jekyll` 失败时先检查 YAML 头部、Liquid 语法和报错文件行号。 |
| `Check site links and assets` 失败 | 查看日志里的 `页面 -> 路径`，核对图片是否上传、大小写是否一致、目标页面是否存在。当前检查不验证外部网址或页内锚点，需手动点开确认。 |
| 文章地址 404 | 确认已提交到 `main`、部署成功、文件名满足日期规则、含 Front Matter、未设 `published: false`；网址使用 slug，并包含项目子路径。 |
| 地址能打开，但列表没有文章 | 核对 `categories`，分类值必须与模板中的 `blog`、`research` 一致。 |
| 首页分类未显示研究方向 | 检查 `_data/research_groups.json` 对应分组是否添加了正确 slug。首页自动收录文章，不需要修改首页配置。 |
| 图片在本地正常，线上不显示 | 确认已提交图片，使用 `relative_url`，路径不是本地磁盘地址，文件名大小写一致。 |
| 网页仍显示旧版本 | 确认最新提交的 `deploy` 成功；浏览器强制刷新。仅提交到其他分支或仅通过 PR 检查不会更新正式站点。 |
| 修改后未重新触发部署 | 确认推送目标是 `main`；必要时手动运行工作流，查看是否有待审批或 Pages 环境配置问题。 |


## 本地预览

使用 Ruby 3.2 和 Bundler：

```bash
bundle install
bundle exec jekyll serve --baseurl /Keith-s-EAI-Learning
```

打开 http://127.0.0.1:4000/Keith-s-EAI-Learning/ 。修改 `_config.yml` 后需要重启预览。

发布前检查：

```bash
bundle exec jekyll build
python3 scripts/check_site.py
```

界面采用固定浅色与精简导航，站点标题为“Keith的学习空间”。首页自动收录已发布文章，首页、研究和学习记录均采用单行列表，显示标题、分类和日期。定制样式集中在 `assets/css/learning.css`。转载署名和许可保留在文章末尾及关于页面。

数学公式和 Mermaid 图由公共 CDN 加载；无网络时正文仍可读取，但公式、图表增强可能不可用。

### 构建排查记录（2026-11-09）

历史参考：Jekyll 4.3.4 + `jekyll-sass-converter` 2.2.0（SassC）会将含 CSS 变量的 `min()` 误作 Sass 数值函数，导致图片样式编译失败。当前两处规则通过 `unquote("min(...)")` 输出原生 CSS，保持浏览器中的尺寸行为。已用相同 Jekyll / Sass 编译器在本地验证构建和链接检查；其他编译器版本需按实际日志判断，勿将此记录视为通用要求。

## 与 AI 协作

在 AI 编程工具中打开此仓库，直接让其编辑 Markdown。例如：“依据这篇论文填写笔记模板，结论标注原文节号，不确定处标待核实；不要改写转载综述的作者判断。”

先检查本地差异，再提交推送。论文原文作为最终依据。

## 来源与许可

网站框架改编自 [Tingde Liu · Research Notes](https://github.com/TingdeLiu/tingdeliu.github.io)，保留 MIT 许可证。两篇转载文章原作者为 Tingde Liu，适用 CC BY 4.0。配图保留原权利归属，具体见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 与 [LICENSE-CONTENT](LICENSE-CONTENT)。
