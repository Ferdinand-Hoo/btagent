# -*- coding: utf-8 -*-
"""
HCI ACL 数据解析 (Host <-> Controller)。
解析 ACL 头后，按 L2CAP CID 分发到 L2CAP 信令 / ATT / SDP 等。
"""
import struct
from typing import Dict, Any

from ..l2cap import parse_l2cap_payload
from ..l2cap.constants import L2CAP_CID_NAMES


def parse_hci_acl(data: bytes) -> Dict[str, Any]:
    """解析 HCI ACL 包体：ACL 头(4) + L2CAP 头(4) + 上层 payload，并按 CID 解析上层。"""
    if len(data) < 4:
        return {'error': f'Too short: {len(data)} bytes'}

    handle_flags = struct.unpack('<H', data[0:2])[0]
    handle = handle_flags & 0x0FFF
    pb_flag = (handle_flags >> 12) & 0x03
    bc_flag = (handle_flags >> 14) & 0x03
    data_len = struct.unpack('<H', data[2:4])[0]

    pb_meaning = {
        0: "First_Non_Auto_Flushable",
        1: "Continuing_Fragment",
        2: "First_Auto_Flushable",
        3: "Complete_L2CAP_PDU"
    }.get(pb_flag, f"Reserved({pb_flag})")

    result = {
        'type': 'ACL_Data',
        'connection_handle_hex': f"0x{handle:04X}",
        'pb_flag': pb_flag,
        'pb_meaning': pb_meaning,
        'bc_flag': bc_flag,
        'data_total_length': data_len,
        'payload_hex': data[4:4 + min(data_len, 32)].hex()
    }

    if len(data) >= 8:
        l2cap_len = struct.unpack('<H', data[4:6])[0]
        cid = struct.unpack('<H', data[6:8])[0]
        l2cap_payload = data[8:8 + min(l2cap_len, len(data) - 8)]

        cid_str = L2CAP_CID_NAMES.get(cid, f"Dynamic_CID_0x{cid:04X}")

        result['l2cap'] = {
            'length': l2cap_len,
            'cid_hex': f"0x{cid:04X}",
            'cid_type': cid_str,
            'l2cap_payload_hex': l2cap_payload.hex()[:48]
        }

        # 按 CID 调用 L2CAP 层解析（信令 / ATT / 后续可扩展 SDP 等）
        try:
            sub = parse_l2cap_payload(cid, l2cap_payload)
            result['l2cap'].update(sub)
        except Exception:
            pass

    return result
