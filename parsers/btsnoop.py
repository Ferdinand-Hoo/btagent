# -*- coding: utf-8 -*-
"""
BTSnoop 文件格式解析与记录编排。
负责：读文件、拆记录、剥 HCI Indicator、按 flags 分发到 HCI 层（命令/事件/ACL），
ACL 由 HCI 层内部再分发到 L2CAP/ATT/SDP 等。
"""
import struct
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

from .hci import (
    HCI_TYPES,
    HCI_INDICATORS,
    HCI_EVENTS,
    EVENT_COMMAND_COMPLETE,
    EVENT_CONNECTION_COMPLETE,
    parse_hci_command,
    parse_hci_event,
    parse_hci_acl,
)

logger = logging.getLogger(__name__)


def _format_abs_time_hms(sec: float) -> str:
    """将 Unix 秒数格式化为 (年-1970)-月-日-时-分-秒（本地时间）。"""
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


@dataclass
class HCIRecord:
    """单条 BTSnoop 记录（含 HCI 及下层解析结果）。"""
    seq: int
    timestamp_abs: int      # 绝对时间，微秒（文件中的原始值，零点由采集端决定）
    timestamp_abs_sec: float  # 绝对时间，秒（同上，便于计算与展示）
    timestamp_rel: float   # 相对时间，毫秒（相对本文件第一条记录）
    flags: int
    packet_type: str
    direction: str
    length: int
    data: bytes
    payload: bytes
    parsed: Dict[str, Any] = None

    def to_dict(self) -> Dict:
        return {
            'seq': self.seq,
            'timestamp_abs_sec': round(self.timestamp_abs_sec, 6),
            'timestamp_rel_ms': round(self.timestamp_rel, 3),
            'direction': self.direction,
            'type': self.packet_type,
            'length': self.length,
            'payload_hex': self.payload.hex()[:64] if self.payload else '',
            'parsed': self.parsed
        }


