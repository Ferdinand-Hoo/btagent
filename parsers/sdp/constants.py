# -*- coding: utf-8 -*-
"""
SDP PDU 与属性常量 (便于后续扩展)。
"""
# SDP PDU 类型 (PDU ID)
SDP_PDU_NAMES = {
    0x01: "SDP_ErrorResponse",
    0x02: "SDP_ServiceSearchRequest",
    0x03: "SDP_ServiceSearchResponse",
    0x04: "SDP_ServiceAttributeRequest",
    0x05: "SDP_ServiceAttributeResponse",
    0x06: "SDP_ServiceSearchAttributeRequest",
    0x07: "SDP_ServiceSearchAttributeResponse",
}

# 常用 SDP 属性 ID (可扩展)
SDP_ATTR_IDS = {
    0x0000: "ServiceRecordHandle",
    0x0001: "ServiceClassIDList",
    0x0004: "ProtocolDescriptorList",
    0x0005: "BrowseGroupList",
    0x0006: "LanguageBaseAttributeIDList",
    0x0009: "BluetoothProfileDescriptorList",
    0x0100: "ServiceName",
    0x0101: "ServiceDescription",
    0x0102: "ProviderName",
}
