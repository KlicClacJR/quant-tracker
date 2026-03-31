"""Quant internship/program tracker MVP entrypoint."""

from __future__ import annotations

import os
from datetime import date

from dotenv import load_dotenv

from config import MAX_ALERTS_PER_RUN, MONITORED_SITES, SEEN_FILE_PATH
from filters import find_relevant_opportunities
from notifier import send_discord_alert
from scraper import scrape_page
from storage import build_seen_hashes, load_seen_items, save_seen_items, stable_item_hash, to_storage_item


def parse_bool_env(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def run() -> None:
    load_dotenv()

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    dry_run = parse_bool_env("DRY_RUN", default=False)
    max_alerts = MAX_ALERTS_PER_RUN

    found_date = date.today().isoformat()

    seen_items = load_seen_items(SEEN_FILE_PATH)
    seen_hashes = build_seen_hashes(seen_items)

    run_hashes: set[str] = set()
    new_items: list[dict] = []

    sites_checked = 0
    scrape_errors = 0
    relevant_count = 0

    print(f"[START] Loaded {len(seen_items)} seen items from {SEEN_FILE_PATH}.")
    print(f"[START] Checking {len(MONITORED_SITES)} sites. DRY_RUN={dry_run}. MAX_ALERTS_PER_RUN={max_alerts}\n")

    for index, site in enumerate(MONITORED_SITES, start=1):
        sites_checked += 1
        firm = site["firm"]
        source = site["source"]
        url = site["url"]

        print(f"[SITE {index}/{len(MONITORED_SITES)}] {firm} | {source}")
        scraped = scrape_page(url)

        if scraped["error"]:
            scrape_errors += 1
            print(f"  [ERROR] {scraped['error']}")
            continue

        relevant = find_relevant_opportunities(
            firm=firm,
            source=source,
            source_page_url=url,
            page_text=scraped["text"],
            links=scraped["links"],
        )
        relevant_count += len(relevant)

        new_from_site = 0
        for item in relevant:
            item_hash = stable_item_hash(
                firm=item["firm"],
                source=item["source"],
                title_or_snippet=item["title_or_snippet"],
                url=item["url"],
            )

            if item_hash in seen_hashes or item_hash in run_hashes:
                continue

            run_hashes.add(item_hash)
            item["hash"] = item_hash
            new_items.append(item)
            new_from_site += 1

        print(f"  [INFO] Relevant matches: {len(relevant)} | New this site: {new_from_site}")

    print(f"\n[INFO] New relevant items this run: {len(new_items)}")

    alerts_sent = 0
    alerts_previewed = 0
    alerts_skipped_cap = 0
    alerts_skipped_no_webhook = 0
    alerts_failed = 0
    warned_missing_webhook = False

    for idx, item in enumerate(new_items):
        alerted = False

        if idx >= max_alerts:
            alerts_skipped_cap += 1
            print(f"  [SKIP] Alert cap reached for {item['firm']} | {item['title_or_snippet'][:80]}")
            seen_items.append(to_storage_item(item, item["hash"], found_date, alerted=alerted))
            continue

        if not webhook_url and not dry_run:
            alerts_skipped_no_webhook += 1
            if not warned_missing_webhook:
                print("  [WARN] DISCORD_WEBHOOK_URL is empty; skipping alert sends.")
                warned_missing_webhook = True
            seen_items.append(to_storage_item(item, item["hash"], found_date, alerted=alerted))
            continue

        result = send_discord_alert(webhook_url, item, found_date, dry_run=dry_run)

        if result["ok"] and result["sent"]:
            alerts_sent += 1
            alerted = True
            print(f"  [ALERTED] {item['firm']} | {item['title_or_snippet'][:80]}")
        elif result["ok"] and result["dry_run"]:
            alerts_previewed += 1
            print(f"  [DRY-RUN] Would send alert for {item['firm']} | {item['title_or_snippet'][:80]}")
            print("  [DRY-RUN] Preview message:")
            print(result["message"])
            print("  [DRY-RUN] End preview\n")
        else:
            alerts_failed += 1
            status = result.get("status_code")
            error = result.get("error", "Unknown error")
            print(f"  [WARN] Alert failed for {item['firm']} (status={status}): {error}")

        seen_items.append(to_storage_item(item, item["hash"], found_date, alerted=alerted))

    save_seen_items(SEEN_FILE_PATH, seen_items)

    print("\n[SUMMARY]")
    print(f"Sites checked: {sites_checked}")
    print(f"Scrape errors: {scrape_errors}")
    print(f"Relevant matches found: {relevant_count}")
    print(f"New unique items found: {len(new_items)}")
    print(f"Alerts sent: {alerts_sent}")
    print(f"Dry-run previews: {alerts_previewed}")
    print(f"Alerts skipped (cap): {alerts_skipped_cap}")
    print(f"Alerts skipped (missing webhook): {alerts_skipped_no_webhook}")
    print(f"Alert failures: {alerts_failed}")
    print(f"History saved: {len(seen_items)} items in {SEEN_FILE_PATH}")


if __name__ == "__main__":
    run()
