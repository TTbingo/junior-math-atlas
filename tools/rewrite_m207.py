"""m2-07 三角函数三篇：related 三类化 + 证明板块结论化。

三类含义：
- 前置：学本文之前应当先会的（概念或工具）
- 后续：学完本文之后接着会用到本文成果的
- 常一起考：中考里常与本文出现在同一道题里的

证明板块改为「结论 N + 证明过程 + 关键一步」结构：
- conclusion：这一条证明了什么（命题本身）
- proof：推理过程
- key：这一步凭什么成立（条件、依据）
"""
import json
import pathlib

C = pathlib.Path(__file__).resolve().parent.parent / "content" / "points"

# ---------------------------------------------------------------- 相关三类
RELATED = {
    "m2-07-01-trig-ratios": [
        {"id": "m2-05-02-similar-triangles", "kind": "前置",
         "note": "锐角三角函数的值就是相似三角形里的对应边之比——AA 判定保证「形状相同则对应边成比例」，比值恒定这件事全靠它"},
        {"id": "m2-02-05-pythagoras", "kind": "前置",
         "note": "三个三角函数值都是「两条边之比」，而边长本身要靠勾股定理算；勾股是本节算数的必备工具"},
        {"id": "m2-01-02-angles", "kind": "前置",
         "note": "互余与互补的概念：两个锐角互余时正弦与余弦互换，这是 $30^{\\circ}$ 与 $60^{\\circ}$ 数值对调的依据"},
        {"id": "m2-07-02-solving-right-triangle", "kind": "后续",
         "note": "知道每个角的值之后，下一步是「已知什么求什么」——本节提供工具，解直角三角形篇负责选工具并求解"},
        {"id": "m2-07-03-trig-applications", "kind": "后续",
         "note": "本节的比值拿到真实场景里就是仰角、俯角、坡角——从「会算」到「会测量」的一步"},
        {"id": "m2-05-03-similar-models", "kind": "常一起考",
         "note": "A 字型、母子型里求线段比值时，用的就是本节的三角函数值；同一道题里「相似定比例」和「三角函数定边长」常常同时出现"},
        {"id": "m1-01-05-quadratic-radicals", "kind": "常一起考",
         "note": "$\\dfrac{\\sqrt3}{2}$、$\\dfrac{\\sqrt2}{2}$ 必须化简成最简根式；答案写成 $\\dfrac{1}{\\sqrt3}$ 就是没化简完"},
    ],
    "m2-07-02-solving-right-triangle": [
        {"id": "m2-07-01-trig-ratios", "kind": "前置",
         "note": "四个三角函数值是本节全部计算的材料，没有它就无从下手"},
        {"id": "m2-02-05-pythagoras", "kind": "前置",
         "note": "求第三条边要靠勾股定理；本节的每道题最后都要用勾股回代验算"},
        {"id": "m2-07-03-trig-applications", "kind": "后续",
         "note": "本节的四条路径放到仰角、俯角、坡角的实景题里，就是本篇的完整应用"},
        {"id": "m2-04-05-arc-sector-cone", "kind": "后续",
         "note": "圆锥的母线、底面半径与高构成直角三角形，解这类题用的正是本节的方法"},
        {"id": "m2-05-03-similar-models", "kind": "常一起考",
         "note": "「定角求边长」用三角函数、「定两边求第三边」用勾股或相似——同一个几何题里这两条路常常都要走"},
        {"id": "m1-03-02-linear-function", "kind": "常一起考",
         "note": "坡度 $i=\\dfrac{h}{b}$ 正是直线斜率 $k$；坡道题在代数里是一次函数，在几何里是直角三角形"},
    ],
    "m2-07-03-trig-applications": [
        {"id": "m2-07-02-solving-right-triangle", "kind": "前置",
         "note": "所有测量题都要先在图上找出直角三角形，再选工具求边——这一步是本篇的固定套路"},
        {"id": "m2-07-01-trig-ratios", "kind": "前置",
         "note": "仰角俯角坡角最终都要化成 tan、sin、cos 的值"},
        {"id": "m2-04-01-circle-properties", "kind": "后续",
         "note": "过圆上一点作切线、由半径垂线定切点，是「测圆塔测烟囱」这类题的标准收尾"},
        {"id": "m1-03-03-linear-function-applications", "kind": "常一起考",
         "note": "坡度固定时「每前进 100 米上升的高度」不变，高度与水平距离成正比——同一个物理情境既是几何题也是一次函数题"},
        {"id": "m2-06-04-geometric-extremum", "kind": "常一起考",
         "note": "「站在何处看物体最大」这类题，底边固定时两边之差最值要用将军饮马，常与三角函数题同场出现"},
    ],
}

