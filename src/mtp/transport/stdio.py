from __future__ import annotations

import sys
from .common import (
    CancellationRegistry,
    EnvelopeHandler,
    cancellation_checker_for,
    invoke_handler_sync,
    mark_cancel_from_envelope,
)
from ..schema import MessageEnvelope


def run_stdio_transport(handler: EnvelopeHandler) -> None:
    """
    Reads line-delimited JSON envelopes from stdin and writes one JSON envelope per line to stdout.
    """
    cancellations = CancellationRegistry()
    for line in sys.stdin:
        raw = line.strip()
        if not raw:
            continue
        try:
            request = MessageEnvelope.from_json(raw)
            if request.kind in {"cancel", "cancel_request"}:
                cancelled_id = mark_cancel_from_envelope(cancellations, request)
                response = MessageEnvelope.create(
                    kind="cancel_ack",
                    payload={"request_id": cancelled_id},
                )
            else:
                response = invoke_handler_sync(
                    handler,
                    request,
                    cancellation_checker_for(cancellations, request),
                )
        except Exception as exc:  # noqa: BLE001
            response = MessageEnvelope.create(
                kind="error",
                payload={"message": str(exc)},
            )
        sys.stdout.write(response.to_json() + "\n")
        sys.stdout.flush()
