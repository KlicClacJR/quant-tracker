"""Send one sample Discord alert (or dry-run preview) for quick webhook testing."""

from __future__ import annotations

import os
from datetime import date

from dotenv import load_dotenv

from notifier import send_discord_alert


def parse_bool_env(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def run() -> None:
    load_dotenv()

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    dry_run = parse_bool_env("DRY_RUN", default=False)

    sample_item = {
        "firm": "Sample Firm",
        "source": "Students",
        "type": "Internship",
        "title_or_snippet": "Quantitative Trader Internship - Undergraduate Program",
        "application_deadline": "April 1, 2026",
        "program_date_or_timeline": "10-week summer internship",
        "match_reason": "target quant/trading internship phrase; student/early-career signal",
        "url": "https://example.com/opportunity",
        "source_page_url": "https://example.com/students",
    }

    result = send_discord_alert(webhook_url, sample_item, date.today().isoformat(), dry_run=dry_run)

    if result["ok"] and result["sent"]:
        print("Webhook test sent successfully.")
        return

    if result["ok"] and result["dry_run"]:
        print("DRY_RUN=true; message preview below:\n")
        print(result["message"])
        return

    status = result.get("status_code")
    error = result.get("error", "Unknown error")
    print(f"Webhook test failed (status={status}): {error}")


if __name__ == "__main__":
    run()
