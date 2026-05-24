# Orquor — Content Calendar 90 Days

Adapted from Frente 3 (`orquor-academy-y-contenido.canvas.tsx`) + Capa Negra's memetic-dominance pipeline. Content engine is hybrid: founder-face (cámara iPhone 15 Pro + Rode + 2 luces) for authority, Synthesia + ElevenLabs for scale.

## Strategic objective for 90 days

Define the ACTO category in the public conversation. By Day 90, three industry voices outside Orquor cite "Auditable Clinical Translation Orchestration" without prompting. Whitepaper has crossed 3,000 downloads. Orquor LinkedIn followers crossed 1,500.

## Cadence per channel

| Channel | Frequency | Format | Length | Purpose |
|---|---|---|---|---|
| YouTube | 1 long-form per week + 2 shorts | 8-15 min long-form, 60s shorts | ~14 publications | Authority + searchable archive |
| LinkedIn | 4 per week | Text-first, 600-1,500 chars + occasional carousel | ~52 posts | B2B conversion + cultivation |
| X | 7 per week (mix of single-tweets + threads) | Threads of 4-7 tweets | ~90 publications | Amplification + opinion |
| Newsletter | 1 every 2 weeks | 700-1,200 words | 6 editions | Direct-to-list capture |
| TikTok/Reels | 4 per week, mostly repurposed from YouTube shorts | 60-90s vertical | ~52 publications | Reach + algorithm discovery |
| Podcast guesting | 1-2 per month | 30-60 min | 4-6 episodes | Authority transfer |

## 90-day master calendar

### Weeks 1-2 — Foundation (Days 1-14): The category drop

| Day | Channel | Topic | Status |
|---|---|---|---|
| 1 | LinkedIn | "Why 'we use AI for translation' is no longer enough in healthcare" — first post under Orquor brand | drafted in `linkedin/dia-001.md` |
| 1 | X | Thread: "5 trade-offs nobody publishes about medical interpretation in 2026" | drafted in `x-twitter/dia-001.md` |
| 2 | LinkedIn | Personal story: 5 versions of Orquor, what each shipped | drafted in `linkedin/dia-002.md` |
| 3 | YouTube | Episode 1: "What is Auditable Clinical Translation Orchestration?" — 12 min | script in `youtube/ep-001-script.md` |
| 3 | LinkedIn | Announcement of YouTube ep 1 + 3-paragraph teaser | drafted in `linkedin/dia-003.md` |
| 5 | X | Thread: "ACTO in 7 tweets — the technical category that should exist by now" | drafted in `x-twitter/dia-005.md` |
| 7 | LinkedIn | "I built our verifier suite using the same methodology I used to evaluate agents at scale for major labs. Here's what most healthcare-AI vendors are skipping." | drafted in `linkedin/dia-007.md` |
| 10 | YouTube | Episode 2: "How verifiers work — a 10-minute walkthrough with code" | outline |
| 12 | LinkedIn | Comparison post: LanguageLine vs AI-only vs ACTO, table format | outline |
| 14 | Newsletter | Edition 1: "The category called ACTO" — sets context for the next 12 weeks | outline |

### Weeks 3-4 — The whitepaper drop (Days 15-28)

Whitepaper goes live on arXiv + blog.orquor.com on Day 17. The week is choreographed around the publication.

| Day | Channel | Topic |
|---|---|---|
| 15 | LinkedIn | "Whitepaper preview — in 48 hours we publish the spec for ACTO publicly" |
| 16 | X | Thread: 7 tweets summarizing the whitepaper, with figures |
| 17 | All channels | **Whitepaper drop day.** LinkedIn long-form post linking to arXiv. X thread. YouTube episode 3 introducing whitepaper. Newsletter edition 2. |
| 18 | LinkedIn | Founder reflection: why we are publishing this rather than keeping it proprietary |
| 19 | LinkedIn | Comment-mining: questions readers asked, with answers |
| 22 | X | Quote-tweets of any voices that picked up the whitepaper |
| 24 | YouTube | Episode 4: "Why we wrote the ACTO whitepaper instead of patenting the moat" |
| 28 | Newsletter | Edition 3: "First week reactions to ACTO" — community-building |

### Weeks 5-8 — Authority compounding (Days 29-56)

Switch from category-launch to authority-building. Each week has a theme.

| Week | Theme | Anchor content |
|---|---|---|
| 5 | "Why outcome-based verifiers" | YouTube ep 5: deep dive on verifier design, with sample code |
| 6 | "Why human-in-the-loop matters" | YouTube ep 6: the cooperative inference stack, with interpreter Camila guest |
| 7 | "Why we built it in Lima" | YouTube ep 7: LATAM sovereign AI story; podcast guesting on Endeavor Perú |
| 8 | "Why audit logs change the legal posture" | YouTube ep 8: with healthcare attorney, regulatory deep-dive |

LinkedIn 3-4 posts per week, X 7 per week. Each week anchors around the theme.

### Weeks 9-12 — Demand generation + Academy soft launch (Days 57-90)

Orquor Academy first cohort opens applications Day 60.

| Day range | Anchor |
|---|---|
| 57-63 | Academy waitlist landing live. "Want to learn how I evaluate LLMs for healthcare? Join Cohort 1" |
| 64-77 | Daily-life-of-an-AI-trainer YouTube series (5 episodes). Direct positioning for Academy. |
| 78-90 | Cohort 1 enrollment closes. Final push. Two webinar sessions live with Q&A. |

## Workflow with Content-Bot (HERMES sub-agent)

1. **Founder records once** per week (Sunday morning): 1 long-form YouTube (10-15 min) + 1 LinkedIn-text-draft + 1 newsletter-draft.
2. **Content-Bot derives** the rest automatically:
   - Transcript → 3 LinkedIn posts → 7 X singletons or 1 thread → 4 vertical shorts → 1 newsletter excerpt
3. **Founder reviews** drafts on Monday morning (1 hour).
4. **Content-Bot schedules** the week. Posts go out per the calendar.
5. **Engagement monitoring** by Content-Bot daily. Replies drafted for founder approval.

## Tooling stack

| Function | Tool | Cost (USD/mo) |
|---|---|---|
| Scheduling | Buffer | 12 |
| Video editing | Descript | 30 |
| Avatar generation (low-effort weeks) | Synthesia Starter | 22 |
| Voice clone | ElevenLabs Starter | 22 |
| Captions | Captions.ai | 20 |
| Analytics | Plausible (self-host) or Fathom | 14 |
| Email + landing | ConvertKit + Resend | 49 + 20 |
| Community | Skool + Discord (free) | 99 |
| **Total** | | **~288/month** |

## Metrics tracked weekly

- LinkedIn followers (target: +200/week by Week 8)
- LinkedIn posts engagement rate (target: 4%+)
- YouTube subscribers (target: 100 in 90 days)
- X followers (target: +500 in 90 days)
- Whitepaper downloads (target: 3,000)
- Newsletter list size (target: 1,200)
- Sales-qualified leads attributed to content (target: 12)
- Time spent by founder on content (target: ≤ 12 hours/week, dropping to 8 by Week 8)
