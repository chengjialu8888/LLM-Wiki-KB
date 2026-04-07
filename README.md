# LLM Wiki Knowledge Base

A skill for building and maintaining personal knowledge bases using LLMs, based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## The Core Idea

Instead of re-deriving knowledge from raw documents on every query (like RAG), the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that compounds over time. The wiki is a persistent, compounding artifact. You never write the wiki yourself — the LLM writes and maintains all of it.

> *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."* — Andrej Karpathy

## Architecture

```
your-vault/
├── SCHEMA.md              # Wiki conventions & LLM behavior rules
├── raw/                   # Immutable source documents
│   ├── assets/            # Downloaded images
│   └── *.md               # Clipped articles, papers, notes
├── wiki/                  # LLM-maintained knowledge wiki
│   ├── index.md           # Content catalog with summaries
│   ├── log.md             # Chronological operation log
│   ├── entities/          # Entity pages (people, orgs, products)
│   ├── concepts/          # Concept pages (techniques, theories)
│   ├── sources/           # Source summary pages
│   ├── comparisons/       # Comparative analyses
│   └── synthesis/         # Cross-cutting syntheses
└── output/                # Generated artifacts (slides, charts, reports)
```

## Operations

| Operation | Description | Script |
|-----------|-------------|--------|
| **Init** | Initialize vault directory structure | `scripts/wiki_init.py` |
| **Ingest** | Add sources → LLM compiles into wiki | `scripts/wiki_ingest.py` |
| **Query** | Ask questions → search wiki → synthesize answers | `scripts/wiki_query.py` |
| **Search** | Full-text search with qmd or grep fallback | `scripts/wiki_search.py` |
| **Lint** | Health check: broken links, orphans, consistency | `scripts/wiki_lint.py` |

## Quick Start

```bash
# 1. Initialize a vault
python scripts/wiki_init.py ~/my-research --domain "AI Research"

# 2. Ingest a source
python scripts/wiki_ingest.py ~/my-research https://example.com/article

# 3. Search the wiki
python scripts/wiki_search.py ~/my-research "transformer architecture"

# 4. Run health check
python scripts/wiki_lint.py ~/my-research --fix
```

## Platform Support

| Platform | Schema File | Adapter |
|----------|-------------|---------|
| Claude Code | `CLAUDE.md` | `adapters/claude-code/` |
| OpenCode / Codex | `AGENTS.md` | `adapters/opencode/` |
| Mira | `SCHEMA.md` | `adapters/mira/` |

## Search

Integrates with [qmd](https://github.com/tobi/qmd) for hybrid BM25/vector search. Falls back to grep + index.md when qmd is not installed.

## References

- [Karpathy's LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- See `references/` for page templates, schema template, Obsidian setup guide, and qmd integration guide.

## License

MIT
