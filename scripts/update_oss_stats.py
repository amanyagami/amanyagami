#!/usr/bin/env python3
"""Regenerate the "Open Source Contributions" card in README.md.

Pulls every PR authored by GITHUB_USER via the GitHub search API (through
the `gh` CLI, so it inherits GH_TOKEN's auth automatically), filters out
the user's own repos and any private/employer repos, and replaces the
content between the OSS-STATS markers in README.md with a fresh summary:
open PR count, PRs opened today/this week, and which external libraries
have merged at least one of the user's PRs.

Safe to run repeatedly - it's idempotent for a given day's data.
"""

import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

GITHUB_USER = "amanyagami"
# Repos under these owners are excluded from the "external contributions"
# count: the user's own repos (not "contributing to open source" in the
# usual sense) and any private/employer org (never surface private data
# in a public README, even if the token happened to have access to it).
EXCLUDED_OWNERS = {"amanyagami", "noahlabsai"}

START_MARKER = "<!-- OSS-STATS:START -->"
END_MARKER = "<!-- OSS-STATS:END -->"

README_PATH = "README.md"


def run_gh(args):
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=True
    )
    return result.stdout


def fetch_prs(user):
    query = f"type:pr+author:{user}"
    out = run_gh(
        [
            "api",
            f"search/issues?q={query}&per_page=100",
            "--paginate",
            "--jq",
            ".items[] | {repo: (.repository_url | sub(\"https://api.github.com/repos/\";\"\")), "
            'state: .state, merged: (.pull_request.merged_at // null), '
            "created: .created_at, url: .html_url, title: .title}",
        ]
    )
    prs = []
    for line in out.splitlines():
        line = line.strip()
        if line:
            prs.append(json.loads(line))
    return prs


def repo_stars(repo):
    try:
        out = run_gh(["api", f"repos/{repo}", "--jq", ".stargazers_count"])
        return int(out.strip())
    except Exception:
        return None


def owner_of(repo):
    return repo.split("/")[0]


def format_stars(n):
    if not n:
        return ""
    if n >= 1000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return str(n)


def badge(label, value, color):
    label_enc = label.replace(" ", "%20").replace("-", "--")
    value_enc = str(value).replace(" ", "%20").replace("-", "--")
    return f"![{label}](https://img.shields.io/badge/{label_enc}-{value_enc}-{color}?style=flat-square)"


def build_card(prs):
    external = [p for p in prs if owner_of(p["repo"]) not in EXCLUDED_OWNERS]

    open_prs = [p for p in external if p["state"] == "open"]
    merged_prs = [p for p in external if p["merged"]]

    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")
    week_ago = now - timedelta(days=7)

    today_count = sum(1 for p in external if p["created"].startswith(today_str))
    week_count = sum(
        1
        for p in external
        if datetime.fromisoformat(p["created"].replace("Z", "+00:00")) >= week_ago
    )

    merged_by_repo = Counter(p["repo"] for p in merged_prs)
    open_by_repo = Counter(p["repo"] for p in open_prs)
    all_repos = sorted(set(merged_by_repo) | set(open_by_repo))

    lines = []
    lines.append(START_MARKER)
    lines.append("### 🚀 Open Source Contributions")
    lines.append("")
    lines.append(
        f"{badge('Open PRs', len(open_prs), 'orange')} "
        f"{badge('Merged', len(merged_prs), 'brightgreen')} "
        f"{badge('This week', week_count, 'blue')} "
        f"{badge('Today', today_count, 'blueviolet')} "
        f"{badge('Libraries', len(all_repos), 'informational')}"
    )
    lines.append("")

    if all_repos:
        lines.append("| Library | Merged | Open |")
        lines.append("|---|:---:|:---:|")
        for repo in all_repos:
            stars = format_stars(repo_stars(repo))
            star_suffix = f" ⭐ {stars}" if stars else ""
            merged_n = merged_by_repo.get(repo, 0)
            open_n = open_by_repo.get(repo, 0)
            merged_cell = f"✅ {merged_n}" if merged_n else "—"
            open_cell = f"🟠 {open_n}" if open_n else "—"
            lines.append(
                f"| [{repo}](https://github.com/{repo}){star_suffix} | {merged_cell} | {open_cell} |"
            )
        lines.append("")

    ts = now.strftime("%Y-%m-%d %H:%M UTC")
    lines.append(
        f"<sub>Auto-updated {ts} by "
        f"[update-oss-stats.yml](.github/workflows/update-oss-stats.yml) · "
        f"excludes private repositories and personal projects</sub>"
    )
    lines.append(END_MARKER)
    return "\n".join(lines)


def main():
    prs = fetch_prs(GITHUB_USER)
    card = build_card(prs)

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL
    )
    if not pattern.search(readme):
        print(
            f"Could not find {START_MARKER} ... {END_MARKER} markers in {README_PATH}",
            file=sys.stderr,
        )
        sys.exit(1)

    new_readme = pattern.sub(card, readme)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)


if __name__ == "__main__":
    main()
