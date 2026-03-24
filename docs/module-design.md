# BTAgent 解析层模块设计文档

## 1. 设计目标

将 BTSnoop 二进制日志文件解析为**结构化的逐条记录**，每条记录携带按蓝牙协议栈各层解析后的结果，供上层做统计分析、诊断报告和 AI 推理使用。

**核心原则：**
- **分层解析**：文件层 → HCI 层 → L2CAP 层 → 应用层，每层只解析本层协议。
- **单一职责**：解析、统计分析、报告生成各自独立，互不耦合。
- **可扩展**：新协议只需在对应层挂接新解析函数，不需改动上层。

---

## 2. 模块总览

```
parsers/
├── main.py              # CLI 入口
├── btsnoop.py           # 文件解析 + 统计分析
├── reporter.py          # 报告生成（Markdown / JSON）
├── hci/
│   ├── __init__.py      # HCI 层公开接口
│   ├── constants.py     # HCI 常量与映射表
│   ├── command.py       # HCI 命令解析
│   ├── event.py         # HCI 事件解析
│   └── acl.py           # HCI ACL 解析 → 调用 L2CAP
├── l2cap/
│   ├── __init__.py      # L2CAP 层公开接口（按 CID 分发）
│   ├── constants.py     # L2CAP 常量（CID、信令码、ATT 操作码）
│   ├── signaling.py     # L2CAP 信令解析
│   └── att.py           # ATT 属性协议解析
└── sdp/
    ├── __init__.py      # SDP 层公开接口
    ├── constants.py     # SDP PDU 常量
    └── parser.py        # SDP PDU 解析（框架已就绪，待接入 L2CAP）
```

---

## 3. 数据流

```
BTSnoop 文件
  └─► BTSnoopParser.parse()         [btsnoop.py]
        ├─► parse_hci_command()     [hci/command.py]   flags == 1
        ├─► parse_hci_event()       [hci/event.py]     flags == 4
        └─► parse_hci_acl()         [hci/acl.py]       flags == 2
              └─► parse_l2cap_payload(cid, payload)    [l2cap/__init__.py]
                    ├─► parse_l2cap_signaling()        [l2cap/signaling.py]  CID 0x0001
                    ├─► parse_att()                    [l2cap/att.py]        CID 0x0004
                    └─► (可扩展) parse_sdp() / RFCOMM / A2DP …

  ↓ 每条记录输出为 HCIRecord.parsed

BTSnoopParser.analyze()              [btsnoop.py]
  └─► 遍历 records，汇总统计（命令数、连接建立/断开、错误、ACL TX/RX）

export_markdown() / export_json()    [reporter.py]
  └─► 读取 parser.records + parser.analyze()，生成报告文件
```

---

## 4. 各模块职责

### 4.1 `main.py` — CLI 入口

**职责：**
- 解析命令行参数（输入文件、输出路径、格式、最大记录数）
- 创建 `BTSnoopParser`，调用 `parse()`
- 调用 `reporter.export_markdown()` 或 `reporter.export_json()`
- 打印简要统计摘要到终端

**不负责：** 任何解析逻辑、任何报告格式化逻辑。

---

### 4.2 `btsnoop.py` — 文件解析 + 统计分析

**职责：**

| 函数/方法 | 说明 |
|-----------|------|
| `BTSnoopParser.parse()` | 读取并校验 BTSnoop 文件魔数；按 24 字节固定头循环拆包；按包体首字节判断 HCI 类型；调用 `_parse_payload()` |
| `_strip_hci_indicator()` | 剥掉包体首字节的 HCI type indicator，得到净载荷 |
| `_parse_payload()` | 按 `flags`（包体首字节）分发：1→命令，4→事件，2→ACL，其余→raw hex |
| `BTSnoopParser.analyze()` | 遍历全部记录，统计命令数、事件数、ACL TX/RX 数、连接建立/断开事件、错误事件、使用过的连接句柄 |
| `HCIRecord` | 单条记录数据结构（dataclass），包含时间戳、方向、类型、原始数据、解析结果 |

**不负责：** 报告文件的生成与格式化（由 `reporter.py` 负责）。

**`HCIRecord` 字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `seq` | int | 记录序号（从 1 开始） |
| `timestamp_abs` | int | 绝对时间戳，微秒（文件原始值） |
| `timestamp_abs_sec` | float | 绝对时间戳，秒 |
| `timestamp_rel` | float | 相对时间，毫秒（相对首条记录） |
| `flags` | int | 包体首字节（HCI 类型：1/2/3/4） |
| `packet_type` | str | 类型名称（CMD / ACL_DATA / SCO_DATA / EVENT） |
| `direction` | str | 方向（Host→Controller / Controller→Host） |
| `length` | int | 本记录实际包体长度 |
| `data` | bytes | 包体原始字节 |
| `payload` | bytes | 剥掉 HCI Indicator 后的净载荷 |
| `parsed` | dict | 各层解析结果合并后的结构化字典 |

