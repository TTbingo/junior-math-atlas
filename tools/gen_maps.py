# -*- coding: utf-8 -*-
"""从 content/modules.json 生成三张领域知识脉络图（content/media/map-*.svg）。

好处：体系扩容 / 调整后重跑一次，脉络图自动与清单一致，不再手工改 SVG。
布局：代数 3 框一行；几何 7 框两行（4 + 3）；统计与概率 2 框一行 + 中间「频率估计」桥接。
同排框统一高度，描述允许三行，超出截断加「…」。
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "content"
MOD = json.loads((C / "modules.json").read_text(encoding="utf-8"))

FONT = "PingFang SC, Microsoft YaHei, Noto Sans SC, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


NO_HEAD = "。，、；：？！）」』”’%"


def wrap(text, max_chars):
    """按显示宽度断行：全角计 1、半角计 0.5；标点不另起一行，末行不留孤字。"""
    lines, buf, w = [], [], 0.0
    for ch in text:
        cw = 1.0 if ord(ch) > 0x2E80 else 0.5
        if w + cw > max_chars and buf and ch not in NO_HEAD:
            lines.append("".join(buf))
            buf, w = [], 0.0
        buf.append(ch)
        w += cw
    if buf:
        lines.append("".join(buf))
    # 末行只剩一两个字时并回上一行
    if len(lines) > 1 and len(lines[-1]) <= 2:
        lines[-2] += lines[-1]
        lines.pop()
    return lines


def short_label(title):
    """脉络图里去掉括注，避免过长。"""
    for l, r in [("（", "）"), ("(", ")")]:
        while l in title:
            a = title.find(l)
            b = title.find(r, a)
            if b == -1:
                break
            title = title[:a] + title[b + 1:]
    return title


def box_body(x, y, w, topic, color, title_size=15, desc_size=10.5, item_size=12.5,
             max_chars=None, desc_max_lines=3):
    """生成主题框内容（不含矩形），返回 (svg, 需要的高度)。"""
    if max_chars is None:
        max_chars = int((w - 24) / item_size)
    out = []
    out.append(f'<text x="{x + 11}" y="{y + 26}" font-size="{title_size}" '
               f'font-weight="600" fill="{color}" font-family="{FONT}">{esc(topic["title"])}</text>')
    # 占比抽出来放标题右侧，避免挤在正文里断行
    desc = topic["desc"]
    m = re.search(r"（约\s*([^）]+)）\s*$", desc)
    if m:
        desc = desc[:m.start()].rstrip("。") + "。"
        out.append(f'<text x="{x + w - 11}" y="{y + 26}" font-size="11" fill="{color}" '
                   f'fill-opacity="0.7" text-anchor="end" font-family="{FONT}">'
                   f'{esc(m.group(1))}</text>')
    desc_lines = wrap(desc, int((w - 22) / desc_size))
    if len(desc_lines) > desc_max_lines:
        desc_lines = desc_lines[:desc_max_lines]
        desc_lines[-1] = desc_lines[-1][:-1] + "…"
    yy = y + 44
    for ln in desc_lines:
        out.append(f'<text x="{x + 11}" y="{yy}" font-size="{desc_size}" fill="#718096" '
                   f'font-family="{FONT}">{esc(ln)}</text>')
        yy += desc_size + 6
    out.append(f'<line x1="{x + 10}" y1="{yy - 5}" x2="{x + w - 10}" y2="{yy - 5}" '
               f'stroke="{color}" stroke-opacity="0.25" stroke-width="1"/>')
    yy += 10
    for pid in topic["points"]:
        label = short_label(MOD["point_titles"][pid])
        for ln in wrap(label, max_chars):
            out.append(f'<text x="{x + 12}" y="{yy}" font-size="{item_size}" fill="#2d3748" '
                       f'font-family="{FONT}">{esc(ln)}</text>')
            yy += item_size + 6.5
    return "".join(out), yy - y + 4


def rect(x, y, w, h, color):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" rx="10" fill="#ffffff" '
            f'stroke="{color}" stroke-width="1.6"/>')


def arrow_h(x1, y, x2, color):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" stroke="{color}" '
            f'stroke-width="2" marker-end="url(#ah-{color[1:]})"/>')


def make_svg(width, height, extra_defs, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" font-family="{FONT}">\n'
            f'<defs>{extra_defs}</defs>\n'
            f'<rect width="{width}" height="{height}" fill="#ffffff"/>\n'
            f'{body}\n</svg>\n')


def arrow_def(color):
    return (f'<marker id="ah-{color[1:]}" viewBox="0 0 10 10" refX="8" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>')


def topics_of(module_id):
    return [t for t in MOD["topics"] if t["module"] == module_id]


def footer(x, y, main_line, source_line):
    return (f'<text x="{x}" y="{y}" font-size="12" fill="#4a5568" font-family="{FONT}">'
            f'{esc(main_line)}</text>'
            f'<text x="{x}" y="{y + 18}" font-size="11" fill="#a0aec0" font-family="{FONT}">'
            f'{esc(source_line)}</text>')


SRC = "脉络依据《初中数学思维导图》整理；括注为近 5 年中考分值占比"


def gen_algebra():
    color = "#2b6cb0"
    ts = topics_of("m1")
    W, gap, margin, y = 760, 26, 18, 22
    bw = (W - margin * 2 - gap * 2) / 3
    bodies, hs = [], []
    for i, t in enumerate(ts):
        b, h = box_body(margin + i * (bw + gap), y, bw, t, color)
        bodies.append(b)
        hs.append(h)
    H = max(hs)
    cy = y + H / 2
    arrows = "".join(arrow_h(margin + bw + i * (bw + gap) - 2, cy,
                             margin + (i + 1) * (bw + gap) + 4, color) for i in range(2))
    rects = "".join(rect(margin + i * (bw + gap), y, bw, H, color) for i in range(3))
    foot_y = y + H + 34
    body = rects + arrows + "".join(bodies) + footer(
        margin, foot_y,
        "主线：数的运算 → 式的运算 → 方程与不等式 → 函数。前一框是后一框的工具箱，顺序不能倒。", SRC)
    Ht = foot_y + 30
    (C / "media/map-algebra.svg").write_text(
        make_svg(W, Ht, arrow_def(color), body), encoding="utf-8")
    return Ht


def gen_geometry():
    color = "#2f855a"
    ts = topics_of("m2")
    W, gap, margin = 760, 22, 16
    row1, row2 = ts[:4], ts[4:]
    bw = (W - margin * 2 - gap * 3) / 4
    y1 = 22
    b1, h1s = [], []
    for i, t in enumerate(row1):
        b, h = box_body(margin + i * (bw + gap), y1, bw, t, color, title_size=14,
                        desc_size=10, item_size=11.5)
        b1.append(b); h1s.append(h)
    h1 = max(h1s)
    cy1 = y1 + h1 / 2
    arrows = [rect(margin + i * (bw + gap), y1, bw, h1, color) for i in range(4)]
    arrows += [arrow_h(margin + bw + i * (bw + gap) - 2, cy1,
                       margin + (i + 1) * (bw + gap) + 6, color) for i in range(3)]

    y2 = y1 + h1 + 58
    b2, h2s = [], []
    for i, t in enumerate(row2):
        b, h = box_body(margin + i * (bw + gap), y2, bw, t, color, title_size=14,
                        desc_size=10, item_size=11.5)
        b2.append(b); h2s.append(h)
    h2 = max(h2s)
    cy2 = y2 + h2 / 2
    arrows += [rect(margin + i * (bw + gap), y2, bw, h2, color) for i in range(3)]
    arrows += [arrow_h(margin + bw + i * (bw + gap) - 2, cy2,
                       margin + (i + 1) * (bw + gap) + 6, color) for i in range(2)]
    # 行间连接：第一行末框底部 → 第二行首框顶部
    x_from = margin + 3 * (bw + gap) + bw / 2
    x_to = margin + bw / 2
    mid = y1 + h1 + 26
    arrows.append(
        f'<path d="M {x_from} {y1 + h1} L {x_from} {mid} L {x_to} {mid} L {x_to} {y2 - 9}" '
        f'fill="none" stroke="{color}" stroke-width="2" marker-end="url(#ah-{color[1:]})"/>')
    foot_y = y2 + h2 + 32
    body = "".join(arrows) + "".join(b1) + "".join(b2) + footer(
        margin, foot_y,
        "主线：先认清线与角，再进三角形做推理，四边形和圆都靠三角形处理，最后用相似、变换、三角函数解决测量与证明。",
        SRC)
    Ht = foot_y + 30
    (C / "media/map-geometry.svg").write_text(
        make_svg(W, Ht, arrow_def(color), body), encoding="utf-8")
    return Ht


def gen_statistics():
    c1, c2 = "#b7791f", "#6b46c1"
    ts = topics_of("m3")
    W, gap, margin, y = 760, 110, 18, 22
    bw = (W - margin * 2 - gap) / 2
    b1, h1 = box_body(margin, y, bw, ts[0], c1)
    b2, h2 = box_body(margin + bw + gap, y, bw, ts[1], c2)
    H = max(h1, h2)
    cy = y + H / 2
    mid_x = margin + bw + gap / 2
    bridge = (
        f'<line x1="{margin + bw + 3}" y1="{cy}" x2="{mid_x - 10}" y2="{cy}" stroke="#718096" '
        f'stroke-width="2" marker-end="url(#ah-718096)"/>'
        f'<text x="{mid_x}" y="{cy - 12}" font-size="12" fill="#4a5568" text-anchor="middle" '
        f'font-family="{FONT}">频率</text>'
        f'<text x="{mid_x}" y="{cy + 14}" font-size="12" fill="#4a5568" text-anchor="middle" '
        f'font-family="{FONT}">估计</text>'
        f'<text x="{mid_x}" y="{cy + 32}" font-size="10" fill="#a0aec0" text-anchor="middle" '
        f'font-family="{FONT}">概率</text>')
    foot_y = y + H + 32
    # 先画矩形底、再画文字，否则白底会盖住内容
    body = (rect(margin, y, bw, H, c1) + rect(margin + bw + gap, y, bw, H, c2)
            + b1 + b2 + bridge + footer(
        margin, foot_y,
        "主线：数据 → 图表 → 统计量 → 判断；事件 → 等可能结果 → 概率。两条线在「用频率估计概率」处接上。", SRC))
    Ht = foot_y + 30
    defs = (arrow_def("#718096") +
            f'<marker id="ah-{c2[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{c2}"/></marker>')
    (C / "media/map-statistics.svg").write_text(
        make_svg(W, Ht, defs, body), encoding="utf-8")
    return Ht


if __name__ == "__main__":
    print("map-algebra:", gen_algebra())
    print("map-geometry:", gen_geometry())
    print("map-statistics:", gen_statistics())
