# ORQUOR

**Auditable Clinical Translation Orchestration.** Multi-agent infrastructure for healthcare and regulated industries. Built in Lima. Operating across LATAM. Designed for proof, not performance.

[![CI/CD](https://github.com/orquor/orquor/actions/workflows/ci.yml/badge.svg)](https://github.com/orquor/orquor/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Verifiers](https://img.shields.io/badge/verifiers-13%20passing-brightgreen.svg)](06-hermes/verifiers/)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-025e8c?logo=dependabot)](.github/dependabot.yml)

---

## What Orquor builds

Orquor constructs the orchestration layer that combines automated speech recognition, machine translation, and certified human interpreters into a single auditable pipeline. Every output is verified by an outcome-based test suite before reaching the screen. Every session is logged with cryptographic timestamping. Every consequential decision is auditable years later.

The company operates under a parent brand with five product verticals:

| Product | Domain | Status |
|---|---|---|
| **Orquor Clinical** | Real-time medical translation EN↔ES with audit logs | In production — LATAM medical-tourism clinics |
| **Orquor Hermes** | Multi-agent orchestration platform B2B SaaS | Internal alpha — public subset in `06-hermes/` |
| **Orquor Academy** | AI Trainer school + placement for Spanish-language LLM evaluation | Landing page live — Cohort 01 Q3 2026 |
| **Orquor Triage** | Asynchronous multilingual clinical triage | Research phase |
| **Orquor Court** | Certified legal interpretation for US courts | Pilot Q1 2027 |
| **Orquor Mental Bridge** | Therapy EN↔ES with LCSW + AI assist | Research phase |

---

## The ACTO category

Orquor defines and publishes **ACTO (Auditable Clinical Translation Orchestration)** as a new technical category. It occupies the gap between human-only Video Remote Interpretation (high accuracy, high cost, no forensic record) and AI-only translation (low cost, high speed, no defensibility).

ACTO requires simultaneous performance on seven axes: latency, cost, medical Word Error Rate, translation faithfulness, audit log granularity, regulatory defensibility, and specialty register adaptation. None are optional.

The category specification is open. We are not patenting it. We are not trademarking the term. Implementations will compete on quality. We will compete by being the best.

**Read the whitepaper:** [`03-whitepaper-acto/whitepaper-acto.md`](03-whitepaper-acto/whitepaper-acto.md)

---

## Repository structure

This is the operational monorepo. Each directory is self-contained and corresponds to a function of the company.

```
01-action-board/       Founder's priority checklist — open first upon return
02-brand/              Brand identity, voice & tone, logo concepts, color palette
03-whitepaper-acto/    ACTO whitepaper source (MD, HTML, PDF, DOCX)
04-web/                Marketing site (index.html), Academy landing, demo page
05-pitch-deck/         Pre-seed pitch deck — 16 slides, HTML standalone
06-hermes/             Hermes multi-agent platform — Python orchestrator + 6 sub-agents + pytest verifiers
07-legal/              Templates: HIPAA BAA, Ley 29733, NDA, IP Assignment, ToS, Contractor Agreement
08-prospects/          HUMINT prospect profiles (Costa Rica + Colombia)
09-content-calendar/   90-day content calendar: LinkedIn, X/Twitter, YouTube, newsletter, email
10-migration-runbook/  ITERAMED → Orquor Clinical migration runbook (Hostinger Edition)
scripts/               Automation scripts — publish, sync, deploy
```

---

## Hermes — Multi-agent orchestration platform

Hermes is the open subset of Orquor's multi-agent orchestration platform. It is a Python-native framework adapted from frontier agent-evaluation research.

### Architecture

```
orchestrator.py          Central coordinator — dispatches tasks, aggregates feedback
├── ops_monitor_bot.py   Observability and system health
├── watchtower_bot.py    OSINT continuous monitoring
├── recruiter_bot.py     Interpreter pipeline management
├── sales_bot.py         HUMINT-style prospect cultivation
├── compliance_watcher_bot.py   HIPAA / Ley 29733 / LGPD monitoring
└── content_bot.py       Multi-channel content distribution

shared_memory.py         MEMORY.md interface + 9-rule feedback decision tree
verifiers/               pytest-based outcome verifiers (13 tests, all passing)
memory/
  ├── MEMORY.md          Shared memory seed
  └── lessons_learned.md Cross-task patterns extracted from operations
```

### Quick start

```bash
cd 06-hermes
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest verifiers/ -v              # 13 passing tests
python orchestrator.py --dry-run --once
```

---

## Verifier methodology

Each verifier checks one outcome property. Atomic. Weighted. Pass-or-fail. The methodology is openly described in the ACTO whitepaper (Section 4). A representative verifier:

```python
def verify_dosage_preserved(source: str, translated: str) -> VerifierResult:
    """V1 — Numeric dosage in source must appear identically in translated.
    Weight: +5 (catastrophic if violated)."""
    s = extract_numeric_dosages(source)
    t = extract_numeric_dosages(translated)
    missing = s - t
    if missing:
        return VerifierResult(False, 5, f"Dosage {missing} missing in translation")
    return VerifierResult(True, 5)
```

The verifier suite shipped here is a representative subset of what runs in production at Orquor Clinical.

---

## Brand

Orquor writes like a VP of Engineering who also knows how to sell. Technical, sober, without ornament. Evidence before adjectives. Data before claims.

**Palette:** `orquor.ink` #0B0F14 · `orquor.bone` #F4F1EB · `orquor.signal` #3B82F6 · `orquor.verify` #10B981
**Type:** Inter Tight (headers), Inter (body), JetBrains Mono (code)
**Logo:** Three concepts in `02-brand/logo-concepts.svg` — iterate with professional designer (Month 2)

Full guidelines: [`02-brand/BRAND_IDENTITY.md`](02-brand/BRAND_IDENTITY.md)

---

## Get involved

| Purpose | Email |
|---|---|
| Research collaboration | `research@orquor.com` |
| Hospital pilot | `hello@orquor.com` |
| Join the team | `careers@orquor.com` |
| Academy applications | `academy@orquor.com` |

We are hiring senior ML engineers (ASR + MT specialization), certified medical interpreters, regulatory affairs counsel, and enterprise sales.

---

## Status

**In production** — Orquor Clinical serving early customers in LATAM medical-tourism clinics. Migration from previous brand (ITERAMED) completed Q2 2026.

**Roadmap** — Telehealth API alpha Q3 2026. Orquor Court pilot Q1 2027. Orquor Hermes platform B2B Q2 2027.

**Funding** — Pre-seed round open. SAFE post-money cap USD 6M. Lead position open for the right LATAM-frontier-tech investor.

**Headcount** — Small. Hiring carefully.

---

## License

Code in this repository: **MIT License** ([`LICENSE`](LICENSE)).
ACTO specification text: **CC BY 4.0**.
Legal templates in `07-legal/`: provided as-is, must be reviewed by qualified counsel before use.

---

Built in Lima. Operating across LATAM. Designed for proof, not performance.

`hello@orquor.com` · [orquor.com](https://orquor.com)
