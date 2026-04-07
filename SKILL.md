---
name: llm-wiki-kb
description: >
  Build and maintain personal knowledge bases as LLM-compiled markdown wikis, inspired by
  Andrej Karpathy's LLM Wiki pattern. The LLM incrementally ingests raw sources (articles,
  papers, repos, images) into a structured, interlinked wiki of .md files — with summaries,
  entity pages, concept pages, cross-references, and a persistent index. All viewable in
  Obsidian. Use this skill whenever the user wants to: create or manage a personal knowledge
  base, ingest documents into a wiki, ask questions against a collection of research materials,
  compile notes into structured knowledge, run health checks on a wiki, generate slides or
  charts from wiki content, search across markdown knowledge bases, or anything involving
  "knowledge management", "research wiki", "second brain", "personal wiki", "Obsidian vault
  management", "Zettelkasten with LLM", or "compile my notes". Even if the user just says
  "add this article to my KB" or "what does my research say about X" — use this skill.
---

# LLM Wiki Knowledge Base

A skill for building and maintaining personal knowledge bases using LLMs, based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## The Core Idea

Most RAG systems re-derive knowledge on every query. This skill takes a fundamentally different approach: the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that compounds over time. When a new source is added, the LLM doesn't just index it — it reads it, extracts key information, and integrates it into the existing wiki, updating entity pages, revising summaries, noting contradictions, and strengthening the evolving synthesis.

**The wiki is a persistent, compounding artifact.** Cross-references are already there. Contradictions have been flagged. The synthesis reflects everything ingested. The human curates sources and asks questions; the LLM does everything else.

## Architecture

```
<vault-root>/                     # Obsidian vault root
├── SCHEMA.md                     # Wiki conventions & LLM behavior rules
├── raw/                          # Immutable source documents
│   ├── assets/                   # Downloaded images
│   └── *.md                      # Clipped articles, papers, notes
├── wiki/                         # LLM-maintained knowledge wiki
│   ├── index.md                  # Content catalog with summaries
│   ├── log.md                    # Chronological operation log
│   ├── overview.md               # High-level synthesis of entire KB
│   ├── entities/                 # Entity pages (people, orgs, products)
│   ├── concepts/                 # Concept pages (techniques, theories)
│   ├── sources/                  # Source summary pages
│   ├── comparisons/              # Comparative analyses
│   └── synthesis/                # Cross-cutting syntheses
└── output/                       # Generated artifacts
    ├── slides/                   # Marp slide decks
    ├── charts/                   # matplotlib / visualization output
    └── reports/                  # Research reports, briefs
```

Three layers:
1. **Raw sources** (`raw/`) — Immutable. The LLM reads from here but never modifies. This is the source of truth.
2. **The wiki** (`wiki/`) — LLM-owned. The LLM creates, updates, and maintains all pages. The human reads it; the LLM writes it.
3. **The schema** (`SCHEMA.md`) — Conventions, page formats, workflows. Co-evolved by human and LLM over time.

## Setup

Before first use, determine the vault path. Check for an environment variable:

```bash
echo $WIKI_VAULT
```

If unset, ask the user for their Obsidian vault path. Then initialize the directory structure:

```bash
python <skill-path>/scripts/wiki_init.py <vault-path>
```

This creates all directories, a starter `SCHEMA.md`, empty `index.md` and `log.md`, and a `.gitignore`. It is idempotent — safe to run on an existing vault.

For search capability, check if `qmd` is available:

```bash
which qmd 2>/dev/null && echo "qmd available" || echo "qmd not found — will use index-based search"
```

If `qmd` is installed, the skill uses hybrid BM25/vector search. Otherwise it falls back to grep + index.md navigation, which works well up to ~100 sources.

## Operations

### 1. Ingest

When the user adds a new source (drops a file into `raw/`, provides a URL, or pastes content):

```bash
python <skill-path>/scripts/wiki_ingest.py <vault-path> <source-path-or-url> [--batch]
```

The ingest flow:
1. **Read** the source document completely
2. **Discuss** key takeaways with the user (unless `--batch` mode)
3. **Create** a source summary page in `wiki/sources/`
4. **Update** relevant entity and concept pages (create new ones if needed)
5. **Update** `wiki/index.md` with the new entry
6. **Update** cross-references and backlinks across affected pages
7. **Append** to `wiki/log.md` with timestamp and summary
8. **Report** what changed — typically 5-15 pages touched per source

For web URLs, the script fetches content and converts to markdown automatically. For images, it downloads them to `raw/assets/` and updates references.

**Important**: Ingest one source at a time by default, staying involved with the user. Batch mode (`--batch`) processes multiple sources with less supervision — useful for initial bulk loading, but the user should review afterward.

**Page format conventions** — every wiki page should include YAML frontmatter:

```yaml
---
title: Page Title
type: entity | concept | source | comparison | synthesis
created: 2026-04-07
updated: 2026-04-07
sources: [source-filename-1, source-filename-2]
tags: [tag1, tag2]
---
```

Use `[[wikilinks]]` for internal links (Obsidian-native). When referencing raw sources, use relative paths: `[source](../raw/filename.md)`.

### 2. Query

When the user asks a question against the wiki:

```bash
python <skill-path>/scripts/wiki_query.py <vault-path> "<question>" [--format md|marp|chart|canvas]
```

The query flow:
1. **Search** — Read `wiki/index.md` to identify relevant pages. If `qmd` is available, also run a search for broader coverage.
2. **Read** — Load the relevant wiki pages (not raw sources — the wiki has already compiled the knowledge).
3. **Synthesize** — Answer the question with citations to wiki pages.
4. **Output** — Render the answer in the requested format:
   - `md` (default): A markdown file saved to `wiki/` or `output/reports/`
   - `marp`: A Marp-format slide deck saved to `output/slides/`
   - `chart`: A matplotlib visualization saved to `output/charts/`
   - `canvas`: An Obsidian Canvas file (`.canvas` JSON)
