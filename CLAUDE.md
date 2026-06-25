# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

**Awesome LLM Wiki** — a curated, auto-updating awesome-list tracking the lineage of [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern (an LLM compiles raw sources once into a persistent, interlinked wiki it then maintains). It is a subproject of the parent `llm-wiki-needs-ui` repo but is its own standalone git repository, meant to be published publicly and earn stars.

The defining trait: **`README.md` is generated, not hand-written.** A small stdlib-only "research agent" sweeps GitHub weekly and regenerates the list. Never hand-edit `README.md` — your change will be overwritten on the next run. Edit the *sources* instead.

## The pipeline (how a build works)

```
GitHub Search API ──> agent/fetch.py ──> data/projects.json ──┐
                                                              ├─> agent/render.py ──> README.md
agent/curation.json (human layer) ────────────────────────────┤
agent/sections/*.md (hand-written prose) ─────────────────────┘
```

- **`agent/fetch.py`** — queries the Search API across several angles (`topic:llm-wiki` + keyword queries), applies a **lineage gate** (`is_lineage()`: must carry the topic, name the lineage, or be karpathy+wiki) so off-topic giants (general RAG frameworks, agent toolkits) don't leak in, then writes `data/projects.json` sorted by stars. Honors `curation.json`.
- **`agent/curation.json`** — the human-in-the-loop layer. `min_stars` (inclusion bar, 25), `exclude` (off-lineage repos that slip through via a mis-applied topic), `overrides` (force a category / cleaner English description), `categories` (display order, titles, blurbs).
- **`agent/render.py`** — deterministically renders `README.md` from the data + the prose in `agent/sections/`. Determinism matters: re-rendering unchanged inputs must produce a byte-identical README so the weekly CI diff shows real changes, not churn.
- **`agent/sections/*.md`** — the opinionated hand-written prose (intro, what-is, origin, guides, critiques, research, how-current, contributing-blurb). `{{TOTAL}}` and `{{GENERATED}}` are substituted at render time.

## Common commands

```bash
make update      # fetch + render (full refresh from GitHub)
make render      # regenerate README.md from existing data + sections only
make fetch       # re-pull project data only
make check       # CI/pre-commit: fail if README.md is stale vs its sources
```

No dependencies — stdlib Python 3 only. Set `GITHUB_TOKEN` to lift the unauthenticated Search rate limit (CI does this automatically via the built-in token).

## Conventions & guardrails

- **Scope is strict: the LLM Wiki lineage only.** Out of scope (keep excluded): general RAG frameworks, generic "second brain"/PKM apps, and the "Company Brain"/org-knowledge thread — that last one belongs in the parent project, not here. Mixing it in dilutes the list's identity.
- **Terminology: use "LLM Wiki"**, not "second brain" (verified against community usage — see DECISIONS.md). "second brain" appears once in the intro as a synonym only.
- After editing any source, **run `make update` (or `make render` for prose-only changes) and commit the regenerated `README.md` alongside** the source edit, or CI's `make check` will flag it.
- The critiques section is deliberately honest (staleness, KB poisoning, no native UI, token cost). Keep it that way — the list competes on trust, not hype.
- `.github/workflows/update.yml` runs `make`-equivalent steps weekly (Mondays 06:00 UTC) and auto-commits. It needs the repo's Actions write permission enabled.

## Files intentionally kept private

`*.internal.md` and `.internal/` are git-ignored and must never be committed to the public repo (launch tactics, build log). See `.gitignore`.
