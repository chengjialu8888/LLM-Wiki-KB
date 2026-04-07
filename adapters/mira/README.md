# Mira Adapter

How to use the LLM Wiki KB skill with Mira (ByteDance's AI assistant).

## Setup

Mira operates within a sandboxed environment. The vault lives in the sandbox workspace.

### Initialization
```
帮我初始化一个知识库，主题是 [你的研究领域]
```

Mira will run `wiki_init.py` in the sandbox workspace, creating:
```
workspace/
├── SCHEMA.md
├── raw/
├── wiki/
└── output/
```

### Persistent Storage
For knowledge bases that persist across sessions, use the `userdata/` directory:
```bash
python scripts/wiki_init.py /mnt/mira_sandbox/userdata/<user_id>/my-kb --domain "AI Research"
```

## Usage in Mira

### Ingest
```
把这篇文章加入我的知识库：https://example.com/article
```
Mira fetches the article, converts to markdown, places in `raw/`, then compiles into the wiki.

### Query
```
根据我的知识库，Transformer 和 Mamba 的主要区别是什么？
```
Mira searches the wiki, reads relevant pages, and synthesizes an answer.

### Output to Feishu
Mira can export wiki content to Feishu docs for sharing:
```
把我知识库中关于 scaling laws 的综合分析导出到飞书文档
```
Uses `upload_to_feishu_tool` to create a formatted Feishu doc.

### Lint
```
检查一下我的知识库健康状况
```

## Key Differences

| Feature | Claude Code / OpenCode | Mira |
|---------|----------------------|------|
| Vault location | Local filesystem | Sandbox workspace or userdata |
| Schema file | CLAUDE.md / AGENTS.md | SCHEMA.md |
| Obsidian viewing | Direct (local) | Download files or export to Feishu |
| qmd search | Install locally | May not be available — grep fallback |
| Output sharing | View in Obsidian | Export to Feishu or upload files |
| Persistence | Always (local files) | userdata/ persists; workspace/ per-session |

## Limitations in Mira

- **No direct Obsidian integration**: Mira runs in a sandbox. To view in Obsidian, download the vault files to your local machine, or use Feishu export.
- **Network restrictions**: Sandbox may have limited network access for web ingest. Use Mira's built-in `web_builtin_fetch` tool for URL fetching.
- **qmd availability**: qmd may not be installed in the sandbox. The skill falls back to grep-based search automatically.

## Recommended Workflow

1. **Build in Mira**: Use Mira for ingest, query, and lint operations
2. **Export to Feishu**: Share analyses and reports via Feishu docs
3. **Optional local sync**: Download the vault to local for Obsidian viewing
4. **Scheduled tasks**: Use Mira's scheduled tasks for automated lint checks or daily ingests

## Integration with Mira Tools

The skill can leverage Mira's built-in tools:
- `web_builtin_fetch` — Fetch web content for ingest
- `web_search` — Search the web during lint (fill data gaps)
- `upload_to_feishu_tool` — Export wiki content to Feishu
- `generate_pictures` — Generate illustrations for wiki pages
- `sandbox` — Execute all Python scripts
