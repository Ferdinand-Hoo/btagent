#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BTSnoop 解析器入口（CLI）。
解析分层：BTSnoop 文件 → HCI(命令/事件/ACL) → L2CAP(信令/ATT) → SDP 等可扩展。
"""
import sys
import argparse
from pathlib import Path

# 脚本直接运行时把项目根加入 path，以包方式导入
if __name__ == '__main__':
    _root = Path(__file__).resolve().parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

try:
    from parsers.btsnoop import BTSnoopParser
    from parsers.reporter import export_markdown, export_json
except ImportError:
    from .btsnoop import BTSnoopParser
    from .reporter import export_markdown, export_json


def main():
    parser = argparse.ArgumentParser(
        description="BTSnoop HCI 解析器 (分层: HCI → L2CAP → SDP)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('input', help='BTSnoop 文件 (.log, .cfa, .btsnoop)')
    parser.add_argument('-o', '--output', help='输出路径')
    parser.add_argument('-f', '--format', choices=['markdown', 'json'], default='markdown')
    parser.add_argument('-n', '--max-records', type=int, default=0, help='最多解析条数，0=不限制')

    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: File not found - {args.input}")
        sys.exit(1)

    try:
        print(f"Parsing: {args.input}")
        p = BTSnoopParser(args.input)
        p.parse()
        print(f"Parsed {len(p.records)} records")

        base = Path(args.input).stem
        out = args.output or f"{base}_parsed.{'md' if args.format == 'markdown' else 'json'}"
        if args.format == 'markdown':
            export_markdown(p, out, args.max_records)
        else:
            export_json(p, out, args.max_records)
        print(f"Output: {out}")

        stats = p.analyze()
        print(f"  Packets: {stats['total_packets']} | Duration: {stats['duration_ms']:.2f} ms")
        print(f"  Commands: {stats['commands']} | Events: {stats['events']} | ACL TX: {stats['acl_tx']} RX: {stats['acl_rx']}")
        print(f"  Command Completes: {len(stats['command_completes'])} | Errors: {stats['error_count']}")
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
