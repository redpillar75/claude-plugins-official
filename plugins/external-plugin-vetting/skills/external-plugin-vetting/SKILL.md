---
name: external-plugin-vetting
description: Safely evaluate, install, and register a third-party GitHub repo as a Claude Code plugin in this marketplace. Covers pre-install vetting, submodule setup, MCP config authoring, plugin.json authoring, and marketplace registration. Use whenever the user provides a GitHub URL with "install" intent.
---

# External Plugin Vetting

Installs a third-party GitHub repo as an external Claude Code plugin in `external_plugins/`. Follows a strict five-phase process: vet, clone, configure, register, commit.

## Phase 1 — Pre-Install Vetting

Before touching the filesystem, evaluate the repo. A plugin that fails any **hard stop** must not be installed.

### Hard Stops (reject immediately)

- No recognizable license file (LICENSE, LICENSE.md, COPYING) — unlicensed code cannot be redistributed
- Repo archived or has zero commits in the last 24 months and zero stars — likely abandoned
- `package.json` or `pyproject.toml` contains a `postinstall` / `prepare` script that executes arbitrary shell commands and the repo has < 100 stars — supply chain risk
- No MCP server surface found: no `mcp`, `stdio`, `http`, or `sse` references in any of `package.json`, `pyproject.toml`, `README.md`, `Makefile` — the plugin will provide nothing to Claude

### Warnings (surface to user, proceed only with acknowledgement)

- Last commit > 12 months ago: flag as potentially stale
- No tests directory and > 500 lines of source: flag as unverified quality
- License is GPL or AGPL: copyleft — may conflict with proprietary use
- README has no usage instructions: configuration will be guesswork

### Vetting checklist to run

```bash
# 1. Check license
curl -s https://api.github.com/repos/<owner>/<repo> | jq '.license.spdx_id, .pushed_at, .stargazers_count, .archived'

# 2. Scan for MCP surface (do this after cloning)
grep -r "mcp\|stdio\|ModelContextProtocol" --include="*.json" --include="*.md" --include="*.py" --include="*.ts" -l .

# 3. Check for dangerous install scripts
cat package.json | jq '.scripts.postinstall, .scripts.prepare' 2>/dev/null
```

Record findings. If all checks pass, proceed.

---

## Phase 2 — Clone as Submodule

The install location is always `external_plugins/<name>/` where `<name>` is the repo name lowercased with hyphens. Never use the full org/repo path as the directory name.

```bash
# From repo root
git submodule add <clone-url> external_plugins/<name>
cd external_plugins/<name>
```

If the repo already exists as a regular directory (not a submodule), remove it from git index first:
```bash
git rm -r --cached external_plugins/<name>
rm -rf external_plugins/<name>
git submodule add <clone-url> external_plugins/<name>
```

---

## Phase 3 — Install Dependencies

Detect the runtime and install. Do this inside the submodule directory.

| Indicator | Command |
|-----------|---------|
| `package.json` present | `npm install` |
| `pyproject.toml` or `requirements.txt` | `pip install -e .` or `pip install -r requirements.txt` |
| Both | npm first, then pip |
| Neither | No install needed; note it |

If `pip install` fails with a packaging conflict from a Debian-managed package:
```bash
pip install -r requirements.txt --ignore-installed packaging
```

---

## Phase 4 — Author Plugin Metadata

Create two files **inside** `external_plugins/<name>/`. These files live in the submodule directory itself, not in the repo root.

### `.mcp.json`

Determine the server transport type by reading the repo's README and source:

