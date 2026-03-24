# -*- coding: utf-8 -*-
"""
BTSnoop 报告生成：将 BTSnoopParser 的解析结果导出为 Markdown 或 JSON。
"""
import json
from typing import List, Dict, Any
from pathlib import Path

from .hci import HCI_EVENTS, EVENT_COMMAND_COMPLETE, EVENT_CONNECTION_COMPLETE


def _format_abs_time_hms(sec: float) -> str:
    """将 Unix 秒数格式化为 (年-1970)-月-日-时-分-秒（本地时间）。"""
    from datetime import datetime
    try:
        sec = float(sec)
    except (TypeError, ValueError):
        return "-"
    if sec < 0 or sec != sec:  # NaN
        return "-"
    try:
        dt = datetime.fromtimestamp(sec)
        year_since_1970 = dt.year - 1970
        s_frac = sec % 1
        base = f"{year_since_1970:04d}-{dt.month:02d}-{dt.day:02d}-{dt.hour:02d}-{dt.minute:02d}-{dt.second:02d}"
        if s_frac != 0:
            return base + f".{int(round(s_frac * 1_000_000)):06d}"
        return base
    except (OSError, ValueError):
        return "-"


def _write_md_overview(f, parser, stats: Dict[str, Any]) -> None:
    f.write("# BTSnoop HCI 日志解析报告\n\n> 分层: HCI 命令/事件/ACL → L2CAP 信令/ATT\n\n")
    f.write("## 📊 概览统计\n\n")
    f.write(f"- **文件**: `{parser.file_path}`\n- **总数据包**: {stats['total_packets']}\n")
    f.write(f"- **绝对时间**: {_format_abs_time_hms(stats.get('first_timestamp_abs_sec', 0))} ~ {_format_abs_time_hms(stats.get('last_timestamp_abs_sec', 0))}\n")
    f.write(f"- **持续时间**: {stats['duration_ms']:.2f} ms\n")
    f.write(f"- **HCI 命令**: {stats['commands']} | **HCI 事件**: {stats['events']}\n")
    f.write(f"- **ACL TX**: {stats['acl_tx']} | **ACL RX**: {stats['acl_rx']}\n")
    f.write(f"- **错误数**: {stats['error_count']}\n")
    f.write(f"- **连接句柄**: {', '.join(stats['handles_used']) if stats['handles_used'] else 'N/A'}\n\n")


def _write_md_command_completes(f, stats: Dict[str, Any]) -> None:
    if not stats['command_completes']:
        return
    f.write("## ✅ Command Complete 验证\n\n")
    f.write("| 序号 | 相对(ms) | 绝对时间 | 命令 | OGF | OCF | 状态 |\n|------|----------|----------|------|-----|-----|------|\n")
    for cc in stats['command_completes'][:10]:
        f.write(f"| {cc['seq']} | {cc['timestamp_ms']:.2f} | {_format_abs_time_hms(cc['timestamp_abs_sec'])} | {cc['command']} | {cc['ogf']} | {cc['ocf']} | {cc['status']} |\n")
    if len(stats['command_completes']) > 10:
        f.write(f"\n... 共 {len(stats['command_completes'])} 个\n")
    f.write("\n")


def _write_md_connections(f, stats: Dict[str, Any]) -> None:
    if not stats['connections_established']:
        return
    f.write("## 🔗 连接建立事件\n\n")
    f.write("| 序号 | 相对(ms) | 绝对时间 | 句柄 | 设备地址 | 状态 |\n|------|----------|----------|------|----------|------|\n")
    for c in stats['connections_established']:
        f.write(f"| {c['seq']} | {c['timestamp_ms']:.2f} | {_format_abs_time_hms(c['timestamp_abs_sec'])} | {c['handle']} | {c['bd_addr']} | {c['status']} |\n")
    f.write("\n")


def _write_md_disconnections(f, stats: Dict[str, Any]) -> None:
    if not stats['connections_disconnected']:
        return
    f.write("## 🔴 断开连接事件\n\n")
    f.write("| 序号 | 相对(ms) | 绝对时间 | 句柄 | 原因 |\n|------|----------|----------|------|------|\n")
    for d in stats['connections_disconnected']:
        f.write(f"| {d['seq']} | {d['timestamp_ms']:.2f} | {_format_abs_time_hms(d['timestamp_abs_sec'])} | {d['handle']} | {d['reason']} |\n")
    f.write("\n")


def _write_md_errors(f, stats: Dict[str, Any]) -> None:
    if not stats['errors']:
        return
    f.write("## ⚠️ 错误事件\n\n")
    f.write("| 序号 | 相对(ms) | 绝对时间 | 事件 | 状态码 | 说明 |\n|------|----------|----------|------|--------|------|\n")
    for e in stats['errors'][:20]:
        f.write(f"| {e['seq']} | {e['timestamp_ms']:.2f} | {_format_abs_time_hms(e['timestamp_abs_sec'])} | {e['event']} | {e['status_hex']} | {e['status_str']} |\n")
    f.write("\n")


