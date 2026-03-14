# -*- coding: utf-8 -*-
"""
L2CAP 层解析：信令、ATT 等按 CID 分发。
由 HCI ACL 解析器在解析完 ACL 头后调用。
"""
from typing import Dict, Any

from .constants import L2CAP_CID_NAMES
from .signaling import parse_l2cap_signaling
from .att import parse_att


def parse_l2cap_payload(cid: int, payload: bytes) -> Dict[str, Any]:
    """按 CID 分发到 L2CAP 信令 / ATT / SDP 等。"""
    if cid == 0x0001:
        return parse_l2cap_signaling(payload)
    if cid == 0x0004:
        return parse_att(payload)
    return {'cid_hex': f"0x{cid:04X}", 'payload_hex': payload.hex()[:64]}

__all__ = ["L2CAP_CID_NAMES", "parse_l2cap_signaling", "parse_att", "parse_l2cap_payload"]
