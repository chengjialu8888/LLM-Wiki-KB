#!/usr/bin/env python3
"""
wiki_search.py — Search the LLM Wiki using qmd or fallback methods.

Usage:
    python wiki_search.py <vault-path> "<query>" [--top-k 10] [--json]

Wraps qmd (hybrid BM25/vector search) when available, with grep fallback.
Designed to be used both by humans (CLI) and by LLMs (as a tool).
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def has_qmd() -> bool:
    """Check if qmd is installed and available."""
    try:
        result = subprocess.run(["qmd", "--version"], capture_output=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def search_qmd(wiki_dir: str, query: str, top_k: int) -> list:
    """Search using qmd hybrid search."""
    try:
        result = subprocess.run(
            ["qmd", "search", query, "--dir", wiki_dir, "--top-k", str(top_k), "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "results" in data:
                return data["results"]
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        print(f"qmd search failed: {e}", file=sys.stderr)
    return []


def search_grep(wiki_dir: str, query: str, top_k: int) -> list:
    """Fallback grep-based search."""
    terms = query.lower().split()
    results = []
    
    for md_file in Path(wiki_dir).rglob("*.md"):
        if md_file.name in ("log.md",):  # skip log, but include index
            continue
        
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        
        content_lower = content.lower()
        
        # Score: number of term occurrences
        score = sum(content_lower.count(t) for t in terms)
        if score == 0:
            continue
        
        # Bonus for terms in title/heading
        first_heading = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if first_heading:
            heading_lower = first_heading.group(1).lower()
            score += sum(5 for t in terms if t in heading_lower)
        
        # Extract title
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else (
            first_heading.group(1) if first_heading else md_file.stem.replace('-', ' ').title()
        )
        
        # Extract snippet
        snippet = ""
        for term in terms:
            idx = content_lower.find(term)
            if idx >= 0:
                start = max(0, idx - 60)
                end = min(len(content), idx + 100)
                snippet = content[start:end].replace('\n', ' ').strip()
                if start > 0: snippet = "…" + snippet
                if end < len(content): snippet += "…"
                break
        
        results.append({
            "title": title,
            "path": str(md_file.relative_to(Path(wiki_dir).parent)),
            "snippet": snippet,
            "score": score
        })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def main():
    parser = argparse.ArgumentParser(description="Search the LLM Wiki.")
    parser.add_argument("vault_path", help="Path to the Obsidian vault root")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top-k", type=int, default=10, help="Max results")
    parser.add_argument("--json", action="store_true", help="Output JSON (default for piped output)")
    args = parser.parse_args()
    
    vault_path = os.path.expanduser(args.vault_path)
    wiki_dir = os.path.join(vault_path, "wiki")
    
    if not os.path.isdir(wiki_dir):
        print(json.dumps({"error": "wiki/ directory not found"}))
        sys.exit(1)
    
    use_json = args.json or not sys.stdout.isatty()
    
    # Try qmd first
    method = "grep"
    if has_qmd():
        results = search_qmd(wiki_dir, args.query, args.top_k)
        if results:
            method = "qmd"
    
    if method == "grep":
        results = search_grep(wiki_dir, args.query, args.top_k)
    
    if use_json:
        output = {
            "query": args.query,
            "method": method,
            "count": len(results),
            "results": results
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"Search: \"{args.query}\" ({method}, {len(results)} results)\n")
        for i, r in enumerate(results, 1):
            title = r.get("title", r.get("path", "?"))
            path = r.get("path", "")
            snippet = r.get("snippet", "")
            print(f"  {i}. {title}")
            print(f"     {path}")
            if snippet:
                print(f"     {snippet}")
            print()


if __name__ == "__main__":
    main()