def _write_md_flow_table(f, records) -> None:
    cmd_ok = HCI_EVENTS.get(EVENT_COMMAND_COMPLETE, "Command Complete")
    conn_ok = HCI_EVENTS.get(EVENT_CONNECTION_COMPLETE, "Connection Complete")

    f.write("## 📋 详细通信流程\n\n```\n")
    f.write(f"{'#':<5} {'绝对时间(年-月-日-时-分-秒)':<28} {'Delta(ms)':<12} {'Direction':<18} {'Type':<12} {'OGF':<6} {'OCF':<6} {'Details'}\n")
    f.write("-" * 125 + "\n")
    for rec in records:
        details, ogf_str, ocf_str = "", "-", "-"
        if rec.parsed:
            if rec.parsed.get('type') == 'HCI_Event':
                details = f"{rec.parsed.get('event_code_hex', 'N/A')} {rec.parsed.get('name', 'Unknown')}"
                if rec.parsed.get('name') == cmd_ok:
                    details += f" -> {rec.parsed.get('command_name', 'Unknown')} [{rec.parsed.get('status_str', 'N/A')}]"
                    ogf_str, ocf_str = rec.parsed.get('ogf', '-'), rec.parsed.get('ocf', '-')
                elif rec.parsed.get('name') == conn_ok:
                    details += f" Handle={rec.parsed.get('connection_handle_hex', 'N/A')} Addr={rec.parsed.get('bd_addr', 'N/A')}"
            elif rec.parsed.get('type') == 'HCI_Command':
                details = f"{rec.parsed.get('opcode_hex', 'N/A')} {rec.parsed.get('name', 'Unknown')}"
                ogf_str, ocf_str = rec.parsed.get('ogf_hex', '-'), rec.parsed.get('ocf_hex', '-')
                if 'bd_addr' in rec.parsed:
                    details += f" Addr={rec.parsed['bd_addr']}"
            elif rec.parsed.get('type') == 'ACL_Data':
                details = f"Handle={rec.parsed.get('connection_handle_hex', 'N/A')}"
                if 'l2cap' in rec.parsed:
                    l2 = rec.parsed['l2cap']
                    details += f" L2CAP({l2['cid_hex']},{l2['cid_type']})"
                    if 'att_operation' in l2:
                        details += f" ATT={l2['att_operation']}"
        f.write(f"{rec.seq:<5} {_format_abs_time_hms(rec.timestamp_abs_sec):<28} {rec.timestamp_rel:<12.2f} {rec.direction:<18} {rec.packet_type:<12} {ogf_str:<6} {ocf_str:<6} {details}\n")
    f.write("```\n\n")


def _write_md_summary(f, stats: Dict[str, Any]) -> None:
    f.write("## 📝 分析总结\n\n")
    if stats['connections_established']:
        f.write(f"1. **连接管理**: {len(stats['connections_established'])} 个连接建立")
        if stats['connections_disconnected']:
            f.write(f"，{len(stats['connections_disconnected'])} 个断开")
        f.write("\n\n")
    if stats['acl_tx'] > 0 or stats['acl_rx'] > 0:
        f.write(f"2. **数据传输**: {stats['acl_tx'] + stats['acl_rx']} 个 ACL 数据包")
        if stats['handles_used']:
            f.write(f"，句柄 {', '.join(stats['handles_used'])}")
        f.write("\n\n")
    f.write("3. **错误状态**: 未发现 HCI 层错误\n\n" if stats['error_count'] == 0 else f"3. **错误状态**: {stats['error_count']} 个错误事件\n\n")
    f.write("---\n\n**架构**: BTSnoop → HCI(命令/事件/ACL) → L2CAP(信令/ATT) → 可扩展 SDP 等\n")


def export_markdown(parser, output_path: str, max_records: int = 0) -> str:
    if not parser.records:
        parser.parse()
    records = parser.records[:max_records] if max_records > 0 else parser.records
    stats = parser.analyze()
    with open(output_path, 'w', encoding='utf-8') as f:
        _write_md_overview(f, parser, stats)
        _write_md_command_completes(f, stats)
        _write_md_connections(f, stats)
        _write_md_disconnections(f, stats)
        _write_md_errors(f, stats)
        _write_md_flow_table(f, records)
        _write_md_summary(f, stats)
    return output_path


def export_json(parser, output_path: str, max_records: int = 0) -> str:
    if not parser.records:
        parser.parse()
    records = parser.records[:max_records] if max_records > 0 else parser.records
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'header': parser.header_info,
            'statistics': parser.analyze(),
            'records': [r.to_dict() for r in records]
        }, f, indent=2, ensure_ascii=False)
    return output_path
