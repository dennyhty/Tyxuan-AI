#!/usr/bin/env python3
"""Minimal Notion API CLI (stdlib only). Token comes only from env NOTION_TOKEN.

Usage:
  notion_cli.py me
  notion_cli.py search [QUERY] [--type page|data_source]
  notion_cli.py page ID                 # page properties
  notion_cli.py blocks ID               # page body (child blocks)
  notion_cli.py db ID                   # database / data source schema
  notion_cli.py query ID [--filter JSON] [--sorts JSON] [--limit N] [--count]
  notion_cli.py create PARENT_DS_ID --props JSON [--children JSON]
  notion_cli.py update PAGE_ID --props JSON
  notion_cli.py archive PAGE_ID         # move to trash (restorable)
  notion_cli.py restore PAGE_ID
  notion_cli.py raw METHOD PATH [--body JSON]

IDs may be page/database ids with or without dashes, or notion.so URLs.
Output is JSON. Writes always need the integration connected to the page
(page menu -> Connections).
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error

BASE = "https://api.notion.com/v1"
# 2025-09-03 introduced data sources; 2022-06-28 still works on plain databases.
VERSION = os.environ.get("NOTION_VERSION", "2025-09-03")
MIN_INTERVAL = 1 / 3  # ~3 req/s
_last = 0.0


def token():
    t = os.environ.get("NOTION_TOKEN")
    if not t:
        sys.exit("NOTION_TOKEN is not set (set it in the cloud environment, never in the repo)")
    return t


def norm_id(s):
    m = re.findall(r"[0-9a-fA-F]{32}", s.replace("-", ""))
    if not m:
        sys.exit(f"cannot find a Notion id in: {s}")
    h = m[-1].lower()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


def call(method, path, body=None, retries=5):
    global _last
    for attempt in range(retries + 1):
        wait = MIN_INTERVAL - (time.time() - _last)
        if wait > 0:
            time.sleep(wait)
        _last = time.time()
        req = urllib.request.Request(
            BASE + path,
            method=method,
            data=None if body is None else json.dumps(body).encode(),
            headers={
                "Authorization": f"Bearer {token()}",
                "Notion-Version": VERSION,
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            payload = e.read().decode()
            if e.code in (429, 502, 503, 504) and attempt < retries:
                delay = float(e.headers.get("Retry-After") or 2 ** attempt)
                time.sleep(delay)
                continue
            sys.exit(f"HTTP {e.code} {method} {path}: {payload}")
    sys.exit("retries exhausted")


def paginate(method, path, body=None, limit=None):
    out, cursor = [], None
    while True:
        b = dict(body or {})
        p = path
        if method == "GET":
            p += ("&" if "?" in p else "?") + "page_size=100" + (f"&start_cursor={cursor}" if cursor else "")
        else:
            b["page_size"] = 100
            if cursor:
                b["start_cursor"] = cursor
        r = call(method, p, None if method == "GET" else b)
        out += r.get("results", [])
        if limit and len(out) >= limit:
            return out[:limit]
        if not r.get("has_more"):
            return out
        cursor = r["next_cursor"]


def resolve_ds(id_):
    """Accept a database id or data source id; return a data source id (or None for old API)."""
    if VERSION < "2025-09-03":
        return None
    try:
        d = call("GET", f"/databases/{id_}")
        ds = d.get("data_sources") or []
        if ds:
            return ds[0]["id"]
    except SystemExit:
        pass
    return id_


def query(id_, flt, sorts, limit):
    body = {}
    if flt: body["filter"] = json.loads(flt)
    if sorts: body["sorts"] = json.loads(sorts)
    ds = resolve_ds(id_)
    path = f"/data_sources/{ds}/query" if ds else f"/databases/{id_}/query"
    return paginate("POST", path, body, limit)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("me")
    s = sp.add_parser("search"); s.add_argument("q", nargs="?", default=""); s.add_argument("--type", choices=["page", "data_source"])
    for n in ("page", "blocks", "db", "archive", "restore"):
        sp.add_parser(n).add_argument("id")
    q = sp.add_parser("query"); q.add_argument("id"); q.add_argument("--filter"); q.add_argument("--sorts")
    q.add_argument("--limit", type=int); q.add_argument("--count", action="store_true")
    c = sp.add_parser("create"); c.add_argument("parent"); c.add_argument("--props", required=True); c.add_argument("--children")
    u = sp.add_parser("update"); u.add_argument("id"); u.add_argument("--props", required=True)
    r = sp.add_parser("raw"); r.add_argument("method"); r.add_argument("path"); r.add_argument("--body")
    a = ap.parse_args()

    if a.cmd == "me":
        res = call("GET", "/users/me")
    elif a.cmd == "search":
        b = {"query": a.q}
        if a.type: b["filter"] = {"property": "object", "value": a.type if VERSION >= "2025-09-03" else ("database" if a.type == "data_source" else "page")}
        res = paginate("POST", "/search", b)
    elif a.cmd == "page":
        res = call("GET", f"/pages/{norm_id(a.id)}")
    elif a.cmd == "blocks":
        res = paginate("GET", f"/blocks/{norm_id(a.id)}/children")
    elif a.cmd == "db":
        i = norm_id(a.id)
        res = call("GET", f"/data_sources/{i}") if VERSION >= "2025-09-03" and _is_ds(i) else call("GET", f"/databases/{i}")
    elif a.cmd == "query":
        rows = query(norm_id(a.id), a.filter, a.sorts, a.limit)
        res = {"count": len(rows)} if a.count else rows
    elif a.cmd == "create":
        i = norm_id(a.parent)
        ptype = "data_source_id" if VERSION >= "2025-09-03" else "database_id"
        body = {"parent": {"type": ptype, ptype: resolve_ds(i) or i}, "properties": json.loads(a.props)}
        if a.children: body["children"] = json.loads(a.children)
        res = call("POST", "/pages", body)
    elif a.cmd == "update":
        res = call("PATCH", f"/pages/{norm_id(a.id)}", {"properties": json.loads(a.props)})
    elif a.cmd == "archive":
        res = call("PATCH", f"/pages/{norm_id(a.id)}", {"in_trash": True})
    elif a.cmd == "restore":
        res = call("PATCH", f"/pages/{norm_id(a.id)}", {"in_trash": False})
    else:
        res = call(a.method.upper(), a.path, json.loads(a.body) if a.body else None)
    json.dump(res, sys.stdout, ensure_ascii=False, indent=2)
    print()


def _is_ds(i):
    try:
        call("GET", f"/data_sources/{i}")
        return True
    except SystemExit:
        return False


if __name__ == "__main__":
    main()
