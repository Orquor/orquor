# Orquor Newsletter — Edition 03

**Send date**: Day 42 · **Subject line**: "The pilot data is in" · **Preview text**: "Five specialties, 1,247 patient encounters, 28,000+ utterances. The first hospital pilot results, what the verifier suite caught, and what we are changing."

---

Hello,

The first hospital pilot of ACTO concluded last week. This edition is the full disclosure of what we found.

The pilot ran for 21 days at a tertiary-care hospital in Lima — 1,247 patient encounters across five specialties: emergency medicine, internal medicine, obstetrics, pediatrics, and orthopedics. Three certified medical interpreters staffed the escalation tier. All sessions were consented under an IRB-approved protocol. The hospital has approved the publication of aggregate data.

This is not preliminary. This is production data from a live hospital. The numbers below will go into the Q3 whitepaper appendix. You are seeing them first.

---

## Pilot design

**Duration**: 21 consecutive days.
**Shifts**: 08:00–20:00 (day shift only; night-shift pilot planned for Q4).
**Specialties**: emergency medicine (34% of encounters), internal medicine (27%), obstetrics (18%), pediatrics (13%), orthopedics (8%).
**Language pairs**: Spanish–English (96%), Spanish–Quechua (4%).
**Interpreters**: 3 certified medical interpreters on rotation for escalation tier.
**Verifier suite**: 78 verifiers (18 added post-pilot-02 based on internal findings).
**IRB**: Protocol approved. All patients consented. Data publication approved by hospital ethics committee.

---

## Aggregate results

| Metric | Result | Baseline |
|---|---|---|
| Encounters | 1,247 | — |
| Utterances | 28,412 | — |
| Routed entirely through AI | 81.7% | — |
| AI + second-pass MT retry | 10.1% | — |
| Escalated to human interpreter | 8.2% | — |
| Medical Word Error Rate (overall) | 3.8% | 11.8% (Whisper Large v3) |
| Medical Word Error Rate (pediatrics) | 5.1% | 14.3% |
| COMET-22 (clinical Spanish) | 0.89 | — |
| COMET-22 (clinical Quechua) | 0.74 | — |
| Latency p50 | 0.7 s | — |
| Latency p99 | 2.1 s | — |
| Verifier precision on escalation | 96.3% | — |
| Verifier recall on critical errors | 100% | — |
| Human interpreter correction rate | 97.1% | — |
| False-positive escalations | 3.7% | — |
| Sent-to-EHR without human review | 91.8% | — |

---

## What the verifier suite caught

The 78 verifiers flagged 2,327 utterances during the pilot (8.2% of total). Of those:

- **Dosage safety verifiers** (14): flagged 312 utterances. 47 were true critical errors — a dosage magnitude mismatch that would have reached the EHR without the verifier. Five of those 47 would have constituted a standard-of-care breach.
- **Allergy and contraindication verifiers** (10): flagged 89 utterances. 12 were true positives involving a contraindicated medication introduced in translation.
- **PHI protection verifiers** (8): flagged 41 utterances. 6 contained patient names in the translation output that were not present in the source utterance — a model hallucination.
- **Terminology and register verifiers** (22): flagged 1,412 utterances. The majority were register-drift detections (formal to colloquial mid-session) and terminology substitutions that did not change clinical meaning but would have degraded EHR quality.
- **Structural and fluency verifiers** (24): flagged 473 utterances. Most were sentence-boundary errors that could produce ambiguity in clinical context.

The highest-impact finding: **five dosage errors blocked in 21 days**. If ACTO were not in the loop, those five translations would have entered the EHR. The verifier suite made the difference between a standard-of-care breach and a corrected translation.

---

## Specialty-level breakdown

**Emergency medicine** — 34% of encounters, but 52% of escalations. The ER is noisy, fast, and patients use non-standard colloquial variants for anatomical terms and symptoms. The verifier suite's false-positive rate was highest in ER (5.2%) for this reason. Expanding the terminology registry with regional colloquial variants is the top priority for Q4.

