# Python SDK and CLI

Use this reference before writing Python or terminal commands. Prefer the exhaustive, current documentation at https://pypi.org/project/meow-sdk/ and https://meow-sdk.readthedocs.io.

## Install and configure

The package supports Python 3.8 and newer and installs both `meow_sdk` and the `meow` CLI.

```bash
python -m pip install meow-sdk
export MEOW_API_KEY="YOUR_PLATFORM_TOKEN"
export MEOW_USERNAME="YOUR_USERNAME"
# Optional for local or self-hosted instances:
export MEOW_URL="https://meowmeowscratch.com"
```

Use a platform token for account-wide SDK/CLI work. Use an app API key when a program must be confined to one app. Never commit either value.

## Create a client

```python
import os
from meow_sdk import Meow

api = Meow(
    base_url=os.getenv("MEOW_URL", "https://meowmeowscratch.com"),
    username=os.getenv("MEOW_USERNAME"),
    api_key=os.environ["MEOW_API_KEY"],
    timeout=30,
)
```

For an anonymous public read, a username is enough:

```python
from meow_sdk import Meow

api = Meow(username="YOUR_USERNAME")
data = api.get("weather-station", "readings")
```

## Create a private collection

New resources are private unless `is_public=True` is deliberately passed.

```python
api.create_app("Weather Station", "weather-station")
api.create_endpoint(
    "weather-station",
    "Readings",
    "readings",
    endpoint_type="collection",
)
api.create_field(
    "weather-station",
    "readings",
    "temperature",
    "Temperature",
    "number",
    required=True,
)
created = api.send("weather-station", "readings", {"temperature": 22.5})
page = api.records("weather-station", "readings", limit=25)
```

Useful method families include:

| Work | Methods |
| --- | --- |
| Public consumer data | `get`, `get_record`, `aggregate`, `export_csv`, `public_dashboard` |
| Records | `send`, `send_many`, `update`, `delete_record`, `records`, `all_records` |
| Apps/endpoints | `apps`, `get_app`, `create_app`, `update_app`, `delete_app`, `endpoints`, `get_endpoint`, `create_endpoint`, `update_endpoint`, `delete_endpoint` |
| Collection schema | `fields`, `create_field`, `update_field`, `delete_field`, `field_types` |
| Static/proxy behavior | `get_payload`, `get_payload_state`, `set_payload`, `get_proxy`, `set_proxy` |
| Operations | `webhooks`, `create_webhook`, `update_webhook`, `delete_webhook`, `get_encryption`, `enable_encryption`, `disable_encryption`, `request_logs` |
| Control panels | `dashboards`, `create_dashboard`, `dashboard_widgets`, `create_dashboard_widget`, `dashboard_state`, `set_dashboard_widget_value` |
| App credentials | `app_keys`, `create_app_key`, `delete_app_key` |
| Discovery | `limits`, `auth_context`, `field_types` |

Use `limits()` with a platform token to inspect enforced capacity. Subscription, checkout, portal, account, and platform-token management remain browser-session operations; do not automate them with an API credential.

Run the bundled inspector when exact signatures may differ from the installed release:

```bash
python scripts/inspect_sdk.py
python scripts/inspect_sdk.py --json
```

## Handle errors

```python
from meow_sdk import AuthError, MeowError, NotFoundError, RateLimitError, ValidationError

try:
    api.send("weather-station", "readings", {"temperature": 22.5})
except AuthError as exc:
    print(f"Check the credential and scope: {exc}")
except ValidationError as exc:
    print(f"Check the field schema and data: {exc}")
except NotFoundError as exc:
    print(f"Check the app and endpoint slugs: {exc}")
except RateLimitError as exc:
    print(f"Back off before retrying: {exc}")
except MeowError as exc:
    print(f"Meow API error {exc.status_code}: {exc}")
```

Retry only `429` and transient `5xx` failures, with a bounded exponential delay. Do not retry validation or authentication failures unchanged.

## CLI examples

The CLI reads `MEOW_API_KEY`, `MEOW_USERNAME`, and optional `MEOW_URL`.

```bash
meow apps
meow endpoints weather-station
meow send weather-station readings temperature=22.5 humidity=65
meow send-batch weather-station readings @records.json
meow records weather-station readings --limit 10
meow get weather-station readings
meow csv weather-station readings
meow dashboards
meow dashboard-data room-controls
meow widget-set room-controls WIDGET_UUID 0.7
meow limits
```

Check `meow --help` and each subcommand's `--help` before emitting less common options. Use the official CLI reference for the full command catalog: https://meow-sdk.readthedocs.io/cli/.

## Raspberry Pi pattern

- Create one app API key for the device and grant only the Read/Write scopes it needs.
- Read the key from an environment file or service manager, not from the script.
- Send a test record and read it back before starting a loop.
- Set a reasonable sampling interval and avoid retry storms while offline.
- Catch hardware read errors separately from API errors and release GPIO or sensor resources during shutdown.
