## Choosing an implementation

There are dozens below. A quick way to narrow down by how you already work:

| If you want… | Start with | Why |
| --- | --- | --- |
| A polished, batteries-included desktop app | [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) | The most complete: knowledge graph, vector search, Deep Research, human review. |
| It to live inside Claude Code / Codex / Cursor | an **Agent skill** — e.g. [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki), [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki) | No new app; your existing agent becomes the wiki maintainer. |
| To build on your existing Obsidian vault | an **Obsidian build** — e.g. [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) (rewrite-style) | Keeps your graph/links; the rewrite approach fights staleness. |
| Everything offline / private (no API calls) | a **local-first** build — e.g. [kytmanov/obsidian-llm-wiki-local](https://github.com/kytmanov/obsidian-llm-wiki-local) | Runs against Ollama; raw sources never leave your machine. |
| Typed entities and graph queries, not flat Markdown | [dimknaf/braindb](https://github.com/dimknaf/braindb) | Upgrades the wiki into a real database. |
| Just to understand the idea first | [the original gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) + [Guides](#guides--references) | Read before you install anything. |

Still unsure? The pattern is plain Markdown either way — start with whatever matches your editor, and you can recompile your sources into a different tool later.