---

### 4.3 `reporter.py` — 报告生成

**职责：**
- 将 `BTSnoopParser` 的解析结果格式化并导出为文件
- 提供 `export_markdown(parser, output_path, max_records)` — Markdown 报告
- 提供 `export_json(parser, output_path, max_records)` — JSON 导出
- 包含时间格式化工具函数 `_format_abs_time_hms()`

**Markdown 报告包含以下章节：**
1. 概览统计（总包数、时间范围、各类型计数、错误数）
2. Command Complete 验证表（前 10 条，含命令名、OGF/OCF、状态）
3. 连接建立事件表
4. 断开连接事件表
5. 错误事件表（前 20 条）
6. 完整通信流程时序表
7. 分析总结

**不负责：** 任何解析逻辑，不直接读取二进制文件。

---

### 4.4 `hci/` — HCI 层

#### `hci/constants.py` — HCI 常量

**负责：** 提供 HCI 协议所需的全部常量与映射表，不含任何解析逻辑。

| 常量/函数 | 说明 |
|-----------|------|
| `parse_opcode(uint16)` | 从 HCI opcode 拆出 OGF（高 6 位）和 OCF（低 10 位） |
| `HCI_TYPES` | 包体首字节 → 类型名称映射（1: CMD, 2: ACL_DATA 等） |
| `HCI_INDICATORS` | 各类型对应的 HCI Indicator 字节值 |
| `HCI_COMMANDS` | (OGF, OCF) → 命令名称映射表 |
| `HCI_EVENTS` | 事件码 → 事件名称映射表 |
| `HCI_ERRORS` | 状态码 → 错误描述映射表（0x00=Success 等） |
| `EVENT_*` 系列常量 | 常用事件码（CONNECTION_COMPLETE、COMMAND_COMPLETE 等） |

#### `hci/command.py` — HCI 命令解析

**负责：** 解析 `flags == 1` 的 HCI Command 包体。

格式：`Opcode(2, LE) + Parameter Length(1) + Parameters(n)`

输出 `parsed` 字段包含：
- `type`: `"HCI_Command"`
- `opcode_hex`, `ogf_hex`, `ocf_hex`, `ogf`, `ocf`
- `name`: 命令名称（查 `HCI_COMMANDS` 映射表）
- `param_length`, `params_hex`
- 部分命令的专有字段（如 Disconnect 的 `connection_handle`、`reason_str`；Create Connection 的 `bd_addr`）

#### `hci/event.py` — HCI 事件解析

**负责：** 解析 `flags == 4` 的 HCI Event 包体。

格式：`Event Code(1) + Parameter Length(1) + Parameters(n)`

已完整解析的事件：

| 事件码 | 事件名 | 解析出的专有字段 |
|--------|--------|-----------------|
| 0x03 | Connection Complete | `connection_handle_hex`, `bd_addr`, `link_type`, `status_str` |
| 0x04 | Connection Request | `bd_addr`, `link_type` |
| 0x05 | Disconnection Complete | `connection_handle_hex`, `reason_str` |
| 0x0E | Command Complete | `command_name`, `ogf`, `ocf`, `status_str`, `return_params_hex` |
| 0x0F | Command Status | `status_str`, `command_opcode_hex` |
| 0x13 | Number of Completed Packets | `handles_info`（句柄 + 完成数列表） |

其余事件码：输出 `event_code_hex` + `name`（已知则为事件名，未知则为 `Event_0xXX`）。

#### `hci/acl.py` — HCI ACL 解析

**负责：** 解析 `flags == 2` 的 HCI ACL Data 包体，并向下调用 L2CAP 层。

格式：`Handle+Flags(2, LE) + Data Length(2, LE) + L2CAP Length(2) + CID(2) + Payload`

解析出：`connection_handle_hex`, `pb_flag`（分片标志）, `bc_flag`

L2CAP 头解析出后，调用 `parse_l2cap_payload(cid, l2cap_payload)`，结果合并到 `result['l2cap']`。

---

### 4.5 `l2cap/` — L2CAP 层

#### `l2cap/constants.py` — L2CAP 常量

**负责：** 提供 L2CAP 相关的全部常量，不含解析逻辑。

| 常量 | 说明 |
|------|------|
| `L2CAP_CID_NAMES` | 固定 CID → 名称映射（0x0001: L2CAP_Signaling, 0x0004: ATT 等） |
| `L2CAP_SIGNALING_CODES` | 信令命令码 → 名称映射（Connection Request/Response、Configure 等） |
| `ATT_OPCODES` | ATT 操作码 → 名称映射（Read Request/Response、Write Command 等） |

