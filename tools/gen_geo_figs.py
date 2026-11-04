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
