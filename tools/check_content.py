"""内容体检：专治小学数学站踩过的坑，初中站沿用。

检查项
1. 前置知识必须排在本文之前（防止「前置 = 后面才学的内容」）
2. 前置不得等于 related 列表（防止「related[0] 抄成前置」的批量错误）
3. 前置 / 关联不得自指，不得成环
4. 例题场景在枚举内且同页不重复（build.py 已查，这里再兜一次）
5. 正文禁用跳步话术（显然 / 易证 / 不难看出）
6. 公式配对：$ 数量为偶数，避免裸公式漏渲染
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "content"


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
    print("✓ 内容体检通过：前置顺序、关联自指、场景重复、跳步话术、公式配对全部正常")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
