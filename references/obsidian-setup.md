# Obsidian Setup Guide

Recommended Obsidian configuration for use with the LLM Wiki Knowledge Base.

## Opening the Vault

1. Open Obsidian
2. Click "Open folder as vault"
3. Select your vault root directory (the one containing `raw/`, `wiki/`, `SCHEMA.md`)

## Essential Settings

### Files and Links
- **New link format**: Shortest path when possible
- **Use [[Wikilinks]]**: ON (this is how the LLM creates internal links)
- **Default location for new attachments**: `raw/assets/` (keeps images organized)

### Editor
- **Show frontmatter**: ON (see page metadata)
- **Readable line length**: ON (better reading experience)

## Recommended Plugins

### Core Plugins (built-in, just enable them)
- **Graph View** — Visualize wiki structure, find clusters and orphans
- **Backlinks** — See which pages link to the current page
- **Outgoing links** — See what the current page links to
- **Search** — Built-in search (good enough for small wikis)
- **Tags** — Browse pages by tag
- **Page preview** — Hover over wikilinks to preview content

### Community Plugins

| Plugin | Purpose | Priority |
|--------|---------|----------|
| **Obsidian Web Clipper** | Save web articles as markdown to `raw/` | Essential |
| **Dataview** | Dynamic tables/lists from page frontmatter | Highly recommended |
| **Marp Slides** | Render Marp-format slide decks | Recommended |
| **Kanban** | Visual board for tracking research tasks | Optional |
| **Calendar** | Navigate by date (useful with log.md) | Optional |
| **Templater** | Custom templates for new pages | Optional |

### Installing Community Plugins
1. Settings → Community Plugins → Turn off Safe Mode
2. Browse → Search for plugin name → Install → Enable

## Obsidian Web Clipper Setup

1. Install the [Obsidian Web Clipper](https://obsidian.md/clipper) browser extension
2. Configure:
   - **Vault**: Select your KB vault
   - **Folder**: `raw/` (save clipped articles directly to raw sources)
   - **Template**: Use default or customize

### Image Download Hotkey

After clipping an article, download its images locally:

1. Settings → Hotkeys
2. Search for "Download all remote images"
3. Bind to `Ctrl+Shift+D` (or your preference)
4. After clipping, open the article in Obsidian and press the hotkey
5. Images are saved to `raw/assets/` and references updated automatically

## Dataview Queries

With Dataview installed and YAML frontmatter on wiki pages, you can create dynamic views:

### All entities by type
```dataview
TABLE type, sources, updated
FROM "wiki/entities"
SORT updated DESC
```

### Recently updated pages
```dataview
TABLE type, tags
FROM "wiki"
WHERE updated
SORT updated DESC
LIMIT 20
```

### Sources by date
```dataview
TABLE author, published, tags
FROM "wiki/sources"
SORT published DESC
```

### Pages with specific tag
```dataview
LIST
FROM "wiki"
WHERE contains(tags, "machine-learning")
```

## Graph View Tips

- **Color groups**: Set colors by folder (entities=blue, concepts=green, sources=gray)
- **Filters**: Hide `raw/` from the graph to focus on wiki structure
- **Depth**: Set link depth to 2 for local exploration
- **Orphan nodes**: Bright red flags — pages that need linking

## Workflow Tips

- Keep Obsidian open alongside your LLM agent terminal
- Use **split view**: index.md on left, current research on right
- After each ingest, check Graph View for new connections
- Use **starred pages** for your current research focus
- The LLM edits files → Obsidian hot-reloads → you see changes instantly
