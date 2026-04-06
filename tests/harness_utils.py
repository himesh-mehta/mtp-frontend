from __future__ import annotations

import shutil
import socket
import tempfile
import time
from pathlib import Path
from uuid import uuid4


def workspace_tempdir(*, prefix: str) -> Path:
    root = Path("tmp")
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{prefix}_{uuid4().hex}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_rmtree(path: Path, *, retries: int = 5, delay_seconds: float = 0.05) -> None:
    for _ in range(max(1, retries)):
        shutil.rmtree(path, ignore_errors=True)
        if not path.exists():
            return
        time.sleep(delay_seconds)
    shutil.rmtree(path, ignore_errors=True)


def wait_for_tcp_listener(host: str, port: int, *, timeout_seconds: float = 5.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        sock = socket.socket()
        try:
            sock.settimeout(0.2)
            sock.connect((host, int(port)))
            return
        except OSError:
            time.sleep(0.02)
        finally:
            sock.close()
    raise TimeoutError(f"Timed out waiting for TCP listener at {host}:{port}")


def workspace_tempfile(*, prefix: str, suffix: str = "") -> Path:
    root = Path("tmp")
    root.mkdir(parents=True, exist_ok=True)
    fd, raw_path = tempfile.mkstemp(prefix=f"{prefix}_", suffix=suffix, dir=str(root))
    Path(raw_path).unlink(missing_ok=True)
    return Path(raw_path)

