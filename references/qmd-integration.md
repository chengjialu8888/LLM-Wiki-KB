# qmd Integration Guide

[qmd](https://github.com/tobi/qmd) is a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking. It runs entirely on-device.

## Installation

```bash
# macOS
brew install tobi/tap/qmd

# From source
go install github.com/tobi/qmd@latest

# Verify
qmd --version
```

## Indexing Your Wiki

```bash
# Index the wiki directory
qmd index <vault-path>/wiki/

# Re-index after changes (fast — only processes modified files)
qmd index <vault-path>/wiki/ --update
```

qmd watches for file changes automatically when running as a server. For CLI usage, re-index before searching if the wiki has been recently updated.

## CLI Usage

```bash
# Basic search
qmd search "transformer architecture" --dir <vault-path>/wiki/

# With result limit
qmd search "attention mechanism tradeoffs" --dir <vault-path>/wiki/ --top-k 5

# JSON output (for LLM tool use)
qmd search "what are the key differences between GPT and BERT" --dir <vault-path>/wiki/ --json

# With LLM re-ranking (more accurate, slower)
qmd search "scaling laws for language models" --dir <vault-path>/wiki/ --rerank
```

## MCP Server Mode

qmd can also run as an MCP server, making it a native tool for LLM agents:

```bash
# Start MCP server
qmd serve --dir <vault-path>/wiki/ --port 8765
```

Configure in your MCP settings:
```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["serve", "--dir", "<vault-path>/wiki/"]
    }
  }
}
```

## Integration with wiki_search.py

The `wiki_search.py` script automatically detects qmd and uses it when available:

1. Checks `which qmd`
2. If found: runs `qmd search ... --json` and parses results
3. If not found: falls back to grep-based search + index.md matching

No configuration needed — just install qmd and it works.

## When to Use qmd vs Index-Based Search

| Scale | Recommendation |
|-------|---------------|
| < 50 pages | Index.md + grep is sufficient |
| 50-200 pages | qmd adds value, especially for semantic queries |
| 200+ pages | qmd strongly recommended |

At small scale, the LLM can read `index.md` and find relevant pages reliably. As the wiki grows, keyword-based search misses semantic connections that qmd's vector search catches.

## Tips

- **Re-index after batch ingests** — `qmd index --update` is fast
- **Use `--rerank` for complex queries** — adds latency but significantly improves relevance
- **JSON output for LLM tools** — always use `--json` when the LLM is consuming results
- **Local only** — qmd runs entirely on your machine, no data leaves your device
