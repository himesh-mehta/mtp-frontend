from __future__ import annotations

import asyncio
from typing import Any

from ..schema import MessageEnvelope
from .common import (
    CancellationRegistry,
    EnvelopeHandler,
    cancellation_checker_for,
    invoke_handler_async,
    mark_cancel_from_envelope,
)


class WebSocketTransportServer:
    """
    Optional websocket envelope transport.

    Requires:
    - pip install websockets
    """

    def __init__(self, host: str, port: int, handler: EnvelopeHandler) -> None:
        self.host = host
        self.port = port
        self.handler = handler
        self._server: Any = None
        self._cancellations = CancellationRegistry()

    async def start(self) -> None:
        try:
            import websockets
        except Exception as exc:  # noqa: BLE001
            raise ImportError("websockets package is required for WebSocketTransportServer.") from exc

        async def _handle_connection(websocket: Any) -> None:
            async for raw in websocket:
                try:
                    request = MessageEnvelope.from_json(raw)
                    if request.kind in {"cancel", "cancel_request"}:
                        cancelled_id = mark_cancel_from_envelope(self._cancellations, request)
                        response = MessageEnvelope.create(
                            kind="cancel_ack",
                            payload={"request_id": cancelled_id},
                        )
                    else:
                        response = await invoke_handler_async(
                            self.handler,
                            request,
                            cancellation_checker_for(self._cancellations, request),
                        )
                except Exception as exc:  # noqa: BLE001
                    response = MessageEnvelope.create(
                        kind="error",
                        payload={"message": str(exc)},
                    )
                await websocket.send(response.to_json())

        self._server = await websockets.serve(_handle_connection, self.host, self.port)

    async def serve_forever(self) -> None:
        if self._server is None:
            await self.start()
        assert self._server is not None
        await self._server.wait_closed()

    async def shutdown(self) -> None:
        if self._server is None:
            return
        self._server.close()
        await self._server.wait_closed()
        self._server = None


def run_ws_transport(handler: EnvelopeHandler, host: str = "127.0.0.1", port: int = 8765) -> None:
    server = WebSocketTransportServer(host=host, port=port, handler=handler)

    async def _runner() -> None:
        await server.start()
        await server.serve_forever()

    asyncio.run(_runner())
