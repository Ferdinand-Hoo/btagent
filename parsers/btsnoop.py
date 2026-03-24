# -*- coding: utf-8 -*-
"""
BTSnoop 文件格式解析与记录编排。
负责：读文件、拆记录、剥 HCI Indicator、按 flags 分发到 HCI 层（命令/事件/ACL），
ACL 由 HCI 层内部再分发到 L2CAP/ATT/SDP 等。
"""
import struct
import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
from .hci import (
    HCI_TYPES,
    HCI_INDICATORS,
    parse_hci_command,
    parse_hci_event,
    parse_hci_acl,
)

logger = logging.getLogger(__name__)


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
        logger.debug("BTSnoop header: %s", self.header_info)

        # 每条 BTSnoop 记录 = 24 字节头 + 变长包体。头布局（大端）:
        #   [0:4]   orig_len   - 原始包长度
        #   [4:8]   incl_len   - 本记录中实际保存的包长度
        #   [8:12]  flags      - 记录头里的"标志"
        #   [12:16] reserved   - 保留/丢弃计数等
        #   [16:24] timestamp  - 时间戳（微秒）
        # HCI 包类型以包体第一个字节为准：1=CMD, 2=ACL_DATA, 3=SCO_DATA, 4=EVENT
        type_map = HCI_TYPES
        offset = 16
        seq = 1

        while offset + 24 <= len(raw_data):
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
            logger.debug("seq=%d flags=%d data=%s", seq, hci_type, pkt_data.hex()[:64])

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
            logger.debug("Parsing payload: flags=%d data=%s", record.flags, data.hex()[:64])
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
            elif rec.flags == 3:
                stats['acl_rx'] += 1
                if rec.parsed and 'connection_handle_hex' in rec.parsed:
                    stats['handles_used'].add(rec.parsed['connection_handle_hex'])

        stats['handles_used'] = sorted(list(stats['handles_used']))
        stats['error_count'] = len(stats['errors'])
        return stats
