## Architecture

```mermaid
flowchart TD

User[Developer / User]

User --> Cursor[Cursor AI Agent]

Cursor --> MCP[MCP Protocol Layer]

MCP --> Tabby[Tabby MCP Server]
MCP --> BTAgent[BTAgent Analyzer]

subgraph Embedded_Device["Embedded Linux Device (Vehicle / ECU)"]
    SSH[SSH Service]
    BTMON[btmon / hcidump]
    BlueZ[BlueZ Bluetooth Stack]
end

Tabby --> SSH
SSH --> BTMON
BTMON --> BlueZ

BTMON --> HCILog[Generated HCI Log]

HCILog --> Tabby

Tabby --> MCP

MCP --> BTAgent

BTAgent --> Parser[HCI Log Parser]

Parser --> Analyzer[Bluetooth Protocol Analyzer]

Analyzer --> Report[Bluetooth Diagnostic Report]

Report --> Cursor
Cursor --> User
```

---

## HCI Log Collection Workflow

```mermaid
sequenceDiagram

participant User
participant Agent as Cursor Agent
participant Tabby as Tabby MCP
participant Vehicle as Vehicle Linux
participant BTAgent as BTAgent Analyzer

User->>Agent: 分析蓝牙连接失败

Agent->>Tabby: run_command("timeout 10 btmon > hci.log")

Tabby->>Vehicle: execute btmon
Vehicle-->>Tabby: return hci.log

Tabby-->>Agent: hci.log

Agent->>BTAgent: analyze_hci_log(hci.log)

BTAgent->>BTAgent: parse ACL / L2CAP / AVRCP

BTAgent-->>Agent: Diagnostic Report

Agent-->>User: 蓝牙问题分析结果
```

---

## Parser 分层架构（BTSnoop / HCI 解析）

解析采用分层设计，便于按协议扩展（HCI → L2CAP → SDP / ATT / RFCOMM 等）。

```
BTSnoop 文件
    → parsers/btsnoop.py (BTSnoopParser)
        → 按 record.flags 分发：
            • Host→Controller (CMD)  → parsers/hci/command.py  (HCI 命令)
            • Controller→Host (EVT)  → parsers/hci/event.py    (HCI 事件)
            • ACL 数据               → parsers/hci/acl.py     (ACL 头 + L2CAP 头)
    → ACL 内按 CID 分发：
        → parsers/l2cap/ (parse_l2cap_payload)
            • CID 0x0001 信令  → l2cap/signaling.py
            • CID 0x0004 ATT   → l2cap/att.py
            • 其他 CID/PSM     → 可扩展 SDP、RFCOMM 等
```

**目录与职责：**

| 目录/文件 | 职责 |
|-----------|------|
| `parsers/btsnoop.py` | 读 BTSnoop、拆记录、剥 HCI Indicator、按 flags 调用 HCI 层 |
| `parsers/hci/` | HCI 命令 / 事件 / ACL 解析；ACL 内调用 L2CAP |
| `parsers/l2cap/` | L2CAP 头、信令、ATT；按 CID 分发，可挂接 SDP 等 |
| `parsers/sdp/` | SDP PDU 解析（占位）；可在 L2CAP 层按 PSM/CID 挂接 |

**扩展方式：** 新增协议（如 RFCOMM）时：在 `parsers/` 下建子包（如 `rfcomm/`），在 L2CAP 的 `parse_l2cap_payload` 中按 CID 或 PSM 识别并调用对应解析函数，将结果合并到 `record.parsed`。

---

## 日志解析层：分层数据流

```mermaid
flowchart LR
    A[BTSnoop 文件] --> B[BTSnoopParser]
    B --> C[HCI: CMD / EVT / ACL]
    C --> D[L2CAP 信令 + 按 CID 分发]
    D --> E[ATT · SDP · RFCOMM · A2DP · AVRCP …]
    E --> F[record.parsed]
```

- **已实现**：HCI 命令/事件/ACL，L2CAP 信令，ATT。
- **扩展**：在 `parse_l2cap_payload` 中按 CID/PSM 挂接新解析器（SDP PSM 0x0001、RFCOMM 0x0003、A2DP 0x0019、AVRCP 0x0017 等），结果合并进 `record.parsed`。

