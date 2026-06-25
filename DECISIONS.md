# Design decisions

Why this list is shaped the way it is. Kept short and honest so contributors can argue with it.

## Why "LLM Wiki" and not "second brain"

"Second brain" predates LLMs (Tiago Forte / PKM) and now means almost anything. Tracking under that banner would drag in generic note apps and dilute the signal. We checked how the community actually labels this specific lineage:

- The [original gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) is titled **LLM Wiki**.
- GitHub's [`llm-wiki`](https://github.com/topics/llm-wiki) topic carries 300+ repos; the projects overwhelmingly name themselves "LLM Wiki", "Karpathy's LLM Wiki", or "LLM-native knowledge base".

So we standardize on **LLM Wiki** and mention "second brain" once, as a synonym. Other accepted synonyms: *LLM-native knowledge base*, *self-maintaining wiki*, *AI-maintained second brain*.

## Why a generated README (a research agent)

Most awesome-lists rot — a maintainer loses interest and star counts/links drift. The thing this list tracks (self-maintaining wikis) suggested the fix: **make the list self-maintaining too.** An agent sweeps GitHub weekly and regenerates the README deterministically. Curation stays human (`agent/curation.json`); discovery and bookkeeping are automated.

## Scope: the lineage only

We deliberately **exclude**:

- General RAG frameworks, vector-DB platforms, agent toolkits that merely mention knowledge bases (e.g. they trended into the `llm-wiki` topic by mis-tagging). A **lineage gate** in `fetch.py` drops these automatically; a few stubborn ones are hand-excluded in `curation.json`.
- Generic "second brain" / PKM apps with no tie to the pattern.
- The **"Company Brain" / org-knowledge** thread. It's related and interesting, but it's a different bet at a different confidence level; folding it in would blur what this list is. It stays in the parent project.

## Inclusion bar

≥25 stars **or** a curation override (so notable-but-new repos, papers, and guides can be added by hand). The bar keeps the auto-discovered long tail from becoming noise while letting humans add what matters below it.

## Honest critiques are a feature

The critiques section documents real failure modes (invisible staleness, knowledge-base poisoning, no native UI, token cost). A list that only promotes isn't trustworthy. The honesty is the point — and it's why the project descriptions stay factual and adjective-free.

## Provenance

This list grew out of a multi-source research pass on the LLM Wiki ecosystem (see the parent project's research note). The market read that motivated it: the pattern is hot (300+ repos, implementations at 100–1200★ each) but **no authoritative curated list existed** — the strongest incumbents had single-digit stars. That gap is the opportunity this repo addresses.
