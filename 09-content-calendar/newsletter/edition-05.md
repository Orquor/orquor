# Orquor Newsletter — Edition 05

**Send date**: Day 70 · **Subject line**: "Where ORQUOR is going — the next 6 months" · **Preview text**: "Product milestones, regulatory filings, commercial pipeline, research publications, and the Orquor Academy expansion. October 2025 through March 2026."

---

Hello,

This edition is the roadmap. No narrative, no interview, no data tables. Just what we are building and why, in chronological order through March 2026.

If you have been reading since Edition 01, you have seen the category defined (ACTO), the verifier methodology published, the pilot data disclosed, and the physician perspective documented. This edition tells you what comes next.

The roadmap is organized into four parallel workstreams: Product, Regulatory, Commercial, and Research. They run concurrently. Dependencies are noted where they exist.

---

## October 2025 — Foundation phase

**Product.**

- Verifier suite reaches 100 verifiers. Pediatric weight-based dosing checker (V79–V82), pregnancy contraindication checker (V83–V86), and Quechua–Spanish code-switching detector (V87) go into production.
- Interpreter-UI latency sprint completes. Target: escalation-path latency p99 under 20 seconds, down from 58 seconds in the pilot. The sprint includes pre-flag context delivery (the interpreter sees the source, the flagged output, and the verifier's reason for flagging in a single view) and a hotkey-based correction interface to eliminate mouse-dependent workflows.
- Night-shift pilot begins at the Lima tertiary-care hospital. 20:00–08:00. Higher-acuity encounters, more trauma, more non-Spanish languages. If the day-shift pilot data holds on night shift, we will have 24-hour operational validation.

**Regulatory.**

- Formal submission to DIGEMID (Peru's drug and medical device regulatory agency) classifying ACTO as a clinical decision-support system (CDSS), not a medical device. This classification is critical: a CDSS classification means ACTO can be deployed without medical device registration, reducing time-to-market in Peru from 18 months to 6. Legal memorandum prepared by healthcare regulatory counsel in Lima.
- Preliminary classification inquiry filed with INVIMA (Colombia) and ANVISA (Brazil). Both agencies have CDSS classification pathways. The goal is a multi-country regulatory opinion by December.

**Commercial.**

- First paid deployment agreement signed. Terms under negotiation with the pilot hospital and one additional hospital in the same health network. Pricing model: per-encounter fee with volume discount tiers; no upfront license fee; no per-seat interpreter fee. The model aligns cost with usage and eliminates the barrier of upfront capital expenditure.
- Orquor Academy Cohort 01 begins. 28 participants selected from 214 applications. Curriculum: cooperative-inference architecture fundamentals, verifier design and calibration, medical ASR fine-tuning, and deployment operations. 12-week program. Tuition: waived for Cohort 01.

**Research.**

- Pilot data submitted to a peer-reviewed journal (target: JAMIA or Lancet Digital Health). The submission includes the full specialty-level breakdown, verifier performance by category, and a detailed appendix on the cooperative-inference architecture.
- Regional colloquial terminology registry (Peruvian coastal Spanish) released as open data on GitHub under CC-BY 4.0.

---

## November 2025 — Expansion phase

**Product.**

- Second obstetrics pilot goes live at a regional hospital in Cusco. Quechua–Spanish pairs predominate (estimated 60% of encounters). The goal is to validate the ASR and MT stack for Quechua at a clinically meaningful scale. COMET-22 target for Quechua: 0.85 (up from 0.74 in the Lima pilot).
- Pediatric ASR fine-tuning completes. The model is trained on 500 hours of consented pediatric clinical audio. Evaluation against the Lima pilot pediatric data (baseline Medical Word Error Rate of 5.1%). Target: Medical Word Error Rate below 4.0%.
- EHR integration module specification published. The module defines a FHIR R4-compliant interface for ACTO-to-EHR data flow: structured encounter note, source and translated utterances with timestamps, verifier flags and resolutions, audit log hash, and human-review sign-off. Published as an open specification so any EHR vendor can implement.

**Regulatory.**

- DIGEMID response expected. If CDSS classification is granted, Peru becomes the first country with a formal regulatory opinion on ACTO. The opinion will be published (redacted) and shared with INVIMA and ANVISA as precedent.
- GDPR and HIPAA compliance audit begins. External auditor engaged for a 6-week assessment of the ACTO data-handling pipeline, audit log storage, PHI minimization, and data residency compliance.

**Commercial.**

- Second paid deployment agreement targeted. Pipeline currently has 4 hospitals in active evaluation: 2 in Peru (Lima and Arequipa), 1 in Colombia (Bogotá), 1 in Mexico (CDMX). The Colombia and Mexico deployments depend on INVIMA and COFEPRIS regulatory opinions, respectively.
- Orquor Academy Cohort 02 applications open. Tuition: $1,200 for the 12-week program. Scholarships available for participants from LATAM public hospitals.

**Research.**

- Cultural-context verifier scoping project begins. Collaboration with Dr. Elena Vargas (pilot lead clinician) and a medical anthropologist from Universidad Peruana Cayetano Heredia. Deliverable: a taxonomy of cultural-concept-to-biomedical-concept mappings for Quechua and Aymara, and a prototype verifier that flags translations where cultural meaning is stripped.
- OpenTimestamps audit log specification published as an IETF Internet-Draft. The specification formalizes the cryptographic timestamping protocol used in the ACTO audit log. Publishing as an IETF draft signals that the protocol is open, inspectable, and not proprietary to ORQUOR.

---

## December 2025 through January 2026 — Validation phase

**Product.**

- Night-shift pilot concludes. Data published in Edition 08.
- Cusco obstetrics pilot completes first 60 days. Quechua COMET-22 evaluation published.
- Multi-site verifier calibration run. The verifier suite is recalibrated against data from two sites (Lima and Cusco) and three specialties (ER, obstetrics, internal medicine). Weights adjusted based on production error frequencies, not pilot estimates.

**Regulatory.**

- Multi-country regulatory dossier completed. Target countries: Peru, Colombia, Brazil, Mexico. The dossier includes the DIGEMID opinion, the pilot data, the verifier calibration methodology, and the GDPR/HIPAA audit results.
- First regulatory briefing with a U.S. agency (target: FDA Digital Health Center of Excellence). The briefing is exploratory — no U.S. deployment planned before Q3 2026 — but early engagement establishes the regulatory posture and signals seriousness to LATAM regulators.

**Commercial.**

- Third paid deployment. Target: first non-pilot-hospital deployment — a new customer that was not part of the original pilot.
- Orquor Academy Cohort 02 begins. 40 participants. Three tracks: deployment engineering, verifier design, and clinical operations.

**Research.**

- Peer-reviewed pilot paper under review (expected 8–12 week review cycle).
- Quechua clinical ASR model released under research license. Trained on the Cusco pilot data plus publicly available Quechua corpora. The first open-source clinical ASR model for Quechua.

---

## February through March 2026 — Scale phase

**Product.**

- ACTO platform reaches general availability (GA) for Spanish–English clinical translation in Peru and Colombia, pending regulatory clearance. GA means: documented API, SLA-backed uptime, 24/7 support, and a self-service deployment option for hospitals with in-house IT.
- Multi-language expansion begins. Aymara–Spanish and Portuguese–Spanish language pairs enter the cooperative-inference stack. Both languages are present in LATAM border-region hospitals and currently have zero AI-based clinical translation coverage.
- Verifier suite reaches 130 verifiers. New categories: multi-language code-switching, pediatric growth-chart reference checking, and drug-interaction cross-referencing against local formularies.

**Regulatory.**

- INVIMA and ANVISA opinions expected. If both are favorable, Colombia and Brazil become deployable markets.
- COFEPRIS (Mexico) preliminary opinion expected. Mexico is the largest single-market opportunity in LATAM for clinical translation (public hospital system covers 70 million people). The regulatory pathway in Mexico is the most complex in the region and is on the critical path for commercial scale.

**Commercial.**

- Pipeline target: 10 hospitals under active evaluation or deployment across 4 countries.
- Revenue target: undisclosed until first full quarter of paid deployments, but the per-encounter model means revenue scales linearly with encounter volume. Internal projections will be shared with investors and will not be published in this newsletter.
- Orquor Academy becomes self-sustaining. Cohort 03 applications open. Alumni network launches.

**Research.**

- Multi-site clinical trial protocol submitted for IRB approval. The trial will compare ACTO-assisted encounters against standard-of-care interpreter-mediated encounters across three sites and four specialties. Primary endpoint: rate of clinically significant errors reaching the EHR. Secondary endpoints: encounter duration, patient satisfaction, interpreter utilization. Target enrollment: 2,000 encounters.
- Cultural-context verifier prototype published. Open-source implementation released alongside the taxonomy.

---

## What is NOT on this roadmap

Three things I am explicitly not committing to, and why.

**1. Direct-to-patient translation (e.g., a consumer app for medical visits).** The clinical risk profile of patient-facing translation without a clinician in the loop is fundamentally different from clinician-mediated translation. ACTO is architected for the clinical setting, with the physician as the final authority. A consumer product would require a different architecture, different verifier suite, and different regulatory posture. Not in 2025–2026.

**2. Non-clinical verticals (legal, financial, diplomatic).** The ACTO architecture — cooperative inference with verifier suites and cryptographic audit logging — is generalizable. But the verifier suite, terminology registries, and regulatory posture are clinical. Expanding to non-clinical verticals would require building domain-specific verifier suites from scratch. Not before 2027.

**3. U.S. market deployment.** The U.S. regulatory pathway for AI-based clinical translation is uncertain and likely to involve FDA 510(k) or De Novo classification, which is a 12-to-24-month process. LATAM has a faster regulatory pathway, higher need (more language pairs, fewer interpreters per capita), and less competition. LATAM-first is the strategy through 2026. U.S. market entry is a 2027 conversation.

---

## The one variable that changes everything

Regulatory classification. If DIGEMID, INVIMA, and ANVISA all classify ACTO as a CDSS, the time-to-market in LATAM is 6 months. If any one of them classifies ACTO as a medical device, time-to-market in that country extends to 18–24 months, and the commercial pipeline shifts accordingly.

The CDSS argument is strong: ACTO does not diagnose, does not prescribe, does not make clinical decisions. It translates and verifies. The physician remains the decision-maker. The audit log proves it.

But regulatory agencies are unpredictable by design. We are preparing for both outcomes. The multi-country dossier is structured so that a favorable opinion in one country creates precedent pressure in others. That is the playbook.

---

## What is next

- **Newsletter Edition 06**: the night-shift pilot results and the interpreter UI latency sprint data.
- **YouTube Episodes 9–12**: Quechua ASR walkthrough, verifier calibration methodology, EHR integration demo, and a regulatory attorney on the LATAM CDSS pathway.
- **Second paid deployment announcement** (NDA-permitting).
- **Orquor Academy Cohort 02 applications open**: reply to this email for the application link.

---

## Reply with one of these

If you have a single sentence, reply with any of these and it goes directly to me:

- "I want to pilot ACTO at [hospital name]"
- "I want to discuss the regulatory pathway in [country]"
- "I want to join Orquor Academy Cohort 02"
- "Disagreement on [X]" — the most useful feedback
- "Send me the FHIR integration spec when it publishes"

Thank you for reading. The next six months are the transition from pilot to product. I will document every step.

Freddy
Founder, Orquor
freddy@orquor.com · orquor.com
Lima, Peru

---

*You are receiving this because you subscribed at orquor.com/news. To stop receiving these, [unsubscribe here].*
