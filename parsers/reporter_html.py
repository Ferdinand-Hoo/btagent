# -*- coding: utf-8 -*-
"""
BTSnoop HTML 报告生成：将 BTSnoopParser 的解析结果渲染为可在浏览器中查看的 HTML 页面。
"""
from .reporter import _format_abs_time_hms
from .hci import HCI_EVENTS, EVENT_COMMAND_COMPLETE, EVENT_CONNECTION_COMPLETE


# ──────────────────────────────────────────────────────────────────────────────
# CSS / JS 骨架
# ──────────────────────────────────────────────────────────────────────────────

_HTML_HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BTAgent — HCI 日志报告</title>
<style>
/* ── reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── 变量 ── */
:root {
  --bg:        #080c14;
  --bg2:       #0d1320;
  --bg3:       #111827;
  --surface:   #161d2d;
  --border:    #1e2d45;
  --border2:   #253350;
  --text:      #c9d8f0;
  --text-dim:  #5a7399;
  --text-muted:#3a5070;
  --blue:      #3b82f6;
  --blue-dim:  #1d4ed8;
  --blue-glow: rgba(59,130,246,0.18);
  --green:     #22c55e;
  --green-dim: #14532d;
  --red:       #ef4444;
  --red-dim:   #450a0a;
  --orange:    #f97316;
  --purple:    #a855f7;
  --cyan:      #06b6d4;
  --sidebar-w: 220px;
  --header-h:  56px;
}

/* ── 基础 ── */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  font-size: 14px;
}

/* ── 顶部 header ── */
.header {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: var(--header-h);
  background: rgba(8, 12, 20, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 24px;
  z-index: 100;
  gap: 16px;
}
.header-logo {
  display: flex;
  align-items: center;
  gap: 10px;
}
.header-logo .dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: var(--blue);
  box-shadow: 0 0 8px var(--blue);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; box-shadow: 0 0 8px var(--blue); }
  50%       { opacity: .6; box-shadow: 0 0 16px var(--blue); }
}
.header-title { font-size: 1rem; font-weight: 700; color: #e2eaf8; letter-spacing: .02em; }
.header-file  { font-size: 0.75rem; color: var(--text-dim); padding: 3px 10px;
                background: var(--surface); border: 1px solid var(--border);
                border-radius: 6px; font-family: monospace; }

/* ── 侧边栏 ── */
.sidebar {
  position: fixed;
  top: var(--header-h); left: 0; bottom: 0;
  width: var(--sidebar-w);
  background: var(--bg2);
  border-right: 1px solid var(--border);
  overflow-y: auto;
  padding: 20px 0;
  z-index: 90;
}
.sidebar-section { padding: 6px 16px 4px; font-size: 0.65rem; font-weight: 700;
                   color: var(--text-muted); text-transform: uppercase; letter-spacing: .1em; }
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 20px;
  color: var(--text-dim);
  font-size: 0.82rem;
  cursor: pointer;
  border-left: 3px solid transparent;
  transition: all .15s;
  text-decoration: none;
}
.nav-item:hover { color: var(--text); background: rgba(59,130,246,.07); }
.nav-item.active { color: var(--blue); border-left-color: var(--blue);
                   background: var(--blue-glow); }
.nav-icon { font-size: 0.9rem; width: 18px; text-align: center; }

/* ── 主内容区 ── */
.main {
  margin-left: var(--sidebar-w);
  margin-top: var(--header-h);
  padding: 32px 36px;
  max-width: 1300px;
}

