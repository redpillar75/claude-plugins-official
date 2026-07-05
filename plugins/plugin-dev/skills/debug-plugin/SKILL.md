---
name: debug-plugin
description: Diagnose why a Claude Code plugin component isn't working — agent not triggering, hook not firing, MCP server failing to connect, skill not loading, or command not appearing. Work through each symptom's diagnostic checklist in order.
---

Use this skill when a plugin component is installed but not behaving: an agent that never gets invoked, a hook that silently does nothing, an MCP server that fails to connect, a skill that never loads, or a command that doesn't appear in `/help`.

## How to Use This Skill

Identify your symptom from the sections below, then work through the checklist for that symptom top-to-bottom. Stop as soon as you find the problem — most failures have one root cause.

---

## Symptom: Agent is never invoked

Claude always handles the task itself instead of delegating to the agent.

**Step 1: Check the description field format**

Read the agent's `.md` file. The `description` field must be a YAML block scalar:

```yaml
description: |
  First line of description.

  <example>
  ...
  </example>
```

If the description looks like this instead, it is broken — the `\n` are literal backslash-n characters, not newlines, and the `<example>` blocks will never be parsed:

```yaml
description: "First line.\n\n<example>\n..."
```

Fix: rewrite the `description` field using `|` and real indented newlines.

**Step 2: Verify at least two `<example>` blocks exist**

The agent description must contain at minimum two blocks of this exact structure:

```
<example>
Context: brief setup.
user: "exact message that triggers this agent"
assistant: "I'll use the agent-name agent to handle this."
<commentary>
Why this triggers the agent.
</commentary>
</example>
```

Agents without two `<example>` blocks are almost never invoked. The model uses these as few-shot examples to learn when to delegate.

**Step 3: Check the trigger phrases in your examples**

Read the `user:` lines in your examples. Ask: does the user message you're actually typing sound like those? If the examples say `"validate my plugin"` but you're typing `"check this"`, the agent won't trigger. Add more examples that match your actual usage patterns.

**Step 4: Verify the frontmatter fields**

Required fields: `name`, `description`, `model`, `color`. Missing any of these will cause the agent to fail silently.

Valid `model` values: `inherit`, `sonnet`, `opus`, `haiku`.
Valid `color` values: `blue`, `cyan`, `green`, `yellow`, `magenta`, `red`.

Run the plugin-validator agent to catch these automatically:
```
/plugin-dev:validate-plugin
```

**Step 5: Confirm the plugin is enabled**

Check `~/.claude/settings.json` for an `enabledPlugins` entry matching this plugin. If the plugin is not listed, install it.

---

## Symptom: Hook is not firing

A `PreToolUse`, `PostToolUse`, `Stop`, or other hook does nothing when the event should trigger it.

**Step 1: Verify the hooks.json wrapper**

Open the plugin's `hooks.json`. The structure must be:

```json
{
  "hooks": {
    "PreToolUse": [...]
  }
}
```

If the event keys are at the top level (no `"hooks"` wrapper), the plugin system ignores the entire file:

```json
{
  "PreToolUse": [...]   ← WRONG — no wrapper
}
```

**Step 2: Check the event name spelling**

