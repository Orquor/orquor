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


# ---------------------------------------------------------------------------
# Multi-dimensional candidate scoring & filtering
# ---------------------------------------------------------------------------

# Weight configuration for candidate evaluation.
# Tune based on role requirements (medical interpreters).
CANDIDATE_SCORING_WEIGHTS = {
    "english": 0.40,          # English proficiency (video screening)
    "medical_bg": 0.25,       # Medical background / domain knowledge
    "spanish_native": 0.15,   # Native Spanish speaker
    "video_submitted": 0.10,  # Has submitted video screening
    "freshness": 0.10,        # How recently the candidate was active
}

# Minimum composite score to auto-advance (if above).
AUTO_ADVANCE_THRESHOLD = 0.72

# Maximum composite score that still triggers auto-reject.
AUTO_REJECT_THRESHOLD = 0.38

# CV keyword signals for medical-background strength
MEDICAL_CV_KEYWORDS: list[str] = [
    "enfermer", "nurs", "medic", "doctor", "physician", "clinical",
    "hospital", "patient", "paciente", "healthcare", "salud",
    "pharma", "farmac", "therapy", "terapia", "diagnos",
    "interpreter", "interprete", "translation", "traduccion",
    "bilingual", "bilingue", "certified", "certificado",
]


def _english_score(score: float | None) -> float:
    """Normalise English screening score to 0-1.  None = 0."""
    if score is None:
        return 0.0
    return max(0.0, min(1.0, score))


def _medical_background_score(has_bg: bool) -> float:
    """Binary medical background → 0.0 or 1.0."""
    return 1.0 if has_bg else 0.0


def _spanish_native_score(is_native: bool) -> float:
    """Native Spanish → full points."""
    return 1.0 if is_native else 0.3


def _video_submitted_score(video_url: str | None) -> float:
    """Submitted video screening → 1.0, otherwise 0.0."""
    return 1.0 if video_url else 0.0


def _freshness_score(last_update: datetime) -> float:
    """Score based on how recently the candidate record was updated.

    Fresh (< 3 days) = 1.0, decays to 0.2 at 30+ days.
    """
    age_days = (datetime.now(timezone.utc) - last_update).days
    if age_days < 0:
        return 1.0
    if age_days <= 3:
        return 1.0
    if age_days <= 7:
        return 0.85
    if age_days <= 14:
        return 0.60
    if age_days <= 30:
        return 0.35
    return 0.20


def score_candidate(c: Candidate) -> float:
    """Compute a composite candidate score (0.0–1.0) across five dimensions.

    Dimensions:
        - **english**: English proficiency from video screening (0-1 normalised).
        - **medical_bg**: Whether the candidate has a medical/healthcare background.
        - **spanish_native**: Native Spanish speaker (critical for medical interpreting).
        - **video_submitted**: Has the candidate completed the video screening step.
        - **freshness**: Recency of candidate activity (decay curve).

    Used by ``filter_candidates`` and ``rank_candidates``.
    """
    scores = {
        "english": _english_score(c.english_screening_score),
        "medical_bg": _medical_background_score(c.medical_background),
        "spanish_native": _spanish_native_score(c.spanish_native),
        "video_submitted": _video_submitted_score(c.video_screening_url),
        "freshness": _freshness_score(c.last_update),
    }
    composite = sum(
        CANDIDATE_SCORING_WEIGHTS[dim] * scores[dim]
        for dim in CANDIDATE_SCORING_WEIGHTS
    )
    return round(composite, 4)


def filter_candidates(
    candidates: list[Candidate],
    min_score: float | None = None,
    require_medical: bool = False,
    require_video: bool = False,
) -> list[Candidate]:
    """Filter candidates by composite score and mandatory criteria.

    Args:
        candidates: Full pipeline list.
        min_score: Minimum composite score (defaults to ``AUTO_ADVANCE_THRESHOLD``).
        require_medical: If True, only keep candidates with medical background.
        require_video: If True, only keep candidates who submitted video.

    Returns:
        Filtered list of candidates that pass all criteria.
    """
    threshold = min_score if min_score is not None else AUTO_ADVANCE_THRESHOLD
    result: list[Candidate] = []
    for c in candidates:
        if score_candidate(c) < threshold:
            continue
        if require_medical and not c.medical_background:
            continue
        if require_video and not c.video_screening_url:
            continue
        result.append(c)
    return result


def rank_candidates(candidates: list[Candidate]) -> list[tuple[Candidate, float]]:
    """Return candidates sorted by composite score (highest first).

    Each element is ``(candidate, score)``.  Use this to prioritise
    interview scheduling and human review.
    """
    scored = [(c, score_candidate(c)) for c in candidates]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored


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

    # --- Candidate scoring, filtering & ranking ---
    ranked = rank_candidates(updated)
    top_candidates = [
        {"candidate_id": c.candidate_id, "name": c.name, "score": s, "status": c.status}
        for c, s in ranked
    ]

    # Filter-ready shortlist (medical + video required)
    interview_ready = filter_candidates(
        updated, require_medical=True, require_video=True
    )

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
        "candidate_scores": {c.candidate_id: score_candidate(c) for c in updated},
        "top_candidates": top_candidates,
        "interview_ready": [c.candidate_id for c in interview_ready],
    }
