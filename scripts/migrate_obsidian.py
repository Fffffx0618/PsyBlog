#!/usr/bin/env python3
"""Normalize this notebook's Obsidian Markdown for MkDocs (dry run by default).

This is deliberately a source migration, not a build-time rewrite. Review the
diff after --write; ambiguous lazy list continuations still need human review.
"""
from __future__ import annotations

import argparse
import html
import os
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

FENCE = re.compile(r"^( *)(`{3,}|~{3,})(.*)$")
LIST = re.compile(r"^( *)(?:[-+*]|\d+[.)])\s+")
CALLOUT = re.compile(r"^\[!\s*([^\]]+?)\s*\]([+-]?)(?:\s*(.*))$")
ADMONITION = re.compile(r'^( *)(?:!!!|\?\?\?\+?)\s+\w+')
QUOTE = re.compile(r"^( *)> ?(.*)$")
TYPES = set("note abstract info tip success question warning failure danger bug example quote".split())
ALIASES = dict(summary="abstract", tldr="abstract", hint="tip", important="tip",
               check="success", done="success", help="question", faq="question",
               caution="warning", attention="warning", fail="failure", missing="failure",
               error="danger", cite="quote", examples="example")
# Obsidian vault paths used by the imported notes. Resolve within this repo only.
VAULT_PATHS = {"人工智能/深度学习/": "AI/DeepLearning/"}


def indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def remove_indent(line: str, width: int) -> str:
    column = 0
    for index, char in enumerate(line):
        if column >= width:
            return " " * (column - width) + line[index:]
        column += 4 - column % 4 if char == "\t" else 1
    return ""


def inline(line: str, path: Path) -> str:
    """Only resolve local attachments when the destination exists unambiguously."""
    def embed(match: re.Match) -> str:
        target, _, size = match[1].partition("|")
        candidates = [path.parent / target, path.parent / "images" / Path(target).name]
        found = next((p for p in candidates if p.is_file()), None)
        if found is None:
            raise ValueError(f"{path}: cannot resolve attachment {target!r}")
        url = quote(os.path.relpath(found, path.parent).replace("\\", "/"), safe="/.-_")
        dimensions = re.fullmatch(r"(\d+)(?:x(\d+))?", size)
        attrs = ""
        if dimensions:
            attrs = f' width="{dimensions[1]}"'
            if dimensions[2]:
                attrs += f' height="{dimensions[2]}"'
        elif size:
            raise ValueError(f"{path}: unsupported attachment size/alias {size!r}")
        return f'<img src="{url}" alt="{html.escape(Path(target).stem, quote=True)}"{attrs}>'

    # Literal inline examples should not become live embeds or HTML.
    parts = re.split(r"(`+[^`]*`+)", line)

    def note_target(target: str) -> str | None:
        url = urlsplit(target)
        if url.scheme or url.netloc or target.startswith(("/", "#")):
            return None
        name = unquote(url.path)
        destination = path.parent / name
        docs_root = next((p for p in path.resolve().parents if p.name == "docs"), None)
        for old, new in VAULT_PATHS.items():
            if name.startswith(old) and docs_root:
                destination = docs_root / new / name[len(old):]
        if destination.suffix != ".md":
            destination = destination.with_suffix(".md")
        if not destination.is_file():
            return None
        relative = quote(os.path.relpath(destination, path.parent), safe="/.-_")
        return relative + ("#" + url.fragment if url.fragment else "")

    def wikilink(match: re.Match) -> str:
        target, _, label = match[1].partition("|")
        resolved = note_target(target)
        if resolved is None:
            raise ValueError(f"{path}: cannot resolve note {target!r}")
        return f'[{label or Path(target).stem}]({resolved})'

    def markdown_link(match: re.Match) -> str:
        return match[1] + (note_target(match[2]) or match[2]) + match[3]
    def image_path(match: re.Match) -> str:
        target = match[2]
        url = urlsplit(target)
        if url.scheme or url.netloc or target.startswith("/"):
            return match[0]
        relative = unquote(url.path)
        if (path.parent / relative).is_file():
            return match[0]
        attachment = path.parent / "images" / Path(relative).name
        if attachment.is_file():
            return match[1] + quote("images/" + attachment.name, safe="/.-_") + match[3]
        return match[0]

    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"!\[\[([^\]]+)\]\]", embed, parts[i])
        parts[i] = re.sub(r"(?<!!)\[\[([^\]]+)\]\]", wikilink, parts[i])
        parts[i] = re.sub(r'(?<!!)(\[[^\]]*\]\()([^\s)]+)(\))', markdown_link, parts[i])
        parts[i] = re.sub(r'''(\bsrc=["'])([^"']+)(["'])''', image_path, parts[i])
        parts[i] = re.sub(r'(!\[[^\]]*\]\()([^\s)]+)(\))', image_path, parts[i])
        parts[i] = parts[i].replace('<div text-align="center">', '<div style="text-align: center">')
    return "".join(parts)


