#!/usr/bin/env python3
"""Local-only example HTTP receiver for DataRelay Control tutorials.

Requires Python 3.9+ standard library; no dependencies or credentials.
Never expose this unauthenticated receiver to the public internet.
"""
import argparse
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def run(bind: str, port: int, status: int, output: Path) -> None:
    class Receiver(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path != "/sink":
                self.send_error(404, "Use /sink")
                return
            raw_length = self.headers.get("Content-Length", "")
            if not raw_length.isdigit() or int(raw_length) > 1024 * 1024:
                self.send_error(413, "Missing or oversized Content-Length")
                return
            raw = self.rfile.read(int(raw_length))
            try:
                payload = json.loads(raw)
            except (ValueError, UnicodeDecodeError):
                self.send_error(400, "Expected JSON")
                return
            if status < 400:
                record = {
                    "received_utc": datetime.now(timezone.utc).isoformat(),
                    "payload": payload,
                }
                with output.open("a", encoding="utf-8") as fp:
                    fp.write(json.dumps(record, ensure_ascii=False) + "\n")
            response = json.dumps({"accepted": status < 400}).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    server = ThreadingHTTPServer((bind, port), Receiver)
    print(f"Listening at http://{bind}:{port}/sink -> {output} (HTTP {status})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="DataRelay Control tutorial HTTP sink")
    ap.add_argument("--bind", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=9011)
    ap.add_argument("--status", type=int, choices=[200, 503], default=200)
    ap.add_argument("--output", type=Path, default=Path("received-9011.ndjson"))
    opts = ap.parse_args()
    run(opts.bind, opts.port, opts.status, opts.output)
