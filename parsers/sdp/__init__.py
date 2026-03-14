# -*- coding: utf-8 -*-
"""
SDP (Service Discovery Protocol) 解析。
通常跑在 L2CAP 动态信道上（PSM 0x0001），后续可在 L2CAP 层按 PSM/CID 上下文调用。
"""
from .constants import SDP_PDU_NAMES
from .parser import parse_sdp

__all__ = ["SDP_PDU_NAMES", "parse_sdp"]
