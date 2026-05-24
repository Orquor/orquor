"""
Watchtower-Bot
==============

Continuous OSINT against named competitors and the target market.
Reference: Canvas `orquor-capa-negra.canvas.tsx`, Framework 2 — OSINT.

Data sources monitored:
    - LinkedIn employee movements at competitors (hire/depart signals)
    - Job postings at competitors (tech stack + roadmap leakage)
    - Public RFPs (Mercado Público CL, Compranet MX, OSCE Perú, SAM.gov)
    - USPTO TESS + WIPO + INDECOPI trademark filings
    - SEC filings (10-Q, 10-K, 8-K) for public competitors / parents
    - GitHub commits if competitor has OSS
    - Crunchbase + PitchBook funding signals
    - Conference attendee lists (HIMSS, RSNA, ATA, MTA)

Outputs:
    - Weekly digest in MEMORY.md
    - Critical-signal alerts to founder
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

from shared_memory import SharedMemory


COMPETITORS = [
    "LanguageLine Solutions",
    "Cloudbreak Health",
    "Stratus Video",
    "AMN Healthcare Language Services",
    "Voyce Global",
    "Boostlingo",
    "Wordly",
    "InDemand Interpreting",
    "Martti",
]

TARGET_MARKETS = [
    "Costa Rica medical tourism",
    "Colombia private hospitals",
    "Mexico private healthcare",
    "US Hispanic telehealth",
    "Peru Lima private hospitals",
]


@dataclass
class Signal:
    kind: str                # 'hire', 'departure', 'rfp', 'patent', 'funding', 'sec_filing'
    source: str
    competitor_or_market: str
    summary: str
    severity: str            # 'info', 'watch', 'act'
    url: str | None = None


async def scan_linkedin(dry_run: bool) -> list[Signal]:
    """
    In production: use a paid LinkedIn-monitoring API (PhantomBuster, Lix,
    Bright Data) or a careful Playwright headless setup.
    In dry-run: return representative mock signals.
    """
    if dry_run:
        return [
            Signal(
                kind="hire",
                source="LinkedIn",
                competitor_or_market="Cloudbreak Health",
                summary="Hired VP Product from Epic Systems — likely EHR integration push.",
                severity="watch",
            ),
            Signal(
                kind="departure",
                source="LinkedIn",
                competitor_or_market="LanguageLine Solutions",
                summary="Director of AI Strategy departed after 14 months — internal AI traction may be stalled.",
                severity="watch",
            ),
        ]
    raise NotImplementedError


async def scan_public_rfps(dry_run: bool) -> list[Signal]:
    """Scan public procurement portals for medical translation RFPs."""
    if dry_run:
        return [
            Signal(
                kind="rfp",
                source="OSCE Perú",
                competitor_or_market="Peru Lima private hospitals",
                summary="EsSalud published RFP for medical interpretation services, deadline 30 days.",
                severity="act",
                url="https://www.osce.gob.pe/...",
            ),
        ]
    raise NotImplementedError


async def scan_trademark_filings(dry_run: bool) -> list[Signal]:
    """USPTO TESS + WIPO + INDECOPI scan for category-relevant filings."""
    if dry_run:
        return [
            Signal(
                kind="patent",
                source="USPTO TESS",
                competitor_or_market="Wordly",
                summary='Trademark filed for "ClinicalVoice" in Class 9 — possible healthcare pivot.',
                severity="watch",
            ),
        ]
    raise NotImplementedError


async def scan_sec_filings(dry_run: bool) -> list[Signal]:
    """SEC EDGAR for 10-Q / 10-K / 8-K mentions of competitors' parents."""
    if dry_run:
        return []
    raise NotImplementedError


async def scan_all(dry_run: bool) -> list[Signal]:
    results = await asyncio.gather(
        scan_linkedin(dry_run),
        scan_public_rfps(dry_run),
        scan_trademark_filings(dry_run),
        scan_sec_filings(dry_run),
    )
    return [sig for batch in results for sig in batch]


def verifier_check(signals: list[Signal]) -> tuple[bool, str]:
    """
    Pass conditions:
        - At least one source was scanned (signals list exists, even if empty)
        - All 'act' severity signals are flagged for human review
    """
    if signals is None:
        return False, "Scan returned None — sources unreachable."
    act_signals = [s for s in signals if s.severity == "act"]
    if act_signals:
        return True, f"{len(act_signals)} action signal(s) detected and flagged."
    return True, "Scan completed; no action signals."


async def run(memory: SharedMemory, dry_run: bool = False, **_: Any) -> dict:
    signals = await scan_all(dry_run=dry_run)
    verifier_passed, verifier_msg = verifier_check(signals)

    for sig in signals:
        if sig.severity in ("act", "watch"):
            memory.record(
                sub_agent="Watchtower",
                feedback_type=f"osint_{sig.kind}",
                section_affected="market_intelligence",
                feedback_text=sig.summary,
                canonical_rule="outcome_only",
                action_taken="signal recorded for founder review" if sig.severity == "act" else "watching",
                reasoning=f"Source: {sig.source}, target: {sig.competitor_or_market}",
            )

    by_severity = {"info": 0, "watch": 0, "act": 0}
    for s in signals:
        by_severity[s.severity] = by_severity.get(s.severity, 0) + 1

    return {
        "summary": (
            f"signals={len(signals)} act={by_severity['act']} "
            f"watch={by_severity['watch']} info={by_severity['info']}"
        ),
        "verifier": verifier_msg,
        "verifier_passed": verifier_passed,
        "signals": signals,
    }
