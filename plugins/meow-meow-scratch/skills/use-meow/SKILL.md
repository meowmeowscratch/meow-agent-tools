---
name: use-meow
description: Build, teach, operate, and troubleshoot Meow Meow Scratch® projects with the REST API, meow-sdk Python client, meow CLI, and Meow MCP server. Use for creating or managing apps, collection/static/proxy endpoints, schemas, records, dashboards, widgets, webhooks, encryption, Raspberry Pi or IoT integrations, configuring Meow MCP in Codex or Claude Code, and explaining API concepts through hands-on Meow projects.
---

# Use Meow Meow Scratch®

Treat Meow Meow Scratch® as the hosted backend for a learning or IoT project. Keep the work understandable to the learner while applying production-safe defaults.

## Load the right reference

- Read [references/platform.md](references/platform.md) when choosing the data model, endpoint type, visibility, credential, or REST route.
- Read [references/sdk.md](references/sdk.md) before writing Python or CLI commands. When the installed SDK version is uncertain, run `python scripts/inspect_sdk.py` before relying on a method signature.
- Read [references/mcp.md](references/mcp.md) when configuring MCP, selecting MCP tools, or diagnosing authentication, redirects, rate limits, and client support.

## Choose the interface

- Use MCP to inspect or operate a live account interactively when Meow tools are available.
- Use the Python SDK for applications, Raspberry Pi programs, and reusable automation.
- Use the CLI for one-off terminal operations and shell workflows.
- Use REST directly when teaching HTTP or integrating a language without an SDK.
- Use the web app for visual setup and for account, credential, and billing operations that API credentials cannot perform.

## Follow the workflow

1. Clarify the outcome, consumer, data shape, update frequency, and whether anonymous internet access is required.
2. Call `connection_status` when diagnosing MCP credentials and `get_limits` before provisioning several resources. Discover existing apps and endpoints before creating anything. Reuse stable slugs when they already represent the requested resource.
3. Choose the narrowest credential:
   - Use a platform token for MCP and account-wide SDK or CLI work across Meow resources.
   - Use an app API key with only the required Read and Write scopes for one device or integration.
   - Use no credential only for direct reads from intentionally public endpoints or shared dashboards.
4. Keep new apps and endpoints private unless the user explicitly asks for public access and understands that the data becomes anonymously readable.
5. Choose the endpoint model:
   - Use `collection` for typed, time-ordered records such as sensor readings or events.
   - Use `static` for one current JSON document such as device state or configuration.
   - Use `proxy` to expose a controlled view of an upstream API.
6. Inspect before writing. For collections, define fields before sending records. Create dashboard widgets with app and endpoint slugs; change a configured value with the widget UUID returned by the API.
7. Make the smallest necessary change, then read the resource back and verify the consumer-facing behavior.
8. Explain the API concept demonstrated by the work—method, URL, authentication, request body, status, response, or pagination—at the learner's level.

## Protect the user

- Never place tokens, app keys, encryption keys, or webhook secrets in source code, prompts, committed configuration, URLs, or logs. Use environment variables or a secret manager.
- Get explicit confirmation immediately before deleting an app, endpoint, record, field, dashboard, widget, key, or webhook; revoking a token; disabling encryption; or replacing important state.
- Warn that newly generated API and encryption keys are shown once. Hand the value to the user without persisting it.
- Do not call account, authentication, platform-token-management, or billing routes with an API credential. Direct the user to the authenticated web app.
- Avoid polling unchanged resources. Respect rate limits and retry only transient failures with bounded exponential backoff.
- Treat proxy targets, webhook destinations, and shared dashboard links as security boundaries. Test them with non-sensitive data first.

## Produce maintainable integrations

- Read `MEOW_API_KEY`, `MEOW_USERNAME`, and optional `MEOW_URL` from the environment.
- Set request timeouts, catch typed SDK errors, and distinguish authentication, validation, not-found, and rate-limit failures.
- Prefer atomic batch writes for multiple records. If one item fails validation, fix the indexed error before retrying the unchanged batch.
- On Raspberry Pi loops, clean up hardware resources, avoid tight retry loops, and keep the app key limited to the target app.
- Prefer a small working request and readback before adding dashboards, webhooks, encryption, transforms, or automation.
- Link to the official docs for exhaustive or version-sensitive details instead of reproducing a stale method catalog.

## Finish with evidence

- Report the created or changed app and endpoint slugs, endpoint type, visibility, credential class used, and any IDs a follow-up call needs.
- Include the consumer URL or a copyable code example when useful, but never include the credential.
- State what was verified and what remains dependent on hardware, network access, or user configuration.