5. **File back** (optional) — If the answer is valuable (comparison, analysis, new connection), file it back into the wiki as a new page. The user's explorations compound in the knowledge base.

For complex multi-step queries, the LLM should plan its research path: which pages to read first, what follow-up searches to run, whether to cross-reference multiple concept pages. Think of it as researching within your own library.

### 3. Lint

Periodic health checks to maintain wiki quality:

```bash
python <skill-path>/scripts/wiki_lint.py <vault-path> [--fix] [--web-search]
```

The lint checks:
- **Contradictions**: Pages that make conflicting claims
- **Stale data**: Claims superseded by newer sources
- **Orphan pages**: Pages with no inbound links
- **Missing pages**: Concepts mentioned frequently but lacking their own page
- **Broken links**: `[[wikilinks]]` pointing to non-existent pages
- **Missing cross-references**: Related pages that should link to each other but don't
- **Data gaps**: Important topics with thin coverage — suggest sources to find
- **Index consistency**: Ensure `index.md` is complete and accurate

With `--fix`, the LLM auto-repairs what it can (broken links, missing cross-refs, index updates). With `--web-search`, it actively searches the web to fill data gaps and update stale claims.

The lint report is appended to `wiki/log.md` and optionally saved as `output/reports/lint-<date>.md`.

### 4. Search

For searching within the wiki:

```bash
python <skill-path>/scripts/wiki_search.py <vault-path> "<query>" [--top-k 10]
```

If `qmd` is available, this wraps it for hybrid BM25/vector search with re-ranking. Otherwise falls back to a combination of:
- Grep-based full-text search
- Index.md keyword matching
- Frontmatter tag filtering

Results include page title, relevance snippet, and path — suitable for both human reading and LLM tool use.

## Output Formats

All outputs should be viewable directly in Obsidian:

| Format | Extension | Obsidian Plugin | Use Case |
|--------|-----------|----------------|----------|
| Markdown | `.md` | Built-in | Articles, analyses, reports |
| Marp slides | `.md` (with marp frontmatter) | Marp Slides | Presentations |
| Charts | `.png` / `.svg` | Built-in image embed | Data visualization |
| Canvas | `.canvas` | Built-in | Relationship maps |
| Dataview | YAML frontmatter | Dataview plugin | Dynamic tables & lists |

When generating Marp slides, use this frontmatter:

```yaml
---
marp: true
theme: default
paginate: true
---
```

## Index & Log Management

**`wiki/index.md`** — Content-oriented catalog. Structure:

```markdown
# Wiki Index
> Auto-maintained by LLM. Last updated: 2026-04-07

## Entities
- [[Entity Name]] — one-line summary (N sources)

## Concepts  
- [[Concept Name]] — one-line summary (N sources)

## Sources
- [[Source Summary]] — title, date, key takeaway

## Comparisons
- [[Comparison Title]] — what's being compared

## Synthesis
- [[Synthesis Title]] — cross-cutting theme
```

The LLM updates this on every ingest and periodically during lint. When answering queries, read the index first to find relevant pages, then drill into specifics.

**`wiki/log.md`** — Chronological, append-only. Format:

```markdown
## [2026-04-07] ingest | "Article Title"
- Created: sources/article-title.md
- Updated: entities/person-name.md, concepts/technique-name.md
- New pages: concepts/new-concept.md
- Index updated: +1 source, +1 concept

## [2026-04-07] query | "What are the tradeoffs of X vs Y?"
- Searched: 5 pages
- Output: comparisons/x-vs-y.md (filed back to wiki)

## [2026-04-07] lint | health check
- Fixed: 3 broken links, 2 missing cross-refs
- Flagged: 1 contradiction (entities/foo.md vs concepts/bar.md)
- Suggested: 2 new sources to investigate
```

Each entry starts with `## [YYYY-MM-DD] operation | description` — this makes the log parseable:
```bash
grep "^## \[" wiki/log.md | tail -10
```

## Tips for Effective Use

- **One source at a time** during active research sessions. Stay engaged, guide emphasis, check the updates in Obsidian in real time.
- **Batch ingest** for initial loading of a document collection. Review afterward.
- **File back valuable queries.** When an answer reveals a new connection or produces a useful comparison, save it to the wiki. Your explorations compound.
- **Use Obsidian Graph View** to see wiki shape — hub pages, orphans, clusters.
- **Run lint weekly** on active wikis. Monthly on dormant ones.
- **The wiki is a git repo.** Commit after significant changes. You get version history for free.

## Platform Adapters

This skill works across multiple LLM agent platforms. Read the appropriate adapter file based on your environment:

- **Claude Code**: `adapters/claude-code/README.md` — Uses CLAUDE.md as schema file, `claude` CLI for operations
- **OpenCode / OpenClaw**: `adapters/opencode/README.md` — Uses AGENTS.md as schema file, compatible with Codex-style workflows
- **Mira**: `adapters/mira/README.md` — Uses sandbox filesystem, integrates with Feishu for output sharing

The core workflows (ingest, query, lint, search) are identical across platforms. Only the schema file name and output delivery mechanism differ.

## References

- `references/karpathy-llm-wiki.md` — Original Karpathy LLM Wiki pattern document (full text)
- `references/page-templates.md` — Templates for each wiki page type
- `references/schema-template.md` — Starter SCHEMA.md template
- `references/qmd-integration.md` — qmd search engine setup and usage guide
- `references/obsidian-setup.md` — Recommended Obsidian plugins and configuration
