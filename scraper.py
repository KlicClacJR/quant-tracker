"""Page scraping helpers using requests + BeautifulSoup."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS, USER_AGENT


def clean_line(value: str) -> str:
    """Normalize whitespace in one line of text."""
    return " ".join(value.split())


def scrape_page(url: str) -> dict[str, Any]:
    """Fetch page HTML and extract visible text + links.

    Returns:
        {
            "url": str,
            "text": str,
            "links": list[dict[str, str]],
            "status_code": int | None,
            "error": str | None,
        }
    """
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
        status_code = response.status_code
        response.raise_for_status()
    except requests.RequestException as exc:
        return {
            "url": url,
            "text": "",
            "links": [],
            "status_code": getattr(getattr(exc, "response", None), "status_code", None),
            "error": str(exc),
        }

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "template"]):
        tag.extract()

    raw_text = soup.get_text(separator="\n")
    normalized_lines = [clean_line(line) for line in raw_text.splitlines()]
    text = "\n".join(line for line in normalized_lines if line)

    links: list[dict[str, str]] = []
    for anchor in soup.find_all("a", href=True):
        href = clean_line(anchor.get("href", ""))
        if not href:
            continue
        absolute_url = urljoin(url, href)
        anchor_text = clean_line(anchor.get_text(" ", strip=True))
        if not anchor_text and not absolute_url:
            continue
        links.append({"text": anchor_text, "url": absolute_url})

    return {
        "url": url,
        "text": text,
        "links": links,
        "status_code": status_code,
        "error": None,
    }
