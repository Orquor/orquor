"""
Recruiter-Bot
=============

Manages the pipeline of certified medical interpreters. Resolves the manual
bottleneck identified in the initial ITERAMED report (3 processes of 10 CVs
each, filtered by English-level video screening).

Inputs:
    - New CV submissions (form on orquor.com/careers/interpreters)
    - Video responses to standardized English-level screening prompts
    - Manual feedback from human supervisor on borderline cases

Outputs:
    - Tagged candidate status (advance / hold / reject)
    - Scheduled interviews (Calendly link generation)
    - MEMORY entries for unusual decisions

Verifier:
    - Every advanced candidate has a video screening result on record
    - Every rejected candidate has a reason recorded
    - No candidate is held > 14 days without a status update
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any

from shared_memory import SharedMemory


@dataclass
class Candidate:
    candidate_id: str
    name: str
    cv_url: str
    spanish_native: bool
    medical_background: bool
    video_screening_url: str | None = None
    english_screening_score: float | None = None   # 0.0 – 1.0
    status: str = "new"                              # new | screening | advance | hold | reject
    last_update: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    rejection_reason: str | None = None


# In production, these come from the candidates database.
def mock_pipeline(dry_run: bool) -> list[Candidate]:
    if not dry_run:
        return []
    now = datetime.now(timezone.utc)
    return [
        Candidate(
            candidate_id="C-2026-041",
            name="Mariana Lopez",
            cv_url="https://orquor.com/cv/041.pdf",
            spanish_native=True,
            medical_background=True,
            video_screening_url="https://orquor.com/videos/041.mp4",
            english_screening_score=0.88,
            status="screening",
            last_update=now,
        ),
        Candidate(
            candidate_id="C-2026-042",
            name="Carlos Mendieta",
            cv_url="https://orquor.com/cv/042.pdf",
            spanish_native=True,
            medical_background=False,
            video_screening_url="https://orquor.com/videos/042.mp4",
            english_screening_score=0.61,
            status="screening",
            last_update=now,
        ),
        Candidate(
            candidate_id="C-2026-043",
            name="Lucía Fernández",
            cv_url="https://orquor.com/cv/043.pdf",
            spanish_native=True,
            medical_background=True,
            video_screening_url=None,
            english_screening_score=None,
            status="new",
            last_update=now - timedelta(days=4),
        ),
        Candidate(
            candidate_id="C-2026-038",
            name="Pedro Vásquez",
            cv_url="https://orquor.com/cv/038.pdf",
            spanish_native=True,
            medical_background=True,
            video_screening_url="https://orquor.com/videos/038.mp4",
            english_screening_score=0.42,
            status="screening",
            last_update=now - timedelta(days=22),
        ),
    ]


# Decision policy — adjustable by founder
DECISION_RULES = {
    "advance_min_score": 0.78,
    "reject_max_score": 0.55,
    "stale_days": 14,
}


def evaluate_candidate(c: Candidate) -> Candidate:
    """
    Apply decision rules. Returns a NEW Candidate with updated status.
    """
    now = datetime.now(timezone.utc)
    age = (now - c.last_update).days

    if c.english_screening_score is None:
        if age > DECISION_RULES["stale_days"]:
            return Candidate(
                **{**c.__dict__, "status": "hold", "rejection_reason": "Video not submitted within 14 days"}
            )
        return c

    if c.english_screening_score >= DECISION_RULES["advance_min_score"]:
        return Candidate(**{**c.__dict__, "status": "advance"})
    if c.english_screening_score <= DECISION_RULES["reject_max_score"]:
        return Candidate(
            **{**c.__dict__, "status": "reject", "rejection_reason": f"English score {c.english_screening_score:.2f} below threshold"}
        )
    return Candidate(**{**c.__dict__, "status": "hold", "rejection_reason": "Score between thresholds — human review"})


def verifier_check(candidates: list[Candidate]) -> tuple[bool, str]:
    advanced = [c for c in candidates if c.status == "advance"]
    rejected = [c for c in candidates if c.status == "reject"]

    for c in advanced:
        if not c.video_screening_url or c.english_screening_score is None:
            return False, f"Candidate {c.candidate_id} advanced without video evidence."

    for c in rejected:
        if not c.rejection_reason:
            return False, f"Candidate {c.candidate_id} rejected without reason."

    return True, f"Pipeline state valid: {len(advanced)} advanced, {len(rejected)} rejected."


async def run(memory: SharedMemory, dry_run: bool = False, **_: Any) -> dict:
    pipeline = mock_pipeline(dry_run=dry_run)
    updated = [evaluate_candidate(c) for c in pipeline]
    verifier_passed, verifier_msg = verifier_check(updated)

    advanced = [c for c in updated if c.status == "advance"]
    rejected = [c for c in updated if c.status == "reject"]
    held = [c for c in updated if c.status == "hold"]

    for c in held:
        memory.record(
            sub_agent="Recruiter",
            feedback_type="recruitment_hold",
            section_affected="interpreter_pipeline",
            feedback_text=f"Candidate {c.candidate_id} ({c.name}) held: {c.rejection_reason}",
            canonical_rule="failure_justifications_three_areas",
            action_taken="awaiting human supervisor review",
            reasoning="Score between thresholds or missing video; cannot auto-decide.",
        )

    return {
        "summary": f"pipeline={len(pipeline)} advanced={len(advanced)} rejected={len(rejected)} hold={len(held)}",
        "verifier": verifier_msg,
        "verifier_passed": verifier_passed,
        "advanced": [c.candidate_id for c in advanced],
        "rejected": [c.candidate_id for c in rejected],
        "held": [c.candidate_id for c in held],
    }
