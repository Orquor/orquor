# Orquor Hermes — Shared MEMORY.md

Persistence layer for cross-sub-agent feedback and decisions. Adapted from OpenClaw Atlas v4 discipline. New entries are inserted at the top of the Historical section.

---

## Canonical rules (do not modify without changelog)

- **outcome_only**: Verifiers evaluate final outputs, not intermediate steps. If feedback pushes to trace-based evaluation, mark CONTESTED.
- **positive_language_signed_weight**: Verifier phrasing describes the desired behavior with positive language; use signed weight (negative for violations). Do not flip polarity.
- **atomic_verifiers**: Each verifier checks one outcome property. Composite verifiers obscure failure attribution and are forbidden.
- **at_least_one_negative**: Every verifier suite must contain at least one negative verifier (weight < 0) that detects disallowed content or behavior.
- **memory_natural_request**: MEMORY entries are written when a feedback event occurs naturally, not because the orchestrator was told to log.
- **verifiers_pytest_form**: Verifiers are pytest test functions. Same function form across Hermes. Maintain identity for replay.
- **failure_justifications_three_areas**: When recording a failure, three areas must be documented: (1) why correct, (2) why present, (3) what model did wrong.
- **single_turn_no_message_after**: Single-turn sub-agent invocations never use mid-stream message after the initial prompt. Contaminates the trajectory.
- **no_start_fresh_during_session**: During an active operation session, do not Start Fresh. Either roll back with audit trail or proceed; never silently reset state.

---

## Lessons learned — cross-task patterns

### Pattern: ambient engagement precedes outreach by 30+ days
Across CR and CO assets, when ambient engagement (comments on their posts, sharing of relevant material) precedes outreach by at least 30 days, reply rate increases by an order of magnitude. Cold DMs without ambient engagement have ~2% reply rate; warm-cultivated DMs have ~28%. Maintain this discipline across Sales-Bot.

### Pattern: verifier failures cluster around dosage units
In production, ~40% of verifier failures involve numeric units (mg vs mcg, mL vs cc). Strengthen V2 with a stricter unit normalization layer.

### Pattern: Compliance items become critical at T-30 days
Compliance-Watcher should escalate at T-30 days, not T-7. T-7 leaves no negotiation room.

---

## Historical feedback (most recent first)

### 2026-05-24T08:50:13.152345+00:00 — content_review_required — Content

- **Source**: content_review_required
- **Section affected**: content_pipeline
- **Feedback literal**: > CW-2026-W21-LI-01 (linkedin): 'Why 'we use AI for translation' is no longer enough in healthcare' awaits human review
- **Canonical rule**: outcome_only
- **Verdict**: ALIGNED
- **Action taken**: awaiting founder/CMO sign-off
- **Reasoning**: Mandatory human review before publish.

---

### 2026-05-24T08:50:13.136113+00:00 — compliance_alert — Compliance-Watcher

- **Source**: compliance_alert
- **Section affected**: Ley 29733
- **Feedback literal**: > LEY-29733-PRIV-001: Register privacy policy with DGAJ-MINJUS (21 days)
- **Canonical rule**: outcome_only
- **Verdict**: ALIGNED
- **Action taken**: alert raised; awaiting founder/counsel action
- **Reasoning**: Item severity=watch, status=approaching.

---

### 2026-05-24T08:50:13.134793+00:00 — compliance_alert — Compliance-Watcher

- **Source**: compliance_alert
- **Section affected**: HIPAA
- **Feedback literal**: > HIPAA-BAA-LAMBDA-001: Sign BAA with Lambda Labs (US-West A100 reserved) (14 days)
- **Canonical rule**: outcome_only
- **Verdict**: ALIGNED
- **Action taken**: alert raised; awaiting founder/counsel action
- **Reasoning**: Item severity=critical, status=approaching.

---

### 2026-05-24T08:50:13.119420+00:00 — cultivation_event — Sales

- **Source**: cultivation_event
- **Section affected**: sales_pipeline
- **Feedback literal**: > Asset CR-02 (CIMA San José) at stage signaled. Notes: Sent DM asking about audit log feature. Reply drafted.
- **Canonical rule**: outcome_only
- **Verdict**: ALIGNED
- **Action taken**: Reply with substance. No pitch. Ask one elicitation question.
- **Reasoning**: Stage advancement evaluated against HUMINT cultivation discipline.

---

### 2026-05-24T08:50:13.102873+00:00 — recruitment_hold — Recruiter

- **Source**: recruitment_hold
- **Section affected**: interpreter_pipeline
- **Feedback literal**: > Candidate C-2026-042 (Carlos Mendieta) held: Score between thresholds — human review
- **Canonical rule**: failure_justifications_three_areas
- **Verdict**: ALIGNED
- **Action taken**: awaiting human supervisor review
- **Reasoning**: Score between thresholds or missing video; cannot auto-decide.

---

### 2026-05-24T08:50:13.102873+00:00 — osint_patent — Watchtower

- **Source**: osint_patent
- **Section affected**: market_intelligence
- **Feedback literal**: > Trademark filed for "ClinicalVoice" in Class 9 — possible healthcare pivot.
- **Canonical rule**: outcome_only
- **Verdict**: ALIGNED
- **Action taken**: watching
- **Reasoning**: Source: USPTO TESS, target: Wordly

---

### 2026-05-24T08:50:13.086129+00:00 — osint_rfp — Watchtower

- **Source**: osint_rfp
- **Section affected**: market_intelligence
- **Feedback literal**: > EsSalud published RFP for medical interpretation services, deadline 30 days.
- **Canonical rule**: outcome_only
- **Verdict**: ALIGNED
- **Action taken**: signal recorded for founder review
- **Reasoning**: Source: OSCE Perú, target: Peru Lima private hospitals

---

### 2026-05-24T08:50:13.086129+00:00 — osint_departure — Watchtower

- **Source**: osint_departure
- **Section affected**: market_intelligence
- **Feedback literal**: > Director of AI Strategy departed after 14 months — internal AI traction may be stalled.
- **Canonical rule**: outcome_only
- **Verdict**: ALIGNED
- **Action taken**: watching
- **Reasoning**: Source: LinkedIn, target: LanguageLine Solutions

---

### 2026-05-24T08:50:13.086129+00:00 — osint_hire — Watchtower

- **Source**: osint_hire
- **Section affected**: market_intelligence
- **Feedback literal**: > Hired VP Product from Epic Systems — likely EHR integration push.
- **Canonical rule**: outcome_only
- **Verdict**: ALIGNED
- **Action taken**: watching
- **Reasoning**: Source: LinkedIn, target: Cloudbreak Health

---

(Empty initially. Entries are inserted here by sub-agents at runtime.)
