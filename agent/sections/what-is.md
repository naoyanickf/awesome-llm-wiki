## What is an LLM Wiki?

In April 2026, Andrej Karpathy described a simple but sticky idea: stop treating your notes like something an LLM re-reads on every question (RAG), and start treating them like **source code that compiles into a binary**.

- **Layer 1 — raw sources.** Articles, papers, notes, transcripts. Immutable ground truth. The LLM reads them but never edits them; you can always recompile.
- **Layer 2 — the wiki.** A directory of interlinked Markdown: entity pages, concept pages, summaries, indexes. The LLM **fully owns and writes** this layer.
- **Layer 3 — the schema.** A `CLAUDE.md` / `AGENTS.md` that turns a general agent into a disciplined wiki maintainer (naming rules, page shapes, linking conventions).

The key claim: *humans abandon wikis because the maintenance burden grows faster than the value.* An LLM doesn't get bored, doesn't forget to update a cross-reference, and can touch fifteen files in one pass — so the wiki **stays maintained because maintenance is now nearly free**. The knowledge becomes a persistent, compounding artifact instead of being rediscovered from scratch on every query.

Your job: curate sources, direct the analysis, ask good questions. The LLM's job: everything else.