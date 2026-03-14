# -*- coding: utf-8 -*-
"""
HCI 事件解析 (Controller -> Host)
格式: Event Code(1) + Parameter Length(1) + Parameters(n)。
"""
import struct
from typing import Dict, Any

from .constants import (
    parse_opcode,
    HCI_COMMANDS,
    HCI_EVENTS,
    HCI_ERRORS,
    EVENT_COMMAND_COMPLETE,
    EVENT_COMMAND_STATUS,
    EVENT_CONNECTION_COMPLETE,
    EVENT_CONNECTION_REQUEST,
    EVENT_DISCONNECTION_COMPLETE,
    EVENT_NUMBER_OF_COMPLETED_PACKETS,
)


def parse_hci_event(data: bytes) -> Dict[str, Any]:
    """解析 HCI Event 包体，返回结构化 dict。"""
    if len(data) < 2:
        return {'error': f'Too short: {len(data)} bytes'}

    event_code = data[0]
    param_len = data[1]
    params = data[2:2 + param_len] if param_len > 0 else b''

    event_name = HCI_EVENTS.get(event_code, f"Event_0x{event_code:02X}")
    result = {
        'type': 'HCI_Event',
        'event_code_hex': f"0x{event_code:02X}",
        'name': event_name,
        'param_length': param_len,
        'params_hex': params.hex()[:64] if params else ''
    }

    if event_code == EVENT_COMMAND_COMPLETE and len(params) >= 4:
        num_cmd, status = params[0], params[3]
        opcode_val = struct.unpack('<H', params[1:3])[0]
        ogf, ocf = parse_opcode(opcode_val)
        cmd_name = HCI_COMMANDS.get((ogf, ocf), f"OGF=0x{ogf:02X}, OCF=0x{ocf:03X}")
        result['num_hci_command_packets'] = num_cmd
        result['command_opcode_hex'] = f"0x{opcode_val:04X}"
        result['command_name'] = cmd_name
        result['ogf'] = f"0x{ogf:02X}"
        result['ocf'] = f"0x{ocf:03X}"
        result['status_hex'] = f"0x{status:02X}"
        result['status_str'] = HCI_ERRORS.get(status, f"Unknown({status})")
        if len(params) > 4:
            result['return_params_hex'] = params[4:].hex()[:64]

    elif event_code == EVENT_COMMAND_STATUS and len(params) >= 4:
        status, num_cmd = params[0], params[1]
        opcode_val = struct.unpack('<H', params[2:4])[0]
        ogf, ocf = parse_opcode(opcode_val)
        result['status_hex'] = f"0x{status:02X}"
        result['status_str'] = HCI_ERRORS.get(status, f"Unknown({status})")
        result['num_hci_command_packets'] = num_cmd
        result['command_opcode_hex'] = f"0x{opcode_val:04X}"
        result['ogf'] = f"0x{ogf:02X}"
        result['ocf'] = f"0x{ocf:03X}"

    elif event_code == EVENT_CONNECTION_COMPLETE and len(params) >= 11:
        status, link_type, enc_mode = params[0], params[9], params[10]
        handle = struct.unpack('<H', params[1:3])[0]
        bd_addr = ':'.join(f'{b:02X}' for b in params[3:9][::-1])
        link_type_str = {0: "SCO", 1: "ACL", 2: "eSCO"}.get(link_type, f"Reserved({link_type})")
        result['status_hex'] = f"0x{status:02X}"
        result['status_str'] = HCI_ERRORS.get(status, f"Unknown({status})")
        result['connection_handle_hex'] = f"0x{handle:04X}"
        result['bd_addr'] = bd_addr
        result['link_type'] = link_type_str
        result['encryption_mode'] = enc_mode

    elif event_code == EVENT_CONNECTION_REQUEST and len(params) >= 10:
        bd_addr = ':'.join(f'{b:02X}' for b in params[0:6][::-1])
        result['bd_addr'] = bd_addr
        result['class_of_device_hex'] = params[6:9].hex()
        result['link_type'] = "ACL" if params[9] == 1 else "SCO" if params[9] == 0 else str(params[9])

    elif event_code == EVENT_DISCONNECTION_COMPLETE and len(params) >= 4:
        status, reason = params[0], params[3]
        handle = struct.unpack('<H', params[1:3])[0]
        result['status_hex'] = f"0x{status:02X}"
        result['status_str'] = HCI_ERRORS.get(status, f"Unknown({status})")
        result['connection_handle_hex'] = f"0x{handle:04X}"
        result['reason_hex'] = f"0x{reason:02X}"
        result['reason_str'] = HCI_ERRORS.get(reason, f"Unknown({reason})")

    elif event_code == EVENT_NUMBER_OF_COMPLETED_PACKETS and len(params) >= 1:
        num_handles = params[0]
        handles_info = []
        off = 1
        for _ in range(num_handles):
            if len(params) >= off + 4:
                h = struct.unpack('<H', params[off:off + 2])[0]
                count = struct.unpack('<H', params[off + 2:off + 4])[0]
                handles_info.append({'connection_handle': f"0x{h:04X}", 'completed_packets': count})
                off += 4
        result['number_of_handles'] = num_handles
        result['handles_info'] = handles_info

    return result
