"""
Compliance-Watcher-Bot
======================

Continuous monitoring of regulatory compliance status across:
    - Peruvian Law 29733 (data protection)
    - HIPAA BAA expirations and renewal windows
    - LGPD (Brazil) when expansion engages
    - ISO 27001 controls (when in process)
    - SOC 2 Type II evidence collection
    - INDECOPI trademark prosecution status

Inputs:
    - Compliance calendar (BAA expirations, audit dates, certification renewals)
    - Document repository status (policies, DPIA records, breach logs)
    - External regulator publications (DGAJ-MINJUS, OCR HHS, ANPD Brazil)

Outputs:
    - Daily compliance posture report
    - Alerts for items due in < 30 days
    - Escalations to founder + legal counsel for material risks
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import date, datetime, timezone, timedelta
from typing import Any

from shared_memory import SharedMemory


@dataclass
class ComplianceItem:
    item_id: str
    framework: str        # "HIPAA", "Ley 29733", "LGPD", "ISO 27001", "SOC 2"
    description: str
    due_date: date | None
    status: str           # "current", "approaching", "overdue", "complete"
    severity: str         # "info", "watch", "critical"


def mock_compliance_state(dry_run: bool) -> list[ComplianceItem]:
    if not dry_run:
        return []
    today = date.today()
    return [
        ComplianceItem(
            item_id="HIPAA-BAA-LAMBDA-001",
            framework="HIPAA",
            description="Sign BAA with Lambda Labs (US-West A100 reserved)",
            due_date=today + timedelta(days=14),
            status="approaching",
            severity="critical",
        ),
        ComplianceItem(
            item_id="LEY-29733-PRIV-001",
            framework="Ley 29733",
            description="Register privacy policy with DGAJ-MINJUS",
            due_date=today + timedelta(days=21),
            status="approaching",
            severity="watch",
        ),
        ComplianceItem(
            item_id="ISO-27001-RISK-001",
            framework="ISO 27001",
            description="Complete risk assessment (Annex A controls 5.x)",
            due_date=today + timedelta(days=45),
            status="current",
            severity="info",
        ),
        ComplianceItem(
            item_id="EO-INSURANCE",
            framework="Insurance",
            description="Bind Errors & Omissions policy (USD 2M minimum)",
            due_date=today + timedelta(days=60),
            status="current",
            severity="critical",
        ),
        ComplianceItem(
            item_id="INDECOPI-TM-9",
            framework="Trademark",
            description="ORQUOR mark prosecution — Nice class 9",
            due_date=today + timedelta(days=120),
            status="current",
            severity="info",
        ),
    ]


def evaluate_state(items: list[ComplianceItem]) -> tuple[list[ComplianceItem], list[ComplianceItem]]:
    """Return (alerts, normal)."""
    today = date.today()
    alerts: list[ComplianceItem] = []
    normal: list[ComplianceItem] = []
    for item in items:
        if item.due_date is None:
            normal.append(item)
            continue
        days_left = (item.due_date - today).days
        if days_left <= 0:
            item.status = "overdue"
            alerts.append(item)
        elif days_left <= 30 and item.severity in ("critical", "watch"):
            item.status = "approaching"
            alerts.append(item)
        else:
            normal.append(item)
    return alerts, normal


def verifier_check(alerts: list[ComplianceItem]) -> tuple[bool, str]:
    """
    Pass conditions:
        - No overdue critical items (would fail this verifier)
    """
    overdue_critical = [a for a in alerts if a.status == "overdue" and a.severity == "critical"]
    if overdue_critical:
        return False, f"{len(overdue_critical)} critical compliance items are overdue."
    return True, f"{len(alerts)} alerts pending; none overdue critical."


async def run(memory: SharedMemory, dry_run: bool = False, **_: Any) -> dict:
    items = mock_compliance_state(dry_run=dry_run)
    alerts, normal = evaluate_state(items)
    verifier_passed, verifier_msg = verifier_check(alerts)

    for alert in alerts:
        days_left = (alert.due_date - date.today()).days if alert.due_date else None
        memory.record(
            sub_agent="Compliance-Watcher",
            feedback_type="compliance_alert",
            section_affected=alert.framework,
            feedback_text=f"{alert.item_id}: {alert.description} ({days_left} days)",
            canonical_rule="outcome_only",
            action_taken="alert raised; awaiting founder/counsel action",
            reasoning=f"Item severity={alert.severity}, status={alert.status}.",
        )

    return {
        "summary": (
            f"items={len(items)} alerts={len(alerts)} "
            + " ".join(f"{a.framework}({a.severity})" for a in alerts)
        ),
        "verifier": verifier_msg,
        "verifier_passed": verifier_passed,
        "alerts": [a.item_id for a in alerts],
    }
