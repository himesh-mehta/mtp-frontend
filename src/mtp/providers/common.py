from __future__ import annotations

import base64
import json
import mimetypes
import re
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from ..media import Audio, File, Image, Video
from ..protocol import ToolBatch, ToolCall


def _read_value(obj: Any, key: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def _coerce_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except Exception:
        return None


def _first_int(source: Any, *keys: str) -> int | None:
    for key in keys:
        value = _coerce_int(_read_value(source, key))
        if value is not None:
            return value
    return None


def extract_usage_metrics(response: Any) -> dict[str, int]:
    usage = _read_value(response, "usage")
    if usage is None:
        usage = _read_value(response, "usage_metadata")
    if usage is None:
        usage = _read_value(response, "usageMetadata")
    if usage is None:
        return {}

    prompt_tokens = _first_int(
        usage,
        "prompt_tokens",
        "input_tokens",
        "prompt_token_count",
        "promptTokenCount",
        "inputTokenCount",
    )

    completion_tokens = _first_int(
        usage,
        "completion_tokens",
        "output_tokens",
        "candidates_token_count",
        "response_token_count",
        "completionTokenCount",
        "outputTokenCount",
        "candidatesTokenCount",
        "responseTokenCount",
    )

    total_tokens = _first_int(
        usage,
        "total_tokens",
        "total_token_count",
        "totalTokenCount",
    )
    if total_tokens is None and prompt_tokens is not None and completion_tokens is not None:
        total_tokens = prompt_tokens + completion_tokens

    reasoning_tokens: int | None = None
    completion_details = _read_value(usage, "completion_tokens_details")
    if completion_details is None:
        completion_details = _read_value(usage, "completionTokensDetails")
    if completion_details is not None:
        reasoning_tokens = _first_int(completion_details, "reasoning_tokens", "reasoningTokenCount")
    if reasoning_tokens is None:
        output_token_details = _read_value(usage, "output_token_details")
        if output_token_details is None:
            output_token_details = _read_value(usage, "outputTokenDetails")
        if output_token_details is not None:
            reasoning_tokens = _first_int(output_token_details, "reasoning", "reasoning_tokens")
    if reasoning_tokens is None:
        reasoning_tokens = _first_int(usage, "thoughts_token_count", "thoughtsTokenCount")

    prompt_details = _read_value(usage, "prompt_tokens_details")
    if prompt_details is None:
        prompt_details = _read_value(usage, "promptTokensDetails")
    cached_input_tokens = None
    cache_write_tokens = None
    if prompt_details is not None:
        cached_input_tokens = _first_int(prompt_details, "cached_tokens", "cachedTokens")
        cache_write_tokens = _first_int(prompt_details, "cache_write_tokens", "cacheWriteTokens")
    if cached_input_tokens is None:
        cached_input_tokens = _first_int(
            usage,
            "cached_content_token_count",
            "cachedContentTokenCount",
        )

    cache_creation_input_tokens = _first_int(
        usage,
        "cache_creation_input_tokens",
        "cacheCreationInputTokens",
    )
    cache_read_input_tokens = _first_int(
        usage,
        "cache_read_input_tokens",
        "cacheReadInputTokens",
    )
    tool_use_prompt_tokens = _first_int(
        usage,
        "tool_use_prompt_token_count",
        "toolUsePromptTokenCount",
    )

    metrics: dict[str, int] = {}
    if prompt_tokens is not None:
        metrics["input_tokens"] = prompt_tokens
    if completion_tokens is not None:
        metrics["output_tokens"] = completion_tokens
    if total_tokens is not None:
        metrics["total_tokens"] = total_tokens
    if reasoning_tokens is not None:
        metrics["reasoning_tokens"] = reasoning_tokens
    if cached_input_tokens is not None:
        metrics["cached_input_tokens"] = cached_input_tokens
    if cache_write_tokens is not None:
        metrics["cache_write_tokens"] = cache_write_tokens
    if cache_creation_input_tokens is not None:
        metrics["cache_creation_input_tokens"] = cache_creation_input_tokens
    if cache_read_input_tokens is not None:
        metrics["cache_read_input_tokens"] = cache_read_input_tokens
    if tool_use_prompt_tokens is not None:
        metrics["tool_use_prompt_tokens"] = tool_use_prompt_tokens
    return metrics


def extract_refs(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        if "$ref" in value and isinstance(value["$ref"], str):
            refs.append(value["$ref"])
        for item in value.values():
            refs.extend(extract_refs(item))
        return refs
    if isinstance(value, list):
        for item in value:
            refs.extend(extract_refs(item))
    return refs


def normalize_refs(value: Any, id_by_index: dict[int, str]) -> Any:
    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if key == "$ref":
                if isinstance(item, int) and item in id_by_index:
                    normalized[key] = id_by_index[item]
                elif isinstance(item, str) and item.isdigit():
                    idx = int(item)
                    normalized[key] = id_by_index.get(idx, item)
                elif isinstance(item, str):
                    match = re.search(r"(\d+)$", item)
                    if match:
                        idx = int(match.group(1))
                        normalized[key] = id_by_index.get(idx, item)
                    else:
                        normalized[key] = item
                else:
                    normalized[key] = item
            else:
                normalized[key] = normalize_refs(item, id_by_index)
        return normalized
    if isinstance(value, list):
        return [normalize_refs(item, id_by_index) for item in value]
    return value


def safe_load_arguments(raw_args: str | None) -> dict[str, Any]:
    raw = raw_args or "{}"
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw_arguments": raw}
    if isinstance(parsed, dict):
        return parsed
    return {"_raw_arguments": raw}


def calls_to_dependency_batches(calls: list[ToolCall]) -> list[ToolBatch]:
    remaining: dict[str, ToolCall] = {call.id: call for call in calls}
    ordered_ids = [call.id for call in calls]
    done: set[str] = set()
    batches: list[ToolBatch] = []

    while remaining:
        ready_ids = [
            call_id
            for call_id in ordered_ids
            if call_id in remaining and all(dep in done for dep in remaining[call_id].depends_on)
        ]
        if not ready_ids:
            unresolved_calls = [remaining[call_id] for call_id in ordered_ids if call_id in remaining]
            batches.append(ToolBatch(mode="sequential", calls=unresolved_calls))
            break

        ready_calls = [remaining.pop(call_id) for call_id in ready_ids]
        mode = "parallel" if len(ready_calls) > 1 else "sequential"
        batches.append(ToolBatch(mode=mode, calls=ready_calls))
        done.update(ready_ids)

    return batches


def _message_content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    try:
        return json.dumps(content, default=str)
    except Exception:
        return str(content)


def _fetch_url_bytes(url: str) -> bytes | None:
    try:
        request = Request(url, headers={"User-Agent": "MTP-SDK/0.1"})
        with urlopen(request, timeout=20) as response:  # noqa: S310
            return response.read()
    except Exception:
        return None


def _guess_mime_from_path(path_or_name: str, default: str) -> str:
    guessed = mimetypes.guess_type(path_or_name)[0]
    return guessed or default


def _to_data_url(payload: bytes, mime_type: str) -> str:
    encoded = base64.b64encode(payload).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def _image_to_openai_part(image: Image) -> dict[str, Any] | None:
    if image.url:
        return {"type": "image_url", "image_url": {"url": image.url}}
    content = image.get_content_bytes()
    if content is None:
        return None
    mime_type = image.mime_type
    if mime_type is None:
        if image.format:
            mime_type = f"image/{image.format}"
        elif image.filepath:
            mime_type = _guess_mime_from_path(str(image.filepath), "image/jpeg")
        else:
            mime_type = "image/jpeg"
    image_url = _to_data_url(content, mime_type)
    part: dict[str, Any] = {"type": "image_url", "image_url": {"url": image_url}}
    if image.detail:
        part["image_url"]["detail"] = image.detail
    return part


def _audio_to_openai_part(audio: Audio) -> dict[str, Any] | None:
    content = audio.get_content_bytes()
    if content is None and audio.url:
        content = _fetch_url_bytes(audio.url)
    if content is None:
        return None
    audio_format = audio.format
    if audio_format is None:
        if audio.filepath:
            audio_format = Path(str(audio.filepath)).suffix.lstrip(".") or "wav"
        elif audio.mime_type and "/" in audio.mime_type:
            audio_format = audio.mime_type.split("/", 1)[1]
        else:
            audio_format = "wav"
    encoded = base64.b64encode(content).decode("utf-8")
    return {"type": "input_audio", "input_audio": {"data": encoded, "format": audio_format}}


def _file_to_openai_part(file: File) -> dict[str, Any] | None:
    if file.content is None and file.filepath is None and file.url is None:
        return None
    raw = file.get_content_bytes()
    if raw is None and file.url:
        raw = _fetch_url_bytes(file.url)
    if raw is None:
        return None
    filename = file.filename
    if filename is None and file.filepath is not None:
        filename = Path(str(file.filepath)).name
    if filename is None and file.url:
        filename = Path(file.url).name or "file"
    if filename is None:
        filename = "file"
    mime_type = file.mime_type or _guess_mime_from_path(filename, "application/octet-stream")
    data_url = _to_data_url(raw, mime_type)
    return {"type": "file", "file": {"filename": filename, "file_data": data_url}}


def format_openai_like_message(
    msg: dict[str, Any],
    *,
    allow_images: bool = True,
    allow_audio: bool = True,
    allow_video: bool = False,
    allow_files: bool = True,
) -> dict[str, Any] | None:
    role = msg.get("role")
    if role not in {"system", "user", "assistant", "tool"}:
        return None

    if role == "tool":
        return {
            "role": "tool",
            "tool_call_id": msg.get("tool_call_id"),
            "content": _message_content_text(msg.get("content", "")),
        }

    new_msg: dict[str, Any] = {"role": role, "content": msg.get("content") or ""}
    if "tool_calls" in msg:
        new_msg["tool_calls"] = msg["tool_calls"]

    media_parts: list[dict[str, Any]] = []
    images = msg.get("images") if isinstance(msg.get("images"), list) else None
    audios = msg.get("audios") if isinstance(msg.get("audios"), list) else None
    if audios is None and isinstance(msg.get("audio"), list):
        audios = msg.get("audio")
    videos = msg.get("videos") if isinstance(msg.get("videos"), list) else None
    files = msg.get("files") if isinstance(msg.get("files"), list) else None

    if allow_images and images:
        for image in images:
            if isinstance(image, Image):
                image_part = _image_to_openai_part(image)
                if image_part is not None:
                    media_parts.append(image_part)

    if allow_audio and audios:
        for audio in audios:
            if isinstance(audio, Audio):
                audio_part = _audio_to_openai_part(audio)
                if audio_part is not None:
                    media_parts.append(audio_part)

    if allow_video and videos:
        for video in videos:
            if isinstance(video, Video) and video.url:
                media_parts.append({"type": "text", "text": f"[video] {video.url}"})

    if allow_files and files:
        for file in files:
            if isinstance(file, File):
                file_part = _file_to_openai_part(file)
                if file_part is not None:
                    media_parts.append(file_part)

    if media_parts:
        text = _message_content_text(msg.get("content", ""))
        parts: list[dict[str, Any]] = [{"type": "text", "text": text}]
        parts.extend(media_parts)
        new_msg["content"] = parts
    return new_msg
