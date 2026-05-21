"""Minimal client-side verification example for signed relay responses."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from relay_service.core import verify_signed_response


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: python examples/verify_signed_response.py <signed-response.json> <secret>")
        return 2

    payload = json.loads(Path(sys.argv[1]).read_text())
    verify_signed_response(payload, secret=sys.argv[2])
    print("signature ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
