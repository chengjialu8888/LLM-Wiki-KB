#!/usr/bin/env python3
from typing import Tuple, Dict, List
"""
wiki_ingest.py — Ingest a source document into the LLM Wiki.

Usage:
    python wiki_ingest.py <vault-path> <source> [--batch] [--no-discuss]

<source> can be:
    - A local file path (relative to vault or absolute)
    - A URL (https://...) — will be fetched and converted to markdown
    - A directory path — ingests all .md files in it (implies --batch)

This script handles the mechanical parts of ingest:
    - URL fetching and markdown conversion
    - Image downloading and localization
    - File placement in raw/
    - Log entry template generation

The actual wiki compilation (summarization, entity extraction, cross-referencing)
is performed by the LLM agent that invokes this script.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser


class HTMLToMarkdown(HTMLParser):
    """Minimal HTML to markdown converter for web articles."""
    
    def __init__(self):
        super().__init__()
        self.result = []
        self.current_tag = None
        self.in_pre = False
        self.in_code = False
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'aside'}
        self.skip_depth = 0
        self.list_depth = 0
        self.images = []
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in self.skip_tags:
            self.skip_depth += 1
            return
        if self.skip_depth > 0:
            return
            
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            self.result.append('\n' + '#' * level + ' ')
            self.current_tag = tag
        elif tag == 'p':
            self.result.append('\n\n')
        elif tag == 'br':
            self.result.append('\n')
        elif tag == 'strong' or tag == 'b':
            self.result.append('**')
        elif tag == 'em' or tag == 'i':
            self.result.append('*')
        elif tag == 'code':
            if self.in_pre:
                return
            self.result.append('`')
            self.in_code = True
        elif tag == 'pre':
            self.result.append('\n```\n')
            self.in_pre = True
        elif tag == 'a':
            href = attrs_dict.get('href', '')
            self.result.append('[')
            self._pending_href = href
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '')
            if src:
                self.result.append(f'![{alt}]({src})')
                self.images.append(src)
        elif tag == 'ul' or tag == 'ol':
            self.list_depth += 1
        elif tag == 'li':
            indent = '  ' * (self.list_depth - 1)
            self.result.append(f'\n{indent}- ')
        elif tag == 'blockquote':
            self.result.append('\n> ')
    
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth > 0:
            return
            
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.result.append('\n')
            self.current_tag = None
        elif tag == 'strong' or tag == 'b':
            self.result.append('**')
        elif tag == 'em' or tag == 'i':
            self.result.append('*')
        elif tag == 'code':
            if self.in_pre:
                return
            self.result.append('`')
            self.in_code = False
        elif tag == 'pre':
            self.result.append('\n```\n')
            self.in_pre = False
        elif tag == 'a':
            href = getattr(self, '_pending_href', '')
            self.result.append(f']({href})')
        elif tag == 'ul' or tag == 'ol':
            self.list_depth = max(0, self.list_depth - 1)
    
    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        self.result.append(data)
    
    def get_markdown(self):
        text = ''.join(self.result)
        # Clean up excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


def fetch_url(url: str) -> Tuple[str, str, List[str]]:
    """Fetch a URL and convert to markdown. Returns (title, markdown, image_urls)."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; LLM-Wiki-KB/1.0)'
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8', errors='replace')
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to fetch {url}: {e}")
    
    # Extract title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else url.split('/')[-1]
    
    # Extract main content (try article, main, then body)
    for tag in ['article', 'main', 'body']:
        pattern = f'<{tag}[^>]*>(.*?)</{tag}>'
        match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if match:
            html_content = match.group(1)
            break
    else:
        html_content = html
    
    converter = HTMLToMarkdown()
    converter.feed(html_content)
    markdown = converter.get_markdown()
    
    return title, markdown, converter.images


def download_images(images: list, assets_dir: str, source_name: str) -> Dict:
    """Download images to local assets directory. Returns url->local_path mapping."""
    os.makedirs(assets_dir, exist_ok=True)
    mapping = {}
    
    for i, img_url in enumerate(images):
        if not img_url.startswith('http'):
            continue
        try:
            ext = os.path.splitext(img_url.split('?')[0])[1] or '.png'
            local_name = f"{source_name}-img-{i:03d}{ext}"
            local_path = os.path.join(assets_dir, local_name)
            
            if not os.path.exists(local_path):
                req = urllib.request.Request(img_url, headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; LLM-Wiki-KB/1.0)'
                })
                with urllib.request.urlopen(req, timeout=15) as resp:
                    with open(local_path, 'wb') as f:
                        f.write(resp.read())
            
            mapping[img_url] = os.path.join("assets", local_name)
        except Exception as e:
            print(f"  ⚠ Failed to download image: {img_url} ({e})", file=sys.stderr)
    
    return mapping


