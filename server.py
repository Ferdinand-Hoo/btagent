#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BTAgent Web 服务（Flask 实现）。

用法：
  python server.py [log_file] [--port PORT]

示例：
  python server.py examples/sample_hci.log
  python server.py examples/sample_hci.log --port 9000
  python server.py          # 显示上传页

访问 http://localhost:8080 即可查看报告。
"""
import sys
import argparse
import tempfile
import os
from pathlib import Path

from flask import Flask, request, render_template_string

# 把项目根加入 path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from parsers.btsnoop import BTSnoopParser
from parsers.reporter_html import build_html

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  # 最大上传 64 MB

# 启动时指定的固定日志文件（可为空）
_FIXED_LOG: str = ""

# 解析结果缓存（路径 → BTSnoopParser）
_cache: dict[str, BTSnoopParser] = {}


def _get_parser(log_path: str) -> BTSnoopParser:
    if log_path not in _cache:
        p = BTSnoopParser(log_path)
        p.parse()
        _cache[log_path] = p
    return _cache[log_path]


# ── 上传页模板 ────────────────────────────────────────────────────────────────

_UPLOAD_TMPL = """<!DOCTYPE html>
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
    cursor: pointer; width: 100%; margin-top: 16px;
  }
  button:hover { background: #3182ce; }
  #filename { font-size: 0.82rem; color: #68d391; margin-top: 10px; min-height: 1.2em; }
  .err { color: #fc8181; font-size: 0.82rem; margin-top: 12px; }
</style>
</head>
<body>
<div class="card">
  <h1>🔵 BTAgent</h1>
  <p>上传 BTSnoop HCI 日志文件，即时查看解析报告</p>
  {% if error %}
  <div class="err">⚠️ {{ error }}</div><br>
  {% endif %}
  <form method="POST" action="/upload" enctype="multipart/form-data">
    <div class="drop-zone" id="drop-zone" onclick="document.getElementById('file-input').click()">
      <div class="icon">📂</div>
      <div>点击或拖拽文件到此处</div>
      <div class="hint">.log / .cfa / .btsnoop</div>
    </div>
    <input type="file" id="file-input" name="logfile" accept=".log,.cfa,.btsnoop">
    <div id="filename">未选择文件</div>
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
    if (e.dataTransfer.files.length) {
      const dt = new DataTransfer();
      dt.items.add(e.dataTransfer.files[0]);
      input.files = dt.files;
      label.textContent = e.dataTransfer.files[0].name;
    }
  });
</script>
</body>
</html>
"""


# ── 路由 ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    if _FIXED_LOG:
        p = _get_parser(_FIXED_LOG)
        return build_html(p)
    return render_template_string(_UPLOAD_TMPL, error=None)


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("logfile")
    if not f or not f.filename:
        return render_template_string(_UPLOAD_TMPL, error="请选择文件"), 400

    suffix = Path(f.filename).suffix or ".log"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        f.save(tmp.name)
        tmp_path = tmp.name

    try:
        p = BTSnoopParser(tmp_path)
        p.file_path = Path(f.filename)   # 显示原始文件名
        p.parse()
        return build_html(p)
    except Exception as e:
        return render_template_string(_UPLOAD_TMPL, error=str(e)), 500
    finally:
        os.unlink(tmp_path)


# ── 入口 ──────────────────────────────────────────────────────────────────────

def main():
    global _FIXED_LOG

    ap = argparse.ArgumentParser(description="BTAgent Web 服务")
    ap.add_argument("logfile", nargs="?", default="", help="BTSnoop 文件路径（省略则显示上传页）")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--host", default="0.0.0.0")
    args = ap.parse_args()

    if args.logfile:
        if not Path(args.logfile).exists():
            print(f"错误: 文件不存在 — {args.logfile}")
            sys.exit(1)
        _FIXED_LOG = args.logfile

    print(f"\n  BTAgent Web 服务已启动")
    print(f"  访问: http://localhost:{args.port}")
    print(f"  日志: {_FIXED_LOG or '（上传模式）'}")
    print(f"  按 Ctrl+C 停止\n")

    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
