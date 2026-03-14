# -*- coding: utf-8 -*-
"""
SDP PDU 解析（占位实现，便于后续扩展）。
SDP 跑在 L2CAP 上，格式: PDU ID(1) + TransactionID(2) + Parameter Length(2) + Parameters。
"""
from typing import Dict, Any

from .constants import SDP_PDU_NAMES


def parse_sdp(payload: bytes) -> Dict[str, Any]:
    """解析 SDP PDU payload，返回 dict。当前仅解析 PDU 类型与长度。"""
    if len(payload) < 5:
        return {'type': 'SDP', 'error': f'Too short: {len(payload)} bytes'}

    pdu_id = payload[0]
    trans_id = int.from_bytes(payload[1:3], 'big')
    param_len = int.from_bytes(payload[3:5], 'big')
    name = SDP_PDU_NAMES.get(pdu_id, f"SDP_PDU_0x{pdu_id:02X}")

    return {
        'type': 'SDP',
        'pdu_id_hex': f"0x{pdu_id:02X}",
        'pdu_name': name,
        'transaction_id': trans_id,
        'parameter_length': param_len,
        'payload_hex': payload[5:5 + param_len].hex()[:64] if len(payload) >= 5 + param_len else payload[5:].hex()[:64]
    }
