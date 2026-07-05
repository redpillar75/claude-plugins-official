# Claude Plugins Official

This is the official Claude Code plugin marketplace. Each plugin extends Claude Code with new skills, agents, commands, hooks, and MCP server configurations.

## Repo Structure

```
plugins/                   # First-party plugins
  <plugin-name>/
    .claude-plugin/
      plugin.json          # Plugin metadata (name, description, author)
    agents/                # Subagent definitions (.md files)
    skills/
      <skill-name>/
        SKILL.md           # Skill definition
    commands/              # Slash command definitions (.md files)
    scripts/               # Helper scripts referenced by hooks or commands
    hooks.json             # Hook definitions for this plugin
    mcp.json               # MCP server configuration for this plugin

external_plugins/          # Third-party plugins maintained here
  <plugin-name>/           # Same structure as plugins/
```

## Plugin Authoring

### plugin.json

```json
{
  "name": "my-plugin",
  "description": "One sentence describing what this plugin does.",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  }
}
```

### Agent Files (`agents/<name>.md`)

Required frontmatter fields:

```yaml
---
name: agent-name
description: |
  One or two sentence description of when to use this agent, written for
  the model that decides whether to invoke it.

  <example>
  Context: brief setup.
  user: "exact user message that should trigger this agent"
  assistant: "I'll use the agent-name agent to handle this."
  <commentary>
  Why this example triggers the agent.
  </commentary>
  </example>

  <example>
  Context: second scenario.
  user: "another trigger message"
  assistant: "Let me launch agent-name to do this."
  <commentary>
  Why.
  </commentary>
  </example>
model: inherit          # or: opus, sonnet, haiku
color: blue             # see valid colors below
---
```

**Valid colors:** `blue`, `cyan`, `green`, `yellow`, `magenta`, `red`

**Rules:**
- The `description` field must be a YAML block scalar (`|`), not a single-line string with `\n` escape sequences.
- At least two `<example>` blocks are required in the description. Without them, the agent will rarely be invoked.
- Examples must use the exact `<example>` / `<commentary>` XML tags — these are parsed by Claude Code.
- The `model` field should be `inherit` unless the agent has specific model requirements (e.g., `opus` for complex multi-step reasoning).
- Agent body (below the frontmatter `---`) is the system prompt. Write it as a direct instruction to the agent, not as documentation.

### Skill Files (`skills/<skill-name>/SKILL.md`)

Required frontmatter:

```yaml
---
name: skill-name
description: One sentence. Used by the model to decide when to load this skill.
---
```

**Rules:**
- The body should include a step-by-step process, an output format, at least one concrete example, and explicit do-nots.
- Keep the SKILL.md body under ~2000 words. For long reference material, add a `references/` subdirectory.
- For scripts the skill invokes, put them in a sibling `scripts/` directory.

### Command Files (`commands/<name>.md`)

Required frontmatter:

```yaml
---
description: "Short description shown in /help"
argument-hint: "REQUIRED_ARG [--optional-flag VALUE]"
allowed-tools: ["Bash", "Read"]  # or: ["Bash(${CLAUDE_PLUGIN_ROOT}/scripts/foo.sh:*)"]
---
```

Use `${CLAUDE_PLUGIN_ROOT}` for portable paths — it expands to the plugin's root directory at runtime.

### hooks.json

Hooks file must wrap event keys in a `hooks` object:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/my-hook.sh" }
        ]
      }
    ]
  }
}
```

Valid hook events: `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, `SubagentStop`.

## Validation

Use the `plugin-validator` agent (from the `plugin-dev` plugin) to validate any plugin before committing:

```
/plugin-dev:validate-plugin
```

It checks: frontmatter completeness, valid agent colors, example blocks in agent descriptions, required plugin.json fields, and hook/MCP JSON structure.

## Common Mistakes

- **`color: pink`** — not a valid color. Use `magenta`.
- **`\n` in description** — agent descriptions must use YAML block scalar `|`. A single-line string with literal `\n` will not render as newlines and will break example parsing.
- **Missing `<example>` blocks** — agents without examples in their description are almost never invoked. Always add at least two.
- **Hardcoded project paths in agents** — agents ship as part of a generic marketplace. Never reference specific files (`constants/errorIds.ts`), services (Sentry, Statsig), or function names that belong to a specific project. Use `CLAUDE.md`-relative instructions instead.
- **hooks.json without `{"hooks": {...}}` wrapper** — the plugin system requires the wrapper. Hooks at the top level will be ignored.
- **`${CLAUDE_PLUGIN_ROOT}` in mcp.json** — this variable is supported in hooks but may not expand in all MCP config contexts. Test before shipping.
