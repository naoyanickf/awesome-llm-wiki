# Contributing to Awesome LLM Wiki

Thanks for helping keep the definitive map of the **LLM Wiki** lineage accurate. This list is generated, so contributing means editing *sources*, never `README.md` directly.

## Scope — what belongs here

Only the **LLM Wiki lineage**: projects, guides, and writing descended from [Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — an LLM that compiles raw sources into a persistent, interlinked wiki it maintains.

In scope: implementations, agent skills/plugins, Obsidian & vault variants, local-first builds, knowledge-graph/DB takes, capture tools, guides, critiques, and on-topic papers.

Out of scope (we deliberately exclude these to keep the list sharp):
- General RAG frameworks, vector-DB platforms, and agent toolkits that merely *mention* knowledge bases.
- Generic "second brain" / PKM apps with no tie to the LLM Wiki pattern.
- "Company Brain" / org-knowledge platforms — a related but distinct thread.

## How to add or fix an entry

### Option 1 — let the agent find it (zero PR)
Add the [`llm-wiki`](https://github.com/topics/llm-wiki) topic to the repo and get it to **≥25 stars**. The weekly sweep will include it automatically.

### Option 2 — open a PR
- **Add now / below the star bar / fix a category or description:** edit [`agent/curation.json`](agent/curation.json).
  - `overrides`: set a cleaner `description` (English preferred) or force a `category`.
  - `exclude`: remove an off-lineage repo that slipped in via a mis-applied topic.
- **Add a guide, critique, or paper** (prose, not a tracked repo): edit the matching file in [`agent/sections/`](agent/sections/) — `guides.md`, `critiques.md`, or `research.md`.
- Then run `make update` (or just `make render` for prose-only changes) and commit the regenerated `README.md` alongside your source edit.

```bash
make update          # fetch + render
git add -A && git commit -m "Add <project>"
```

## Quality bar

- Real, working projects with a clear LLM Wiki tie. No vaporware, no SEO farms.
- Descriptions: one line, factual, English where possible. No marketing adjectives.
- Categories follow `agent/curation.json → categories`. When in doubt, pick the most specific one.

## Ground rules

Be accurate and fair to every project — this list competes on trust, not hype. The critiques section is honest *because* the project descriptions are.
