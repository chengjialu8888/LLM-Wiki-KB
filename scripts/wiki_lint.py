#!/usr/bin/env python3
"""
wiki_lint.py — Health check and maintenance for the LLM Wiki.

Usage:
    python wiki_lint.py <vault-path> [--fix] [--web-search] [--verbose]

Checks:
    - Broken wikilinks
    - Orphan pages (no inbound links)
    - Missing pages (referenced but don't exist)
    - Index consistency
    - Frontmatter completeness
    - Cross-reference gaps

Returns a JSON report with findings and suggested fixes.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def scan_wiki_pages(vault_path: str) -> dict:
    """Scan all wiki pages and extract metadata."""
    wiki_dir = os.path.join(vault_path, "wiki")
    pages = {}
    
    for md_file in Path(wiki_dir).rglob("*.md"):
        rel_path = str(md_file.relative_to(vault_path))
        content = md_file.read_text(encoding="utf-8")
        
        # Extract frontmatter
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        frontmatter = {}
        if fm_match:
            for line in fm_match.group(1).split('\n'):
                kv = line.split(':', 1)
                if len(kv) == 2:
                    frontmatter[kv[0].strip()] = kv[1].strip().strip('"\'')
        
        # Extract wikilinks
        wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', content)
        
        # Extract standard markdown links to wiki
        md_links = re.findall(r'\[([^\]]+)\]\((?:\.\./)?(wiki/[^)]+)\)', content)
        
        # Word count (rough)
        text_only = re.sub(r'---.*?---', '', content, count=1, flags=re.DOTALL)
        text_only = re.sub(r'```.*?```', '', text_only, flags=re.DOTALL)
        word_count = len(text_only.split())
        
        page_name = md_file.stem
        pages[page_name] = {
            "path": rel_path,
            "full_path": str(md_file),
            "frontmatter": frontmatter,
            "wikilinks": wikilinks,
            "md_links": md_links,
            "word_count": word_count,
            "has_frontmatter": bool(fm_match),
        }
    
    return pages


def check_broken_links(pages: dict) -> list:
    """Find wikilinks that point to non-existent pages."""
    issues = []
    all_page_names = set(pages.keys())
    # Also match with various normalizations
    normalized = {name.lower().replace(' ', '-'): name for name in all_page_names}
    
    for page_name, info in pages.items():
        for link in info["wikilinks"]:
            link_normalized = link.lower().replace(' ', '-')
            if link_normalized not in normalized and link not in all_page_names:
                issues.append({
                    "type": "broken_link",
                    "severity": "warning",
                    "page": page_name,
                    "path": info["path"],
                    "link": link,
                    "message": f"Page '{page_name}' links to [[{link}]] which does not exist"
                })
    return issues


def check_orphan_pages(pages: dict) -> list:
    """Find pages with no inbound links."""
    issues = []
    # Special pages that don't need inbound links
    special = {"index", "log", "overview"}
    
    # Build inbound link map
    inbound = defaultdict(set)
    for page_name, info in pages.items():
        for link in info["wikilinks"]:
            link_norm = link.lower().replace(' ', '-')
            inbound[link_norm].add(page_name)
    
    for page_name, info in pages.items():
        if page_name in special:
            continue
        page_norm = page_name.lower().replace(' ', '-')
        if page_norm not in inbound and page_name not in inbound:
            issues.append({
                "type": "orphan_page",
                "severity": "info",
                "page": page_name,
                "path": info["path"],
                "message": f"Page '{page_name}' has no inbound links — consider linking from related pages"
            })
    return issues


def check_frontmatter(pages: dict) -> list:
    """Check for missing or incomplete frontmatter."""
    issues = []
    special = {"index", "log"}
    required_fields = {"title", "type", "created"}
    
    for page_name, info in pages.items():
        if page_name in special:
            continue
        if not info["has_frontmatter"]:
            issues.append({
                "type": "missing_frontmatter",
                "severity": "warning",
                "page": page_name,
                "path": info["path"],
                "message": f"Page '{page_name}' has no YAML frontmatter"
            })
        else:
            missing = required_fields - set(info["frontmatter"].keys())
            if missing:
                issues.append({
                    "type": "incomplete_frontmatter",
                    "severity": "info",
                    "page": page_name,
                    "path": info["path"],
                    "missing_fields": list(missing),
                    "message": f"Page '{page_name}' is missing frontmatter: {', '.join(missing)}"
                })
    return issues


def check_index_consistency(pages: dict, vault_path: str) -> list:
    """Check that index.md lists all wiki pages."""
    issues = []
    index_path = os.path.join(vault_path, "wiki", "index.md")
    
    if not os.path.exists(index_path):
        issues.append({
            "type": "missing_index",
            "severity": "error",
            "message": "wiki/index.md does not exist"
        })
        return issues
    
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read().lower()
    
    special = {"index", "log", "overview"}
    
    for page_name in pages:
        if page_name in special:
            continue
        if page_name.lower() not in index_content and page_name.replace('-', ' ').lower() not in index_content:
            issues.append({
                "type": "missing_from_index",
                "severity": "warning",
                "page": page_name,
                "path": pages[page_name]["path"],
                "message": f"Page '{page_name}' exists but is not listed in index.md"
            })
    return issues


def compute_stats(pages: dict, vault_path: str) -> dict:
    """Compute wiki statistics."""
    raw_dir = os.path.join(vault_path, "raw")
    raw_count = sum(1 for f in Path(raw_dir).glob("*.md")) if os.path.exists(raw_dir) else 0
    
    total_words = sum(info["word_count"] for info in pages.values())
    total_links = sum(len(info["wikilinks"]) for info in pages.values())
    
    type_counts = defaultdict(int)
    for info in pages.values():
        ptype = info["frontmatter"].get("type", "unknown")
        type_counts[ptype] += 1
    
    return {
        "total_pages": len(pages),
        "total_words": total_words,
        "total_wikilinks": total_links,
        "raw_sources": raw_count,
        "pages_by_type": dict(type_counts),
        "avg_words_per_page": round(total_words / max(len(pages), 1)),
    }


def main():
    parser = argparse.ArgumentParser(description="Lint the LLM Wiki knowledge base.")
    parser.add_argument("vault_path", help="Path to the Obsidian vault root")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues where possible")
    parser.add_argument("--web-search", action="store_true", help="Search web to fill data gaps")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()
    
    vault_path = os.path.expanduser(args.vault_path)
    
    if not os.path.exists(os.path.join(vault_path, "wiki")):
        print(json.dumps({"error": "No wiki/ directory found. Run wiki_init.py first."}, indent=2))
        sys.exit(1)
    
    pages = scan_wiki_pages(vault_path)
    
    # Run all checks
    all_issues = []
    all_issues.extend(check_broken_links(pages))
    all_issues.extend(check_orphan_pages(pages))
    all_issues.extend(check_frontmatter(pages))
    all_issues.extend(check_index_consistency(pages, vault_path))
    
    stats = compute_stats(pages, vault_path)
    
    # Summarize
    by_severity = defaultdict(int)
    by_type = defaultdict(int)
    for issue in all_issues:
        by_severity[issue["severity"]] += 1
        by_type[issue["type"]] += 1
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "vault_path": vault_path,
        "stats": stats,
        "issue_count": len(all_issues),
        "by_severity": dict(by_severity),
        "by_type": dict(by_type),
        "issues": all_issues,
    }
    
    if args.fix:
        report["fix_instructions"] = (
            "Auto-fix requested. The LLM should now:\n"
            "1. Fix broken links by creating stub pages or correcting link targets\n"
            "2. Add missing pages to index.md\n"
            "3. Add frontmatter to pages missing it\n"
            "4. Link orphan pages from relevant existing pages\n"
            "5. Append lint results to wiki/log.md"
        )
    
    if args.web_search:
        report["web_search_instructions"] = (
            "Web search requested. The LLM should:\n"
            "1. Identify data gaps from the issues list\n"
            "2. Search the web for missing/stale information\n"
            "3. Update wiki pages with fresh data\n"
            "4. Note all web-sourced updates in wiki/log.md"
        )
    
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # Summary to stderr for human readability
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"Wiki Lint Report — {vault_path}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)
    print(f"Pages: {stats['total_pages']} | Words: {stats['total_words']:,} | Links: {stats['total_wikilinks']}", file=sys.stderr)
    print(f"Raw sources: {stats['raw_sources']}", file=sys.stderr)
    print(f"\nIssues: {len(all_issues)}", file=sys.stderr)
    for sev in ["error", "warning", "info"]:
        if sev in by_severity:
            print(f"  {sev}: {by_severity[sev]}", file=sys.stderr)


if __name__ == "__main__":
    main()
