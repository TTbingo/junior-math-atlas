# -*- coding: utf-8 -*-
"""几何第一批（m2-01 五篇 + m2-02 收尾四篇）配图生成器。

纪律（CLAUDE.md）：
- SVG 是 XML：所有文本经 esc() 转义，禁止裸 < > &
- width/height 与 viewBox 严格一致
- 图内文字与正文数字严格一致（alt / caption / SVG 内三方对齐）
"""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "content" / "media"

DARK = "#1f2937"
GREY = "#6b7280"
GREYM = "#9ca3af"
BLUE = "#2563eb"
BLUEF = "#dbeafe"
GRN = "#16a34a"
GRNF = "#dcfce7"
RED = "#dc2626"
REDF = "#fee2e2"
YEL = "#b45309"
YELF = "#fef3c7"
PURP = "#7c3aed"
PURPF = "#ede9fe"


def esc(s):
    return (str(s).replace("&", "&amp;")
            .replace("<", "&lt;").replace(">", "&gt;"))


class Fig:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.buf = []

    def line(self, x1, y1, x2, y2, color=DARK, width=2.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.buf.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>')

    def poly(self, pts, fill="none", stroke=DARK, width=2.0, dash=None):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.buf.append(
            f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{width}" stroke-linejoin="round"{d}/>')

    def circle(self, x, y, r, fill="none", stroke=DARK, width=1.5):
        self.buf.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{width}"/>')

    def dot(self, x, y, color=DARK, r=3.5):
        self.buf.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" '
            f'stroke="{color}" stroke-width="1"/>')

    def rect(self, x, y, w, h, fill="none", stroke=DARK, width=1.6):
        """以左上角为起点画矩形。"""
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
                  fill, stroke, width)

    def text(self, x, y, s, size=12, color=DARK, anchor="start", weight=None):
        w = f' font-weight="{weight}"' if weight else ""
        self.buf.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-family="Noto Sans SC, PingFang SC, '
            f'Microsoft YaHei, sans-serif"{w}>{esc(s)}</text>')

    def arc(self, cx, cy, r, a1, a2, color=DARK, width=1.6, dash=None,
            span_pass=None):
        """以 (cx,cy) 为圆心、半径 r 的圆弧，从屏幕角 a1 画到 a2（度，0=东，90=南）。
        默认走劣弧（<180°）；span_pass='cw' 或 'ccw' 指定跨越方向（用于大角）。"""
        a1r, a2r = math.radians(a1), math.radians(a2)
        x1, y1 = cx + r * math.cos(a1r), cy + r * math.sin(a1r)
        x2, y2 = cx + r * math.cos(a2r), cy + r * math.sin(a2r)
        if span_pass is None:
            # 取两侧夹角中较小的一个：diff 落在 [-180,180)，符号决定绕行方向
            diff = ((a2 - a1 + 180) % 360) - 180
            sweep = 1 if diff >= 0 else 0
            large = 0
        else:
            sweep = 1 if span_pass == "cw" else 0
            large = 0
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.buf.append(
            f'<path d="M {x1:.1f} {y1:.1f} A {r} {r} 0 {large} {sweep} '
            f'{x2:.1f} {y2:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="{width}"{d}/>')

    def arrow_head(self, x, y, dx, dy, color=DARK, size=9):
        """在 (x,y) 处画箭头，指向 (dx,dy) 单位方向。"""
        ang = math.atan2(dy, dx)
        a1 = ang + math.radians(152)
        a2 = ang - math.radians(152)
        p1 = (x + size * math.cos(a1), y + size * math.sin(a1))
        p2 = (x + size * math.cos(a2), y + size * math.sin(a2))
        self.poly([(x, y), p1, p2], fill=color, stroke=color, width=1)

    def arrow_line(self, x1, y1, x2, y2, color=DARK, width=2.0, dash=None):
        self.line(x1, y1, x2, y2, color, width, dash)
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy)
        self.arrow_head(x2, y2, dx / n, dy / n, color)

    def right_angle(self, vx, vy, d1, d2, size=11, color=DARK):
        """在顶点 (vx,vy) 画直角符号，两边方向为屏幕角 d1、d2。"""
        p1 = (vx + size * math.cos(math.radians(d1)),
              vy + size * math.sin(math.radians(d1)))
        p2 = (vx + size * math.cos(math.radians(d2)),
              vy + size * math.sin(math.radians(d2)))
        pc = (p1[0] + p2[0] - vx, p1[1] + p2[1] - vy)
        self.poly([p1, pc, p2], fill="none", stroke=color, width=1.4)

    def tick(self, x1, y1, x2, y2, n=1, color=DARK, size=6):
        """线段中点的相等记号（垂直小短线，可重复 n 次）。"""
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        n_ = math.hypot(dx, dy)
        ux, uy = -dy / n_, dx / n_
        for i in range(n):
            off = (i - (n - 1) / 2) * 6
            cx, cy = mx + ux * 0, my + uy * 0
            sx, sy = cx + ux * 0 + dx / n_ * 0, cy
            a = (mx + ux * 0 + (i - (n - 1) / 2) * 5 * (dx / n_),
                 my + (i - (n - 1) / 2) * 5 * (dy / n_))
            self.line(a[0] - ux * size / 2, a[1] - uy * size / 2,
                      a[0] + ux * size / 2, a[1] + uy * size / 2, color, 1.8)

    def chevron(self, x, y, color=DARK, size=7):
        """平行线的 > 记号。"""
        self.buf.append(
            f'<path d="M {x:.1f} {y - size / 2:.1f} L {x + size:.1f} {y:.1f} '
            f'L {x:.1f} {y + size / 2:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="1.6"/>')

    def save(self, name):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" '
               f'height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
               f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>'
               + "".join(self.buf) + "</svg>")
        (OUT / name).write_text(svg, encoding="utf-8")
        print("saved", name)


def fig_lines():
    f = Fig(760, 300)
    rows = [
        ("直线", 70, "无端点，两方无限延伸", "记作直线 AB（两个大写字母）"),
        ("射线", 150, "一个端点，向一方无限延伸", "端点写在前：射线 OA"),
        ("线段", 230, "两个端点，可以度量长度", "记作线段 AB，AB = BA"),
    ]
    for name, y, desc, note in rows:
        f.text(56, y + 5, name, 14, DARK, weight="bold")
        if name == "直线":
            f.line(150, y, 340, y, DARK, 2.2)
            f.arrow_head(150, y, -1, 0, DARK)
            f.arrow_head(340, y, 1, 0, DARK)
            f.dot(200, y); f.dot(300, y)
            f.text(200, y + 22, "A", 13, DARK, anchor="middle")
            f.text(300, y + 22, "B", 13, DARK, anchor="middle")
        elif name == "射线":
            f.dot(170, y)
            f.line(170, y, 340, y, DARK, 2.2)
            f.arrow_head(340, y, 1, 0, DARK)
            f.dot(285, y)
            f.text(163, y + 22, "O", 13, DARK, anchor="middle")
            f.text(285, y - 12, "A", 13, DARK, anchor="middle")
        else:
            f.dot(170, y); f.dot(340, y)
            f.line(170, y, 340, y, DARK, 2.2)
            f.tick(170, y, 340, y, 1)
            f.text(163, y + 22, "A", 13, DARK, anchor="middle")
            f.text(347, y + 22, "B", 13, DARK, anchor="middle")
        f.text(392, y - 2, desc, 13, DARK)
        f.text(392, y + 20, note, 12, GREY)
    f.text(392, 66, "", 12, GREY)
    f.save("lines-basic.svg")


