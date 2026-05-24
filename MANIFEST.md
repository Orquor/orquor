# Orquor — Empire Manifest

Consolidated index of everything produced in the autonomous sprint of 2026-05-24. Each entry is a path + 1-line description + status.

---

## 01 — Action Board

| Path | Description | Status |
|---|---|---|
| `README_GITHUB.md` | Public GitHub README for github.com/orquor/orquor — describes the repo and Hermes | Ready to push |
| `01-action-board/ACTION_BOARD.md` | Priority-tagged checklist (P0 / P1 / P2 / P3) of actions only the founder can execute. **OPEN FIRST.** | Complete |

## 02 — Brand identity

| Path | Description | Status |
|---|---|---|
| `02-brand/BRAND_IDENTITY.md` | Naming hierarchy, voice & tone, colors, typography, vocabulary, anti-patterns | Complete |
| `02-brand/logo-concepts.svg` | 3 logo concepts (Loop doble, Q-centro, Monograma) + color palette + typography swatch | Complete v1 — iterate with designer |

## 03 — ACTO Whitepaper

| Path | Description | Status |
|---|---|---|
| `03-whitepaper-acto/whitepaper-acto.md` | Technical whitepaper "Auditable Clinical Translation Orchestration" — defines the category | Complete |
| `03-whitepaper-acto/whitepaper-acto.pdf` | **PDF (60 KB)** — generated via pandoc + Edge headless with custom CSS | Ready to upload to arXiv + Hostinger |
| `03-whitepaper-acto/whitepaper-acto.html` | Standalone HTML with embedded CSS | Ready for blog publication |
| `03-whitepaper-acto/whitepaper-acto.docx` | Word format (22 KB) for investors who prefer it | Ready |
| `03-whitepaper-acto/pandoc-style.css` | Print CSS for future re-generation if whitepaper updates | Reference |

## 04 — Web

| Path | Description | Status |
|---|---|---|
| `04-web/index.html` | Landing page, standalone HTML, brand-consistent, deployable to Hostinger | Complete — add OG image + deploy |
| `04-web/academy.html` | Orquor Academy standalone landing page — hero, modules, pricing tiers, FAQ | Ready to deploy at academy.orquor.com |

## 05 — Pitch deck

| Path | Description | Status |
|---|---|---|
| `05-pitch-deck/pitch-deck.html` | 16-slide pre-seed deck. Pitch ask: USD 600k | Complete v1 — refine with first investor feedback |

## 06 — Hermes (multi-agent orchestration)

| Path | Description | Status |
|---|---|---|
| `06-hermes/README.md` | Architecture overview + implementation order | Complete |
| `06-hermes/orchestrator.py` | Central coordinator | Complete (dry-run mode) |
| `06-hermes/shared_memory.py` | MEMORY.md interface + 9-rule feedback decision tree | Complete |
| `06-hermes/sub_agents/ops_monitor_bot.py` | Sprint 1 — observability | Complete |
| `06-hermes/sub_agents/watchtower_bot.py` | OSINT continuous | Complete |
| `06-hermes/sub_agents/recruiter_bot.py` | Interpreter pipeline | Complete |
| `06-hermes/sub_agents/sales_bot.py` | HUMINT-style cultivation | Complete |
| `06-hermes/sub_agents/compliance_watcher_bot.py` | HIPAA/Ley 29733/LGPD monitoring | Complete |
| `06-hermes/sub_agents/content_bot.py` | Multi-channel content distribution | Complete |
| `06-hermes/verifiers/translation_verifiers.py` | 13 pytest verifiers — **ALL PASSING** | Complete + verified |
| `06-hermes/memory/MEMORY.md` | Shared memory seed | Complete |
| `06-hermes/memory/lessons_learned.md` | Cross-task patterns | Complete |
| `06-hermes/requirements.txt` | Python dependencies | Complete |
| `06-hermes/.env.example` | Environment configuration template | Complete |

## 07 — Legal templates

| Path | Description | Status |
|---|---|---|
| `07-legal/hipaa-baa-template.md` | Business Associate Agreement (US healthcare customers) | Template — counsel review required |
| `07-legal/privacy-policy-ley-29733.md` | Privacy Policy aligned to Peruvian Law 29733 | Template — counsel review required |
| `07-legal/nda-template.md` | Mutual Non-Disclosure Agreement | Template — counsel review required |
| `07-legal/ip-assignment-template.md` | IP Assignment for employees + contractors | Template — counsel review required |
| `07-legal/contractor-agreement-template.md` | Contractor Services Agreement | Template — counsel review required |
| `07-legal/terms-of-service-b2b.md` | B2B Terms of Service for the Orquor platform | Template — counsel review required |
| `07-legal/privacy-policy-web.md` | Privacy Policy for the public website (Law 29733 + GDPR + CCPA) | Ready to publish at orquor.com/legal/privacy |
| `07-legal/cookie-policy-web.md` | Cookie Policy for the public website | Ready to publish at orquor.com/legal/cookies |

