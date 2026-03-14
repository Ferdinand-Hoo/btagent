# 解析器：所有 Py 文件功能与调用顺序

## 文件一览

| 文件 | 功能 | 被谁调用 |
|------|------|----------|
| **parsers/main.py** | CLI 入口：参数、BTSnoopParser、导出、统计 | 用户直接运行 |
| **parsers/__init__.py** | 包导出：BTSnoopParser, HCIRecord | 外部 `from parsers import ...` |
| **parsers/btsnoop.py** | BTSnoop 文件解析、记录编排、按 flags 分发、分析/导出 | main, 外部 import |
| **parsers/hci/__init__.py** | HCI 层导出：常量 + command/event/acl 解析函数 | btsnoop |
| **parsers/hci/constants.py** | HCI 常量：parse_opcode, OGF/OCF 映射, 类型/指示/命令/事件/错误码 | hci/command, hci/event, hci/__init__ |
| **parsers/hci/command.py** | HCI 命令解析 (Host→Controller) | btsnoop → _parse_payload |
| **parsers/hci/event.py** | HCI 事件解析 (Controller→Host) | btsnoop → _parse_payload |
| **parsers/hci/acl.py** | HCI ACL 解析；调 L2CAP 按 CID 解析 | btsnoop → _parse_payload |
| **parsers/l2cap/__init__.py** | L2CAP 入口：parse_l2cap_payload，按 CID 分发 | hci/acl.py |
| **parsers/l2cap/constants.py** | L2CAP 常量：CID 名、信令码、ATT 操作码 | l2cap/__init__, signaling, att |
| **parsers/l2cap/signaling.py** | L2CAP 信令解析 (CID 0x0001) | l2cap/__init__ → parse_l2cap_payload |
| **parsers/l2cap/att.py** | ATT 解析 (CID 0x0004) | l2cap/__init__ → parse_l2cap_payload |
| **parsers/sdp/__init__.py** | SDP 包导出：parse_sdp, SDP_PDU_NAMES | 尚未接入数据流 |
| **parsers/sdp/constants.py** | SDP PDU 名、属性 ID | sdp/parser |
| **parsers/sdp/parser.py** | SDP PDU 解析（占位） | 可在 L2CAP 层按 PSM/CID 挂接 |

---

## 调用顺序（自上而下）

### 1. 入口层

```
main.py (CLI)
  ├─ argparse
  ├─ BTSnoopParser(file_path, vendor_type_map)
  ├─ p.parse()                    → btsnoop.parse()
  ├─ p.export_markdown() / export_json()
  └─ p.analyze()
```

### 2. 文件与分发层

```
btsnoop.py
  ├─ 依赖: hci/__init__ (HCI_TYPES*, HCI_INDICATORS*, parse_hci_command, parse_hci_event, parse_hci_acl)
  │
  ├─ parse()
  │   ├─ 读文件、校验 btsnoop 魔数、解析文件头
  │   └─ 每条记录:
  │       ├─ _strip_hci_indicator()
  │       └─ _parse_payload(record)   ──────────────────────────┐
  │                                                               │
  ├─ _parse_payload(record)  ◄────────────────────────────────────┘
  │   ├─ flags==0     → parse_hci_command(payload)   [hci/command]
  │   ├─ flags==3     → parse_hci_event(payload)      [hci/event]
  │   ├─ flags==2/4/1 → parse_hci_acl(payload)        [hci/acl]  （视 vendor_type_map 与首字节）
  │   └─ 其他         → {'raw_hex': ...}
  │
  ├─ export_markdown() / export_json()  使用 self.records
  └─ analyze()  统计 commands/events/acl_tx/acl_rx 等
```

### 3. HCI 层

