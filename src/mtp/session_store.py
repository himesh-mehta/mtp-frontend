from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import threading
from typing import Any, Protocol

from .media import coerce_audios, coerce_files, coerce_images, coerce_videos


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if is_dataclass(value):
        return _json_safe(asdict(value))
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        try:
            return _json_safe(to_dict())
        except Exception:
            return str(value)
    return str(value)


def _restore_message_media(message: dict[str, Any]) -> dict[str, Any]:
    restored = dict(message)
    if "images" in restored:
        restored["images"] = coerce_images(restored.get("images"))
    if "audios" in restored:
        restored["audios"] = coerce_audios(restored.get("audios"))
    if "videos" in restored:
        restored["videos"] = coerce_videos(restored.get("videos"))
    if "files" in restored:
        restored["files"] = coerce_files(restored.get("files"))
    return restored


@dataclass(slots=True)
class SessionRun:
    run_id: str
    input: str
    final_text: str
    cancelled: bool = False
    paused: bool = False
    total_tool_calls: int = 0
    created_at: str = field(default_factory=_utc_now_iso)


@dataclass(slots=True)
class SessionRecord:
    session_id: str
    user_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    messages: list[dict[str, Any]] = field(default_factory=list)
    runs: list[SessionRun] = field(default_factory=list)
    created_at: str = field(default_factory=_utc_now_iso)
    updated_at: str = field(default_factory=_utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["messages"] = [_json_safe(message) for message in self.messages]
        payload["metadata"] = _json_safe(self.metadata)
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SessionRecord:
        runs_data = data.get("runs") or []
        runs: list[SessionRun] = []
        for item in runs_data:
            if not isinstance(item, dict):
                continue
            runs.append(
                SessionRun(
                    run_id=str(item.get("run_id") or ""),
                    input=str(item.get("input") or ""),
                    final_text=str(item.get("final_text") or ""),
                    cancelled=bool(item.get("cancelled")),
                    paused=bool(item.get("paused")),
                    total_tool_calls=int(item.get("total_tool_calls") or 0),
                    created_at=str(item.get("created_at") or _utc_now_iso()),
                )
            )

        messages_data = data.get("messages") or []
        messages: list[dict[str, Any]] = []
        for item in messages_data:
            if isinstance(item, dict):
                messages.append(_restore_message_media(item))

        return cls(
            session_id=str(data.get("session_id") or ""),
            user_id=data.get("user_id"),
            metadata=data.get("metadata") if isinstance(data.get("metadata"), dict) else {},
            messages=messages,
            runs=runs,
            created_at=str(data.get("created_at") or _utc_now_iso()),
            updated_at=str(data.get("updated_at") or _utc_now_iso()),
        )


class SessionStore(Protocol):
    def get_session(self, session_id: str, *, user_id: str | None = None) -> SessionRecord | None:
        ...

    def upsert_session(self, session: SessionRecord) -> SessionRecord:
        ...


class JsonSessionStore:
    def __init__(self, *, db_path: str | Path = "tmp/mtp_json_db", session_table: str = "mtp_sessions") -> None:
        self.db_path = Path(db_path)
        self.session_table = session_table
        self._lock = threading.RLock()

    @property
    def file_path(self) -> Path:
        return self.db_path / f"{self.session_table}.json"

    def _read_all(self) -> list[dict[str, Any]]:
        self.db_path.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")
            return []
        raw = self.file_path.read_text(encoding="utf-8")
        if not raw.strip():
            return []
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in session store: {self.file_path}") from exc
        if not isinstance(payload, list):
            raise ValueError(f"Session store payload must be a list: {self.file_path}")
        return [item for item in payload if isinstance(item, dict)]

    def _write_all(self, rows: list[dict[str, Any]]) -> None:
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(json.dumps(rows, indent=2, ensure_ascii=True), encoding="utf-8")

    def get_session(self, session_id: str, *, user_id: str | None = None) -> SessionRecord | None:
        with self._lock:
            for row in self._read_all():
                if row.get("session_id") != session_id:
                    continue
                stored_user_id = row.get("user_id")
                if user_id is not None and stored_user_id is not None and stored_user_id != user_id:
                    continue
                return SessionRecord.from_dict(row)
        return None

    def upsert_session(self, session: SessionRecord) -> SessionRecord:
        with self._lock:
            rows = self._read_all()
            serialized = session.to_dict()
            serialized["updated_at"] = _utc_now_iso()
            if not serialized.get("created_at"):
                serialized["created_at"] = serialized["updated_at"]

            for idx, row in enumerate(rows):
                if row.get("session_id") == session.session_id:
                    rows[idx] = serialized
                    break
            else:
                rows.append(serialized)

            self._write_all(rows)
            return SessionRecord.from_dict(serialized)