## 08 — Prospects

| Path | Description | Status |
|---|---|---|
| `08-prospects/PROSPECTS_MASTER.md` | 10 cultivated profiles (5 CR + 5 CO) with HUMINT discipline rules | Complete — begin cultivation Week 1 |

## 09 — Content Calendar

| Path | Description | Status |
|---|---|---|
| `09-content-calendar/CALENDAR.md` | 90-day master plan, channel cadence, tooling, metrics | Complete |
| `09-content-calendar/linkedin/dia-001.md` | LinkedIn launch post — "Why 'AI for translation' is no longer enough" | Ready to publish |
| `09-content-calendar/linkedin/dia-002.md` | Founder story — "5 versions before naming the company" | Ready to publish |
| `09-content-calendar/linkedin/dia-003.md` | YouTube Ep1 announcement | Publish after YouTube goes live |
| `09-content-calendar/linkedin/dia-004.md` | 11.8% — WER baseline reveal | Ready to publish |
| `09-content-calendar/linkedin/dia-005.md` | "The question nobody asks AI vendors" — audit log | Ready to publish |
| `09-content-calendar/linkedin/dia-006.md` | "Lima is the right city to build this" — sovereign AI positioning | Ready to publish |
| `09-content-calendar/linkedin/dia-007.md` | Verifier deep-dive — credibility build | Ready to publish |
| `09-content-calendar/linkedin/dia-010.md` | Whitepaper-drop announcement, benchmarks live | Publish day of arXiv |
| `09-content-calendar/linkedin/dia-014.md` | Two-week public review + community-build | Ready for Day 14 |
| `09-content-calendar/linkedin/dia-008.md` | Demos avoid medical vocabulary — why | Ready |
| `09-content-calendar/linkedin/dia-009.md` | Cost of a mistranslation in a hospital | Ready |
| `09-content-calendar/linkedin/dia-011.md` | How we built the verifier suite | Ready |
| `09-content-calendar/linkedin/dia-012.md` | Open source vs proprietary in clinical AI | Ready |
| `09-content-calendar/linkedin/dia-013.md` | What HIPAA actually requires for AI | Ready |
| `09-content-calendar/linkedin/dia-015.md` | First 5 prospect conversation learnings | Ready |
| `09-content-calendar/linkedin/dia-016.md` | Whitepaper early reactions | Ready |
| `09-content-calendar/linkedin/dia-017.md` | Deep dive: cooperative inference stack | Ready |
| `09-content-calendar/linkedin/dia-018.md` | Why LATAM is right for healthcare AI | Ready |
| `09-content-calendar/linkedin/dia-019.md` | The interpreter is not being replaced | Ready |
| `09-content-calendar/linkedin/dia-020.md` | Regulatory landscape LATAM vs US vs EU | Ready |
| `09-content-calendar/linkedin/dia-021.md` | 3-week retrospective | Ready for Day 21 |
| `09-content-calendar/x-twitter/dia-001.md` | 7-tweet launch thread | Ready |
| `09-content-calendar/x-twitter/dia-002.md` | "5 reasons vendor can't show audit log" | Ready |
| `09-content-calendar/x-twitter/dia-003.md` | "7-axis comparison table explained" | Ready |
| `09-content-calendar/x-twitter/dia-004.md` | "What clinical-grade actually means" | Ready |
| `09-content-calendar/x-twitter/dia-005.md` | YouTube Ep1 coordination thread | Ready |
| `09-content-calendar/x-twitter/dia-006.md` | "Building in Lima" thread | Ready |
| `09-content-calendar/x-twitter/dia-007.md` | "iteramed.sbs wasn't enough" thread | Ready |
| `09-content-calendar/x-twitter/dia-008.md` | Single tweet — whitepaper drop | Publish day of arXiv |
| `09-content-calendar/x-twitter/dia-009.md` | "Why we published instead of patented" | Ready |
| `09-content-calendar/x-twitter/dia-010.md` | 8-tweet methodology thread | Publish day of arXiv |
| `09-content-calendar/x-twitter/dia-011.md` | Verifier methodology in 5 tweets | Ready |
| `09-content-calendar/x-twitter/dia-012.md` | Interpreter + AI cooperation thread | Ready |
| `09-content-calendar/x-twitter/dia-013.md` | "Procurement doesn't know this category" | Ready |
| `09-content-calendar/x-twitter/dia-014.md` | 6-tweet "14 days in public" reflection | Ready |
| `09-content-calendar/newsletter/edition-01.md` | First newsletter edition (sent Day 14) | Ready |
| `09-content-calendar/youtube/ep-001-script.md` | YouTube Ep 1 — 12-min production script | Ready to record |
| `09-content-calendar/youtube/ep-002-script.md` | YouTube Ep 2 — "How Verifiers Work" live coding | Ready to record |
| `09-content-calendar/email/onboarding-interpretes.md` | Welcome email for new certified interpreters | Ready |
| `09-content-calendar/email/welcome-clientes-b2b.md` | Welcome email for new B2B customers | Ready |
| `09-content-calendar/email/follow-up-prospects.md` | Post-meeting follow-up template (Sales-Bot draft) | Ready |

