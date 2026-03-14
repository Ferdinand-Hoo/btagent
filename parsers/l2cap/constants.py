# -*- coding: utf-8 -*-
"""
L2CAP 常量：CID、信令码、ATT 操作码等。
"""
# 常用 CID (Channel ID)
L2CAP_CID_NAMES = {
    0x0001: "L2CAP_Signaling",
    0x0002: "Connectionless",
    0x0004: "ATT",
    0x0005: "LE_Signaling",
    0x0006: "SM_LE",
    0x0007: "SM_BREDR",
}

# L2CAP 信令命令码 (Code)
L2CAP_SIGNALING_CODES = {
    0x01: "Command_Reject",
    0x02: "Connection_Request",
    0x03: "Connection_Response",
    0x04: "Configure_Request",
    0x05: "Configure_Response",
    0x06: "Disconnection_Request",
    0x07: "Disconnection_Response",
    0x08: "Echo_Request",
    0x09: "Echo_Response",
    0x0A: "Information_Request",
    0x0B: "Information_Response",
}

# ATT 操作码 (部分)
ATT_OPCODES = {
    0x01: "Error_Response",
    0x04: "Find_Information_Request",
    0x05: "Find_Information_Response",
    0x08: "Read_By_Type_Request",
    0x09: "Read_By_Type_Response",
    0x0A: "Read_Request",
    0x0B: "Read_Response",
    0x0C: "Read_Blob_Request",
    0x0D: "Read_Blob_Response",
    0x12: "Write_Request",
    0x13: "Write_Response",
    0x52: "Write_Command",
    0xD2: "Signed_Write_Command",
}