---

## 单条记录解析流程（决策流程）

一条 BTSnoop 记录从原始 payload 到 `record.parsed` 的分发与解析决策。

```mermaid
flowchart TD
    A["一条 BTSnoop 记录\nrecord.payload"] --> B{record.flags?}
    B -->|"0 (CMD)"| C["parse_hci_command\n→ HCI 命令"]
    B -->|"3 (EVT)"| D["parse_hci_event\n→ HCI 事件"]
    B -->|"2/4/1/5 (ACL)"| E["parse_hci_acl\n→ ACL 头 + L2CAP 头"]
    C --> Z["record.parsed"]
    D --> Z
    E --> F{cid?}
    F -->|"0x0001"| G["parse_l2cap_signaling\n→ L2CAP 信令"]
    F -->|"0x0004"| H["parse_att\n→ ATT"]
    F -->|"其他"| I["cid_hex + payload_hex"]
    G --> Z
    H --> Z
    I --> Z
```

---

## 解析器调用链（自上而下）

从 CLI 入口到各层解析函数的调用顺序。

```mermaid
flowchart TB
    subgraph Entry["入口"]
        Main["main.py\nCLI"]
    end

    subgraph File["文件与分发"]
        Parse["BTSnoopParser.parse()"]
        Strip["_strip_hci_indicator()"]
        Payload["_parse_payload(record)"]
    end

    subgraph HCI["HCI 层"]
        ParseCmd["parse_hci_command()"]
        ParseEvt["parse_hci_event()"]
        ParseACL["parse_hci_acl()"]
    end

    subgraph L2CAP["L2CAP 层"]
        L2Payload["parse_l2cap_payload(cid, payload)"]
        L2Sig["parse_l2cap_signaling()"]
        L2Att["parse_att()"]
    end

    Main --> Parse
    Parse --> Strip
    Parse --> Payload
    Payload --> ParseCmd
    Payload --> ParseEvt
    Payload --> ParseACL
    ParseACL --> L2Payload
    L2Payload --> L2Sig
    L2Payload --> L2Att
```

---

## 解析层模块依赖

各 Python 模块的 import 与调用关系（仅解析层）。

```mermaid
flowchart LR
    subgraph Entry["入口"]
        main["main.py"]
    end

    subgraph Core["核心"]
        btsnoop["btsnoop.py"]
        hci_init["hci/__init__.py"]
    end

    subgraph HCI["hci"]
        hci_const["constants"]
        command["command.py"]
        event["event.py"]
        acl["acl.py"]
    end

    subgraph L2CAP["l2cap"]
        l2cap_init["__init__.py"]
        l2cap_const["constants"]
        signaling["signaling.py"]
        att["att.py"]
    end

    subgraph SDP["sdp"]
        sdp_parser["parser.py"]
    end

    main --> btsnoop
    btsnoop --> hci_init
    hci_init --> hci_const
    hci_init --> command
    hci_init --> event
    hci_init --> acl
    command --> hci_const
    event --> hci_const
    acl --> l2cap_init
    l2cap_init --> l2cap_const
    l2cap_init --> signaling
    l2cap_init --> att
    signaling --> l2cap_const
    att --> l2cap_const
```

---

## 日志解析层边界

在整体系统中，**日志解析层**对应下图中从「HCI Log / BTSnoop」到「结构化解析结果」的整条链路；上游是日志采集（如 Tabby + btmon），下游是分析与报告（Bluetooth Protocol Analyzer → Report）。

```mermaid
flowchart LR
    subgraph Collect["日志采集"]
        BTMON["btmon / 设备"]
        RawLog["HCI Log\nBTSnoop 文件"]
    end

    subgraph ParseLayer["日志解析层（本项目）"]
        Parser["BTSnoopParser\n+ HCI / L2CAP / ATT"]
        Struct["HCIRecord\n结构化解析结果"]
    end

    subgraph Downstream["下游"]
        Analyzer["协议分析 / 诊断"]
        Report["诊断报告"]
    end

    BTMON --> RawLog
    RawLog --> Parser
    Parser --> Struct
    Struct --> Analyzer
    Analyzer --> Report
```