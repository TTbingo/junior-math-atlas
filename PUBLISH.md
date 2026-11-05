# 初中数学知识图谱 · workbuddy.host 发布包

本目录是**初中站**（`TTbingo/junior-math-atlas`）的静态产物，用于发布到 workbuddy.host。

## 为什么单独一个目录

WorkBuddy 的发布工具按 **workspace 根目录**（含 `.wbapp_*.genie` 标记的那一层）绑定 app，
而不是按传入的 `directory` 绑定。同一个 workspace 里已经有「小学数学知识点图谱」
（appId `wbapp_kHGLrsiTw1074ukrOuud1h`，域名 `primary-math-atlas.app.workbuddy.host`），
**再往这个 workspace 发布会直接覆盖小学站**——2026-11-05 已踩过一次并恢复。

所以初中站要拿到自己的 app（域名 `junior-math-atlas.app.workbuddy.host`），
必须在一个**没有 .genie 标记的全新 workspace** 里发布。

## 发布步骤

1. 在 WorkBuddy 里新建一个会话，工作目录选一个**全新的空目录**（不要选到本仓库所在 workspace）。
2. 把本目录的内容复制到那个新目录，或直接把 `directory` 指向本目录（若工具允许跨 workspace）。
3. 执行发布：

```
workbuddy_sites_deploy(
  directory="<新目录绝对路径>",
  appName="初中数学知识图谱",
  domainPrefix="junior-math-atlas",
  entryHtml="index.html",
  language="static",
  userAskedToPublish=True,
)
```

4. 拿到链接后验证（需带分享码，裸请求 403）：

```bash
curl -s "https://junior-math-atlas.app.workbuddy.host/?sharecode=XXXX" | grep -o "<title>[^<]*</title>"
# 期望：<title>初中数学知识图谱</title>
```

5. 确认小学站没被影响：

```bash
curl -s "https://primary-math-atlas.app.workbuddy.host/?sharecode=BYT4SQX5HE" | grep -o "<title>[^<]*</title>"
# 期望：<title>小学数学知识点图谱</title>
```

## 本目录内容

`dist/` 的完整拷贝（218 个文件）：首页、3 个模块页、12 个主题页、61 个知识点页、
CSS/JS/本地化 KaTeX、65 张 SVG 配图。

线上版本已同时发布在 GitHub Pages：
<https://ttbingo.github.io/junior-math-atlas/>
