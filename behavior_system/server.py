import io, json, os, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import pandas as pd
from .predict import BehaviorModel
from .config import FEAT_LABELS

HERE = os.path.dirname(__file__)


def make_handler(art):
    bm = BehaviorModel(art)
    html = open(os.path.join(HERE, "ui.html"), encoding="utf-8").read()

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def _send(self, obj, code=200, ctype="application/json"):
            body = obj.encode() if isinstance(obj, str) else json.dumps(obj).encode()
            self.send_response(code); self.send_header("Content-Type", ctype + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/": return self._send(html, ctype="text/html")
            if u.path == "/api/summary":
                m = bm.meta
                return self._send({k: m[k] for k in ("dataset", "synthetic", "n_users", "n_pos", "n_neg", "W", "T", "min_posts",
                                    "max_posts", "feats", "cohort", "results", "thresholds")} |
                                  {"labels": FEAT_LABELS, "sources": m.get("sources", {}), "results_by_source": m.get("results_by_source", []),
                                   "users": {k: {"label": v["label"], "risk": v["risk_oof"], "n_windows": v["n_windows"],
                                                 "source": v.get("source", "thai"), "group": v.get("group", "")}
                                             for k, v in m["users"].items()}})
            if u.path == "/api/user":
                uid = parse_qs(u.query).get("id", [""])[0]
                d = bm.meta["users"].get(uid)
                return self._send(d, 200) if d else self._send({"error": "unknown user"}, 404)
            self._send({"error": "not found"}, 404)

        def do_POST(self):
            if self.path != "/api/analyze": return self._send({"error": "not found"}, 404)
            try:
                n = int(self.headers.get("Content-Length", 0)); body = json.loads(self.rfile.read(n))
                df = pd.read_csv(io.StringIO(body["csv"]))
                tcol = next((c for c in df.columns if c.lower() in ("created_date", "timestamp", "created_at", "date", "time")), df.columns[0])
                xcol = next((c for c in df.columns if c.lower() in ("anonymised_text", "text", "tweet", "content")), None)
                r = bm.score_posts(df, tcol, xcol or "anonymised_text")
                self._send(r)
            except Exception as e:
                self._send({"error": str(e)}, 400)
    return H


def serve(art="artifacts", port=8000, open_browser=True):
    srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(art))
    url = f"http://127.0.0.1:{port}"
    print(f"\n  UI running at {url}   (Ctrl+C to stop)\n")
    if open_browser: threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: print("stopped")
