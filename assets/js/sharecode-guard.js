/* sharecode-guard.js — 让站内跳转始终携带 workbuddy.host 的分享码
 *
 * 背景：workbuddy.host 的分享门禁只认 ?sharecode= 参数。站内原先是纯相对链接，
 * 一旦点进子页，地址栏的分享码就消失；此时刷新、复制或转发都会得到
 * 403「链接不完整」。本脚本把分享码透传到所有站内链接与地址栏。
 *
 * 行为：
 *   1. 从当前 URL 读取 sharecode 并记忆（sessionStorage 优先，localStorage 兜底）；
 *   2. 若当前 URL 缺参数但已有记忆值，用 replaceState 补回地址栏（不发新请求、不产生历史记录）；
 *   3. 给所有同源 <a> 链接补上 sharecode；
 *   4. 点击时再兜底补一次，覆盖动态插入的链接。
 * 在 GitHub Pages 等无分享码环境会自动空转，不产生副作用。
 */
(function () {
  'use strict';

  var KEY = 'mathsite:sharecode';
  var m = /[?&]sharecode=([A-Za-z0-9_-]+)/.exec(location.search);
  var code = m ? m[1] : null;

  try {
    if (code) {
      localStorage.setItem(KEY, code);
      sessionStorage.setItem(KEY, code);
    }
  } catch (e) { /* 隐私模式下存储不可用，忽略 */ }

  if (!code) {
    try { code = sessionStorage.getItem(KEY) || localStorage.getItem(KEY); } catch (e) { code = null; }
  }
  if (!code) return;

  function withCode(href) {
    if (!href) return href;
    if (/^(#|mailto:|tel:|javascript:|data:|blob:)/i.test(href)) return href;
    var u;
    try { u = new URL(href, location.href); } catch (e) { return href; }
    if (u.origin !== location.origin) return href;
    if (u.searchParams.get('sharecode')) return href;
    u.searchParams.set('sharecode', code);
    return u.pathname + u.search + u.hash;
  }

  // 1) 地址栏补码：让「复制当前地址」永远拿到完整链接
  if (!m) {
    try {
      var cur = new URL(location.href);
      cur.searchParams.set('sharecode', code);
      history.replaceState(null, '', cur.pathname + cur.search + cur.hash);
    } catch (e) { /* ignore */ }
  }

  // 2) 静态链接补码
  function patch(root) {
    var list = (root || document).querySelectorAll('a[href]');
    for (var i = 0; i < list.length; i++) {
      var h = list[i].getAttribute('href');
      var n = withCode(h);
      if (n && n !== h) list[i].setAttribute('href', n);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { patch(document); });
  } else {
    patch(document);
  }

  // 3) 点击兜底（含动态插入的链接、新窗口打开）
  document.addEventListener('click', function (ev) {
    var t = ev.target;
    var a = t && t.closest ? t.closest('a[href]') : null;
    if (!a) return;
    var h = a.getAttribute('href');
    var n = withCode(h);
    if (n && n !== h) a.setAttribute('href', n);
  }, true);
})();
