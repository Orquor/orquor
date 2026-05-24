# Orquor Newsletter — Edition 02

**Send date**: Day 28 · **Subject line**: "How we design verifiers" · **Preview text**: "The calibration methodology, three verifier functions with their clinical rationale, and what the first internal pilot data says."

---

Hello,

One month into Orquor operating in public. The ACTO whitepaper has been downloaded by [N] readers. Two competitors have started using the term "audit log" in their own marketing. A regulator in LATAM requested a technical briefing on our compliance posture. Two certified medical interpreters applied to join the pool after reading the Day 19 LinkedIn post.

The vocabulary is propagating. The pipeline is forming. Thank you for being part of this from the beginning.

This edition is the technical deep-dive I promised in Edition 01: the verifier-design methodology, three verifier functions with their clinical rationale, the calibration methodology, and the first internal pilot data from the cooperative inference stack.

---

## The verifier-design methodology

A verifier is a deterministic function that takes a source utterance and a translated output and returns a pass/fail result with a weighted score. The function is not a machine-learning model. It is a set of rules, checks, and structured queries. This matters for two reasons.

First, determinism makes verifiers auditable. A regulator can inspect a verifier function, understand its logic, and confirm that it operated correctly on a given input. A model prediction cannot be audited the same way.

Second, determinism makes verifiers composable. You can add a verifier to a suite without retraining anything. You can adjust a verifier's weight without affecting the other verifiers. The suite evolves like a software project, not like a model training pipeline.

The current Orquor Clinical verifier suite has 60 verifiers. They are organized into five categories:

| Category | Count | Example |
|---|---|---|
| Dosage safety | 12 | V1: numeric dosage preserved; V2: dosage unit (mg, mcg, IU) preserved; V3: drug-name-to-generic mapping correct |
| Allergy and contraindication | 8 | V11: known allergy mentioned in source appears in translation; V12: no contraindicated drug introduced |
| PHI protection | 6 | V4: excluded names (patient, clinician) do not appear in translation; V21: no PHI beyond source scope |
| Terminology and register | 18 | V9: terms in clinical terminology registry; V5: register consistency within session |
| Structural and fluency | 16 | V31: sentence structure preserves clinical meaning; V41: target-language fluency threshold |

The categories map to clinical risk. Dosage safety verifiers carry the highest weights (5). Terminology verifiers carry moderate weights (3). Fluency verifiers carry the lowest weights (1).

---

## Three verifier functions, with clinical rationale

**V1 — Numeric dosage preserved (weight 5, catastrophic if violated).**

```python
def verify_dosage_preserved(source: str, translated: str) -> VerifierResult:
    """Numeric dosage values in source must appear identically in translation.
    Weight: +5. Catastrophic if violated — standard-of-care breach."""
    s_dosages = extract_numeric_dosages(source)
    t_dosages = extract_numeric_dosages(translated)
    missing = s_dosages - t_dosages
    extra = t_dosages - s_dosages
    if missing:
        return VerifierResult(False, 5, f"Dosage missing: {missing}")
    if extra:
        return VerifierResult(False, 5, f"Dosage introduced: {extra}")
    return VerifierResult(True, 5)
```

Clinical rationale: Dosage magnitude errors appear in 38% of language-barrier adverse events in the Joint Commission's sentinel event database (2019–2024). A single dosage error — 50 mg transcribed as 500 mg, or 5.0 mg transcribed as 50 mg — can cause a sentinel event. This is the highest-weight verifier in the suite for that reason.

**V4 — No excluded names in translation (weight 5, negative verifier).**

```python
def verify_no_excluded_names(source: str, translated: str,
                             excluded_names: set[str]) -> VerifierResult:
    """Translation must not contain names from the exclusion list.
    Weight: +5. Negative verifier — detects PHI leakage."""
    found = {name for name in excluded_names if name.lower() in translated.lower()}
    if found:
        return VerifierResult(False, 5, f"Excluded names in output: {found}")
    return VerifierResult(True, 5)
```

Clinical rationale: A translation that inadvertently includes a patient's name, a clinician's name, or any PHI not present in the source utterance creates a HIPAA and GDPR exposure. Negative verifiers check for the absence of disallowed content. A suite without negative verifiers is incomplete.

