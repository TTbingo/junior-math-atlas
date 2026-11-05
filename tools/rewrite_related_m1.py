"""全站 related 三类化：前置 / 后续 / 常一起考。

判定规则（逐条人工判定，不是模板套用）：
- 前置：学本文之前必须先会的概念或工具 —— 目标排在本篇之前，且是该结论的前提
- 后续：学完本文之后，接着会用到本文成果的篇目 —— 目标排在本篇之后，且直接建立在本文之上
- 常一起考：中考里常与本文出现在同一道题里的篇目 —— 多为跨领域的对照或同源

每条的 note 保留原有内容并补上「为什么是这一类」的说明。
"""
import json
import pathlib

C = pathlib.Path(__file__).resolve().parent.parent / "content" / "points"

# pid -> [(target_id, kind, note)]
PLAN = {
    # ==================== 代数 m1-01 ====================
    "m1-01-01-real-numbers": [
        ("m1-01-02-integral-expressions", "后续",
         "实数的运算律（交换律、结合律、分配律）搬到字母上，就是整式的加减乘；本篇是整式运算的地基"),
        ("m1-01-05-quadratic-radicals", "后续",
         "把开方运算整理成二次根式的化简规则，是运算律在根式上的延伸"),
        ("m1-01-04-algebraic-fractions", "后续",
         "分式要求分母不为零，与本篇「零没有倒数」是同一条限制；分式是运算律的又一次搬家"),
        ("m2-02-05-pythagoras", "常一起考",
         "勾股定理算出斜边长常常是无理数，必须用二次根式表示——几何题与本篇的根式化简同场出现"),
    ],
    "m1-01-02-integral-expressions": [
        ("m1-01-01-real-numbers", "前置",
         "整式的运算律直接来自实数的运算律，不先有实数运算律就没法说「去括号法则」"),
        ("m1-01-03-factorization", "后续",
         "乘法把积展开成和，因式分解把和收成积，两条路要能来回走"),
        ("m1-01-04-algebraic-fractions", "后续",
         "约分与通分要靠整式乘法与因式分解把分子分母拆开，整式运算在这里变成工具"),
        ("m1-02-03-quadratic-equation", "后续",
         "一元二次方程的配方法，就是反过来用完全平方公式展开——同一个公式两个方向用"),
        ("m2-03-04-trapezoid", "常一起考",
         "化简含字母的代数式（如 $a+(b-a)$）常在几何面积公式里出现；面积公式化简题与整式运算同考"),
    ],
    "m1-01-03-factorization": [
        ("m1-01-02-integral-expressions", "前置",
         "因式分解是把「和」收成「积」，得先会整式的乘法与展开"),
        ("m1-01-04-algebraic-fractions", "后续",
         "分式约分的第一步就是把分子分母各自分解，找出公因式——本篇是分式运算的开路工具"),
        ("m1-02-03-quadratic-equation", "后续",
         "一元二次方程降次求解，靠因式分解把二次式拆成两个一次因式的积等于零"),
        ("m1-02-04-discriminant-vieta", "后续",
         "二次三项式能否分解成两个一次因式，取决于判别式是否为完全平方数"),
        ("m2-05-03-similar-models", "常一起考",
         "几何里「比例线段」要先用字母设出各段长再列式，列出的式子往往要靠因式分解化简；代数与几何在综合题里合流"),
    ],
    "m1-01-04-algebraic-fractions": [
        ("m1-01-02-integral-expressions", "前置",
         "分式的分子分母都是整式，运算律来自整式"),
        ("m1-01-03-factorization", "前置",
         "约分要找出分子分母的公因式，这一步就是因式分解"),
        ("m1-01-05-quadratic-radicals", "常一起考",
         "分式的分母有理化与根式的分母有理化是同一套「同乘共轭」思路"),
        ("m1-02-05-fractional-equation", "后续",
         "分式方程去分母后必须检验，正是因为分母不能为零——本篇的限制直接决定了后续的解法"),
        ("m1-03-04-inverse-proportion", "常一起考",
         "反比例函数 $y=\\dfrac{k}{x}$ 就是分式，两者的定义域限制完全同源"),
    ],
    "m1-01-05-quadratic-radicals": [
        ("m1-01-01-real-numbers", "前置",
         "算术平方根是实数范围内的运算，没有实数概念就谈不上「平方根有意义」"),
        ("m1-01-03-factorization", "前置",
         "根式化简常要用因式分解配平方，如 $\\sqrt{a^2-2a+1}$"),
        ("m1-02-03-quadratic-equation", "后续",
         "求根公式里的根号要先化简，才能把两根写成最简形式"),
        ("m1-02-04-discriminant-vieta", "后续",
         "判别式 $\\sqrt{b^{2}-4ac}$ 是否存在、是否开得尽，决定了根的性质"),
        ("m2-02-05-pythagoras", "常一起考",
         "勾股定理求斜边或直角边，结果几乎都是二次根式，必须化简——几何计算题几乎每题都要用根式化简"),
    ],
    # ==================== 代数 m1-02 ====================
    "m1-02-01-linear-equation": [
        ("m1-01-02-integral-expressions", "前置",
         "解方程要先去括号、合并同类项，用的都是整式运算"),
        ("m1-02-02-linear-system", "后续",
         "两个未知数要两个方程，解法仍靠等式性质，只是先消去一个未知数"),
        ("m1-02-06-inequality", "后续",
         "不等式也有类似的三条性质，但两边乘除负数时不等号方向要反转——学完方程再学不等式，性质成对出现"),
        ("m1-02-07-equation-word-problems", "后续",
         "把实际问题的等量关系翻译成方程，本篇的解法是它的工具"),
    ],
    "m1-02-02-linear-system": [
        ("m1-02-01-linear-equation", "前置",
         "消元法每次消元后得到的就是一个一元一次方程，解法完全一致"),
        ("m1-02-07-equation-word-problems", "后续",
         "两个未知量、两条条件的应用题，列的就是方程组"),
        ("m1-02-06-inequality", "后续",
         "不等式组同样是两条条件的交集，但解集是一个范围而不是一个点——两者的解法结构对应"),
        ("m1-03-01-coordinates-and-function", "常一起考",
         "方程组的解就是两条直线交点坐标；代数解法与图象法在中考里常常各占一问"),
    ],
    "m1-02-03-quadratic-equation": [
        ("m1-01-03-factorization", "前置",
         "因式分解法是解一元二次方程的基本方法之一"),
        ("m1-01-05-quadratic-radicals", "前置",
         "配方法与公式法都要用到二次根式的化简"),
        ("m1-02-04-discriminant-vieta", "后续",
         "不解方程也能判断根的个数，还能直接读出两根之和与积"),
        ("m1-03-06-quadratic-function-equation", "后续",
         "方程的根就是抛物线与 x 轴交点的横坐标——同一个根换一种看法就是图象上的交点"),
        ("m1-02-07-equation-word-problems", "后续",
         "面积、增长率类应用题列出的常是二次方程，解完要按实际取舍"),
    ],
    "m1-02-04-discriminant-vieta": [
        ("m1-02-03-quadratic-equation", "前置",
         "判别式是对一元二次方程根的判别，脱离方程本身无从谈起"),
        ("m1-01-03-factorization", "前置",
         "「能否分解成两个一次因式」与「判别式是否为完全平方数」是同一件事的两种说法，必须先会因式分解才看得出这个等价"),
        ("m1-03-06-quadratic-function-equation", "后续",
         "判别式就是抛物线与 x 轴交点的个数，韦达定理对应两交点横坐标的和与积"),
        ("m1-03-05-quadratic-function", "后续",
         "二次函数与坐标轴交点、顶点位置都要靠判别式判断"),
    ],
    "m1-02-05-fractional-equation": [
        ("m1-01-04-algebraic-fractions", "前置",
         "解分式方程的第一步是去分母，而去分母的依据就是分式的运算规则"),
        ("m1-02-07-equation-word-problems", "后续",
         "工程、行程、销售中的单位量问题，列出的常是分式方程"),
        ("m1-02-08-inequality-applications", "常一起考",
         "不等式应用题同样要按实际意义取舍，但取舍的是范围端点而非增根——两类题都考「解完要检验」"),
        ("m1-03-04-inverse-proportion", "常一起考",
         "反比例函数 $y=\\dfrac{k}{x}$ 的定义域也是「分母不为零」，取值限制同源"),
    ],
    "m1-02-06-inequality": [
        ("m1-02-01-linear-equation", "前置",
         "不等式的三条基本性质与等式的变形性质一一对应，等式基础在前"),
        ("m1-02-08-inequality-applications", "后续",
         "方案决策题要把「至多」「至少」翻成不等式，再取整数解"),
        ("m1-03-03-linear-function-applications", "后续",
         "$kx+b>0$ 的解集就是直线在 x 轴上方的部分对应的横坐标范围——不等式与图象在此合流"),
        ("m1-02-07-equation-word-problems", "常一起考",
         "应用题的条件给的是等量关系时列方程，给的是范围时列不等式，两者在同一份试卷里常成对出现"),
    ],
    "m1-02-07-equation-word-problems": [
        ("m1-02-01-linear-equation", "前置",
         "列出的方程最终要靠一元一次方程的解法求出，工具在前"),
        ("m1-02-02-linear-system", "前置",
         "两个未知量的应用题列的是方程组"),
        ("m1-02-03-quadratic-equation", "前置",
         "面积与增长率类问题列出的常是二次方程"),
        ("m1-02-08-inequality-applications", "后续",
         "条件给的是范围而不是等值时，把方程换成不等式，其余步骤相同"),
        ("m1-03-03-linear-function-applications", "后续",
         "方案选择问题可以用一次函数建模，与方程解法互为补充"),
        ("m1-02-05-fractional-equation", "常一起考",
         "工程与行程中的单位量问题，列出的常是分式方程，解完要验根——同一种题型可能列三种方程"),
    ],
    "m1-02-08-inequality-applications": [
        ("m1-02-06-inequality", "前置",
         "「至多」「至少」必须先翻成不等式才能求解"),
        ("m1-02-07-equation-word-problems", "前置",
         "取整数解、检验取舍这些步骤与列方程解应用题完全一致"),
        ("m1-03-03-linear-function-applications", "后续",
         "方案比较可用一次函数的增减性直接判断，比逐个数方案更快"),
        ("m1-03-02-linear-function", "常一起考",
         "把总费用写成 $W=kx+b$ 就要先会求一次函数的解析式；一次函数与不等式应用题在中考里常合并成一题"),
    ],
    # ==================== 代数 m1-03 ====================
    "m1-03-01-coordinates-and-function": [
        ("m1-01-01-real-numbers", "前置",
         "函数的概念建立在实数范围上，函数值是有序数对里的那个数"),
        ("m1-03-02-linear-function", "后续",
         "一次函数的图象就是坐标系里的一条直线，$k$ 与 $b$ 各自控制方向与位置"),
        ("m2-06-03-transform-coordinates", "后续",
         "平移、对称、折叠都可以用坐标的变化来描述——坐标系是这些变换的舞台"),
        ("m1-02-02-linear-system", "常一起考",
         "方程组的解对应两条直线的交点坐标；代数解法与图象法在中考里常各占一问"),
        ("m3-01-02-statistical-charts", "常一起考",
         "统计图表就是坐标系里的柱形与折线，横纵轴的读法与函数图象完全一样"),
    ],
    "m1-03-02-linear-function": [
        ("m1-03-01-coordinates-and-function", "前置",
         "一次函数的图象必须画在坐标系里，没有坐标系的语言就说不出「$k$ 决定倾斜方向」"),
        ("m1-03-03-linear-function-applications", "后续",
         "一次函数与方程、不等式的关系，都靠图象上的交点与上下位置读出"),
        ("m1-03-04-inverse-proportion", "后续",
         "反比例函数的图象是双曲线，增减性只在同一支内成立，与直线的全局单调不同——两者对照着学最省力"),
        ("m1-02-07-equation-word-problems", "常一起考",
         "把实际问题中的均匀变化写成一次函数，是建模的入门；同一道应用题可能先列方程再写成函数"),
    ],
    "m1-03-03-linear-function-applications": [
        ("m1-03-02-linear-function", "前置",
         "$k$、$b$ 的几何意义是判断增减与快慢的基础"),
        ("m1-02-06-inequality", "前置",
         "$kx+b>0$ 的解集就是直线在 x 轴上方的部分对应的横坐标范围——不等式基础在前"),
        ("m1-03-04-inverse-proportion", "后续",
         "反比例函数与直线的交点通常有两个，比较大小要分段讨论"),
        ("m1-03-06-quadratic-function-equation", "后续",
         "抛物线与直线的交点、二次不等式的解集，用的是同一套「交点＋上下方」的读图逻辑"),
        ("m1-02-08-inequality-applications", "常一起考",
         "方案决策的不等式解法与本页的函数解法互为验证，结论应一致——两种方法要能互相印证"),
    ],
    "m1-03-04-inverse-proportion": [
        ("m1-03-02-linear-function", "前置",
         "反比例函数的增减性要与一次函数对照着判断，必须先分清直线的全局单调与双曲线的分支单调"),
        ("m1-02-05-fractional-equation", "前置",
         "$y=\\dfrac{k}{x}$ 就是分式，定义域限制 $x\\ne 0$ 与分式方程分母不为零同一条"),
        ("m1-03-05-quadratic-function", "后续",
         "抛物线有一个顶点与对称轴，双曲线有两支，形态与性质都不同——接着学抛物线正好对照"),
        ("m1-03-03-linear-function-applications", "常一起考",
         "反比例与一次函数的交点、上下方区域，是中考综合题的常见组合"),
    ],
    "m1-03-05-quadratic-function": [
        ("m1-03-02-linear-function", "前置",
         "抛物线的开口方向与对称轴要靠与直线的倾斜方向作对照来理解"),
        ("m1-02-03-quadratic-equation", "前置",
         "抛物线与 x 轴的交点横坐标就是方程的根，没有方程就无从说起交点"),
        ("m1-03-06-quadratic-function-equation", "后续",
         "抛物线与 x 轴的交点个数由判别式决定，交点横坐标就是方程的根"),
        ("m1-03-07-quadratic-function-applications", "后续",
         "利润最大、面积最大、动点面积都是先写出二次函数再求顶点"),
        ("m1-02-04-discriminant-vieta", "前置",
         "判断抛物线与 x 轴交点个数，用的就是判别式"),
    ],
    "m1-03-06-quadratic-function-equation": [
        ("m1-03-05-quadratic-function", "前置",
         "抛物线的顶点与对称轴位置决定交点在哪，必须先懂图象"),
        ("m1-02-04-discriminant-vieta", "前置",
         "交点个数就是判别式的符号，韦达定理给出两交点横坐标的和与积"),
        ("m1-03-07-quadratic-function-applications", "后续",
         "求落点、求最大高度，都要先找抛物线与轴的交点或顶点"),
        ("m1-02-03-quadratic-equation", "前置",
         "解一元二次方程的四种方法，是求交点横坐标的工具"),
        ("m1-03-03-linear-function-applications", "常一起考",
         "直线与 x 轴交点对应一次方程，抛物线对应二次方程，读图逻辑一致"),
    ],
    "m1-03-07-quadratic-function-applications": [
        ("m1-03-05-quadratic-function", "前置",
         "求最值就是求顶点，必须先会配方与顶点坐标"),
        ("m1-03-06-quadratic-function-equation", "前置",
         "求交点与轴的交点位置、判交点个数，都要用到方程与图象的关系"),
        ("m2-06-04-geometric-extremum", "常一起考",
         "几何最值用对称与展开，代数最值用顶点，两类题的建模思路可以互借——中考常把两种最值放一道题里对比"),
        ("m1-02-08-inequality-applications", "常一起考",
         "方案题的约束条件（销量非负、长度为正）就是这里的自变量范围"),
        ("m1-03-03-linear-function-applications", "常一起考",
         "线性模型只有一个最优端点，二次模型有内部顶点，这是两类应用题的分界"),
    ],
}


def apply():
    for pid, items in PLAN.items():
        p = C / f"{pid}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        rel = [{"id": tid, "kind": kind, "note": note} for tid, kind, note in items]
        d["sections"]["related"] = rel
        pre = [t for t, k, _ in items if k == "前置"]
        d["prerequisites"] = pre
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        kinds = {}
        for _, k, _ in items:
            kinds[k] = kinds.get(k, 0) + 1
        print(f"{pid}: {kinds}")


apply()
