# Supply Chain Risk Checklist

Run these checks before installing any external plugin. Low-star repos with install scripts or unusual dependencies carry the highest risk.

## GitHub API quick scan

```bash
curl -s "https://api.github.com/repos/<owner>/<repo>" | jq '{
  license: .license.spdx_id,
  pushed_at: .pushed_at,
  stars: .stargazers_count,
  archived: .archived,
  fork: .fork
}'
```

**Red flags:**
- `"license": null` — unlicensed, hard stop
- `"archived": true` — frozen, proceed only if explicitly requested by user
- `"pushed_at"` more than 2 years ago — likely abandoned
- `"fork": true` — check if the upstream is more appropriate

## Dangerous install scripts

```bash
# Node
cat package.json | jq '.scripts | {postinstall, prepare, preinstall}'

# Python
cat pyproject.toml | grep -A5 "\[tool.hatch"
cat setup.py 2>/dev/null | head -30
```

**Rule:** Any `postinstall` or `prepare` script that calls `curl`, `wget`, `bash`, `sh`, `exec`, or similar on a repo with < 100 stars is a hard stop.

## Dependency audit

```bash
# Node — check for known vulnerabilities
npm audit --audit-level=high

# Python — check for suspicious packages
pip install safety && safety check -r requirements.txt
```

## MCP surface verification

After cloning, confirm the repo actually provides MCP tools:

```bash
grep -r "server.tool\|@mcp.tool\|tools:\|addTool\|register_tool" \
  --include="*.ts" --include="*.js" --include="*.py" -l .
```

If this returns nothing, the repo may not expose any tools to Claude. Check the README for clarification before proceeding.

## License compatibility quick reference

| License | Use | Notes |
|---------|-----|-------|
| MIT | ✅ Go ahead | Most permissive |
| Apache 2.0 | ✅ Go ahead | Patent clause included |
| BSD (2 or 3-clause) | ✅ Go ahead | Attribution required |
| ISC | ✅ Go ahead | Functionally MIT |
| MPL-2.0 | ⚠️ Warn user | File-level copyleft |
| LGPL | ⚠️ Warn user | Library-level copyleft |
| GPL-2.0 / GPL-3.0 | ⚠️ Warn user | Project-level copyleft |
| AGPL-3.0 | ⚠️ Warn user | Network use triggers copyleft |
| SSPL | 🚫 Hard stop | MongoDB's restrictive license |
| No license | 🚫 Hard stop | All rights reserved by default |
| BUSL | 🚫 Hard stop | Business source — time-limited open |