# ---------------------------------------------------------------- 证明结论化
STEPS = {
    "m2-07-01-trig-ratios": [
        {
            "conclusion": "结论 1：锐角三角函数的值只由这个角决定，与三角形的大小无关。",
            "proof": "取两个形状相同、大小不同的直角三角形 $\\triangle ABC$ 与 $\\triangle A'B'C'$，其中 $\\angle C=\\angle C'=90^{\\circ}$、$\\angle A=\\angle A'$。由 AA 判定得 $\\triangle ABC\\sim\\triangle A'B'C'$，于是对应边成比例：$\\dfrac{BC}{B'C'}=\\dfrac{AC}{A'C'}=\\dfrac{AB}{A'B'}$。于是「对边比邻边」「邻边比斜边」「对边比斜边」这三个比值，在两个三角形里都相等——它们由 $\\angle A$ 唯一确定，与三角形的大小无关。这正是锐角三角函数能按「角」来取值的理由。",
            "key": "关键一步：AA 相似。它保证两个三角形对应边成比例，是「比值相等」这句话唯一的依据；没有相似，三角形大小一变比值就跟着变。",
        },
        {
            "conclusion": "结论 2：$\\sin30^{\\circ}=\\dfrac12$，$\\cos30^{\\circ}=\\dfrac{\\sqrt3}{2}$，$\\tan30^{\\circ}=\\dfrac{\\sqrt3}{3}$。",
            "proof": "作一个含 $30^{\\circ}$ 角的直角三角形 $\\triangle ABC$，$\\angle A=30^{\\circ}$、$\\angle C=90^{\\circ}$。取斜边 $AB$ 的中点 $M$，连 $CM$。由「直角三角形斜边上的中线等于斜边的一半」得 $CM=AM=BM=\\dfrac12 AB$；又 $BM=CM$，所以 $\\triangle BCM$ 是等边三角形，$\\angle MBC=60^{\\circ}$，即 $\\angle B=60^{\\circ}$。此时 $BC=CM=\\dfrac12 AB$，故 $\\sin30^{\\circ}=\\dfrac{BC}{AB}=\\dfrac12$；由勾股定理 $AC^2=AB^2-BC^2=\\dfrac34 AB^2$，得 $AC=\\dfrac{\\sqrt3}{2}AB$，于是 $\\cos30^{\\circ}=\\dfrac{AC}{AB}=\\dfrac{\\sqrt3}{2}$、$\\tan30^{\\circ}=\\dfrac{BC}{AC}=\\dfrac{1}{\\sqrt3}=\\dfrac{\\sqrt3}{3}$。",
            "key": "关键一步：斜边上的中线等于斜边的一半。这一句把 $30^{\\circ}$ 的锐角三角形变成了等边三角形，是 $30^{\\circ}$ 的值能算出来的枢纽；$60^{\\circ}$ 的三个值由结论 3 与它互换对边邻边得到。",
        },
        {
            "conclusion": "结论 3：$45^{\\circ}$ 的三个三角函数值是 $\\sin45^{\\circ}=\\cos45^{\\circ}=\\dfrac{\\sqrt2}{2}$，$\\tan45^{\\circ}=1$。",
            "proof": "取一个等腰直角三角形 $\\triangle ABC$，$\\angle A=45^{\\circ}$、$\\angle C=90^{\\circ}$，两直角边 $AC=BC=a$。由勾股定理 $AB=\\sqrt{AC^2+BC^2}=\\sqrt2 a$。于是 $\\sin45^{\\circ}=\\dfrac{BC}{AB}=\\dfrac{a}{\\sqrt2 a}=\\dfrac{\\sqrt2}{2}$，$\\cos45^{\\circ}=\\dfrac{AC}{AB}=\\dfrac{\\sqrt2}{2}$（两者相等，因为对边与邻边一样长），$\\tan45^{\\circ}=\\dfrac{BC}{AC}=1$。",
            "key": "关键一步：等腰直角三角形的两直角边相等，所以对边与邻边可以互换——这是 $45^{\\circ}$ 处正弦与余弦相等的唯一理由；换成一般锐角就不相等了。",
        },
        {
            "conclusion": "结论 4：两个锐角互余时，正弦与余弦互换，即 $\\sin A=\\cos B$（当 $\\angle A+\\angle B=90^{\\circ}$）。",
            "proof": "设 $\\angle A+\\angle B=90^{\\circ}$。在 $\\triangle ABC$ 中（$\\angle C=90^{\\circ}$），$BC$ 是 $\\angle A$ 的对边，同时它也是 $\\angle B$ 的邻边。于是同一个比值可以写成两种形式：按 $\\angle A$ 看，$\\sin A=\\dfrac{BC}{AB}$；按 $\\angle B$ 看，$\\cos B=\\dfrac{BC}{AB}$。两者相等，故 $\\sin A=\\cos B$；把 $B$ 换成 $90^{\\circ}-A$ 即得 $\\sin A=\\cos(90^{\\circ}-A)$。",
            "key": "关键一步：$BC$ 这条边同时扮演两个角色——它是 $\\angle A$ 的对边、$\\angle B$ 的邻边。同一条边写成两个不同的比，才逼出这个等式。",
        },
    ],
    "m2-07-02-solving-right-triangle": [
        {
            "conclusion": "结论 1：已知一条直角边和一个锐角时，用正切或余弦都能求边；已知斜边和一个锐角时，用正弦或余弦。",
            "proof": "在直角三角形 $\\triangle ABC$ 中（$\\angle C=90^{\\circ}$），设 $\\angle A=\\alpha$，记 $BC=a$（对 $\\alpha$）、$AC=b$（邻 $\\alpha$）、$AB=c$（斜边）。按定义 $\\tan\\alpha=\\dfrac{a}{b}$、$\\sin\\alpha=\\dfrac{a}{c}$、$\\cos\\alpha=\\dfrac{b}{c}$。若已知 $b$ 与 $\\alpha$，则 $a=b\\tan\\alpha$（用正切），也可用 $c=\\dfrac{b}{\\cos\\alpha}$、$a=\\sqrt{c^2-b^2}$（用余弦）；若已知 $c$ 与 $\\alpha$，则 $a=c\\sin\\alpha$、$b=c\\cos\\alpha$。可见「已知什么」直接决定「用哪个函数」。",
            "key": "关键一步：三个函数里恰好有一个是「对边比邻边」的正切，它能直接接住「一条直角边 + 一个角」；另外两个都带斜边，得先绕道求出斜边。",
        },
        {
            "conclusion": "结论 2：已知两条直角边时，先用勾股定理求第三条边，再用三角函数求角。",
            "proof": "设 $a$、$b$ 为两条直角边，$c$ 为斜边。由勾股定理 $c=\\sqrt{a^2+b^2}$，得到完整的三边长。再用正切 $\\tan\\alpha=\\dfrac{a}{b}$ 求出 $\\alpha$ 的值——注意此时若 $\\alpha$ 较小，$\\dfrac{a}{b}$ 也就小，两者必须对应，否则会算到另一个锐角上去。",
            "key": "关键一步：先用勾股补齐斜边，再算角。正切值本身不告诉你角的大小，必须结合「$\\alpha$ 是较小的那个锐角还是较大的那个」来定位。",
        },
        {
            "conclusion": "结论 3：初中阶段不能「由两条边求角」。",
            "proof": "三角函数给出的是比值（一个数），而不是角度本身。已知两边虽然能确定这个三角形，但要由 $\\tan\\alpha=\\dfrac{a}{b}$ 反求出 $\\alpha$ 的具体度数，需要求三角函数值对应的角，那要用到反三角函数（或查表），这超出初中范围。所以初中解直角三角形必须至少给出一个锐角。",
            "key": "关键一步：比值到角度的反向映射在初中没有工具。这条限制决定了做选择题时看到「已知两边求角」要警惕——它通常需要反三角函数。",
        },
        {
            "conclusion": "结论 4：解完必须用勾股定理回代验算。",
            "proof": "设算出的三边为 $a$、$b$、$c$，检验 $a^2+b^2=c^2$ 是否成立。若不成立，说明某一步用错了函数或选错了对应关系（最常见是把邻边当对边）。勾股定理是三条边之间的整体约束，任何一步算错都会让这个等式失衡，所以它是自查的利器。",
            "key": "关键一步：等式 $a^2+b^2=c^2$ 对三条边同时成立。它能把「某一条边算错」和「全都算错但比例还对」这两类错误区分开——前者等式失衡，后者等式成立但角不对。",
        },
    ],
    "m2-07-03-trig-applications": [
        {
            "conclusion": "结论 1：测树高（或其他标杆）时，物体高 = 水平距离 $\\times \\tan\\alpha$ + 测量者眼睛离地高度。",
            "proof": "设树高为 $h$，观测点到树底的水平距离为 $b$，观测者眼睛离地 $e$，视线与水平线的夹角为仰角 $\\alpha$。过眼睛作水平线，与树干交于点 $M$，则 $EM=b$、$\\angle E=\\alpha$，且 $M$ 在树身上。由 $\\tan\\alpha=\\dfrac{EM}{EM'}$ 得 $EM'=b\\tan\\alpha$，其中 $EM'$ 是从眼睛高度到树顶的高度差。再加上眼睛离地的 $e$，得 $h=b\\tan\\alpha+e$。若忽略 $e$，量出来的树高会系统性偏小——这是这道题最常见的错误。",
            "key": "关键一步：把「物体高」拆成「眼睛高度」加「眼睛以上的树高」。这一步拆分做错，整道题的答案就会差一个固定的 $e$。",
        },
        {
            "conclusion": "结论 2：测山高（山顶在山脚正上方）时，山高 = 水平距离 $\\times (\\tan\\alpha+\\tan\\beta)$。",
            "proof": "设观测点为 $P$，山脚落点为 $C$，山顶为 $T$（$T$ 在 $C$ 正上方），$P$ 到 $C$ 的水平距离为 $d$。$\\alpha$ 是 $P$ 看山顶的仰角，$\\beta$ 是 $P$ 看落点的俯角。山体把 $P$ 到 $T$ 的竖直高度差分成两段：$P$ 到 $C$ 水平面的高度差 $=d\\tan\\beta$（俯角一侧，由 $\\tan\\beta=\\dfrac{\\text{高度差}}{d}$ 得），$C$ 平面到山顶的高度差 $=d\\tan\\alpha$（仰角一侧，同理）。两段相加得山高 $H=d(\\tan\\alpha+\\tan\\beta)$。",
            "key": "关键一步：仰角与俯角对应的是两段不同的高度差，必须相加而不是相减。俯角定的是「观测点比落点高多少」，仰角定的是「山顶比观测点高多少」，两段首尾相接。",
        },
        {
            "conclusion": "结论 3：坡度等于坡角的正切，即 $i=\\dfrac{h}{b}=\\tan\\alpha$。",
            "proof": "在坡角示意图中，坡面、铅直线与水平面构成直角三角形，坡角 $\\alpha$ 的对边是铅直高度 $h$，邻边是水平长度 $b$。按正切定义 $\\tan\\alpha=\\dfrac{h}{b}$，而这个比值正是坡度 $i$ 的定义（每前进单位水平距离上升的高度）。所以 $i=\\tan\\alpha$。若 $i=0.75$，则 $h:b=3:4$，斜边比 $5$，得到 $3:4:5$ 这个常见三角形。",
            "key": "关键一步：坡度与坡角用的是同一个直角三角形里的同一个比，只是斜边那条边被省掉了。把 $i$ 转成整数比，题目往往就变成了勾股或相似的问题。",
        },
    ],
}

for pid, rel in RELATED.items():
    p = C / f"{pid}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["sections"]["related"] = rel
    # 前置从 related 的「前置」类派生，与新结构保持一致
    pre = [r["id"] for r in rel if r["kind"] == "前置"]
    old_pre = d.get("prerequisites", [])
    keep = [x for x in old_pre if x not in pre]
    d["prerequisites"] = pre + keep
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{pid}: related 三类化完成（前置 {len(pre)} / 后续 {sum(1 for r in rel if r['kind']=='后续')} / 常一起考 {sum(1 for r in rel if r['kind']=='常一起考')}）")

for pid, steps in STEPS.items():
    p = C / f"{pid}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["sections"]["why"]["steps"] = steps
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{pid}: 证明板块结论化完成（{len(steps)} 条结论）")