def normalize(lines: list[str], path: Path) -> list[str]:
    out: list[str] = []
    i = 0
    list_indents: list[int] = []

    def blank():
        if out and out[-1].strip():
            out.append("")

    while i < len(lines):
        raw = lines[i]
        # Expand only leading tabs; code and math payloads below are copied.
        prefix = re.match(r"^[ \t]*", raw)[0]
        line = prefix.expandtabs(4) + raw[len(prefix):]
        stripped = line.strip()
        if not stripped:
            blank()
            i += 1
            continue

        fence = FENCE.match(line)
        if fence:
            blank()
            opening = i
            payload = []
            i += 1
            while i < len(lines):
                closing = lines[i].strip()
                if re.fullmatch(re.escape(fence[2][0]) + "{" + str(len(fence[2])) + r",}", closing):
                    break
                payload.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError(f"{path}: unclosed code fence at line {opening + 1}")
            # Obsidian accepts fences indented further than their contents.
            # Move the whole code block to its shallowest indentation; preserve
            # code indentation relative to that container (especially Python).
            source_base = min(indent(s.expandtabs(4)) for s in [line, *payload, lines[i]] if s.strip())
            target_base = source_base
            if list_indents and source_base > list_indents[-1]:
                target_base = (list_indents[0] // 4) * 4 + 4 * len(list_indents)
            pad = " " * target_base
            out.append(pad + fence[2] + fence[3].strip())
            out.extend(pad + remove_indent(s, source_base) if s else "" for s in payload)
            out.append(pad + closing)
            i += 1
            blank()
            list_indents = []
            continue

        # Obsidian permits display math immediately after prose/list labels.
        # Give each display expression a paragraph of its own for arithmatex.
        math_parts = list(re.finditer(r"\$\$(.+?)\$\$", line))
        if math_parts and not QUOTE.match(line) and "`" not in line and not (len(math_parts) == 1 and stripped == math_parts[0][0]):
            pad = " " * (indent(line) + (4 if LIST.match(line) else 0))
            pieces = []
            last = 0
            for match in math_parts:
                prose = line[last:match.start()].strip()
                if prose:
                    pieces.append((" " * indent(line) if last == 0 else pad) + prose)
                pieces.extend(["", pad + "$$", pad + match[1], pad + "$$", ""])
                last = match.end()
            if line[last:].strip():
                pieces.append(pad + line[last:].strip())
            lines = lines[:i] + pieces + lines[i + 1:]
            continue

        if not QUOTE.match(line) and "`" not in line and line.count("$$") == 1 and not stripped.startswith("$$"):
            prose, first = line.split("$$", 1)
            pad = " " * (indent(line) + (4 if LIST.match(line) else 0))
            pieces = [prose.rstrip(), "", pad + "$$"]
            if first.strip():
                pieces.append(pad + first.strip())
            end = i + 1
            while end < len(lines) and "$$" not in lines[end]:
                pieces.append(pad + lines[end].lstrip())
                end += 1
            if end == len(lines):
                raise ValueError(f"{path}: unclosed display math at line {i + 1}")
            tail, suffix = lines[end].split("$$", 1)
            if tail.strip():
                pieces.append(pad + tail.strip())
            pieces.extend([pad + "$$", ""])
            if suffix.strip():
                pieces.append(pad + suffix.strip())
            lines = lines[:i] + pieces + lines[end + 1:]
            continue

        if stripped.startswith("$$"):
            blank()
            pad = " " * indent(line)
            if len(stripped) > 4 and stripped.endswith("$$"):
                out.extend([pad + "$$", pad + stripped[2:-2].lstrip(), pad + "$$"])
                i += 1
            else:
                out.append(pad + "$$")
                if stripped[2:].strip():
                    out.append(pad + stripped[2:])
                i += 1
                while i < len(lines):
                    if "$$" in lines[i]:
                        tail, suffix = lines[i].split("$$", 1)
                        if tail.strip():
                            out.append(pad + tail.lstrip())
                        out.append(pad + "$$")
                        i += 1
                        if suffix.strip():
                            lines = lines[:i] + [pad + suffix.strip()] + lines[i:]
                        break
                    if lines[i].strip():
                        out.append(pad + lines[i].lstrip())
                    i += 1
            blank()
            list_indents = []
            continue

        # Quotes are recursive, so nested callouts retain their nesting.
        q = QUOTE.match(line)
        if q:
            pad = q[1]
            content = []
            quote_fence = None
            while i < len(lines):
                qline = QUOTE.match(lines[i])
                if not qline or qline[1] != pad:
                    break
                # A second callout at the same level starts a new box.
                if content and not quote_fence and CALLOUT.match(qline[2].strip()):
                    break
                nested_fence = FENCE.match(qline[2].expandtabs(4))
                if nested_fence:
                    if quote_fence is None:
                        quote_fence = nested_fence[2]
                    elif not nested_fence[3].strip() and nested_fence[2][0] == quote_fence[0] and len(nested_fence[2]) >= len(quote_fence):
                        quote_fence = None
                content.append(qline[2])
                i += 1
            callout = CALLOUT.match(content[0].strip())
            blank()
            if callout:
                pad = " " * ((len(pad) // 4) * 4)
                original, folding, title = callout.groups()
                kind = ALIASES.get(original.lower(), original.lower())
                if kind not in TYPES:
                    title = title or original
                    kind = "note"
                marker = {"": "!!!", "-": "???", "+": "???+"}[folding]
                title = (title or "").replace('"', "&quot;")
                out.append(pad + marker + " " + kind + (f' "{title}"' if title else ""))
                out.append("")
                out.extend(pad + "    " + s if s else "" for s in normalize(content[1:], path))
            else:
                out.extend(pad + "> " + s if s else pad + ">" for s in normalize(content, path))
            blank()
            list_indents = []
            continue

        admonition = ADMONITION.match(line)
        if admonition:
            base = indent(line)
            target_base = (base // 4) * 4
            body = []
            i += 1
            while i < len(lines):
                expanded = lines[i].expandtabs(4)
                if expanded.strip() and indent(expanded) < base + 4:
                    break
                # Remove container indentation without altering code's interior.
                body.append(remove_indent(lines[i], base + 4))
                i += 1
            blank()
            out.extend([" " * target_base + line.lstrip(), ""])
            out.extend(" " * (target_base + 4) + s if s else "" for s in normalize(body, path))
            blank()
            list_indents = []
            continue

        # Keep raw HTML blocks intact. Our notebook primarily uses image divs.
        if re.match(r"<(?:div|pre|script|style|table)\b", stripped) and 'markdown="1"' not in stripped:
            tag = re.match(r"<(\w+)", stripped)[1]
            blank()
            out.append(inline(line, path))
            i += 1
            if f"</{tag}>" not in stripped:
                while i < len(lines):
                    out.append(inline(lines[i], path) if tag == "div" else lines[i])
                    end = f"</{tag}>" in lines[i]
                    i += 1
                    if end:
                        break
            blank()
            list_indents = []
            continue

        item = LIST.match(line)
        if item:
            source_indent = len(item[1])
            if not list_indents:
                blank()
                list_indents = [source_indent]
            else:
                while len(list_indents) > 1 and source_indent < list_indents[-1]:
                    list_indents.pop()
                if source_indent > list_indents[-1]:
                    list_indents.append(source_indent)
                elif source_indent < list_indents[0]:
                    list_indents = [source_indent]
            # Preserve already-normalized 4-space levels; normalize common 2/3-space nesting.
            base = (list_indents[0] // 4) * 4
            line = " " * (base + 4 * (len(list_indents) - 1)) + line.lstrip()
        else:
            block = bool(re.match(r"(?:#{1,6}\s|(?:---+|\*\*\*+)\s*$|\|)", stripped))
            if block or (stripped.startswith("**") and list_indents):
                blank()
                list_indents = []
            elif list_indents and (not out or not out[-1].strip()):
                list_indents = []
            # Do not split adjacent table rows with blanks.
            if stripped.startswith("|") and len(out) > 1 and not out[-1] and out[-2].lstrip().startswith("|"):
                out.pop()

        out.append(inline(line, path))
        if re.match(r"^(?:#{1,6}\s|---+\s*$)", stripped):
            blank()
        i += 1

    while out and not out[-1].strip():
        out.pop()
    return out


def convert(text: str, path: Path) -> str:
    lines = text.splitlines()
    frontmatter = []
    if lines and lines[0] == "---":
        for end in range(1, len(lines)):
            if lines[end] == "---":
                frontmatter, lines = lines[:end + 1] + [""], lines[end + 1:]
                break
    return "\n".join(frontmatter + normalize(lines, path)).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", type=Path, nargs="*", default=[Path("docs")])
    parser.add_argument("--write", action="store_true", help="write changes (otherwise only list files)")
    args = parser.parse_args()
    files = sorted({p for root in args.paths for p in (root.rglob("*.md") if root.is_dir() else [root])})
    changes = []
    # Resolve every attachment before writing any file.
    for path in files:
        original = path.read_text(encoding="utf-8")
        converted = convert(original, path)
        if converted != original:
            changes.append((path, converted))
    for path, converted in changes:
        print(path)
        if args.write:
            newline = "\r\n" if b"\r\n" in path.read_bytes() else "\n"
            path.write_text(converted, encoding="utf-8", newline=newline)
    print(f"{len(changes)} file(s) {'updated' if args.write else 'would change'}")


if __name__ == "__main__":
    main()
