# -*- coding: utf-8 -*-
"""
L2CAP 信令解析 (CID 0x0001)。
格式: Code(1) + Identifier(1) + Length(2) + 数据，小端。
"""
import struct
from typing import Dict, Any

from .constants import L2CAP_SIGNALING_CODES


def parse_l2cap_signaling(payload: bytes) -> Dict[str, Any]:
    """解析 L2CAP 信令信道 payload，返回 dict。"""
    if len(payload) < 4:
        return {'type': 'L2CAP_Signaling', 'error': f'Too short: {len(payload)} bytes'}

    code = payload[0]
    ident = payload[1]
    length = struct.unpack('<H', payload[2:4])[0]
    data = payload[4:4 + length] if len(payload) >= 4 + length else payload[4:]

    name = L2CAP_SIGNALING_CODES.get(code, f"Unknown_0x{code:02X}")
    result = {
        'type': 'L2CAP_Signaling',
        'code': code,
        'code_name': name,
        'identifier': ident,
        'length': length,
        'payload_hex': data.hex()[:48] if data else ''
    }
    return result
