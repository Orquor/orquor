"""
Orquor Hermes — Shared Memory
=============================

Persistence layer shared across all sub-agents. Adapted directly from the
OpenClaw Atlas MEMORY.md discipline. Each sub-agent reads and writes here.

Storage stack:
- Postgres for structured records (events, decisions, feedback)
- Qdrant for vector retrieval (semantic memory)
- MEMORY.md markdown file for human-readable persistence

The MEMORY.md file is the source of truth for cross-task lessons. Postgres
and Qdrant are operational indexes over the same content.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional


# -----------------------------------------------------------------------------
# Data model
# -----------------------------------------------------------------------------


class FeedbackVerdict(str, Enum):
    """The 9-rule decision tree from OpenClaw Atlas adapted to Hermes."""

    ALIGNED = "ALIGNED"
    PARTIALLY_ALIGNED = "PARTIALLY_ALIGNED"
    CONTESTED = "CONTESTED"


class FeedbackSource(str, Enum):
    AUTOMATED_VERIFIER = "automated_verifier"
    HUMAN_SUPERVISOR = "human_supervisor"
    CUSTOMER = "customer"
    PEER_AGENT = "peer_agent"
    EXTERNAL_AUDITOR = "external_auditor"


@dataclass
class MemoryEntry:
    """A single entry in the shared MEMORY.md."""

    timestamp: str
    sub_agent: str
    feedback_type: str
    section_affected: str
    feedback_text: str
    canonical_rule: str
    verdict: FeedbackVerdict
    action_taken: str
    reasoning: str
    outcome: Optional[str] = None
    task_id: Optional[str] = None

    @classmethod
    def now(cls, **kwargs: Any) -> "MemoryEntry":
        ts = datetime.now(timezone.utc).isoformat()
        return cls(timestamp=ts, **kwargs)

    def to_markdown(self) -> str:
        outcome_line = f"- **Outcome posterior**: {self.outcome}\n" if self.outcome else ""
        task_id_line = f" — task {self.task_id}" if self.task_id else ""
        return (
            f"### {self.timestamp} — {self.feedback_type} — {self.sub_agent}{task_id_line}\n\n"
            f"- **Source**: {self.feedback_type}\n"
            f"- **Section affected**: {self.section_affected}\n"
            f"- **Feedback literal**: > {self.feedback_text}\n"
            f"- **Canonical rule**: {self.canonical_rule}\n"
            f"- **Verdict**: {self.verdict.value}\n"
            f"- **Action taken**: {self.action_taken}\n"
            f"- **Reasoning**: {self.reasoning}\n"
            f"{outcome_line}"
            f"\n---\n\n"
        )


# -----------------------------------------------------------------------------
# Decision tree (the 9 rules — verbatim discipline from OpenClaw Atlas)
# -----------------------------------------------------------------------------


CANONICAL_RULES = {
    "outcome_only": (
        "Verifiers evaluate final outputs, not intermediate steps. "
        "If feedback pushes to trace-based evaluation, mark CONTESTED."
    ),
    "positive_language_signed_weight": (
        "Verifier phrasing describes the desired behavior with positive language; "
        "use signed weight (negative for violations). Do not flip polarity."
    ),
    "atomic_verifiers": (
        "Each verifier checks one outcome property. Composite verifiers obscure "
        "failure attribution and are forbidden."
    ),
    "at_least_one_negative": (
        "Every verifier suite must contain at least one negative verifier "
        "(weight < 0) that detects disallowed content or behavior."
    ),
    "memory_natural_request": (
        "MEMORY entries are written when a feedback event occurs naturally, "
        "not because the orchestrator was told to log."
    ),
    "verifiers_pytest_form": (
        "Verifiers are pytest test functions. Same function form across Hermes. "
        "Maintain identity for replay."
    ),
    "failure_justifications_three_areas": (
        "When recording a failure, three areas must be documented: "
        "(1) why correct, (2) why present, (3) what model did wrong."
    ),
    "single_turn_no_message_after": (
        "Single-turn sub-agent invocations never use mid-stream message after the "
        "initial prompt. Contaminates the trajectory."
    ),
    "no_start_fresh_during_session": (
        "During an active operation session, do not Start Fresh. Either roll back "
        "with audit trail or proceed; never silently reset state."
    ),
}


def validate_feedback(feedback_text: str, proposed_action: str) -> FeedbackVerdict:
    """
    Apply the 9-rule decision tree to incoming feedback.

    Returns CONTESTED if the feedback contradicts any canonical rule;
    ALIGNED if it cites or aligns with a rule; PARTIALLY_ALIGNED otherwise.

    This is a deliberately simple heuristic. In production, an LLM call
    augments this with semantic understanding.
    """
    lower = feedback_text.lower()

    # Rule 1: outcome-only — reject trace-based push
    if any(t in lower for t in ["trajectory", "step-by-step", "intermediate step", "trace"]):
        if "evaluate" in lower or "verifier" in lower:
            return FeedbackVerdict.CONTESTED

    # Rule 2: positive-language + signed-weight
    if "reward absence" in lower or "flip polarity" in lower:
        return FeedbackVerdict.CONTESTED

    # Rule 3: composite verifiers
    if "stack with OR" in lower or "combine these checks" in lower:
        return FeedbackVerdict.CONTESTED

    # Rule 5: explicit instruction to MEMORY
    if "create a MEMORY.md as instruction" in lower:
        return FeedbackVerdict.CONTESTED

    return FeedbackVerdict.ALIGNED


# -----------------------------------------------------------------------------
# Memory file persistence
# -----------------------------------------------------------------------------


class SharedMemory:
    """File-backed shared memory for the Hermes orchestrator and sub-agents."""

    def __init__(self, memory_dir: Path):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.markdown_path = self.memory_dir / "MEMORY.md"
        self.lessons_path = self.memory_dir / "lessons_learned.md"
        self.events_jsonl = self.memory_dir / "events.jsonl"
        self._ensure_markdown_header()

    def _ensure_markdown_header(self) -> None:
        if not self.markdown_path.exists():
            self.markdown_path.write_text(
                "# Orquor Hermes — Shared MEMORY.md\n\n"
                "Persistence layer for cross-sub-agent feedback and decisions. "
                "Adapted from OpenClaw Atlas v4 discipline. New entries are inserted "
                "at the top of the Historical section.\n\n"
                "---\n\n"
                "## Canonical rules (do not modify without changelog)\n\n"
                + "\n".join(f"- **{k}**: {v}" for k, v in CANONICAL_RULES.items())
                + "\n\n---\n\n## Historical feedback (most recent first)\n\n",
                encoding="utf-8",
            )

    def append_entry(self, entry: MemoryEntry) -> None:
        """Insert a new entry at the top of the Historical section."""
        text = self.markdown_path.read_text(encoding="utf-8")
        marker = "## Historical feedback (most recent first)\n\n"
        if marker not in text:
            text += marker
        before, after = text.split(marker, 1)
        new_text = before + marker + entry.to_markdown() + after
        self.markdown_path.write_text(new_text, encoding="utf-8")

        with self.events_jsonl.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), default=str) + "\n")

    def record(
        self,
        sub_agent: str,
        feedback_type: str,
        section_affected: str,
        feedback_text: str,
        canonical_rule: str,
        action_taken: str,
        reasoning: str,
        outcome: Optional[str] = None,
        task_id: Optional[str] = None,
    ) -> MemoryEntry:
        verdict = validate_feedback(feedback_text, action_taken)
        entry = MemoryEntry.now(
            sub_agent=sub_agent,
            feedback_type=feedback_type,
            section_affected=section_affected,
            feedback_text=feedback_text,
            canonical_rule=canonical_rule,
            verdict=verdict,
            action_taken=action_taken,
            reasoning=reasoning,
            outcome=outcome,
            task_id=task_id,
        )
        self.append_entry(entry)
        return entry

    def read_recent(self, n: int = 20) -> list[dict]:
        """Read the n most recent events from the JSONL log."""
        if not self.events_jsonl.exists():
            return []
        lines = self.events_jsonl.read_text(encoding="utf-8").strip().splitlines()
        recent = lines[-n:]
        return [json.loads(line) for line in recent if line.strip()]
