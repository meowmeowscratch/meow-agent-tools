#!/usr/bin/env python3
"""Print the installed meow-sdk version and public Meow method signatures."""

import argparse
import inspect
import json
import sys


def inspect_sdk():
    """Return JSON-serializable metadata without making network requests."""
    try:
        import meow_sdk
        from meow_sdk import Meow
    except ImportError as exc:
        raise RuntimeError(
            "meow-sdk is not installed. Run: python -m pip install meow-sdk"
        ) from exc

    methods = {}
    for name, member in inspect.getmembers(Meow, predicate=inspect.isfunction):
        if not name.startswith("_"):
            methods[name] = str(inspect.signature(member))

    return {
        "version": getattr(meow_sdk, "__version__", "unknown"),
        "module": inspect.getfile(Meow),
        "methods": methods,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    try:
        result = inspect_sdk()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("meow-sdk {} ({})".format(result["version"], result["module"]))
        for name, signature in result["methods"].items():
            print("{}{}".format(name, signature))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
