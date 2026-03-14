# -*- coding: utf-8 -*-
"""
HCI 命令解析 (Host -> Controller)
格式: Opcode(2) + Parameter Length(1) + Parameters(n)，Opcode 小端。
"""
import struct
from typing import Dict, Any

from .constants import parse_opcode, HCI_COMMANDS, HCI_ERRORS


def parse_hci_command(data: bytes) -> Dict[str, Any]:
    """解析 HCI Command 包体，返回结构化 dict。"""
    if len(data) < 3:
        return {'error': f'Too short: {len(data)} bytes'}

    opcode_val = struct.unpack('<H', data[0:2])[0]
    param_len = data[2]
    params = data[3:3 + param_len] if param_len > 0 else b''

    ogf, ocf = parse_opcode(opcode_val)
    cmd_name = HCI_COMMANDS.get((ogf, ocf), f"OGF=0x{ogf:02X}, OCF=0x{ocf:03X}")

    result = {
        'type': 'HCI_Command',
        'opcode_hex': f"0x{opcode_val:04X}",
        'ogf_hex': f"0x{ogf:02X}",
        'ocf_hex': f"0x{ocf:03X}",
        'ogf': ogf,
        'ocf': ocf,
        'name': cmd_name,
        'param_length': param_len,
        'params_hex': params.hex()[:64] if params else ''
    }

    if (ogf, ocf) == (0x03, 0x0003):
        result['description'] = "Reset Bluetooth Controller"
    elif (ogf, ocf) == (0x01, 0x0006) and len(params) >= 3:
        handle = struct.unpack('<H', params[0:2])[0]
        reason = params[2]
        result['connection_handle'] = f"0x{handle:04X}"
        result['reason_hex'] = f"0x{reason:02X}"
        result['reason_str'] = HCI_ERRORS.get(reason, f"Unknown({reason})")
    elif (ogf, ocf) == (0x01, 0x0005) and len(params) >= 11:
        bd_addr = ':'.join(f'{b:02X}' for b in params[5::-1])
        pkt_type = struct.unpack('<H', params[6:8])[0]
        result['bd_addr'] = bd_addr
        result['packet_type_hex'] = f"0x{pkt_type:04X}"

    return result
