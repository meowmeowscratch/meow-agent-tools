# Meow MCP server

Use this reference to install the packaged integration, configure a standalone MCP client, choose tools, or diagnose a connection.

## Contents

- [Support boundary](#support-boundary)
- [Authentication](#authentication)
- [Packaged Codex installation](#packaged-codex-installation)
- [Packaged Claude Code installation](#packaged-claude-code-installation)
- [Standalone Codex configuration](#standalone-codex-configuration)
- [Standalone Claude Code configuration](#standalone-claude-code-configuration)
- [Tool map](#tool-map)
- [Safety and limits](#safety-and-limits)
- [Troubleshooting](#troubleshooting)

## Support boundary

The hosted Meow server uses Streamable HTTP at:

```text
https://meowmeowscratch.com/mcp/
```

Keep the trailing slash to avoid a redirect during MCP negotiation.

The repository supports Codex and Claude Code with one shared skill and separate native wrappers:

| Client | Marketplace | MCP definition |
| --- | --- | --- |
| Codex | `.agents/plugins/marketplace.json` | `.mcp.json` using `bearer_token_env_var` |
| Claude Code | `.claude-plugin/marketplace.json` | `claude.mcp.json` using an expanded Authorization header |

Do not collapse these MCP files into one. Their authentication fields are client-specific even though both connect to the same server. Claude support here means Claude Code, not an account-level Claude.ai or Claude Desktop connector.

## Authentication

Create a platform token under **Account → Platform Tokens**, then configure the same variable in the client-specific user file:

| Client | Recommended user-level source |
| --- | --- |
| Codex | `~/.codex/.env` |
| Claude Code | `~/.claude/settings.json` under `env` |

For Codex, create or edit `~/.codex/.env`:

```dotenv
MEOW_PLATFORM_API_KEY=YOUR_PLATFORM_TOKEN
```

For Claude Code, merge the variable into the existing `env` object in `~/.claude/settings.json`:

```json
{
  "env": {
    "MEOW_PLATFORM_API_KEY": "YOUR_PLATFORM_TOKEN"
  }
}
```

Claude Code does not document `~/.claude/.env` as a startup source. Use `~/.claude/settings.json` for the supported per-user equivalent. Restart the client after adding or rotating the token, and avoid defining the same variable in several sources.

Use a platform token because the MCP tool set performs account-wide discovery and management. App API keys are intentionally limited to one app and are better suited to devices and single-app integrations.

The MCP connection always requires a Bearer token. Some consumer tools read data that is public downstream, but the hosted MCP session itself is still authenticated.

These files are plaintext. Keep them outside repositories, restrict them to your user account (for example, `chmod 600` on macOS or Linux), and never commit them. They configure Codex or Claude Code only; SDK, CLI, CI, and other standalone clients still need `MEOW_PLATFORM_API_KEY` in their own process environment or secret manager.

## Packaged Codex installation

From GitHub:

```bash
codex plugin marketplace add meowmeowscratch/meow-agent-tools
codex plugin add meow-meow-scratch@meow-agent-tools
```

From the repository root during local development:

```bash
codex plugin marketplace add "$PWD"
codex plugin add meow-meow-scratch@meow-agent-tools
```

The plugin's `.mcp.json` reads the Bearer token from `MEOW_PLATFORM_API_KEY`; Codex can load it from `~/.codex/.env`. Start a new thread after installing or updating the plugin, then use `/mcp` to confirm that the server and tools are available.

## Packaged Claude Code installation

From GitHub:

```bash
claude plugin marketplace add meowmeowscratch/meow-agent-tools
claude plugin install meow-meow-scratch@meow-agent-tools
```

From the repository root during local development:

```bash
claude plugin marketplace add "$PWD"
claude plugin install meow-meow-scratch@meow-agent-tools
```

The Claude manifest points to `claude.mcp.json`, which expands `MEOW_PLATFORM_API_KEY` from Claude Code's environment into the Authorization header. Configure the variable under `env` in `~/.claude/settings.json`, then start a new session or run `/reload-plugins`, verify the server with `/mcp`, and invoke the skill with `/meow-meow-scratch:use-meow` when explicit selection is useful.

## Standalone Codex configuration

Use this when installing the whole plugin is unnecessary:

```bash
codex mcp add meow \
  --url https://meowmeowscratch.com/mcp/ \
  --bearer-token-env-var MEOW_PLATFORM_API_KEY
codex mcp list
```

Equivalent `~/.codex/config.toml` or trusted project `.codex/config.toml`:

```toml
[mcp_servers.meow]
url = "https://meowmeowscratch.com/mcp/"
bearer_token_env_var = "MEOW_PLATFORM_API_KEY"
```

Restart Codex after changing configuration and use `/mcp` to verify the server.

## Standalone Claude Code configuration

Place this in the project's `.mcp.json`:

```json
{
  "mcpServers": {
    "meow": {
      "type": "http",
      "url": "https://meowmeowscratch.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${MEOW_PLATFORM_API_KEY}"
      }
    }
  }
}
```

Make `MEOW_PLATFORM_API_KEY` available through `~/.claude/settings.json` as shown in [Authentication](#authentication), or launch Claude Code from a shell where it is set. Approve the project server and check `/mcp`. Do not place the token directly in the project file or URL.

## Tool map

The server exposes schema-defined tools in these families:

| Family | Typical operations |
| --- | --- |
| Discovery | Verify the credential, inspect enforced limits, and list apps, endpoints, fields, records, dashboards, widgets, and field types |
| Structure | Create, update, and delete apps, endpoints, and collection fields |
| Data | Send one record or an atomic batch; inspect, update, delete, aggregate, and export records; read a bare static document or its metadata envelope |
| Integrations | Configure proxy requests, webhooks, response encryption, and request logs |
| Control panels | Create widgets with app and endpoint slugs, read canonical state, and write through a widget UUID |
| Consumer views | Read public endpoints or records and open shared dashboards |

Start with `connection_status`; call `get_limits` before a large provisioning task. List and inspect before mutating. Obtain record, field, widget, webhook, or key UUIDs from discovery tools rather than guessing them. Endpoint slugs are sufficient for canonical dashboard creation.

## Safety and limits

- The hosted service allows 60 tool calls per token per minute. Avoid polling unchanged resources.
- Require human approval immediately before destructive calls, key revocation, encryption changes, or sensitive writes. The server does not add a separate human approval gate.
- Keep apps and endpoints private by default. Making either public can expose endpoint data anonymously.
- Treat returned API keys and encryption keys as one-time secrets; never persist them in the repository or agent configuration.
- API credentials cannot access identity, account, platform-token-management, or billing routes. Those tools may be discoverable because of SDK parity but will be rejected; use the web app.
- Review organization policy when a managed Codex or Claude environment restricts plugins or MCP servers.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `401` or missing tools | Confirm `MEOW_PLATFORM_API_KEY` contains an active platform token in `~/.codex/.env`, `~/.claude/settings.json`, or the process that launched the client; restart the client, then call `connection_status` once tools load |
| Redirect or negotiation failure | Use the exact `/mcp/` URL with the trailing slash |
| `403` | Confirm the route is a Meow resource route; use the web app for account, platform-token-management, and billing operations |
| `429` | Reduce calls and wait for the one-minute window; do not aggressively retry |
| Codex shows old configuration | Reinstall or refresh the plugin and start a new thread |
| Claude shows old configuration | Run `/reload-plugins` or start a new Claude Code session |
| Claude reports a missing variable | Confirm the `env` object in `~/.claude/settings.json` contains `MEOW_PLATFORM_API_KEY`, restart Claude Code, and inspect `claude mcp list` |
| Plugin is installed but MCP is absent | Check client or workspace policy, then inspect `/mcp` and the client's debug output |

Official references:

- Meow Meow Scratch® docs: https://meowmeowscratch.com/docs
- Codex plugins: https://learn.chatgpt.com/docs/build-plugins
- Claude Code plugins: https://code.claude.com/docs/en/plugins
- Claude Code MCP: https://code.claude.com/docs/en/mcp
- Claude Code environment variables: https://code.claude.com/docs/en/env-vars
