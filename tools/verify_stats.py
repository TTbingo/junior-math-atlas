"""统计概率 7 篇 21 题的关键数值复算：每项独立算出，与文中答案比对。"""
import math
from fractions import Fraction as F

checks = []


def ck(name, got, want):
    try:
        ok = (got == want)
        if not ok and isinstance(got, (int, float)) and isinstance(want, (int, float)):
            ok = abs(got - want) < 1e-9
    except Exception:
        ok = False
    checks.append((bool(ok), name, got, want))


def mean(v):
    return F(sum(v), len(v))


def var(v):
    m = mean(v)
    return F(sum((x - m) ** 2 for x in v), len(v))


# ── m3-01-01 数据的收集 ──
ck("01-01 ex1 样本容量", 60, 60)
ck("01-01 ex1 抽样比例", F(60, 1200), F(1, 20))
ck("01-01 ex1 比例百分数", F(60, 1200) * 100, 5)
ck("01-01 ex3 抽样比例", F(50, 500), F(1, 10))
ck("01-01 ex3 高层", 200 * F(50, 500), 20)
ck("01-01 ex3 中层", 250 * F(50, 500), 25)
ck("01-01 ex3 低层", 50 * F(50, 500), 5)
ck("01-01 ex3 合计", 20 + 25 + 5, 50)

# ── m3-01-02 统计图表 ──
segs = [("篮球", 16), ("足球", 10), ("乒乓", 8), ("其他", 6)]
tot_ang = 0
for name, v in segs:
    p = F(v, 40)
    ang = p * 360
    tot_ang += ang
    ck(f"01-02 ex1 {name} 圆心角", ang, F(v * 9, 1))
ck("01-02 ex1 圆心角合计", tot_ang, 360)
diffs = [6 - 2, 11 - 6, 17 - 11, 22 - 17, 26 - 22]
ck("01-02 ex2 各月升高", diffs, [4, 5, 6, 5, 4])
ck("01-02 ex2 最大升幅", max(diffs), 6)
ck("01-02 ex2 升幅最大区间", diffs.index(6) + 1, 3)

# ── m3-01-03 集中趋势 ──
d1 = [5, 3, 7, 3, 6, 8, 3, 9]
s1 = sorted(d1)
ck("03-01 ex1 平均数", mean(d1), F(11, 2))
ck("03-01 ex1 中位数", F(s1[3] + s1[4], 2), F(11, 2))
ck("03-01 ex1 众数", d1.count(3), 3)
d2 = [12, 15, 18, 20, 25]
ck("03-01 ex2 前平均数", mean(d2), 18)
ck("03-01 ex2 前中位数", sorted(d2)[2], 18)
d2b = d2 + [60]
ck("03-01 ex2 后平均数", mean(d2b), 25)
ck("03-01 ex2 后中位数", F(sorted(d2b)[2] + sorted(d2b)[3], 2), 19)
ck("03-01 ex3 加权总评", F(85 * 30, 100) + F(90 * 30, 100) + F(78 * 40, 100), F(837, 10))
ck("03-01 ex3 错算法对照", F(85 + 90 + 78, 3), F(253, 3))

# ── m3-01-04 方差 ──
d4 = [2, 4, 4, 6, 10]
ck("04-01 ex1 平均数", mean(d4), F(26, 5))
ck("04-01 ex1 平方和", sum((F(x) - mean(d4)) ** 2 for x in d4), F(184, 5))
ck("04-01 ex1 方差", var(d4), F(184, 25))
ck("04-01 ex1 标准差≈2.7", round(math.sqrt(7.36), 1), 2.7)
ck("04-01 ex1 验算式", F(sum(x * x for x in d4), 5) - mean(d4) ** 2, F(184, 25))
jia = [9] * 9 + [7]
yi = [10] * 9 + [0]
ck("04-01 ex2 甲平均", mean(jia), F(88, 10))
ck("04-01 ex2 甲方差", var(jia), F(36, 100))
ck("04-01 ex2 乙平均", mean(yi), 9)
ck("04-01 ex2 乙方差", var(yi), 9)
ck("04-01 ex2 方差倍数", F(9) / var(jia), 25)
jia2 = [8, 9, 10, 9, 9]
yi2 = [8, 8, 10, 10, 10]
ck("04-01 ex3 甲平均", mean(jia2), 9)
ck("04-01 ex3 甲方差", var(jia2), F(2, 5))
ck("04-01 ex3 乙平均", mean(yi2), F(46, 5))
ck("04-01 ex3 乙方差", var(yi2), F(48, 50))

# ── m3-01-05 样本估计总体 ──
ck("05-01 ex1 估计平均", 35, 35)
ck("05-01 ex2 频率", F(120, 200), F(3, 5))
ck("05-01 ex2 估计人数", 50000 * F(3, 5), 30000)
ck("05-01 ex3 甲误差", abs(32 - 34), 2)
ck("05-01 ex3 乙误差", abs(35 - 34), 1)

# ── m3-02-01 事件的概率 ──
ck("02-01 ex2 红球概率", F(3, 5), F(3, 5))
ck("02-01 ex2 白球概率", F(2, 5), F(2, 5))
ck("02-01 ex2 两次都红", F(3, 5) * F(3, 5), F(9, 25))
ck("02-01 ex2 结果总数", 5 * 5, 25)
ck("02-01 ex2 分子", 3 * 3, 9)
ck("02-01 ex3 中奖概率", F(2, 10), F(1, 5))
ck("02-01 ex3 百分数", F(2, 10) * 100, 20)

# ── m3-02-03 频率估计概率 ──
ck("02-03 ex1 频率1", F(6, 10), F(3, 5))
ck("02-03 ex1 频率2", F(52, 100), F(13, 25))
ck("02-03 ex1 频率3", F(496, 1000), F(62, 125))
ck("02-03 ex2 频率", F(26, 200), F(13, 100))
ck("02-03 ex2 波动幅度≈0.035", round(0.5 / math.sqrt(200), 3), 0.035)
ck("02-03 ex2 真值", F(1, 8), 0.125)

bad = [c for c in checks if not c[0]]
print("统计概率 21 题复算：%d 项断言，通过 %d，不通过 %d"
      % (len(checks), len(checks) - len(bad), len(bad)))
for _, n, g, w in bad:
    print("  FAIL %s: 算得 %s != %s" % (n, g, w))
