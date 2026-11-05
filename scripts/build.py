"""Build the site and append source-file dates from Git history."""
from datetime import datetime
from html import escape
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def file_dates(source):
    result = subprocess.run(
        ["git", "log", "--follow", "--format=%aI", "--", str(source.relative_to(ROOT))],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    dates = result.stdout.splitlines()
    if dates:
        return datetime.fromisoformat(dates[-1]), datetime.fromisoformat(dates[0])
    # Untracked files have no Git history yet; use local filesystem dates.
    stat = source.stat()
    return (
        datetime.fromtimestamp(getattr(stat, "st_birthtime", stat.st_mtime), TIMEZONE),
        datetime.fromtimestamp(stat.st_mtime, TIMEZONE),
    )


def time_element(value):
    value = value.astimezone(TIMEZONE)
    return f'<time datetime="{escape(value.isoformat())}">{value:%Y-%m-%d %H:%M}</time>'


def append_dates():
    for source in sorted((ROOT / "docs").rglob("*")):
        if source.suffix.lower() not in {".md", ".html"}:
            continue
        target = ROOT / "site" / source.relative_to(ROOT / "docs").with_suffix(".html")
        if not target.is_file():
            continue
        created, updated = file_dates(source)
        metadata = (
            '<footer class="page-dates" aria-label="文件时间">'
            f'<span>创建时间：{time_element(created)}</span> '
            f'<span>最近编辑：{time_element(updated)}</span> '
            '</footer>\n'
        )
        content = target.read_text(encoding="utf-8")
        if '</article>' in content:
            content = content.replace('</article>', metadata + '</article>', 1)
        else:
            content = content.replace('</body>', metadata + '</body>', 1)
        target.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "zensical", "build", "--clean"], cwd=ROOT, check=True)
    append_dates()
