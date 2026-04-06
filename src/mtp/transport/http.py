from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from ..schema import MessageEnvelope
from .common import (
    CancellationRegistry,
    EnvelopeHandler,
    cancellation_checker_for,
    invoke_handler_sync,
    mark_cancel_from_envelope,
)


class HTTPTransportServer:
    def __init__(self, host: str, port: int, handler: EnvelopeHandler) -> None:
        self.host = host
        self.port = port
        self.handler = handler
        self._server: ThreadingHTTPServer | None = None
        self._cancellations = CancellationRegistry()

    def start(self) -> None:
        outer = self

        class _Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                try:
                    content_length = int(self.headers.get("Content-Length", "0"))
                    raw = self.rfile.read(content_length).decode("utf-8")
                    request = MessageEnvelope.from_json(raw)
                    if request.kind in {"cancel", "cancel_request"}:
                        cancelled_id = mark_cancel_from_envelope(outer._cancellations, request)
                        response = MessageEnvelope.create(
                            kind="cancel_ack",
                            payload={"request_id": cancelled_id},
                        )
                    else:
                        response = invoke_handler_sync(
                            outer.handler,
                            request,
                            cancellation_checker_for(outer._cancellations, request),
                        )
                    body = response.to_json().encode("utf-8")
                    self.send_response(200)
                except Exception as exc:  # noqa: BLE001
                    error_env = MessageEnvelope.create(
                        kind="error",
                        payload={"message": str(exc)},
                    )
                    body = error_env.to_json().encode("utf-8")
                    self.send_response(400)

                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args) -> None:  # noqa: A003
                return

        self._server = ThreadingHTTPServer((self.host, self.port), _Handler)
        self._server.serve_forever()

    def shutdown(self) -> None:
        if self._server is not None:
            self._server.shutdown()
