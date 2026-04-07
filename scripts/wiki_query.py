#!/usr/bin/env python3
"""
wiki_query.py — Search and query the LLM Wiki.

Usage:
    python wiki_query.py <vault-path> "<query>" [--top-k 10] [--format md|marp|chart]

Search strategy:
    1. If qmd is available, use hybrid BM25/vector search
    2. Otherwise, search index.md + grep fallback

Returns JSON with matched pages and snippets, suitable for LLM consumption.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def search_with_qmd(vault_path: str, query: str, top_k: int = 10) -> list:
    """Use qmd for hybrid search if available."""
    wiki_dir = os.path.join(vault_path, "wiki")
    try:
        result = subprocess.run(
            ["qmd", "search", query, "--dir", wiki_dir, "--top-k", str(top_k), "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass
    return []


def search_with_index(vault_path: str, query: str, top_k: int = 10) -> list:
    """Search using index.md content matching."""
    index_path = os.path.join(vault_path, "wiki", "index.md")
    results = []
    
    if not os.path.exists(index_path):
        return results
    
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()
    
    query_terms = set(query.lower().split())
    
    # Parse index entries: - [[Page Name]] — description
    pattern = r'-\s*\[\[([^\]]+)\]\]\s*[—–-]\s*(.*?)$'
    for match in re.finditer(pattern, index_content, re.MULTILINE):
        page_name = match.group(1)
        description = match.group(2).strip()
        
        # Score by term overlap
        text = (page_name + " " + description).lower()
        score = sum(1 for term in query_terms if term in text)
        
        if score > 0:
            # Find the actual file
            page_slug = page_name.lower().replace(' ', '-')
            page_path = None
            for subdir in ['entities', 'concepts', 'sources', 'comparisons', 'synthesis']:
                candidate = os.path.join(vault_path, "wiki", subdir, f"{page_slug}.md")
                if os.path.exists(candidate):
                    page_path = f"wiki/{subdir}/{page_slug}.md"
                    break
            
            if not page_path:
                # Try direct match
                candidate = os.path.join(vault_path, "wiki", f"{page_slug}.md")
                if os.path.exists(candidate):
                    page_path = f"wiki/{page_slug}.md"
            
            results.append({
                "page": page_name,
                "path": page_path,
                "summary": description,
                "score": score
            })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def search_with_grep(vault_path: str, query: str, top_k: int = 10) -> list:
    """Fallback: grep-based full-text search across wiki."""
    wiki_dir = os.path.join(vault_path, "wiki")
    results = []
    
    terms = query.lower().split()
    
    for md_file in Path(wiki_dir).rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        
        content_lower = content.lower()
        score = sum(content_lower.count(term) for term in terms)
        
        if score > 0:
            # Extract title from frontmatter or first heading
            title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
            if not title_match:
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else md_file.stem.replace('-', ' ').title()
            
            # Extract snippet around first match
            for term in terms:
                idx = content_lower.find(term)
                if idx >= 0:
                    start = max(0, idx - 80)
                    end = min(len(content), idx + 120)
                    snippet = content[start:end].replace('\n', ' ').strip()
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(content):
                        snippet = snippet + "..."
                    break
            else:
                snippet = ""
            
            rel_path = str(md_file.relative_to(vault_path))
            results.append({
                "page": title,
                "path": rel_path,
                "snippet": snippet,
                "score": score
            })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def generate_output_template(query: str, fmt: str) -> str:
    """Generate an output template for the specified format."""
    if fmt == "marp":
        return f"""\
---
marp: true
theme: default
paginate: true
---

# {{title}}

---

## Query
> {query}

---

## Key Findings

<!-- Fill with findings from wiki research -->

---

## Details

<!-- Detailed analysis slides -->

---

## Sources & References

<!-- Wiki page citations -->
"""
    elif fmt == "chart":
        return f"""\
# Chart Request: {query}

Generate a matplotlib chart using this template:

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

fig, ax = plt.subplots(figsize=(10, 6))

# TODO: Fill with data from wiki research
# ax.bar(categories, values)
# ax.plot(x, y)

ax.set_title('{{title}}')
ax.set_xlabel('{{xlabel}}')
ax.set_ylabel('{{ylabel}}')
plt.tight_layout()
plt.savefig('output/charts/{{filename}}.png', dpi=150)
print("Chart saved to output/charts/{{filename}}.png")
```
"""
    else:  # md
        return f"""\
---
title: "{{title}}"
type: synthesis
created: {{date}}
query: "{query}"
sources: []
tags: []
---

# {{title}}

> Generated from wiki query: {query}

## Summary

<!-- Synthesized answer -->

## Analysis

<!-- Detailed analysis with citations to wiki pages -->

## References

<!-- List of wiki pages consulted -->
"""


def main():
    parser = argparse.ArgumentParser(description="Query the LLM Wiki knowledge base.")
    parser.add_argument("vault_path", help="Path to the Obsidian vault root")
    parser.add_argument("query", help="Search query or question")
    parser.add_argument("--top-k", type=int, default=10, help="Number of results to return")
    parser.add_argument("--format", choices=["md", "marp", "chart", "canvas"], default="md",
                       help="Output format template")
    args = parser.parse_args()
    
    vault_path = os.path.expanduser(args.vault_path)
    
    # Try qmd first, then index, then grep
    results = search_with_qmd(vault_path, args.query, args.top_k)
    search_method = "qmd"
    
    if not results:
        results = search_with_index(vault_path, args.query, args.top_k)
        search_method = "index"
    
    if not results:
        results = search_with_grep(vault_path, args.query, args.top_k)
        search_method = "grep"
    
    output = {
        "query": args.query,
        "search_method": search_method,
        "result_count": len(results),
        "results": results,
    }
    
    if args.format != "md":
        output["output_template"] = generate_output_template(args.query, args.format)
    
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