def slugify(text: str) -> str:
    """Convert text to kebab-case filename."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:80].strip('-')


def ingest_file(vault_path: str, source_path: str, batch: bool = False) -> Dict:
    """Ingest a single source file. Returns metadata about what was done."""
    vault_path = os.path.expanduser(vault_path)
    raw_dir = os.path.join(vault_path, "raw")
    assets_dir = os.path.join(vault_path, "raw", "assets")
    
    today = datetime.now().strftime("%Y-%m-%d")
    result = {"status": "ok", "source": source_path, "actions": []}
    
    # Determine if URL or local file
    if source_path.startswith("http://") or source_path.startswith("https://"):
        print(f"Fetching: {source_path}")
        title, markdown, images = fetch_url(source_path)
        slug = slugify(title)
        
        # Add frontmatter
        content = f"""\
---
title: "{title}"
url: "{source_path}"
clipped: {today}
type: web-article
---

# {title}

> Source: {source_path}
> Clipped: {today}

{markdown}
"""
        # Save to raw/
        raw_file = os.path.join(raw_dir, f"{slug}.md")
        with open(raw_file, "w", encoding="utf-8") as f:
            f.write(content)
        result["actions"].append(f"Created raw/{slug}.md")
        result["raw_file"] = f"raw/{slug}.md"
        result["title"] = title
        
        # Download images
        if images:
            print(f"  Downloading {len(images)} images...")
            img_map = download_images(images, assets_dir, slug)
            if img_map:
                # Update image references in the file
                with open(raw_file, "r", encoding="utf-8") as f:
                    updated = f.read()
                for url, local in img_map.items():
                    updated = updated.replace(url, local)
                with open(raw_file, "w", encoding="utf-8") as f:
                    f.write(updated)
                result["actions"].append(f"Downloaded {len(img_map)} images to raw/assets/")
    
    else:
        # Local file
        source_path = os.path.expanduser(source_path)
        if not os.path.isabs(source_path):
            # Try relative to vault first, then cwd
            if os.path.exists(os.path.join(vault_path, source_path)):
                source_path = os.path.join(vault_path, source_path)
            elif os.path.exists(source_path):
                source_path = os.path.abspath(source_path)
            else:
                result["status"] = "error"
                result["error"] = f"File not found: {source_path}"
                return result
        
        # If file is not already in raw/, copy it
        if not source_path.startswith(os.path.join(vault_path, "raw")):
            filename = os.path.basename(source_path)
            dest = os.path.join(raw_dir, filename)
            if not os.path.exists(dest):
                import shutil
                shutil.copy2(source_path, dest)
                result["actions"].append(f"Copied to raw/{filename}")
        
        filename = os.path.basename(source_path)
        result["raw_file"] = f"raw/{filename}"
        result["title"] = os.path.splitext(filename)[0].replace('-', ' ').replace('_', ' ').title()
    
    # Generate ingest instruction for the LLM
    result["llm_instruction"] = f"""
Source ingested to: {result.get('raw_file', source_path)}
Title: {result.get('title', 'Unknown')}

Next steps for LLM:
1. Read the source file completely
2. Create wiki/sources/{slugify(result.get('title', 'unknown'))}.md with summary
3. Identify and update/create relevant entity pages in wiki/entities/
4. Identify and update/create relevant concept pages in wiki/concepts/
5. Update wiki/index.md with new entries
6. Update cross-references in all affected pages
7. Append ingest entry to wiki/log.md
"""
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Ingest a source into the LLM Wiki.")
    parser.add_argument("vault_path", help="Path to the Obsidian vault root")
    parser.add_argument("source", help="Source file path or URL")
    parser.add_argument("--batch", action="store_true", help="Batch mode — less interactive")
    parser.add_argument("--no-discuss", action="store_true", help="Skip discussion of key takeaways")
    args = parser.parse_args()
    
    # Handle directory input
    if os.path.isdir(args.source):
        files = sorted(Path(args.source).glob("*.md"))
        print(f"Batch ingesting {len(files)} markdown files from {args.source}")
        results = []
        for f in files:
            r = ingest_file(args.vault_path, str(f), batch=True)
            results.append(r)
            if r["status"] == "ok":
                print(f"  ✓ {r.get('title', f.name)}")
            else:
                print(f"  ✗ {f.name}: {r.get('error', 'unknown error')}")
        
        print(f"\nIngested {sum(1 for r in results if r['status'] == 'ok')}/{len(results)} files")
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        result = ingest_file(args.vault_path, args.source, batch=args.batch)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
