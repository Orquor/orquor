# Changelog

All notable changes to the Orquor project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Orquor adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2026-05-24

### Foundation

- Repository structure initialized: 11 operational directories with self-contained functions.
- `README.md` — Public-facing project description, product verticals table, ACTO category definition.
- `README_GITHUB.md` — GitHub organization profile README.
- `MANIFEST.md` — Consolidated index of all artifacts produced in the autonomous sprint.
- `AGENTES.md` — Three-agent architecture document (Claude, Qwen, Hermes) with roles and communication protocol.
- `NEXT_TASKS.md` — Priority task queue for multi-agent coordination.
- `CONTRIBUTING.md` — Contribution guidelines: scope, setup, verifier methodology, PR process, code style.
- `LICENSE` — MIT License for all code in the repository.

### Whitepaper

- `03-whitepaper-acto/whitepaper-acto.md` — Technical whitepaper defining the ACTO (Auditable Clinical Translation Orchestration) category.
- `03-whitepaper-acto/whitepaper-acto.pdf` — PDF generated via pandoc + Edge headless, ready for arXiv submission.
- `03-whitepaper-acto/whitepaper-acto.html` — Standalone HTML with embedded CSS for blog publication.
- `03-whitepaper-acto/whitepaper-acto.docx` — Word format for investor distribution.
- `03-whitepaper-acto/pandoc-style.css` — Print CSS for whitepaper regeneration.
- `03-whitepaper-acto/arxiv-submission.md` — arXiv submission preparation document.

### Brand

- `02-brand/BRAND_IDENTITY.md` — Complete brand identity: naming hierarchy, voice and tone, colors, typography, vocabulary rules.
- `02-brand/logo-concepts.svg` — Three logo concepts (Loop doble, Q-centro, Monograma) with color palette and typography swatch.

### Verifiers

- `06-hermes/verifiers/translation_verifiers.py` — 13 pytest-based outcome verifiers, all passing.
- Verifier methodology: atomic checks, weighted (1–5), deterministic, no external API dependencies.
- `VerifierResult` contract defined and enforced across the suite.

### Hermes Platform

- `06-hermes/orchestrator.py` — Central coordinator supporting dry-run mode.
- `06-hermes/shared_memory.py` — MEMORY.md interface with 9-rule feedback decision tree.
- `06-hermes/sub_agents/ops_monitor_bot.py` — Observability and system health agent.
- `06-hermes/sub_agents/watchtower_bot.py` — OSINT continuous monitoring agent.
- `06-hermes/sub_agents/recruiter_bot.py` — Interpreter pipeline management agent.
- `06-hermes/sub_agents/sales_bot.py` — HUMINT-style prospect cultivation agent.
- `06-hermes/sub_agents/compliance_watcher_bot.py` — HIPAA / Ley 29733 / LGPD monitoring agent.
- `06-hermes/sub_agents/content_bot.py` — Multi-channel content distribution agent.
- `06-hermes/memory/MEMORY.md` — Shared memory seed for agent coordination.
- `06-hermes/memory/lessons_learned.md` — Cross-task patterns extracted from operations.
- `06-hermes/requirements.txt` — Python dependency specification.
- `06-hermes/.env.example` — Environment configuration template.

### CI/CD and Automation

- `scripts/setup-dev.sh` — Development environment setup script.
- `scripts/seed-db.sh` — Database seeding script.
- `scripts/monitor.sh` — System monitoring script.

### Landing

- `04-web/index.html` — Marketing landing page, standalone HTML, brand-consistent, deployable to Hostinger.
- `04-web/academy.html` — Orquor Academy standalone landing page with hero, modules, pricing tiers, and FAQ.

### Documentation

- `docs/architecture.md` — System architecture documentation.
- `docs/api-reference.md` — API reference documentation.

### Legal

- `07-legal/hipaa-baa-template.md` — Business Associate Agreement template.
- `07-legal/privacy-policy-ley-29733.md` — Privacy Policy aligned to Peruvian Law 29733.
- `07-legal/nda-template.md` — Mutual Non-Disclosure Agreement template.
- `07-legal/ip-assignment-template.md` — IP Assignment for employees and contractors.
- `07-legal/contractor-agreement-template.md` — Contractor Services Agreement template.
- `07-legal/terms-of-service-b2b.md` — B2B Terms of Service template.
- `07-legal/privacy-policy-web.md` — Public website Privacy Policy (Law 29733 + GDPR + CCPA).
- `07-legal/cookie-policy-web.md` — Public website Cookie Policy.
- `07-legal/sla-clinical.md` — Clinical SLA template.

### Content

- `09-content-calendar/CALENDAR.md` — 90-day master content plan with channel cadence and metrics.
- LinkedIn posts: 21 days of content (dia-001 through dia-021), plus dia-022 through dia-030.
- X/Twitter posts: 21 days of content (dia-001 through dia-021).
- YouTube scripts: Episodes 1 through 8.
- Newsletter editions: 1 through 5.
- Email templates: interpreter onboarding, B2B client welcome, prospect follow-up, outreach, full onboarding.

### Prospects

- `08-prospects/PROSPECTS_MASTER.md` — 10 cultivated profiles (5 Costa Rica + 5 Colombia) with HUMINT discipline rules.

### Pitch Deck

- `05-pitch-deck/pitch-deck.html` — 16-slide pre-seed deck. Pitch ask: USD 600k.

### Migration

- `10-migration-runbook/RUNBOOK.md` — 8-phase ITERAMED to Orquor Clinical migration runbook, Hostinger Edition.

### Governance

- `CHANGELOG.md` — This file.
- `SECURITY.md` — Security policy and vulnerability disclosure process.
- `CODE_OF_CONDUCT.md` — Contributor Covenant Code of Conduct.

---

## Versioning conventions

- **MAJOR** (X.0.0): Breaking changes to the ACTO specification, verifier contract, or public API surface.
- **MINOR** (0.X.0): New verifiers, sub-agents, documentation chapters, or legal templates added in a backward-compatible manner.
- **PATCH** (0.0.X): Corrections, typo fixes, formatting updates, dependency bumps.

Pre-release tags (`-alpha`, `-beta`, `-rc`) will be used for Hermes platform releases prior to B2B launch (Q2 2027).
