.PHONY: update fetch render check

update: fetch render ## Refresh data from GitHub, then regenerate README.md

fetch: ## Pull the latest LLM Wiki projects from the GitHub Search API
	python3 agent/fetch.py

render: ## Regenerate README.md from data/ + agent/sections/
	python3 agent/render.py

check: render ## Fail if README.md is out of date with its sources (for CI / pre-commit)
	@git diff --exit-code README.md \
		&& echo "README.md is up to date" \
		|| (echo "README.md is stale — run 'make render' and commit" && exit 1)
