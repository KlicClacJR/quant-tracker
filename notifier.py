"""Discord webhook notification helpers."""

from __future__ import annotations

import time
from typing import Any

import requests

from config import SNIPPET_MAX_CHARS


def truncate_text(value: str, max_chars: int) -> str:
    text = " ".join(value.split())
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def build_discord_message(item: dict[str, Any], found_date: str) -> str:
    title_snippet = truncate_text(item.get("title_or_snippet", ""), SNIPPET_MAX_CHARS)
    reason = truncate_text(item.get("match_reason", "strict quant/student match"), 180)

    application_deadline = item.get("application_deadline", "") or "Not found"
    program_date_or_timeline = item.get("program_date_or_timeline", "") or "Not found"

    return (
        "🚨 NEW QUANT OPPORTUNITY\n\n"
        f"Firm: {item.get('firm', 'Unknown')}\n"
        f"Source: {item.get('source', 'Unknown')}\n"
        f"Type: {item.get('type', 'Opportunity')}\n"
        f"Title/Snippet: {title_snippet}\n\n"
        f"Application Deadline: {application_deadline}\n"
        f"Program Date / Timeline: {program_date_or_timeline}\n\n"
        f"Reason Matched: {reason}\n\n"
        "Opportunity URL:\n"
        f"{item.get('url', '')}\n\n"
        "Source Page:\n"
        f"{item.get('source_page_url', '')}\n\n"
        "Found:\n"
        f"{found_date}"
    )


def _parse_retry_after_seconds(response: requests.Response) -> float:
    try:
        payload = response.json()
    except ValueError:
        return 0.0

    retry_after = payload.get("retry_after", 0)
    if not isinstance(retry_after, (int, float)):
        return 0.0

    # Discord may return seconds; some endpoints may include millisecond-style values.
    if retry_after > 100:
        return min(retry_after / 1000.0, 30.0)

    return min(float(retry_after), 30.0)


def send_discord_alert(
    webhook_url: str,
    item: dict[str, Any],
    found_date: str,
    dry_run: bool = False,
    max_retries: int = 2,
) -> dict[str, Any]:
    """Send one alert message to Discord or return a dry-run preview."""
    message = build_discord_message(item, found_date)

    if dry_run:
        return {
            "ok": True,
            "sent": False,
            "dry_run": True,
            "message": message,
            "status_code": None,
            "error": "",
        }

    if not webhook_url:
        return {
            "ok": False,
            "sent": False,
            "dry_run": False,
            "message": message,
            "status_code": None,
            "error": "Missing DISCORD_WEBHOOK_URL",
        }

    payload = {
        "content": message,
        "allowed_mentions": {"parse": []},
    }

    for attempt in range(max_retries + 1):
        try:
            response = requests.post(webhook_url, json=payload, timeout=15)
        except requests.RequestException as exc:
            return {
                "ok": False,
                "sent": False,
                "dry_run": False,
                "message": message,
                "status_code": None,
                "error": str(exc),
            }

        if response.status_code in (200, 204):
            return {
                "ok": True,
                "sent": True,
                "dry_run": False,
                "message": message,
                "status_code": response.status_code,
                "error": "",
            }

        if response.status_code == 429 and attempt < max_retries:
            wait_seconds = _parse_retry_after_seconds(response)
            if wait_seconds > 0:
                time.sleep(wait_seconds)
            continue

        error_text = truncate_text(response.text or "Discord webhook request failed", 240)
        return {
            "ok": False,
            "sent": False,
            "dry_run": False,
            "message": message,
            "status_code": response.status_code,
            "error": error_text,
        }

    return {
        "ok": False,
        "sent": False,
        "dry_run": False,
        "message": message,
        "status_code": None,
        "error": "Failed to send Discord message after retries",
    }
