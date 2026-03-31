"""Simple JSON storage for seen opportunity tracking."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def ensure_seen_file(path: str) -> None:
    target = Path(path)
    if not target.exists():
        target.write_text("[]\n", encoding="utf-8")


def load_seen_items(path: str) -> list[dict[str, Any]]:
    ensure_seen_file(path)
    target = Path(path)

    try:
        content = target.read_text(encoding="utf-8").strip()
        if not content:
            return []
        data = json.loads(content)
    except (json.JSONDecodeError, OSError):
        return []

    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def save_seen_items(path: str, items: list[dict[str, Any]]) -> None:
    target = Path(path)
    target.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def stable_item_hash(firm: str, source: str, title_or_snippet: str, url: str) -> str:
    normalized = "|".join(
        [
            " ".join(firm.lower().split()),
            " ".join(source.lower().split()),
            " ".join(title_or_snippet.lower().split()),
            " ".join(url.lower().split()),
        ]
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def build_seen_hashes(items: list[dict[str, Any]]) -> set[str]:
    hashes: set[str] = set()
    for item in items:
        item_hash = item.get("hash")
        if isinstance(item_hash, str) and item_hash:
            hashes.add(item_hash)
    return hashes


def to_storage_item(item: dict[str, Any], item_hash: str, found_date: str, alerted: bool) -> dict[str, Any]:
    return {
        "firm": item["firm"],
        "source": item["source"],
        "source_page_url": item["source_page_url"],
        "title_or_snippet": item["title_or_snippet"],
        "url": item["url"],
        "hash": item_hash,
        "first_seen_date": found_date,
        "alerted": alerted,
        "match_reason": item.get("match_reason", ""),
        "type": item.get("type", "Opportunity"),
        "score": item.get("score", 0),
        "application_deadline": item.get("application_deadline", ""),
        "program_date_or_timeline": item.get("program_date_or_timeline", ""),
    }
