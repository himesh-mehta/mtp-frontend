from __future__ import annotations

import base64
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4


def _read_bytes_from_source(
    *,
    content: bytes | str | None = None,
    filepath: str | Path | None = None,
) -> bytes | None:
    if content is None and filepath is None:
        return None
    if isinstance(content, bytes):
        return content
    if isinstance(content, str):
        return content.encode("utf-8")
    if filepath is not None:
        path = Path(filepath)
        if path.exists() and path.is_file():
            return path.read_bytes()
    return None


@dataclass(slots=True)
class Image:
    url: str | None = None
    filepath: str | Path | None = None
    content: bytes | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    format: str | None = None
    mime_type: str | None = None
    detail: str | None = None
    alt_text: str | None = None

    def get_content_bytes(self) -> bytes | None:
        return _read_bytes_from_source(content=self.content, filepath=self.filepath)

    def to_base64(self) -> str | None:
        raw = self.get_content_bytes()
        if raw is None:
            return None
        return base64.b64encode(raw).decode("utf-8")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Image":
        content = data.get("content")
        if isinstance(content, str):
            try:
                content = base64.b64decode(content)
            except Exception:
                content = content.encode("utf-8")
        return cls(
            url=data.get("url"),
            filepath=data.get("filepath"),
            content=content if isinstance(content, bytes) else None,
            id=str(data.get("id") or uuid4()),
            format=data.get("format"),
            mime_type=data.get("mime_type"),
            detail=data.get("detail"),
            alt_text=data.get("alt_text"),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "url": self.url,
            "filepath": str(self.filepath) if self.filepath is not None else None,
            "format": self.format,
            "mime_type": self.mime_type,
            "detail": self.detail,
            "alt_text": self.alt_text,
        }
        encoded = self.to_base64()
        if encoded is not None:
            payload["content"] = encoded
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(slots=True)
class Audio:
    url: str | None = None
    filepath: str | Path | None = None
    content: bytes | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    format: str | None = None
    mime_type: str | None = None
    transcript: str | None = None

    def get_content_bytes(self) -> bytes | None:
        return _read_bytes_from_source(content=self.content, filepath=self.filepath)

    def to_base64(self) -> str | None:
        raw = self.get_content_bytes()
        if raw is None:
            return None
        return base64.b64encode(raw).decode("utf-8")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Audio":
        content = data.get("content")
        if isinstance(content, str):
            try:
                content = base64.b64decode(content)
            except Exception:
                content = content.encode("utf-8")
        return cls(
            url=data.get("url"),
            filepath=data.get("filepath"),
            content=content if isinstance(content, bytes) else None,
            id=str(data.get("id") or uuid4()),
            format=data.get("format"),
            mime_type=data.get("mime_type"),
            transcript=data.get("transcript"),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "url": self.url,
            "filepath": str(self.filepath) if self.filepath is not None else None,
            "format": self.format,
            "mime_type": self.mime_type,
            "transcript": self.transcript,
        }
        encoded = self.to_base64()
        if encoded is not None:
            payload["content"] = encoded
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(slots=True)
class Video:
    url: str | None = None
    filepath: str | Path | None = None
    content: bytes | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    format: str | None = None
    mime_type: str | None = None

    def get_content_bytes(self) -> bytes | None:
        return _read_bytes_from_source(content=self.content, filepath=self.filepath)

    def to_base64(self) -> str | None:
        raw = self.get_content_bytes()
        if raw is None:
            return None
        return base64.b64encode(raw).decode("utf-8")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Video":
        content = data.get("content")
        if isinstance(content, str):
            try:
                content = base64.b64decode(content)
            except Exception:
                content = content.encode("utf-8")
        return cls(
            url=data.get("url"),
            filepath=data.get("filepath"),
            content=content if isinstance(content, bytes) else None,
            id=str(data.get("id") or uuid4()),
            format=data.get("format"),
            mime_type=data.get("mime_type"),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "url": self.url,
            "filepath": str(self.filepath) if self.filepath is not None else None,
            "format": self.format,
            "mime_type": self.mime_type,
        }
        encoded = self.to_base64()
        if encoded is not None:
            payload["content"] = encoded
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(slots=True)
class File:
    id: str | None = None
    url: str | None = None
    filepath: str | Path | None = None
    content: bytes | str | None = None
    mime_type: str | None = None
    filename: str | None = None
    format: str | None = None

    def get_content_bytes(self) -> bytes | None:
        return _read_bytes_from_source(content=self.content, filepath=self.filepath)

    def to_base64(self) -> str | None:
        raw = self.get_content_bytes()
        if raw is None:
            return None
        return base64.b64encode(raw).decode("utf-8")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "File":
        content = data.get("content")
        if isinstance(content, str):
            try:
                content = base64.b64decode(content)
            except Exception:
                pass
        return cls(
            id=data.get("id"),
            url=data.get("url"),
            filepath=data.get("filepath"),
            content=content if isinstance(content, (bytes, str)) else None,
            mime_type=data.get("mime_type"),
            filename=data.get("filename"),
            format=data.get("format"),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "url": self.url,
            "filepath": str(self.filepath) if self.filepath is not None else None,
            "mime_type": self.mime_type,
            "filename": self.filename,
            "format": self.format,
        }
        if isinstance(self.content, str):
            payload["content"] = self.content
        else:
            encoded = self.to_base64()
            if encoded is not None:
                payload["content"] = encoded
        return {k: v for k, v in payload.items() if v is not None}


def _coerce_media_list(
    values: Iterable[Any] | None,
    *,
    ctor: Any,
) -> list[Any] | None:
    if values is None:
        return None
    out: list[Any] = []
    for item in values:
        if isinstance(item, ctor):
            out.append(item)
        elif isinstance(item, dict):
            out.append(ctor.from_dict(item))
    return out or None


def coerce_images(values: Iterable[Any] | None) -> list[Image] | None:
    return _coerce_media_list(values, ctor=Image)


def coerce_audios(values: Iterable[Any] | None) -> list[Audio] | None:
    return _coerce_media_list(values, ctor=Audio)


def coerce_videos(values: Iterable[Any] | None) -> list[Video] | None:
    return _coerce_media_list(values, ctor=Video)


def coerce_files(values: Iterable[Any] | None) -> list[File] | None:
    return _coerce_media_list(values, ctor=File)
