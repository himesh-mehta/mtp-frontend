from __future__ import annotations

import asyncio
import inspect
import threading
from typing import Any, Awaitable, Callable

from ..schema import MessageEnvelope

EnvelopeResponse = MessageEnvelope
EnvelopeHandler = Callable[..., EnvelopeResponse | Awaitable[EnvelopeResponse]]


class CancellationRegistry:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._cancelled_ids: set[str] = set()

    def cancel(self, request_id: str) -> None:
        with self._lock:
            self._cancelled_ids.add(request_id)

    def is_cancelled(self, request_id: str | None) -> bool:
        if not request_id:
            return False
        with self._lock:
            return request_id in self._cancelled_ids


def extract_request_id(envelope: MessageEnvelope) -> str | None:
    metadata = envelope.metadata if isinstance(envelope.metadata, dict) else {}
    payload = envelope.payload if isinstance(envelope.payload, dict) else {}
    for key in ("request_id", "run_id", "id", "call_id"):
        value = metadata.get(key)
        if value:
            return str(value)
    for key in ("request_id", "run_id", "id", "call_id"):
        value = payload.get(key)
        if value:
            return str(value)
    return None


def cancellation_checker_for(
    registry: CancellationRegistry,
    envelope: MessageEnvelope,
) -> Callable[[], bool]:
    request_id = extract_request_id(envelope)
    return lambda: registry.is_cancelled(request_id)


def mark_cancel_from_envelope(registry: CancellationRegistry, envelope: MessageEnvelope) -> str | None:
    payload = envelope.payload if isinstance(envelope.payload, dict) else {}
    metadata = envelope.metadata if isinstance(envelope.metadata, dict) else {}
    request_id = payload.get("request_id") or payload.get("id") or metadata.get("request_id") or metadata.get("id")
    if not request_id:
        return None
    request_id_str = str(request_id)
    registry.cancel(request_id_str)
    return request_id_str


def _invoke_handler(handler: EnvelopeHandler, envelope: MessageEnvelope, cancel_checker: Callable[[], bool]) -> Any:
    try:
        signature = inspect.signature(handler)
    except Exception:
        return handler(envelope)
    if "cancel_checker" in signature.parameters:
        return handler(envelope, cancel_checker=cancel_checker)
    return handler(envelope)


def invoke_handler_sync(
    handler: EnvelopeHandler,
    envelope: MessageEnvelope,
    cancel_checker: Callable[[], bool],
) -> MessageEnvelope:
    result = _invoke_handler(handler, envelope, cancel_checker)
    if inspect.isawaitable(result):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(result)
        raise RuntimeError("Async envelope handler cannot be invoked in an active event loop.")
    return result


async def invoke_handler_async(
    handler: EnvelopeHandler,
    envelope: MessageEnvelope,
    cancel_checker: Callable[[], bool],
) -> MessageEnvelope:
    result = _invoke_handler(handler, envelope, cancel_checker)
    if inspect.isawaitable(result):
        return await result
    return result
