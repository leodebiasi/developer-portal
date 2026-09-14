#!/usr/bin/env python3
"""One-shot migration: Docusaurus ONZ docs -> Mintlify developer-portal."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

SRC = Path("/Users/thalesog/Git/developers.onz.software")
DST = Path("/Users/thalesog/Git/developer-portal")
SRC_DOCS = SRC / "docs"
SRC_SPECS = SRC / "static" / "specs"

PAGE_MAP: dict[str, str] = {}

HTML_TAGS = {
    "br", "img", "a", "p", "div", "span", "table", "tr", "td", "th",
    "ul", "ol", "li", "code", "pre", "em", "strong", "h1", "h2", "h3",
    "h4", "details", "summary", "hr", "blockquote", "sup", "sub",
}


def dest_for(src_rel: str) -> str:
    if src_rel == "intro":
        return "index"
    if src_rel.startswith("cobrancas/"):
        return "qrcodes/" + src_rel.split("/", 1)[1]
    if src_rel.startswith("pagamentos/"):
        return "contas/" + src_rel.split("/", 1)[1]
    if src_rel.startswith("banking-api/"):
        return "banking/" + src_rel.split("/", 1)[1]
    return "getting-started/" + src_rel


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    text = text.replace("\r\n", "\n")
    fm: dict[str, str] = {}
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            raw = text[4:end]
            body = text[end + 5 :]
            for line in raw.splitlines():
                if ":" not in line:
                    continue
                key, val = line.split(":", 1)
                fm[key.strip()] = val.strip().strip("'\"")
    while True:
        m = re.match(r"^(displayed_sidebar|unlisted|id):[^\n]*\n+", body)
        if not m:
            break
        body = body[m.end() :]
    return fm, body.lstrip("\n")


def first_h1(body: str) -> tuple[str | None, str]:
    m = re.match(r"^# (.+)\n+", body)
    if not m:
        return None, body
    return m.group(1).strip(), body[m.end() :]


def first_paragraph(body: str) -> str:
    for block in re.split(r"\n\s*\n", body.strip()):
        line = block.strip()
        if not line or line.startswith("#") or line.startswith("!") or line.startswith("```"):
            continue
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"[*_`]", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) > 20:
            return line[:180].rstrip(" ,;:") + ("…" if len(line) > 180 else "")
    return ""


def escape_prose(chunk: str) -> str:
    out: list[str] = []
    i = 0
    n = len(chunk)
    while i < n:
        if chunk[i] == "`":
            j = chunk.find("`", i + 1)
            if j == -1:
                out.append(chunk[i:])
                break
            out.append(chunk[i : j + 1])
            i = j + 1
            continue
        ch = chunk[i]
        if ch in "{}":
            out.append("\\" + ch)
            i += 1
            continue
        if ch == "<":
            close = chunk.find(">", i)
            inner = chunk[i + 1 : close] if close != -1 else ""
            tag = inner.split()[0].lower().lstrip("/") if inner else ""
            if tag in HTML_TAGS or inner.startswith("http"):
                out.append(ch)
            else:
                out.append("\\<")
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def escape_mdx(body: str) -> str:
    parts: list[str] = []
    i = 0
    n = len(body)
    while i < n:
        if body.startswith("```", i):
            end = body.find("```", i + 3)
            if end == -1:
                parts.append(body[i:])
                break
            end += 3
            parts.append(body[i:end])
            i = end
            continue
        nxt = body.find("```", i)
        chunk = body[i:] if nxt == -1 else body[i:nxt]
        parts.append(escape_prose(chunk))
        i = n if nxt == -1 else nxt
    return "".join(parts)


def split_href(href: str) -> tuple[str, str]:
    if "#" in href:
        path, frag = href.split("#", 1)
        return path, "#" + frag
    return href, ""


def rewrite_href(href: str, src_rel: str) -> str:
    href = href.strip()
    if not href or href.startswith(("http://", "https://", "mailto:", "tel:")):
        return href
    path, frag = split_href(href)

    if re.search(r"\.(png|jpe?g|svg|gif|webp)$", path, re.I):
        name = Path(path).name
        parent = Path(path).parent.name
        if parent in {"pix-automatico"}:
            return f"/images/{parent}/{name}"
        return f"/images/{name}"

    if path.startswith("/docs/"):
        key = path[len("/docs/") :].rstrip("/")
        if key in PAGE_MAP:
            return "/" + PAGE_MAP[key] + frag
        if key == "intro":
            return "/" + frag
    if path.startswith("/reference/"):
        rest = path[len("/reference/") :].strip("/")
        mapping = {
            "qrcodes": "/api-reference/qrcodes",
            "accounts": "/api-reference/contas",
            "cloudpix": "/api-reference/cloudpix",
            "onboarding": "/api-reference/onboarding",
            "spb": "/api-reference/spb",
            "cash-operations": "/api-reference/cash",
        }
        return mapping.get(rest, path) + frag
    if path in {"/banking-api/api-reference", "/banking-api/api-reference/"}:
        return "/api-reference/banking" + frag

    raw = path
    if raw.endswith(".md"):
        raw = raw[:-3]
    src_dir = Path(src_rel).parent
    resolved = Path(src_dir / raw).as_posix()
    parts: list[str] = []
    for part in resolved.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    key = "/".join(parts)
    if key in PAGE_MAP:
        dest = PAGE_MAP[key]
        return ("/" + dest if dest != "index" else "/") + frag
    stem = Path(raw).name
    for k, v in PAGE_MAP.items():
        if k.endswith("/" + stem) or k == stem:
            return ("/" + v if v != "index" else "/") + frag
    if key == "intro":
        return "/" + frag
    return href


LINK_RE = re.compile(r"(!?\[([^\]]*)\]\()([^)]+)(\))")


def rewrite_links(body: str, src_rel: str) -> str:
    def repl(m: re.Match[str]) -> str:
        prefix, href, close = m.group(1), m.group(3), m.group(4)
        return prefix + rewrite_href(href, src_rel) + close

    return LINK_RE.sub(repl, body)


def convert_md(src: Path, src_rel: str) -> str:
    raw = src.read_text()
    raw = raw.replace("https://api.example.com", "https://secureapi.onz.finance")
    raw = raw.replace("https://api.bancodigital.com", "https://secureapi.onz.finance")
    fm, body = parse_frontmatter(raw)
    h1, body = first_h1(body)
    title = fm.get("title") or fm.get("sidebar_label") or h1 or src.stem
    sidebar = fm.get("sidebar_label")
    desc = first_paragraph(body) or title
    body = rewrite_links(body, src_rel)
    body = escape_mdx(body)
    lines = ["---", f"title: {json.dumps(title, ensure_ascii=False)}"]
    if desc:
        lines.append(f"description: {json.dumps(desc, ensure_ascii=False)}")
    if sidebar and sidebar != title:
        lines.append(f"sidebarTitle: {json.dumps(sidebar, ensure_ascii=False)}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + body.rstrip() + "\n"


def copy_assets() -> None:
    images = DST / "images"
    if images.exists():
        shutil.rmtree(images)
    images.mkdir()
    for folder in (SRC_DOCS / "img", SRC_DOCS / "image"):
        if not folder.exists():
            continue
        for p in folder.rglob("*"):
            if not p.is_file() or p.name.startswith("."):
                continue
            rel = p.relative_to(folder)
            dest = images / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
    arch = SRC_SPECS / "spb-architecture.png"
    if arch.exists():
        shutil.copy2(arch, images / "spb-architecture.png")

    shutil.copy2(SRC / "static" / "img" / "logo-primary.svg", DST / "logo" / "light.svg")
    shutil.copy2(SRC / "static" / "img" / "logo.svg", DST / "logo" / "dark.svg")
    shutil.copy2(SRC / "static" / "img" / "favicon.ico", DST / "favicon.ico")

    openapi = DST / "openapi"
    if openapi.exists():
        shutil.rmtree(openapi)
    openapi.mkdir()
    copies = {
        "accounts.yaml": "accounts.yaml",
        "qrcodes.yaml": "qrcodes.yaml",
        "cloudpix.yaml": "cloudpix.yaml",
        "onboarding.yaml": "onboarding.yaml",
        "cash-operations.yaml": "cash-operations.yaml",
        "banking-api.json": "banking-api.json",
        ".generated/spb-combined.swagger.yaml": "spb.yaml",
    }
    for src_name, dest_name in copies.items():
        shutil.copy2(SRC_SPECS / src_name, openapi / dest_name)

    qrcodes = openapi / "qrcodes.yaml"
    text = qrcodes.read_text()
    text = text.replace(
        "/docs/cobrancas/pix-automatico-jornadas",
        "/qrcodes/pix-automatico-jornadas",
    )
    qrcodes.write_text(text)


def convert_all() -> None:
    md_files = sorted(p for p in SRC_DOCS.rglob("*.md") if p.is_file())
    for p in md_files:
        rel = p.relative_to(SRC_DOCS).with_suffix("").as_posix()
        PAGE_MAP[rel] = dest_for(rel)

    for p in md_files:
        rel = p.relative_to(SRC_DOCS).with_suffix("").as_posix()
        if rel == "intro":
            continue
        dest_rel = PAGE_MAP[rel] + ".mdx"
        dest = DST / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(convert_md(p, rel))
        print("converted", rel, "->", dest_rel)



def main() -> None:
    raise SystemExit(
        "scripts/migrate.py was the one-shot converter. The POC was hand-tuned afterwards; do not re-run."

[Showing lines 1-300 of 306. Use :301 to continue]