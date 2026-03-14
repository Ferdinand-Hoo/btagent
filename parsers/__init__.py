# -*- coding: utf-8 -*-
"""
BTSnoop 解析器：分层架构
- btsnoop: 文件格式与记录编排 (HCIRecord, BTSnoopParser)
- hci: HCI 命令 / 事件 / ACL 解析
- l2cap: L2CAP 信令 / ATT 解析 (由 HCI ACL 调用)
- sdp: SDP 解析 (可接在 L2CAP 上扩展)
"""
from .btsnoop import BTSnoopParser, HCIRecord

__all__ = ["BTSnoopParser", "HCIRecord"]
