"""生成初中站骨架：taxonomy / site / modules / standards。

体系来源：《中考冲刺专题突破·数学》(2024) 三部分
  第一部分 玩转基础 31 讲 → 第二部分 专题专练 31 微专题 → 第三部分 满分突破 25 微专题
只生成清单（modules.json），正文由 content/points/*.json 逐篇补。
"""
import json
import pathlib

C = pathlib.Path(__file__).resolve().parent.parent / "content"

SECTIONS = [
    ("explanation", "说明", "paragraphs", 120),
    ("scenarios", "使用场景", "paragraphs", 100),
    ("cautions", "注意点", "paragraphs", 80),
    ("why", "原理：为什么成立", "why", 0),
    ("method", "解题思路", "paragraphs", 140),
    ("examples", "按场景的例题", "examples", 3),
    ("inferences", "常用推论", "items", 2),
    ("pitfalls", "易错点", "pitfalls", 2),
    ("intuition", "直观理解", "text", 80),
    ("related", "关联知识点", "related", 2),
]

TAX = {
    "schema": 1,
    "site_title": "初中数学专题图谱",
    "domains": ["数与代数", "图形与几何", "统计与概率", "综合与实践"],
    "segments": {"4": "第四学段（7~9 年级）"},
    "strands": {
        "数与代数": ["数与式", "方程与不等式", "函数"],
        "图形与几何": ["图形的性质", "图形的变化", "图形与坐标"],
        "统计与概率": ["抽样与数据分析", "随机事件的概率"],
        "综合与实践": ["主题活动", "项目学习"],
    },
    "verbs": {
        "了解": ["知道", "初步认识"],
        "理解": ["认识", "会"],
        "掌握": ["能"],
        "运用": ["证明", "应用"],
        "经历": ["感受", "尝试"],
        "体验": ["体会"],
        "感悟": [],
        "探索": [],
    },
    "verb_to_difficulty": {
        "了解": 1, "经历": 1, "感悟": 1, "体验": 1,
        "理解": 2, "认识": 2, "会": 2,
        "掌握": 3, "能": 3, "运用": 4,
    },
    "literacy": ["抽象能力", "运算能力", "几何直观", "空间观念", "推理能力",
                  "数据观念", "模型观念", "应用意识", "创新意识"],
    "scopes": {"core": "中考必考", "common": "中考常见", "extended": "压轴拓展"},
    "scenes": ["测量与工程", "行程与速度", "销售与利润", "方案选择", "图形设计",
               "竞技与游戏", "数据调查", "金融与增长", "物理情境", "生活优化"],
    "sections": [
        {"key": k, "title": t, "kind": kind, "min_len": mn}
        for k, t, kind, mn in SECTIONS
    ],
    # 初中允许「证明」，但禁止跳步话术：结论必须写出理由链
    "forbidden_words": ["显然", "易证", "不难看出"],
}

SITE = {
    "schema": 1,
    "title": "初中数学专题图谱",
    "subtitle": "按《中考冲刺专题突破》三部分梳理：先夯实考点，再炼模型，最后冲满分",
    "nav": [{"label": "全部知识点", "href": "index.html"}],
    "default_theme": "auto",
    "source_note": "体系依据《中考冲刺专题突破·数学》(2024) 三部分；原理与解题思路按中考通法重写，例题均为自编并逐题验算。",
}

