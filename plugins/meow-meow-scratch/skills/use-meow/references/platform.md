# Meow Meow Scratch™ platform

Use this reference to model a project, choose credentials and visibility, or call the REST API directly.

## Mental model

Meow Meow Scratch™ provides a hosted backend for learning APIs and connecting Raspberry Pi and IoT projects.

```text
account
├── apps
│   ├── collection endpoint → field schema + records
│   ├── static endpoint     → one JSON payload
│   └── proxy endpoint      → controlled upstream request
└── dashboards → widgets bound to endpoint UUIDs and key paths
```

- An **app** is a Meow Meow Scratch™ project containing endpoints.
- A **collection** stores typed records. Define fields before sending data.
- A **static endpoint** stores one JSON document and suits current device state or configuration.
- A **proxy endpoint** calls an upstream URL and may apply a JMESPath response transform.
- A **dashboard** presents or changes endpoint values through widgets such as toggles, sliders, colors, numbers, text, selects, and read-only displays.

New apps and endpoints should remain private unless anonymous internet access is intentionally required.

## Credentials

| Credential | Scope | Prefer for |
| --- | --- | --- |
| Platform token | Meow resources across the account | MCP, SDK/CLI discovery, multi-app automation |
| App API key | One app plus its selected Read/Write scopes | Raspberry Pi, device, or single-app integration |
| None | Public consumer reads only | Public examples and intentionally open datasets |

Store credentials in `MEOW_API_KEY`. Full key values are shown once. API credentials authenticate resource calls but are intentionally denied access to identity, account, platform-token-management, and billing routes; perform those operations in the web app.

## URL shapes

The SDK defaults to `https://meowmeowscratch.com`; `/api` is appended internally.

```text
Management: /api/apps/{app}/endpoints/{endpoint}/...
Consumer:   /api/v1/{username}/{app}/{endpoint}/
MCP:        https://meowmeowscratch.com/mcp/
```

Preserve trailing slashes. A private consumer request needs `Authorization: Bearer <key>`. A public consumer request does not.

Collection record operations use:

```text
GET, POST     /api/apps/{app}/endpoints/{endpoint}/records/
GET, PATCH,
DELETE        /api/apps/{app}/endpoints/{endpoint}/records/{record_uuid}/
```

Record bodies wrap user data as `{"data": {...}}`. Lists use `limit` and `offset`; the default is 25 and maximum is 100. Consumer collection reads can filter with lookups such as `temperature__gte=20`, aggregate with `aggregate=avg,max&field=temperature`, or request CSV with `format=csv`.

## Teach with the request cycle

When the user is learning APIs, name each part of the interaction:

1. The HTTP method expresses intent: `GET` reads, `POST` creates, `PATCH` changes, and `DELETE` removes.
2. The URL identifies the app, endpoint, and sometimes a record UUID.
3. The Bearer header proves what the caller may access.
4. The JSON body carries structured data.
5. The status code summarizes the result: commonly `200`, `201`, or `204` for success; `400`, `401`/`403`, `404`, or `429` for common failures.
6. The response body provides data or a useful error message.

Start with one record and read it back. Then add schema validation, filters, pagination, dashboards, webhooks, or hardware.

## Official resources

- Platform docs: https://meowmeowscratch.com/docs
- Meow projects and source: https://github.com/meowmeowscratch
- Python package: https://pypi.org/project/meow-sdk/
- SDK documentation: https://meow-sdk.readthedocs.io
