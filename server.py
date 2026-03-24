#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BTAgent Web 服务（标准库实现，无需第三方依赖）。

用法：
  python server.py [log_file] [--port PORT]

示例：
  python server.py examples/sample_hci.log
  python server.py examples/sample_hci.log --port 9000

访问 http://localhost:8080 即可查看报告。
"""
import sys
import argparse
import threading
import webbrowser
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# 把项目根加入 path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from parsers.btsnoop import BTSnoopParser
from parsers.reporter_html import build_html

# ── 全局解析器缓存（避免每次请求重新解析） ──
_parser_cache: dict[str, BTSnoopParser] = {}


def _get_parser(log_path: str) -> BTSnoopParser:
    if log_path not in _parser_cache:
        p = BTSnoopParser(log_path)
        p.parse()
        _parser_cache[log_path] = p
    return _parser_cache[log_path]


# ── 上传页 HTML ──
_UPLOAD_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>BTAgent — 上传日志</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #0f1117; color: #e2e8f0;
    display: flex; align-items: center; justify-content: center;
    min-height: 100vh;
  }
  .card {
    background: #1a202c; border: 1px solid #2d3748;
    border-radius: 14px; padding: 40px 48px; width: 420px; text-align: center;
  }
  h1 { font-size: 1.4rem; color: #63b3ed; margin-bottom: 8px; }
  p  { font-size: 0.85rem; color: #718096; margin-bottom: 28px; }
  .drop-zone {
    border: 2px dashed #4a5568; border-radius: 10px;
    padding: 36px 20px; cursor: pointer; margin-bottom: 20px;
    transition: border-color 0.2s;
  }
  .drop-zone:hover, .drop-zone.over { border-color: #63b3ed; }
  .drop-zone .icon { font-size: 2rem; margin-bottom: 10px; }
  .drop-zone .hint { font-size: 0.8rem; color: #718096; }
  input[type=file] { display: none; }
  button {
    background: #2b6cb0; color: #fff; border: none;
    padding: 10px 32px; border-radius: 8px; font-size: 0.9rem;
    cursor: pointer; width: 100%;
  }
  button:hover { background: #3182ce; }
  #filename { font-size: 0.82rem; color: #68d391; margin-top: 10px; }
</style>
</head>
<body>
<div class="card">
  <h1>🔵 BTAgent</h1>
  <p>上传 BTSnoop HCI 日志文件，即时查看解析报告</p>
  <form method="POST" action="/upload" enctype="multipart/form-data" id="form">
    <div class="drop-zone" id="drop-zone" onclick="document.getElementById('file-input').click()">
      <div class="icon">📂</div>
      <div>点击或拖拽文件到此处</div>
      <div class="hint">.log / .cfa / .btsnoop</div>
    </div>
    <input type="file" id="file-input" name="logfile" accept=".log,.cfa,.btsnoop">
    <div id="filename">未选择文件</div>
    <br>
    <button type="submit">解析并查看报告 →</button>
  </form>
</div>
<script>
  const input = document.getElementById('file-input');
  const zone  = document.getElementById('drop-zone');
  const label = document.getElementById('filename');
  input.addEventListener('change', () => {
    label.textContent = input.files[0]?.name || '未选择文件';
  });
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('over'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('over'));
  zone.addEventListener('drop', e => {
    e.preventDefault(); zone.classList.remove('over');
    const dt = e.dataTransfer;
    if (dt.files.length) {
      // 把拖入的文件挂到 input，再提交
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(dt.files[0]);
      input.files = dataTransfer.files;
      label.textContent = dt.files[0].name;
    }
  });
</script>
</body>
</html>
"""


def _parse_multipart(data: bytes, boundary: bytes):
    """极简 multipart 解析，只取第一个 file part 的文件名和内容。"""
    delim = b"--" + boundary
    parts = data.split(delim)
    for part in parts[1:]:
        if b"\r\n\r\n" not in part:
            continue
        header_raw, body = part.split(b"\r\n\r\n", 1)
        # 去掉末尾 \r\n--
        body = body.rstrip(b"\r\n").rstrip(b"--").rstrip(b"\r\n")
        headers = header_raw.decode(errors="replace")
        if 'filename="' in headers:
            fname = headers.split('filename="')[1].split('"')[0]
            return fname, body
    return None, None


class Handler(BaseHTTPRequestHandler):
    # 如果启动时指定了固定文件，直接用；否则走上传流程
    fixed_log: str = ""

    def log_message(self, fmt, *args):
        # 只打印简要日志
        print(f"  {self.address_string()} {fmt % args}")

    def _send(self, code: int, ctype: str, body: bytes):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "":
            if self.fixed_log:
                # 直接渲染固定文件
                try:
                    p = _get_parser(self.fixed_log)
                    html = build_html(p)
                    self._send(200, "text/html; charset=utf-8", html.encode())
                except Exception as e:
                    self._send(500, "text/plain", f"解析失败: {e}".encode())
            else:
                self._send(200, "text/html; charset=utf-8", _UPLOAD_PAGE.encode())

        elif path == "/favicon.ico":
            self._send(204, "text/plain", b"")

        else:
            self._send(404, "text/plain", b"Not Found")

    def do_POST(self):
        if self.path != "/upload":
            self._send(404, "text/plain", b"Not Found")
            return

        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._send(400, "text/plain", b"Bad Request")
            return

        boundary = content_type.split("boundary=")[-1].encode()
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)

        fname, file_bytes = _parse_multipart(data, boundary)
        if not fname or not file_bytes:
            self._send(400, "text/plain", "未收到文件".encode())
            return

        # 写到临时文件，解析
        import tempfile, os
        suffix = Path(fname).suffix or ".log"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            p = BTSnoopParser(tmp_path)
            p.file_path = Path(fname)   # 显示原始文件名
            p.parse()
            html = build_html(p)
            self._send(200, "text/html; charset=utf-8", html.encode())
        except Exception as e:
            self._send(500, "text/plain", f"解析失败: {e}".encode())
        finally:
            os.unlink(tmp_path)


def main():
    ap = argparse.ArgumentParser(description="BTAgent Web 服务")
    ap.add_argument("logfile", nargs="?", default="", help="BTSnoop 文件路径（省略则显示上传页）")
    ap.add_argument("--port", type=int, default=8080)
    args = ap.parse_args()

    if args.logfile and not Path(args.logfile).exists():
        print(f"错误: 文件不存在 — {args.logfile}")
        sys.exit(1)

    Handler.fixed_log = args.logfile

    server = HTTPServer(("0.0.0.0", args.port), Handler)
    url = f"http://localhost:{args.port}"
    print(f"\n  BTAgent Web 服务已启动")
    print(f"  访问: {url}")
    if args.logfile:
        print(f"  日志: {args.logfile}")
    else:
        print(f"  模式: 上传文件")
    print(f"  按 Ctrl+C 停止\n")

    # 延迟 0.5s 后自动打开浏览器
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  已停止。")


if __name__ == "__main__":
    main()
