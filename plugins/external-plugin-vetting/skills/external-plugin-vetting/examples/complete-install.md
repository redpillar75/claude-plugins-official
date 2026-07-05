# Example: Complete Plugin Install (ElevenLabs)

This is a worked example of the full vetting and install process for a real plugin.

## Input

User says: `https://github.com/elevenlabs/elevenlabs-mcp.git install`

## Phase 1 — Vetting

```bash
curl -s "https://api.github.com/repos/elevenlabs/elevenlabs-mcp" | jq '{
  license: .license.spdx_id,
  pushed_at: .pushed_at,
  stars: .stargazers_count,
  archived: .archived
}'
# → { "license": "MIT", "pushed_at": "2025-06-01T...", "stars": 847, "archived": false }
```

Result: MIT license, active, 847 stars. No hard stops.

README scan: Documents `npx @elevenlabs/mcp` as the MCP command. Transport: stdio.

## Phase 2 — Clone as Submodule

```bash
git submodule add https://github.com/elevenlabs/elevenlabs-mcp.git external_plugins/elevenlabs-mcp
cd external_plugins/elevenlabs-mcp
```

## Phase 3 — Install Dependencies

```bash
npm install
# → added 42 packages in 3.2s
```

## Phase 4 — Author Plugin Metadata

**`external_plugins/elevenlabs-mcp/.mcp.json`:**
```json
{
  "mcpServers": {
    "elevenlabs": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@elevenlabs/mcp@latest"],
      "env": {
        "ELEVENLABS_API_KEY": "${ELEVENLABS_API_KEY}"
      }
    }
  }
}
```

**`external_plugins/elevenlabs-mcp/.claude-plugin/plugin.json`:**
```json
{
  "name": "elevenlabs-mcp",
  "description": "Text-to-speech and voice generation via ElevenLabs — generate audio, clone voices, and manage voice library from Claude.",
  "version": "1.2.0",
  "author": { "name": "ElevenLabs", "url": "https://elevenlabs.io" },
  "homepage": "https://github.com/elevenlabs/elevenlabs-mcp",
  "license": "MIT",
  "keywords": ["elevenlabs", "tts", "text-to-speech", "voice", "audio"]
}
```

## Phase 5 — Register in Marketplace

Add to `.claude-plugin/marketplace.json` plugins array:
```json
{
  "name": "elevenlabs-mcp",
  "description": "Text-to-speech and voice generation via ElevenLabs — generate audio, clone voices, and manage voice library from Claude.",
  "version": "1.2.0",
  "author": {
    "name": "ElevenLabs",
    "email": "support@anthropic.com"
  },
  "source": "./external_plugins/elevenlabs-mcp",
  "category": "ai",
  "strict": false
}
```

## Phase 6 — Commit and Push

```bash
git add external_plugins/elevenlabs-mcp
git add external_plugins/elevenlabs-mcp/.mcp.json
git add external_plugins/elevenlabs-mcp/.claude-plugin/plugin.json
git add .gitmodules
git add .claude-plugin/marketplace.json
git commit -m "Install elevenlabs-mcp as external plugin

Source: https://github.com/elevenlabs/elevenlabs-mcp.git
License: MIT
MCP transport: stdio"
git push -u origin claude/install-davinci-magihuman-yPJbu
```

## Common Mistakes to Avoid

- Putting `.claude-plugin/plugin.json` in the repo root instead of inside `external_plugins/elevenlabs-mcp/`
- Using `"source": "https://github.com/..."` in marketplace.json instead of the local path `"./external_plugins/elevenlabs-mcp"`
- Using `git add .` and accidentally staging unrelated changes
- Forgetting to add `.gitmodules` — submodule registration won't persist
