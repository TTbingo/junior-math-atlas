"""内容体检：专治小学数学站踩过的坑，初中站沿用。

检查项
1. 前置知识必须排在本文之前（防止「前置 = 后面才学的内容」）
2. 前置不得等于 related 列表（防止「related[0] 抄成前置」的批量错误）
3. 前置 / 关联不得自指，不得成环
4. 例题场景在枚举内且同页不重复（build.py 已查，这里再兜一次）
5. 正文禁用跳步话术（显然 / 易证 / 不难看出）
6. 公式配对：$ 数量为偶数，避免裸公式漏渲染
7. 概念超前引用：正文不得使用排在后面的点位才引入的概念词
   （2026-11-04 教训：二元一次方程组用「方程是一条直线」作主要解释，
     而坐标系与一次函数分别排在 m1-03-01 / m1-03-02，学生当时还没学。
     prerequisites 顺序对了不等于正文没超前引用。）
   允许「提前借用」，但同一段必须写明是借用，否则报错。
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "content"

# 概念词 → 首次引入它的点位。正文在引入点之前出现该词，视为超前引用。
CONCEPT_INTRO = {
    "平面直角坐标系": "m1-03-01-coordinates-and-function",
    "坐标平面": "m1-03-01-coordinates-and-function",
    "一次函数": "m1-03-02-linear-function",
    "反比例函数": "m1-03-04-inverse-proportion",
    "双曲线": "m1-03-04-inverse-proportion",
    "二次函数": "m1-03-05-quadratic-function",
    "抛物线": "m1-03-05-quadratic-function",
    "判别式": "m1-02-04-discriminant-vieta",
    # —— 几何术语（登记前已核实 m1 全部未占用；小学已学、m1 已用的通用词
    #    （三角形/矩形/正方形/平行/四边形/垂线/轴对称/旋转/平移）不登记，避免误报）——
    "对顶角": "m2-01-03-parallel-lines",
    "邻补角": "m2-01-03-parallel-lines",
    "同位角": "m2-01-03-parallel-lines",
    "内错角": "m2-01-03-parallel-lines",
    "同旁内角": "m2-01-03-parallel-lines",
    "点到直线的距离": "m2-01-03-parallel-lines",
    "命题": "m2-01-04-propositions-proof",
    "垂直平分线": "m2-01-05-constructions",
    "全等": "m2-02-02-congruent-triangles",
    "等腰三角形": "m2-02-04-isosceles-triangle",
    "等边三角形": "m2-02-04-isosceles-triangle",
    "勾股": "m2-02-05-pythagoras",
    "中位线": "m2-02-06-triangle-midline",
    "菱形": "m2-03-03-special-parallelogram",
    "垂径定理": "m2-04-01-circle-properties",
    "圆心角": "m2-04-02-central-inscribed-angles",
    "圆周角": "m2-04-02-central-inscribed-angles",
    "切线": "m2-04-04-tangent-lines",
    "弧长": "m2-04-05-arc-sector-cone",
    "扇形": "m2-04-05-arc-sector-cone",
    "圆锥": "m2-04-05-arc-sector-cone",
    # 2026-11-04 二批调整：正多边形（各边相等、各角相等）在多边形篇 m2-03-01 正式引入，
    # m2-04-06 只展开它与圆的关系——登记随引入点前移。
    "正多边形": "m2-03-01-polygon",
    "相似": "m2-05-02-similar-triangles",
    "位似": "m2-05-04-homothety",
    "投影": "m2-05-05-projection-views",
    "三视图": "m2-05-05-projection-views",
    "三角函数": "m2-07-01-trig-ratios",
    "正弦": "m2-07-01-trig-ratios",
    "余弦": "m2-07-01-trig-ratios",
    "正切": "m2-07-01-trig-ratios",
}
# 注：「对称轴」不列入。x 轴、y 轴本身就是对称轴，属几何基础用语，不是抛物线的专属概念。

# 同段出现这些词，说明作者已声明是提前借用，放行
BORROW_MARKERS = ("提前借用", "后续学习", "等学了", "等学到", "以后会学", "后面会学",
                  "后面才学", "再回看", "下一篇")

# related 本就是跨篇导航，不参与超前检查
SKIP_SECTIONS = ("related",)


def _paras(v):
    """把一个板块摊平成若干段落字符串。"""
    if isinstance(v, str):
        return [v]
    if isinstance(v, list):
        out = []
        for x in v:
            out.extend(_paras(x))
        return out
    if isinstance(v, dict):
        out = []
        for x in v.values():
            out.extend(_paras(x))
        return out
    return []


def main():
    mod = json.loads((C / "modules.json").read_text(encoding="utf-8"))
    tax = json.loads((C / "taxonomy.json").read_text(encoding="utf-8"))
    plan = [p for t in mod["topics"] for p in t["points"]]
    order = {pid: i for i, pid in enumerate(plan)}
    points = {}
    for f in sorted((C / "points").glob("*.json")):
        points[f.stem] = json.loads(f.read_text(encoding="utf-8"))

    bad = []
    for pid, p in points.items():
        secs = p.get("sections", {})
        rel_ids = [r["id"] for r in secs.get("related", [])]
        pre = p.get("prerequisites", [])

        for x in pre:
            if x == pid:
                bad.append(f"{pid}: 前置指向自己")
            elif x in order and order[x] > order[pid]:
                bad.append(f"{pid}: 前置 {x} 排在本文之后（应先学）")
            if x in rel_ids:
                bad.append(f"{pid}: 前置 {x} 同时出现在 related，疑似 related[0] 顶替前置")

        for r in rel_ids:
            if r == pid:
                bad.append(f"{pid}: related 指向自己")
            if r not in order:
                bad.append(f"{pid}: related {r} 不在清单")

        scenes = [e.get("scene") for e in secs.get("examples", [])]
        if len(scenes) != len(set(scenes)):
            bad.append(f"{pid}: 例题场景重复 {scenes}")

        blob = json.dumps(secs, ensure_ascii=False)
        for w in tax["forbidden_words"]:
            if w in blob:
                bad.append(f"{pid}: 命中跳步话术「{w}」")
        for k, v in secs.items():
            text = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
            if text.count("$") % 2:
                bad.append(f"{pid}.{k}: $ 不成对（{text.count('$')} 个）")

        # 概念超前引用
        for k, v in secs.items():
            if k in SKIP_SECTIONS:
                continue
            for para in _paras(v):
                hit = [w for w in CONCEPT_INTRO if w in para]
                if not hit:
                    continue
                if any(m in para for m in BORROW_MARKERS):
                    continue
                for w in hit:
                    intro = CONCEPT_INTRO[w]
                    if intro not in order:
                        continue
                    if order[pid] < order[intro]:
                        bad.append(
                            f"{pid}.{k}: 超前引用「{w}」（该概念在 {intro} 才引入，本篇排在它之前）"
                        )

    # 环检测：prerequisites 图上是否有环
    state = {}

    def dfs(u, path):
        state[u] = 1
        for v in points.get(u, {}).get("prerequisites", []):
            if v not in points:
                continue
            if state.get(v) == 1:
                bad.append(f"前置成环：{' → '.join(path + [u, v])}")
            elif state.get(v) is None:
                dfs(v, path + [u])
        state[u] = 2

    for pid in points:
        if state.get(pid) is None:
            dfs(pid, [])

    print(f"检查 {len(points)} 篇（清单共 {len(plan)} 个点位，待写 {len(plan) - len(points)}）")
    if bad:
        print(f"✗ {len(bad)} 条问题")
        for b in bad:
            print("  ✗", b)
        return 1
    print("✓ 内容体检通过：前置顺序、关联自指、场景重复、跳步话术、公式配对、概念超前全部正常")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
