"""线上站点冒烟验证：检查渲染、公式、配图加载、站内跳转、控制台报错。

用法: python tools/verify_online.py [BASE_URL] [SHARECODE]
默认 BASE_URL = https://ttbingo.github.io/junior-math-atlas
带门禁的域名（app.workbuddy.host）需传 SHARECODE，首次访问会种 cookie。
"""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else
        "https://ttbingo.github.io/junior-math-atlas").rstrip("/")
CODE = sys.argv[2] if len(sys.argv) > 2 else ""
ENTRY = BASE + (f"/?sharecode={CODE}" if CODE else "/")
SHOTS = ".shots"


def main():
    errs, fails = [], []
    os.makedirs(SHOTS, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1360, "height": 900})
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))

        # ── 首页 ──
        pg.goto(ENTRY, wait_until="networkidle", timeout=60000)
        cards = pg.locator(".mod-card").count()
        idx = pg.evaluate("(window.__SEARCH_INDEX__||[]).length")
        links = pg.locator("a[href]").count()
        print(f"首页: 模块卡片={cards} 搜索索引={idx} 链接数={links}")
        if cards != 3:
            fails.append(f"模块卡片数异常: {cards}（应为 3：代数/几何/统计与概率）")
        # 索引 = 3 模块 + 12 主题 + 61 知识点 = 76
        if idx != 76:
            fails.append(f"搜索索引条数异常: {idx}（应为 76 = 3 模块 + 12 主题 + 61 知识点）")

        # ── 站内跳转 ──
        pg.locator(".mod-card").first.click()
        pg.wait_for_load_state("networkidle")
        print(f"点模块卡片 -> {pg.url}")
        if not pg.url.startswith(BASE + "/m"):
            fails.append(f"模块跳转 URL 异常: {pg.url}")
        topics = pg.locator('a[href*="/t/"]').count()
        print(f"模块页: 主题链接={topics}")
        if topics == 0:
            fails.append("模块页无主题链接")

        # ── 知识点页：公式 / 教材定位 / 证明 / 关联三类 ──
        pg.goto(BASE + "/points/m2-07-01-trig-ratios/", wait_until="networkidle",
                timeout=60000)
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(600)
        pg.evaluate("window.scrollTo(0, 0)")
        pg.wait_for_timeout(200)
        katex = pg.locator(".katex").count()
        kerr = pg.locator(".katex-error").count()
        bare = pg.evaluate(
            r"document.body.innerText.match(/(^|[^\\])\$[^$\n]{1,40}\$/g)||[]")
        tb = pg.locator(".textbook").count()
        tb_line = pg.inner_text(".tb-line") if tb else ""
        proof = pg.locator(".proof-item").count()
        tags = pg.eval_on_selector_all(".rel-tag", "els=>els.map(e=>e.innerText)")
        ptref = pg.locator("a.ptref").count()
        print(f"知识点页: KaTeX={katex} 错误={kerr} 裸$={len(bare)} | "
              f"教材定位={tb_line[:40]} | 证明={proof} | 三类={tags} | 链接={ptref}")
        if katex == 0:
            fails.append("知识点页未渲染公式")
        if kerr:
            fails.append(f"KaTeX 报错 {kerr} 处")
        if bare:
            fails.append(f"残留裸 $ 公式: {bare[:3]}")
        if tb != 1 or not tb_line:
            fails.append("教材定位区块缺失")
        if proof == 0:
            fails.append("证明板块为空")
        if sorted(tags) != sorted(["前置", "后续", "常一起考"]):
            fails.append(f"关联三类不齐: {tags}")
        if ptref == 0:
            fails.append("正文无知识点跳转链接")
        pg.screenshot(path=f"{SHOTS}/gh-point.png", full_page=False)

        # ── 配图真实加载（懒加载需滚动）──
        pg.goto(BASE + "/points/m2-04-01-circle-properties/", wait_until="networkidle",
                timeout=60000)
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(700)
        bad_img = pg.evaluate(
            "[...document.images].filter(i=>!i.complete||i.naturalWidth===0)"
            ".map(i=>i.currentSrc||i.src)")
        n_img = pg.evaluate("document.images.length")
        print(f"圆的性质页: 图片={n_img} 加载失败={len(bad_img)}")
        if n_img == 0:
            fails.append("配图未出现在页面")
        if bad_img:
            fails.append(f"配图加载失败: {bad_img[:2]}")

        # ── 搜索 ──
        pg.goto(ENTRY, wait_until="networkidle")
        pg.keyboard.press("Control+k")
        pg.wait_for_timeout(400)
        if pg.locator("#search-input, .search-input, input[type=search]").count():
            pg.locator("#search-input, .search-input, input[type=search]").first.fill("相似")
            pg.wait_for_timeout(600)
            hits = pg.locator("#search-results a").count()
            print(f"搜索「相似」命中={hits}")
            if hits == 0:
                fails.append("搜索无结果")
        pg.screenshot(path=f"{SHOTS}/gh-search.png")

        pg.goto(ENTRY, wait_until="networkidle")
        pg.screenshot(path=f"{SHOTS}/gh-home.png", full_page=False)
        br.close()

    print(f"\n控制台错误: {len(errs)}")
    for e in errs[:5]:
        print("  !", e[:120])
    print(f"失败项: {len(fails)}")
    for f in fails:
        print("  X", f)
    sys.exit(1 if (fails or errs) else 0)


if __name__ == "__main__":
    main()