# (模块 id, 标题, 简称, 描述, 领域, 主题定义)
# 主题: (节 id 后缀, 标题, 描述, 领域, [(序号, 标题, slug)])
PARTS = [
    ("m1", "第一部分 · 玩转基础", "基础",
     "31 讲覆盖中考全部考点：数与式、方程与不等式、函数、三角形与四边形、相似、圆、图形变换、统计与概率。先把概念和定理的来路讲清，再练基础题型。",
     [
         ("01", "数与式", "实数、整式、二次根式、因式分解、分式：初中代数的全部语言。", "数与代数",
          [(1, "实数", "real-numbers"),
           (2, "整式", "integral-expressions"),
           (3, "二次根式", "quadratic-radicals"),
           (4, "因式分解", "factorization"),
           (5, "分式", "algebraic-fractions")]),
         ("02", "方程与不等式", "从一元一次到一元二次：等式与不等式的变形规则、解的判定。", "数与代数",
          [(1, "一次方程（组）", "linear-equations"),
           (2, "分式方程", "fractional-equations"),
           (3, "一元二次方程", "quadratic-equations"),
           (4, "根的判别式与根与系数的关系", "discriminant-vieta"),
           (5, "一元一次不等式（组）", "linear-inequalities")]),
         ("03", "函数", "坐标系是舞台，函数是主角：一次、反比例、二次三类函数的图象与性质。", "数与代数",
          [(1, "平面直角坐标系与函数", "coordinate-system-functions"),
           (2, "一次函数", "linear-function"),
           (3, "反比例函数", "inverse-proportion"),
           (4, "二次函数的图象和性质", "quadratic-graph"),
           (5, "二次函数综合题", "quadratic-comprehensive"),
           (6, "二次函数的应用", "quadratic-applications")]),
         ("04", "三角形与四边形", "几何证明的主战场：全等、特殊三角形、平行四边形家族的判定与性质。", "图形与几何",
          [(1, "几何初步", "geometry-basics"),
           (2, "三角形及特殊三角形", "triangles"),
           (3, "全等三角形", "congruence"),
           (4, "直角三角形的边角关系", "right-triangle-ratios"),
           (5, "四边形与平行四边形", "quadrilaterals"),
           (6, "特殊的平行四边形", "special-parallelograms")]),
         ("05", "相似图形", "相似是长度的比例语言：判定、性质、与全等的分工。", "图形与几何",
          [(1, "相似图形（一）", "similarity-1"),
           (2, "相似图形（二）", "similarity-2")]),
         ("06", "圆", "圆的基本性质、直线与圆的位置关系、弧长扇形与圆锥的计算。", "图形与几何",
          [(1, "圆的基本性质", "circle-properties"),
           (2, "直线与圆的位置关系", "line-circle-position"),
           (3, "圆的有关计算", "circle-calculations")]),
         ("07", "图形变换与投影", "平移、旋转、轴对称三把手术刀，加上三视图。", "图形与几何",
          [(1, "平移、旋转与对称", "transformations"),
           (2, "投影与视图", "projection-views")]),
         ("08", "统计与概率", "数据的收集与整理、概率的古典计算。", "统计与概率",
          [(1, "数据的收集与整理", "data-collection"),
           (2, "概率", "probability")]),
     ]),
    ("m2", "第二部分 · 专题专练", "专题",
     "31 个微专题，把中考高频模型一次讲透：全等的四种辅助线、相似的四种结构、圆与最值的四类构图、函数与应用的固定套路。每个专题只回答两件事——识别信号是什么，为什么要这样作辅助线。",
     [
         ("01", "含参与方程不等式", "参数藏在系数里：分类讨论的边界在哪里。", "数与代数",
          [(1, "含参分式方程", "parametric-fractional"),
           (2, "含参不等式（组）", "parametric-inequalities")]),
         ("02", "几何基础与全等模型", "中点、角平分线、垂直三类信号对应的辅助线。", "图形与几何",
          [(1, "几何初步相关模型", "geometry-models"),
           (2, "倍长中线模型", "double-median"),
           (3, "截长补短模型", "cut-and-supplement"),
           (4, "一线三垂直模型", "three-perpendiculars"),
           (5, "三角形的中位线", "triangle-midline")]),
         ("03", "相似模型", "从「一线三等角」到「子母型」：比例关系的四种常见来源。", "图形与几何",
          [(1, "一线三等角模型", "equal-angles"),
           (2, "子母型相似", "mother-child-similarity"),
           (3, "基本相似模型", "basic-similarity"),
           (4, "相似图形综合", "similarity-comprehensive")]),
         ("04", "圆与最值模型", "动点轨迹、定边定角、将军饮马、阿氏圆：最值问题的几何解法。", "图形与几何",
          [(1, "四点共圆", "concyclic"),
           (2, "定义圆与定边定角", "defined-circle"),
           (3, "将军饮马与点圆最值", "drinking-horse"),
           (4, "胡不归与阿氏圆", "apollonius"),
           (5, "逆等线与费马点", "fermat-point"),
           (6, "定值", "fixed-value"),
           (7, "圆综合", "circle-comprehensive")]),
         ("05", "图形变换专题", "旋转出全等，折叠出等腰：变换背后的不变量。", "图形与几何",
          [(1, "图形的旋转", "rotation"),
           (2, "图形的平移与折叠", "folding")]),
         ("06", "函数专题", "反比例与二次函数的综合套路：k 的几何意义、存在性与面积。", "数与代数",
          [(1, "反比例函数 k 的求法", "inverse-k"),
           (2, "反比例函数综合", "inverse-comprehensive"),
           (3, "二次函数中多边形的存在性", "quadratic-polygon-existence"),
           (4, "二次函数中面积的计算", "quadratic-area")]),
         ("07", "应用题与创新", "把文字翻译成方程、函数或不等式，再用数学说话。", "综合与实践",
          [(1, "方程不等式类应用题", "equation-applications"),
           (2, "函数类应用题", "function-applications"),
           (3, "尺规作图", "ruler-compass"),
           (4, "数学文化与学科融合", "math-culture"),
           (5, "统计与概率", "statistics-probability"),
           (6, "综合实践与数学应用", "practice"),
           (7, "找规律与新定义", "patterns")]),
     ]),
    ("m3", "第三部分 · 满分突破", "满分",
     "25 个压轴微专题：图形变换、最值与定值、隐形圆、存在性、双曲线与抛物线综合、新定义。目标不是多做题，而是看到条件就能判断该调用哪一套构图。",
     [
         ("01", "图形变换", "折叠与旋转压轴：先找不变量，再定轨迹。", "图形与几何",
          [(1, "平移与折叠", "translation-folding"),
           (2, "旋转与瓜豆原理", "rotation-gua-dou")]),
         ("02", "最值与定值", "七类最值构图的完整谱系。", "图形与几何",
          [(1, "单线段最值", "single-segment-extremum"),
           (2, "多线段和差最值", "broken-line-extremum"),
           (3, "胡不归与阿氏圆", "apollonius"),
           (4, "费马点", "fermat"),
           (5, "逆等线", "reverse-equal-line"),
           (6, "线段比与周长面积最值", "ratio-perimeter-area"),
           (7, "定值", "fixed-value")]),
         ("03", "三角函数与“12345”模型", "用三角函数把角度信息变成比例信息。", "图形与几何",
          [(1, "三角函数与“12345”模型", "trig-12345")]),
         ("04", "隐形圆", "没有圆却要作圆：三类隐形圆的识别。", "图形与几何",
          [(1, "四点共圆", "concyclic"),
           (2, "定义圆", "defined-circle"),
           (3, "定边定角及其他", "fixed-side-angle")]),
         ("05", "坐标系中的存在性", "设点、列方程、验范围：存在性问题的固定流程。", "数与代数",
          [(1, "多边形的存在性", "polygon-existence"),
           (2, "角度的存在性", "angle-existence")]),
         ("06", "双曲线综合", "反比例函数的二级结论与综合应用。", "数与代数",
          [(1, "双曲线二级结论", "hyperbola-lemmas"),
           (2, "双曲线综合", "hyperbola-comprehensive")]),
         ("07", "圆与多边形综合", "圆与四边形、相似、最值的交叉。", "图形与几何",
          [(1, "圆综合", "circle-comprehensive"),
           (2, "多边形综合", "polygon-comprehensive")]),
         ("08", "抛物线综合", "图象分析、参数讨论、几何综合。", "数与代数",
          [(1, "抛物线图象分析", "parabola-analysis"),
           (2, "抛物线综合", "parabola-comprehensive")]),
         ("09", "中考新题型", "网格作图、新定义、综合实践：读懂规则再动手。", "综合与实践",
          [(1, "网格中的尺规作图", "grid-construction"),
           (2, "新定义之几何与函数", "new-definition-geometry"),
           (3, "新定义之数论", "new-definition-number"),
           (4, "综合与实践", "comprehensive-practice")]),
     ]),
]


