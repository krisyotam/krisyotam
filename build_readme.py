import json
import re
import pathlib
import urllib.request
from datetime import datetime

BASE = "https://krisyotam.com"
ESSAYS_URL = f"{BASE}/api/content?type=essays"
BLOG_URL = f"{BASE}/api/content?type=blog"
TIL_URL = f"{BASE}/api/content?type=til"


def fetch_json(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        # essays endpoint wraps in {"essays": [...]}
        if isinstance(data, dict) and "essays" in data:
            return data["essays"]
        return data
    except Exception as e:
        print(f"Warning: failed to fetch {url}: {e}")
        return []


def fmt_entry(title, url, date_str):
    if date_str:
        return f"* [{title}]({url}) - {date_str}"
    return f"* [{title}]({url})"


def build_essays(items, limit=8):
    lines = ["### On the Essays"]
    sorted_items = sorted(items, key=lambda x: x.get("start_date") or "", reverse=True)
    for item in sorted_items[:limit]:
        cat = (item.get("category") or "unknown").lower().replace(" ", "-")
        slug = item["slug"]
        url = f"{BASE}/essays/{cat}/{slug}"
        lines.append(fmt_entry(item["title"], url, item.get("start_date")))
    if not items:
        lines.append("*Nothing yet.*")
    lines.append("")
    lines.append(f"More on [krisyotam.com/essays]({BASE}/essays)")
    return "\n".join(lines)


def build_blog(items, limit=8):
    lines = ["### On my Blog"]
    sorted_items = sorted(items, key=lambda x: x.get("start_date") or "", reverse=True)
    for item in sorted_items[:limit]:
        cat = (item.get("category") or "unknown").lower().replace(" ", "-")
        slug = item["slug"]
        url = f"{BASE}/blog/{cat}/{slug}"
        lines.append(fmt_entry(item["title"], url, item.get("start_date")))
    if not items:
        lines.append("*Nothing yet.*")
    lines.append("")
    lines.append(f"More on [krisyotam.com/blog]({BASE}/blog)")
    return "\n".join(lines)


def build_til(items, limit=8):
    lines = ["### TIL"]
    sorted_items = sorted(items, key=lambda x: x.get("date") or "", reverse=True)
    for item in sorted_items[:limit]:
        slug = item["slug"]
        url = f"{BASE}/til/{slug}"
        lines.append(fmt_entry(item["title"], url, item.get("date")))
    if not items:
        lines.append("*Nothing yet.*")
    lines.append("")
    lines.append(f"More on [krisyotam.com/til]({BASE}/til)")
    return "\n".join(lines)


def replace_section(content, marker, replacement):
    pattern = re.compile(
        rf"(<!-- {marker} starts -->).*?(<!-- {marker} ends -->)",
        re.DOTALL,
    )
    return pattern.sub(rf"\1\n{replacement}\n\2", content)


def main():
    essays = fetch_json(ESSAYS_URL)
    blog = fetch_json(BLOG_URL)
    til = fetch_json(TIL_URL)

    readme = pathlib.Path("README.md").read_text()

    readme = replace_section(readme, "essays", build_essays(essays))
    readme = replace_section(readme, "blog", build_blog(blog))
    readme = replace_section(readme, "til", build_til(til))

    pathlib.Path("README.md").write_text(readme)
    print(f"README updated: {len(essays)} essays, {len(blog)} blog, {len(til)} TILs")


if __name__ == "__main__":
    main()
