# Quant Opportunity Tracker (MVP)

This bot checks a list of finance/trading firm pages for **quant/trading/research internships, student programs, and early-career events**, then alerts a Discord channel only for **new** high-signal matches.

## What The Bot Does
- Loads monitored firm URLs from `config.py`.
- Scrapes visible page text + links with `requests` and `BeautifulSoup`.
- Applies strict keyword filtering to prioritize high-quality quant/student opportunities and reduce noise.
- Extracts explicit timing metadata when present:
  - `application_deadline`
  - `program_date_or_timeline`
- Deduplicates with stable hashes and saves history in `seen.json`.
- Sends clean Discord webhook alerts with mention-safe payloads.
- Supports `DRY_RUN` so you can test without posting.
- Limits webhook floods with `MAX_ALERTS_PER_RUN` (still saves all findings to history).

## Files
- `main.py` - run-once bot pipeline.
- `config.py` - monitored URLs, filtering terms, score threshold, alert cap.
- `scraper.py` - HTTP fetch + page extraction.
- `filters.py` - relevance scoring + deadline/timeline extraction.
- `storage.py` - JSON history handling.
- `notifier.py` - Discord message formatting + webhook send logic.
- `test_webhook.py` - send one sample alert (or dry-run preview) without scraping.
- `.env.example` - environment template.
- `seen.json` - auto-created history file.

## Setup
1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env`:

```bash
cp .env.example .env
```

3. Set values in `.env`:

```env
DISCORD_WEBHOOK_URL=
DRY_RUN=false
```

### DRY_RUN behavior
- `DRY_RUN=true`: the bot prints the exact Discord message it **would** send and does not post.
- `DRY_RUN=false`: the bot posts to the webhook normally.

## Run
```bash
python main.py
```

The script runs once and exits.

## Quick Webhook Test (No Scraping)
```bash
python test_webhook.py
```

Useful to verify webhook formatting and env setup quickly.

## Reset `seen.json`
If you want the bot to treat everything as new again:

```bash
rm -f seen.json
```

On next run, it will recreate `seen.json` automatically.

Alternative non-destructive reset:

```bash
echo "[]" > seen.json
```

## Daily Automation on macOS (cron)
Example: run every day at 8:00 AM

```cron
0 8 * * * cd /Users/emmetsurmeli/Desktop/quant_tracker && /usr/bin/python3 main.py >> bot.log 2>&1
```

## Tuning
- Edit monitored pages in `MONITORED_SITES` (`config.py`).
- Tighten/relax filters in `config.py` and scoring logic in `filters.py`.
- Change flood safeguard with `MAX_ALERTS_PER_RUN` in `config.py`.

## Limitations
- `requests` scraping can miss jobs loaded only via JavaScript.
- Deadline/timeline extraction is regex + nearby-line heuristic (MVP), so it only captures explicitly present patterns.
- Some pages may still require manual checking even with strict filtering.

## Stored Fields (`seen.json`)
Each record includes:
- `firm`, `source`, `source_page_url`
- `title_or_snippet`, `url`, `hash`
- `first_seen_date`, `alerted`
- `match_reason`, `type`, `score`
- `application_deadline`
- `program_date_or_timeline`
