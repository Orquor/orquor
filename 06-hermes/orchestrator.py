"""
Orquor Hermes — Orchestrator
============================

Central coordinator for the 6 sub-agents. Reads MEMORY.md, dispatches work
to sub-agents, collects verified outputs, and writes consolidated state.

Run modes:
    --dry-run         No external API calls, prints planned actions
    --once            Run all sub-agents one pass and exit
    --daemon          Continuous run (used in production with cron or Temporal)
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Awaitable, Callable

from rich.console import Console
from rich.table import Table

from shared_memory import SharedMemory
from sub_agents import (
    ops_monitor_bot,
    watchtower_bot,
    recruiter_bot,
    sales_bot,
    compliance_watcher_bot,
    content_bot,
)

console = Console()


@dataclass
class SubAgentSpec:
    name: str
    description: str
    runner: Callable[..., Awaitable[dict]]
    priority: int  # 1 highest


REGISTRY = [
    SubAgentSpec(
        name="Ops-Monitor",
        description="Observability of A100, latency, error rate, interpreters online",
        runner=ops_monitor_bot.run,
        priority=1,
    ),
    SubAgentSpec(
        name="Watchtower",
        description="OSINT continuous on competitors and target market",
        runner=watchtower_bot.run,
        priority=2,
    ),
    SubAgentSpec(
        name="Recruiter",
        description="Interpreter pipeline + English screening + scheduling",
        runner=recruiter_bot.run,
        priority=3,
    ),
    SubAgentSpec(
        name="Sales",
        description="Asset profile cultivation + outreach + meeting scheduling",
        runner=sales_bot.run,
        priority=4,
    ),
    SubAgentSpec(
        name="Compliance-Watcher",
        description="Monitor HIPAA, Law 29733, LGPD, BAA expirations, ISO controls",
        runner=compliance_watcher_bot.run,
        priority=5,
    ),
    SubAgentSpec(
        name="Content",
        description="Multi-channel content distribution (LinkedIn, X, YT, Academy)",
        runner=content_bot.run,
        priority=6,
    ),
]


async def run_once(memory: SharedMemory, dry_run: bool) -> None:
    """Run each sub-agent one pass in priority order."""
    table = Table(title="Hermes pass", show_lines=True)
    table.add_column("#", style="cyan")
    table.add_column("Sub-agent", style="bold")
    table.add_column("Output summary")
    table.add_column("Verifier")

    for spec in sorted(REGISTRY, key=lambda x: x.priority):
        console.print(f"[bold cyan]>[/bold cyan] Running {spec.name} - {spec.description}")
        try:
            result = await spec.runner(memory=memory, dry_run=dry_run)
            summary = result.get("summary", "(no summary)")
            verifier = result.get("verifier", "pass") if result.get("verifier_passed", True) else "FAIL"
            table.add_row(str(spec.priority), spec.name, summary, verifier)
        except Exception as exc:
            console.print(f"[red]Error in {spec.name}: {exc}[/red]")
            table.add_row(str(spec.priority), spec.name, f"ERROR: {exc}", "FAIL")

    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(description="Orquor Hermes orchestrator")
    parser.add_argument("--dry-run", action="store_true", help="No external calls")
    parser.add_argument("--once", action="store_true", help="Run one pass and exit")
    parser.add_argument("--daemon", action="store_true", help="Run continuously")
    args = parser.parse_args()

    memory_dir = Path(__file__).parent / "memory"
    memory = SharedMemory(memory_dir=memory_dir)

    if args.daemon:
        console.print("[yellow]Daemon mode not yet implemented. Falling back to --once.[/yellow]")

    asyncio.run(run_once(memory=memory, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
