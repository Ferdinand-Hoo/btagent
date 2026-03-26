# BTAgent

将 **BTSnoop 格式** 的蓝牙 HCI 抓包（`.log` / `.cfa` / `.btsnoop`）解析为结构化记录，并导出 **Markdown / JSON** 报告，或通过 **Web 界面** 上传查看 HTML 报告。解析按协议栈分层：**BTSnoop 文件 → HCI（命令 / 事件 / ACL）→ L2CAP（信令、ATT）**，SDP 等可在下层继续扩展。

适用于 Linux / 车机等环境下的蓝牙协议排障与日志分析。

## 功能概览

- 读取标准 BTSnoop 文件头与记录体，按 HCI 类型分发解析
- HCI：命令、事件、ACL 数据；ACL 内按 L2CAP CID 解析信令与 ATT
- 终端统计：包数量、时长、命令/事件/ACL 收发、命令完成与错误汇总
- 导出：`markdown` / `json`（CLI）；浏览器内 **HTML** 报告（Web）
- 设计说明见仓库内 [`docs/module-design.md`](docs/module-design.md) 与 [`docs/log-parsing-layer-design.md`](docs/log-parsing-layer-design.md)

## 环境要求

- **Python 3.10+**（推荐 3.12）
- 仅使用 CLI 时：标准库即可（从项目根目录运行以保证包导入正确）
- 使用 Web 服务时：需要安装 **Flask**

```bash
pip install flask
```

## 命令行用法

在项目根目录执行（将 `parsers` 作为包导入）：

```bash
python parsers/main.py <BTSnoop文件> [-o 输出路径] [-f markdown|json] [-n 最大记录数]
```

- 未指定 `-o` 时，默认生成 `<输入文件名>_parsed.md` 或 `.json`
- `-n 0` 表示不限制记录数

示例（仓库内自带样例）：

```bash
python parsers/main.py examples/sample_hci.log
python parsers/main.py examples/btsnoop_hci.log -f json -o out.json
```

## Web 服务

启动后默认监听 `8080`，可在浏览器打开上传页或直接绑定本地日志文件。

```bash
# 上传模式：首页选择/拖拽 BTSnoop 文件
python server.py

# 固定解析某个文件（首页直接展示报告）
python server.py examples/sample_hci.log

# 指定端口与监听地址
python server.py --port 9000 --host 127.0.0.1
```

单次上传大小上限为 64 MB（见 `server.py` 中 `MAX_CONTENT_LENGTH`）。

## 项目结构（解析层）

```
parsers/
├── main.py           # CLI 入口
├── btsnoop.py        # BTSnoop 解析与 analyze() 统计
├── reporter.py       # Markdown / JSON 报告
├── reporter_html.py  # HTML 报告（供 server 使用）
├── hci/              # HCI 命令、事件、ACL
├── l2cap/            # L2CAP 信令、ATT
└── sdp/              # SDP 解析框架（可按需接入 ACL）
```

根目录 **`server.py`** 为 Flask 应用，负责上传与 HTML 展示。

## 许可证

MIT
