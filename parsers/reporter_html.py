# -*- coding: utf-8 -*-
"""
BTSnoop HTML 报告生成：将 BTSnoopParser 的解析结果渲染为可在浏览器中查看的 HTML 页面。
"""
from .reporter import _format_abs_time_hms
from .hci import HCI_EVENTS, EVENT_COMMAND_COMPLETE, EVENT_CONNECTION_COMPLETE


# ──────────────────────────────────────────────────────────────────────────────
# HTML 骨架
# ──────────────────────────────────────────────────────────────────────────────

_HTML_HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BTSnoop HCI 日志解析报告</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #0f1117;
    color: #e2e8f0;
    line-height: 1.6;
  }
  /* ── 顶部 banner ── */
  .banner {
    background: linear-gradient(135deg, #1a1f2e 0%, #16213e 100%);
    border-bottom: 1px solid #2d3748;
    padding: 24px 32px;
  }
  .banner h1 { font-size: 1.5rem; font-weight: 700; color: #63b3ed; }
  .banner .subtitle { font-size: 0.85rem; color: #718096; margin-top: 4px; }
  /* ── 主容器 ── */
  .container { max-width: 1400px; margin: 0 auto; padding: 24px 32px; }
  /* ── 统计卡片 ── */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
  }
  .stat-card {
    background: #1a202c;
    border: 1px solid #2d3748;
    border-radius: 10px;
    padding: 18px 20px;
  }
  .stat-card .label { font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 0.05em; }
  .stat-card .value { font-size: 1.6rem; font-weight: 700; color: #e2e8f0; margin-top: 4px; }
  .stat-card.highlight .value { color: #63b3ed; }
  .stat-card.warn .value { color: #fc8181; }
  .stat-card.ok .value { color: #68d391; }
  /* ── 章节 ── */
  .section { margin-bottom: 36px; }
  .section-title {
    font-size: 1rem;
    font-weight: 600;
    color: #a0aec0;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid #2d3748;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  /* ── 通用表格 ── */
  .tbl-wrap { overflow-x: auto; border-radius: 8px; border: 1px solid #2d3748; }
  table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
  thead th {
    background: #1a202c;
    color: #718096;
    text-align: left;
    padding: 10px 14px;
    font-weight: 600;
    white-space: nowrap;
  }
  tbody tr { border-top: 1px solid #2d3748; }
  tbody tr:hover { background: #1e2536; }
  tbody td { padding: 9px 14px; color: #cbd5e0; white-space: nowrap; }
  /* ── badge ── */
  .badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 9999px;
  }
  .badge-green  { background: #1c4532; color: #68d391; }
  .badge-blue   { background: #1a365d; color: #63b3ed; }
  .badge-red    { background: #4a1942; color: #fc8181; }
  .badge-gray   { background: #2d3748; color: #a0aec0; }
  .badge-orange { background: #3d2006; color: #f6ad55; }
  /* ── 流程表（等宽字体） ── */
  .flow-wrap {
    background: #141820;
    border: 1px solid #2d3748;
    border-radius: 8px;
    overflow-x: auto;
  }
  .flow-wrap table { font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace; }
  .flow-wrap thead th { background: #1a202c; }
  .flow-wrap tbody td { white-space: nowrap; }
  /* 方向列色 */
  .dir-host  { color: #63b3ed; }
  .dir-ctrl  { color: #68d391; }
  /* 类型列 */
  .type-cmd   { color: #f6ad55; }
  .type-evt   { color: #68d391; }
  .type-acl   { color: #b794f4; }
  /* ── 摘要卡 ── */
  .summary-list { list-style: none; padding: 0; }
  .summary-list li {
    padding: 10px 16px;
    background: #1a202c;
    border: 1px solid #2d3748;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 0.88rem;
    color: #cbd5e0;
  }
  .summary-list li strong { color: #e2e8f0; }
  /* ── 分页控件 ── */
  .pager {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    font-size: 0.82rem;
    color: #718096;
  }
  .pager button {
    background: #2d3748;
    border: none;
    color: #e2e8f0;
    padding: 4px 12px;
    border-radius: 6px;
    cursor: pointer;
  }
  .pager button:hover { background: #4a5568; }
  .pager button:disabled { opacity: 0.4; cursor: default; }
  #page-info { min-width: 80px; text-align: center; }
</style>
</head>
<body>
"""

_HTML_FOOT = """
<script>
// ── 通信流程分页 ──
(function () {
  const tbody = document.getElementById('flow-tbody');
  if (!tbody) return;
  const rows = Array.from(tbody.querySelectorAll('tr'));
  const PAGE = 100;
  let page = 0;
  const total = Math.ceil(rows.length / PAGE);

  function render() {
    rows.forEach((r, i) => {
      r.style.display = (i >= page * PAGE && i < (page + 1) * PAGE) ? '' : 'none';
    });
    document.getElementById('page-info').textContent =
      `第 ${page + 1} / ${total} 页（共 ${rows.length} 条）`;
    document.getElementById('btn-prev').disabled = page === 0;
    document.getElementById('btn-next').disabled = page >= total - 1;
  }

  document.getElementById('btn-prev').addEventListener('click', () => { page--; render(); });
  document.getElementById('btn-next').addEventListener('click', () => { page++; render(); });
  render();
})();
</script>
</body>
</html>
"""


# ──────────────────────────────────────────────────────────────────────────────
# 辅助函数
# ──────────────────────────────────────────────────────────────────────────────

def _esc(s: str) -> str:
    """HTML 转义。"""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def _badge(text: str, kind: str = "gray") -> str:
    return f'<span class="badge badge-{kind}">{_esc(text)}</span>'


def _dir_badge(direction: str) -> str:
    if "Host" in direction and "Controller" in direction:
        if direction.startswith("Host"):
            return f'<span class="dir-host">↑ H→C</span>'
        else:
            return f'<span class="dir-ctrl">↓ C→H</span>'
    return _esc(direction)


def _type_cell(ptype: str) -> str:
    cls = {"CMD": "type-cmd", "EVENT": "type-evt", "ACL_DATA": "type-acl"}.get(ptype, "")
    return f'<span class="{cls}">{_esc(ptype)}</span>' if cls else _esc(ptype)


# ──────────────────────────────────────────────────────────────────────────────
# 各章节生成
# ──────────────────────────────────────────────────────────────────────────────

def _html_overview(parser, stats: dict) -> str:
    err_class = "warn" if stats["error_count"] > 0 else "ok"
    cards = [
        ("总数据包",   stats["total_packets"],  "highlight"),
        ("HCI 命令",  stats["commands"],        ""),
        ("HCI 事件",  stats["events"],          ""),
        ("ACL TX",    stats["acl_tx"],          ""),
        ("ACL RX",    stats["acl_rx"],          ""),
        ("错误数",    stats["error_count"],     err_class),
        ("持续时间",  f"{stats['duration_ms']:.0f} ms", ""),
    ]
    cards_html = "".join(
        f'<div class="stat-card {cls}">'
        f'<div class="label">{label}</div>'
        f'<div class="value">{_esc(str(val))}</div>'
        f'</div>'
        for label, val, cls in cards
    )
    handles = ", ".join(stats["handles_used"]) if stats["handles_used"] else "N/A"
    t_start = _format_abs_time_hms(stats.get("first_timestamp_abs_sec", 0))
    t_end   = _format_abs_time_hms(stats.get("last_timestamp_abs_sec", 0))
    return f"""
<div class="stats-grid">{cards_html}</div>
<div class="section">
  <div class="section-title">📁 文件信息</div>
  <div class="tbl-wrap">
    <table>
      <tbody>
        <tr><td style="color:#718096;width:140px">文件路径</td><td><code style="color:#63b3ed">{_esc(str(parser.file_path))}</code></td></tr>
        <tr><td style="color:#718096">时间范围</td><td>{_esc(t_start)} &nbsp;→&nbsp; {_esc(t_end)}</td></tr>
        <tr><td style="color:#718096">连接句柄</td><td>{_esc(handles)}</td></tr>
      </tbody>
    </table>
  </div>
</div>
"""


def _html_command_completes(stats: dict) -> str:
    cc_list = stats["command_completes"]
    if not cc_list:
        return ""
    rows = ""
    for cc in cc_list[:50]:
        status_cls = "green" if cc["status"] == "Success" else "red"
        rows += (
            f"<tr>"
            f"<td>{cc['seq']}</td>"
            f"<td>{cc['timestamp_ms']:.2f}</td>"
            f"<td>{_esc(_format_abs_time_hms(cc['timestamp_abs_sec']))}</td>"
            f"<td>{_esc(cc['command'])}</td>"
            f"<td>{_esc(str(cc['ogf']))}</td>"
            f"<td>{_esc(str(cc['ocf']))}</td>"
            f"<td>{_badge(cc['status'], status_cls)}</td>"
            f"</tr>\n"
        )
    total_tip = f"（共 {len(cc_list)} 条，显示前 50）" if len(cc_list) > 50 else ""
    return f"""
<div class="section">
  <div class="section-title">✅ Command Complete 验证 {total_tip}</div>
  <div class="tbl-wrap">
    <table>
      <thead><tr>
        <th>序号</th><th>相对(ms)</th><th>绝对时间</th>
        <th>命令</th><th>OGF</th><th>OCF</th><th>状态</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</div>
"""


def _html_connections(stats: dict) -> str:
    conn_list = stats["connections_established"]
    disc_list = stats["connections_disconnected"]
    if not conn_list and not disc_list:
        return ""

    conn_rows = "".join(
        f"<tr><td>{c['seq']}</td><td>{c['timestamp_ms']:.2f}</td>"
        f"<td>{_esc(_format_abs_time_hms(c['timestamp_abs_sec']))}</td>"
        f"<td><code>{_esc(c['handle'])}</code></td>"
        f"<td><code>{_esc(c['bd_addr'])}</code></td>"
        f"<td>{_badge(c['status'], 'green' if c['status']=='Success' else 'red')}</td></tr>\n"
        for c in conn_list
    )
    disc_rows = "".join(
        f"<tr><td>{d['seq']}</td><td>{d['timestamp_ms']:.2f}</td>"
        f"<td>{_esc(_format_abs_time_hms(d['timestamp_abs_sec']))}</td>"
        f"<td><code>{_esc(d['handle'])}</code></td>"
        f"<td>{_esc(d['reason'])}</td></tr>\n"
        for d in disc_list
    )

    conn_section = f"""
  <div class="section-title">🔗 连接建立事件</div>
  <div class="tbl-wrap" style="margin-bottom:16px">
    <table>
      <thead><tr><th>序号</th><th>相对(ms)</th><th>绝对时间</th><th>句柄</th><th>设备地址</th><th>状态</th></tr></thead>
      <tbody>{conn_rows}</tbody>
    </table>
  </div>""" if conn_rows else ""

    disc_section = f"""
  <div class="section-title">🔴 断开连接事件</div>
  <div class="tbl-wrap">
    <table>
      <thead><tr><th>序号</th><th>相对(ms)</th><th>绝对时间</th><th>句柄</th><th>原因</th></tr></thead>
      <tbody>{disc_rows}</tbody>
    </table>
  </div>""" if disc_rows else ""

    return f'<div class="section">{conn_section}{disc_section}</div>'


def _html_errors(stats: dict) -> str:
    if not stats["errors"]:
        return ""
    rows = "".join(
        f"<tr><td>{e['seq']}</td><td>{e['timestamp_ms']:.2f}</td>"
        f"<td>{_esc(_format_abs_time_hms(e['timestamp_abs_sec']))}</td>"
        f"<td>{_esc(e['event'])}</td>"
        f"<td><code>{_esc(e['status_hex'])}</code></td>"
        f"<td>{_badge(e['status_str'], 'red')}</td></tr>\n"
        for e in stats["errors"][:20]
    )
    return f"""
<div class="section">
  <div class="section-title">⚠️ 错误事件</div>
  <div class="tbl-wrap">
    <table>
      <thead><tr><th>序号</th><th>相对(ms)</th><th>绝对时间</th><th>事件</th><th>状态码</th><th>说明</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</div>
"""


def _html_flow_table(records) -> str:
    cmd_ok  = HCI_EVENTS.get(EVENT_COMMAND_COMPLETE, "Command Complete")
    conn_ok = HCI_EVENTS.get(EVENT_CONNECTION_COMPLETE, "Connection Complete")

    rows = ""
    for rec in records:
        details = ogf_str = ocf_str = ""
        p = rec.parsed or {}
        ptype = p.get("type", "")
        if ptype == "HCI_Event":
            details = f"{p.get('event_code_hex','')} {p.get('name','')}"
            if p.get("name") == cmd_ok:
                details += f" → {p.get('command_name','')} [{p.get('status_str','')}]"
                ogf_str = str(p.get("ogf", ""))
                ocf_str = str(p.get("ocf", ""))
            elif p.get("name") == conn_ok:
                details += f" Handle={p.get('connection_handle_hex','')} Addr={p.get('bd_addr','')}"
        elif ptype == "HCI_Command":
            details = f"{p.get('opcode_hex','')} {p.get('name','')}"
            ogf_str = str(p.get("ogf_hex", ""))
            ocf_str = str(p.get("ocf_hex", ""))
            if "bd_addr" in p:
                details += f" Addr={p['bd_addr']}"
        elif ptype == "ACL_Data":
            details = f"Handle={p.get('connection_handle_hex','')}"
            if "l2cap" in p:
                l2 = p["l2cap"]
                details += f" L2CAP({l2['cid_hex']},{l2['cid_type']})"
                if "att_operation" in l2:
                    details += f" ATT={l2['att_operation']}"

        rows += (
            f"<tr>"
            f"<td style='color:#718096'>{rec.seq}</td>"
            f"<td>{_esc(_format_abs_time_hms(rec.timestamp_abs_sec))}</td>"
            f"<td style='text-align:right'>{rec.timestamp_rel:.2f}</td>"
            f"<td>{_dir_badge(rec.direction)}</td>"
            f"<td>{_type_cell(rec.packet_type)}</td>"
            f"<td style='color:#718096'>{_esc(ogf_str)}</td>"
            f"<td style='color:#718096'>{_esc(ocf_str)}</td>"
            f"<td>{_esc(details)}</td>"
            f"</tr>\n"
        )

    return f"""
<div class="section">
  <div class="section-title">📋 详细通���流程</div>
  <div class="pager">
    <button id="btn-prev">◀ 上一页</button>
    <span id="page-info"></span>
    <button id="btn-next">下一页 ▶</button>
    <span>每页 100 条</span>
  </div>
  <div class="flow-wrap">
    <table>
      <thead><tr>
        <th>#</th><th>绝对时间</th><th>Delta(ms)</th>
        <th>方向</th><th>类型</th><th>OGF</th><th>OCF</th><th>详情</th>
      </tr></thead>
      <tbody id="flow-tbody">{rows}</tbody>
    </table>
  </div>
</div>
"""


def _html_summary(stats: dict) -> str:
    items = []
    if stats["connections_established"]:
        txt = f"{len(stats['connections_established'])} 个连接建立"
        if stats["connections_disconnected"]:
            txt += f"，{len(stats['connections_disconnected'])} 个断开"
        items.append(f"<strong>连接管理：</strong>{txt}")
    if stats["acl_tx"] > 0 or stats["acl_rx"] > 0:
        total_acl = stats["acl_tx"] + stats["acl_rx"]
        handles = "，句柄 " + ", ".join(stats["handles_used"]) if stats["handles_used"] else ""
        items.append(f"<strong>数据传输：</strong>{total_acl} 个 ACL 数据包{handles}")
    if stats["error_count"] == 0:
        items.append("<strong>错误状态：</strong>未发现 HCI 层错误 ✅")
    else:
        items.append(f"<strong>错误状态：</strong>{stats['error_count']} 个错误事件 ⚠️")
    items.append("<strong>架构：</strong>BTSnoop → HCI(命令/事件/ACL) → L2CAP(信令/ATT) → 可扩展 SDP 等")
    li_html = "".join(f"<li>{item}</li>" for item in items)
    return f"""
<div class="section">
  <div class="section-title">📝 分析总结</div>
  <ul class="summary-list">{li_html}</ul>
</div>
"""


# ──────────────────────────────────────────────────────────────────────────────
# 公开接口
# ──────────────────────────────────────────────────────────────────────────────

def build_html(parser, max_records: int = 0) -> str:
    """将解析结果渲染为完整 HTML 字符串（不写文件，供 server 直接返回）。"""
    if not parser.records:
        parser.parse()
    records = parser.records[:max_records] if max_records > 0 else parser.records
    stats = parser.analyze()

    body = (
        _html_overview(parser, stats)
        + _html_command_completes(stats)
        + _html_connections(stats)
        + _html_errors(stats)
        + _html_flow_table(records)
        + _html_summary(stats)
    )

    return (
        _HTML_HEAD
        + '<div class="banner">'
        + '<h1>BTSnoop HCI 日志解析报告</h1>'
        + f'<div class="subtitle">分层: HCI 命令/事件/ACL → L2CAP 信令/ATT &nbsp;|&nbsp; {len(records)} 条记录</div>'
        + "</div>"
        + f'<div class="container">{body}</div>'
        + _HTML_FOOT
    )


def export_html(parser, output_path: str, max_records: int = 0) -> str:
    """将 HTML 报告写入文件。"""
    html = build_html(parser, max_records)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path
