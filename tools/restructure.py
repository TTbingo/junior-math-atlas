# -*- coding: utf-8 -*-
"""把站点体系重构为「三大领域 → 主题 → 知识点」。

体系依据：资料库《初中数学思维导图》(11 章 / 34 张图) 的考点框架，
重组为代数 / 几何 / 统计与概率三大领域，共 12 主题 / 62 知识点。
各主题括号内的占比为思维导图标注的「近 5 年中考分值占比」，仅作复习优先级参考。
《初中数学冲刺专题突破》与几何模型 / 最值模型等资料只作为内容与例题的来源参照，
不决定目录结构。

运行：python tools/restructure.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "content"

MODULES = [
    {
        "id": "m1", "no": 1, "title": "代数", "short": "代数",
        "strand": "数与代数",
        "desc": "用符号表示关系，用运算求解关系：实数 → 式子 → 方程 → 函数。（中考约 43.2% 分值）",
        "map": "map-algebra.svg",
    },
    {
        "id": "m2", "no": 2, "title": "几何", "short": "几何",
        "strand": "图形与几何",
        "desc": "从直观确认到演绎推理：线与角 → 三角形 → 四边形 → 圆 → 相似与变换。（中考约 45.5% 分值）",
        "map": "map-geometry.svg",
    },
    {
        "id": "m3", "no": 3, "title": "统计与概率", "short": "统计概率",
        "strand": "统计与概率",
        "desc": "用数据说话，用可能性判断：收数据 → 画图 → 算统计量 → 估概率。（中考约 11.3% 分值）",
        "map": "map-statistics.svg",
    },
]

TOPICS = [
    ("m1", "数与式", "实数是根，整式与因式分解是运算的两面，分式与二次根式把除法和开方也纳入同一套运算法则。（约 15.4%）", [
        ("real-numbers", "实数及其运算"),
        ("integral-expressions", "整式的运算"),
        ("factorization", "因式分解"),
        ("algebraic-fractions", "分式"),
        ("quadratic-radicals", "二次根式"),
    ]),
    ("m1", "方程与不等式", "方程是「已知关系求未知量」的工具，不等式把等号换成不等号，解法母体完全一致。（约 9.4%）", [
        ("linear-equation", "一元一次方程"),
        ("linear-system", "二元一次方程组"),
        ("quadratic-equation", "一元二次方程"),
        ("discriminant-vieta", "根的判别式与根与系数的关系"),
        ("fractional-equation", "分式方程"),
        ("inequality", "一元一次不等式（组）"),
        ("equation-word-problems", "列方程（组）解应用题"),
        ("inequality-applications", "不等式（组）的应用与方案决策"),
    ]),
    ("m1", "函数", "函数是研究变化的语言：一次函数匀速、反比例函数成反比、二次函数先减后增。（约 18.4%）", [
        ("coordinates-and-function", "平面直角坐标系与函数"),
        ("linear-function", "一次函数的图象与性质"),
        ("linear-function-applications", "一次函数与方程、不等式及方案选择"),
        ("inverse-proportion", "反比例函数与 k 的几何意义"),
        ("quadratic-function", "二次函数的图象与性质"),
        ("quadratic-function-equation", "二次函数与一元二次方程"),
        ("quadratic-function-applications", "二次函数的综合应用（最值·面积·动点）"),
    ]),
    ("m2", "图形的初步认识", "点、线、角是几何的字母表，平行线的性质是把角搬来搬去的传送带。（约 4.7%）", [
        ("lines-rays-segments", "直线、射线、线段"),
        ("angles", "角与角平分线"),
        ("parallel-lines", "相交线与平行线"),
        ("propositions-proof", "命题、定理与证明"),
        ("constructions", "尺规作图"),
    ]),
    ("m2", "三角形", "三角形是最简单的封闭图形，也是全部几何推理的主战场。（约 3.8%）", [
        ("triangle-basics", "三角形的基本性质"),
        ("congruent-triangles", "全等三角形"),
        ("congruent-models", "全等三角形的基本模型"),
        ("isosceles-triangle", "等腰三角形与等边三角形"),
        ("pythagoras", "直角三角形与勾股定理"),
        ("triangle-midline", "三角形的中位线"),
    ]),
    ("m2", "四边形", "四边形靠对角线拆成三角形来处理，特殊四边形是加了限制条件的平行四边形。（约 4.5%）", [
        ("polygon", "多边形与内角和"),
        ("parallelogram", "平行四边形"),
        ("special-parallelogram", "矩形、菱形、正方形"),
        ("trapezoid", "梯形与中点四边形"),
    ]),
    ("m2", "圆", "圆的性质几乎都藏在半径、弦、圆心角这三样东西的组合里，切线是它与外界联系的通道。（约 11.9%）", [
        ("circle-properties", "圆的概念与垂径定理"),
        ("central-inscribed-angles", "圆心角、弧与圆周角定理"),
        ("circle-position", "点、直线与圆的位置关系"),
        ("tangent-lines", "切线的判定与切线长定理"),
        ("arc-sector-cone", "弧长、扇形面积与圆锥"),
        ("regular-polygon", "正多边形与圆"),
    ]),
    ("m2", "相似与投影", "相似是「形状不变、大小可变」，投影是三视图背后的光线模型。（约 5.6% + 1.8%）", [
        ("proportional-segments", "平行线分线段成比例"),
        ("similar-triangles", "相似三角形的判定与性质"),
        ("similar-models", "相似三角形的基本模型"),
        ("homothety", "位似"),
        ("projection-views", "投影与视图"),
    ]),
    ("m2", "图形与变换", "平移、旋转、轴对称都是全等变换，变换把分散的条件搬到一起，折叠与最值是它的高阶战场。（约 10.2%）", [
        ("symmetry", "轴对称与中心对称"),
        ("translation-rotation", "平移与旋转"),
        ("transform-coordinates", "变换与坐标（含折叠问题）"),
        ("geometric-extremum", "动点与最值问题（将军饮马·隐圆）"),
    ]),
    ("m2", "锐角三角函数", "三角函数把直角三角形的边与角连成比例关系，是测量问题的通用工具。（约 3%）", [
        ("trig-ratios", "锐角三角函数与特殊角"),
        ("solving-right-triangle", "解直角三角形"),
        ("trig-applications", "解直角三角形的实际应用"),
    ]),
    ("m3", "统计", "先收数据、再画图、最后用统计量概括，用样本估计总体后才能下结论。（约 6%）", [
        ("data-collection", "数据的收集与整理"),
        ("statistical-charts", "统计图表（含频数分布直方图）"),
        ("central-tendency", "平均数、中位数、众数"),
        ("variance", "方差与数据波动"),
        ("sample-estimation", "用样本估计总体"),
    ]),
    ("m3", "概率", "概率是可能性的度量：先分清事件类型，再用列举或频率把它算出来。（约 5.3%）", [
        ("event-probability", "事件的分类与概率"),
        ("probability-methods", "求概率的方法"),
        ("frequency-estimate", "用频率估计概率"),
    ]),
]


def main():
    topics, titles = [], {}
    counters = {}
    for module_id, title, desc, points in TOPICS:
        counters[module_id] = counters.get(module_id, 0) + 1
        tid = f"{module_id}-{counters[module_id]:02d}"
        pids = []
        for i, (slug, ptitle) in enumerate(points, 1):
            pid = f"{tid}-{i:02d}-{slug}"
            pids.append(pid)
            titles[pid] = ptitle
        topics.append({"id": tid, "module": module_id, "no": counters[module_id],
                       "title": title, "desc": desc, "points": pids})

    mod = {
        "schema": 1,
        "note": "体系依据《初中数学思维导图》考点框架，重组为代数 / 几何 / 统计与概率三大领域；"
                "《中考冲刺专题突破》与几何模型 / 最值模型资料作为内容与例题的来源参照。",
        "modules": MODULES,
        "topics": topics,
        "point_titles": titles,
    }
    (C / "modules.json").write_text(
        json.dumps(mod, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site = {
        "schema": 1,
        "title": "初中数学知识图谱",
        "subtitle": "按代数、几何、统计与概率三大领域梳理：先讲清原理，再给可复用的解题思路",
        "nav": [{"label": "全部知识点", "href": "index.html"}],
        "default_theme": "auto",
        "source_note": "知识脉络依据《初中数学思维导图》；内容与题型参照《中考冲刺专题突破·数学》(2024)"
                       "与几何模型、最值模型等资料。原理与解题思路按初中课标重写，例题均为自编并逐题验算。",
    }
    (C / "site.json").write_text(
        json.dumps(site, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    tax = json.loads((C / "taxonomy.json").read_text(encoding="utf-8-sig"))
    tax["site_title"] = "初中数学知识图谱"
    (C / "taxonomy.json").write_text(
        json.dumps(tax, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    n_points = len(titles)
    print(f"模块 {len(MODULES)} / 主题 {len(topics)} / 知识点 {n_points}")
    for t in topics:
        print(f"  {t['id']} {t['title']}  {len(t['points'])} 篇")


if __name__ == "__main__":
    main()
