# -*- coding: utf-8 -*-
"""把站点体系重构为「三大领域 → 主题 → 知识点」。

体系依据：资料库《初中数学思维导图》的十一章脉络，
重组为代数 / 几何 / 统计与概率三大领域，共 12 主题 / 45 知识点。
《初中数学冲刺专题突破》只作为内容与例题的来源参照，不再决定目录结构。

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
        "desc": "从实数与式子的运算出发，用方程和不等式刻画相等与不等，再用函数描述变化。"
                "主线是「用符号表示关系，用运算求解关系」。",
        "map": "map-algebra.svg",
    },
    {
        "id": "m2", "no": 2, "title": "几何", "short": "几何",
        "strand": "图形与几何",
        "desc": "从直线、角、平行线起步，经过三角形、四边形、圆，走到相似、变换与三角函数。"
                "主线是「从直观确认到演绎推理」。",
        "map": "map-geometry.svg",
    },
    {
        "id": "m3", "no": 3, "title": "统计与概率", "short": "统计概率",
        "strand": "统计与概率",
        "desc": "先学会把数据收齐、画清、算准，再用频率估计概率、用列举法算概率。"
                "主线是「用数据说话，用可能性做判断」。",
        "map": "map-statistics.svg",
    },
]

TOPICS = [
    ("m1", "数与式", "实数是根，整式与分式是运算语言，二次根式把开方也纳入同一套运算法则。", [
        ("real-numbers", "实数及其运算"),
        ("integral-expressions", "整式与因式分解"),
        ("algebraic-fractions", "分式"),
        ("quadratic-radicals", "二次根式"),
    ]),
    ("m1", "方程与不等式", "方程是「已知关系求未知量」的工具，不等式把等号换成不等号，解法母体完全一致。", [
        ("linear-equation", "一元一次方程"),
        ("linear-system", "二元一次方程组"),
        ("quadratic-equation", "一元二次方程"),
        ("discriminant-vieta", "根的判别式与根与系数的关系"),
        ("fractional-equation", "分式方程"),
        ("inequality", "一元一次不等式（组）"),
        ("equation-word-problems", "列方程解应用题"),
    ]),
    ("m1", "函数", "函数是研究变化的语言：一次函数匀速、反比例函数成反比、二次函数先减后增。", [
        ("coordinates-and-function", "平面直角坐标系与函数"),
        ("linear-function", "一次函数"),
        ("inverse-proportion", "反比例函数"),
        ("quadratic-function", "二次函数"),
    ]),
    ("m2", "图形的初步认识", "点、线、角是几何的字母表，平行线的性质是把角搬来搬去的传送带。", [
        ("lines-rays-segments", "直线、射线、线段"),
        ("angles", "角与角平分线"),
        ("parallel-lines", "相交线与平行线"),
    ]),
    ("m2", "三角形", "三角形是最简单的封闭图形，也是全部几何推理的主战场。", [
        ("triangle-basics", "三角形的基本性质"),
        ("congruent-triangles", "全等三角形"),
        ("isosceles-triangle", "等腰三角形与等边三角形"),
        ("pythagoras", "直角三角形与勾股定理"),
    ]),
    ("m2", "四边形", "四边形靠对角线拆成三角形来处理，特殊四边形是加了限制条件的平行四边形。", [
        ("polygon", "多边形与内角和"),
        ("parallelogram", "平行四边形"),
        ("special-parallelogram", "矩形、菱形、正方形"),
        ("trapezoid", "梯形与中位线"),
    ]),
    ("m2", "圆", "圆的性质几乎都藏在半径、弦、圆心角这三样东西的组合里。", [
        ("circle-properties", "圆的概念与性质"),
        ("circle-position", "与圆有关的位置关系"),
        ("arc-sector-cone", "弧长、扇形面积与圆锥"),
        ("regular-polygon", "正多边形与圆"),
    ]),
    ("m2", "相似与投影", "相似是「形状不变、大小可变」，投影是三视图背后的光线模型。", [
        ("similar-triangles", "相似三角形"),
        ("homothety", "位似"),
        ("projection-views", "投影与视图"),
    ]),
    ("m2", "图形与变换", "平移、旋转、轴对称都是全等变换，变换把分散的条件搬到一起。", [
        ("symmetry", "轴对称与中心对称"),
        ("translation-rotation", "平移与旋转"),
        ("transform-coordinates", "变换与坐标"),
    ]),
    ("m2", "锐角三角函数", "三角函数把直角三角形的边与角连成比例关系，是测量问题的通用工具。", [
        ("trig-ratios", "锐角三角函数"),
        ("solving-right-triangle", "解直角三角形"),
    ]),
    ("m3", "统计", "先收数据、再画图、最后用统计量概括，三步走完一次数据分析。", [
        ("data-collection", "数据的收集与整理"),
        ("statistical-charts", "统计图表"),
        ("central-tendency", "平均数、中位数、众数"),
        ("variance", "方差与数据波动"),
    ]),
    ("m3", "概率", "概率是可能性的度量：先分清事件类型，再用列举或频率把它算出来。", [
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
        "note": "体系依据《初中数学思维导图》十一章脉络，重组为代数 / 几何 / 统计与概率三大领域；"
                "《中考冲刺专题突破》作为内容与例题的来源参照。",
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
        "source_note": "知识脉络依据《初中数学思维导图》；内容与题型参照《中考冲刺专题突破·数学》(2024)。"
                       "原理与解题思路按初中课标重写，例题均为自编并逐题验算。",
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
