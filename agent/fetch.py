#!/usr/bin/env python3
"""Discover LLM Wiki lineage projects from GitHub and write data/projects.json.

The "research agent" half of this repo. Queries the GitHub Search API across a
set of angles (the `topic:llm-wiki` tag plus keyword searches that catch repos
which never bothered to tag themselves), merges + dedupes by full_name, applies
the curation rules in curation.json (exclusions, category overrides, pinned
non-repo sources), and emits a single sorted projects.json that render.py turns
into README.md.

Stdlib only — no pip install. Set GITHUB_TOKEN in the environment to lift the
unauthenticated search rate limit (used by CI); works without one locally.
"""
import json, os, sys, time, urllib.request, urllib.parse, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CURATION = json.loads((ROOT / "agent" / "curation.json").read_text())

# Search angles. `topic:llm-wiki` is the spine; the keyword queries catch
# lineage repos that did not self-tag. Order does not matter (results merge).
QUERIES = [
    "topic:llm-wiki",
    '"llm wiki" in:name,description',
    "karpathy wiki in:name,description",
    '"llm-native" "knowledge base" in:name,description',
    '"self-maintaining" wiki in:name,description',
]

# Category assignment: first rule whose keywords match (name+desc+topics) wins.
# A repo's category can always be force-set in curation.json -> "overrides".
CATEGORY_RULES = [
    ("obsidian-vault",   ["obsidian", "vault"]),
    ("agent-skills-cli", ["skill", "claude code", "codex", "cursor", "copilot", "mcp", "cli", "agent harness"]),
    ("knowledge-graph",  ["graph", "database", "typed entit", "braindb", "entities", "relations"]),
    ("capture-ingest",   ["clip", "clipper", "ingest", "import", "capture", "transcript"]),
    ("local-first",      ["local", "ollama", "offline", "privacy", "on-device", "local-first"]),
    ("guides-refs",      ["guide", "tutorial", "step-by-step", "step by step", "stack", "reference", "blueprint", "bootstrap", "how to", "walkthrough"]),
]
DEFAULT_CATEGORY = "implementations"

# Lineage gate: the broad keyword queries drag in big off-lineage repos
# (general RAG frameworks, agent toolkits) that happen to share a word. A repo
# only counts as LLM-Wiki lineage if it carries the topic tag or names the
# lineage explicitly. This keeps the agent honest without hand-excluding every
# unrelated giant that trends into the search.
LINEAGE_PHRASES = [
    "llm wiki", "llm-wiki", "llmwiki", "llm-native wiki",
    "self-maintaining wiki", "self-building wiki", "wiki that builds itself",
]


def is_lineage(repo):
    topics = [t.lower() for t in (repo.get("topics") or [])]
    if "llm-wiki" in topics:
        return True
    hay = (repo.get("name", "") + " " + (repo.get("description") or "")).lower()
    if any(p in hay for p in LINEAGE_PHRASES):
        return True
    if "karpathy" in hay and "wiki" in hay:
        return True
    return False


def gh_search(q, per_page=50, pages=1):
    items, token = [], os.environ.get("GITHUB_TOKEN")
    headers = {"User-Agent": "awesome-llm-wiki-agent", "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for page in range(1, pages + 1):
        params = urllib.parse.urlencode(
            {"q": q, "sort": "stars", "order": "desc", "per_page": per_page, "page": page}
        )
        url = "https://api.github.com/search/repositories?" + params
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                data = json.load(r)
        except Exception as e:  # noqa: BLE001 — never let one query kill the run
            print(f"  ! query failed ({q!r} p{page}): {e}", file=sys.stderr)
            break
        items.extend(data.get("items", []))
        if len(data.get("items", [])) < per_page:
            break
        time.sleep(2)
    return items


def classify(repo):
    hay = " ".join([
        repo.get("name", ""),
        repo.get("description") or "",
        " ".join(repo.get("topics", []) or []),
    ]).lower()
    for cat, kws in CATEGORY_RULES:
        if any(k in hay for k in kws):
            return cat
    return DEFAULT_CATEGORY


def main():
    excl = set(CURATION.get("exclude", []))
    overrides = CURATION.get("overrides", {})
    min_stars = CURATION.get("min_stars", 15)

    merged = {}
    for q in QUERIES:
        print(f"query: {q}", file=sys.stderr)
        for repo in gh_search(q):
            fn = repo["full_name"]
            if fn in merged:
                continue
            merged[fn] = repo
        time.sleep(4)  # stay under the unauthenticated search rate limit

    projects = []
    for fn, r in merged.items():
        if fn in excl or r.get("archived") or r.get("fork"):
            continue
        if fn not in overrides and not is_lineage(r):
            continue  # off-lineage keyword collision — drop
        if r.get("stargazers_count", 0) < min_stars and fn not in overrides:
            continue
        ov = overrides.get(fn, {})
        projects.append({
            "full_name": fn,
            "url": r["html_url"],
            "description": ov.get("description") or (r.get("description") or "").strip(),
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "language": r.get("language"),
            "pushed_at": r.get("pushed_at", "")[:10],
            "category": ov.get("category") or classify(r),
        })

    projects.sort(key=lambda p: p["stars"], reverse=True)
    out = {
        "generated_at": time.strftime("%Y-%m-%d", time.gmtime()),
        "total_tracked": len(projects),
        "projects": projects,
    }
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "projects.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(projects)} projects -> data/projects.json", file=sys.stderr)


if __name__ == "__main__":
    main()