def main():
    modules, topics = [], []
    for no, (mid, title, short, desc, tdefs) in enumerate(PARTS, start=1):
        modules.append({"id": mid, "no": no, "title": title, "short": short,
                        "desc": desc, "strand": " / ".join(sorted({t[3] for t in tdefs}))})
        for tno, (suffix, ttitle, tdesc, domain, points) in enumerate(tdefs, start=1):
            tid = f"{mid}-{suffix}"
            pids = [f"{tid}-{seq:02d}-{slug}" for seq, _, slug in points]
            topics.append({"id": tid, "module": mid, "no": tno, "title": ttitle,
                           "desc": tdesc, "domain": domain, "points": pids})

    # 清单里保留全部 87 个 id，正文按时序补写；同时给标题索引供后续写作引用
    index = {}
    for t in topics:
        for pid in t["points"]:
            index[pid] = t["id"]

    (C / "modules.json").write_text(json.dumps(
        {"schema": 1,
         "note": "体系依据《中考冲刺专题突破·数学》(2024)：第一部分 31 讲、第二部分 31 微专题、第三部分 25 微专题。",
         "modules": modules, "topics": topics},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (C / "taxonomy.json").write_text(json.dumps(TAX, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8")
    (C / "site.json").write_text(json.dumps(SITE, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    (C / "standards.json").write_text(json.dumps(
        {"schema": 1, "items": []}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    n_pts = sum(len(t["points"]) for t in topics)
    print(f"模块 {len(modules)} / 主题 {len(topics)} / 知识点 {n_pts}")
    print(f"点位索引已生成：{len(index)} 条")


if __name__ == "__main__":
    main()
