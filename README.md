# Meow Agent Tools

Agent tooling for [Meow Meow Scratch™](https://meowmeowscratch.com/), packaged for both Codex and Claude Code. The repository provides one shared `use-meow` skill plus native marketplace, plugin, and MCP configuration for each client.

Use it to build and manage APIs, teach HTTP concepts, connect Raspberry Pi or IoT projects, work with the Python SDK and CLI, and let an agent operate Meow resources through MCP.

## Compatibility

| Capability | Codex | Claude Code |
| --- | --- | --- |
| Marketplace installation | `.agents/plugins/marketplace.json` | `.claude-plugin/marketplace.json` |
| Plugin manifest | `.codex-plugin/plugin.json` | `.claude-plugin/plugin.json` |
| Shared agent workflow | `skills/use-meow/SKILL.md` | `skills/use-meow/SKILL.md` |
| Hosted MCP server | `.mcp.json` | `claude.mcp.json` through the Claude manifest |
| Secret source | `MEOW_PLATFORM_API_KEY` | `MEOW_PLATFORM_API_KEY` |

The skill, scripts, and references are shared. Only the marketplace, manifest, and MCP authentication wrapper differ. Claude support refers to **Claude Code**; this repository does not define a Claude.ai or Claude Desktop connector.

## Before installation

Create a platform token under **Account → Platform Tokens** in Meow Meow Scratch™, then expose it to the process that launches your agent:

```bash
export MEOW_PLATFORM_API_KEY="YOUR_PLATFORM_TOKEN"
```

Use a platform token for MCP because the tool set discovers and manages resources across your account. Store an app API key in `MEOW_APP_API_KEY` instead for a Raspberry Pi, device, or other integration that should be restricted to one app. The ambiguous `MEOW_API_KEY` name is not supported.

Never commit either credential. The repository contains environment-variable names only.

## Install in Codex

### From GitHub

```bash
codex plugin marketplace add meowmeowscratch/meow-agent-tools
codex plugin add meow-meow-scratch@meow-agent-tools
```

### From a local checkout

Run these commands from the repository root:

```bash
codex plugin marketplace add "$PWD"
codex plugin add meow-meow-scratch@meow-agent-tools
```

Start a new Codex thread after installation, then inspect `/mcp` if the Meow tools do not appear. Ask naturally for a Meow task or choose Meow Meow Scratch™ from the installed plugins and skills.

## Install in Claude Code

### From GitHub

```bash
claude plugin marketplace add meowmeowscratch/meow-agent-tools
claude plugin install meow-meow-scratch@meow-agent-tools
```

### From a local checkout

Run these commands from the repository root:

```bash
claude plugin marketplace add "$PWD"
claude plugin install meow-meow-scratch@meow-agent-tools
```

Start a new Claude Code session or run `/reload-plugins`, then use `/mcp` to verify the `meow` server. Invoke the skill explicitly with:

```text
/meow-meow-scratch:use-meow
```

Claude Code can also select the skill automatically when the request mentions Meow Meow Scratch™, `meow-sdk`, the Meow CLI, MCP, Raspberry Pi, or an IoT project.

## Use only the skill

The skill follows the shared `SKILL.md` format and does not require MCP for documentation, SDK, CLI, REST, or code-generation work.

For personal Codex use:

```bash
mkdir -p ~/.codex/skills
cp -R plugins/meow-meow-scratch/skills/use-meow ~/.codex/skills/
```

For personal Claude Code use:

```bash
mkdir -p ~/.claude/skills
cp -R plugins/meow-meow-scratch/skills/use-meow ~/.claude/skills/
```

Live account operations still require a configured Meow MCP connection or another authenticated Meow client. See the [MCP reference](plugins/meow-meow-scratch/skills/use-meow/references/mcp.md) for standalone client configuration.

## What the skill covers

- Choosing between REST, Python SDK, CLI, MCP, and the web app.
- Designing collection, static, and proxy endpoints.
- Creating schemas, records, dashboards, widgets, webhooks, and integrations.
- Teaching methods, URLs, headers, JSON bodies, status codes, pagination, and errors.
- Building maintainable Raspberry Pi and IoT clients.
- Choosing platform tokens versus app-scoped API keys.
- Keeping new apps and endpoints private unless public access is intentional.
- Confirming destructive changes and protecting one-time credentials.

The bundled SDK inspector reports the installed package version and public method signatures without making a network request:

```bash
python plugins/meow-meow-scratch/skills/use-meow/scripts/inspect_sdk.py
```

## Repository layout

```text
meow-agent-tools/
├── .agents/plugins/marketplace.json         # Codex marketplace
├── .claude-plugin/marketplace.json          # Claude Code marketplace
└── plugins/meow-meow-scratch/
    ├── .codex-plugin/plugin.json             # Codex manifest
    ├── .claude-plugin/plugin.json            # Claude Code manifest
    ├── .mcp.json                             # Codex MCP authentication
    ├── claude.mcp.json                       # Claude Code MCP authentication
    └── skills/use-meow/
        ├── SKILL.md                          # Shared workflow
        ├── agents/openai.yaml                # Codex skill metadata
        ├── references/                       # Platform, SDK, CLI, and MCP guides
        └── scripts/inspect_sdk.py            # Offline SDK inspection
```

Keep both plugin versions aligned when publishing a release. Validate the Claude package with `claude plugin validate .`, and validate the shared skill and Codex manifest before publishing.

## Security model

- The MCP server receives a Bearer platform token from `MEOW_PLATFORM_API_KEY`; neither client configuration contains its value.
- Platform tokens provide account-wide Meow resource access but cannot access identity, account, platform-token-management, or billing routes through API authentication.
- App API keys are restricted to one app and should receive only the required Read and Write scopes.
- The hosted MCP service does not add its own human approval gate. Agent clients should require confirmation for destructive and sensitive operations.
- Public apps or endpoints may expose data anonymously. Keep resources private by default.

## Links

- [Meow Meow Scratch™ documentation](https://meowmeowscratch.com/docs)
- [meow-sdk on PyPI](https://pypi.org/project/meow-sdk/)
- [SDK documentation](https://meow-sdk.readthedocs.io)
- [Meow Meow Scratch™ projects](https://github.com/meowmeowscratch)
- [Codex plugin documentation](https://learn.chatgpt.com/docs/build-plugins)
- [Claude Code plugin documentation](https://code.claude.com/docs/en/plugins)
