# Keith's EAI Learning

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
| 首页研究地图 | `_data/home_tree.yml` |
| 研究页分组 | `_data/research_groups.json` |
| 时间线 | `pages/timeline.md` |
| 学习记录入口 | `pages/blog.html` |
| 站点名称与导航 | `_config.yml` |
| 布局与公共组件 | `_layouts/`、`_includes/` |
| 自动发布 | `.github/workflows/deploy.yml` |

新增个人笔记：复制 `templates/paper.md` 到 `_posts/blog/YYYY-MM-DD-title.md`，填写标题、日期和内容。`categories: blog` 会自动进入学习记录列表。

新增研究文章：放入 `_posts/research/`，设 `categories: research`，并把文件名去掉日期后的 slug 加入首页与研究分组配置。

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

数学公式和 Mermaid 图由公共 CDN 加载；无网络时正文仍可读取，但公式、图表增强可能不可用。

### 构建排查记录（2026-11-09）

历史参考：Jekyll 4.3.4 + `jekyll-sass-converter` 2.2.0（SassC）会将含 CSS 变量的 `min()` 误作 Sass 数值函数，导致图片样式编译失败。当前两处规则通过 `unquote("min(...)")` 输出原生 CSS，保持浏览器中的尺寸行为。已用相同 Jekyll / Sass 编译器在本地验证构建和链接检查；其他编译器版本需按实际日志判断，勿将此记录视为通用要求。

## 与 AI 协作

在 AI 编程工具中打开此仓库，直接让其编辑 Markdown。例如：“依据这篇论文填写笔记模板，结论标注原文节号，不确定处标待核实；不要改写转载综述的作者判断。”

先检查本地差异，再提交推送。论文原文作为最终依据。

## 来源与许可

网站框架改编自 [Tingde Liu · Research Notes](https://github.com/TingdeLiu/tingdeliu.github.io)，保留 MIT 许可证。两篇转载文章原作者为 Tingde Liu，适用 CC BY 4.0。配图保留原权利归属，具体见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 与 [LICENSE-CONTENT](LICENSE-CONTENT)。
