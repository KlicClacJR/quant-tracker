"""Candidate extraction, relevance filtering, and timing metadata extraction."""

from __future__ import annotations

import re
from typing import Any

from config import (
    EVENT_TERMS,
    EXCLUDE_TERMS,
    FILTER_SCORE_THRESHOLD,
    GENERIC_TECH_TERMS,
    GENERIC_UNRELATED_TERMS,
    INTERNSHIP_SIGNAL_TERMS,
    KNOWN_STUDENT_PAGE_TERMS,
    PROGRAM_EVENT_SIGNAL_TERMS,
    PROGRAM_TERMS,
    QUANT_SIGNAL_TERMS,
    STUDENT_SIGNAL_TERMS,
    TARGET_PROGRAM_EVENT_PHRASES,
    TARGET_ROLE_PHRASES,
)

MONTH_NAME_PATTERN = (
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
)

DEADLINE_TRIGGERS = [
    "apply by",
    "application deadline",
    "deadline",
    "applications close",
    "apply before",
    "closes on",
    "due by",
]

TIMELINE_TRIGGERS = [
    "program dates",
    "event date",
    "summit date",
    "internship timeline",
    "begins",
    "starts on",
    "runs from",
    "over the course of",
]

DATE_PATTERN = re.compile(
    rf"(?i)\b{MONTH_NAME_PATTERN}\s+\d{{1,2}}(?:,\s*\d{{4}})?\b|\b\d{{1,2}}/\d{{1,2}}/\d{{2,4}}\b"
)
DATE_RANGE_PATTERN = re.compile(
    rf"(?i)\b(?:from\s+)?{MONTH_NAME_PATTERN}\s+\d{{1,2}}(?:,\s*\d{{4}})?"
    rf"\s*(?:-|–|—|to|through)\s*(?:{MONTH_NAME_PATTERN}\s+)?\d{{1,2}}(?:,\s*\d{{4}})?\b"
)
WEEK_OF_PATTERN = re.compile(rf"(?i)\bweek of\s+{MONTH_NAME_PATTERN}\s+\d{{1,2}}(?:,\s*\d{{4}})?\b")
DURATION_PATTERN = re.compile(
    r"(?i)\b(?:one[-\s]?week[^,.;\n]{0,80}|"
    r"\d+\s*[- ]?(?:day|days|week|weeks|month|months)\b[^,.;\n]{0,80}|"
    r"over the course of[^,.;\n]{0,80}|"
    r"a few days\b[^,.;\n]{0,60})"
)

DEADLINE_CAPTURE_PATTERN = re.compile(
    r"(?i)\b(?:apply by|application deadline|deadline|applications close|apply before|closes on|due by)\b"
    r"\s*[:\-]?\s*(.{1,140})"
)
TIMELINE_CAPTURE_PATTERN = re.compile(
    r"(?i)\b(?:program dates|event date|summit date|internship timeline|begins|starts on|runs from|"
    r"over the course of)\b\s*[:\-]?\s*(.{1,160})"
)


def normalize(value: str) -> str:
    return " ".join(value.lower().split())


def clean_capture(value: str) -> str:
    cleaned = " ".join(value.split()).strip(" -:|;,.\t")
    return cleaned[:200]


def term_in_text(text: str, term: str) -> bool:
    escaped = re.escape(term)
    pattern = rf"(?<!\w){escaped}(?!\w)"
    return re.search(pattern, text) is not None


def contains_any(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term_in_text(text, term)]


def has_any_signal(text: str) -> bool:
    return bool(
        contains_any(text, QUANT_SIGNAL_TERMS)
        or contains_any(text, STUDENT_SIGNAL_TERMS)
        or contains_any(text, TARGET_ROLE_PHRASES)
        or contains_any(text, TARGET_PROGRAM_EVENT_PHRASES)
    )


def classify_opportunity(text: str) -> str:
    text_lower = normalize(text)

    if contains_any(text_lower, INTERNSHIP_SIGNAL_TERMS):
        return "Internship"

    if contains_any(text_lower, EVENT_TERMS):
        return "Event"

    if contains_any(text_lower, PROGRAM_TERMS):
        return "Program"

    return "Opportunity"


def is_known_student_context(source: str, page_url: str) -> bool:
    context = normalize(f"{source} {page_url}")
    return any(term in context for term in KNOWN_STUDENT_PAGE_TERMS)


