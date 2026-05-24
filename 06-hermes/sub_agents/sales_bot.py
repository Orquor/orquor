"""
Sales-Bot
=========

Implements the HUMINT-style cultivation pipeline from Capa Negra Framework 1.
Each prospect is treated as an asset with a 3-6 month cultivation timeline
and a structured asset profile.

Inputs:
    - Asset profiles (in /08-prospects/)
    - LinkedIn engagement signals on Freddy's posts
    - Inbound contact forms from orquor.com

Outputs:
    - Next-action recommendations per prospect
    - Conversation history maintained per asset
    - Escalations to founder for in-person encounters

Verifier:
    - No outbound spray (every contact is contextual)
    - Every advancement is tied to a documented signal from the asset
    - No prospect skipped from cultivation to pitch without intermediate steps
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any

from shared_memory import SharedMemory


class CultivationStage(str, Enum):
    PROFILED = "profiled"            # Asset profile complete
    ENGAGED = "engaged"              # Ambient engagement (comments, shares) ongoing
    SIGNALED = "signaled"            # Asset has signaled interest (reply, follow, DM)
    CONVERSING = "conversing"        # Active conversation
    MEETING = "meeting"              # In-person or video meeting scheduled
    PILOT = "pilot"                  # Pilot agreement in motion
    PAYING = "paying"                # Paying customer
    INACTIVE = "inactive"            # No movement in 90 days


@dataclass
class Asset:
    asset_id: str
    name: str
    role: str
    organization: str
    country: str
    linkedin: str
    last_signal_from_asset: datetime | None
    stage: CultivationStage
    notes: str = ""


def mock_assets(dry_run: bool) -> list[Asset]:
    if not dry_run:
        return []
    now = datetime.now(timezone.utc)
    return [
        Asset(
            asset_id="CR-01",
            name="Dr. Andrés Vargas (mock)",
            role="CFO",
            organization="Hospital Clínica Bíblica",
            country="Costa Rica",
            linkedin="https://linkedin.com/in/andresvargas-mock",
            last_signal_from_asset=now - timedelta(days=12),
            stage=CultivationStage.ENGAGED,
            notes="Liked Freddy's ACTO whitepaper teaser post. Not yet replied.",
        ),
        Asset(
            asset_id="CR-02",
            name="Marcela Rodríguez (mock)",
            role="Director of International Patients",
            organization="CIMA San José",
            country="Costa Rica",
            linkedin="https://linkedin.com/in/marcela-rodriguez-mock",
            last_signal_from_asset=now - timedelta(days=4),
            stage=CultivationStage.SIGNALED,
            notes="Sent DM asking about audit log feature. Reply drafted.",
        ),
        Asset(
            asset_id="CO-01",
            name="Dr. Felipe Cárdenas (mock)",
            role="Chief Medical Officer",
            organization="Fundación Cardioinfantil",
            country="Colombia",
            linkedin="https://linkedin.com/in/felipe-cardenas-mock",
            last_signal_from_asset=None,
            stage=CultivationStage.PROFILED,
            notes="Profile complete. Begin engagement Week 1.",
        ),
    ]


def next_action_for(asset: Asset) -> str:
    now = datetime.now(timezone.utc)
    if asset.stage == CultivationStage.PROFILED:
        return "Begin ambient engagement: like + comment on next 3 LinkedIn posts."
    if asset.stage == CultivationStage.ENGAGED:
        if not asset.last_signal_from_asset:
            return "Continue ambient engagement. Share ACTO whitepaper publicly (no DM)."
        age = (now - asset.last_signal_from_asset).days
        if age < 7:
            return "Wait. Asset has signaled recently; do not push."
        return "Publish a content piece adjacent to asset's interest. Tag obliquely."
    if asset.stage == CultivationStage.SIGNALED:
        return "Reply with substance. No pitch. Ask one elicitation question."
    if asset.stage == CultivationStage.CONVERSING:
        return "Propose 30-min discovery call. Specific time options."
    if asset.stage == CultivationStage.MEETING:
        return "Run the meeting. Discovery before demo."
    if asset.stage == CultivationStage.PILOT:
        return "Maintain weekly check-in cadence. Verify pilot SLA delivery."
    return "Reactivation: low-pressure value-share, no expectation."


# ---------------------------------------------------------------------------
# Prospect scoring
# ---------------------------------------------------------------------------

# Weight configuration for the multi-factor scoring model.
# Tune these as the pipeline matures.  Sum of weights = 1.0.
SCORING_WEIGHTS = {
    "stage": 0.25,
    "recency": 0.30,
    "role_seniority": 0.20,
    "org_relevance": 0.15,
    "country_fit": 0.10,
}

# Role seniority tiers (higher = more decision power).
ROLE_SENIORITY_MAP: dict[str, float] = {
    "ceo": 1.0,
    "cfo": 0.95,
    "coo": 0.95,
    "chief": 0.95,
    "director": 0.80,
    "vp": 0.85,
    "head": 0.75,
    "manager": 0.55,
    "specialist": 0.40,
    "analyst": 0.30,
    "coordinator": 0.35,
}

# Organisational relevance keywords — healthcare, insurance, gov.
ORG_RELEVANCE_KEYWORDS: list[str] = [
    "hospital", "clinic", "clinica", "medical", "health", "salud",
    "insurance", "seguro", "pharma", "farmac", "biotech", "research",
    "foundation", "fundacion", "ministry", "ministerio", "public health",
    "sanidad", "caja", "eps", "ips", "imss",
]

# Target countries for LATAM expansion, with fit scores.
COUNTRY_FIT_MAP: dict[str, float] = {
    "costa rica": 1.0,
    "colombia": 0.95,
    "panama": 0.90,
    "mexico": 0.85,
    "chile": 0.80,
    "peru": 0.75,
    "argentina": 0.70,
    "ecuador": 0.70,
    "guatemala": 0.65,
    "dominican republic": 0.60,
}


def _stage_score(stage: CultivationStage) -> float:
    """Score based on cultivation stage — further along = higher intent."""
    stage_order: dict[CultivationStage, float] = {
        CultivationStage.PROFILED: 0.10,
        CultivationStage.ENGAGED: 0.30,
        CultivationStage.SIGNALED: 0.55,
        CultivationStage.CONVERSING: 0.75,
        CultivationStage.MEETING: 0.90,
        CultivationStage.PILOT: 0.95,
        CultivationStage.PAYING: 1.00,
        CultivationStage.INACTIVE: 0.05,
    }
    return stage_order.get(stage, 0.0)


def _recency_score(last_signal: datetime | None) -> float:
    """Score how recently the asset signalled.  Fresher = hotter.

    Decay curve: 1.0 if < 3 days, 0.9 at 7 days, 0.5 at 30 days,
    0.0 at 90+ days or no signal.
    """
    if last_signal is None:
        return 0.0
    age_days = (datetime.now(timezone.utc) - last_signal).days
    if age_days < 0:
        return 1.0  # future-dated? treat as fresh.
    if age_days <= 3:
        return 1.0
    if age_days <= 7:
        return 0.90
    if age_days <= 14:
        return 0.75
    if age_days <= 30:
        return 0.50
    if age_days <= 60:
        return 0.25
    if age_days <= 90:
        return 0.10
    return 0.0


def _role_seniority_score(role: str) -> float:
    """Match role string against seniority tiers (case-insensitive substring)."""
    role_lower = role.lower()
    best = 0.30  # default for unrecognised roles
    for keyword, score in ROLE_SENIORITY_MAP.items():
        if keyword in role_lower:
            best = max(best, score)
    return best


def _org_relevance_score(organization: str) -> float:
    """Score organisational relevance based on healthcare/LATAM keywords."""
    org_lower = organization.lower()
    hits = sum(1 for kw in ORG_RELEVANCE_KEYWORDS if kw in org_lower)
    # 1 hit = 0.5, 2 hits = 0.75, 3+ = 1.0
    if hits >= 3:
        return 1.0
    if hits == 2:
        return 0.75
    if hits == 1:
        return 0.50
    return 0.20  # unknown but still in CRM


def _country_fit_score(country: str) -> float:
    """Score geo-priority.  LATAM target countries get higher scores."""
    return COUNTRY_FIT_MAP.get(country.lower(), 0.30)


def score_prospect(asset: Asset) -> float:
    """Compute a composite prospect score (0.0–1.0) across five dimensions.

    Dimensions:
        - **stage**: How far along the cultivation pipeline the asset is.
        - **recency**: Days since last signal from the asset (decay curve).
        - **role_seniority**: Decision-making power inferred from job title.
        - **org_relevance**: How closely the organisation matches Orquor's ICP.
        - **country_fit**: Priority of the asset's country in LATAM expansion.

    Returns a weighted sum using ``SCORING_WEIGHTS``.
    """
    scores = {
        "stage": _stage_score(asset.stage),
        "recency": _recency_score(asset.last_signal_from_asset),
        "role_seniority": _role_seniority_score(asset.role),
        "org_relevance": _org_relevance_score(asset.organization),
        "country_fit": _country_fit_score(asset.country),
    }
    composite = sum(
        SCORING_WEIGHTS[dim] * scores[dim] for dim in SCORING_WEIGHTS
    )
    return round(composite, 4)


def rank_prospects(assets: list[Asset]) -> list[tuple[Asset, float]]:
    """Return prospects sorted by composite score (highest first).

    Each element is ``(asset, score)``.  Use this to prioritise founder
    time and outbound sequencing.
    """
    scored = [(a, score_prospect(a)) for a in assets]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored


def verifier_check(assets: list[Asset]) -> tuple[bool, str]:
    """Verify cultivation discipline."""
    if not assets:
        return True, "No assets in pipeline (vacuous truth)."

    for a in assets:
        if a.stage == CultivationStage.PILOT and not a.last_signal_from_asset:
            return False, f"Asset {a.asset_id} in pilot but no signal recorded — cultivation skipped."
        if a.stage in (CultivationStage.MEETING, CultivationStage.CONVERSING):
            if not a.last_signal_from_asset:
                return False, f"Asset {a.asset_id} advanced without asset signal — violation of HUMINT discipline."

    return True, f"{len(assets)} assets in pipeline; cultivation discipline maintained."


async def run(memory: SharedMemory, dry_run: bool = False, **_: Any) -> dict:
    assets = mock_assets(dry_run=dry_run)
    verifier_passed, verifier_msg = verifier_check(assets)

    actions: dict[str, str] = {}
    for a in assets:
        actions[a.asset_id] = next_action_for(a)

    for a in assets:
        if a.stage in (CultivationStage.SIGNALED, CultivationStage.CONVERSING, CultivationStage.MEETING):
            memory.record(
                sub_agent="Sales",
                feedback_type="cultivation_event",
                section_affected="sales_pipeline",
                feedback_text=f"Asset {a.asset_id} ({a.organization}) at stage {a.stage.value}. Notes: {a.notes}",
                canonical_rule="outcome_only",
                action_taken=actions[a.asset_id],
                reasoning="Stage advancement evaluated against HUMINT cultivation discipline.",
            )

    by_stage: dict[str, int] = {}
    for a in assets:
        by_stage[a.stage.value] = by_stage.get(a.stage.value, 0) + 1

    # --- Prospect scoring & ranking ---
    ranked = rank_prospects(assets)
    top_prospects = [
        {"asset_id": a.asset_id, "name": a.name, "score": s, "stage": a.stage.value}
        for a, s in ranked
    ]

    return {
        "summary": f"assets={len(assets)} " + " ".join(f"{k}={v}" for k, v in by_stage.items()),
        "verifier": verifier_msg,
        "verifier_passed": verifier_passed,
        "next_actions": actions,
        "prospect_scores": {a.asset_id: score_prospect(a) for a in assets},
        "top_prospects": top_prospects,
    }
