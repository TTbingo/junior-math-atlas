# CLAUDE.md — 初中数学知识图谱

纯静态站：`content/*.json` → `build.py`（Python 标准库，零依赖）→ `dist/`。
体系：三大领域（代数 / 几何 / 统计与概率）→ 主题 → 知识点，脉络依据资料库《初中数学思维导图》；
《中考冲刺专题突破·数学》(2024) 只作为内容与例题来源，不决定目录结构。对外说明见 `README.md`，本文只写「改代码/写内容时必须知道」的规则。

## 命令速查

```bash
python tools/restructure.py     # 改领域/主题/知识点清单后重新生成 modules.json
python build.py                 # 构建 dist/
python build.py --check         # 只校验：死链/裸公式/禁用词/十板块/模板残留
python tools/check_content.py   # 内容体检：前置顺序、前置≠关联、场景重复、跳步话术、公式配对、概念超前引用
MATH_NO_CLEAN=1 python build.py # 原地覆盖（沙箱禁止整树删 dist 时用）
```

## 硬规则

1. **只改 `content/`，不手改 `dist/`**；`dist/` 是产物，重跑 build 即覆盖。
2. **id 规则**：`m{领域}-{主题}-{序号}-{slug}`，前两段必须在 `modules.json` 中已定义，且该 id 出现在所属主题的 `points` 清单里，否则校验失败。`point_titles` 存全部 61 个知识点中文名，待写条目靠它显示标题。
3. **十板块齐全**：`explanation / scenarios / cautions / why / method / examples / inferences / pitfalls / intuition / related`。`why` 必须含 `steps`（≥2）与 `experiment`；`method` 写「解题思路」，不是知识点复述。
4. **前置 ≠ 关联**：`prerequisites` 必须是排在本文之前的真先修，且不得出现在 `related` 中。小学站的 87 条前置错误就是把 `related[0]` 直接抄成前置，`check_content.py` 会拦。
5. **`related` 单向书写**：构建时 `idx.incoming` 自动补「指向本知识点」分组；两向都写会重复（`render_related` 有去重兜底，但数据应单向）。
6. **允许写「证明」**，但禁用跳步话术 `显然 / 易证 / 不难看出`；几何证明必须写全判定依据（如 SAS 的三组条件）。
7. **例题**：≥3 道，场景取自 `taxonomy.scenes` 且同页不重复；`solution` 写完整算式，`answer` 给结论；数值必须自己验算一遍。
8. **SVG 是 XML**：文本中 `<`、`>` 写成 `&lt;`、`&gt;`；`media` 的 `width/height` 必须与 `viewBox` 一致，否则图被拉伸或裁切。

9. **不得超前引用概念**：正文不许把排在后面的点位才引入的概念当解释工具。`check_content.py` 的 `CONCEPT_INTRO` 表会拦（抛物线 / 二次函数 / 一次函数 / 反比例函数 / 双曲线 / 平面直角坐标系 / 判别式）。确需借用，同一段必须写明「提前借用」「后续学习」「等学了」等字样，否则报错。
   - 背景（2026-11-04）：二元一次方程组用「一个二元一次方程像一条直线：满足它的点有无穷多个，两个方程就是两条直线，交点就是唯一解」当直观理解的主框架，而坐标系与一次函数分别排在 `m1-03-01` / `m1-03-02`。**`prerequisites` 顺序对，不代表正文没超前引用**——旧版 check_content 只查字段，查不出这种。

10. **配图三件套必须一一对齐**：`media[].alt`（描述）、`media[].caption`（图注）、SVG 内实际画的内容与文字标注，三者要讲同一件事、同一个数。改正文里的面积/块数/边长，必须同步改 alt、caption 与 SVG 内文字。
    - 背景（2026-11-04）：`radical-simplify.svg` 画的是「面积 12 切成 4 块、每块面积 3、边长 2√3」（正确），正文却写「先取一块面积 4 的正方形，剩下面积 3」（12−4=8≠3，错），alt 写「三个面积 4 的小正方形并排」（错），caption 写「边长 2 的整块 + 剩下的部分」（错）。**图是对的、字全错，且图文互相矛盾**——只截图看图的复核方式查不出来，必须读图内的 `text` 元素再和正文对照。

11. **交付前的读内容复核**：`build.py --check` 只保证结构（链接、公式渲染、十板块、禁用词），`check_content.py` 只保证语义规则，两者都不读数学。每批内容交付前必须逐篇通读一遍 `sections` 的正文，例题逐题复算，配图 `text` 与正文交叉核对。**不要用「校验全绿」代替「内容读过」。**

## 环境陷阱（继承自小学站，已踩过）

- 目标篇目未写作时，`related` / `prerequisites` 指向它会触发 KeyError —— 两处渲染已加「未成稿则跳过」保护，新增引用不必等对方成稿。
- `build.py --check` 的产物自检按 `taxonomy.sections` 的标题逐页比对，改板块标题会让所有旧页失败，改标题要同步重构建。
- 禁用词来自 `taxonomy.forbidden_words`，不再有硬编码常量。
- workbuddy.host 部署需 `?sharecode=`，子资源由 HttpOnly cookie 放行，产物内不嵌分享码（若后续部署沿用此通道）。

## 目录职责

| 路径 | 作用 |
|---|---|
| `content/modules.json` | 3 领域 / 12 主题 / 61 知识点清单 + 中文名映射 |
| `content/points/*.json` | 正文，一篇一文件 |
| `content/media/*.svg` | 配图；`map-*.svg` 是三个领域的知识脉络图（模块页顶部渲染） |
| `tools/restructure.py` | 由脚本内的 `MODULES`/`TOPICS` 定义生成清单，改体系只改脚本 |
| `tools/gen_maps.py` | 读 modules.json 生成 `map-*.svg`；脉络图不再手改，改清单后重跑 |
| `tools/check_content.py` | 内容语义体检 |
| `build.py` | 构建 + `verify_output()` 产物自检 |

12. **脉络图**：`modules.json` 每个领域带 `map` 字段指向 `content/media/map-*.svg`，模块页据此渲染；`viewBox` 宽固定 760、内置字号 ≥12px，否则缩放后看不清。
