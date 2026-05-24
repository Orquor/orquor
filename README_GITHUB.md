# Orquor

**Auditable Clinical Translation Orchestration.** Multi-agent infrastructure for healthcare and regulated industries.

Orquor builds the orchestration layer that combines automated speech recognition, machine translation, and certified human interpreters into a single auditable pipeline. Every output is verified by an outcome-based test suite before reaching the screen. Every session is logged with cryptographic timestamping. Every consequential decision is auditable years later.

We operate from Lima, Peru, serving healthcare networks across Latin America and the United States.

---

## What is in this repo

This is the public-facing repository of Orquor. The directory layout below reflects the internal organization of the company's operational artifacts.

| Folder | Purpose |
|---|---|
| `01-action-board/` | Operating priorities for the founder |
| `02-brand/` | Brand identity guidelines + logo concepts |
| `03-whitepaper-acto/` | The ACTO whitepaper — Markdown, HTML, PDF, DOCX |
| `04-web/` | Marketing site (index.html) and Orquor Academy landing |
| `05-pitch-deck/` | Pre-seed pitch deck (HTML) |
| `06-hermes/` | Hermes — multi-agent orchestration platform. Python sub-agents, pytest verifier suite, shared MEMORY.md |
| `07-legal/` | Templates: BAA, Privacy Policy, NDA, IP Assignment, ToS, Contractor Agreement |
| `08-prospects/` | Prospect master sheet (internal — not committed publicly) |
| `09-content-calendar/` | 90-day content calendar with ready-to-publish copy |
| `10-migration-runbook/` | Technical migration runbook (Hostinger Edition) |

---

## The ACTO whitepaper

Read the technical specification of what we are building:

- **arXiv**: [link will be added here on publication]
- **Direct PDF**: [orquor.com/whitepaper-acto.pdf](https://orquor.com/whitepaper-acto.pdf)
- **Markdown source**: [`03-whitepaper-acto/whitepaper-acto.md`](03-whitepaper-acto/whitepaper-acto.md)

The category is open. We are not patenting. We are not trademarking the term. The implementations will compete on quality. We will compete by being the best.

---

## Hermes

Hermes is the open subset of our multi-agent orchestration platform. It is a Python-native framework adapted from frontier agent-evaluation research, with:

- An orchestrator coordinating six initial sub-agents (Ops-Monitor, Watchtower, Recruiter, Sales, Compliance-Watcher, Content)
- A shared MEMORY.md persistence layer with cross-agent feedback discipline
- A verifier suite (~13 tests in this public subset) using pytest with weighted outcome-based checks
- A canonical 9-rule decision tree for feedback validation

```bash
cd 06-hermes
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest verifiers/translation_verifiers.py -v  # 13 passing tests
python orchestrator.py --dry-run --once       # see Hermes in action
```

---

## Verifier methodology

The verifier suite shipped here is a representative subset of what runs in production at Orquor Clinical. The methodology is openly described in the whitepaper. Sample verifier:

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

Each verifier checks one outcome property. Atomic. Weighted. Pass-or-fail.

---

## Get involved

- **Research collaboration** — `research@orquor.com`. Access to the full verifier suite under collaboration license. Co-publication welcome.
- **Hospital pilot** — `hello@orquor.com`. Schedule a 30-minute discovery call. We will run a head-to-head against your current vendor on your worst hour of audio.
- **Join the team** — `careers@orquor.com`. We are hiring senior ML engineers (ASR + MT specialization), certified medical interpreters, regulatory affairs counsel, and enterprise sales.
- **Academy applications** — `academy@orquor.com`. Cohort 01 of Orquor Academy opens applications in Q3 2026.

---

## Status

**In production** — Orquor Clinical serving early customers in LATAM medical-tourism clinics. Migration from previous brand (ITERAMED) completed Q2 2026.

**Roadmap** — Telehealth API alpha Q3 2026. Orquor Court pilot Q1 2027. Orquor Hermes platform B2B Q2 2027.

**Headcount** — Small. Hiring carefully.

**Funding** — Pre-seed round open. SAFE post-money cap USD 6M. Lead position open for the right LATAM-frontier-tech investor.

---

## License

The code in this public repository is released under the **MIT License**. The ACTO specification text is released under **CC BY 4.0**. Legal templates in `07-legal/` are provided as-is and must be reviewed by qualified counsel before use.

---

Built in Lima. Operating across LATAM. Designed for proof, not performance.

`hello@orquor.com` · [orquor.com](https://orquor.com)
