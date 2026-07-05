# MCP Transport Types Reference

## How to identify the transport type

Read the repo's README and source in this order:

1. **Search for explicit MCP docs in the README** — most repos document this directly ("run `npx` to start the MCP server" → stdio; "start the server then connect Claude" → HTTP/SSE)
2. **Check package.json scripts** — a `"mcp"` or `"start"` script that launches a process → stdio; a script that starts an HTTP server → HTTP or SSE
3. **Search source for transport keywords:**
   ```bash
   grep -r "StdioServerTransport\|stdio\|createServer\|SSEServerTransport\|StreamableHTTPServerTransport" --include="*.ts" --include="*.js" -l .
   ```

## stdio

**When:** The MCP server is a CLI process Claude spawns on demand. This is the most common pattern.

**Signals:** `StdioServerTransport`, `process.stdin`, `npx <pkg> mcp` or similar invocation in README.

**Template:**
```json
{
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "my-mcp-package@latest"],
      "env": {
        "API_KEY": "${MY_API_KEY}"
      }
    }
  }
}
```

Alternative commands (use what the repo documents):
- `"command": "python", "args": ["-m", "my_package.mcp"]`
- `"command": "uvx", "args": ["my-package"]`
- `"command": "node", "args": ["dist/index.js"]`

## HTTP (Streamable HTTP)

**When:** The server is a long-running HTTP process. Claude connects over HTTP.

**Signals:** `StreamableHTTPServerTransport`, Express/Fastify server on a fixed port, README says "start the server first".

**Template:**
```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "http://localhost:3000/mcp",
      "headers": {
        "Authorization": "Bearer ${MY_API_KEY}"
      }
    }
  }
}
```

## SSE (Server-Sent Events)

**When:** Older HTTP transport using event streams. Less common in newer repos; `SSEServerTransport` in source.

**Template:**
```json
{
  "mcpServers": {
    "my-server": {
      "type": "sse",
      "url": "http://localhost:3000/sse"
    }
  }
}
```

## Python-specific commands

| Runtime | Command style |
|---------|--------------|
| pip-installed module | `python -m package_name.mcp` |
| uv-managed | `uvx package-name` |
| Direct script | `python path/to/server.py` |

Always prefer `uvx` or `npx` over global installs when the repo supports it — they handle versioning automatically.
