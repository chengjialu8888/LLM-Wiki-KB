# Karpathy LLM Wiki — Original Reference

> Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
> Author: Andrej Karpathy
> Date: April 4, 2026

This skill is based on Andrej Karpathy's LLM Wiki pattern. The full original document
is reproduced here for reference. The skill's SKILL.md operationalizes these ideas into
concrete workflows and scripts.

## Key Design Principles (extracted)

1. **Persistent compounding artifact** — The wiki accumulates knowledge, unlike RAG which re-derives on every query
2. **LLM-owned wiki** — The human reads, the LLM writes. The human rarely edits directly.
3. **Three layers** — Raw (immutable sources) → Wiki (LLM-maintained) → Schema (conventions)
4. **Operations** — Ingest, Query, Lint — each with distinct workflows
5. **Index + Log** — Content catalog (index.md) + chronological record (log.md)
6. **File back valuable queries** — Explorations compound in the knowledge base
7. **Obsidian as IDE** — The LLM is the programmer, the wiki is the codebase, Obsidian is the IDE
8. **Git for free** — The wiki is just markdown files in a directory = version control built-in

## The Memex Connection

Karpathy draws a parallel to Vannevar Bush's Memex (1945) — a personal, curated knowledge
store with associative trails. The key insight: Bush's vision was closer to this than to what
the web became. The part he couldn't solve was maintenance. LLMs handle that.