#### `l2cap/__init__.py` — L2CAP 分发入口

**负责：** 按 CID 将 L2CAP payload 分发到对应子解析器，是整个 L2CAP 层的唯一入口。

```
parse_l2cap_payload(cid, payload):
    CID 0x0001 → parse_l2cap_signaling()
    CID 0x0004 → parse_att()
    其他 CID   → 返回 cid_hex + payload_hex（待扩展）
```

扩展新协议时，只需在此处增加 `if cid == xxx` 分支。

#### `l2cap/signaling.py` — L2CAP 信令解析

**负责：** 解析 CID 0x0001 的信令信道 payload。

格式：`Code(1) + Identifier(1) + Length(2, LE) + Data`

输出：`type: "L2CAP_Signaling"`, `code_name`（查 `L2CAP_SIGNALING_CODES`）, `identifier`, `payload_hex`

当前解析到信令命令级别（连接请求/响应、配置请求/响应、断开请求/响应等），payload 字段保留供深度解析扩展。

#### `l2cap/att.py` — ATT 属性协议解析

**负责：** 解析 CID 0x0004 的 ATT 信道 payload。

格式：`ATT Opcode(1) + Parameters`

输出：`type: "ATT"`, `att_opcode_hex`, `att_operation`（查 `ATT_OPCODES`）, `payload_hex`

---

### 4.6 `sdp/` — SDP 层（框架已就绪，未接入）

**职责：** 解析 SDP（Service Discovery Protocol）PDU。

格式：`PDU ID(1) + Transaction ID(2, BE) + Parameter Length(2, BE) + Parameters`

当前实现：解析出 `pdu_name`、`transaction_id`、`parameter_length`，payload 保留为 hex。

**待完成：** 在 `l2cap/__init__.py` 中按 PSM 0x0001 或对应动态 CID 挂接 `parse_sdp()`。

---

## 5. 模块依赖关系

```
main.py
  ├── btsnoop.py
  │     └── hci/__init__.py
  │           ├── hci/constants.py
  │           ├── hci/command.py  ──► hci/constants.py
  │           ├── hci/event.py    ──► hci/constants.py
  │           └── hci/acl.py      ──► l2cap/__init__.py
  │                                       ├── l2cap/constants.py
  │                                       ├── l2cap/signaling.py ──► l2cap/constants.py
  │                                       └── l2cap/att.py       ──► l2cap/constants.py
  └── reporter.py
        └── hci/__init__.py  (仅用 HCI_EVENTS、EVENT_* 常量做报告格式化)
```

**依赖方向：** 单向，上层调用下层，下层不感知上层。`sdp/` 目前独立，未被任何��块 import。

---

## 6. 扩展指南

### 扩展 L2CAP 上层协议（如 RFCOMM、A2DP、AVRCP）

在 `l2cap/__init__.py` 的 `parse_l2cap_payload()` 中增加分支：

```python
# 示例：挂接 RFCOMM（PSM 0x0003 对应的动态 CID 需在建连时追踪）
if cid == 动态CID:
    from ..rfcomm import parse_rfcomm
    return parse_rfcomm(payload)
```

新建 `parsers/rfcomm/` 子包，结构参考 `l2cap/`（`__init__.py` + `constants.py` + `parser.py`）。

### 扩展 HCI 命令/事件的深度解析

在 `hci/command.py` 或 `hci/event.py` 的 if-elif 链中增加对新 opcode/event_code 的专有字段解析。常量统一加到 `hci/constants.py`。

### 接入 SDP

1. 在 `l2cap/__init__.py` 中识别 SDP 动态 CID，调用 `from ..sdp import parse_sdp`
2. 在 `sdp/parser.py` 中补充 Parameters 的逐字段解析

---

## 7. 当前实现状态

| 模块 | 状态 |
|------|------|
| BTSnoop 文件解析 | 完整实现 |
| HCI 命令解析 | 核心命令已覆盖，可持续补充 |
| HCI 事件解析 | 核心事件已完整解析 |
| HCI ACL 解析 | 完整实现 |
| L2CAP 信令 | 命令码级别已识别，payload 待深度解析 |
| ATT | 操作码级别已识别 |
| SDP | 框架就绪，未接入 L2CAP 分发 |
| RFCOMM / A2DP / AVRCP | 未实现 |
| 统计分析 | 连接建立/断开、命令完成、ACL TX/RX、错误 |
| Markdown 报告 | 完整实现 |
| JSON 导出 | 完整实现 |
