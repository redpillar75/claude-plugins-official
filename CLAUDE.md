# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is the **Claude Code Plugins Directory** — a marketplace of plugins (commands, agents, skills, hooks, MCP servers, LSP servers) that Claude Code can install. There is no build/runtime application code; the repo's content *is* the product. Contributions are Anthropic-internal only — external PRs are auto-closed by `.github/workflows/close-external-prs.yml` unless the author has write access.

## Repository structure

- **`.claude-plugin/marketplace.json`** — the single manifest listing every plugin in the marketplace. Each entry has `name`, `description`, `version`, `author`, `source` (relative path to the plugin dir), `category`, and `strict`. LSP plugins additionally declare an `lspServers` block (command, args, `extensionToLanguage` map).
- **`/plugins`** — internal plugins developed/maintained by Anthropic.
- **`/external_plugins`** — thin wrappers around third-party MCP servers (Asana, GitHub, Stripe, Slack, Supabase, etc). These are almost always just `.claude-plugin/plugin.json` + `.mcp.json`, nothing else.

Every plugin directory follows this shape (all subdirs optional except the manifest):
```
plugin-name/
├── .claude-plugin/plugin.json   # required: name, description, author
├── .mcp.json                    # MCP server config (stdio/http/sse)
├── commands/*.md                # slash commands (frontmatter: description)
├── agents/*.md                  # subagent definitions (frontmatter: name, description)
├── skills/*/SKILL.md            # skills (frontmatter: description or when_to_use)
├── hooks/hooks.json              # lifecycle hooks, scripts referenced via ${CLAUDE_PLUGIN_ROOT}
└── README.md
```
`plugins/example-plugin` is the reference implementation demonstrating all of these; `plugins/plugin-dev` contains in-depth skills/references on authoring each piece (agent-development, command-development, hook-development, mcp-integration, plugin-settings, plugin-structure).

**Adding or changing a plugin requires updating both** the plugin's own directory *and* its entry in `.claude-plugin/marketplace.json` (source path, category, version) — the manifest is not auto-generated from the filesystem.

## Commands

There is no application build/lint/test suite. The one piece of automated validation is frontmatter linting for agent/skill/command markdown files, run in CI via `.github/workflows/validate-frontmatter.yml` on PRs that touch `**/agents/*.md`, `**/skills/*/SKILL.md`, or `**/commands/*.md`:

```bash
cd .github/scripts && bun install yaml
bun .github/scripts/validate-frontmatter.ts <path-or-file...>   # e.g. a whole plugin dir, or specific .md files
```

It checks that frontmatter YAML parses and that required fields are present: `name`+`description` for agents, `description` (or `when_to_use`) for skills, `description` for commands. Run it against changed files before pushing plugin changes.
