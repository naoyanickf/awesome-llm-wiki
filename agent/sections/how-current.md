## How this list stays current

Most awesome-lists rot. This one is rebuilt by a tiny research agent so it doesn't.

1. **`agent/fetch.py`** sweeps the GitHub Search API across several angles (the `topic:llm-wiki` tag plus keyword queries that catch untagged repos), applies a lineage gate so off-topic giants don't sneak in, and writes [`data/projects.json`](data/projects.json).
2. **`agent/curation.json`** is the human layer: the inclusion bar (≥25 ⭐), exclusions, and category/description overrides. Editing it is the main way to shape the list.
3. **`agent/render.py`** turns that data plus the hand-written prose in [`agent/sections/`](agent/sections/) into this `README.md` — deterministically, so the weekly diff shows real changes (projects added, stars moved), not churn.
4. A **GitHub Action** runs the whole thing weekly and opens a commit. Stdlib-only Python; no dependencies.

Run it yourself:

```bash
make update      # fetch + render
# or:
python3 agent/fetch.py && python3 agent/render.py
```

Last data pull: **{{GENERATED}}** · projects tracked: **{{TOTAL}}**.