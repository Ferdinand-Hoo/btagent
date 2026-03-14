# -*- coding: utf-8 -*-
"""
HCI 常量与映射表 (Bluetooth Core Spec Vol 4 Part E)
"""
from typing import Tuple

def parse_opcode(opcode_uint16: int) -> Tuple[int, int]:
    """OGF = bits 15-10, OCF = bits 9-0。例: 0x0C03 -> (0x03, 0x003)."""
    ogf = (opcode_uint16 >> 10) & 0x3F
    ocf = opcode_uint16 & 0x3FF
    return ogf, ocf

HCI_TYPES = {
    0: "SCO_TX", 1: "ACL_TX", 2: "CMD", 3: "EVT", 4: "ACL_RX", 5: "SCO_RX",
}
HCI_TYPES_VENDOR = {
    0: "CMD", 1: "SCO_TX", 2: "ACL_TX", 3: "EVT", 4: "ACL_RX", 5: "SCO_RX",
}

HCI_INDICATORS = {
    0: 0x01, 1: 0x02, 2: 0x03, 3: 0x04, 4: 0x02, 5: 0x03,
}
HCI_INDICATORS_VENDOR = {0: 0x01, 1: 0x03, 2: 0x02, 3: 0x04, 4: 0x02, 5: 0x03}

EVENT_INQUIRY_COMPLETE = 0x01
EVENT_INQUIRY_RESULT = 0x02
EVENT_CONNECTION_COMPLETE = 0x03
EVENT_CONNECTION_REQUEST = 0x04
EVENT_DISCONNECTION_COMPLETE = 0x05
EVENT_COMMAND_COMPLETE = 0x0E
EVENT_COMMAND_STATUS = 0x0F
EVENT_NUMBER_OF_COMPLETED_PACKETS = 0x13
EVENT_PAGE_SCAN_REPETITION_MODE_CHANGE = 0x20
EVENT_IO_CAPABILITY_REQUEST = 0x30
EVENT_LE_META = 0x3E

HCI_COMMANDS = {
    (0x01, 0x0001): "Inquiry", (0x01, 0x0002): "Inquiry Cancel",
    (0x01, 0x0005): "Create Connection", (0x01, 0x0006): "Disconnect",
    (0x01, 0x0009): "Accept Connection Request", (0x01, 0x000F): "Change Connection Packet Type",
    (0x01, 0x0019): "Remote Name Request", (0x01, 0x001D): "Read RSSI",
    (0x02, 0x000D): "Exit Sniff Mode", (0x02, 0x000F): "Write Default Link Policy Settings",
    (0x03, 0x0001): "Set Event Mask", (0x03, 0x0003): "Reset", (0x03, 0x0005): "Set Event Filter",
    (0x03, 0x0013): "Write Local Name", (0x03, 0x0017): "Read Page Timeout",
    (0x03, 0x0018): "Write Page Timeout", (0x03, 0x001A): "Write Scan Enable",
    (0x03, 0x001C): "Write Page Scan Activity", (0x03, 0x001E): "Write Inqury Scan Activity",
    (0x03, 0x0024): "Write Class of Device", (0x03, 0x0033): "Host Buffer Size",
    (0x03, 0x0044): "Read Inquiry Mode", (0x03, 0x0045): "Write Inquiry Mode",
    (0x03, 0x0052): "Write Extended Inqury Response", (0x03, 0x0056): "Write Simple Pairing Mode",
    (0x03, 0x0058): "Read Inquiry Response Transmit Power Level",
    (0x03, 0x005A): "Read Default Erroneous Data Reporting",
    (0x03, 0x006D): "Write LE Host Supported", (0x03, 0x007A): "Write Secure Connections Host Support",
    (0x03, 0x007D): "Read Local OOB Extended Data",
    (0x04, 0x0001): "Read Local Version Information",
    (0x04, 0x0002): "Read Local Supported Commands", (0x04, 0x0003): "Read Local Supported Features",
    (0x04, 0x0004): "Read Local Extended Features", (0x04, 0x0005): "Read Buffer Size",
    (0x04, 0x0009): "Read BD_ADDR", (0x04, 0x0013): "Read Local Extended Features",
    (0x05, 0x0001): "Read Failed Contact Counter", (0x06, 0x0001): "Read Loopback Mode",
    (0x08, 0x0001): "LE Set Event Mask", (0x08, 0x0002): "LE Read Buffer Size",
    (0x08, 0x0003): "LE Read Local Supported Features Page 0",
    (0x08, 0x0006): "LE Set Advertising Parameters",
    (0x08, 0x0007): "LE Read Advertising Channel TX Power",
    (0x08, 0x0008): "LE Set Advertising Data", (0x08, 0x000A): "LE Set Advertising Enable",
    (0x08, 0x000D): "LE Create Connection", (0x08, 0x000F): "LE Read Filter Accept List Size",
    (0x08, 0x001C): "LE Read Supported States",
    (0x3F, 0x0007): "Vendor Command 0x007", (0x3F, 0x001D): "Vendor Command 0x01D",
    (0x3F, 0x0028): "Vendor Command 0x028", (0x3F, 0x0029): "Vendor Command 0x029",
    (0x3F, 0x0073): "Vendor Command 0x073",
}

HCI_EVENTS = {
    EVENT_INQUIRY_COMPLETE: "Inquiry Complete", EVENT_INQUIRY_RESULT: "Inquiry Result",
    EVENT_CONNECTION_COMPLETE: "Connection Complete", EVENT_CONNECTION_REQUEST: "Connection Request",
    EVENT_DISCONNECTION_COMPLETE: "Disconnection Complete",
    EVENT_COMMAND_COMPLETE: "Command Complete", EVENT_COMMAND_STATUS: "Command Status",
    EVENT_NUMBER_OF_COMPLETED_PACKETS: "Number of Completed Packets",
    EVENT_IO_CAPABILITY_REQUEST: "IO Capability Request", EVENT_LE_META: "LE Meta Event",
    EVENT_PAGE_SCAN_REPETITION_MODE_CHANGE: "Page Scan Repetition Mode Change",
}

HCI_ERRORS = {
    0x00: "Success", 0x01: "Unknown HCI Command", 0x02: "Unknown Connection Identifier",
    0x03: "Hardware Failure", 0x04: "Page Timeout", 0x05: "Authentication Failure",
    0x06: "PIN or Key Missing", 0x07: "Memory Capacity Exceeded", 0x08: "Connection Timeout",
    0x09: "Connection Limit Exceeded", 0x0C: "Command Disallowed",
    0x12: "Invalid HCI Command Parameters", 0x13: "Remote User Terminated Connection",
    0x16: "Connection Terminated By Local Host", 0x22: "LMP Response Timeout",
}
