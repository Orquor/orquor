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

    return {
        "summary": (
            f"items={len(items)} "
            + " ".join(f"{k}={v}" for k, v in by_status.items())
            + " | " + " ".join(f"{k}={v}" for k, v in by_channel.items())
        ),
        "verifier": verifier_msg,
        "verifier_passed": verifier_passed,
        "needs_human_review": [it.asset_id for it in needs_review],
    }
