## Critiques & open problems

The pattern is genuinely good, but it is not free of failure modes. A list that only cheerleads isn't useful — here is the honest counter-reading, drawn from people who ran it for months.

- **Confident-but-stale memory.** Append-only wikis go stale *invisibly* — nothing about reading a page tells you a fact is from 2024. The `lint` pass does not reliably detect staleness, and synthesis pages rot before their sources do. ([theaioperator: "I rebuilt Karpathy's LLM Wiki — here's what's missing"](https://theaioperator.io/p/i-rebuilt-karpathys-llm-wiki-heres))
- **Knowledge-base poisoning.** Because the LLM authors Layer 2, its summaries become indistinguishable from primary sources over time; queries start retrieving AI-written pages *as if they were the originals*. Unlike ordinary RAG hallucination, this corrupts the substrate itself. ([foundand: "The hidden flaw in Karpathy's LLM Wiki"](https://foundanand.medium.com/the-hidden-flaw-in-karpathys-llm-wiki-e3a86a94b459))
- **Token cost is a line item.** Each ingest touches 10–15 pages; at scale, maintenance is a real, recurring compute bill, not a rounding error.
- **It still has no native UI.** The default workflow is "open Obsidian next to it" or `cat` files in a terminal — the reason several projects in this list exist at all.
- **Contradiction handling doesn't auto-scale.** The original flags contradictions at ingest but leaves resolution to you; past a few hundred sources that becomes the bottleneck (and motivates the *rewrite*-style vaults above).

If you're evaluating the pattern for anything beyond personal notes, weigh these first.