# OpenCode / OpenClaw Adapter

How to use the LLM Wiki KB skill with OpenAI Codex, OpenCode, or similar agent platforms.

## Setup

1. **Schema file**: Copy `references/schema-template.md` to your vault root as `AGENTS.md`:
   ```bash
   cp <skill-path>/references/schema-template.md ~/my-vault/AGENTS.md
   ```
   OpenCode/Codex reads `AGENTS.md` as project instructions.

2. **Environment variable**:
   ```bash
   export WIKI_VAULT=~/my-vault
   ```

3. **Tool configuration**: Register the wiki scripts as available tools in your agent config:
   ```yaml
   tools:
     - name: wiki_init
       command: python <skill-path>/scripts/wiki_init.py $WIKI_VAULT
     - name: wiki_ingest
       command: python <skill-path>/scripts/wiki_ingest.py $WIKI_VAULT
     - name: wiki_query
       command: python <skill-path>/scripts/wiki_query.py $WIKI_VAULT
     - name: wiki_search
       command: python <skill-path>/scripts/wiki_search.py $WIKI_VAULT
     - name: wiki_lint
       command: python <skill-path>/scripts/wiki_lint.py $WIKI_VAULT
   ```

## Usage

The workflows are identical to other platforms. The agent reads `AGENTS.md` for conventions
and uses the scripts for mechanical operations. The core ingest/query/lint loop works the same.

### Key Differences from Claude Code
- Schema file is named `AGENTS.md` instead of `CLAUDE.md`
- Tool registration may need explicit configuration depending on the agent platform
- Some agents may need explicit permission grants for file system access

## Codex-Specific Notes

If using OpenAI Codex (cloud sandbox):
- The vault must be accessible within the sandbox filesystem
- Codex can run Python scripts directly via `bash` tool
- For web ingest, ensure the sandbox has network access
- qmd may need to be installed within the sandbox environment

## Pi / OpenCode Notes

If using the Pi agent or OpenCode:
- Both support `AGENTS.md` as the project instruction file
- File system access is typically available by default
- Python scripts run natively
- qmd can be installed via `go install` if Go is available
