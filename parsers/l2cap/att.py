# -*- coding: utf-8 -*-
"""
ATT (Attribute Protocol) 解析 (CID 0x0004)。
"""
from typing import Dict, Any

from .constants import ATT_OPCODES


def parse_att(payload: bytes) -> Dict[str, Any]:
    """解析 ATT 信道 payload（首字节为 ATT 操作码）。"""
    if not payload:
        return {'type': 'ATT', 'error': 'Empty payload'}

    opcode = payload[0]
    name = ATT_OPCODES.get(opcode, f"ATT_0x{opcode:02X}")
    return {
        'type': 'ATT',
        'att_opcode_hex': f"0x{opcode:02X}",
        'att_operation': name,
        'payload_hex': payload[1:].hex()[:48] if len(payload) > 1 else ''
    }
