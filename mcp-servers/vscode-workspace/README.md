# VSCode Workspace MCP Server

Provides workspace root and git repository information to Claude Code skills, independent of the terminal's current working directory.

## Features

- **`get_workspace_root`**: Returns the VSCode workspace root, git repository root, and fallback path
- **`check_git_repository`**: Checks if a path is inside a git repository

## Installation

### 1. Install dependencies

```bash
cd B:\ai\ai-nix\mcp-servers\vscode-workspace
npm install
```

### 2. Configure in Claude Code

Add to `~/.claude/config.json`:

```json
{
  "mcpServers": {
    "vscode-workspace": {
      "command": "node",
      "args": [
        "B:\\ai\\ai-nix\\mcp-servers\\vscode-workspace\\index.js"
      ]
    }
  }
}
```

Or for macOS/Linux:

```json
{
  "mcpServers": {
    "vscode-workspace": {
      "command": "node",
      "args": [
        "/path/to/ai-nix/mcp-servers/vscode-workspace/index.js"
      ]
    }
  }
}
```

### 3. Restart Claude Code

After updating config.json, restart Claude Code for the MCP server to be loaded.

## Usage

### From Python init_instance.py scripts

```python
import subprocess
import json
import sys

def get_workspace_root_from_mcp():
    """Try to get workspace root from MCP server."""
    try:
        # Call the MCP tool via Claude Code harness
        # This is a placeholder - actual implementation depends on
        # how skills invoke MCP tools
        result = subprocess.run(
            ['claude', 'mcp', 'call', 'vscode-workspace', 'get_workspace_root'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return Path(data['workspaceRoot'])
    except:
        pass
    return None

def find_workspace(start: Path) -> Path:
    """Return the workspace root using multiple strategies."""
    # 1. Try MCP server (if available)
    mcp_workspace = get_workspace_root_from_mcp()
    if mcp_workspace:
        return mcp_workspace
    
    # 2. Try git from current location
    start = start.expanduser().resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    
    # 3. Fallback to OS-specific data directory
    return get_fallback_path()
```

### From SKILL.md via Bash

Skills can use the MCP tool via Claude Code's tool interface:

```bash
# Claude Code will translate this to an MCP call
workspace_info=$(claude-mcp-tool vscode-workspace get_workspace_root)
workspace_root=$(echo "$workspace_info" | jq -r '.workspaceRoot')

python <skill>/scripts/init_instance.py --workspace "$workspace_root" ...
```

## Response Format

### get_workspace_root

```json
{
  "workspaceRoot": "B:\\ai\\ai-nix",
  "resolvedFrom": "git-command",
  "isGitRepository": true,
  "gitRoot": "B:\\ai\\ai-nix"
}
```

Or with fallback:

```json
{
  "workspaceRoot": "C:\\.data",
  "resolvedFrom": "fallback",
  "isGitRepository": false,
  "gitRoot": null,
  "warning": "No git repository found. Using fallback: C:\\.data"
}
```

### check_git_repository

```json
{
  "path": "B:\\ai\\ai-nix\\dac",
  "isGitRepository": true,
  "gitRoot": "B:\\ai\\ai-nix",
  "exists": true
}
```

## Fallback Paths

When no git repository is found:

| OS | Fallback Path |
|---|---|
| Windows | `C:\.data` |
| macOS | `~/Library/Application Support/claude-skills` |
| Linux | `~/.local/share/claude-skills` |

## Testing

Test the MCP server directly:

```bash
cd B:\ai\ai-nix\mcp-servers\vscode-workspace
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | node index.js
```

Or test workspace resolution:

```bash
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_workspace_root","arguments":{}}}' | node index.js
```

## Troubleshooting

**Server not loading:**
- Check `~/.claude/config.json` syntax with `jq . ~/.claude/config.json`
- Verify node version: `node --version` (requires >=18.0.0)
- Check Claude Code logs for MCP server errors

**Wrong workspace returned:**
- Pass explicit `hint` parameter with expected workspace path
- Check that the path contains a `.git` directory
- Verify git command works: `git rev-parse --show-toplevel`

**Dependencies not found:**
- Run `npm install` in the mcp-servers/vscode-workspace directory
- Check that `@modelcontextprotocol/sdk` is installed