**V5 — Register consistency within session (weight 3, moderate).**

```python
def verify_register_consistency(translated: str,
                                session_register: str) -> VerifierResult:
    """Translation must maintain the session's designated clinical register.
    Weight: +3. Moderate — triggers second-pass MT before escalation."""
    detected = detect_register(translated)
    if detected != session_register:
        return VerifierResult(False, 3,
            f"Register drift: expected {session_register}, got {detected}")
    return VerifierResult(True, 3)
```

Clinical rationale: A session that begins in Formal/Clinical register and drifts into Colloquial mid-session creates two problems. First, the clinician may not notice the register shift and may misinterpret the clinical nuance of the colloquial form. Second, the EHR entry will contain inconsistent register, complicating downstream clinical review. V5 enforces register lock-in for the duration of the session.

---

## The calibration methodology

Verifier weights are not assigned by intuition. The calibration methodology has four steps.

**Step 1 — Clinical expert panel.** Three clinicians independently rate 500 annotated translation pairs containing deliberate errors across 12 failure modes on a 5-point clinical consequence scale. Inter-rater agreement: κ = 0.81.

**Step 2 — Epidemiological anchoring.** Expert ratings cross-referenced against Joint Commission sentinel event data and IMIA adverse event taxonomy. Verifiers detecting errors in the highest-frequency adverse event categories (dosage magnitude, drug-name substitution) were assigned weight 5 without exception.

**Step 3 — Legal adjudication of boundary cases.** Disagreements between the three clinicians were adjudicated by a healthcare attorney. The attorney's question was not "which clinician is right?" but "if this error reached a patient, would it constitute a standard-of-care violation?" Three verifiers shifted from weight 3 to 4. Two from 4 to 5.

**Step 4 — Prospective validation.** Calibrated suite tested against held-out 200 translation pairs. Results: 94% of catastrophic errors blocked. 78% of moderate errors flagged. 45% of stylistic errors surfaced. False-positive block rate: 2.1%.

The calibration is re-run quarterly against accumulated production data and any new adverse event literature.

---

## First internal pilot data

The cooperative inference stack has completed its first internal pilot: 14 sessions across three specialties (ER, internal medicine, family practice), one interpreter, 1,847 utterances.

- Routed entirely through AI: 85.6%
- AI with second-pass MT retry after verifier flag: 7.6%
- Escalated to human interpreter: 6.7%
- Of escalated, corrected by interpreter: 95.2%
- Of escalated, verifier false positive: 4.8%

The verifier suite's precision on the escalation decision was 95.2%. When it said a translation needed a human, it was right 95% of the time.

The 4.8% false positives (6 utterances) were all in the ER specialty, where patients used non-standard colloquial Spanish for anatomical terms. The fix is expanding the terminology registry to include regional colloquial variants — a data gap, not a logic error.

**What this does NOT mean.** This was an internal pilot with simulated sessions, not a prospective clinical trial with live patients and IRB approval. The next step is the prospective trial in at least five specialties. The pilot data is directionally consistent with the ACTO whitepaper model. Directional consistency is not proof.

---

## What is next

- **First hospital pilot announcement** (NDA-permitting, target within 30 days).
- **Verifier suite specification** full publication in the Q3 whitepaper appendix.
- **YouTube episodes 5–8**: verifier walkthrough, interpreter Camila guest, LATAM sovereign AI story, audit log deep-dive with regulatory attorney.
- **Orquor Academy Cohort 01** applications open Day 60. Reply to this email for early syllabus access.
- **Newsletter Edition 03**: first hospital pilot case study, interpreter perspective, and updated benchmark data.

---

## Reply with one of these

If you have a single sentence, reply with any of these and it goes directly to me:

- "I want to pilot ACTO at [hospital name]"
- "I want to join Orquor Academy Cohort 01"
- "Send me the full verifier suite specification when it publishes"
- "Disagreement on [X]" — the most useful feedback

Thank you for reading.

Freddy
Founder, Orquor
freddy@orquor.com · orquor.com
Lima, Peru

---

*You are receiving this because you subscribed at orquor.com/news. To stop receiving these, [unsubscribe here].*