class BTSnoopParser:
    """
    BTSnoop 解析器：文件层 + 按 flags 分发到 HCI 命令/事件/ACL，
    ACL 内部分发到 L2CAP 信令 / ATT / 后续可接 SDP 等。
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.records: List[HCIRecord] = []
        self.header_info: Dict[str, Any] = {}
        self.base_timestamp = None

    def _strip_hci_indicator(self, data: bytes, flags: int) -> Tuple[bytes, bool]:
        indicators = HCI_INDICATORS
        if not data:
            return data, False
        expected = indicators.get(flags)
        if expected and data[0] == expected:
            return data[1:], True
        return data, False

    def parse(self) -> List[HCIRecord]:
        with open(self.file_path, 'rb') as f:
            raw_data = f.read()

        if len(raw_data) < 16:
            raise ValueError("文件太小，不是有效的 BTSnoop 文件")
        if raw_data[:8] != b'btsnoop\x00':
            raise ValueError(f"无效的 BTSnoop 文件开头8字节: {raw_data[:8].hex()}")

        version = struct.unpack('>I', raw_data[8:12])[0]
        link_type = struct.unpack('>I', raw_data[12:16])[0]
        self.header_info = {'magic': 'btsnoop', 'version': version, 'link_type': link_type, 'file_size': len(raw_data)}
        # 打印 header_info
        print(self.header_info)
        # 每条 BTSnoop 记录 = 24 字节头 + 变长包体。头布局（大端）:
        #   [0:4]   orig_len   - 原始包长度
        #   [4:8]   incl_len   - 本记录中实际保存的包长度
        #   [8:12]  flags      - 记录头里的“标志”：不同实现含义不一，有的当方向/类型用，本解析器不用
        #   [12:16] reserved   - 保留/丢弃计数等
        #   [16:24] timestamp - 时间戳（微秒）
        # HCI 包类型以包体第一个字节为准：1=CMD, 2=ACL_DATA, 3=SCO_DATA, 4=EVENT
        type_map = HCI_TYPES
        offset = 16
        seq = 1

        while offset + 24 <= len(raw_data):
            orig_len = struct.unpack('>I', raw_data[offset:offset + 4])[0]
            incl_len = struct.unpack('>I', raw_data[offset + 4:offset + 8])[0]
            timestamp = struct.unpack('>Q', raw_data[offset + 16:offset + 24])[0]
            pkt_data = raw_data[offset + 24:offset + 24 + incl_len] if incl_len > 0 else b''
            hci_type = pkt_data[0] if pkt_data else 0

            if self.base_timestamp is None:
                self.base_timestamp = timestamp
            rel_time = (timestamp - self.base_timestamp) / 1000.0
            abs_time_sec = timestamp / 1_000_000.0

            packet_type = type_map.get(hci_type, f"Unknown({hci_type})")
            direction = "Host->Controller" if hci_type in (1, 2) else "Controller->Host" if hci_type in (3, 4) else "Unknown"

            clean_payload, _ = self._strip_hci_indicator(pkt_data, hci_type)

            record = HCIRecord(
                seq=seq,
                timestamp_abs=timestamp,
                timestamp_abs_sec=abs_time_sec,
                timestamp_rel=rel_time,
                flags=hci_type,
                packet_type=packet_type,
                direction=direction,
                length=incl_len,
                data=pkt_data,
                payload=clean_payload,
                parsed=None
            )
            record.parsed = self._parse_payload(record)
            self.records.append(record)

            offset += 24 + incl_len
            seq += 1

        self.header_info['total_records'] = len(self.records)
        return self.records

    def _parse_payload(self, record: HCIRecord) -> Dict[str, Any]:
        """按 flags 分发到 HCI 命令 / 事件 / ACL（ACL 内部再走 L2CAP/ATT）。"""
        data = record.payload
        if not data:
            return {}

        try:
            print(f"Parsing payload: flags={record.flags}, data={data.hex()[:64]}")
            if record.flags == 1:
                return parse_hci_command(data)
            if record.flags == 4:
                return parse_hci_event(data)
            if record.flags == 2:
                return parse_hci_acl(data)
            return {'raw_hex': data.hex()[:64]}
        except Exception as e:
            logger.warning("_parse_payload failed: %s", e, exc_info=True)
            return {'parse_error': str(e), 'raw_hex': data.hex()[:64]}

    def analyze(self) -> Dict[str, Any]:
        if not self.records:
            self.parse()

        stats = {
            'total_packets': len(self.records),
            'commands': 0,
            'events': 0,
            'acl_tx': 0,
            'acl_rx': 0,
            'errors': [],
            'connections_established': [],
            'connections_disconnected': [],
            'handles_used': set(),
            'command_completes': []
        }

        if len(self.records) > 1:
            stats['duration_ms'] = round(self.records[-1].timestamp_rel - self.records[0].timestamp_rel, 2)
        else:
            stats['duration_ms'] = 0.0
        if self.records:
            stats['first_timestamp_abs_sec'] = round(self.records[0].timestamp_abs_sec, 6)
            stats['last_timestamp_abs_sec'] = round(self.records[-1].timestamp_abs_sec, 6)
        else:
            stats['first_timestamp_abs_sec'] = stats['last_timestamp_abs_sec'] = 0.0

        for rec in self.records:
            if rec.flags == 1:
                stats['commands'] += 1
            elif rec.flags == 4:
                stats['events'] += 1
                if rec.parsed:
                    if rec.parsed.get('status_hex') and rec.parsed.get('status_str') != "Success":
                        stats['errors'].append({
                            'seq': rec.seq, 'timestamp_ms': round(rec.timestamp_rel, 2),
                            'timestamp_abs_sec': round(rec.timestamp_abs_sec, 6),
                            'event': rec.parsed.get('name', 'Unknown'),
                            'status_hex': rec.parsed.get('status_hex'), 'status_str': rec.parsed.get('status_str')
                        })
                    if rec.parsed.get('name') == 'Command Complete':
                        stats['command_completes'].append({
                            'seq': rec.seq, 'timestamp_ms': round(rec.timestamp_rel, 2),
                            'timestamp_abs_sec': round(rec.timestamp_abs_sec, 6),
                            'command': rec.parsed.get('command_name', 'Unknown'),
                            'opcode': rec.parsed.get('command_opcode_hex'),
                            'ogf': rec.parsed.get('ogf'), 'ocf': rec.parsed.get('ocf'),
                            'status': rec.parsed.get('status_str')
                        })
                    if rec.parsed.get('name') == 'Connection Complete':
                        stats['connections_established'].append({
                            'seq': rec.seq, 'timestamp_ms': round(rec.timestamp_rel, 2),
                            'timestamp_abs_sec': round(rec.timestamp_abs_sec, 6),
                            'handle': rec.parsed.get('connection_handle_hex'),
                            'bd_addr': rec.parsed.get('bd_addr'), 'status': rec.parsed.get('status_str')
                        })
                    if rec.parsed.get('name') == 'Disconnection Complete':
                        stats['connections_disconnected'].append({
                            'seq': rec.seq, 'timestamp_ms': round(rec.timestamp_rel, 2),
                            'timestamp_abs_sec': round(rec.timestamp_abs_sec, 6),
                            'handle': rec.parsed.get('connection_handle_hex'),
                            'reason': rec.parsed.get('reason_str')
                        })
            elif rec.flags == 2:
                stats['acl_tx'] += 1
                if rec.parsed and 'connection_handle_hex' in rec.parsed:
                    stats['handles_used'].add(rec.parsed['connection_handle_hex'])

        stats['handles_used'] = sorted(list(stats['handles_used']))
        stats['error_count'] = len(stats['errors'])
        return stats

    def _write_md_overview(self, f, stats: Dict[str, Any]) -> None:
        f.write("# BTSnoop HCI 日志解析报告\n\n> 分层: HCI 命令/事件/ACL → L2CAP 信令/ATT\n\n")
        f.write("## 📊 概览统计\n\n")
        f.write(f"- **文件**: `{self.file_path}`\n- **总数据包**: {stats['total_packets']}\n")
        f.write(f"- **绝对时间**: {_format_abs_time_hms(stats.get('first_timestamp_abs_sec', 0))} ~ {_format_abs_time_hms(stats.get('last_timestamp_abs_sec', 0))}\n")
        f.write(f"- **持续时间**: {stats['duration_ms']:.2f} ms\n")
        f.write(f"- **HCI 命令**: {stats['commands']} | **HCI 事件**: {stats['events']}\n")
        f.write(f"- **ACL TX**: {stats['acl_tx']} | **ACL RX**: {stats['acl_rx']}\n")
        f.write(f"- **错误数**: {stats['error_count']}\n")
        f.write(f"- **连接句柄**: {', '.join(stats['handles_used']) if stats['handles_used'] else 'N/A'}\n\n")

    def _write_md_command_completes(self, f, stats: Dict[str, Any]) -> None:
        if not stats['command_completes']:
            return
        f.write("## ✅ Command Complete 验证\n\n")
        f.write("| 序号 | 相对(ms) | 绝对时间 | 命令 | OGF | OCF | 状态 |\n|------|----------|----------|------|-----|-----|------|\n")
        for cc in stats['command_completes'][:10]:
            f.write(f"| {cc['seq']} | {cc['timestamp_ms']:.2f} | {_format_abs_time_hms(cc['timestamp_abs_sec'])} | {cc['command']} | {cc['ogf']} | {cc['ocf']} | {cc['status']} |\n")
        if len(stats['command_completes']) > 10:
            f.write(f"\n... 共 {len(stats['command_completes'])} 个\n")
        f.write("\n")

    def _write_md_connections(self, f, stats: Dict[str, Any]) -> None:
        if not stats['connections_established']:
            return
        f.write("## 🔗 连接建立事件\n\n")
        f.write("| 序号 | 相对(ms) | 绝对时间 | 句柄 | 设备地址 | 状态 |\n|------|----------|----------|------|----------|------|\n")
        for c in stats['connections_established']:
            f.write(f"| {c['seq']} | {c['timestamp_ms']:.2f} | {_format_abs_time_hms(c['timestamp_abs_sec'])} | {c['handle']} | {c['bd_addr']} | {c['status']} |\n")
        f.write("\n")

    def _write_md_disconnections(self, f, stats: Dict[str, Any]) -> None:
        if not stats['connections_disconnected']:
            return
        f.write("## 🔴 断开连接事件\n\n")
        f.write("| 序号 | 相对(ms) | 绝对时间 | 句柄 | 原因 |\n|------|----------|----------|------|------|\n")
        for d in stats['connections_disconnected']:
            f.write(f"| {d['seq']} | {d['timestamp_ms']:.2f} | {_format_abs_time_hms(d['timestamp_abs_sec'])} | {d['handle']} | {d['reason']} |\n")
        f.write("\n")

    def _write_md_errors(self, f, stats: Dict[str, Any]) -> None:
        if not stats['errors']:
            return
        f.write("## ⚠️ 错误事件\n\n")
        f.write("| 序号 | 相对(ms) | 绝对时间 | 事件 | 状态码 | 说明 |\n|------|----------|----------|------|--------|------|\n")
        for e in stats['errors'][:20]:
            f.write(f"| {e['seq']} | {e['timestamp_ms']:.2f} | {_format_abs_time_hms(e['timestamp_abs_sec'])} | {e['event']} | {e['status_hex']} | {e['status_str']} |\n")
        f.write("\n")

    def _write_md_flow_table(self, f, records_to_export: List[HCIRecord]) -> None:
        f.write("## 📋 详细通信流程\n\n```\n")
        f.write(f"{'#':<5} {'绝对时间(年-月-日-时-分-秒)':<28} {'Delta(ms)':<12} {'Direction':<18} {'Type':<12} {'OGF':<6} {'OCF':<6} {'Details'}\n")
        f.write("-" * 125 + "\n")
        cmd_ok = HCI_EVENTS.get(EVENT_COMMAND_COMPLETE, "Command Complete")
        conn_ok = HCI_EVENTS.get(EVENT_CONNECTION_COMPLETE, "Connection Complete")
        for rec in records_to_export:
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

    def _write_md_summary(self, f, stats: Dict[str, Any]) -> None:
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

    def export_markdown(self, output_path: str, max_records: int = 0) -> str:
        if not self.records:
            self.parse()
        records = self.records[:max_records] if max_records > 0 else self.records
        stats = self.analyze()
        with open(output_path, 'w', encoding='utf-8') as f:
            self._write_md_overview(f, stats)
            self._write_md_command_completes(f, stats)
            self._write_md_connections(f, stats)
            self._write_md_disconnections(f, stats)
            self._write_md_errors(f, stats)
            self._write_md_flow_table(f, records)
            self._write_md_summary(f, stats)
        return output_path

    def export_json(self, output_path: str, max_records: int = 0) -> str:
        if not self.records:
            self.parse()
        records = self.records[:max_records] if max_records > 0 else self.records
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'header': self.header_info,
                'statistics': self.analyze(),
                'records': [r.to_dict() for r in records]
            }, f, indent=2, ensure_ascii=False)
        return output_path
