#!/usr/bin/env python3
"""
wiki_init.py — Initialize an LLM Wiki Knowledge Base vault.

Usage:
    python wiki_init.py <vault-path> [--domain <domain-name>]

Creates the directory structure, starter files, and SCHEMA.md.
Idempotent — safe to run on an existing vault.
"""

import argparse
import os
import sys
from datetime import datetime

DIRS = [
    "raw",
    "raw/assets",
    "wiki",
    "wiki/entities",
    "wiki/concepts",
    "wiki/sources",
    "wiki/comparisons",
    "wiki/synthesis",
    "output",
    "output/slides",
    "output/charts",
    "output/reports",
]

GITIGNORE = """\
# OS
.DS_Store
Thumbs.db

# Obsidian
.obsidian/workspace.json
.obsidian/workspace-mobile.json

# Temporary
*.tmp
*.bak
"""

def create_index(vault_path: str):
    path = os.path.join(vault_path, "wiki", "index.md")
    if os.path.exists(path):
        return False
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""\
# Wiki Index

> Auto-maintained by LLM. Last updated: {today}
> 
> This file catalogs every page in the wiki. Read this first when answering queries
> to find relevant pages, then drill into specifics.

## Overview
- [[overview]] — High-level synthesis of the entire knowledge base

## Entities
<!-- People, organizations, products, datasets -->

## Concepts
<!-- Techniques, theories, methodologies, frameworks -->

## Sources
<!-- Summary pages for each ingested raw source -->

## Comparisons
<!-- Side-by-side analyses -->

## Synthesis
<!-- Cross-cutting themes and meta-analyses -->
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def create_log(vault_path: str):
    path = os.path.join(vault_path, "wiki", "log.md")
    if os.path.exists(path):
        return False
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""\
# Wiki Log

> Chronological, append-only record of all wiki operations.
> Each entry: `## [YYYY-MM-DD] operation | description`
> Parse with: `grep "^## \\[" wiki/log.md | tail -10`

## [{today}] init | Knowledge base initialized
- Created directory structure
- Created index.md, log.md, overview.md, SCHEMA.md
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def create_overview(vault_path: str, domain: str):
    path = os.path.join(vault_path, "wiki", "overview.md")
    if os.path.exists(path):
        return False
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""\
---
title: Overview
type: synthesis
created: {today}
updated: {today}
sources: []
tags: [overview, meta]
---

# {domain or 'Knowledge Base'} — Overview

> This page provides a high-level synthesis of the entire knowledge base.
> It is automatically updated as new sources are ingested and new connections emerge.

## Summary

*This knowledge base is empty. Ingest your first source to begin building.*

## Key Themes

*No themes yet.*

## Open Questions

*No open questions yet.*

## Statistics
- Total sources: 0
- Total wiki pages: 3 (index, log, overview)
- Total words: ~0
- Last ingest: N/A
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def create_schema(vault_path: str, domain: str):
    path = os.path.join(vault_path, "SCHEMA.md")
    if os.path.exists(path):
        return False

    # Read template if available
    template_path = os.path.join(os.path.dirname(__file__), "..", "references", "schema-template.md")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("{{DOMAIN}}", domain or "General Research")
        content = content.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d"))
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        content = f"""\
# SCHEMA — {domain or 'Knowledge Base'} Wiki

> Created: {today}
> This file defines conventions for the LLM wiki maintainer.

## Directory Structure
- `raw/` — Immutable source documents. Never modify.
- `wiki/` — LLM-maintained wiki pages. All edits go here.
- `output/` — Generated artifacts (slides, charts, reports).

## Page Conventions
- Every wiki page has YAML frontmatter: title, type, created, updated, sources, tags
- Use [[wikilinks]] for internal links
- Use relative paths for raw source references
- Keep pages focused — one entity/concept per page

## Ingest Workflow
1. Read the new source completely
2. Create a summary page in wiki/sources/
3. Update or create entity and concept pages
4. Update index.md and log.md
5. Update cross-references across affected pages

## Query Workflow
1. Read index.md to find relevant pages
2. Read the relevant wiki pages
3. Synthesize an answer with citations
4. Optionally file valuable answers back into wiki/

## Naming Conventions
- Filenames: kebab-case (e.g., `transformer-architecture.md`)
- Use descriptive names, not IDs
- Source summaries: `sources/<source-title>.md`
- Entity pages: `entities/<entity-name>.md`
- Concept pages: `concepts/<concept-name>.md`
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def main():
    parser = argparse.ArgumentParser(description="Initialize an LLM Wiki Knowledge Base vault.")
    parser.add_argument("vault_path", help="Path to the Obsidian vault root")
    parser.add_argument("--domain", default="", help="Domain name for this knowledge base (e.g., 'AI Research')")
    args = parser.parse_args()

    vault_path = os.path.expanduser(args.vault_path)

    # Create directories
    created_dirs = []
    for d in DIRS:
        full_path = os.path.join(vault_path, d)
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
            created_dirs.append(d)

    # Create .gitignore
    gitignore_path = os.path.join(vault_path, ".gitignore")
    gitignore_created = False
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(GITIGNORE)
        gitignore_created = True

    # Create starter files
    index_created = create_index(vault_path)
    log_created = create_log(vault_path)
    overview_created = create_overview(vault_path, args.domain)
    schema_created = create_schema(vault_path, args.domain)

    # Report
    print(f"✓ Vault initialized at: {vault_path}")
    if created_dirs:
        print(f"  Created {len(created_dirs)} directories: {', '.join(created_dirs)}")
    else:
        print("  All directories already exist")
    
    files_created = []
    if index_created: files_created.append("wiki/index.md")
    if log_created: files_created.append("wiki/log.md")
    if overview_created: files_created.append("wiki/overview.md")
    if schema_created: files_created.append("SCHEMA.md")
    if gitignore_created: files_created.append(".gitignore")
    
    if files_created:
        print(f"  Created {len(files_created)} files: {', '.join(files_created)}")
    else:
        print("  All starter files already exist (no overwrite)")
    
    print(f"\nNext steps:")
    print(f"  1. Open {vault_path} as an Obsidian vault")
    print(f"  2. Drop source documents into raw/")
    print(f"  3. Run: python wiki_ingest.py {vault_path} raw/<source-file>")


if __name__ == "__main__":
    main()
