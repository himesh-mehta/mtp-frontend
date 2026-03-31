from __future__ import annotations

import sys
from typing import Callable

from ..schema import MessageEnvelope


EnvelopeHandler = Callable[[MessageEnvelope], MessageEnvelope]


def run_stdio_transport(handler: EnvelopeHandler) -> None:
    """
    Reads line-delimited JSON envelopes from stdin and writes one JSON envelope per line to stdout.
    """
    for line in sys.stdin:
        raw = line.strip()
        if not raw:
            continue
        try:
            request = MessageEnvelope.from_json(raw)
            response = handler(request)
        except Exception as exc:  # noqa: BLE001
            response = MessageEnvelope.create(
                kind="error",
                payload={"message": str(exc)},
            )
        sys.stdout.write(response.to_json() + "\n")
        sys.stdout.flush()