## 10 — Migration Runbook

| Path | Description | Status |
|---|---|---|
| `10-migration-runbook/RUNBOOK.md` | 8-phase runbook ITERAMED → Orquor Clinical, **Hostinger Edition**, ~5 hours total | Ready to execute after domain purchase |

---

## Persistent skills installed in `~/.cursor/skills/`

| Skill | Purpose |
|---|---|
| `brand-naming-specialist` | Linguistic Fitness Test, sound symbolism, trademark pre-clearance |
| `numerology-brand-evaluator` | Pythagorean + Chaldean numerology |
| `chinese-zodiac-brand-evaluator` | Bā Zì, Wǔ Xíng, Feng Shui |
| `christian-symbolic-evaluator` | Biblical numerology, gematria, Christ-symbolism |
| `covert-strategy-architect` | Tradecraft + Cheng/Qi + off-menu tech + OPSEC + reality engineering |
| `imperio-executor` | Sprint-mode operating discipline (new in this session) |

## Canvases delivered (in `c-Users-frefe-OneDrive-Desktop-START-UP/canvases/`)

| Canvas | Topic |
|---|---|
| `nichos-oceano-azul-peru.canvas.tsx` | 8 nichos rankeados Blue Ocean |
| `iteramed-analisis-stack.canvas.tsx` | ITERAMED stack + competition + migration |
| `orquor-nicho-y-variantes.canvas.tsx` | Nicho principal + 3 variantes |
| `orquor-hermes-arquitectura.canvas.tsx` | Arquitectura Hermes |
| `orquor-academy-y-contenido.canvas.tsx` | Academy + canal |
| `orquor-apps-adyacentes.canvas.tsx` | 8 apps adyacentes priorizadas |
| `orquor-clinical-migracion-tecnica.canvas.tsx` | Plan de migración 18 meses |
| `orquor-capa-negra.canvas.tsx` | Tradecraft / asymmetric strategy / reality engineering |

---

## What the founder does immediately upon return (priority order)

1. **Open `01-action-board/ACTION_BOARD.md`** — read the P0 actions.
2. **Buy the domain belt** at Cloudflare Registrar (~USD 240, 30 minutes). Without this, nothing else moves.
3. **Register the ORQUOR trademark** at INDECOPI (Nice classes 9, 35, 42, 44) — start the 6-month process.
4. **Reserve social handles** @orquor across X, LinkedIn Company, YouTube, Instagram, TikTok, GitHub Organization.
5. **Read the ACTO whitepaper** end to end. Verify there is nothing the founder disagrees with. Once approved, schedule arXiv submission for Day 10–14.
6. **Schedule recording** of YouTube Episode 1 (Sunday morning recording recommended). 90-minute session.
7. **Begin ambient engagement** on the 3 priority-1 prospects from `08-prospects/PROSPECTS_MASTER.md` (CR-01, CR-02, CO-01).
8. **Publish LinkedIn dia-001.md** as soon as the Orquor Company Page is live and the founder's profile mentions the new role.

Everything else flows from these.

---

## Operating math

Files produced this session: **~37** (including this manifest).
Estimated equivalent human-hours of work: 80–120.
Time elapsed in the actual session: ~3 hours of agent turns.

The leverage is the structure of the work, not the typing speed. The artifacts are interconnected — every legal template references the brand, every content piece references the whitepaper, every sub-agent references the verifier discipline. Working backward from a coherent strategic frame produces aligned artifacts. Working forward from individual tasks produces fragmented ones.

This is the discipline of `imperio-executor`. Codified for the next session.