def score_candidate(candidate_text: str, source: str, page_url: str) -> dict[str, Any]:
    """Return strict keyword-based relevance scoring details for one snippet."""
    text = normalize(candidate_text)

    matched_target_roles = contains_any(text, TARGET_ROLE_PHRASES)
    matched_target_programs = contains_any(text, TARGET_PROGRAM_EVENT_PHRASES)
    matched_quant = contains_any(text, QUANT_SIGNAL_TERMS)
    matched_student = contains_any(text, STUDENT_SIGNAL_TERMS)
    matched_internship = contains_any(text, INTERNSHIP_SIGNAL_TERMS)
    matched_program_event = contains_any(text, PROGRAM_EVENT_SIGNAL_TERMS)

    matched_excludes = contains_any(text, EXCLUDE_TERMS)
    matched_generic_unrelated = contains_any(text, GENERIC_UNRELATED_TERMS)
    matched_generic_tech = contains_any(text, GENERIC_TECH_TERMS)

    known_student_context = is_known_student_context(source, page_url)

    has_quant_signal = bool(matched_quant or matched_target_roles or matched_target_programs)
    has_student_signal = bool(matched_student or matched_internship or matched_program_event)
    has_target_phrase = bool(matched_target_roles or matched_target_programs)

    has_internship_signal = bool(matched_internship)
    has_program_event_signal = bool(matched_program_event or matched_target_programs)

    generic_tech_without_quant = bool(matched_generic_tech and not has_quant_signal)
    hard_excluded = bool(matched_excludes or matched_generic_unrelated or generic_tech_without_quant)

    role_match = has_target_phrase and has_student_signal
    core_match = has_quant_signal and has_student_signal and (has_internship_signal or has_program_event_signal)
    student_context_match = (
        known_student_context and has_quant_signal and has_student_signal and (has_internship_signal or has_program_event_signal)
    )

    score = 0
    if has_target_phrase:
        score += 5
    if has_quant_signal:
        score += 3
    if has_student_signal:
        score += 2
    if has_internship_signal:
        score += 1
    if has_program_event_signal:
        score += 1
    if known_student_context:
        score += 1
    if hard_excluded:
        score -= 6

    passes_logic = role_match or core_match or student_context_match
    is_relevant = passes_logic and not hard_excluded and score >= FILTER_SCORE_THRESHOLD

    reason_parts = []
    if matched_target_roles:
        reason_parts.append("target quant/trading internship phrase")
    if matched_target_programs:
        reason_parts.append("target student program/event phrase")
    if matched_quant:
        reason_parts.append("quant/trading signal")
    if matched_student:
        reason_parts.append("student/early-career signal")
    if matched_excludes:
        reason_parts.append("excluded role keywords")
    if matched_generic_unrelated:
        reason_parts.append("generic unrelated internship")
    if generic_tech_without_quant:
        reason_parts.append("generic software internship without quant signal")

    return {
        "is_relevant": is_relevant,
        "score": score,
        "reason": "; ".join(reason_parts) if reason_parts else "strict quant/student match",
        "classification": classify_opportunity(candidate_text),
        "matched_excludes": matched_excludes,
    }


def build_page_lines(page_text: str) -> list[str]:
    lines: list[str] = []
    for raw_line in page_text.split("\n"):
        line = " ".join(raw_line.split())
        if line:
            lines.append(line)
    return lines


def find_line_index(page_lines: list[str], snippet: str) -> int:
    target = normalize(snippet)
    if not target:
        return -1

    for idx, line in enumerate(page_lines):
        if normalize(line) == target:
            return idx

    for idx, line in enumerate(page_lines):
        if target in normalize(line):
            return idx

    return -1


