# Claude Code Adapter

How to use the LLM Wiki KB skill with [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Setup

1. **Schema file**: Copy `references/schema-template.md` to your vault root as `CLAUDE.md`:
   ```bash
   cp <skill-path>/references/schema-template.md ~/my-vault/CLAUDE.md
   ```
   Claude Code automatically reads `CLAUDE.md` as project context.

2. **Environment variable**: Set the vault path:
   ```bash
   export WIKI_VAULT=~/my-vault
   ```
   Or add to your Claude Code project's `.env` file.

3. **MCP tools** (optional): If using qmd as MCP server, add to `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "qmd": {
         "command": "qmd",
         "args": ["serve", "--dir", "wiki/"]
       }
     }
   }
   ```

## Usage in Claude Code

Claude Code can directly read/write files in your vault. The typical workflow:

### Ingest
```
> Add this article to my KB: https://example.com/article
```
Claude reads the skill, runs `wiki_ingest.py`, then performs the wiki compilation (creating/updating pages, index, log).

### Query
```
> What does my research say about transformer efficiency?
```
Claude reads `wiki/index.md`, finds relevant pages, reads them, and synthesizes an answer.

### Lint
```
> Run a health check on my wiki
```
Claude runs `wiki_lint.py` and fixes issues.

## Permissions

Claude Code needs file read/write permissions for your vault directory. If prompted, allow access to the vault path.

## Tips

- Claude Code's `CLAUDE.md` is the natural home for the wiki schema
- Use `/add-dir` to add your vault to the project if it's in a different location
- Claude Code can run Python scripts directly — all `scripts/` tools work natively
- For large wikis, consider setting up qmd MCP for better search