```
hci/__init__.py
  ├─ 从 constants 导出: parse_opcode, HCI_*, EVENT_*
  ├─ 从 command 导出: parse_hci_command
  ├─ 从 event 导出:   parse_hci_event
  └─ 从 acl 导出:     parse_hci_acl

hci/constants.py
  └─ 仅被 hci 包内引用，无外部调用

hci/command.py
  └─ 依赖: constants (parse_opcode, HCI_COMMANDS, HCI_ERRORS)
  └─ parse_hci_command(data)  → 返回 dict，不再往下调

hci/event.py
  └─ 依赖: constants (parse_opcode, HCI_*, EVENT_*, HCI_ERRORS)
  └─ parse_hci_event(data)    → 返回 dict，不再往下调

hci/acl.py
  ├─ 依赖: 无 hci 内依赖（延迟导入 l2cap）
  └─ parse_hci_acl(data)
        ├─ 解析 ACL 头 4 字节、L2CAP 头 4 字节
        └─ _get_l2cap() → parse_l2cap_payload(cid, l2cap_payload)   [l2cap/__init__]
```

### 4. L2CAP 层

```
l2cap/__init__.py
  ├─ 依赖: constants (L2CAP_CID_NAMES), signaling (parse_l2cap_signaling), att (parse_att)
  └─ parse_l2cap_payload(cid, payload)
        ├─ cid==0x0001 → parse_l2cap_signaling(payload)   [signaling]
        ├─ cid==0x0004 → parse_att(payload)               [att]
        └─ 其他        → {'cid_hex', 'payload_hex'}

l2cap/constants.py
  └─ 被 __init__, signaling, att 引用

l2cap/signaling.py
  └─ 依赖: constants (L2CAP_SIGNALING_CODES)
  └─ parse_l2cap_signaling(payload)  → 返回 dict，不再往下调

l2cap/att.py
  └─ 依赖: constants (ATT_OPCODES)
  └─ parse_att(payload)  → 返回 dict，不再往下调
```

### 5. SDP 层（当前未接入）

```
sdp/__init__.py    → 导出 parse_sdp, SDP_PDU_NAMES
sdp/constants.py   → SDP_PDU_NAMES, SDP_ATTR_IDS
sdp/parser.py      → parse_sdp(payload)，可被 l2cap 在识别 SDP 信道后调用
```

---

## 单条记录完整调用链

```
BTSnoop 一条记录
  → btsnoop.BTSnoopParser._parse_payload(record)
       │
       ├─ [命令] parse_hci_command(payload)
       │           ← hci/command.py，用 hci/constants
       │
       ├─ [事件] parse_hci_event(payload)
       │           ← hci/event.py，用 hci/constants
       │
       └─ [ACL]  parse_hci_acl(payload)
                   ← hci/acl.py
                   → l2cap.parse_l2cap_payload(cid, l2cap_payload)
                        ← l2cap/__init__.py
                        ├─ cid 0x0001 → parse_l2cap_signaling(payload)  ← l2cap/signaling.py
                        ├─ cid 0x0004 → parse_att(payload)              ← l2cap/att.py
                        └─ 其他 → 仅 cid/payload_hex
```

---

## 依赖关系简图（谁 import 谁）

```
main.py
    └─ parsers.btsnoop (BTSnoopParser, HCIRecord)

parsers/__init__.py
    └─ .btsnoop

btsnoop.py
    └─ .hci (HCI_TYPES*, HCI_INDICATORS*, parse_hci_command, parse_hci_event, parse_hci_acl)

hci/__init__.py
    └─ .constants, .command, .event, .acl

hci/command.py, hci/event.py
    └─ .constants

hci/acl.py
    └─ ..l2cap (延迟: parse_l2cap_payload, L2CAP_CID_NAMES)

l2cap/__init__.py
    └─ .constants, .signaling, .att

l2cap/signaling.py, l2cap/att.py
    └─ .constants

sdp/__init__.py
    └─ .constants, .parser

sdp/parser.py
    └─ .constants
```

以上即所有 Py 文件的功能与调用顺序逻辑。
