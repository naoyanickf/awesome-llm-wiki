#!/usr/bin/env python3
"""Render README.md from data/projects.json + the prose in agent/sections/.

The "list" half of the repo. Deterministic: same inputs -> byte-identical
README, so the weekly CI job produces clean, reviewable diffs (projects added,
star counts moved) instead of churn. Prose lives in agent/sections/*.md so the
opinionated writing stays hand-edited; the project tables are generated.
"""
import json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "projects.json").read_text())
CUR = json.loads((ROOT / "agent" / "curation.json").read_text())
SECTIONS = ROOT / "agent" / "sections"


def sec(name):
    p = SECTIONS / f"{name}.md"
    return p.read_text().strip() if p.exists() else ""


def star_badge(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def table(projects):
    rows = ["| Project | Stars | Lang | Updated | What it is |",
            "| --- | --- | --- | --- | --- |"]
    for p in projects:
        name = f"[{p['full_name']}]({p['url']})"
        lang = p["language"] or "—"
        desc = (p["description"] or "").replace("|", "\\|").replace("\n", " ").strip() or "—"
        if len(desc) > 140:
            desc = desc[:137].rstrip() + "…"
        rows.append(f"| {name} | {star_badge(p['stars'])} | {lang} | {p['pushed_at'] or '—'} | {desc} |")
    return "\n".join(rows)


def main():
    projects = DATA["projects"]
    by_cat = {}
    for p in projects:
        by_cat.setdefault(p["category"], []).append(p)

    gen = DATA["generated_at"]
    total = DATA["total_tracked"]
    top = max(projects, key=lambda p: p["stars"])

    out = []
    out.append(sec("00-intro").replace("{{TOTAL}}", str(total)).replace("{{GENERATED}}", gen))
    out.append("")
    out.append("## Contents\n")
    toc = ["- [What is an LLM Wiki?](#what-is-an-llm-wiki)",
           "- [The origin](#the-origin)",
           "- [Choosing an implementation](#choosing-an-implementation)"]
    for c in CUR["categories"]:
        if by_cat.get(c["id"]):
            anchor = c["title"].lower().replace(" & ", "--").replace(" ", "-")
            toc.append(f"- [{c['title']}](#{anchor}) ({len(by_cat[c['id']])})")
    toc += ["- [Guides & references](#guides--references)",
            "- [Critiques & open problems](#critiques--open-problems)",
            "- [Research](#research)",
            "- [How this list stays current](#how-this-list-stays-current)",
            "- [Contributing](#contributing)",
            "- [Maintainer](#maintainer)"]
    out.append("\n".join(toc))
    out.append("")
    out.append(sec("what-is"))
    out.append("")
    out.append(sec("origin"))
    out.append("")
    out.append(sec("choosing"))
    out.append("")

    for c in CUR["categories"]:
        items = by_cat.get(c["id"])
        if not items:
            continue
        out.append(f"## {c['title']}\n")
        out.append(c["blurb"] + "\n")
        out.append(table(items))
        out.append("")

    out.append(sec("guides"))
    out.append("")
    out.append(sec("critiques"))
    out.append("")
    out.append(sec("research"))
    out.append("")
    out.append(sec("how-current").replace("{{GENERATED}}", gen).replace("{{TOTAL}}", str(total)))
    out.append("")
    out.append(sec("contributing-blurb"))
    out.append("")
    out.append("## Maintainer\n")
    out.append(
        "Curated by **[@naoyanickf](https://x.com/naoyanickf)**. "
        "Spotted a missing project or a wrong description? "
        "[Open a PR](CONTRIBUTING.md) or ping me on X.\n"
    )
    out.append(
        f"---\n\n_Tracking {total} projects in the LLM Wiki lineage. "
        f"Auto-refreshed weekly — last data pull {gen}. "
        f"Largest project right now: [{top['full_name']}]({top['url']}) "
        f"({star_badge(top['stars'])} ⭐). "
        "Built and maintained by a small research agent ([agent/](agent/)) — "
        "a self-updating list, fitting for self-updating wikis._\n"
    )

    readme = "\n".join(out).rstrip() + "\n"
    # collapse 3+ blank lines to 2
    while "\n\n\n" in readme:
        readme = readme.replace("\n\n\n", "\n\n")
    (ROOT / "README.md").write_text(readme)
    print(f"wrote README.md ({len(readme)} chars, {total} projects, {datetime.date.today()})")


if __name__ == "__main__":
    main()