def extract_candidates(page_lines: list[str], links: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Build candidate snippets from page text lines and anchor texts."""
    candidates: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str]] = set()

    for idx, line in enumerate(page_lines):
        if len(line) < 24 or len(line) > 280:
            continue

        if not has_any_signal(normalize(line)):
            continue

        key = (line.lower(), "")
        if key in seen_keys:
            continue

        seen_keys.add(key)
        candidates.append({"snippet": line, "url": "", "candidate_type": "text", "line_index": idx})

    for link in links:
        anchor_text = " ".join(link.get("text", "").split())
        href = " ".join(link.get("url", "").split())

        if not href:
            continue

        if not anchor_text:
            anchor_text = href

        if len(anchor_text) > 220:
            anchor_text = anchor_text[:220]

        if not has_any_signal(normalize(anchor_text)):
            continue

        key = (anchor_text.lower(), href.lower())
        if key in seen_keys:
            continue

        seen_keys.add(key)
        candidates.append(
            {
                "snippet": anchor_text,
                "url": href,
                "candidate_type": "link",
                "line_index": find_line_index(page_lines, anchor_text),
            }
        )

    return candidates


def build_context_lines(candidate: dict[str, Any], page_lines: list[str], window: int = 3) -> list[str]:
    context_lines: list[str] = []
    seen: set[str] = set()

    def add_line(line: str) -> None:
        normalized = normalize(line)
        if not normalized or normalized in seen:
            return
        seen.add(normalized)
        context_lines.append(line)

    add_line(candidate.get("snippet", ""))

    line_index = candidate.get("line_index", -1)
    if isinstance(line_index, int) and 0 <= line_index < len(page_lines):
        start = max(0, line_index - window)
        end = min(len(page_lines), line_index + window + 1)
        for idx in range(start, end):
            add_line(page_lines[idx])

    return context_lines


def extract_date_value(text: str) -> str:
    for pattern in [DATE_RANGE_PATTERN, WEEK_OF_PATTERN, DATE_PATTERN]:
        match = pattern.search(text)
        if match:
            return clean_capture(match.group(0))
    return ""


def extract_timeline_value(text: str) -> str:
    for pattern in [DATE_RANGE_PATTERN, WEEK_OF_PATTERN, DATE_PATTERN, DURATION_PATTERN]:
        match = pattern.search(text)
        if match:
            return clean_capture(match.group(0))
    return ""


def has_trigger(line: str, triggers: list[str]) -> bool:
    line_lower = normalize(line)
    return any(term_in_text(line_lower, trigger) for trigger in triggers)


def extract_application_deadline(context_lines: list[str]) -> str:
    for idx, line in enumerate(context_lines):
        if not has_trigger(line, DEADLINE_TRIGGERS):
            continue

        inline = DEADLINE_CAPTURE_PATTERN.search(line)
        if inline:
            captured = clean_capture(inline.group(1))
            date_candidate = extract_date_value(captured)
            if date_candidate:
                return date_candidate

        date_in_line = extract_date_value(line)
        if date_in_line:
            return date_in_line

        if idx + 1 < len(context_lines):
            date_next_line = extract_date_value(context_lines[idx + 1])
            if date_next_line:
                return date_next_line

    return ""


def extract_program_date_or_timeline(context_lines: list[str]) -> str:
    for idx, line in enumerate(context_lines):
        line_has_timeline_trigger = has_trigger(line, TIMELINE_TRIGGERS)
        has_duration_signal = DURATION_PATTERN.search(line) is not None
        has_explicit_timeline_shape = DATE_RANGE_PATTERN.search(line) is not None or WEEK_OF_PATTERN.search(line) is not None

        if not line_has_timeline_trigger and not has_duration_signal and not has_explicit_timeline_shape:
            continue

        if line_has_timeline_trigger:
            inline = TIMELINE_CAPTURE_PATTERN.search(line)
            if inline:
                captured = clean_capture(inline.group(1))
                timeline_candidate = extract_timeline_value(captured)
                if timeline_candidate:
                    return timeline_candidate
                if captured:
                    return captured

        timeline_in_line = extract_timeline_value(line)
        if timeline_in_line:
            return timeline_in_line

        if line_has_timeline_trigger and idx + 1 < len(context_lines):
            timeline_next_line = extract_timeline_value(context_lines[idx + 1])
            if timeline_next_line:
                return timeline_next_line

    return ""


def extract_timing_metadata(candidate: dict[str, Any], page_lines: list[str]) -> dict[str, str]:
    context_lines = build_context_lines(candidate, page_lines)
    application_deadline = extract_application_deadline(context_lines)
    program_date_or_timeline = extract_program_date_or_timeline(context_lines)

    return {
        "application_deadline": application_deadline,
        "program_date_or_timeline": program_date_or_timeline,
    }


def dedupe_relevant_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Prefer one high-quality alert per opportunity URL/type within a page."""
    deduped: dict[tuple[str, str], dict[str, Any]] = {}

    for item in items:
        key = (normalize(item["url"]), normalize(item["type"]))
        current = deduped.get(key)

        if current is None:
            deduped[key] = item
            continue

        current_score = int(current.get("score", 0))
        new_score = int(item.get("score", 0))

        if new_score > current_score:
            deduped[key] = item
            continue

        if new_score == current_score and len(item["title_or_snippet"]) < len(current["title_or_snippet"]):
            deduped[key] = item

    return list(deduped.values())


def find_relevant_opportunities(
    firm: str,
    source: str,
    source_page_url: str,
    page_text: str,
    links: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Return relevant candidate opportunities for one page."""
    relevant: list[dict[str, Any]] = []
    page_lines = build_page_lines(page_text)
    candidates = extract_candidates(page_lines, links)

    for candidate in candidates:
        snippet = candidate["snippet"]
        scoring = score_candidate(snippet, source, source_page_url)
        if not scoring["is_relevant"]:
            continue

        timing = extract_timing_metadata(candidate, page_lines)

        relevant.append(
            {
                "firm": firm,
                "source": source,
                "source_page_url": source_page_url,
                "title_or_snippet": snippet,
                "url": candidate["url"] or source_page_url,
                "match_reason": scoring["reason"],
                "score": scoring["score"],
                "type": scoring["classification"],
                "application_deadline": timing["application_deadline"],
                "program_date_or_timeline": timing["program_date_or_timeline"],
            }
        )

    return dedupe_relevant_items(relevant)