Valid event names (case-sensitive): `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, `SubagentStop`.

Any other spelling (e.g., `pre-tool-use`, `pretooluse`, `BeforeToolUse`) will silently not match.

**Step 3: Verify the script path**

If the hook runs a command, the `command` field must use `${CLAUDE_PLUGIN_ROOT}` to resolve correctly:

```json
{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/my-hook.sh" }
```

A hardcoded absolute path will work on your machine and break everywhere else. A relative path won't work at all.

**Step 4: Test the script directly**

Run the hook script manually from the terminal to confirm it executes without errors:

```bash
CLAUDE_PLUGIN_ROOT=/path/to/plugin bash /path/to/plugin/scripts/my-hook.sh
```

If it fails here, fix the script before debugging the hook wiring.

**Step 5: Check the matcher**

The `matcher` field is a glob pattern matched against the tool name. `"Bash"` matches any Bash call. `"Bash(git commit:*)"` only matches Bash calls starting with `git commit`. If your matcher is too specific, it won't trigger.

---

## Symptom: MCP server fails to connect

The MCP server shows as disconnected or its tools are not available.

**Step 1: Check the mcp.json syntax**

Parse the file with `jq . mcp.json`. A JSON syntax error will prevent the server from loading entirely. Check for trailing commas, unclosed braces, or wrong quote types.

**Step 2: Verify the server type and required fields**

- **stdio**: must have `"command"` (the executable to run)
- **sse** or **http**: must have `"url"`
- **ws**: must have `"url"`

A stdio server missing `"command"` or an HTTP server missing `"url"` will fail immediately.

**Step 3: Confirm the command/binary exists**

For stdio servers, run the command manually to confirm it's installed and executable:

```bash
which <your-mcp-server-command>
<your-mcp-server-command> --help
```

If the command isn't found, install the package first.

**Step 4: Check for `${CLAUDE_PLUGIN_ROOT}` in mcp.json**

Unlike hooks.json, `${CLAUDE_PLUGIN_ROOT}` may not expand inside mcp.json in all contexts. If the server path uses this variable, replace it with the absolute path or a path relative to the plugin root that your server resolves itself. Test with a hardcoded absolute path first to confirm whether variable expansion is the issue.

**Step 5: Check authentication requirements**

If the MCP server requires OAuth or an API key, it will connect but immediately fail on the first tool call. In an interactive Claude Code session, run `/mcp` to see server status and authorize any servers requiring OAuth. For API key–based servers, verify the key is set in the environment or in the server's `env` config block.

**Step 6: Inspect server startup output**

For stdio servers, run the server command directly and look for startup errors:

```bash
<your-mcp-server-command> 2>&1 | head -20
```

Most MCP servers print their startup errors to stderr.

---

## Symptom: Skill is never loaded

The model doesn't seem to apply the skill's instructions even when the topic matches.

**Step 1: Verify the file is named exactly `SKILL.md`**

The file must be named `SKILL.md` (all caps) inside a `skills/<skill-name>/` directory. A file named `skill.md`, `Skill.md`, or just placed in `skills/` without a subdirectory won't be discovered.

**Step 2: Check the description field**

The `description` field in the frontmatter is what the model reads to decide whether to load the skill. It must be specific enough to match the user's actual request but not so narrow it misses related phrasings. If the description says "Use when implementing Stripe payments" but the user asks "how do I add a checkout flow", it may not match.

Check: does your description contain the vocabulary your users actually use?

**Step 3: Verify the frontmatter parses correctly**

The frontmatter must be valid YAML between `---` markers. Run:

```bash
python3 -c "
import sys
content = open('skills/<skill-name>/SKILL.md').read()
fm = content.split('---')[1]
import yaml; print(yaml.safe_load(fm))
"
```

A YAML parse error means the skill metadata is invisible to the runtime.

**Step 4: Confirm the plugin is enabled**

Same as for agents: the plugin containing this skill must be listed in `enabledPlugins` in `~/.claude/settings.json`.

---

## Symptom: Command doesn't appear in `/help`

**Step 1: Verify the file location and name**

Commands must be `.md` files in the `commands/` directory of the plugin. The command name in `/help` will be `<plugin-name>:<filename-without-extension>`.

**Step 2: Check frontmatter**

Required field: `description` (shown in `/help`). Optional but expected: `argument-hint`. A missing `description` will cause the command to not appear or appear with no description.

**Step 3: Confirm the plugin is enabled and the path is correct**

Confirm `${CLAUDE_PLUGIN_ROOT}` is resolving correctly for any `allowed-tools` entries that restrict Bash to specific scripts. If the script path doesn't match what's on disk, the command will fail when invoked.

---

## Never Do

- **Never skip the wrapper check** on hooks.json. It is the single most common hook bug and is invisible at a glance.
- **Never assume `\n` in a YAML string is a newline.** It is not. Use a block scalar (`|`) for multi-line agent descriptions.
- **Never hardcode absolute paths** in hooks or MCP config. Use `${CLAUDE_PLUGIN_ROOT}` in hooks; test MCP configs with absolute paths temporarily to isolate variable expansion issues.
- **Never debug an MCP server inside Claude** before confirming the server starts cleanly from the terminal. Claude won't show you startup errors.
- **Never write a single `<example>` block** in an agent description and wonder why the agent doesn't trigger. Two is the minimum.
