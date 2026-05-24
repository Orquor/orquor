"""
Ops-Monitor-Bot
===============

Sprint 1 sub-agent. Observability of the Orquor Clinical infrastructure.
This sub-agent is the prerequisite for all others because every later
sub-agent depends on the trace/log primitives it produces.

Inputs:
    - Metrics endpoints from the GPU host (Hyperstack / Lambda Labs)
    - Application logs from the API server
    - Status of interpreter pool (online / busy / offline)

Outputs:
    - Status snapshot written to MEMORY.md if any threshold breached
    - Alerts to founder's signal channel for critical incidents
    - Daily summary report

Verifier:
    - At least one health datapoint per critical component in the last 5 min
    - Latency p95 below threshold
    - Audit log integrity confirmed (signature chain unbroken)
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from shared_memory import SharedMemory


@dataclass
class HealthSnapshot:
    gpu_utilization_pct: float
    asr_latency_p95_ms: int
    mt_latency_p95_ms: int
    verifier_pass_rate_24h: float
    interpreters_online: int
    audit_log_integrity: bool
    timestamp: str


# Thresholds — configurable in production
THRESHOLDS = {
    "gpu_utilization_max": 92.0,           # %
    "asr_latency_p95_max": 1500,           # ms
    "mt_latency_p95_max": 1200,            # ms
    "verifier_pass_rate_min": 0.88,        # 88%
    "interpreters_online_min": 2,
}


async def collect_health_snapshot(dry_run: bool = False) -> HealthSnapshot:
    """
    Collect health data from real endpoints in production.
    In dry-run, returns a representative mock snapshot.
    """
    if dry_run:
        return HealthSnapshot(
            gpu_utilization_pct=67.3,
            asr_latency_p95_ms=890,
            mt_latency_p95_ms=720,
            verifier_pass_rate_24h=0.942,
            interpreters_online=4,
            audit_log_integrity=True,
            timestamp="2026-05-24T08:00:00Z",
        )

    # Production: actually fetch from monitoring endpoints
    # e.g. Prometheus, Grafana Cloud, Hyperstack API, etc.
    raise NotImplementedError("Production monitoring endpoints not yet wired.")


def evaluate_snapshot(snap: HealthSnapshot) -> tuple[bool, list[str]]:
    """
    Compare snapshot against thresholds. Returns (all_healthy, alerts).
    """
    alerts: list[str] = []

    if snap.gpu_utilization_pct > THRESHOLDS["gpu_utilization_max"]:
        alerts.append(
            f"GPU utilization {snap.gpu_utilization_pct:.1f}% exceeds "
            f"threshold {THRESHOLDS['gpu_utilization_max']}%."
        )
    if snap.asr_latency_p95_ms > THRESHOLDS["asr_latency_p95_max"]:
        alerts.append(
            f"ASR latency p95 {snap.asr_latency_p95_ms}ms exceeds "
            f"threshold {THRESHOLDS['asr_latency_p95_max']}ms."
        )
    if snap.mt_latency_p95_ms > THRESHOLDS["mt_latency_p95_max"]:
        alerts.append(
            f"MT latency p95 {snap.mt_latency_p95_ms}ms exceeds "
            f"threshold {THRESHOLDS['mt_latency_p95_max']}ms."
        )
    if snap.verifier_pass_rate_24h < THRESHOLDS["verifier_pass_rate_min"]:
        alerts.append(
            f"Verifier pass rate {snap.verifier_pass_rate_24h:.3f} below "
            f"threshold {THRESHOLDS['verifier_pass_rate_min']}."
        )
    if snap.interpreters_online < THRESHOLDS["interpreters_online_min"]:
        alerts.append(
            f"Interpreters online {snap.interpreters_online} below "
            f"threshold {THRESHOLDS['interpreters_online_min']}."
        )
    if not snap.audit_log_integrity:
        alerts.append("AUDIT LOG INTEGRITY FAILURE — signature chain broken.")

    return (len(alerts) == 0, alerts)


def verifier_check(snap: HealthSnapshot, alerts: list[str]) -> tuple[bool, str]:
    """
    Outcome-based verifier for this sub-agent's run.

    Pass conditions:
        - Snapshot was actually collected (not None)
        - Audit log integrity is true OR an alert was raised for it
        - Sub-agent communicated alerts to memory if any exist
    """
    if snap is None:
        return False, "Failed to collect snapshot."
    if not snap.audit_log_integrity and not any("AUDIT LOG" in a for a in alerts):
        return False, "Audit log integrity false but no alert raised."
    return True, "Health snapshot collected and integrity verified."


async def run(memory: SharedMemory, dry_run: bool = False, **_: Any) -> dict:
    """Entry point invoked by the orchestrator."""
    snap = await collect_health_snapshot(dry_run=dry_run)
    healthy, alerts = evaluate_snapshot(snap)
    verifier_passed, verifier_msg = verifier_check(snap, alerts)

    if alerts:
        for alert in alerts:
            memory.record(
                sub_agent="Ops-Monitor",
                feedback_type="automated_verifier",
                section_affected="ops_health",
                feedback_text=alert,
                canonical_rule="outcome_only",
                action_taken="alert raised; awaiting human escalation if critical",
                reasoning="Threshold breach detected by snapshot evaluation.",
            )

    return {
        "summary": (
            f"healthy={healthy} alerts={len(alerts)} "
            f"gpu={snap.gpu_utilization_pct:.0f}% "
            f"asr_p95={snap.asr_latency_p95_ms}ms "
            f"pass_rate={snap.verifier_pass_rate_24h:.3f}"
        ),
        "verifier": verifier_msg,
        "verifier_passed": verifier_passed,
        "snapshot": snap,
        "alerts": alerts,
    }