- **stdio** (most common — a CLI tool that Claude spawns):
```json
{
  "mcpServers": {
    "<name>": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "<npm-package>@latest", "mcp"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

- **HTTP** (a running server Claude connects to over HTTP):
```json
{
  "mcpServers": {
    "<name>": {
      "type": "http",
      "url": "http://localhost:PORT/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

- **SSE** (Server-Sent Events stream):
```json
{
  "mcpServers": {
    "<name>": {
      "type": "sse",
      "url": "http://localhost:PORT/sse",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

**Env var conventions:**
- Always use `${VAR_NAME}` syntax for secrets — never hardcode values
- Name vars `<SERVICE>_API_KEY`, `<SERVICE>_API_SECRET`, `<SERVICE>_HOST` etc.
- For local services (Ollama, self-hosted), default the URL to localhost and document the port

**Validation: before writing `.mcp.json`, confirm:**
- [ ] Transport type matches what the repo actually exposes
- [ ] Package name / command exists (search npmjs.com or PyPI if unsure)
- [ ] All required env vars are listed; no optional-but-undocumented ones are silently omitted
- [ ] No secrets or real API key values appear anywhere in the file

### `.claude-plugin/plugin.json`

```json
{
  "name": "<name>",
  "description": "<one sentence: what it does for Claude>",
  "version": "<version from package.json or pyproject.toml, else 1.0.0>",
  "author": { "name": "<org or author name>", "url": "<repo homepage>" },
  "homepage": "<repo URL>",
  "license": "<SPDX identifier, e.g. MIT>",
  "keywords": ["<3-5 relevant terms>"]
}
```

Rules:
- `description` must describe what Claude can *do* with this plugin, not what the underlying tool is
- `version` must match the upstream release, not be invented
- `license` must match the actual license file in the repo
- Do not add fields that don't appear in this schema

---

## Phase 5 — Register in Marketplace

Open `.claude-plugin/marketplace.json` at the repo root. Add an entry to the `"plugins"` array. Find the last entry in the array and append after it:

```json
{
  "name": "<name>",
  "description": "<same as plugin.json description>",
  "version": "<same version>",
  "author": {
    "name": "<org or author name>",
    "email": "support@anthropic.com"
  },
  "source": "./external_plugins/<name>",
  "category": "<choose: development | productivity | data | communication | infrastructure | ai>",
  "strict": false
}
```

`"source"` must point to the submodule directory, not the GitHub URL.

---

## Phase 6 — Commit and Push

Stage all new and modified files:

```bash
git add external_plugins/<name>
git add external_plugins/<name>/.mcp.json
git add external_plugins/<name>/.claude-plugin/plugin.json
git add .gitmodules
git add .claude-plugin/marketplace.json
```

Commit message format:
```
Install <name> as external plugin

Source: <clone-url>
License: <SPDX>
MCP transport: <stdio|http|sse>
```

Then push to the active branch (`claude/install-davinci-magihuman-yPJbu`).

---

## Final Checklist

Before reporting success to the user, verify every item:

- [ ] License checked — not unlicensed, not disqualifying copyleft
- [ ] MCP surface confirmed — plugin actually exposes tools to Claude
- [ ] Dependencies installed without error
- [ ] `.mcp.json` uses correct transport type and `${VAR}` env syntax
- [ ] `.claude-plugin/plugin.json` inside the submodule directory (not the repo root)
- [ ] `marketplace.json` entry has `"source"` pointing to `./external_plugins/<name>`
- [ ] `git submodule status` shows the submodule at a clean commit hash
- [ ] All files staged and committed
- [ ] Pushed to active branch

---

## Do Not

- Do not install a repo that has no MCP server surface — it will provide nothing to Claude
- Do not install an unlicensed repo
- Do not hardcode any API key or secret value in `.mcp.json`
- Do not put `.claude-plugin/plugin.json` in the repo root — it belongs inside `external_plugins/<name>/`
- Do not use `npm install -g` as the installation method for the plugin metadata — install deps locally or confirm the global install is intentional and document it
- Do not invent a version number — read it from the upstream source
- Do not skip the `git submodule add` step and just `git add` the directory — that creates an embedded repo, not a submodule
- Do not push to `main` — always push to the active feature branch