/* ── 统计卡片网格 ── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 14px;
  margin-bottom: 36px;
}
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px 20px;
  position: relative;
  overflow: hidden;
  transition: transform .15s, border-color .15s;
}
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: var(--accent, var(--border));
}
.stat-card:hover { transform: translateY(-2px); border-color: var(--border2); }
.stat-card.c-blue   { --accent: var(--blue); }
.stat-card.c-green  { --accent: var(--green); }
.stat-card.c-red    { --accent: var(--red); }
.stat-card.c-purple { --accent: var(--purple); }
.stat-card.c-cyan   { --accent: var(--cyan); }
.stat-card.c-orange { --accent: var(--orange); }

.stat-label { font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase;
              letter-spacing: .06em; font-weight: 600; }
.stat-value { font-size: 1.8rem; font-weight: 800; margin-top: 6px; color: #e8f0ff;
              line-height: 1; }
.stat-card.c-blue   .stat-value { color: var(--blue); }
.stat-card.c-green  .stat-value { color: var(--green); }
.stat-card.c-red    .stat-value { color: var(--red); }
.stat-card.c-purple .stat-value { color: var(--purple); }
.stat-card.c-cyan   .stat-value { color: var(--cyan); }
.stat-card.c-orange .stat-value { color: var(--orange); }
.stat-sub { font-size: 0.72rem; color: var(--text-muted); margin-top: 4px; }

/* ── 章节 ── */
.section { margin-bottom: 40px; scroll-margin-top: 80px; }
.section-header {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 16px;
}
.section-icon {
  width: 32px; height: 32px;
  border-radius: 8px;
  background: var(--surface);
  border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.95rem;
}
.section-title { font-size: 0.95rem; font-weight: 600; color: #c0d0e8; }
.section-count { font-size: 0.72rem; color: var(--text-dim); background: var(--surface);
                 border: 1px solid var(--border); border-radius: 9999px;
                 padding: 2px 9px; margin-left: auto; }

/* ── 信息行（文件信息） ── */
.info-grid {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}
.info-row {
  display: flex; align-items: center;
  padding: 11px 18px;
  border-bottom: 1px solid var(--border);
  font-size: 0.82rem;
}
.info-row:last-child { border-bottom: none; }
.info-key { color: var(--text-dim); width: 110px; flex-shrink: 0; font-weight: 500; }
.info-val { color: var(--text); font-family: monospace; }

/* ── 通用表格 ── */
.tbl-wrap {
  border-radius: 10px;
  border: 1px solid var(--border);
  overflow: hidden;
  overflow-x: auto;
}
table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
thead th {
  background: var(--bg3);
  color: var(--text-dim);
  text-align: left;
  padding: 10px 14px;
  font-weight: 600;
  white-space: nowrap;
  border-bottom: 1px solid var(--border);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: .05em;
}
tbody tr { border-bottom: 1px solid var(--border); transition: background .1s; }
tbody tr:last-child { border-bottom: none; }
tbody tr:nth-child(even) { background: rgba(255,255,255,.018); }
tbody tr:hover { background: rgba(59,130,246,.07); }
tbody td { padding: 9px 14px; color: var(--text); }

/* ── 流程表（等宽） ── */
.flow-tbl tbody td, .flow-tbl thead th {
  font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", "Consolas", monospace;
  font-size: 0.76rem;
}

/* ── badge ── */
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 0.68rem; font-weight: 700;
  padding: 2px 8px; border-radius: 9999px;
  letter-spacing: .03em;
}
.badge::before { content: '●'; font-size: .5rem; }
.bg-green  { background: rgba(34,197,94,.12);  color: #4ade80; border: 1px solid rgba(34,197,94,.25); }
.bg-blue   { background: rgba(59,130,246,.12); color: #60a5fa; border: 1px solid rgba(59,130,246,.25); }
.bg-red    { background: rgba(239,68,68,.12);  color: #f87171; border: 1px solid rgba(239,68,68,.25); }
.bg-gray   { background: rgba(148,163,184,.08);color: #94a3b8; border: 1px solid rgba(148,163,184,.15); }
.bg-orange { background: rgba(249,115,22,.12); color: #fb923c; border: 1px solid rgba(249,115,22,.25); }

/* ── 方向 / 类型标签 ── */
.dir-up   { color: #60a5fa; font-weight: 600; }
.dir-down { color: #4ade80; font-weight: 600; }
.t-cmd  { color: #fbbf24; }
.t-evt  { color: #4ade80; }
.t-acl  { color: #c084fc; }

/* ── 分页控件 ── */
.pager {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 12px; font-size: 0.78rem; color: var(--text-dim);
}
.pager button {
  background: var(--surface); border: 1px solid var(--border);
  color: var(--text); padding: 5px 14px; border-radius: 7px;
  cursor: pointer; font-size: 0.78rem; transition: all .15s;
}
.pager button:hover:not(:disabled) { background: var(--border); color: #e8f0ff; }
.pager button:disabled { opacity: .3; cursor: default; }
#page-info { min-width: 100px; text-align: center; }

/* ── 摘要条目 ── */
.summary-list { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.summary-list li {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 13px 18px;
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  font-size: 0.84rem; color: var(--text);
}
.summary-list li .s-icon { font-size: 1rem; flex-shrink: 0; margin-top: 1px; }

/* ── 配对/折叠行 ── */
.pair-summary {
  cursor: default;
  background: rgba(59,130,246,.05);
}
.pair-summary:hover { background: rgba(59,130,246,.10) !important; }
.pair-summary .expand-icon { cursor: pointer; }
.pair-summary td:first-child { white-space: nowrap; }
.expand-icon {
  display: inline-block;
  font-size: .65rem;
  color: var(--blue);
  transition: transform .18s;
  margin-right: 4px;
}
.expand-icon.open { transform: rotate(90deg); }
.pair-child { background: rgba(0,0,0,.25); }
.pair-child td:first-child { border-left: 2px solid var(--border2); }
.pair-resp td:first-child { border-left: 2px solid rgba(34,197,94,.35); }
.row-clickable { cursor: pointer; transition: background .15s; }
.row-clickable:hover { background: rgba(255,255,255,.05); }
.details-row { background: var(--bg2); }
.details-pre { margin: 0; padding: 12px 16px; font-family: monospace; font-size: 0.75rem; color: #a1b0c8; white-space: pre-wrap; word-break: break-all; }

/* ── 滚动条 ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 9999px; }

/* ── 筛选栏 ── */
.filter-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 18px; margin-bottom: 12px;
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
}
.filter-group { display: flex; align-items: center; gap: 8px; }
.filter-btn {
  padding: 5px 14px; border-radius: 7px; font-size: 0.78rem;
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--text-dim); cursor: pointer; transition: all .15s;
}
.filter-btn:hover { background: var(--border); color: var(--text); }
.filter-btn.active { background: var(--blue); color: white; border-color: var(--blue); }
.time-diff-display {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 12px; background: var(--bg3); border-radius: 7px;
  font-size: 0.8rem;
}
.msg-select { cursor: pointer; width: 16px; height: 16px; }

/* ── 选中状态 ── */
.selectable-row { cursor: pointer; user-select: none; }
.selectable-row.selected { background: rgba(59,130,246,.25) !important; }

/* ── 详情侧边栏 ── */
.detail-sidebar {
  position: fixed; top: var(--header-h); right: -400px; bottom: 0; width: 400px;
  background: var(--bg2); border-left: 1px solid var(--border);
  transition: right .3s; z-index: 90; display: flex; flex-direction: column;
}
.detail-sidebar.open { right: 0; }
.detail-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px; border-bottom: 1px solid var(--border);
}
.detail-title { font-weight: 600; font-size: 0.9rem; color: var(--text); }
.detail-close {
  background: transparent; border: none; color: var(--text-dim);
  font-size: 1.2rem; cursor: pointer; padding: 4px 8px;
  transition: color .15s;
}
.detail-close:hover { color: var(--text); }
.detail-content {
  flex: 1; overflow-y: auto; padding: 16px 20px;
  font-family: monospace; font-size: 0.75rem; color: var(--text);
}
.detail-content pre { margin: 0; white-space: pre-wrap; word-break: break-all; }

/* ── 响应式 ── */
@media (max-width: 900px) {
  .sidebar { display: none; }
  .main { margin-left: 0; padding: 20px 16px; }
}
</style>
</head>
<body>
"""

_HTML_FOOT = """
<script>
// ── 侧边栏高亮（IntersectionObserver）──
(function () {
  const sections = document.querySelectorAll('.section[id]');
  const navItems = document.querySelectorAll('.nav-item[href^="#"]');
  if (!sections.length) return;
  const obs = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        navItems.forEach(n => n.classList.remove('active'));
        const a = document.querySelector(`.nav-item[href="#${en.target.id}"]`);
        if (a) a.classList.add('active');
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
  sections.forEach(s => obs.observe(s));
  if (navItems.length) navItems[0].classList.add('active');
})();

// ── 折叠/展开配对行 ──
function toggleGroup(gid) {
  const children = document.querySelectorAll(`tr.pair-child[data-gid="${gid}"]`);
  const icon = document.getElementById(`icon-${gid}`);
  const isOpen = icon && icon.classList.contains('open');
  children.forEach(tr => { tr.style.display = isOpen ? 'none' : ''; });
  if (icon) icon.classList.toggle('open', !isOpen);
}

// ── 折叠/展开 Details ──
function toggleDetails(did) {
  const detailsRow = document.getElementById(did);
  if (detailsRow) {
    detailsRow.style.display = detailsRow.style.display === 'none' ? '' : 'none';
  }
}

// ── 通信流程分页 ──
(function () {
  const tbody = document.getElementById('flow-tbody');
  if (!tbody) return;
  // 只统计顶层行（pair-summary 和 普通行），不计 pair-child 和 details-row
  const topRows = Array.from(tbody.querySelectorAll('tr:not(.pair-child):not(.details-row)'));
  const PAGE = 100;
  let page = 0;
  const total = Math.ceil(topRows.length / PAGE);

  function render() {
    // 先把所有非child行按分页显隐
    topRows.forEach((r, i) => {
      const show = (i >= page * PAGE && i < (page + 1) * PAGE);
      r.style.display = show ? '' : 'none';
      // 同步隐藏该行关联的子行（若有）
      const gid = r.dataset.gid;
      if (gid) {
        const icon = document.getElementById(`icon-${gid}`);
        const isOpen = icon && icon.classList.contains('open');
        document.querySelectorAll(`tr.pair-child[data-gid="${gid}"]`).forEach(child => {
          child.style.display = (show && isOpen) ? '' : 'none';
          // 这里顺带隐藏 details
          const dRow = document.getElementById('d-' + child.dataset.seq);
          if(dRow) dRow.style.display = 'none';
        });
      }
      // 将本行关联的 details 行也隐藏
      const did = 'd-' + r.dataset.seq;
      const dRow = document.getElementById(did);
      if (dRow) dRow.style.display = 'none';
    });
    document.getElementById('page-info').textContent =
      `第 ${page + 1} / ${total} 页`;
    document.getElementById('btn-prev').disabled = page === 0;
    document.getElementById('btn-next').disabled = page >= total - 1;
  }
  document.getElementById('btn-prev').addEventListener('click', () => { page--; render(); });
  document.getElementById('btn-next').addEventListener('click', () => { page++; render(); });
  render();
})();

// ── 协议筛选 ──
(function () {
  const filterBtns = document.querySelectorAll('.filter-btn:not(#btn-toggle-all)');
  const tbody = document.getElementById('flow-tbody');
  if (!tbody || !filterBtns.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const allRows = tbody.querySelectorAll('tr:not(.details-row)');
      allRows.forEach(row => {
        if (filter === 'all') {
          if (row.classList.contains('pair-child')) {
            // 还原到各组折叠状态，不强制展开
            const gid = row.dataset.gid;
            const icon = document.getElementById(`icon-${gid}`);
            row.style.display = (icon && icon.classList.contains('open')) ? '' : 'none';
          } else {
            row.style.display = '';
          }
        } else {
          if (row.classList.contains('pair-child')) {
            // 子行跟随父组过滤结果
            const gid = row.dataset.gid;
            const icon = document.getElementById(`icon-${gid}`);
            const parentRow = tbody.querySelector(`tr.pair-summary[data-gid="${gid}"]`);
            const parentVisible = !parentRow || parentRow.style.display !== 'none';
            row.style.display = (parentVisible && icon && icon.classList.contains('open')) ? '' : 'none';
          } else {
            const app = row.dataset.app;
            row.style.display = (app === filter) ? '' : 'none';
          }
        }
      });
    });
  });
})();

// ── 全部折叠 / 展开 ──
function toggleAllGroups() {
  const btn = document.getElementById('btn-toggle-all');
  const icons = document.querySelectorAll('.expand-icon');
  const anyOpen = Array.from(icons).some(ic => ic.classList.contains('open'));
  // anyOpen → 折叠全部；全部已折叠 → 展开全部
  icons.forEach(icon => {
    const gid = icon.id.replace('icon-', '');
    const parentRow = document.querySelector(`tr.pair-summary[data-gid="${gid}"]`);
    const parentVisible = !parentRow || parentRow.style.display !== 'none';
    const children = document.querySelectorAll(`tr.pair-child[data-gid="${gid}"]`);
    if (anyOpen) {
      icon.classList.remove('open');
      children.forEach(tr => { tr.style.display = 'none'; });
    } else {
      icon.classList.add('open');
      children.forEach(tr => { tr.style.display = parentVisible ? '' : 'none'; });
    }
  });
  btn.textContent = anyOpen ? '全部展开' : '全部折叠';
}

// ── 消息选择和时间差计算 ──
let selectedRows = [];

function handleRowClick(event, row) {
  // 展开图标本身由自身 onclick 处理，此处跳过
  if (event.target.classList.contains('expand-icon')) return;

  // 可折叠摘要行：单击只做展开/折叠，不弹详情侧边栏
  if (row.classList.contains('pair-summary')) {
    const gid = row.dataset.gid;
    if (gid) toggleGroup(gid);
    return;
  }

  const isCtrlPressed = event.ctrlKey || event.metaKey;

  if (!isCtrlPressed) {
    selectedRows.forEach(r => r.classList.remove('selected'));
    selectedRows = [];
  }

  if (row.classList.contains('selected')) {
    row.classList.remove('selected');
    selectedRows = selectedRows.filter(r => r !== row);
  } else {
    if (selectedRows.length >= 2) {
      selectedRows[0].classList.remove('selected');
      selectedRows.shift();
    }
    row.classList.add('selected');
    selectedRows.push(row);
  }

  updateTimeDiff();

  // 多选时隐藏详情侧边栏（此时显示时间差，遮住会干扰）
  if (selectedRows.length >= 2) {
    closeDetailSidebar();
    return;
  }

  // 单选：再次点击同一行则关闭，否则切换到新行
  const sidebar = document.getElementById('detail-sidebar');
  if (sidebar.classList.contains('open') && sidebar.dataset.activeSeq === row.dataset.seq) {
    closeDetailSidebar();
  } else {
    showDetailSidebar(row);
  }
}

function showDetailSidebar(row) {
  const seq = row.dataset.seq;
  const data = window.recordsData[seq];
  const sidebar = document.getElementById('detail-sidebar');
  const content = document.getElementById('detail-content');

  if (data) {
    const jsonStr = JSON.stringify(data, null, 2);
    content.innerHTML = `<pre>${jsonStr}</pre>`;
    sidebar.dataset.activeSeq = seq;
    sidebar.classList.add('open');
  }
}

function closeDetailSidebar() {
  const sidebar = document.getElementById('detail-sidebar');
  sidebar.classList.remove('open');
  delete sidebar.dataset.activeSeq;
}

function updateTimeDiff() {
  const timeDiffDisplay = document.getElementById('time-diff');
  const timeDiffValue = document.getElementById('time-diff-value');

  if (selectedRows.length === 2) {
    const t1 = parseFloat(selectedRows[0].dataset.time);
    const t2 = parseFloat(selectedRows[1].dataset.time);
    const diff = Math.abs(t2 - t1);
    timeDiffValue.textContent = diff.toFixed(2) + ' ms';
    timeDiffDisplay.style.display = 'flex';
  } else {
    timeDiffDisplay.style.display = 'none';
  }
}

function clearSelection() {
  selectedRows.forEach(r => r.classList.remove('selected'));
  selectedRows = [];
  document.getElementById('time-diff').style.display = 'none';
}
</script>
</body>
</html>
"""


# ──────────────────────────────────────────────────────────────────────────────
# 辅助函数
# ──────────────────────────────────────────────────────────────────────────────

def _esc(s) -> str:
    return (str(s)
            .replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _badge(text: str, kind: str = "gray") -> str:
    cls = {"green": "bg-green", "blue": "bg-blue", "red": "bg-red",
           "orange": "bg-orange"}.get(kind, "bg-gray")
    return f'<span class="badge {cls}">{_esc(text)}</span>'


# ──────────────────────────────────────────────────────────────────────────────
# 章节生成
# ──────────────────────────────────────────────────────────────────────────────

def _html_header(parser) -> str:
    return (
        '<div class="header">'
        '  <div class="header-logo">'
        '    <div class="dot"></div>'
        '    <span class="header-title">BTAgent</span>'
        '  </div>'
        f' <span class="header-file">{_esc(str(parser.file_path))}</span>'
        '</div>'
    )


def _html_sidebar(stats: dict) -> str:
    items = [
        ("#overview",  "📊", "概览统计"),
        ("#fileinfo",  "📁", "文件信息"),
    ]
    if stats["connections_established"] or stats["connections_disconnected"]:
        items.append(("#connections", "🔗", "连接事件"))
    if stats["errors"]:
        items.append(("#errors", "⚠️", "错误事件"))
    items.append(("#flow", "📋", "通信流程"))
    items.append(("#summary", "📝", "分析总结"))

    nav = ""
    for href, icon, label in items:
        nav += (
            f'<a class="nav-item" href="{href}">'
            f'  <span class="nav-icon">{icon}</span>{label}'
            f'</a>'
        )
    return (
        '<div class="sidebar">'
        '  <div class="sidebar-section">导航</div>'
        + nav +
        '</div>'
    )


def _html_stats(stats: dict) -> str:
    err_cls = "c-red" if stats["error_count"] > 0 else "c-green"
    cards = [
        ("总数据包",  stats["total_packets"],             "c-blue",   "packets"),
        ("HCI 命令",  stats["commands"],                  "c-orange",  "commands"),
        ("HCI 事件",  stats["events"],                    "c-cyan",   "events"),
        ("ACL TX",    stats["acl_tx"],                    "c-purple", "packets"),
        ("ACL RX",    stats["acl_rx"],                    "c-purple", "packets"),
        ("错误数",    stats["error_count"],               err_cls,    "errors"),
        ("持续时间",  f"{stats['duration_ms']:.0f} ms",  "c-blue",   "duration"),
    ]
    html = '<div class="stats-grid" id="overview">'
    for label, val, cls, sub in cards:
        html += (
            f'<div class="stat-card {cls}">'
            f'  <div class="stat-label">{label}</div>'
            f'  <div class="stat-value">{_esc(str(val))}</div>'
            f'  <div class="stat-sub">{sub}</div>'
            f'</div>'
        )
    html += '</div>'
    return html


def _html_fileinfo(parser, stats: dict) -> str:
    t_start = _format_abs_time_hms(stats.get("first_timestamp_abs_sec", 0))
    t_end   = _format_abs_time_hms(stats.get("last_timestamp_abs_sec", 0))
    handles = ", ".join(stats["handles_used"]) or "N/A"
    rows = [
        ("文件路径", f'<code style="color:#60a5fa">{_esc(str(parser.file_path))}</code>'),
        ("开始时间", _esc(t_start)),
        ("结束时间", _esc(t_end)),
        ("连接句柄", _esc(handles)),
    ]
    rows_html = "".join(
        f'<div class="info-row"><span class="info-key">{k}</span><span class="info-val">{v}</span></div>'
        for k, v in rows
    )
    return (
        '<div class="section" id="fileinfo">'
        '  <div class="section-header">'
        '    <div class="section-icon">📁</div>'
        '    <span class="section-title">文件信息</span>'
        '  </div>'
        f'  <div class="info-grid">{rows_html}</div>'
        '</div>'
    )


def _html_command_completes(stats: dict) -> str:
    cc_list = stats["command_completes"]
    if not cc_list:
        return ""
    show = cc_list[:50]
    rows = ""
    for cc in show:
        ok = cc["status"] == "Success"
        rows += (
            f"<tr>"
            f"<td>{cc['seq']}</td>"
            f"<td style='color:var(--text-dim)'>{cc['timestamp_ms']:.2f}</td>"
            f"<td style='font-family:monospace'>{_esc(_format_abs_time_hms(cc['timestamp_abs_sec']))}</td>"
            f"<td><strong>{_esc(cc['command'])}</strong></td>"
            f"<td style='color:var(--text-dim)'>{_esc(str(cc['ogf']))}</td>"
            f"<td style='color:var(--text-dim)'>{_esc(str(cc['ocf']))}</td>"
            f"<td>{_badge(cc['status'], 'green' if ok else 'red')}</td>"
            f"</tr>\n"
        )
    tip = f"共 {len(cc_list)} 条，显示前 50" if len(cc_list) > 50 else f"共 {len(cc_list)} 条"
    return (
        '<div class="section" id="commands">'
        '  <div class="section-header">'
        '    <div class="section-icon">✅</div>'
        '    <span class="section-title">Command Complete 验证</span>'
        f'   <span class="section-count">{tip}</span>'
        '  </div>'
        '  <div class="tbl-wrap"><table>'
        '    <thead><tr>'
        '      <th>#</th><th>相对(ms)</th><th>绝对时间</th>'
        '      <th>命令</th><th>OGF</th><th>OCF</th><th>状态</th>'
        '    </tr></thead>'
        f'   <tbody>{rows}</tbody>'
        '  </table></div>'
        '</div>'
    )


def _html_connections(stats: dict) -> str:
    conn_list = stats["connections_established"]
    disc_list = stats["connections_disconnected"]
    if not conn_list and not disc_list:
        return ""

    conn_rows = "".join(
        f"<tr>"
        f"<td>{c['seq']}</td>"
        f"<td style='color:var(--text-dim)'>{c['timestamp_ms']:.2f}</td>"
        f"<td style='font-family:monospace'>{_esc(_format_abs_time_hms(c['timestamp_abs_sec']))}</td>"
        f"<td><code style='color:var(--cyan)'>{_esc(c['handle'])}</code></td>"
        f"<td><code style='color:var(--blue)'>{_esc(c['bd_addr'])}</code></td>"
        f"<td>{_badge(c['status'], 'green' if c['status']=='Success' else 'red')}</td>"
        f"</tr>\n"
        for c in conn_list
    )
    disc_rows = "".join(
        f"<tr>"
        f"<td>{d['seq']}</td>"
        f"<td style='color:var(--text-dim)'>{d['timestamp_ms']:.2f}</td>"
        f"<td style='font-family:monospace'>{_esc(_format_abs_time_hms(d['timestamp_abs_sec']))}</td>"
        f"<td><code style='color:var(--cyan)'>{_esc(d['handle'])}</code></td>"
        f"<td>{_esc(d['reason'])}</td>"
        f"</tr>\n"
        for d in disc_list
    )

    conn_tbl = (
        '<p style="font-size:.8rem;color:var(--text-dim);margin-bottom:8px;font-weight:600">🔗 连接建立</p>'
        '<div class="tbl-wrap" style="margin-bottom:20px"><table>'
        '<thead><tr><th>#</th><th>相对(ms)</th><th>绝对时间</th><th>句柄</th><th>设备地址</th><th>状态</th></tr></thead>'
        f'<tbody>{conn_rows}</tbody>'
        '</table></div>'
    ) if conn_rows else ""

    disc_tbl = (
        '<p style="font-size:.8rem;color:var(--text-dim);margin-bottom:8px;font-weight:600">🔴 断开连接</p>'
        '<div class="tbl-wrap"><table>'
        '<thead><tr><th>#</th><th>相对(ms)</th><th>绝对时间</th><th>句柄</th><th>原因</th></tr></thead>'
        f'<tbody>{disc_rows}</tbody>'
        '</table></div>'
    ) if disc_rows else ""

    total = len(conn_list) + len(disc_list)
    return (
        '<div class="section" id="connections">'
        '  <div class="section-header">'
        '    <div class="section-icon">🔗</div>'
        '    <span class="section-title">连接事件</span>'
        f'   <span class="section-count">{total} 条</span>'
        '  </div>'
        + conn_tbl + disc_tbl +
        '</div>'
    )


def _html_errors(stats: dict) -> str:
    if not stats["errors"]:
        return ""
    rows = "".join(
        f"<tr>"
        f"<td>{e['seq']}</td>"
        f"<td style='color:var(--text-dim)'>{e['timestamp_ms']:.2f}</td>"
        f"<td style='font-family:monospace'>{_esc(_format_abs_time_hms(e['timestamp_abs_sec']))}</td>"
        f"<td>{_esc(e['event'])}</td>"
        f"<td><code style='color:var(--orange)'>{_esc(e['status_hex'])}</code></td>"
        f"<td>{_badge(e['status_str'], 'red')}</td>"
        f"</tr>\n"
        for e in stats["errors"][:20]
    )
    return (
        '<div class="section" id="errors">'
        '  <div class="section-header">'
        '    <div class="section-icon">⚠️</div>'
        '    <span class="section-title">错误事件</span>'
        f'   <span class="section-count">{len(stats["errors"])} 条</span>'
        '  </div>'
        '  <div class="tbl-wrap"><table>'
        '    <thead><tr>'
        '      <th>#</th><th>相对(ms)</th><th>绝对时间</th>'
        '      <th>事件</th><th>状态码</th><th>说明</th>'
        '    </tr></thead>'
        f'   <tbody>{rows}</tbody>'
        '  </table></div>'
        '</div>'
    )


def _rec_details(rec):
    """提取 (item, status, app) 字符串"""
    cmd_ok  = HCI_EVENTS.get(EVENT_COMMAND_COMPLETE, "Command Complete")
    conn_ok = HCI_EVENTS.get(EVENT_CONNECTION_COMPLETE, "Connection Complete")
    p = rec.parsed or {}
    ptype = p.get("type", "")

    item = ""
    status = ""
    app = "HCI"  # 默认为 HCI

    if ptype == "HCI_Event":
        item = p.get("name", f"Event {p.get('event_code_hex', '')}")
        if item == cmd_ok:
            item = p.get("command_name", "Command Complete")
            status = p.get("status_str", "")
        elif item == conn_ok:
            status = p.get("status_str", "")
    elif ptype == "HCI_Command":
        item = p.get("name", f"Command {p.get('opcode_hex', '')}")
    elif ptype == "ACL_Data":
        # 优先显示 L2CAP 层的具体命令名
        if "l2cap" in p:
            l2 = p["l2cap"]
            if l2.get("type") == "L2CAP_Signaling":
                app = "L2CAP"
                item = l2.get("code_name", "L2CAP Signaling")
            elif l2.get("cid_type") == "ATT":
                app = "ATT"
                item = l2.get("att_operation", "ATT Data")
            elif l2.get("cid_type") == "SDP":
                app = "SDP"
                item = l2.get("pdu_name", "SDP Data")
            else:
                app = "L2CAP"
                item = "ACL Data"
        else:
            item = "ACL Data"

    # 特殊前缀
    if ptype in ["HCI_Command", "HCI_Event"]:
        item = "HCI " + item

    return item, status, app


def _pair_records(records):
    """
    将 records 配对：
    1. HCI_Command + Command Complete Event
    2. L2CAP Request + L2CAP Response
    返回列表，每个元素是 (req_or_standalone, resp_or_None)。
    """
    from collections import defaultdict
    cmd_ok = HCI_EVENTS.get(EVENT_COMMAND_COMPLETE, "Command Complete")
    result = []
    used = set()

    # 建立 HCI Command Complete 待匹配表：opcode → [event_index]
    hci_resp: dict[str, list] = defaultdict(list)
    for i, rec in enumerate(records):
        p = rec.parsed or {}
        if p.get("type") == "HCI_Event" and p.get("name") == cmd_ok:
            key = p.get("command_opcode_hex", "")
            if key:
                hci_resp[key].append(i)

    # 建立 L2CAP Response 待匹配表：(handle, identifier, resp_code) → [index]
    l2cap_resp: dict[tuple, list] = defaultdict(list)
    for i, rec in enumerate(records):
        p = rec.parsed or {}
        if p.get("type") == "ACL_Data" and "l2cap" in p:
            l2 = p["l2cap"]
            if l2.get("type") == "L2CAP_Signaling":
                code = l2.get("code")
                ident = l2.get("identifier")
                handle = p.get("connection_handle_hex", "")
                # Response code 是奇数（0x03, 0x05, 0x07, 0x09, 0x0B）
                if code and ident is not None and code % 2 == 1:
                    key = (handle, ident, code)
                    l2cap_resp[key].append(i)

    hci_cursors: dict[str, int] = {k: 0 for k in hci_resp}
    l2cap_cursors: dict[tuple, int] = {k: 0 for k in l2cap_resp}

    for i, rec in enumerate(records):
        if i in used:
            continue
        p = rec.parsed or {}
        matched = None

        # 尝试匹配 HCI Command
        if p.get("type") == "HCI_Command":
            opcode = p.get("opcode_hex", "")
            queue = hci_resp.get(opcode, [])
            cursor = hci_cursors.get(opcode, 0)
            while cursor < len(queue):
                j = queue[cursor]
                cursor += 1
                if j > i and j not in used:
                    matched = j
                    used.add(j)
                    break
            hci_cursors[opcode] = cursor

        # 尝试匹配 L2CAP Request
        elif p.get("type") == "ACL_Data" and "l2cap" in p:
            l2 = p["l2cap"]
            if l2.get("type") == "L2CAP_Signaling":
                code = l2.get("code")
                ident = l2.get("identifier")
                handle = p.get("connection_handle_hex", "")
                # Request code 是偶数（0x02, 0x04, 0x06, 0x08, 0x0A）
                if code and ident is not None and code % 2 == 0:
                    resp_code = code + 1
                    key = (handle, ident, resp_code)
                    queue = l2cap_resp.get(key, [])
                    cursor = l2cap_cursors.get(key, 0)
                    while cursor < len(queue):
                        j = queue[cursor]
                        cursor += 1
                        if j > i and j not in used:
                            matched = j
                            used.add(j)
                            break
                    l2cap_cursors[key] = cursor

        result.append((rec, records[matched] if matched is not None else None))
        used.add(i)

    return result


def _html_flow_table(records) -> str:
    import json
    pairs = _pair_records(records)
    group_id = 0
    rows = ""

    def _details_row(rec):
        did = f"d-{rec.seq}"
        parsed = rec.parsed or {}
        # 为了更好地显示，移除一些太冗余的外层字段，直接展示解析后的核心数据
        display_dict = {k: v for k, v in parsed.items() if k not in ["type", "direction", "packet_type"]}
        json_str = json.dumps(display_dict, indent=2, ensure_ascii=False)
        return (
            f"<tr id='{did}' class='details-row' style='display:none'>"
            f"<td colspan='6'><pre class='details-pre'>{_esc(json_str)}</pre></td>"
            f"</tr>\n"
        )

    for cmd_rec, resp_rec in pairs:
        item, status, app = _rec_details(cmd_rec)

        if resp_rec is not None:
            # ── 配对行：可折叠 ──
            gid = f"g{group_id}"; group_id += 1
            r_item, r_status, r_app = _rec_details(resp_rec)
            status_ok = r_status == "Success"
            status_badge = _badge(r_status, "green" if status_ok else "red") if r_status else ""
            rtt = f"{resp_rec.timestamp_rel - cmd_rec.timestamp_rel:.2f} ms"

            # 摘要行显示通用名称（去掉 _Request/_Response 后缀，L2CAP 加前缀）
            summary_item = item.replace("_Request", "").replace("_Response", "")
            if app == "L2CAP":
                summary_item = f"L2CAP {summary_item}"

            # 摘要行（Command）
            rows += (
                f"<tr class='pair-summary selectable-row' data-gid='{gid}' data-app='{app}' data-time='{cmd_rec.timestamp_rel}' data-seq='{cmd_rec.seq}' onclick='handleRowClick(event, this)'>"
                f"<td style='color:var(--text-muted);white-space:nowrap'>"
                f"  <span class='expand-icon' id='icon-{gid}' onclick='event.stopPropagation(); toggleGroup(\"{gid}\")''>▶</span> "
                f"  {cmd_rec.seq}…{resp_rec.seq}"
                f"</td>"
                f"<td style='font-weight:600;color:var(--blue)'>{_esc(summary_item)}</td>"
                f"<td>{status_badge} <span style='margin-left:8px;color:var(--text-muted);font-size:.72rem'>RTT {rtt}</span></td>"
                f"<td>{_esc(_format_abs_time_hms(cmd_rec.timestamp_abs_sec))}</td>"
                f"<td style='text-align:right;color:var(--text-dim)'>{cmd_rec.timestamp_rel:.2f}</td>"
                f"<td>{_badge(app, 'blue')}</td>"
                f"</tr>\n"
            )
            # 展开后：CMD 子行
            rows += (
                f"<tr class='pair-child selectable-row' data-gid='{gid}' data-seq='{cmd_rec.seq}' data-app='{app}' data-time='{cmd_rec.timestamp_rel}' style='display:none' onclick='handleRowClick(event, this)'>"
                f"<td style='color:var(--text-muted);padding-left:28px'>{cmd_rec.seq}</td>"
                f"<td style='color:#94a3b8'>→ {_esc(item)}</td>"
                f"<td></td>"
                f"<td>{_esc(_format_abs_time_hms(cmd_rec.timestamp_abs_sec))}</td>"
                f"<td style='text-align:right;color:var(--text-dim)'>{cmd_rec.timestamp_rel:.2f}</td>"
                f"<td>{_badge(app, 'blue')}</td>"
                f"</tr>\n"
            )

            # 展开后：RESP 子行
            rows += (
                f"<tr class='pair-child pair-resp selectable-row' data-gid='{gid}' data-seq='{resp_rec.seq}' data-app='{r_app}' data-time='{resp_rec.timestamp_rel}' style='display:none' onclick='handleRowClick(event, this)'>"
                f"<td style='color:var(--text-muted);padding-left:28px'>{resp_rec.seq}</td>"
                f"<td style='color:#94a3b8'>← {_esc(r_item)}</td>"
                f"<td>{_badge(r_status, 'green' if r_status == 'Success' else 'red')}</td>"
                f"<td>{_esc(_format_abs_time_hms(resp_rec.timestamp_abs_sec))}</td>"
                f"<td style='text-align:right;color:var(--text-dim)'>{resp_rec.timestamp_rel:.2f}</td>"
                f"<td>{_badge(r_app, 'blue')}</td>"
                f"</tr>\n"
            )
        else:
            # ── 普通单行 ──
            status_ok = status == "Success" if status else True
            status_badge = _badge(status, "green" if status_ok else "red") if status else ""
            arrow = "→" if cmd_rec.direction == "Host->Controller" else "←"

            rows += (
                f"<tr class='selectable-row' data-seq='{cmd_rec.seq}' data-app='{app}' data-time='{cmd_rec.timestamp_rel}' onclick='handleRowClick(event, this)'>"
                f"<td style='color:var(--text-muted);padding-left:20px'>{cmd_rec.seq}</td>"
                f"<td style='color:var(--text)'>{arrow} {_esc(item)}</td>"
                f"<td>{status_badge}</td>"
                f"<td>{_esc(_format_abs_time_hms(cmd_rec.timestamp_abs_sec))}</td>"
                f"<td style='text-align:right;color:var(--text-dim)'>{cmd_rec.timestamp_rel:.2f}</td>"
                f"<td>{_badge(app, 'blue')}</td>"
                f"</tr>\n"
            )

    # 收集所有记录的 parsed 数据
    records_data = {}
    for rec in records:
        parsed = rec.parsed or {}
        display_dict = {k: v for k, v in parsed.items() if k not in ["type", "direction", "packet_type"]}
        records_data[rec.seq] = display_dict

    records_json = json.dumps(records_data, ensure_ascii=False)

    return (
        '<div class="section" id="flow">'
        '  <div class="section-header">'
        '    <div class="section-icon">📋</div>'
        '    <span class="section-title">详细通信流程</span>'
        f'   <span class="section-count">共 {len(records)} 条 / {group_id} 组配对</span>'
        '  </div>'
        '  <div class="filter-bar">'
        '    <div class="filter-group">'
        '      <label style="font-weight:600;margin-right:12px">协议筛选:</label>'
        '      <button class="filter-btn active" data-filter="all">全部</button>'
        '      <button class="filter-btn" data-filter="HCI">HCI</button>'
        '      <button class="filter-btn" data-filter="L2CAP">L2CAP</button>'
        '      <button class="filter-btn" data-filter="ATT">ATT</button>'
        '      <button class="filter-btn" data-filter="SDP">SDP</button>'
        '    </div>'
        '    <div style="display:flex;align-items:center;gap:8px">'
        '      <button id="btn-toggle-all" class="filter-btn" onclick="toggleAllGroups()">全部展开</button>'
        '      <div class="time-diff-display" id="time-diff" style="display:none">'
        '      <span style="color:var(--text-muted)">时间差:</span> '
        '      <span id="time-diff-value" style="font-weight:600;color:var(--green)">0.00 ms</span>'
        '        <button onclick="clearSelection()" style="margin-left:8px;padding:2px 8px;font-size:0.85rem">清除</button>'
        '      </div>'
        '    </div>'
        '  </div>'
        '  <div class="pager">'
        '    <button id="btn-prev">← 上一页</button>'
        '    <span id="page-info"></span>'
        '    <button id="btn-next">下一页 →</button>'
        '    <span style="color:var(--text-muted)">每页 100 条 &nbsp;|&nbsp; 点击配对组展开，点击子行查看详情</span>'
        '  </div>'
        '  <div class="tbl-wrap">'
        '    <table class="flow-tbl">'
        '      <thead><tr>'
        '        <th style="width:60px">#</th>'
        '        <th>Item</th>'
        '        <th>Status</th>'
        '        <th>Time</th>'
        '        <th style="text-align:right">Time delta</th>'
        '        <th>Application</th>'
        '      </tr></thead>'
        f'     <tbody id="flow-tbody">{rows}</tbody>'
        '    </table>'
        '  </div>'
        f'  <script>window.recordsData = {records_json};</script>'
        '</div>'
    )


def _html_summary(stats: dict) -> str:
    items = []
    if stats["connections_established"]:
        txt = f"{len(stats['connections_established'])} 个连接建立"
        if stats["connections_disconnected"]:
            txt += f"，{len(stats['connections_disconnected'])} 个断开"
        items.append(("🔗", f"<strong>连接管理</strong> &nbsp;{txt}"))

    if stats["acl_tx"] > 0 or stats["acl_rx"] > 0:
        total_acl = stats["acl_tx"] + stats["acl_rx"]
        handles = "，句柄 " + ", ".join(stats["handles_used"]) if stats["handles_used"] else ""
        items.append(("📦", f"<strong>数据传输</strong> &nbsp;{total_acl} 个 ACL 数据包{handles}"))

    if stats["error_count"] == 0:
        items.append(("✅", "<strong>错误状态</strong> &nbsp;未发现 HCI 层错误"))
    else:
        items.append(("⚠️", f"<strong>错误状态</strong> &nbsp;{stats['error_count']} 个错误事件"))

    items.append(("🏗️", "<strong>解析架构</strong> &nbsp;BTSnoop → HCI(命令/事件/ACL) → L2CAP(信令/ATT) → 可扩展 SDP 等"))

    li_html = "".join(
        f'<li><span class="s-icon">{icon}</span><span>{text}</span></li>'
        for icon, text in items
    )
    return (
        '<div class="section" id="summary">'
        '  <div class="section-header">'
        '    <div class="section-icon">📝</div>'
        '    <span class="section-title">分析总结</span>'
        '  </div>'
        f'  <ul class="summary-list">{li_html}</ul>'
        '</div>'
    )


# ──────────────────────────────────────────────────────────────────────────────
# 公开接口
# ───────��──────────────────────────────────────────────────────────────────────

def build_html(parser, max_records: int = 0) -> str:
    if not parser.records:
        parser.parse()
    records = parser.records[:max_records] if max_records > 0 else parser.records
    stats = parser.analyze()

    body = (
        _html_stats(stats)
        + _html_fileinfo(parser, stats)

        + _html_connections(stats)
        + _html_errors(stats)
        + _html_flow_table(records)
        + _html_summary(stats)
    )

    return (
        _HTML_HEAD
        + _html_header(parser)
        + _html_sidebar(stats)
        + f'<div class="main">{body}</div>'
        + '<div class="detail-sidebar" id="detail-sidebar">'
        + '  <div class="detail-header">'
        + '    <span class="detail-title">详细信息</span>'
        + '    <button class="detail-close" onclick="closeDetailSidebar()">✕</button>'
        + '  </div>'
        + '  <div class="detail-content" id="detail-content">'
        + '    <p style="color:var(--text-dim);text-align:center;padding:40px 20px">点击消息行查看详细信息</p>'
        + '  </div>'
        + '</div>'
        + _HTML_FOOT
    )


def export_html(parser, output_path: str, max_records: int = 0) -> str:
    html = build_html(parser, max_records)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path