def fig_angle():
    f = Fig(760, 300)
    O = (230, 250)
    r = 185
    aA, aB, aC = 215, 285, 250
    A = (O[0] + r * math.cos(math.radians(aA)), O[1] + r * math.sin(math.radians(aA)))
    B = (O[0] + r * math.cos(math.radians(aB)), O[1] + r * math.sin(math.radians(aB)))
    C = (O[0] + r * math.cos(math.radians(aC)), O[1] + r * math.sin(math.radians(aC)))
    f.line(O[0], O[1], A[0], A[1], DARK, 2.2)
    f.line(O[0], O[1], B[0], B[1], DARK, 2.2)
    f.line(O[0], O[1], C[0], C[1], RED, 2.2)
    for p, name, off in [(O, "O", (-14, 16)), (A, "A", (-16, -6)),
                         (B, "B", (6, -8)), (C, "C", (0, -12))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.arc(O[0], O[1], 46, aA, aC, BLUE, 1.8)
    f.arc(O[0], O[1], 46, aC, aB, GRN, 1.8)
    for adeg, lab, col in [(232.5, "35°", BLUE), (267.5, "35°", GRN)]:
        lx = O[0] + 66 * math.cos(math.radians(adeg))
        ly = O[1] + 66 * math.sin(math.radians(adeg))
        f.text(lx, ly, lab, 12, col, anchor="middle")
    f.arc(O[0], O[1], 112, aA, aB, GREY, 1.2, dash="4 3")
    f.text(O[0] + 134 * math.cos(math.radians(240)),
           O[1] + 134 * math.sin(math.radians(240)),
           "70°", 12, GREY, anchor="middle")
    f.text(230, 286, "OC 平分 ∠AOB：∠AOC = ∠COB = 35°", 13, DARK, anchor="middle")
    # 右侧说明
    f.text(560, 120, "把 ∠AOB 沿 OC 对折，", 13, DARK, anchor="middle")
    f.text(560, 146, "OA 与 OB 完全重合。", 13, DARK, anchor="middle")
    f.text(560, 184, "折痕 OC 就是角平分线：", 12, GREY, anchor="middle")
    f.text(560, 208, "分出的两个角都等于原角的一半。", 12, GREY, anchor="middle")
    f.save("angle-bisector.svg")


def fig_parallel():
    f = Fig(760, 340)
    # 左：对顶角
    O = (180, 172)
    f.text(180, 36, "① 相交：对顶角", 14, DARK, anchor="middle", weight="bold")
    f.line(40, 82, 320, 262, DARK, 2.2)
    f.line(40, 262, 320, 82, DARK, 2.2)
    f.dot(*O)
    f.text(174, 190, "O", 12, DARK, anchor="end")
    d1 = math.degrees(math.atan2(82 - 262, 40 - 320))   # l2 上行方向
    f.arc(O[0], O[1], 34, 212.7, 327.3, RED, 1.8)
    f.text(O[0], O[1] - 54, "∠1", 12, RED, anchor="middle")
    f.arc(O[0], O[1], 34, 32.7, 147.3, RED, 1.8)
    f.text(O[0], O[1] + 56, "∠3", 12, RED, anchor="middle")
    f.arc(O[0], O[1], 24, 327.3, 32.7, BLUE, 1.8)
    f.text(O[0] + 44, O[1] + 4, "∠2", 12, BLUE, anchor="middle")
    f.arc(O[0], O[1], 24, 147.3, 212.7, BLUE, 1.8)
    f.text(O[0] - 44, O[1] + 4, "∠4", 12, BLUE, anchor="middle")
    f.text(180, 316, "对顶角相等：∠1 = ∠3，∠2 = ∠4", 13, DARK, anchor="middle")
    # 右：三线八角
    f.text(575, 36, "② 平行：三线八角", 14, DARK, anchor="middle", weight="bold")
    f.line(410, 105, 740, 105, DARK, 2.2)
    f.line(410, 235, 740, 235, DARK, 2.2)
    f.line(460, 50, 710, 290, GREY, 2.0)
    f.chevron(700, 105, PURP, 8)
    f.chevron(688, 105, PURP, 8)
    f.chevron(700, 235, PURP, 8)
    f.chevron(688, 235, PURP, 8)
    P = (517.3, 105)
    Q = (652.7, 235)
    f.dot(*P); f.dot(*Q)
    f.text(505, 92, "P", 12, DARK, anchor="middle")
    f.text(640, 224, "Q", 12, DARK, anchor="middle")
    # 同位角（红）：两条线的左上角
    f.arc(P[0], P[1], 26, 180, 223.8, RED, 1.8)
    f.text(P[0] - 44, P[1] - 24, "1", 12, RED, anchor="middle")
    f.arc(Q[0], Q[1], 26, 180, 223.8, RED, 1.8)
    f.text(Q[0] - 44, Q[1] - 24, "1", 12, RED, anchor="middle")
    # 内错角（绿）：P 南侧大角 / Q 北侧大角
    f.arc(P[0], P[1], 34, 50, 170, GRN, 1.8)
    f.text(P[0] - 10, P[1] + 50, "2", 12, GRN, anchor="middle")
    f.arc(Q[0], Q[1], 34, 230, 350, GRN, 1.8)
    f.text(Q[0] + 14, Q[1] - 52, "2", 12, GRN, anchor="middle")
    # 同旁内角（蓝）：P 右下小角 / Q 东侧小角
    f.arc(P[0], P[1], 16, 2, 40, BLUE, 1.8)
    f.text(P[0] + 30, P[1] + 14, "3", 12, BLUE, anchor="middle")
    f.arc(Q[0], Q[1], 16, 300, 356, BLUE, 1.8)
    f.text(Q[0] + 34, Q[1] - 26, "3", 12, BLUE, anchor="middle")
    f.text(575, 316, "a∥b：红=同位角，绿=内错角，蓝=同旁内角", 13, DARK, anchor="middle")
    f.save("parallel-angles.svg")


def fig_counterexample():
    f = Fig(760, 300)
    # 左：真命题
    f.text(180, 36, "真命题：对顶角相等", 14, DARK, anchor="middle", weight="bold")
    O = (180, 165)
    f.line(60, 75, 300, 255, DARK, 2.2)
    f.line(60, 255, 300, 75, DARK, 2.2)
    f.dot(*O)
    f.arc(O[0], O[1], 30, 212.7, 327.3, RED, 1.8)
    f.text(O[0], O[1] - 48, "∠1", 12, RED, anchor="middle")
    f.arc(O[0], O[1], 30, 32.7, 147.3, RED, 1.8)
    f.text(O[0], O[1] + 50, "∠3", 12, RED, anchor="middle")
    f.text(180, 292, "∠1 = ∠3（可由补角推导）", 12, DARK, anchor="middle")
    # 右：假命题的反例
    f.text(550, 36, "假命题：相等的角是对顶角", 14, DARK, anchor="middle", weight="bold")
    O2 = (540, 240)
    aA, aB, aC = 210, 270, 240
    r = 130
    A = (O2[0] + r * math.cos(math.radians(aA)), O2[1] + r * math.sin(math.radians(aA)))
    B = (O2[0] + r * math.cos(math.radians(aB)), O2[1] + r * math.sin(math.radians(aB)))
    C = (O2[0] + r * math.cos(math.radians(aC)), O2[1] + r * math.sin(math.radians(aC)))
    f.line(O2[0], O2[1], A[0], A[1], DARK, 2.2)
    f.line(O2[0], O2[1], B[0], B[1], DARK, 2.2)
    f.line(O2[0], O2[1], C[0], C[1], GRN, 2.2)
    for p, name, off in [(O2, "O", (12, 18)), (A, "A", (-12, 0)),
                         (B, "B", (10, -6)), (C, "C", (0, -10))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.arc(O2[0], O2[1], 34, aA, aC, GRN, 1.8)
    f.arc(O2[0], O2[1], 34, aC, aB, GRN, 1.8)
    for rr, adeg in ((58, 225), (76, 255)):
        lx = O2[0] + rr * math.cos(math.radians(adeg))
        ly = O2[1] + rr * math.sin(math.radians(adeg))
        f.text(lx, ly, "30°", 12, GRN, anchor="middle")
    f.text(560, 292, "反例：∠AOC = ∠BOC = 30°，但不是对顶角", 12, DARK, anchor="middle")
    f.save("counterexample.svg")


def fig_construction():
    f = Fig(760, 380)
    f.text(380, 28, "作线段 AB 的垂直平分线", 14, DARK, anchor="middle", weight="bold")
    A = (280, 200)
    B = (480, 200)
    r = 150
    C = (380, 200 - 111.8)
    D = (380, 200 + 111.8)
    # 作图弧（虚线）：圆心 A、B，半径 r
    f.arc(A[0], A[1], r, -48.2, -100, GREY, 1.4, dash="5 4")
    f.arc(B[0], B[1], r, -131.8, -80, GREY, 1.4, dash="5 4")
    f.arc(A[0], A[1], r, 48.2, 100, GREY, 1.4, dash="5 4")
    f.arc(B[0], B[1], r, 131.8, 80, GREY, 1.4, dash="5 4")
    # 线段与垂直平分线
    f.line(A[0], A[1], B[0], B[1], DARK, 2.2)
    f.line(C[0], C[1], D[0], D[1], RED, 2.2)
    for p, name, off in [(A, "A", (-12, 20)), (B, "B", (12, 20)),
                         (C, "C", (-16, -6)), (D, "D", (14, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    M = (380, 200)
    f.right_angle(M[0], M[1], 0, 90, 10, DARK)
    f.text(394, 186, "M（中点）", 12, DARK)
    # 左侧说明
    f.text(40, 150, "以 A、B 为圆心，", 12, DARK)
    f.text(40, 172, "等长半径（大于 AB 一半）", 12, DARK)
    f.text(40, 194, "画弧，两弧交于 C、D。", 12, DARK)
    f.text(40, 230, "CA=CB、DA=DB", 12, RED, weight="bold")
    f.text(40, 252, "（同一半径），", 12, GREY)
    f.text(40, 274, "CD 就是垂直平分线。", 12, DARK)
    f.save("perp-bisector-construction.svg")


def fig_models():
    f = Fig(760, 480)
    # ① 平移型
    f.text(128, 36, "① 平移型", 14, DARK, anchor="middle", weight="bold")
    t1 = [(30, 330), (150, 330), (90, 190)]
    t2 = [(125, 225), (245, 225), (185, 120)]
    for (a, b) in zip(t1, t2):
        f.line(a[0], a[1], b[0], b[1], GREYM, 1.4, dash="4 3")
    f.poly(t1, GRNF, GRN, 2.0)
    f.poly(t2, BLUEF, BLUE, 2.0)
    f.tick(t1[0][0], t1[0][1], t1[2][0], t1[2][1], 1, DARK)
    f.tick(t2[0][0], t2[0][1], t2[2][0], t2[2][1], 1, DARK)
    f.tick(t1[1][0], t1[1][1], t1[2][0], t1[2][1], 2, DARK)
    f.tick(t2[1][0], t2[1][1], t2[2][0], t2[2][1], 2, DARK)
    f.arrow_line(92, 306, 148, 244, GREY, 1.6)
    f.text(128, 430, "对应点连线", 12, GREY, anchor="middle")
    f.text(128, 452, "平行且相等", 12, GREY, anchor="middle")
    # ② 旋转型（手拉手）
    f.text(380, 36, "② 旋转型（手拉手）", 14, DARK, anchor="middle", weight="bold")
    O = (380, 250)
    A = (286, 216)
    B = (397, 152)
    C = (478, 233)
    D = (414, 344)
    for p, name, off in [(O, "O", (-14, 4)), (A, "A", (-12, -4)),
                         (B, "B", (12, -10)), (C, "C", (14, -2)),
                         (D, "D", (12, 12))]:
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.line(A[0], A[1], B[0], B[1], BLUE, 2.0)
    f.line(C[0], C[1], D[0], D[1], GRN, 2.0)
    f.line(O[0], O[1], A[0], A[1], BLUE, 2.0)
    f.line(O[0], O[1], B[0], B[1], BLUE, 2.0)
    f.line(O[0], O[1], C[0], C[1], GRN, 2.0)
    f.line(O[0], O[1], D[0], D[1], GRN, 2.0)
    f.line(A[0], A[1], C[0], C[1], RED, 1.8, dash="6 4")
    f.line(B[0], B[1], D[0], D[1], RED, 1.8, dash="6 4")
    for p in (O, A, B, C, D):
        f.dot(p[0], p[1])
    f.tick(O[0], O[1], A[0], A[1], 1, DARK)
    f.tick(O[0], O[1], B[0], B[1], 1, DARK)
    f.tick(O[0], O[1], C[0], C[1], 2, DARK)
    f.tick(O[0], O[1], D[0], D[1], 2, DARK)
    f.arc(O[0], O[1], 26, 200, 280, YEL, 1.8)
    f.arc(O[0], O[1], 26, 350, 70, YEL, 1.8)
    f.text(O[0] - 36, O[1] - 62, "∠1", 11, YEL, anchor="middle")
    f.text(O[0] + 58, O[1] + 62, "∠1", 11, YEL, anchor="middle")
    f.text(380, 430, "OA=OB、OC=OD、∠AOB=∠COD", 12, DARK, anchor="middle")
    f.text(380, 452, "→ SAS → △AOC≌△BOD → AC=BD", 12, RED, anchor="middle")
    # ③ 一线三等角（90° 特例：一线三垂直）
    f.text(635, 36, "③ 一线三等角", 14, DARK, anchor="middle", weight="bold")
    Bv = (560, 340)
    Dv = (635, 340)
    Cv = (710, 340)
    Av = (560, 265)
    Ev = (710, 265)
    f.line(Bv[0], Bv[1], Cv[0], Cv[1], DARK, 2.2)
    f.poly([Bv, Av, Dv], GRNF, GRN, 2.0)
    f.poly([Dv, Ev, Cv], BLUEF, BLUE, 2.0)
    f.line(Dv[0], Dv[1], Av[0], Av[1], GRN, 2.0)
    f.line(Dv[0], Dv[1], Ev[0], Ev[1], BLUE, 2.0)
    f.line(Cv[0], Cv[1], Ev[0], Ev[1], BLUE, 2.0)
    f.right_angle(Bv[0], Bv[1], 0, 270, 10, DARK)
    f.right_angle(Dv[0], Dv[1], 225, 315, 10, DARK)
    f.right_angle(Cv[0], Cv[1], 180, 270, 10, DARK)
    for p, name, off in [(Bv, "B", (-12, 18)), (Dv, "D", (0, 18)),
                         (Cv, "C", (12, 18)), (Av, "A", (-12, -4)),
                         (Ev, "E", (12, -4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(635, 430, "∠B = ∠ADE = ∠C（图为 90° 特例）", 12, DARK, anchor="middle")
    f.text(635, 452, "配 AB = DC → ASA → △ABD≌△DEC", 12, RED, anchor="middle")
    f.save("congruent-models.svg")


def fig_isosceles():
    f = Fig(760, 340)
    A = (380, 60)
    B = (230, 290)
    C = (530, 290)
    M = (380, 290)
    f.poly([A, B, C], "none", DARK, 2.2)
    f.line(A[0], A[1], M[0], M[1], RED, 2.2)
    for p, name, off in [(A, "A", (0, -12)), (B, "B", (-14, 16)),
                         (C, "C", (14, 16)), (M, "D", (0, 18))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    # 腰相等记号
    f.tick(A[0], A[1], B[0], B[1], 1, DARK)
    f.tick(A[0], A[1], C[0], C[1], 1, DARK)
    # 底边两段相等
    f.tick(B[0], B[1], M[0], M[1], 2, DARK)
    f.tick(M[0], M[1], C[0], C[1], 2, DARK)
    # 底角相等弧
    aB = math.degrees(math.atan2(A[1] - B[1], A[0] - B[0]))
    f.arc(B[0], B[1], 34, 0, aB, RED, 1.8)
    f.text(B[0] + 52, B[1] - 18, "∠B", 11, RED, anchor="middle")
    aC = math.degrees(math.atan2(A[1] - C[1], A[0] - C[0]))
    f.arc(C[0], C[1], 34, 180, aC, RED, 1.8)
    f.text(C[0] - 52, C[1] - 18, "∠C", 11, RED, anchor="middle")
    # 顶角被 AD 平分
    aAB = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
    aAC = math.degrees(math.atan2(C[1] - A[1], C[0] - A[0]))
    f.arc(A[0], A[1], 40, aAC, 90, BLUE, 1.8)
    f.arc(A[0], A[1], 40, 90, aAB, BLUE, 1.8)
    f.right_angle(M[0], M[1], 180, 270, 10, DARK)
    f.text(300, 330, "AB = AC（腰）", 12, DARK, anchor="middle")
    f.text(470, 330, "∠B = ∠C（等边对等角）", 12, RED, anchor="middle")
    f.text(380, 330, "", 12, DARK)
    f.text(380, 314, "", 12, DARK)
    f.text(620, 175, "AD 一人三职：", 13, DARK, anchor="middle", weight="bold")
    f.text(620, 200, "顶角平分线（蓝弧）", 12, BLUE, anchor="middle")
    f.text(620, 224, "底边中线（双记号）", 12, GRN, anchor="middle")
    f.text(620, 248, "底边上的高（直角记号）", 12, DARK, anchor="middle")
    f.save("isosceles-three-in-one.svg")


def fig_pythagoras():
    f = Fig(760, 340)
    f.text(380, 28, "勾股定理的拼图证明（四个全等的直角三角形）", 14, DARK,
           anchor="middle", weight="bold")
    ox, oy = 268, 50
    S = 224
    a, b = 96, 128
    outer = [(ox, oy), (ox + S, oy), (ox + S, oy + S), (ox, oy + S)]
    inner = [(ox + a, oy), (ox + S, oy + a), (ox + b, oy + S), (ox, oy + b)]
    t1 = [(ox, oy), (ox + a, oy), (ox, oy + b)]
    t2 = [(ox + a, oy), (ox + S, oy), (ox + S, oy + a)]
    t3 = [(ox + S, oy + a), (ox + S, oy + S), (ox + b, oy + S)]
    t4 = [(ox + b, oy + S), (ox, oy + S), (ox, oy + b)]
    for t, fill in [(t1, GRNF), (t2, BLUEF), (t3, GRNF), (t4, BLUEF)]:
        f.poly(t, fill, DARK, 1.6)
    f.poly(inner, YELF, YEL, 2.2)
    f.poly(outer, "none", DARK, 2.5)
    # 直角记号
    f.right_angle(ox, oy, 0, 90, 10)
    f.right_angle(ox + S, oy, 180, 90, 10)
    f.right_angle(ox + S, oy + S, 180, 270, 10)
    f.right_angle(ox, oy + S, 0, 270, 10)
    # 边长标注
    f.text(ox + a / 2, oy - 8, "a", 13, DARK, anchor="middle")
    f.text(ox + a + b / 2, oy - 8, "b", 13, DARK, anchor="middle")
    f.text(ox - 12, oy + b / 2, "b", 13, DARK, anchor="end")
    f.text(ox - 12, oy + b + a / 2, "a", 13, DARK, anchor="end")
    f.text(ox + S + 12, oy + a / 2, "a", 13, DARK)
    f.text(ox + S + 12, oy + a + b / 2, "b", 13, DARK)
    f.text(ox + b / 2, oy + S + 20, "b", 13, DARK, anchor="middle")
    f.text(ox + b + a / 2, oy + S + 20, "a", 13, DARK, anchor="middle")
    # 内部正方形标注
    f.text(ox + a + 46, oy + a - 18, "c", 13, RED, weight="bold")
    f.text((inner[0][0] + inner[1][0] + inner[2][0] + inner[3][0]) / 4,
           (inner[0][1] + inner[1][1] + inner[2][1] + inner[3][1]) / 4 + 6,
           "c²", 16, RED, anchor="middle", weight="bold")
    # 左侧推导
    f.text(30, 110, "(a+b)² = 4×½ab + c²", 14, DARK, weight="bold")
    f.text(30, 140, "展开：a²+2ab+b² = 2ab+c²", 12, GREY)
    f.text(30, 170, "得 a²+b² = c²", 14, RED, weight="bold")
    f.text(30, 210, "大正方形边长 a+b；", 12, GREY)
    f.text(30, 232, "四个三角形全等；", 12, GREY)
    f.text(30, 254, "中间是边长 c 的正方形。", 12, GREY)
    f.save("pythagoras-square.svg")


def fig_midline():
    f = Fig(760, 340)
    A = (300, 42)
    B = (150, 292)
    C = (610, 292)
    D = (225, 167)
    E = (455, 167)
    F = (380, 292)
    f.poly([A, D, E], GRNF, GRN, 1.8)
    f.poly([B, D, F], BLUEF, BLUE, 1.8)
    f.poly([D, E, F], YELF, YEL, 1.8)
    f.poly([E, C, F], PURPF, PURP, 1.8)
    f.poly([A, B, C], "none", DARK, 2.2)
    f.line(D[0], D[1], E[0], E[1], RED, 2.5)
    for p, name, off in [(A, "A", (0, -12)), (B, "B", (-14, 18)),
                         (C, "C", (14, 18)), (D, "D", (-14, -6)),
                         (E, "E", (14, -6)), (F, "F", (0, 20))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    # 中点记号
    f.tick(A[0], A[1], D[0], D[1], 1, DARK)
    f.tick(D[0], D[1], B[0], B[1], 1, DARK)
    f.tick(A[0], A[1], E[0], E[1], 1, DARK)
    f.tick(E[0], E[1], C[0], C[1], 1, DARK)
    f.tick(B[0], B[1], F[0], F[1], 1, DARK)
    f.tick(F[0], F[1], C[0], C[1], 1, DARK)
    f.text(340, 152, "DE（中位线）", 12, RED, anchor="middle")
    f.text(380, 332, "DE∥BC 且 DE=½BC；三条中位线把三角形分成 4 个全等的小三角形",
           12, DARK, anchor="middle")
    f.save("triangle-midline.svg")




# ============ 几何第二批（m2-03 四边形 4 篇） ============

def fig_polygon():
    f = Fig(760, 340)
    # ① 左：五边形拆三角形
    f.text(200, 40, "① 内角和：拆三角形", 14, DARK, anchor="middle", weight="bold")
    cx, cy, R = 200, 185, 110
    ang = [-90, -18, 54, 126, 198]
    V = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a)))
         for a in ang]
    A, B, C, D, E = V
    f.poly([A, B, C], GRNF, GRN, 1.8)
    f.poly([A, C, D], BLUEF, BLUE, 1.8)
    f.poly([A, D, E], YELF, YEL, 1.8)
    f.poly(V, "none", DARK, 2.2)
    f.line(A[0], A[1], C[0], C[1], RED, 2.2)
    f.line(A[0], A[1], D[0], D[1], RED, 2.2)
    for p, name, off in [(A, "A", (0, -12)), (B, "B", (14, 4)),
                         (C, "C", (12, 18)), (D, "D", (-10, 18)),
                         (E, "E", (-14, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(200, 316, "从 A 出发的 2 条对角线，分成 3 个三角形", 12, DARK, anchor="middle")
    f.text(200, 336, "内角和 = 3×180° = 540°", 13, RED, anchor="middle", weight="bold")
    # ② 右：正五边形外角和
    f.text(580, 40, "② 外角和：走一圈", 14, DARK, anchor="middle", weight="bold")
    cx2, cy2, R2 = 580, 178, 80
    W = [(cx2 + R2 * math.cos(math.radians(a)), cy2 + R2 * math.sin(math.radians(a)))
         for a in ang]
    f.poly(W, "none", DARK, 2.2)
    for i in range(5):
        Vi, Vn, Vp = W[i], W[(i + 1) % 5], W[(i - 1) % 5]
        t_in = math.degrees(math.atan2(Vi[1] - Vp[1], Vi[0] - Vp[0]))
        t_out = math.degrees(math.atan2(Vn[1] - Vi[1], Vn[0] - Vi[0]))
        f.arc(Vi[0], Vi[1], 18, t_in, t_out, RED, 1.8)
        if i in (1, 3):
            ex = Vi[0] + 34 * math.cos(math.radians(t_in))
            ey = Vi[1] + 34 * math.sin(math.radians(t_in))
            f.line(Vi[0], Vi[1], ex, ey, GREY, 1.4, dash="5 4")
            mid = (t_in + t_out) / 2
            lx = Vi[0] + 48 * math.cos(math.radians(mid))
            ly = Vi[1] + 48 * math.sin(math.radians(mid))
            f.text(lx, ly, "72°", 12, RED, anchor="middle")
    f.text(580, 316, "每个外角 72°（沿边走，每个顶点转一次）", 12, DARK, anchor="middle")
    f.text(580, 336, "外角和 = 5×72° = 360°，与边数无关", 13, RED,
           anchor="middle", weight="bold")
    f.save("polygon-interior.svg")


def fig_parallelogram():
    f = Fig(760, 360)
    # ① 左：性质三件套
    f.text(210, 40, "① 性质三件套", 14, DARK, anchor="middle", weight="bold")
    A, B, C, D = (120, 90), (360, 90), (300, 270), (60, 270)
    O = (210, 180)
    f.poly([A, B, C, D], "none", DARK, 2.2)
    f.line(A[0], A[1], C[0], C[1], GREY, 1.6)
    f.line(B[0], B[1], D[0], D[1], GREY, 1.6)
    # 对边平行记号（紫色）与相等记号
    f.chevron(250, 90, PURP, 8)
    f.chevron(190, 270, PURP, 8)
    f.tick(A[0], A[1], B[0], B[1], 1, DARK)
    f.tick(C[0], C[1], D[0], D[1], 1, DARK)
    f.tick(A[0], A[1], D[0], D[1], 2, DARK)
    f.tick(B[0], B[1], C[0], C[1], 2, DARK)
    # 对角线互相平分记号
    f.tick(A[0], A[1], O[0], O[1], 3, DARK)
    f.tick(O[0], O[1], C[0], C[1], 3, DARK)
    f.tick(B[0], B[1], O[0], O[1], 4, DARK)
    f.tick(O[0], O[1], D[0], D[1], 4, DARK)
    # 对角相等弧
    aAD = math.degrees(math.atan2(D[1] - A[1], D[0] - A[0]))
    f.arc(A[0], A[1], 22, 0, aAD, RED, 2.0)
    aCB = math.degrees(math.atan2(B[1] - C[1], B[0] - C[0]))
    f.arc(C[0], C[1], 22, 180, aCB, RED, 2.0)
    f.arc(B[0], B[1], 22, 180, aAD, BLUE, 2.0)
    f.arc(D[0], D[1], 22, 0, aCB, BLUE, 2.0)
    for p, name, off in [(A, "A", (-10, -6)), (B, "B", (10, -6)),
                         (C, "C", (12, 18)), (D, "D", (-12, 18)),
                         (O, "O", (12, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(210, 320, "红弧：∠A=∠C；蓝弧：∠B=∠D（邻角互补）", 12, DARK,
           anchor="middle")
    f.text(210, 342, "对边平行且相等，对角线互相平分", 12, DARK, anchor="middle")
    # ② 右：沿对角线拆成两个全等三角形
    f.text(590, 40, "② 拆开看：两个全等三角形", 14, DARK, anchor="middle", weight="bold")
    A2, B2, C2, D2 = (480, 110), (700, 110), (660, 280), (440, 280)
    f.poly([A2, B2, C2], GRNF, GRN, 1.8)
    f.poly([A2, C2, D2], BLUEF, BLUE, 1.8)
    f.line(A2[0], A2[1], C2[0], C2[1], DARK, 1.8)
    f.line(A2[0], A2[1], B2[0], B2[1], DARK, 2.0)
    f.line(B2[0], B2[1], C2[0], C2[1], DARK, 2.0)
    f.line(C2[0], C2[1], D2[0], D2[1], DARK, 2.0)
    f.line(D2[0], D2[1], A2[0], A2[1], DARK, 2.0)
    # 内错角弧：AD 截 AC（绿），AB 截 AC（蓝）
    aA2C2 = math.degrees(math.atan2(C2[1] - A2[1], C2[0] - A2[0]))
    aA2D2 = math.degrees(math.atan2(D2[1] - A2[1], D2[0] - A2[0]))
    f.arc(A2[0], A2[1], 22, aA2C2, aA2D2, GRN, 1.8)
    f.arc(A2[0], A2[1], 22, 0, aA2C2, BLUE, 1.8)
    aC2A2 = aA2C2 + 180
    aC2B2 = math.degrees(math.atan2(B2[1] - C2[1], B2[0] - C2[0]))
    aC2D2 = math.degrees(math.atan2(D2[1] - C2[1], D2[0] - C2[0]))
    f.arc(C2[0], C2[1], 22, aC2B2, aC2A2, GRN, 1.8)
    f.arc(C2[0], C2[1], 22, aC2D2, aC2A2, BLUE, 1.8)
    f.text(560, 304, "同色弧＝一对内错角", 12, DARK, anchor="middle")
    for p, name, off in [(A2, "A", (-12, -6)), (B2, "B", (10, -6)),
                         (C2, "C", (12, 18)), (D2, "D", (-12, 18))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(590, 336, "AB∥DC、AD∥BC → 内错角相等 + 公共边 AC", 12, DARK,
           anchor="middle")
    f.text(590, 356, "→ ASA → 两个三角形全等 → 对边相等", 12, RED,
           anchor="middle", weight="bold")
    f.save("parallelogram-properties.svg")


def fig_special():
    f = Fig(760, 380)
    # ① 矩形
    f.text(140, 52, "① 矩形：加直角", 14, DARK, anchor="middle", weight="bold")
    A, B, C, D = (50, 120), (230, 120), (230, 260), (50, 260)
    O = (140, 190)
    f.poly([A, B, C, D], "none", DARK, 2.2)
    f.line(A[0], A[1], C[0], C[1], GREY, 1.6)
    f.line(B[0], B[1], D[0], D[1], GREY, 1.6)
    f.right_angle(A[0], A[1], 0, 90, 9, DARK)
    f.right_angle(B[0], B[1], 180, 90, 9, DARK)
    f.right_angle(C[0], C[1], 180, 270, 9, DARK)
    f.right_angle(D[0], D[1], 0, 270, 9, DARK)
    for p, q in [(A, O), (B, O), (C, O), (D, O)]:
        f.tick(p[0], p[1], q[0], q[1], 1, DARK)
    for p, name, off in [(A, "A", (-16, -10)), (B, "B", (16, -10)),
                         (C, "C", (16, 20)), (D, "D", (-16, 20)),
                         (O, "O", (14, -6))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(140, 316, "对角线相等且互相平分", 12, DARK, anchor="middle")
    f.text(140, 338, "OA=OB=OC=OD", 13, RED, anchor="middle", weight="bold")
    # ② 菱形
    f.text(380, 52, "② 菱形：邻边相等", 14, DARK, anchor="middle", weight="bold")
    A2, B2, C2, D2 = (380, 100), (480, 190), (380, 280), (280, 190)
    O2 = (380, 190)
    f.poly([A2, B2, C2, D2], "none", DARK, 2.2)
    f.line(A2[0], A2[1], C2[0], C2[1], GREY, 1.6)
    f.line(B2[0], B2[1], D2[0], D2[1], GREY, 1.6)
    f.right_angle(O2[0], O2[1], 90, 180, 9, DARK)
    for s, e in [(A2, B2), (B2, C2), (C2, D2), (D2, A2)]:
        f.tick(s[0], s[1], e[0], e[1], 1, DARK)
    f.tick(A2[0], A2[1], O2[0], O2[1], 2, DARK)
    f.tick(O2[0], O2[1], C2[0], C2[1], 2, DARK)
    f.tick(B2[0], B2[1], O2[0], O2[1], 3, DARK)
    f.tick(O2[0], O2[1], D2[0], D2[1], 3, DARK)
    for p, name, off in [(A2, "A", (0, -12)), (B2, "B", (16, 4)),
                         (C2, "C", (0, 22)), (D2, "D", (-16, 4)),
                         (O2, "O", (12, -8))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(400, 146, "d1/2", 11, GREY)
    f.text(430, 184, "d2/2", 11, GREY)
    f.text(380, 316, "对角线互相垂直平分、平分对角", 12, DARK, anchor="middle")
    f.text(380, 338, "面积 = 1/2 × d1 × d2", 13, RED, anchor="middle", weight="bold")
    # ③ 正方形
    f.text(620, 52, "③ 正方形：两样都加", 14, DARK, anchor="middle", weight="bold")
    A3, B3, C3, D3 = (540, 130), (700, 130), (700, 290), (540, 290)
    O3 = (620, 210)
    f.poly([A3, B3, C3, D3], "none", DARK, 2.2)
    f.line(A3[0], A3[1], C3[0], C3[1], GREY, 1.6)
    f.line(B3[0], B3[1], D3[0], D3[1], GREY, 1.6)
    f.right_angle(O3[0], O3[1], 90, 180, 9, DARK)
    for p, q in [(A3, O3), (B3, O3), (C3, O3), (D3, O3)]:
        f.tick(p[0], p[1], q[0], q[1], 1, DARK)
    for p, name, off in [(A3, "A", (-16, -10)), (B3, "B", (16, -10)),
                         (C3, "C", (16, 20)), (D3, "D", (-16, 20)),
                         (O3, "O", (14, -6))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(620, 316, "对角线相等 + 互相垂直平分", 12, DARK, anchor="middle")
    f.text(620, 338, "正方形 = 矩形 ∩ 菱形", 13, RED, anchor="middle", weight="bold")
    f.save("special-quadrilaterals.svg")


def fig_trapezoid():
    f = Fig(760, 380)
    # ① 左：等腰梯形平移一腰
    f.text(230, 40, "① 等腰梯形：平移一腰", 14, DARK, anchor="middle", weight="bold")
    A, B, C, D = (140, 110), (320, 110), (370, 280), (90, 280)
    E = (190, 280)  # A + (C - B)，AE ∥ BC
    f.poly([A, B, C, E], BLUEF, BLUE, 1.6)
    f.poly([A, D, E], GRNF, GRN, 1.6)
    f.poly([A, B, C, D], "none", DARK, 2.2)
    f.line(A[0], A[1], E[0], E[1], RED, 2.2, dash="7 4")
    # 腰相等记号 + 平行记号
    f.tick(A[0], A[1], D[0], D[1], 1, DARK)
    f.tick(B[0], B[1], C[0], C[1], 1, DARK)
    f.chevron(215, 150, PURP, 7)
    f.chevron(348, 195, PURP, 7)
    # 等腰三角形 ADE 底角弧
    aDA = math.degrees(math.atan2(A[1] - D[1], A[0] - D[0]))
    f.arc(D[0], D[1], 22, 0, aDA, GRN, 1.8)
    aEA = math.degrees(math.atan2(A[1] - E[1], A[0] - E[0]))
    f.arc(E[0], E[1], 22, 180, aEA, GRN, 1.8)
    f.text(D[0] + 46, D[1] - 26, "∠ADE", 11, GRN, anchor="middle")
    f.text(E[0] + 52, E[1] - 26, "∠AED", 11, GRN, anchor="middle")
    for p, name, off in [(A, "A", (-12, -4)), (B, "B", (10, -4)),
                         (C, "C", (14, 18)), (D, "D", (-12, 18)),
                         (E, "E", (0, 20))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(230, 322, "AE∥BC：拆成平行四边形 ABCE + 等腰 △ADE", 12, DARK,
           anchor="middle")
    f.text(230, 346, "AD=AE=BC → ∠ADE=∠AED", 12, RED, anchor="middle", weight="bold")
    # ② 右：中点四边形
    f.text(575, 40, "② 中点四边形：连中点", 14, DARK, anchor="middle", weight="bold")
    A2, B2, C2, D2 = (450, 100), (700, 120), (660, 300), (470, 280)
    f.line(A2[0], A2[1], C2[0], C2[1], GREY, 1.6, dash="6 4")
    f.line(B2[0], B2[1], D2[0], D2[1], GREY, 1.6, dash="6 4")
    E2 = ((A2[0] + B2[0]) / 2, (A2[1] + B2[1]) / 2)
    F2 = ((B2[0] + C2[0]) / 2, (B2[1] + C2[1]) / 2)
    G2 = ((C2[0] + D2[0]) / 2, (C2[1] + D2[1]) / 2)
    H2 = ((D2[0] + A2[0]) / 2, (D2[1] + A2[1]) / 2)
    f.poly([E2, F2, G2, H2], YELF, YEL, 2.0)
    f.poly([A2, B2, C2, D2], "none", DARK, 2.2)
    for s, e in [(A2, E2), (E2, B2), (B2, F2), (F2, C2),
                 (C2, G2), (G2, D2), (D2, H2), (H2, A2)]:
        f.tick(s[0], s[1], e[0], e[1], 1, GREY, size=5)
    for p, name, off in [(A2, "A", (-14, -6)), (B2, "B", (14, -6)),
                         (C2, "C", (14, 18)), (D2, "D", (-14, 18)),
                         (E2, "E", (0, -10)), (F2, "F", (16, 4)),
                         (G2, "G", (0, 22)), (H2, "H", (-16, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(575, 322, "EF、HG 都是中位线：平行于 AC 且等于 AC 的一半", 12, DARK,
           anchor="middle")
    f.text(575, 346, "同理 EH、FG 平行于 BD → EFGH 是平行四边形", 12, RED,
           anchor="middle", weight="bold")
    f.save("trapezoid-midpoints.svg")



# ============ 几何第三批（m2-04 圆 6 篇） ============

def fig_circle_perp():
    f = Fig(760, 360)
    # ① 垂径定理
    f.text(190, 40, "① 垂径定理：连圆心，作垂线", 14, DARK, anchor="middle", weight="bold")
    O, R = (190, 175), 110
    half = math.sqrt(110**2 - 50**2)
    A, B = (190 - half, 225), (190 + half, 225)
    D, C = (190, 225), (190, 285)
    f.circle(O[0], O[1], R, "none", DARK, 2.2)
    f.line(A[0], A[1], B[0], B[1], DARK, 2.2)
    f.line(O[0], O[1], C[0], C[1], RED, 2.2)
    f.line(O[0], O[1], A[0], A[1], GREY, 1.4)
    f.text(128, 196, "R", 11, GREY)
    aA = math.degrees(math.atan2(A[1] - O[1], A[0] - O[0]))
    aB = math.degrees(math.atan2(B[1] - O[1], B[0] - O[0]))
    f.arc(O[0], O[1], R, aB, aA, RED, 3.2)
    f.right_angle(D[0], D[1], -90, 180, 9)
    f.tick(A[0], A[1], D[0], D[1], 1, DARK)
    f.tick(D[0], D[1], B[0], B[1], 1, DARK)
    f.text(204, 196, "d", 12, RED)
    f.text(141, 245, "a/2", 12, DARK, anchor="middle")
    for p, name, off in [(O, "O", (12, 4)), (A, "A", (-16, 0)), (B, "B", (16, 0)),
                         (D, "D", (-14, 18)), (C, "C", (14, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(190, 316, "OD⊥AB → AD=DB，OD 平分弧 AB", 12, DARK, anchor="middle")
    f.text(190, 341, "R²=d²+(a/2)²（勾股）", 13, RED, anchor="middle", weight="bold")
    # ② 拱桥
    f.text(600, 40, "② 拱桥：矢高与半径", 14, DARK, anchor="middle", weight="bold")
    O2, R2 = (600, 155), 100
    half2 = math.sqrt(R2**2 - 75**2)
    A2, B2 = (600 - half2, 230), (600 + half2, 230)
    aA2 = math.degrees(math.atan2(A2[1] - O2[1], A2[0] - O2[0]))
    aB2 = math.degrees(math.atan2(B2[1] - O2[1], B2[0] - O2[0]))
    arch = [(600 + R2 * math.cos(math.radians(a)),
             155 + R2 * math.sin(math.radians(a)))
            for a in [aA2 + i * 3 for i in range(int((aB2 + 360 - aA2) / 3) + 1)]]
    f.poly(arch, "none", DARK, 2.4)
    f.line(505, 230, 715, 230, DARK, 2.2)
    f.line(O2[0], O2[1], 600, 55, GREY, 1.4)
    f.text(588, 104, "R", 11, GREY)
    f.line(O2[0], O2[1], 600, 230, GREY, 1.4, dash="5 4")
    f.right_angle(600, 230, -90, 180, 9)
    f.arrow_line(575, 230, 575, 58, RED, 1.8)
    f.text(560, 150, "h", 12, RED)
    f.arrow_line(A2[0], 254, B2[0], 254, GREY, 1.6)
    f.text(600, 276, "a（跨度）", 12, GREY, anchor="middle")
    for p, name, off in [(O2, "O", (12, 4)), ((600, 230), "M", (12, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    # 桥面弦的两端点：图上要标出 A、B（alt 与 caption 都提到弦 AB）
    f.dot(A2[0], A2[1]); f.dot(B2[0], B2[1])
    f.text(A2[0] - 2, 214, "A", 13, DARK, anchor="middle")
    f.text(B2[0] + 2, 214, "B", 13, DARK, anchor="middle")
    f.text(600, 316, "R² = (a/2)² + (R−h)²", 13, RED, anchor="middle", weight="bold")
    f.text(600, 341, "圆心到桥面 = R−h（垂足是跨度中点）", 12, DARK, anchor="middle")
    f.save("circle-perpendicular.svg")


def fig_central_inscribed():
    f = Fig(760, 380)
    # ① 圆心角与圆周角
    f.text(200, 36, "① 圆周角 = 圆心角的一半", 14, DARK, anchor="middle", weight="bold")
    O, R = (200, 195), 120
    A = (200 + R * math.cos(math.radians(140)), 195 + R * math.sin(math.radians(140)))
    B = (200 + R * math.cos(math.radians(40)), 195 + R * math.sin(math.radians(40)))
    C = (200, 75)
    f.circle(O[0], O[1], R, "none", DARK, 2.0)
    f.arc(O[0], O[1], R, 40, 140, RED, 3.2)
    f.line(O[0], O[1], A[0], A[1], DARK, 2.0)
    f.line(O[0], O[1], B[0], B[1], DARK, 2.0)
    f.line(C[0], C[1], A[0], A[1], BLUE, 2.2)
    f.line(C[0], C[1], B[0], B[1], BLUE, 2.2)
    f.arc(O[0], O[1], 26, 40, 140, RED, 2.0)
    f.text(200, 239, "100°", 12, RED, anchor="middle")
    aCA = math.degrees(math.atan2(A[1] - C[1], A[0] - C[0]))
    aCB = math.degrees(math.atan2(B[1] - C[1], B[0] - C[0]))
    f.arc(C[0], C[1], 30, aCB, aCA, BLUE, 2.0)
    f.text(200, 122, "50°", 12, BLUE, anchor="middle")
    f.text(200, 331, "弧 AB", 11, RED, anchor="middle")
    for p, name, off in [(O, "O", (12, 4)), (A, "A", (-14, 18)), (B, "B", (14, 18)),
                         (C, "C", (0, -12))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(200, 355, "∠AOB=100°（圆心角），∠ACB=50°（圆周角）", 12, DARK, anchor="middle")
    # ② 直径所对的圆周角
    f.text(600, 36, "② 直径所对的圆周角是直角", 14, DARK, anchor="middle", weight="bold")
    O2, R2 = (600, 190), 110
    A2, B2 = (490, 190), (710, 190)
    C2, D2 = (600, 80), (600, 300)
    f.circle(O2[0], O2[1], R2, "none", DARK, 2.0)
    f.line(A2[0], A2[1], B2[0], B2[1], DARK, 3.0)
    for P in (C2, D2):
        f.line(P[0], P[1], A2[0], A2[1], BLUE, 2.0)
        f.line(P[0], P[1], B2[0], B2[1], BLUE, 2.0)
    f.right_angle(C2[0], C2[1], 45, 135, 9)
    f.right_angle(D2[0], D2[1], 225, 315, 9)
    for p, name, off in [(O2, "O", (10, -12)), (A2, "A", (-16, -8)), (B2, "B", (16, -8)),
                         (C2, "C", (0, -12)), (D2, "D", (0, 20))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(600, 340, "AB 是直径 → ∠ACB=∠ADB=90°", 12, DARK, anchor="middle")
    f.text(600, 362, "90° 圆周角反过来锁定直径", 13, RED, anchor="middle", weight="bold")
    f.save("central-inscribed.svg")


def fig_circle_position():
    f = Fig(760, 400)
    f.text(380, 26, "① 点与圆：比较 OP 与半径 r", 14, DARK, anchor="middle", weight="bold")
    # 三个点位置场景
    for cx, px, verdict in [(130, 155, "d<r：点在圆内"), (380, 425, "d=r：点在圆上"),
                            (630, 700, "d>r：点在圆外")]:
        f.circle(cx, 120, 45, "none", DARK, 1.8)
        f.line(cx, 120, px, 120, GREY, 1.4, dash="5 4")
        f.dot(cx, 120)
        f.text(cx + 8, 112, "O", 12, DARK)
        f.dot(px, 120, RED)
        f.text(px + 9, 108, "P", 12, RED)
        f.text(cx, 186, verdict, 12, DARK, anchor="middle")
        f.text((cx + px) / 2, 132, "d", 11, GREY, anchor="middle")
    f.text(380, 212, "② 直线与圆：比较圆心距 d 与半径 r", 14, DARK, anchor="middle", weight="bold")
    # 相交
    f.circle(130, 318, 42, "none", DARK, 1.8)
    f.line(85, 343, 175, 343, DARK, 2.2)
    f.line(130, 318, 130, 343, GREY, 1.4, dash="5 4")
    f.text(138, 334, "d", 11, GREY)
    for x in (130 - math.sqrt(42**2 - 25**2), 130 + math.sqrt(42**2 - 25**2)):
        f.dot(x, 343, RED, 2.6)
    f.dot(130, 318)
    f.text(138, 310, "O", 12, DARK)
    f.text(130, 382, "d<r：相交（两个公共点）", 12, DARK, anchor="middle")
    # 相切
    f.circle(380, 318, 42, "none", DARK, 1.8)
    f.line(335, 276, 425, 276, DARK, 2.2)
    f.line(380, 318, 380, 276, GREY, 1.4, dash="5 4")
    f.text(388, 296, "d", 11, GREY)
    f.right_angle(380, 276, -90, 180, 8)
    f.dot(380, 276, RED)
    f.dot(380, 318)
    f.text(388, 310, "O", 12, DARK)
    f.text(380, 382, "d=r：相切（一个公共点）", 12, DARK, anchor="middle")
    # 相离
    f.circle(630, 318, 42, "none", DARK, 1.8)
    f.line(585, 254, 675, 254, DARK, 2.2)
    f.line(630, 318, 630, 254, GREY, 1.4, dash="5 4")
    f.text(638, 282, "d", 11, GREY)
    f.dot(630, 318)
    f.text(638, 310, "O", 12, DARK)
    f.text(630, 382, "d>r：相离（无公共点）", 12, DARK, anchor="middle")
    f.save("circle-position.svg")


def fig_tangent():
    f = Fig(760, 390)
    # ① 切线性质
    f.text(200, 36, "① 切线：恰一个公共点，垂直于半径", 14, DARK, anchor="middle", weight="bold")
    O, R = (190, 190), 95
    f.circle(O[0], O[1], R, "none", DARK, 2.0)
    f.line(75, 285, 305, 285, DARK, 2.4)
    f.line(190, 190, 190, 285, RED, 2.2)
    f.right_angle(190, 285, -90, 0, 10)
    f.text(146, 240, "半径", 11, RED)
    f.line(100, 80, 280, 130, GREY, 1.5, dash="6 4")
    f.dot(165.5, 98.2, GREY, 2.6)
    f.dot(258.3, 124.0, GREY, 2.6)
    f.text(284, 105, "割线", 11, GREY)
    for p, name, off in [(O, "O", (12, 4)), ((190, 285), "C", (10, 20)),
                         ((75, 285), "A", (-12, -12)), ((305, 285), "B", (12, -12))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(200, 352, "切线 AB ⊥ 半径 OC；割线（虚线）有两个公共点", 12, DARK, anchor="middle")
    # ② 切线长定理
    f.text(570, 36, "② 切线长定理：PA=PB，OP 平分 ∠APB", 14, DARK, anchor="middle", weight="bold")
    O2, R2, P = (560, 240), 80, (560, 70)
    pa = math.sqrt(170**2 - 80**2)
    th = math.degrees(math.acos(80 / 170))
    A = (560 + 80 * math.cos(math.radians(-90 + th)), 240 + 80 * math.sin(math.radians(-90 + th)))
    B = (560 + 80 * math.cos(math.radians(-90 - th)), 240 + 80 * math.sin(math.radians(-90 - th)))
    f.circle(O2[0], O2[1], R2, "none", DARK, 2.0)
    f.line(P[0], P[1], A[0], A[1], DARK, 2.2)
    f.line(P[0], P[1], B[0], B[1], DARK, 2.2)
    f.line(O2[0], O2[1], A[0], A[1], BLUE, 1.8)
    f.line(O2[0], O2[1], B[0], B[1], BLUE, 1.8)
    f.line(P[0], P[1], O2[0], O2[1], RED, 2.0, dash="6 4")
    aPtoA = math.degrees(math.atan2(A[1] - P[1], A[0] - P[0]))
    aPtoB = math.degrees(math.atan2(B[1] - P[1], B[0] - P[0]))
    f.arc(P[0], P[1], 24, aPtoA, 90, GRN, 1.8)
    f.arc(P[0], P[1], 24, 90, aPtoB, GRN, 1.8)
    aAtoO = math.degrees(math.atan2(O2[1] - A[1], O2[0] - A[0]))
    aAtoP = math.degrees(math.atan2(P[1] - A[1], P[0] - A[0]))
    f.right_angle(A[0], A[1], aAtoO, aAtoP, 9)
    aBtoO = math.degrees(math.atan2(O2[1] - B[1], O2[0] - B[0]))
    aBtoP = math.degrees(math.atan2(P[1] - B[1], P[0] - B[0]))
    f.right_angle(B[0], B[1], aBtoO, aBtoP, 9)
    f.tick(P[0], P[1], A[0], A[1], 1, DARK)
    f.tick(P[0], P[1], B[0], B[1], 1, DARK)
    f.text(520, 106, "平分", 11, GRN, anchor="middle")
    for p, name, off in [(P, "P", (0, -14)), (O2, "O", (12, 4)),
                         (A, "A", (18, 6)), (B, "B", (-18, 6))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(570, 352, "∠OAP=∠OBP=90°；∠AOB+∠APB=180°", 12, DARK, anchor="middle")
    f.text(570, 374, "HL 全等：△OAP≌△OBP", 13, RED, anchor="middle", weight="bold")
    f.save("tangent-lines.svg")


def fig_arc_cone():
    f = Fig(760, 380)
    # ① 扇形
    f.text(190, 34, "① 扇形：n° 占整圆的 n/360", 14, DARK, anchor="middle", weight="bold")
    O, R = (190, 205), 110
    arcpts = [(190 + R * math.cos(math.radians(a)), 205 + R * math.sin(math.radians(a)))
              for a in range(30, 151, 5)]
    f.poly([O] + arcpts + [O], YELF, DARK, 1.6)
    f.arc(O[0], O[1], R, 30, 150, RED, 3.0)
    A, B = arcpts[0], arcpts[-1]
    f.line(O[0], O[1], A[0], A[1], DARK, 2.2)
    f.line(O[0], O[1], B[0], B[1], DARK, 2.2)
    f.arc(O[0], O[1], 26, 30, 150, DARK, 1.6)
    f.text(190, 249, "n°", 12, DARK, anchor="middle")
    f.text(238, 214, "R", 11, GREY)
    f.text(190, 334, "l（弧长）", 12, RED, anchor="middle")
    for p, name, off in [(O, "O", (12, 4)), (A, "A", (16, 4)), (B, "B", (-16, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(190, 358, "l=nπR/180　S=nπR²/360=½lR", 12, RED, anchor="middle", weight="bold")
    # ② 圆锥与展开
    f.text(600, 34, "② 圆锥：侧面展开是扇形", 14, DARK, anchor="middle", weight="bold")
    V, base, rx, ry = (460, 90), (460, 280), 65, 13
    f.line(V[0], V[1], base[0] - rx, base[1], DARK, 2.2)
    f.line(V[0], V[1], base[0] + rx, base[1], DARK, 2.2)
    ell = [(460 + rx * math.cos(math.radians(a)), 280 + ry * math.sin(math.radians(a)))
           for a in range(0, 360, 6)]
    f.poly(ell, "none", DARK, 1.8)
    f.line(V[0], V[1], base[0], base[1], GREY, 1.4, dash="5 4")
    f.text(468, 188, "h", 12, GREY)
    f.line(base[0], base[1], base[0] + rx, base[1], GREY, 1.6)
    f.text(492, 298, "r", 12, GREY)
    f.right_angle(460, 280, -90, 0, 8)
    f.text(516, 170, "l（母线）", 11, DARK, anchor="middle")
    for p, name, off in [(V, "V", (0, -12)), (base, "O", (10, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    # 展开扇形
    O2, R2 = (665, 250), 85
    pts = [(665 + R2 * math.cos(math.radians(a)), 250 + R2 * math.sin(math.radians(a)))
           for a in range(120, 241, 5)]
    f.poly([O2] + pts + [O2], YELF, DARK, 1.6)
    f.arc(O2[0], O2[1], R2, 120, 240, RED, 3.0)
    E1, E2 = pts[0], pts[-1]
    f.line(O2[0], O2[1], E1[0], E1[1], DARK, 2.0)
    f.line(O2[0], O2[1], E2[0], E2[1], DARK, 2.0)
    f.arc(O2[0], O2[1], 26, 120, 240, DARK, 1.6)
    f.text(620, 250, "θ", 12, DARK, anchor="middle")
    f.text(560, 306, "2πr", 12, RED, anchor="middle")
    f.text(640, 206, "l", 11, DARK, anchor="middle")
    f.arrow_line(540, 250, 573, 250, RED, 1.8)
    f.text(554, 220, "剪开摊平", 11, RED, anchor="middle")
    for p, name, off in [(O2, "O", (12, 4)), (E1, "", (0, 0)), (E2, "", (0, 0))]:
        if name:
            f.dot(p[0], p[1])
            f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(600, 336, "母线 l → 扇形半径；底面周长 2πr → 扇形弧长", 12, DARK, anchor="middle")
    f.text(600, 360, "S侧=πrl；θ=360°·r/l", 12, RED, anchor="middle", weight="bold")
    f.save("arc-sector-cone.svg")


def fig_regular_poly():
    f = Fig(760, 380)
    # ① 正六边形
    f.text(200, 30, "① 正六边形：两圆同心，R=a", 14, DARK, anchor="middle", weight="bold")
    O, R = (200, 190), 95
    V = [(200 + R * math.cos(math.radians(a)), 190 + R * math.sin(math.radians(a)))
         for a in (-90, -30, 30, 90, 150, 210)]
    A, B, C = V[0], V[1], V[2]
    f.circle(O[0], O[1], R, "none", DARK, 1.8)
    rin = R * math.sqrt(3) / 2
    inner = [(200 + rin * math.cos(math.radians(a)), 190 + rin * math.sin(math.radians(a)))
             for a in range(0, 360, 5)]
    f.poly(inner, "none", GREY, 1.4, dash="5 4")
    f.poly(V, "none", DARK, 2.2)
    f.line(O[0], O[1], B[0], B[1], RED, 2.0)
    f.text(236, 160, "R", 11, RED)
    M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    f.line(O[0], O[1], M[0], M[1], GREY, 1.6, dash="5 4")
    f.right_angle(M[0], M[1], 120, 210, 8)
    f.text(210, 152, "r", 11, GREY)
    f.text(231, 100, "a/2", 11, DARK, anchor="middle")
    f.dot(M[0], M[1])
    f.text(252, 124, "M", 12, DARK, anchor="middle")
    f.arc(O[0], O[1], 32, -30, 30, PURP, 2.0)
    f.text(246, 190, "60°", 12, PURP, anchor="middle")
    for p, name, off in [(O, "O", (12, 4)), (A, "A", (0, -12)), (B, "B", (16, 0)),
                         (C, "C", (16, 8))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(200, 330, "中心角 60°=外角；边心距 r=√3/2·R", 12, DARK, anchor="middle")
    f.text(200, 354, "R²=r²+(a/2)²；S=½×周长×r", 12, RED, anchor="middle", weight="bold")
    # ② 正方形
    f.text(600, 30, "② 正方形：对角线即直径", 14, DARK, anchor="middle", weight="bold")
    O2, R2 = (600, 190), 80
    S = [(600 + R2 * math.cos(math.radians(a)), 190 + R2 * math.sin(math.radians(a)))
         for a in (225, 315, 45, 135)]
    A2, B2, C2, D2 = S[3], S[2], S[1], S[0]
    f.circle(O2[0], O2[1], R2, "none", DARK, 1.8)
    f.poly(S, "none", DARK, 2.2)
    f.line(A2[0], A2[1], C2[0], C2[1], GREY, 1.4)
    f.line(B2[0], B2[1], D2[0], D2[1], GREY, 1.4)
    # O→C 半条对角线：标外接圆直径 2R
    f.line(O2[0], O2[1], C2[0], C2[1], GREY, 1.6, dash="5 4")
    f.right_angle(C2[0], C2[1], 180, 90, 8)
    f.text(615, 148, "2R=√2·a", 11, GREY, anchor="middle")
    # 边心距：O 垂直到边 AB 的中点，垂足处画直角记号
    f.line(O2[0], O2[1], O2[0], A2[1], GREY, 1.6)
    f.right_angle(O2[0], A2[1], 180, 270, 8)
    f.text(590, 216, "r=a/2", 11, GREY, anchor="end")
    f.text(600, 288, "a", 12, DARK, anchor="middle")
    for p, name, off in [(O2, "O", (0, -20)), (A2, "A", (-14, -8)), (B2, "B", (14, -8)),
                         (C2, "C", (14, 20)), (D2, "D", (-14, 20))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(600, 330, "对角线=2R=√2·a，边心距 r=a/2", 12, DARK, anchor="middle")
    f.text(600, 354, "面积=½×周长×r=a²", 12, RED, anchor="middle", weight="bold")
    f.save("regular-polygon.svg")




# ============ 几何第四批（m2-05 相似与投影 5 篇） ============

def fig_prop_segments():
    f = Fig(760, 340)
    # ① 左：三条平行线截两条直线
    f.text(190, 30, "① 平行截割：对应线段成比例", 14, DARK, anchor="middle", weight="bold")
    y1, y2, y3 = 70, 170, 270
    for y in (y1, y2, y3):
        f.line(40, y, 340, y, GRN, 2.2)
        f.chevron(190, y, GRN, 8)
    A, D = (70, y1), (150, y1)
    B, E = (135, y2), (285, y2)
    C, F = (200, y3), (420, y3)
    f.line(A[0], A[1], C[0], C[1], DARK, 2.0)
    f.line(D[0], D[1], F[0], F[1], BLUE, 2.0)
    for p, name, off, col in [(A, "A", (-13, -6), DARK), (B, "B", (-13, -8), DARK), (C, "C", (-13, 6), DARK),
                              (D, "D", (13, -6), BLUE), (E, "E", (13, -8), BLUE), (F, "F", (13, 6), BLUE)]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, col, anchor="middle")
    f.tick(A[0], A[1], B[0], B[1], 1, DARK)
    f.tick(D[0], D[1], E[0], E[1], 1, BLUE)
    f.tick(B[0], B[1], C[0], C[1], 2, DARK)
    f.tick(E[0], E[1], F[0], F[1], 2, BLUE)
    f.text(190, 306, "AB/BC = DE/EF", 13, RED, anchor="middle", weight="bold")
    f.text(190, 330, "平行线等距时退化为等分", 11, GREY, anchor="middle")
    # ② 右：三角形比例转移
    f.text(580, 30, "② 比例转移：DE∥BC", 14, DARK, anchor="middle", weight="bold")
    A2 = (500, 70)
    B2, C2 = (430, 280), (700, 280)
    D2 = (A2[0] + 0.5 * (B2[0] - A2[0]), A2[1] + 0.5 * (B2[1] - A2[1]))
    E2 = (A2[0] + 0.5 * (C2[0] - A2[0]), A2[1] + 0.5 * (C2[1] - A2[1]))
    f.poly([A2, B2, C2], "none", DARK, 2.2)
    f.line(D2[0], D2[1], E2[0], E2[1], GRN, 2.2)
    f.chevron((D2[0] + E2[0]) / 2, (D2[1] + E2[1]) / 2, GRN, 7)
    f.chevron((B2[0] + C2[0]) / 2, B2[1], GRN, 7)
    for p, name, off in [(A2, "A", (0, -12)), (B2, "B", (-12, 18)), (C2, "C", (12, 18)),
                         (D2, "D", (-16, -6)), (E2, "E", (14, -6))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(580, 306, "AD/DB = AE/EC = DE/BC", 13, RED, anchor="middle", weight="bold")
    f.text(580, 330, "合比：AD/AB = AE/AC", 11, GREY, anchor="middle")
    f.save("proportional-segments.svg")


def fig_similar_tri():
    f = Fig(760, 360)
    f.text(190, 30, "① 定义：三角等、三边成比例", 14, DARK, anchor="middle", weight="bold")
    # 小三角形 ABC（左）
    A, B, C = (55, 110), (180, 280), (35, 280)
    f.poly([A, B, C], GRNF, DARK, 1.8)
    # 大三角形 DEF（右）
    D, E, Fp = (245, 80), (378, 250), (228, 250)
    f.poly([D, E, Fp], "none", DARK, 1.8)
    f.arc(A[0], A[1], 20, math.degrees(math.atan2(C[1] - A[1], C[0] - A[0])),
          math.degrees(math.atan2(B[1] - A[1], B[0] - A[0])), RED, 1.8)
    f.arc(D[0], D[1], 22, math.degrees(math.atan2(Fp[1] - D[1], Fp[0] - D[0])),
          math.degrees(math.atan2(E[1] - D[1], E[0] - D[0])), RED, 1.8)
    f.arc(B[0], B[1], 20, math.degrees(math.atan2(A[1] - B[1], A[0] - B[0])),
          math.degrees(math.atan2(C[1] - B[1], C[0] - B[0])), BLUE, 1.8)
    f.arc(E[0], E[1], 22, math.degrees(math.atan2(D[1] - E[1], D[0] - E[0])),
          math.degrees(math.atan2(Fp[1] - E[1], Fp[0] - E[0])), BLUE, 1.8)
    f.arc(C[0], C[1], 20, math.degrees(math.atan2(B[1] - C[1], B[0] - C[0])),
          math.degrees(math.atan2(A[1] - C[1], A[0] - C[0])), PURP, 1.8)
    f.arc(Fp[0], Fp[1], 22, math.degrees(math.atan2(E[1] - Fp[1], E[0] - Fp[0])),
          math.degrees(math.atan2(D[1] - Fp[1], D[0] - Fp[0])), PURP, 1.8)
    for p, name, off in [(A, "A", (-12, -10)), (B, "B", (14, 14)), (C, "C", (-12, 14)),
                         (D, "D", (-4, -12)), (E, "E", (14, 14)), (Fp, "F", (-12, 14))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.arrow_line(196, 200, 218, 200, GREY, 1.6)
    f.text(207, 180, "k", 14, RED, anchor="middle", weight="bold")
    f.text(190, 306, "∠A=∠D、∠B=∠E、∠C=∠F", 12, DARK, anchor="middle")
    f.text(190, 330, "DE/AB=EF/BC=FD/CA=k", 13, RED, anchor="middle", weight="bold")
    # ② 性质
    f.text(585, 30, "② 性质：线性 k、面积 k²", 14, DARK, anchor="middle", weight="bold")
    A3, B3, C3 = (490, 100), (620, 270), (455, 270)
    A4 = (A3[0] + 0.55 * (B3[0] - A3[0]), A3[1] + 0.55 * (B3[1] - A3[1]))
    A5 = (A3[0] + 0.55 * (C3[0] - A3[0]), A3[1] + 0.55 * (C3[1] - A3[1]))
    f.poly([A3, B3, C3], GRNF, DARK, 1.6)
    f.poly([A3, A4, A5], YELF, DARK, 1.6)
    f.line(A3[0], A3[1], A3[0], 270, GREY, 1.3, dash="5 4")
    f.right_angle(A3[0], 270, 90, 180, 7)
    f.line(490, 180, 445, 180, GREY, 1.0)
    f.text(438, 184, "h", 11, GREY, anchor="end")
    f.line(510, 140, 540, 118, GREY, 1.0)
    f.text(545, 114, "h′=k·h", 11, DARK)
    f.text(524, 245, "内部相似", 10, GREY, anchor="middle")
    for p, name, off in [(A3, "A", (0, -12)), (B3, "B", (12, 16)), (C3, "C", (-12, 16))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(585, 306, "高/中线/周长比 = k", 13, RED, anchor="middle", weight="bold")
    f.text(585, 330, "面积比 = k²", 13, RED, anchor="middle", weight="bold")
    f.save("similar-triangles.svg")


def fig_similar_models():
    f = Fig(760, 380)
    for t, x in zip(["A 字型", "8 字型", "母子型（射影）", "一线三垂直"], [95, 285, 475, 665]):
        f.text(x, 30, t, 13, DARK, anchor="middle", weight="bold")
    # ① A 字型
    A, B, C = (95, 55), (170, 330), (22, 330)
    D = (A[0] + 0.5 * (B[0] - A[0]), A[1] + 0.5 * (B[1] - A[1]))
    E = (A[0] + 0.5 * (C[0] - A[0]), A[1] + 0.5 * (C[1] - A[1]))
    f.poly([A, B, C], "none", DARK, 2.0)
    f.poly([A, D, E], YELF, GRN, 2.0)
    f.chevron((D[0] + E[0]) / 2, (D[1] + E[1]) / 2, GRN, 7)
    f.chevron(96, 330, GRN, 7)
    for p, name, off in [(A, "A", (0, -12)), (B, "B", (12, 16)), (C, "C", (-10, 16)),
                         (D, "D", (14, 0)), (E, "E", (-14, 0))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(95, 356, "DE∥BC，共角 ∠A", 11, GREY, anchor="middle")
    # ② 8 字型
    yT, yB = 80, 320
    f.line(215, yT, 355, yT, GRN, 2.0)
    f.line(215, yB, 355, yB, GRN, 2.0)
    f.chevron(285, yT, GRN, 7)
    f.chevron(285, yB, GRN, 7)
    P = (285, 200)
    A2, B2 = (225, yT), (345, yT)
    C2, D2 = (225, yB), (345, yB)
    f.line(A2[0], A2[1], D2[0], D2[1], DARK, 1.8)
    f.line(B2[0], B2[1], C2[0], C2[1], DARK, 1.8)
    f.poly([A2, P, B2], YELF, DARK, 1.8)
    f.poly([C2, P, D2], BLUEF, BLUE, 1.8)
    f.arc(P[0], P[1], 18, math.degrees(math.atan2(A2[1] - P[1], A2[0] - P[0])),
          math.degrees(math.atan2(D2[1] - P[1], D2[0] - P[0])), RED, 1.8)
    f.arc(P[0], P[1], 18, math.degrees(math.atan2(B2[1] - P[1], B2[0] - P[0])),
          math.degrees(math.atan2(C2[1] - P[1], C2[0] - P[0])), RED, 1.8)
    for p, name, off in [(A2, "A", (-12, -8)), (B2, "B", (12, -8)), (C2, "C", (-12, 16)), (D2, "D", (12, 16))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(285, 356, "对顶角 + 平行线", 11, GREY, anchor="middle")
    # ③ 母子型
    B3, C3 = (390, 330), (560, 330)
    A3 = (415, 105)
    D3 = (508, 330)
    f.poly([A3, D3, B3], GRNF, DARK, 1.2)
    f.poly([A3, D3, C3], BLUEF, DARK, 1.2)
    f.poly([A3, B3, C3], "none", DARK, 2.0)
    f.line(A3[0], A3[1], D3[0], D3[1], RED, 2.0)
    f.right_angle(A3[0], A3[1], math.degrees(math.atan2(B3[1] - A3[1], B3[0] - A3[0])),
                  math.degrees(math.atan2(C3[1] - A3[1], C3[0] - A3[0])), 9)
    f.right_angle(D3[0], D3[1], -90, 180, 8)
    for p, name, off in [(A3, "A", (0, -12)), (B3, "B", (-10, 16)), (C3, "C", (12, 16)), (D3, "D", (16, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(475, 356, "AD²=BD·DC 等", 11, GREY, anchor="middle")
    # ④ 一线三垂直
    y = 300
    f.line(585, y, 745, y, DARK, 1.8)
    B4, D4, C4 = (588, y), (628, y), (730, y)
    A4b = (588, 210)
    E4 = (730, 255.6)
    f.poly([A4b, B4, D4], YELF, DARK, 1.6)
    f.poly([D4, C4, E4], BLUEF, DARK, 1.6)
    f.line(A4b[0], A4b[1], D4[0], D4[1], DARK, 1.8)
    f.line(D4[0], D4[1], E4[0], E4[1], DARK, 1.8)
    f.line(C4[0], C4[1], E4[0], E4[1], DARK, 1.8)
    f.right_angle(B4[0], B4[1], 90, 180, 8)
    f.right_angle(C4[0], C4[1], -90, 180, 8)
    aAD = math.degrees(math.atan2(A4b[1] - D4[1], A4b[0] - D4[0]))
    aDE = math.degrees(math.atan2(E4[1] - D4[1], E4[0] - D4[0]))
    f.right_angle(D4[0], D4[1], aAD, aDE, 8)
    for p, name, off in [(A4b, "A", (0, -12)), (B4, "B", (-10, 16)), (D4, "D", (0, 18)),
                         (C4, "C", (12, 16)), (E4, "E", (12, -8))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(665, 356, "∠B=∠C=∠ADE=90°", 11, GREY, anchor="middle")
    f.save("similar-models.svg")


def fig_homothety():
    f = Fig(760, 380)
    f.text(190, 30, "① 位似：对应点连线过中心", 14, DARK, anchor="middle", weight="bold")
    O = (70, 190)
    A, B, C = (95, 136), (131, 225), (168, 173)
    k = 2.0
    A2 = (O[0] + k * (A[0] - O[0]), O[1] + k * (A[1] - O[1]))
    B2 = (O[0] + k * (B[0] - O[0]), O[1] + k * (B[1] - O[1]))
    C2 = (O[0] + k * (C[0] - O[0]), O[1] + k * (C[1] - O[1]))
    for Q in (A2, B2, C2):
        d = math.hypot(Q[0] - O[0], Q[1] - O[1])
        f.line(O[0], O[1], Q[0] + 16 * (Q[0] - O[0]) / d, Q[1] + 16 * (Q[1] - O[1]) / d, GREY, 1.2, dash="5 4")
    f.poly([A, B, C], YELF, DARK, 1.8)
    f.poly([A2, B2, C2], "none", DARK, 1.8)
    f.tick(O[0], O[1], A[0], A[1], 1, DARK)
    f.tick(A[0], A[1], A2[0], A2[1], 1, DARK)
    for p, name, off in [(O, "O", (-14, 8)), (A, "A", (-13, -6)), (B, "B", (12, 6)), (C, "C", (14, 4)),
                         (A2, "A′", (0, -12)), (B2, "B′", (12, 4)), (C2, "C′", (14, -4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(190, 356, "OA′=2·OA（k=2），两三角形相似", 12, DARK, anchor="middle")
    # ② 右：坐标版
    f.text(600, 30, "② 坐标版：(x,y)→(kx,ky)", 14, DARK, anchor="middle", weight="bold")
    O0 = (430, 335)
    f.arrow_line(O0[0], O0[1], 720, O0[1], DARK, 1.6)
    f.arrow_line(O0[0], O0[1], O0[0], 75, DARK, 1.6)
    u = 30
    A3 = (O0[0] + 1 * u, O0[1] - 1 * u)
    B3 = (O0[0] + 3 * u, O0[1] - 1 * u)
    C3 = (O0[0] + 2 * u, O0[1] - 3 * u)
    A3p = (O0[0] + 2 * u, O0[1] - 2 * u)
    B3p = (O0[0] + 6 * u, O0[1] - 2 * u)
    C3p = (O0[0] + 4 * u, O0[1] - 6 * u)
    f.poly([A3, B3, C3], YELF, DARK, 1.8)
    f.poly([A3p, B3p, C3p], "none", BLUE, 1.8)
    for Q in (A3p, B3p, C3p):
        f.line(O0[0], O0[1], Q[0], Q[1], GREY, 1.2, dash="5 4")
    f.text(O0[0] - 10, O0[1] + 16, "O", 12, DARK, anchor="middle")
    f.text(712, O0[1] + 16, "x", 11, DARK)
    f.text(O0[0] - 12, 84, "y", 11, DARK)
    f.text(A3[0] - 6, A3[1] - 6, "A(1,1)", 10, DARK, anchor="end")
    f.text(B3[0] + 2, B3[1] + 16, "B(3,1)", 10, DARK, anchor="start")
    f.text(C3[0] - 6, C3[1] - 6, "C(2,3)", 10, DARK, anchor="end")
    f.line(A3p[0] + 2, A3p[1] + 6, 566, 302, GREY, 0.9)
    f.text(570, 306, "A′(2,2)", 10, BLUE)
    f.text(B3p[0] + 6, B3p[1] + 4, "B′(6,2)", 10, BLUE)
    f.text(C3p[0] + 8, C3p[1], "C′(4,6)", 10, BLUE)
    f.text(600, 356, "k=2：坐标乘 2，面积 ×4", 12, RED, anchor="middle", weight="bold")
    f.save("homothety.svg")


def fig_projection_views():
    f = Fig(760, 400)
    f.text(230, 26, "① 平行投影：影长测高", 14, DARK, anchor="middle", weight="bold")
    # 太阳光线箭头
    for x0 in (50, 110, 170):
        f.arrow_line(x0, 60, x0 + 38, 98, YEL, 1.8)
    f.text(120, 46, "太阳光（平行）", 11, YEL, anchor="middle")
    # 地面
    f.line(30, 300, 460, 300, DARK, 2.0)
    # 杆 1
    f.poly([(100, 300), (100, 250), (175, 300)], YELF, DARK, 1.6)
    f.line(100, 250, 100, 300, DARK, 2.2)
    f.line(100, 250, 175, 300, GREY, 1.3, dash="5 4")
    # 杆 2（高）
    f.poly([(240, 300), (240, 150), (435, 300)], BLUEF, "none", 0)
    f.line(240, 150, 240, 300, DARK, 2.2)
    f.line(240, 150, 435, 300, GREY, 1.3, dash="5 4")
    f.text(92, 278, "50", 10, DARK, anchor="end")
    f.text(134, 320, "影 75", 10, RED, anchor="middle")
    f.arrow_line(248, 152, 248, 296, RED, 1.6)
    f.text(234, 225, "150", 10, DARK, anchor="middle")
    f.arrow_line(300, 282, 430, 282, RED, 1.6)
    f.text(348, 268, "影 x", 10, RED, anchor="middle")
    f.text(230, 338, "50/75 = 150/x → x = 225", 13, RED, anchor="middle", weight="bold")
    f.text(230, 362, "光线平行 → 两「高—影」三角形相似", 11, DARK, anchor="middle")
    # ② 右：三视图
    f.text(600, 26, "② 三视图（正投影）", 14, DARK, anchor="middle", weight="bold")
    g = 30
    # 俯视图（带层数数字）
    ox, oy = 450, 90
    f.poly([(ox, oy), (ox + 2 * g, oy), (ox + 2 * g, oy + 2 * g), (ox, oy + 2 * g)], "none", DARK, 1.8)
    f.line(ox + g, oy, ox + g, oy + 2 * g, GREY, 1.2)
    f.line(ox, oy + g, ox + 2 * g, oy + g, GREY, 1.2)
    f.text(ox + g / 2, oy + g / 2 + 4, "2", 13, RED, anchor="middle")
    f.text(ox + 3 * g / 2, oy + g / 2 + 4, "1", 12, DARK, anchor="middle")
    f.text(ox + g / 2, oy + 3 * g / 2 + 4, "1", 12, DARK, anchor="middle")
    f.text(ox + 3 * g / 2, oy + 3 * g / 2 + 4, "1", 12, DARK, anchor="middle")
    f.text(ox + g, oy - 10, "俯视图（数字=层数）", 11, DARK, anchor="middle")
    # 主视图（俯视图正下方，长对正）
    my = 240
    f.poly([(ox, my + 2 * g), (ox, my + g), (ox + g, my + g), (ox + g, my), (ox + 2 * g, my), (ox + 2 * g, my + 2 * g)],
           "none", DARK, 1.8)
    f.text(ox + g, my + 2 * g + 18, "主视图", 11, DARK, anchor="middle")
    # 左视图（主视图右侧，高平齐）
    lx = 620
    f.poly([(lx, my + 2 * g), (lx, my + g), (lx + g, my + g), (lx + g, my), (lx + 2 * g, my), (lx + 2 * g, my + 2 * g)],
           "none", DARK, 1.8)
    f.text(lx + g, my + 2 * g + 18, "左视图", 11, DARK, anchor="middle")
    # 对齐虚线：长对正
    f.line(ox, oy + 2 * g, ox, my + 2 * g, GREY, 1.1, dash="4 3")
    f.line(ox + 2 * g, oy + 2 * g, ox + 2 * g, my + 2 * g, GREY, 1.1, dash="4 3")
    # 高平齐
    f.line(ox + 2 * g, my, lx, my, GREY, 1.1, dash="4 3")
    f.line(ox + 2 * g, my + 2 * g, lx, my + 2 * g, GREY, 1.1, dash="4 3")
    # 宽相等：俯视图右边与左视图左侧各一段短虚线
    f.line(ox + 2 * g - 14, oy + g, ox + 2 * g + 6, oy + g, GREY, 1.1, dash="2 3")
    f.line(lx - 6, oy + g, lx + 14, oy + g, GREY, 1.1, dash="2 3")
    f.text(556, 132, "宽相等", 10, GREY, anchor="middle")
    f.text(536, my - 8, "高平齐", 10, GREY, anchor="middle")
    f.text(ox - 8, (oy + 2 * g + my) / 2 + 4, "长对正", 10, GREY, anchor="middle")
    f.text(600, 362, "三图互检：长对正、高平齐、宽相等", 12, RED, anchor="middle", weight="bold")
    f.save("projection-views.svg")


def fig_symmetry():
    f = Fig(760, 380)
    # ① 左：轴对称
    f.text(190, 30, "① 轴对称：对称轴垂直平分对应点连线", 14, DARK, anchor="middle", weight="bold")
    lx = 200
    f.line(lx, 55, lx, 330, DARK, 2.0)
    f.text(lx + 8, 66, "l", 12, DARK)
    A, B, C = (90, 110), (140, 230), (60, 245)
    A2 = (2 * lx - A[0], A[1])
    B2 = (2 * lx - B[0], B[1])
    C2 = (2 * lx - C[0], C[1])
    for P, Q in [(A, A2), (B, B2), (C, C2)]:
        f.line(P[0], P[1], Q[0], Q[1], GREY, 1.2, dash="5 4")
        mx = (P[0] + Q[0]) / 2
        f.tick(P[0], P[1], mx, P[1], 1, GREY)
        f.tick(mx, P[1], Q[0], Q[1], 1, GREY)
    f.poly([A, B, C], YELF, DARK, 1.8)
    f.poly([A2, B2, C2], "none", DARK, 1.8)
    f.right_angle(lx, 110, 90, 0, 11, GREY)
    f.text(lx - 12, 126, "M", 11, DARK, anchor="middle")
    for p, name, off in [(A, "A", (-12, -6)), (B, "B", (0, -10)), (C, "C", (-8, -8)),
                         (A2, "A′", (12, -6)), (B2, "B′", (2, -14)), (C2, "C′", (12, -8))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(190, 356, "翻折重合：AB=A′B′，AM=MA′，l⊥AA′", 12, DARK, anchor="middle")
    # ② 右：中心对称
    f.text(580, 30, "② 中心对称：对称中心平分对应点连线", 14, DARK, anchor="middle", weight="bold")
    O = (580, 195)
    A, B, C = (460, 120), (440, 255), (550, 275)
    A2 = (2 * O[0] - A[0], 2 * O[1] - A[1])
    B2 = (2 * O[0] - B[0], 2 * O[1] - B[1])
    C2 = (2 * O[0] - C[0], 2 * O[1] - C[1])
    for P, Q in [(A, A2), (B, B2), (C, C2)]:
        f.line(P[0], P[1], Q[0], Q[1], GREY, 1.2, dash="5 4")
    f.poly([A, B, C], YELF, DARK, 1.8)
    f.poly([A2, B2, C2], "none", DARK, 1.8)
    # 等长刻痕放在靠近 O 的 30% 处，避开 B′C′ 边
    for P in (B, B2):
        t = 0.55
        f.tick(O[0], O[1], O[0] + t * (P[0] - O[0]), O[1] + t * (P[1] - O[1]), 2, DARK)
    f.dot(O[0], O[1], RED)
    f.text(O[0] + 12, O[1] + 18, "O", 12, RED, anchor="middle")
    for p, name, off in [(A, "A", (-10, -8)), (B, "B", (-12, 4)), (C, "C", (12, 4)),
                         (A2, "A′", (12, -8)), (B2, "B′", (12, 4)), (C2, "C′", (12, 4))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(580, 356, "旋转 180° 重合：OB=OB′，O 是 BB′ 中点", 12, DARK, anchor="middle")
    f.save("symmetry.svg")


def fig_translation_rotation():
    f = Fig(760, 380)
    # ① 左：平移
    f.text(200, 30, "① 平移：方向 + 距离", 14, DARK, anchor="middle", weight="bold")
    A, B, C = (80, 245), (160, 195), (180, 270)
    dx, dy = 150, -80
    A2 = (A[0] + dx, A[1] + dy)
    B2 = (B[0] + dx, B[1] + dy)
    C2 = (C[0] + dx, C[1] + dy)
    for P, Q in [(A, A2), (B, B2), (C, C2)]:
        f.arrow_line(P[0], P[1], Q[0], Q[1], GREY, 1.6)
        f.tick(P[0], P[1], Q[0], Q[1], 1, GREY)
    f.poly([A, B, C], YELF, DARK, 1.8)
    f.poly([A2, B2, C2], "none", DARK, 1.8)
    for p, name, off in [(A, "A", (-12, -6)), (B, "B", (0, -10)), (C, "C", (10, 10)),
                         (A2, "A′", (0, 16)), (B2, "B′", (6, -10)), (C2, "C′", (10, 10))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(300, 74, "位移向量处处相同", 11, GREY, anchor="middle")
    f.text(200, 356, "对应点连线平行且相等，图形不变", 12, DARK, anchor="middle")
    # ② 右：旋转（绕 O 逆时针 90°，两个三角形互不重叠）
    f.text(590, 30, "② 旋转：中心 + 方向 + 角度", 14, DARK, anchor="middle", weight="bold")
    O = (620, 250)
    A, B, C = (700, 205), (730, 175), (655, 150)

    def rot(p):
        dx_, dy_ = p[0] - O[0], p[1] - O[1]
        return (O[0] + dy_, O[1] - dx_)

    A2, B2, C2 = rot(A), rot(B), rot(C)
    f.line(O[0], O[1], A[0], A[1], GREY, 1.2, dash="5 4")
    f.line(O[0], O[1], A2[0], A2[1], GREY, 1.2, dash="5 4")
    f.tick(O[0], O[1], A[0], A[1], 1, GREY)
    f.tick(O[0], O[1], A2[0], A2[1], 1, GREY)
    r = math.hypot(A[0] - O[0], A[1] - O[1])
    aA = math.degrees(math.atan2(A[1] - O[1], A[0] - O[0]))
    aA2 = math.degrees(math.atan2(A2[1] - O[1], A2[0] - O[0]))
    mid = aA + (((aA2 - aA + 180) % 360) - 180) / 2
    f.arc(O[0], O[1], r, aA, aA2, RED, 1.2)
    f.arc(O[0], O[1], 45, aA, aA2, RED, 2.0)
    px, py = O[0] + r * math.cos(math.radians(aA2)), O[1] + r * math.sin(math.radians(aA2))
    f.arrow_head(px, py, (px - O[0]) / r, (py - O[1]) / r, RED, 8)
    f.poly([A, B, C], YELF, DARK, 1.8)
    f.poly([A2, B2, C2], "none", DARK, 1.8)
    f.dot(O[0], O[1], RED)
    f.text(O[0] + 12, O[1] + 18, "O", 12, RED, anchor="middle")
    amx = O[0] + 66 * math.cos(math.radians(mid))
    amy = O[1] + 66 * math.sin(math.radians(mid))
    f.text(amx, amy, "旋转角", 11, RED, anchor="middle")
    for p, name, off in [(A, "A", (10, 6)), (B, "B", (10, -4)), (C, "C", (-12, -6)),
                         (A2, "A′", (-12, 4)), (B2, "B′", (-10, -8)), (C2, "C′", (-12, 8))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(590, 356, "OA=OA′，∠AOA′=旋转角（方向不写要考虑两解）", 12, DARK, anchor="middle")
    f.save("translation-rotation.svg")


def fig_transform_coords():
    f = Fig(680, 360)
    f.text(340, 28, "三种对称的坐标规律：P(3,1) 的三个像", 14, DARK, anchor="middle", weight="bold")
    O = (340, 240)
    u = 50
    f.arrow_line(O[0], O[1], 650, O[1], DARK, 1.6)
    f.arrow_line(O[0], O[1], O[0], 52, DARK, 1.6)
    f.text(640, O[1] + 20, "x", 11, DARK)
    f.text(O[0] - 14, 62, "y", 11, DARK)
    f.text(O[0] - 14, O[1] + 18, "O", 12, DARK, anchor="middle")
    P = (O[0] + 3 * u, O[1] - 1 * u)
    P1 = (O[0] + 3 * u, O[1] + 1 * u)
    P2 = (O[0] - 3 * u, O[1] - 1 * u)
    P3 = (O[0] - 3 * u, O[1] + 1 * u)
    # 轴向刻度数字
    for k, lab in [(3, "3"), (-3, "−3")]:
        f.text(O[0] + k * u + 7, O[1] + 20, lab, 10, GREY)
    f.poly([P, P1, P3, P2], "none", GREYM, 1.2, dash="4 4")
    f.line(P[0], P[1], P1[0], P1[1], GREY, 1.2, dash="5 4")
    f.line(P[0], P[1], P2[0], P2[1], GREY, 1.2, dash="5 4")
    f.line(P[0], P[1], P3[0], P3[1], GREY, 1.2, dash="5 4")
    f.tick(P[0], P[1], P1[0], P1[1], 1, GREY)
    f.tick(P[0], P[1], P2[0], P2[1], 1, GREY)
    f.dot(P[0], P[1], YEL)
    f.text(P[0] + 10, P[1] - 10, "P(3,1)", 12, YEL)
    f.dot(P1[0], P1[1], BLUE)
    f.text(P1[0] + 10, P1[1] + 18, "P₁(3,−1)", 12, BLUE)
    f.text(P1[0] + 10, P1[1] - 12, "关于 x 轴：y 变号", 11, BLUE)
    f.dot(P2[0], P2[1], GRN)
    f.text(P2[0] - 10, P2[1] - 12, "P₂(−3,1)", 12, GRN, anchor="end")
    f.text(P2[0] - 10, P2[1] + 18, "关于 y 轴：x 变号", 11, GRN, anchor="end")
    f.dot(P3[0], P3[1], PURP)
    f.text(P3[0] - 10, P3[1] + 18, "P₃(−3,−1)", 12, PURP, anchor="end")
    f.text(P3[0] - 10, P3[1] - 12, "关于原点：双变号", 11, PURP, anchor="end")
    f.text(340, 338, "四点是同一矩形的四角：变谁的号，一目了然", 12, DARK, anchor="middle")
    f.save("transform-coordinates.svg")


def fig_geometric_extremum():
    f = Fig(760, 400)
    # ① 左：将军饮马
    f.text(230, 28, "① 将军饮马：对称拉直", 14, DARK, anchor="middle", weight="bold")
    ry = 225
    f.line(40, ry, 440, ry, BLUE, 2.2)
    f.text(50, ry - 8, "l", 12, BLUE)
    A, B = (90, 125), (330, 160)
    A2 = (90, 2 * ry - A[1])
    f.line(A[0], A[1], A2[0], A2[1], GREY, 1.2, dash="5 4")
    f.right_angle(A2[0], ry, 90, 0, 10, GREY)
    f.text(A2[0] - 14, ry + 16, "M", 11, DARK, anchor="middle")
    f.tick(A[0], A[1], A[0], ry, 1, GREY)
    f.tick(A[0], ry, A2[0], A2[1], 1, GREY)
    t = (ry - A2[1]) / (B[1] - A2[1])
    Px = A2[0] + t * (B[0] - A2[0])
    f.line(A2[0], A2[1], B[0], B[1], RED, 2.0)
    f.line(A[0], A[1], Px, ry, DARK, 1.4, dash="5 4")
    for p, name, off in [(A, "A", (-12, -6)), (B, "B", (12, -6)), (A2, "A′", (-14, 10)),
                         ((Px, ry), "P", (0, 20))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 12, DARK, anchor="middle")
    f.text(230, 372, "AP+PB = A′P+PB ≥ A′B（两点之间线段最短）", 12, RED, anchor="middle", weight="bold")
    # ② 右：隐圆
    f.text(590, 28, "② 隐圆：定边直角锁圆", 14, DARK, anchor="middle", weight="bold")
    O = (610, 255)
    r = 75
    A, B = (O[0] - r, O[1]), (O[0] + r, O[1])
    Q = (O[0], O[1] - 100)
    Pn = (O[0], O[1] - r)
    Pf = (O[0], O[1] + r)
    f.circle(O[0], O[1], r, "none", GREY, 1.4)
    f.line(A[0], A[1], B[0], B[1], DARK, 1.8)
    f.line(Pn[0], Pn[1], A[0], A[1], DARK, 1.4)
    f.line(Pn[0], Pn[1], B[0], B[1], DARK, 1.4)
    f.right_angle(Pn[0], Pn[1], 135, 45, 10, RED)
    f.line(Q[0], Q[1], Pf[0], Pf[1], PURP, 1.1, dash="2 4")
    f.line(Q[0], Q[1], Pn[0], Pn[1], PURP, 2.2)
    f.text(566, 240, "r=3", 11, GRN)
    f.text(624, 232, "d=4", 11, PURP)
    f.text(Q[0] - 10, Q[1] - 4, "Q", 12, DARK, anchor="end")
    f.text(Pn[0] - 10, Pn[1] - 2, "P", 12, DARK, anchor="end")
    f.text(630, (Q[1] + Pn[1]) / 2 + 6, "min=1", 11, PURP)
    f.text(622, 316, "max=7", 11, PURP)
    for p in (A, B, O, Q, Pn):
        f.dot(p[0], p[1])
    f.dot(Pf[0], Pf[1], GREYM)
    f.text(A[0] - 12, A[1] - 6, "A", 12, DARK, anchor="middle")
    f.text(B[0] + 12, B[1] - 6, "B", 12, DARK, anchor="middle")
    f.text(O[0] - 12, O[1] + 22, "O", 12, GREY, anchor="middle")
    f.text(590, 372, "∠APB=90° → P 在以 AB 为直径的圆上，QP ∈ [d−r, d+r]", 12, RED, anchor="middle", weight="bold")
    f.save("geometric-extremum.svg")


def fig_trig_ratios():
    f = Fig(700, 430)
    f.text(30, 32, "① 锐角三角函数：对边、邻边、斜边", 15, DARK, weight="bold")
    A, B, C = (170, 300), (500, 110), (500, 300)
    # 斜边 AB（灰）、A 的邻边 AC（蓝）、A 的对边 BC（红）
    f.line(A[0], A[1], B[0], B[1], GREY, 3.0)
    f.line(A[0], A[1], C[0], C[1], BLUE, 3.0)
    f.line(B[0], B[1], C[0], C[1], RED, 3.0)
    # 直角记号在 C
    f.right_angle(C[0], C[1], 180, 270, 12)
    # 角 A 的弧（红色）
    aA = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
    f.arc(A[0], A[1], 52, aA, 0, RED, 2.2)
    f.text(A[0] + 62, A[1] - 14, "α", 14, RED, anchor="middle", weight="bold")
    # 角 B 的弧（绿色）
    aB = math.degrees(math.atan2(A[1] - B[1], A[0] - B[0]))
    f.arc(B[0], B[1], 48, 90, aB, GRN, 2.2)
    f.text(B[0] - 32, B[1] + 34, "β", 14, GRN, anchor="middle", weight="bold")
    for p, name, off in [(A, "A", (-14, 16)), (B, "B", (12, -6)), (C, "C", (16, 10))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    # 边名：a 在 BC 右侧，b 在 AC 下方，c 在 AB 中点上方
    f.text(516, 214, "a", 14, RED, anchor="middle", weight="bold")
    f.text(335, 324, "b", 14, BLUE, anchor="middle", weight="bold")
    f.text(322, 190, "c", 14, GREY, anchor="middle", weight="bold")
    f.text(516, 214, "", 10, RED)
    # 说明：对 A 而言
    f.text(516, 240, "A 的对边", 11, RED)
    f.text(380, 346, "A 的邻边", 11, BLUE)
    f.text(300, 168, "斜边", 11, GREY)
    # 右侧公式区
    x0 = 566
    f.text(x0, 96, "以 A 为准：", 12, DARK, weight="bold")
    f.text(x0, 124, "sin A = a / c", 13, RED)
    f.text(x0, 150, "cos A = b / c", 13, BLUE)
    f.text(x0, 176, "tan A = a / b", 13, DARK)
    f.text(x0, 210, "以 B 为准：", 12, GRN, weight="bold")
    f.text(x0, 238, "sin B = b / c", 13, GRN)
    f.text(x0, 264, "cos B = a / c", 13, GRN)
    f.text(x0, 290, "tan B = b / a", 13, GRN)
    f.line(x0, 306, 686, 306, GREY, 1.0)
    f.text(x0, 330, "换到另一个角，", 11, DARK)
    f.text(x0, 352, "a 与 b 就互换", 11, DARK)
    f.text(x0, 382, "斜边 c 始终不变", 11, GREY)
    f.save("trig-ratios.svg")


def fig_right_triangle():
    f = Fig(760, 380)
    f.text(28, 30, "① 解直角三角形的三条路径　　② 坡角与坡度", 15, DARK, weight="bold")
    # 左：通用示意图
    A, B, C = (120, 250), (250, 105), (250, 250)
    f.line(A[0], A[1], B[0], B[1], GREY, 3.2)      # 斜边
    f.line(A[0], A[1], C[0], C[1], BLUE, 2.6)     # 一条直角边
    f.line(B[0], B[1], C[0], C[1], GRN, 2.6)      # 另一条直角边
    f.right_angle(C[0], C[1], 180, 270, 10)
    aA = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
    f.arc(A[0], A[1], 44, aA, 0, RED, 2.0)
    f.text(A[0] + 56, A[1] - 6, "α", 14, RED, anchor="middle", weight="bold")
    for p, name, off in [(A, "A", (-14, 16)), (B, "B", (12, -6)), (C, "C", (16, 10))]:
        f.dot(p[0], p[1])
        f.text(p[0] + off[0], p[1] + off[1], name, 13, DARK, anchor="middle")
    f.text(146, 146, "c（斜边）", 11, GREY, anchor="middle")
    f.text(186, 272, "已知 b", 11, BLUE, anchor="middle")
    f.text(272, 180, "求 a", 11, GRN, anchor="middle")
    f.text(120, 292, "未知边先标出，再选公式", 11, DARK)
    # 三条路径
    y0 = 316
    f.text(28, y0, "已知斜边 → 用正弦、余弦", 12, RED)
    f.text(28, y0 + 22, "已知一条直角边和锐角 → 用正切或余弦", 12, BLUE)
    f.text(28, y0 + 44, "已知两条直角边 → 先勾股，再求比值", 12, GRN)
    # 右：坡角示意图
    O = (520, 300)
    f.line(460, 300, 745, 300, DARK, 2.0)          # 地面
    f.line(O[0], O[1], 700, 180, GREY, 3.0)         # 坡面
    f.line(O[0], O[1], O[0], 180, BLUE, 2.4)        # 铅直
    f.arc(O[0], O[1], 54, -34, 0, RED, 2.2)
    f.text(O[0] + 66, O[1] - 10, "α", 13, RED, anchor="middle", weight="bold")
    f.text(O[0] - 14, O[1] + 18, "O", 12, DARK, anchor="middle")
    f.text(612, 232, "l", 13, GREY, anchor="middle", weight="bold")
    f.text(502, 240, "h", 13, BLUE, anchor="middle", weight="bold")
    f.text(614, 322, "b", 13, DARK, anchor="middle", weight="bold")
    f.text(464, 324, "地面", 11, GREY)
    f.text(470, 104, "坡角 α 是坡面与水平面的夹角", 12, DARK)
    f.text(470, 130, "坡度 i = h / b = tan α", 13, RED, weight="bold")
    f.text(470, 156, "i = 0.75 表示每 100 米水平距离上升 75 米", 11, GREY)
    f.save("right-triangle-solving.svg")


def fig_trig_applications():
    f = Fig(780, 360)
    f.text(24, 28, "三角函数的三种典型应用", 15, DARK, weight="bold")
    # ── 左格：测树高 ──
    f.text(130, 56, "测树高", 13, DARK, anchor="middle", weight="bold")
    gy = 300
    f.line(30, gy, 250, gy, DARK, 2.0)                      # 地面
    f.line(210, gy, 210, 110, GRN, 3.0)                     # 树
    f.text(222, 150, "树", 11, GRN)
    E = (60, gy - 26)                                       # 眼睛
    f.line(30, E[1], 250, E[1], GREY, 1.2, dash="5 4")      # 视平线
    f.text(34, E[1] - 6, "视平线", 10, GREY)
    f.line(E[0], E[1], 210, 110, RED, 2.0)                  # 视线
    f.arc(E[0], E[1], 46, -30, 0, RED, 2.0)
    f.text(E[0] + 58, E[1] - 6, "α", 12, RED, anchor="middle", weight="bold")
    f.dot(E[0], E[1])
    f.text(88, 292, "眼睛", 10, DARK, anchor="middle")
    f.line(E[0], gy, 210, gy, BLUE, 1.6, dash="4 3")        # 水平距离 b
    f.text(135, gy + 16, "b", 12, BLUE, anchor="middle", weight="bold")
    f.line(E[0], E[1], E[0], gy, BLUE, 1.6, dash="4 3")     # 眼睛高 e
    f.text(E[0] - 14, (E[1] + gy) / 2, "e", 11, BLUE, anchor="middle")
    f.text(214, (gy + 110) / 2, "h", 12, GRN, anchor="middle", weight="bold")
    f.text(130, 336, "h = b·tan α + e", 13, RED, anchor="middle", weight="bold")
    f.line(258, 60, 258, 320, GREY, 1.0)
    # ── 中格：测山高（山顶在山脚落点正上方）──
    f.text(400, 56, "测山高", 13, DARK, anchor="middle", weight="bold")
    P, C, T = (300, 260), (500, 300), (500, 96)
    f.line(270, 300, 540, 300, DARK, 1.8)                   # 地面
    f.line(T[0], T[1], C[0], C[1], GRN, 3.0)                # 山体
    f.line(T[0], T[1], 452, 300, GRN, 2.0)                  # 山另一侧
    f.text(436, 252, "山", 11, GRN)
    f.line(P[0], P[1], T[0], T[1], RED, 2.0)                # 视线（山顶）
    f.line(P[0], P[1], C[0], C[1], BLUE, 2.0)               # 视线（山脚落点）
    f.line(280, P[1], 520, P[1], GREY, 1.2, dash="5 4")     # 水平线
    aA = math.degrees(math.atan2(T[1] - P[1], T[0] - P[0]))
    f.arc(P[0], P[1], 42, aA, 0, RED, 2.0)
    f.text(P[0] + 54, P[1] - 10, "α", 12, RED, anchor="middle", weight="bold")
    aC = math.degrees(math.atan2(C[1] - P[1], C[0] - P[0]))
    f.arc(P[0], P[1], 42, 0, aC, BLUE, 2.0)
    f.text(P[0] + 56, P[1] + 22, "β", 12, BLUE, anchor="middle", weight="bold")
    f.dot(P[0], P[1]); f.text(P[0] - 14, P[1] + 18, "P", 11, DARK, anchor="middle")
    f.text(400, P[1] - 8, "d", 11, DARK, anchor="middle")
    f.text(C[0] + 14, 196, "H", 12, GRN, anchor="middle", weight="bold")
    f.text(400, 336, "H = d·(tan α + tan β)", 13, RED, anchor="middle", weight="bold")
    f.line(528, 60, 528, 320, GREY, 1.0)
    # ── 右格：坡角与坡度 ──
    f.text(670, 56, "坡角与坡度", 13, DARK, anchor="middle", weight="bold")
    O2 = (585, 230)
    f.line(540, 230, 760, 230, DARK, 2.0)
    f.line(O2[0], O2[1], 720, 128, GREY, 3.0)               # 坡面
    f.line(O2[0], O2[1], O2[0], 128, BLUE, 2.4)             # 铅直
    f.arc(O2[0], O2[1], 48, -34, 0, RED, 2.2)
    f.text(O2[0] + 60, O2[1] - 10, "α", 13, RED, anchor="middle", weight="bold")
    f.text(O2[0] - 14, O2[1] + 18, "O", 12, DARK, anchor="middle")
    f.text(660, 168, "l", 12, GREY, anchor="middle", weight="bold")
    f.text(569, 180, "h", 12, BLUE, anchor="middle", weight="bold")
    f.text(660, 252, "b", 12, DARK, anchor="middle", weight="bold")
    f.text(536, 222, "地面", 11, GREY)
    f.text(650, 282, "i = h / b = tan α", 13, RED, anchor="middle", weight="bold")
    f.text(650, 306, "坡度 i 就是坡角的正切", 11, GREY, anchor="middle")
    f.text(650, 330, "i = 0.75 → 3 : 4 : 5", 12, DARK, anchor="middle")
    f.save("trig-applications.svg")



def fig_data_collection():
    f = Fig(740, 360)
    f.text(24, 28, "普查与抽样调查：总体里的每个个体，和抽出来的那一部分", 15, DARK, weight="bold")
    # ── 左：普查 ──
    f.text(185, 60, "普查：每一个都查", 13, DARK, anchor="middle", weight="bold")
    f.rect(50, 78, 270, 170, "none", DARK, 1.8)
    f.text(56, 94, "总体：全校 1200 名学生", 11, GREY)
    for r in range(4):
        for c in range(12):
            x, y = 72 + c * 20, 118 + r * 30
            f.dot(x, y, GREYM, 2.6)
    for (dx, dy) in [(0, 0), (1, 0), (0, 1)]:
        x, y = 72 + (2 + dx) * 20, 118 + dy * 30
        f.dot(x, y, RED, 4.2)
    f.text(185, 268, "三个红点代表「一个不漏地问」——问遍 1200 人", 11, RED, anchor="middle")
    f.text(185, 290, "结论精确，但费时费钱", 11, GREY, anchor="middle")
    # ── 右：抽样 ──
    f.text(470, 60, "抽样调查：抽一部分", 13, DARK, anchor="middle", weight="bold")
    f.rect(340, 78, 250, 170, "none", DARK, 1.8)
    f.text(346, 94, "总体：全校 1200 名学生", 11, GREY)
    for r in range(4):
        for c in range(10):
            x, y = 360 + c * 22, 118 + r * 30
            f.dot(x, y, GREYM, 2.6)
    picked = [(0, 0), (3, 1), (5, 0), (7, 2), (2, 3)]
    for (c, r) in picked:
        x, y = 360 + c * 22, 118 + r * 30
        f.dot(x, y, GRN, 4.2)
        f.line(x, y, 618, 118, GRN, 1.0, dash="3 3")
    f.rect(618, 96, 104, 96, GRNF, GRN, 1.8)
    f.text(670, 128, "样本", 13, GRN, anchor="middle", weight="bold")
    f.text(670, 152, "50 人", 13, GRN, anchor="middle", weight="bold")
    f.text(670, 176, "样本容量 = 50", 10, GREY, anchor="middle")
    f.text(470, 268, "五个绿点代表随机抽到的 50 人", 11, GRN, anchor="middle")
    f.text(470, 290, "便宜快速，但结论是估计值", 11, GREY, anchor="middle")
    f.text(370, 330, "抽样要成立靠三条：随机 · 有代表性 · 样本量足够", 12, DARK, weight="bold")
    f.save("data-collection.svg")


def fig_statistical_charts():
    f = Fig(780, 340)
    f.text(24, 28, "三种统计图各管一件事", 15, DARK, weight="bold")
    # ── 条形图 ──
    f.text(140, 56, "条形图：比多少", 12, DARK, anchor="middle", weight="bold")
    ox, oy = 60, 280
    f.line(ox, 40, ox, oy, DARK, 1.6)
    f.line(ox, oy, 240, oy, DARK, 1.6)
    for v in (4, 8, 12, 16):
        y = oy - v * 11.5
        f.line(ox - 4, y, ox, y, GREYM, 1.0)
        f.text(ox - 8, y + 4, str(v), 9, GREY, anchor="end")
    data = [("篮球", 16), ("足球", 10), ("乒乓", 8), ("其他", 6)]
    for i, (name, v) in enumerate(data):
        x = ox + 22 + i * 40
        h = v * 11.5
        f.rect(x, oy - h, 26, h, BLUEF, BLUE, 1.8)
        f.text(x + 13, oy - h - 6, str(v), 11, BLUE, anchor="middle", weight="bold")
        f.text(x + 13, oy + 16, name, 10, DARK, anchor="middle")
    f.text(26, 160, "人数", 10, GREY)
    f.text(140, 316, "纵轴必须从 0 起", 10, RED, anchor="middle")
    f.line(258, 40, 258, 320, GREY, 1.0)
    # ── 折线图 ──
    f.text(400, 56, "折线图：看变化", 12, DARK, anchor="middle", weight="bold")
    ox2, oy2 = 300, 280
    f.line(ox2, 60, ox2, oy2, DARK, 1.6)
    f.line(ox2, oy2, 490, oy2, DARK, 1.6)
    pts = [(1, 2), (2, 6), (3, 11), (4, 17), (5, 22), (6, 26)]
    xy = [(ox2 + 24 + (i) * 30, oy2 - v * 8) for i, (m, v) in enumerate(pts)]
    for i in range(len(xy) - 1):
        f.line(xy[i][0], xy[i][1], xy[i + 1][0], xy[i + 1][1], RED, 2.0)
    for (x, y), (m, v) in zip(xy, pts):
        f.dot(x, y, RED, 3.2)
        f.text(x, oy2 + 16, f"{m}月", 9, DARK, anchor="middle")
        f.text(x + 9, y - 11, str(v), 9, RED)
    f.text(292, 60, "气温", 10, GREY)
    f.text(400, 316, "横轴是连续变化的时间", 10, RED, anchor="middle")
    f.line(508, 40, 508, 320, GREY, 1.0)
    # ── 扇形图 ──
    f.text(650, 56, "扇形图：看占比", 12, DARK, anchor="middle", weight="bold")
    cx, cy, r = 640, 175, 78
    segs = [("篮球", 144), ("足球", 90), ("乒乓", 72), ("其他", 54)]
    a0 = -90.0
    for i, (name, ang) in enumerate(segs):
        a1 = a0 + ang
        poly_pts = [(cx, cy)]
        steps = max(4, int(ang / 8))
        for k in range(steps + 1):
            a = math.radians(a0 + ang * k / steps)
            poly_pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        f.poly(poly_pts, [BLUEF, REDF, GRNF, YELF][i], [BLUE, RED, GRN, YEL][i], 1.6)
        amid = math.radians(a0 + ang / 2)
        lx, ly = cx + (r + 26) * math.cos(amid), cy + (r + 26) * math.sin(amid)
        f.text(lx, ly, f"{name}\n{ang}°", 10, [BLUE, RED, GRN, YEL][i], anchor="middle")
        a0 = a1
    f.text(650, 316, "圆心角 = 360° × 百分比", 10, RED, anchor="middle")
    f.save("statistical-charts.svg")


def fig_central_tendency():
    f = Fig(720, 330)
    f.text(24, 28, "同一组数据的三个代表数", 15, DARK, weight="bold")
    x0, x1, y = 90, 650, 205

    def X(v):
        return x0 + (v - 2) / 8 * (x1 - x0)

    f.line(x0 - 20, y, x1 + 30, y, DARK, 2.0)
    for v in (2, 4, 6, 8, 10):
        f.line(X(v), y - 6, X(v), y + 6, DARK, 1.4)
        f.text(X(v), y + 26, str(v), 11, DARK, anchor="middle")
    f.text(x1 + 40, y + 4, "数据", 11, GREY)
    for v, dy in [(2, 0), (4, -18), (4, 18), (6, 0), (10, 0)]:
        f.dot(X(v), y + dy, PURP, 5.0)
    f.text(X(2) - 14, y - 12, "2", 11, PURP, anchor="end")
    f.text(X(10) + 14, y - 12, "10", 11, PURP, anchor="start")
    # 众数 4
    f.line(X(4), y - 44, X(4), y - 26, GRN, 1.8)
    f.text(X(4), y - 58, "众数 = 4", 12, GRN, anchor="middle", weight="bold")
    f.text(X(4), y - 76, "出现次数最多（3 次）", 10, GREY, anchor="middle")
    # 中位数 4（5 个数取正中间）
    f.line(X(4), y + 44, X(4), y + 26, BLUE, 1.8)
    f.text(X(4), y + 62, "中位数 = 4", 12, BLUE, anchor="middle", weight="bold")
    f.text(X(4), y + 80, "排序后正中间那个", 10, GREY, anchor="middle")
    # 平均数 5.2
    xa = X(5.2)
    f.line(xa, y + 44, xa, y + 26, RED, 1.8)
    f.text(xa + 14, y + 62, "平均数 = 5.2", 12, RED, anchor="middle", weight="bold")
    f.text(xa + 14, y + 80, "被 10 这个极端值拉偏", 10, GREY, anchor="middle")
    f.text(360, 128, "数据：2、4、4、6、10", 12, DARK, anchor="middle")
    f.text(360, 306, "极端值 10 把平均数拉走，中位数与众数分毫未动", 12, DARK, anchor="middle", weight="bold")
    f.save("central-tendency.svg")


def fig_variance():
    f = Fig(720, 400)
    f.text(24, 28, "平均数几乎相同，稳定性却天差地别", 15, DARK, weight="bold")
    rows = [
        # 标题, 刻度下限, 刻度上限, 刻度, 平均数, 方差, 标准差, 多数数据值, 多数次数, 少数数据值
        ("甲：10 次射击，9 环 9 次、7 环 1 次", 7, 9, (7, 8, 9), 8.8, "0.36", "0.6", 9, 9, 7),
        ("乙：10 次射击，10 环 9 次、0 环 1 次", 0, 10, (0, 2, 4, 6, 8, 10), 9, "9", "3", 10, 9, 0),
    ]
    for idx, (title, lo, hi, ticks, mean, var, sd, big, cnt, small) in enumerate(rows):
        y0 = 120 + idx * 155
        f.text(40, y0 - 46, title, 12, DARK, weight="bold")
        x0, x1 = 130, 630

        def X(v, lo=lo, hi=hi, x0=x0, x1=x1):
            return x0 + (v - lo) / (hi - lo) * (x1 - x0)

        f.line(x0 - 30, y0, x1 + 40, y0, DARK, 2.0)
        for v in ticks:
            f.line(X(v), y0 - 5, X(v), y0 + 5, GREYM, 1.2)
            f.text(X(v), y0 + 24, str(v), 10, GREY, anchor="middle")
        # 多数数据叠在 big 处，用微小偏移表示「多次」
        for k in range(cnt):
            f.dot(X(big) + (k % 3 - 1) * 5, y0 - 18 + (k // 3 - 1) * 5, PURP, 4.0)
        f.dot(X(small), y0 - 18, PURP, 4.8)
        xm = X(mean)
        f.line(xm, y0 - 38, xm, y0 + 16, RED, 1.6, dash="4 3")
        f.text(xm, y0 - 48, f"平均数 {mean}", 10, RED, anchor="middle")
        f.text(360, y0 + 52, f"方差 {var}，标准差 {sd}", 11, DARK, anchor="middle")
    f.text(360, 372, "点越聚在平均数附近，方差越小；乙有一次 0 环，波动被放大到 25 倍", 12, DARK, anchor="middle", weight="bold")
    f.save("variance.svg")



def fig_sample_estimation():
    f = Fig(740, 330)
    f.text(24, 28, "用样本估计总体：从抽出来的那一部分，推断全体", 15, DARK, weight="bold")
    # 左：抽样
    f.text(160, 62, "第一步：抽样", 13, DARK, anchor="middle", weight="bold")
    f.rect(45, 82, 230, 150, "none", DARK, 1.8)
    f.text(52, 100, "总体：全校 800 名学生", 11, GREY)
    for r in range(3):
        for c in range(9):
            f.dot(66 + c * 22, 124 + r * 32, GREYM, 2.6)
    for (c, r) in [(0, 0), (3, 1), (5, 0), (7, 2), (2, 2), (6, 1)]:
        x, y = 66 + c * 22, 124 + r * 32
        f.dot(x, y, GRN, 4.2)
        f.line(x, y, 240, 160, GRN, 1.0, dash="3 3")
    f.rect(240, 132, 108, 74, GRNF, GRN, 1.8)
    f.text(294, 156, "样本 100 人", 12, GRN, anchor="middle", weight="bold")
    f.text(294, 176, "平均 35 分钟", 11, GRN, anchor="middle")
    f.text(294, 196, "样本平均数", 10, GREY, anchor="middle")
    f.text(160, 262, "样本的统计量", 12, GRN, anchor="middle", weight="bold")
    # 箭头
    f.arrow_line(360, 160, 434, 160, DARK, 2.6)
    f.text(397, 142, "估计", 12, DARK, anchor="middle", weight="bold")
    # 右：估计
    f.text(590, 62, "第二步：推断全体", 13, DARK, anchor="middle", weight="bold")
    f.rect(452, 82, 250, 150, "none", DARK, 1.8)
    f.text(459, 100, "总体：全校 800 名学生", 11, GREY)
    f.rect(472, 120, 210, 44, BLUEF, BLUE, 1.8)
    f.text(577, 147, "估计：平均阅读时间 ≈ 35 分钟", 12, BLUE, anchor="middle", weight="bold")
    f.text(577, 186, "估计值 ≠ 真值，存在抽样误差", 11, RED, anchor="middle")
    f.text(577, 208, "加「约」是诚实，不是含糊", 10, GREY, anchor="middle")
    f.text(590, 262, "总体的估计值", 12, BLUE, anchor="middle", weight="bold")
    f.text(370, 306, "抽样方法随机且有代表性 → 无系统性偏差；样本容量足够 → 偶然波动小", 12, DARK, anchor="middle", weight="bold")
    f.save("sample-estimation.svg")


def fig_events_probability():
    f = Fig(740, 330)
    f.text(24, 28, "三类事件与概率这把尺子", 15, DARK, weight="bold")
    boxes = [
        ("必然事件", "太阳从东方升起", "P = 1", GRNF, GRN, 45),
        ("不可能事件", "石头从天上掉下来", "P = 0", REDF, RED, 265),
        ("随机事件", "掷一枚骰子的点数", "0 < P < 1", BLUEF, BLUE, 485),
    ]
    for title, body, val, fill, stroke, bx in boxes:
        f.rect(bx, 70, 210, 120, fill, stroke, 1.8)
        f.text(bx + 105, 96, title, 13, stroke, anchor="middle", weight="bold")
        f.text(bx + 105, 126, body, 11, DARK, anchor="middle")
        f.text(bx + 105, 168, val, 14, stroke, anchor="middle", weight="bold")
    # 概率标度条
    f.text(370, 226, "概率：可能性大小的刻度", 12, DARK, anchor="middle", weight="bold")
    x0, x1, y = 90, 650, 262
    f.line(x0, y, x1, y, DARK, 3.0)
    for v, lab in [(x0, "0"), (x1, "1")]:
        f.line(v, y - 8, v, y + 8, DARK, 2.0)
    f.text(x0, y + 26, "0 · 一定不会发生", 11, GREY, anchor="middle")
    f.text(x1, y + 26, "1 · 一定会发生", 11, GREY, anchor="middle")
    xa = x0 + (x1 - x0) * 0.42
    f.line(xa, y - 26, xa, y + 8, RED, 2.4)
    f.text(xa, y - 36, "P(A)", 13, RED, anchor="middle", weight="bold")
    f.text(370, y + 48, "前提：结果总数有限，且每种结果出现的机会均等", 11, DARK, anchor="middle")
    f.save("events-probability.svg")


def fig_frequency_estimate():
    f = Fig(760, 350)
    f.text(24, 28, "频率随试验次数增加而稳定在概率附近", 15, DARK, weight="bold")
    # 左：频率折线
    ox, oy = 80, 270
    f.line(ox, 60, ox, oy, DARK, 1.6)
    f.line(ox, oy, 470, oy, DARK, 1.6)
    for lab, v in [("0.6", 0.6), ("0.5", 0.5), ("0.4", 0.4)]:
        y = oy - v * 320
        f.line(ox - 4, y, ox, y, GREYM, 1.0)
        f.text(ox - 8, y + 4, lab, 9, GREY, anchor="end")
    f.text(ox - 30, 200, "频率", 10, GREY)
    f.line(ox, oy - 0.5 * 320, 470, oy - 0.5 * 320, RED, 1.4, dash="5 4")
    f.text(452, oy - 0.5 * 320 - 8, "P = 0.5", 11, RED, anchor="end", weight="bold")
    seq = [0.7, 0.4, 0.6, 0.5, 0.45, 0.55, 0.5, 0.5, 0.5, 0.48, 0.52, 0.5]
    px = [ox + 30 + i * 30 for i in range(len(seq))]
    py = [oy - v * 320 for v in seq]
    for i in range(len(px) - 1):
        f.line(px[i], py[i], px[i + 1], py[i + 1], BLUE, 1.8)
    for x, y in zip(px, py):
        f.dot(x, y, BLUE, 2.8)
    f.text(275, oy + 22, "试验次数 →（越多越稳）", 10, DARK, anchor="middle")
    f.text(275, 316, "次数少时频率乱跳，次数多时收紧在 P 附近", 10, BLUE, anchor="middle")
    f.line(500, 50, 500, 320, GREY, 1.0)
    # 右：模拟试验
    f.text(630, 56, "模拟试验：转盘代替摸球", 12, DARK, anchor="middle", weight="bold")
    cx, cy, r = 585, 160, 68
    f.circle(cx, cy, r, "none", DARK, 2.0)
    for k in range(8):
        a0 = math.radians(-90 + k * 45)
        a1 = math.radians(-90 + (k + 1) * 45)
        pts = [(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)),
               (cx + r * math.cos(a1), cy + r * math.sin(a1))]
        f.poly(pts, REDF if k == 0 else "none", RED if k == 0 else GREY, 1.6 if k == 0 else 1.0)
    f.text(cx + r * 0.5, cy - r * 0.5, "红区", 10, RED, anchor="middle")
    f.text(585, 250, "8 等份，1 份为红", 10, GREY, anchor="middle")
    f.text(630, 278, "转 200 次，红区停了 26 次", 11, DARK, anchor="middle")
    f.text(630, 298, "频率 26/200 = 0.13", 12, RED, anchor="middle", weight="bold")
    f.text(630, 318, "于是估计 P ≈ 0.13", 11, DARK, anchor="middle")
    f.save("frequency-estimate.svg")


if __name__ == "__main__":
    fig_lines()
    fig_angle()
    fig_parallel()
    fig_counterexample()
    fig_construction()
    fig_models()
    fig_isosceles()
    fig_pythagoras()
    fig_midline()
    fig_polygon()
    fig_parallelogram()
    fig_special()
    fig_trapezoid()
    fig_circle_perp()
    fig_central_inscribed()
    fig_circle_position()
    fig_tangent()
    fig_arc_cone()
    fig_regular_poly()
    fig_prop_segments()
    fig_similar_tri()
    fig_similar_models()
    fig_homothety()
    fig_projection_views()
    fig_symmetry()
    fig_translation_rotation()
    fig_transform_coords()
    fig_geometric_extremum()
    fig_trig_ratios()
    fig_right_triangle()
    fig_trig_applications()
    fig_data_collection()
    fig_statistical_charts()
    fig_central_tendency()
    fig_variance()
    fig_sample_estimation()
    fig_events_probability()
    fig_frequency_estimate()
