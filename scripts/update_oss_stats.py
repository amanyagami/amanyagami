#!/usr/bin/env python3
"""Regenerate the visible public PR table in README.md.

Pulls every PR authored by GITHUB_USER through the `gh` CLI, keeps only
public repositories outside the user's own namespace, and replaces the content between the OSS-STATS
markers with linked counts for merged and pending PRs. The same
source data updates the compact summary in the Engineering Snapshot.

Safe to run repeatedly - it is idempotent for a given snapshot of GitHub.
"""

import json
import re
import subprocess
import sys
import urllib.parse
from collections import defaultdict
from datetime import datetime, timezone

GITHUB_USER = "amanyagami"
EXCLUDED_OWNERS = {GITHUB_USER}
EXCLUDED_REPOS = {"noahlabsai/arapuca"}

START_MARKER = "<!-- OSS-STATS:START -->"
END_MARKER = "<!-- OSS-STATS:END -->"
SUMMARY_START_MARKER = "<!-- OSS-SUMMARY:START -->"
SUMMARY_END_MARKER = "<!-- OSS-SUMMARY:END -->"

README_PATH = "README.md"

PUBLIC_REPO_CACHE = {}


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


def repo_is_public(repo):
    """Only publish PR activity for public repositories."""
    if repo not in PUBLIC_REPO_CACHE:
        try:
            visibility = run_gh(["api", f"repos/{repo}", "--jq", ".visibility"])
            PUBLIC_REPO_CACHE[repo] = visibility.strip() == "public"
        except Exception:
            PUBLIC_REPO_CACHE[repo] = False
    return PUBLIC_REPO_CACHE[repo]


def owner_of(repo):
    return repo.split("/", 1)[0]


def public_prs(prs):
    return [
        pr
        for pr in prs
        if owner_of(pr["repo"]) not in EXCLUDED_OWNERS
        and pr["repo"] not in EXCLUDED_REPOS
        and repo_is_public(pr["repo"])
    ]


def status_of(pr):
    if pr["merged"]:
        return "merged"
    if pr["state"] == "open":
        return "pending"
    return "closed"


def pr_search_url(repo, user, status):
    """Live GitHub search for a repository/status pair."""
    status_query = {
        "merged": "is:merged",
        "pending": "is:open",
    }[status]
    query = f"repo:{repo} is:pr author:{user} {status_query}"
    return f"https://github.com/search?q={urllib.parse.quote(query)}&type=pullrequests"


def cell(matches, repo, user, status):
    """Render a linked status count, using a direct PR link when possible."""
    icons = {"merged": "✅", "pending": "🟠"}
    labels = {"merged": "merged", "pending": "pending"}
    if not matches:
        return "—"
    icon = icons[status]
    label = labels[status]
    if len(matches) == 1:
        return f"[{icon} 1 {label}]({matches[0]['url']})"
    return f"[{icon} {len(matches)} {label}]({pr_search_url(repo, user, status)})"


def build_card(prs):
    by_repo = defaultdict(lambda: defaultdict(list))
    for pr in prs:
        status = status_of(pr)
        if status in ("merged", "pending"):
            by_repo[pr["repo"]][status].append(pr)

    lines = [
        START_MARKER,
        "### Public PR activity",
        "",
        "✅ merged · 🟠 pending — linked counts refresh automatically.",
        "",
        "| Repository | PR status |",
        "|---|---|",
    ]

    for repo in sorted(by_repo):
        statuses = by_repo[repo]
        status_cells = " · ".join(
            cell(statuses.get(status, []), repo, GITHUB_USER, status)
            for status in ("merged", "pending")
        )
        lines.append(
            f"| [{repo}](https://github.com/{repo}) | {status_cells} |"
        )

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.extend(
        [
            "",
            f"<sub>Auto-updated {ts} by "
            f"[update-oss-stats.yml](.github/workflows/update-oss-stats.yml) · "
            f"includes public external PRs authored by {GITHUB_USER}; excludes personal and excluded repositories</sub>",
            END_MARKER,
        ]
    )
    return "\n".join(lines)


def build_summary(prs):
    counts = defaultdict(int)
    for pr in prs:
        counts[status_of(pr)] += 1
    return (
        f"✅ [{counts['merged']} merged](#open-source-systems-work) · "
        f"🟠 [{counts['pending']} pending](#open-source-systems-work)"
    )


def main():
    prs = public_prs(fetch_prs(GITHUB_USER))
    card = build_card(prs)
    summary = build_summary(prs)

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    card_pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL
    )
    summary_pattern = re.compile(
        re.escape(SUMMARY_START_MARKER) + r".*?" + re.escape(SUMMARY_END_MARKER),
        re.DOTALL,
    )
    if not card_pattern.search(readme):
        print(
            f"Could not find {START_MARKER} ... {END_MARKER} markers in {README_PATH}",
            file=sys.stderr,
        )
        sys.exit(1)
    if not summary_pattern.search(readme):
        print(
            f"Could not find {SUMMARY_START_MARKER} ... {SUMMARY_END_MARKER} markers in {README_PATH}",
            file=sys.stderr,
        )
        sys.exit(1)

    new_readme = card_pattern.sub(lambda _match: card, readme)
    new_readme = summary_pattern.sub(
        lambda _match: f"{SUMMARY_START_MARKER}{summary}{SUMMARY_END_MARKER}",
        new_readme,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)


if __name__ == "__main__":
    main()
