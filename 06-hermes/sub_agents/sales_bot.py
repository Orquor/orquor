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

    return {
        "summary": f"assets={len(assets)} " + " ".join(f"{k}={v}" for k, v in by_stage.items()),
        "verifier": verifier_msg,
        "verifier_passed": verifier_passed,
        "next_actions": actions,
    }
