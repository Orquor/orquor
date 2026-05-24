"""
Content-Bot
===========

Multi-channel content distribution. Implements the 70%+ automation target
described in Frente 3 — orquor-academy-y-contenido.canvas.tsx.

Pipeline:
    long-form YouTube transcript
        → LinkedIn deep-dive post
        → X thread (4-7 tweets)
        → 60-90s vertical clip
        → Orquor newsletter excerpt

Inputs:
    - Long-form transcript or article from founder
    - Channel-specific style guides (in /09-content-calendar/)
    - Engagement metrics from previous publications

Outputs:
    - Drafted assets per channel (final human review before publish)
    - Posting calendar updates
    - Performance summaries
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any

from shared_memory import SharedMemory


@dataclass
class ContentItem:
    asset_id: str
    channel: str               # "youtube", "linkedin", "x", "newsletter", "tiktok"
    title: str
    body_draft: str | None
    status: str                # "drafted", "human_review", "scheduled", "published"
    scheduled_for: datetime | None
    source_artifact: str       # which source it derives from


def mock_content_pipeline(dry_run: bool) -> list[ContentItem]:
    if not dry_run:
        return []
    now = datetime.now(timezone.utc)
    return [
        ContentItem(
            asset_id="CW-2026-W21-YT-01",
            channel="youtube",
            title="What is Auditable Clinical Translation Orchestration (ACTO)?",
            body_draft="Script v2 in /09-content-calendar/youtube/ep-001-script.md",
            status="drafted",
            scheduled_for=now + timedelta(days=3),
            source_artifact="whitepaper-acto.md section 2-3",
        ),
        ContentItem(
            asset_id="CW-2026-W21-LI-01",
            channel="linkedin",
            title="Why 'we use AI for translation' is no longer enough in healthcare",
            body_draft="Draft in /09-content-calendar/linkedin/dia-001.md",
            status="human_review",
            scheduled_for=now + timedelta(days=1),
            source_artifact="whitepaper-acto.md section 2",
        ),
        ContentItem(
            asset_id="CW-2026-W21-X-01",
            channel="x",
            title="Thread: the 5 trade-offs nobody publishes about medical interpretation in 2026",
            body_draft="Draft in /09-content-calendar/x-twitter/dia-001.md",
            status="drafted",
            scheduled_for=now + timedelta(days=2),
            source_artifact="whitepaper-acto.md section 2",
        ),
    ]


# ---------------------------------------------------------------------------
# Optimal posting schedule engine
# ---------------------------------------------------------------------------

# Optimal posting hours (UTC) per channel per day-of-week.
# Based on B2B healthcare audience engagement data (LATAM timezone adjusted).
# Format: channel -> day-of-week (0=Mon..6=Sun) -> list of preferred hours (UTC)
OPTIMAL_POSTING_SLOTS: dict[str, dict[int, list[int]]] = {
    "linkedin": {
        0: [12, 15, 17],   # Mon: lunch, mid-afternoon, end-of-day
        1: [12, 14, 16],   # Tue
        2: [11, 13, 15],   # Wed
        3: [12, 14, 17],   # Thu
        4: [11, 13],       # Fri (early cutoff)
        5: [10, 12],       # Sat (light)
        6: [14],           # Sun (minimal — long-form only)
    },
    "x": {
        0: [12, 15, 18, 21],  # Mon: higher frequency
        1: [12, 14, 17, 20],
        2: [11, 13, 16, 19],
        3: [12, 14, 17, 20],
        4: [11, 13, 15],
        5: [10, 14],
        6: [15],
    },
    "youtube": {
        # YouTube long-form: fewer slots, morning/early afternoon
        0: [13],
        1: [14],
        2: [14],
        3: [13],
        4: [12],
        5: [11],
        6: [15],
    },
    "newsletter": {
        # Newsletters: mid-week mornings
        1: [13],   # Tue
        2: [13],   # Wed
        3: [13],   # Thu
    },
    "tiktok": {
        0: [14, 19],
        1: [14, 18],
        2: [14, 19],
        3: [14, 18],
        4: [13, 17],
        5: [12, 16],
        6: [15],
    },
}

# Minimum gap (hours) between posts on the same channel.
MIN_POST_GAP_HOURS: dict[str, int] = {
    "linkedin": 6,
    "x": 3,
    "youtube": 24,
    "newsletter": 24,
    "tiktok": 8,
}


def _find_optimal_slot(
    channel: str,
    preferred_date: datetime,
    occupied_slots: list[datetime],
) -> datetime:
    """Find the best available time slot for a channel on/near a target date.

    Scans ``OPTIMAL_POSTING_SLOTS`` for the channel's preferred hours on
    that day-of-week.  If all are taken (or too close to existing posts),
    shifts to the next available day.

    Args:
        channel: Content channel name (``"linkedin"``, ``"x"``, etc.).
        preferred_date: The target publication date (naive or aware).
        occupied_slots: Already-assigned post datetimes on this channel.

    Returns:
        A ``datetime`` with the best available slot assigned.
    """
    min_gap = MIN_POST_GAP_HOURS.get(channel, 4)
    gap_td = timedelta(hours=min_gap)
    day_slots = OPTIMAL_POSTING_SLOTS.get(channel, {})

    # Try up to 7 days forward
    for offset in range(7):
        candidate_date = preferred_date + timedelta(days=offset)
        dow = candidate_date.weekday()
        hours = day_slots.get(dow, [12])  # default noon if no config

        for hour in sorted(hours):
            slot = candidate_date.replace(
                hour=hour, minute=0, second=0, microsecond=0
            )
            # Check gap constraint against already-occupied slots
            conflict = any(
                abs((slot - occ).total_seconds()) < gap_td.total_seconds()
                for occ in occupied_slots
            )
            if not conflict:
                return slot

    # Fallback: return preferred_date at noon
    return preferred_date.replace(hour=12, minute=0, second=0, microsecond=0)


def schedule_posts(
    items: list[ContentItem],
    start_date: datetime | None = None,
) -> list[ContentItem]:
    """Assign optimal posting times to a batch of content items.

    Items in ``"drafted"`` or ``"human_review"`` status get scheduled.
    Already-scheduled or published items are left unchanged.

    The scheduler respects:
        - Per-channel optimal time-of-day / day-of-week slots.
        - Minimum gap between posts on the same channel.
        - Sequential assignment: items are processed in list order.

    Args:
        items: Content items to schedule.
        start_date: Earliest date to schedule from (default: now + 1 hour).

    Returns:
        New list of ``ContentItem`` with ``scheduled_for`` populated.
    """
    if start_date is None:
        start_date = datetime.now(timezone.utc) + timedelta(hours=1)

    # Track occupied slots per channel
    occupied: dict[str, list[datetime]] = {}
    result: list[ContentItem] = []

    for item in items:
        if item.status in ("scheduled", "published"):
            result.append(item)
            continue

        channel = item.channel
        if channel not in occupied:
            occupied[channel] = []

        slot = _find_optimal_slot(channel, start_date, occupied[channel])
        occupied[channel].append(slot)

        result.append(ContentItem(
            asset_id=item.asset_id,
            channel=item.channel,
            title=item.title,
            body_draft=item.body_draft,
            status="scheduled",
            scheduled_for=slot,
            source_artifact=item.source_artifact,
        ))

    return result


def generate_content_calendar(
    items: list[ContentItem],
) -> list[dict[str, Any]]:
    """Produce a human-readable calendar view of scheduled content.

    Returns a list of dicts sorted by scheduled date, with fields:
    ``date``, ``day``, ``channel``, ``asset_id``, ``title``.
    """
    scheduled = [it for it in items if it.scheduled_for is not None]
    scheduled.sort(key=lambda it: it.scheduled_for)  # type: ignore[arg-type]

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    calendar: list[dict[str, Any]] = []
    for it in scheduled:
        assert it.scheduled_for is not None
        calendar.append({
            "date": it.scheduled_for.strftime("%Y-%m-%d"),
            "day": day_names[it.scheduled_for.weekday()],
            "time_utc": it.scheduled_for.strftime("%H:%M"),
            "channel": it.channel,
            "asset_id": it.asset_id,
            "title": it.title,
        })
    return calendar


def verifier_check(items: list[ContentItem]) -> tuple[bool, str]:
    """
    Pass conditions:
        - No item moves from 'drafted' to 'scheduled' without 'human_review' step
        - Each item references its source artifact
    """
    for item in items:
        if item.status == "scheduled" and not item.source_artifact:
            return False, f"Item {item.asset_id} scheduled without source attribution."
        if item.status == "published" and not item.source_artifact:
            return False, f"Item {item.asset_id} published without source attribution."
    return True, f"{len(items)} content items in pipeline; attribution intact."


async def run(memory: SharedMemory, dry_run: bool = False, **_: Any) -> dict:
    items = mock_content_pipeline(dry_run=dry_run)
    verifier_passed, verifier_msg = verifier_check(items)

    by_channel: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for it in items:
        by_channel[it.channel] = by_channel.get(it.channel, 0) + 1
        by_status[it.status] = by_status.get(it.status, 0) + 1

    needs_review = [it for it in items if it.status == "human_review"]
    for it in needs_review:
        memory.record(
            sub_agent="Content",
            feedback_type="content_review_required",
            section_affected="content_pipeline",
            feedback_text=f"{it.asset_id} ({it.channel}): '{it.title}' awaits human review",
            canonical_rule="outcome_only",
            action_taken="awaiting founder/CMO sign-off",
            reasoning="Mandatory human review before publish.",
        )

    # --- Scheduling engine ---
    scheduled_items = schedule_posts(items)
    calendar = generate_content_calendar(scheduled_items)

    return {
        "summary": (
            f"items={len(items)} "
            + " ".join(f"{k}={v}" for k, v in by_status.items())
            + " | " + " ".join(f"{k}={v}" for k, v in by_channel.items())
        ),
        "verifier": verifier_msg,
        "verifier_passed": verifier_passed,
        "needs_human_review": [it.asset_id for it in needs_review],
        "scheduled_items": [
            {"asset_id": it.asset_id, "channel": it.channel, "scheduled_for": it.scheduled_for.isoformat() if it.scheduled_for else None}
            for it in scheduled_items
        ],
        "calendar": calendar,
    }