**Pediatrics** — 13% of encounters, but the highest Medical Word Error Rate (5.1%). Pediatric encounters involve parent-as-proxy communication, higher rates of diminutives and non-standard dosage formulations (liquid suspensions, weight-based dosing), and more emotional content. The ASR component of the cooperative stack needs pediatric-specific fine-tuning.

**Obstetrics** — 18% of encounters, lowest Medical Word Error Rate (2.4%). Predictable clinical vocabulary, structured encounter flow, high repetition rate of standard phrases. This is the most favorable specialty for AI-first routing. We are accelerating the obstetrics expansion.

**Internal medicine and orthopedics** — within expected ranges. No specialty-specific anomalies requiring architecture changes.

---

## What we are changing as a result

**1. Terminology registry regionalization.** The ER false positives were concentrated in colloquial anatomical terms (e.g., "la boca del estómago" for epigastrium, "el huesito de la muñeca" for carpal bone). We are building a regional colloquial-to-standard terminology map, starting with Peruvian coastal Spanish, and releasing it as open data so other LATAM implementations can contribute.

**2. Pediatric ASR fine-tuning.** Pediatric encounters will route through a pediatric-specific ASR model fine-tuned on 500 hours of consented pediatric clinical audio. This is a 90-day project starting next week. The model will be released under research license.

**3. Obstetrics acceleration.** Given the favorable metrics, we are prioritizing two additional obstetrics pilots in Q4 — one in Lima, one in a high-altitude regional hospital in Cusco where Quechua–Spanish pairs predominate.

**4. Night-shift pilot.** Day-shift data covers 08:00–20:00. Night-shift encounters have different characteristics: fewer encounters per hour, but higher acuity per encounter, higher proportion of trauma, and more non-Spanish languages (Quechua, Aymara, and in border regions, Portuguese). Night-shift pilot targeted for Q4.

**5. Verifier suite expansion.** 78 verifiers going to approximately 100 by end of Q4. Top candidate additions: pediatric weight-based dosing checker, pregnancy contraindication checker, and multi-language code-switching detector for Quechua–Spanish utterances.

---

## What this data does and does not say

This data says ACTO can operate in a live hospital, with real patients, across five specialties, and catch critical errors before they reach the EHR. That is what we set out to demonstrate, and the data supports it.

This data does not say ACTO is ready for deployment without human escalation infrastructure. The 8.2% escalation rate is real and necessary. The 3.7% false-positive rate is acceptable but must decline below 2% before we can recommend reducing interpreter staffing ratios. The pediatric numbers indicate domain-specific work remains.

This data also does not say anything about Quechua performance at scale. The 4% of encounters in Spanish–Quechua showed a COMET-22 of 0.74, which is directionally useful but far below the 0.85 threshold we require for EHR-eligible translation. More data, more fine-tuning, and more Quechua-speaking interpreters in the escalation pool are needed.

---

## What is next

- **Newsletter Edition 04**: interview with Dr. [Name], the lead clinician on the pilot, on what the verifier data means from a physician's perspective.
- **YouTube Episode 06**: walkthrough of the five blocked dosage errors — what the source said, what the model output, what the verifier caught, and what reached the EHR after correction.
- **Second hospital pilot** (Q4): two obstetrics pilots, one night-shift pilot, and pediatric ASR fine-tuning.
- **Whitepaper Q3 appendix**: full pilot data, verifier-suite performance by specialty, and the regional terminology registry.
- **Orquor Academy Cohort 01**: applications close Day 60. If you have not applied, reply to this email.

---

## Reply with one of these

If you have a single sentence, reply with any of these and it goes directly to me:

- "I want to pilot ACTO at [hospital name]"
- "I want access to the pilot dataset under research license"
- "I want to join Orquor Academy Cohort 01"
- "Disagreement on [X]" — the most useful feedback

Thank you for reading.

Freddy
Founder, Orquor
freddy@orquor.com · orquor.com
Lima, Peru

---

*You are receiving this because you subscribed at orquor.com/news. To stop receiving these, [unsubscribe here].*
