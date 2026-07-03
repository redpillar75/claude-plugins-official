# Claude Plugins Official Directory

This repository maintains the official marketplace of high-quality plugins for Claude Code.

## Directory Structure

```
.
├── /plugins/              # ~30 internal plugins developed by Anthropic
├── /external_plugins/     # Third-party plugins from partners and community
├── /.claude-plugin/       # Plugin marketplace manifest (marketplace.json)
├── /.github/              # CI/CD workflows and build scripts
└── README.md              # User-facing documentation
```

## Understanding Plugin Anatomy

Each plugin (internal or external) follows this structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json        # Plugin metadata: name, version, description, MCP servers, skills, agents, commands
├── .mcp.json              # Optional: MCP server configuration (stdio, SSE, or subprocess)
├── commands/              # Optional: Slash commands (e.g., /review, /simplify)
├── agents/                # Optional: Custom agent definitions
├── skills/                # Optional: Claude Code skills (extending /slash commands)
├── README.md              # Plugin documentation (for developers and users)
└── (source code)          # TypeScript, Python, or language-specific implementation
```

**Key files:**
- `plugin.json` – Required. Defines plugin identity, MCP servers, skills, agents, commands.
- `.mcp.json` – Optional. Configures any MCP servers the plugin provides.
- `skills/` – Slash commands the plugin adds to Claude Code (e.g., `/dataviz`, `/code-review`).
- `commands/` – Simpler text-based commands (legacy; prefer skills for new plugins).

## Common Tasks

### Add a new internal plugin

1. Copy `/plugins/example-plugin/` to `/plugins/your-plugin-name/`
2. Edit `.claude-plugin/plugin.json`:
   - Update `name`, `version`, `description`, `owner`
   - Add MCP servers (if applicable) under `mcpServers`
   - Add skills under `skills`
3. Implement your plugin code
4. Update `README.md` with usage and setup instructions
5. Test locally with `/plugin install ./plugins/your-plugin-name`

### Test a plugin locally

```bash
claude /plugin install ./plugins/my-plugin-name
```

Then use the plugin's commands/skills in Claude Code. To uninstall:

```bash
claude /plugin remove my-plugin-name
```

### Validate plugin.json

The plugin manifest must follow the schema. Use your IDE's JSON schema support or check against `.claude-plugin/marketplace.json` for examples.

### Update the marketplace manifest

The `.claude-plugin/marketplace.json` is auto-generated from all plugins' `plugin.json` files during CI/CD. Do not edit it directly. It's regenerated on every commit to `main`.

## Contributing

### Internal Plugin Guidelines

- Plugins should solve real Claude Code workflows (code review, testing, formatting, etc.)
- Keep plugins focused and single-purpose
- Document your plugin thoroughly in `README.md`
- Test locally before pushing
- Ensure `plugin.json` follows the schema

### External Plugin Submission

Third-party partners can submit plugins for inclusion. See [plugin directory submission form](https://clau.de/plugin-directory-submission) for details. External plugins must meet security and quality standards.

### Naming Conventions

- Internal plugins use hyphens: `code-review`, `frontend-design`
- Plugin directories match the `name` field in `plugin.json`
- Skills should be concise and memorable: `/review`, `/simplify`, `/dataviz`

## Getting Help

- **Plugin Development Docs:** https://code.claude.com/docs/en/plugins
- **Plugin Examples:** See `/plugins/example-plugin` and other internal plugins
- **MCP Documentation:** https://modelcontextprotocol.io/docs
- **Issues/Feedback:** Use GitHub Issues in this repository
