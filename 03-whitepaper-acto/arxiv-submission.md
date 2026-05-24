---
# arXiv Submission Metadata
# This file contains the formatted abstract, metadata, and suggested categories
# for submitting this paper to arXiv.org.
---

## Metadata

- **Title:** Auditable Clinical Translation Orchestration: A Verifier-Backed Approach to Real-Time Medical Language Bridging
- **Authors:** Freddy Rojas (Orquor)
- **Date:** 2026
- **License:** arXiv.org perpetual, non-exclusive license (default)
- **Comments:** 8 pages, 4 tables, 1 code appendix. Preliminary benchmark results.

## Suggested arXiv Categories

| Priority | Category | Description |
|----------|----------|-------------|
| **Primary** | `cs.CL` | Computation and Language — machine translation, speech recognition, NLP for clinical text |
| Secondary | `cs.CR` | Cryptography and Security — cryptographic timestamping, audit log integrity, tamper-evident protocols |
| Secondary | `cs.CY` | Computers and Society — healthcare regulation, HIPAA, GDPR, LGPD, data privacy law |
| Tertiary | `cs.SD` | Sound — automated speech recognition (ASR) component |
| Tertiary | `cs.HC` | Human-Computer Interaction — human-in-the-loop clinical workflows |

**Rationale:** Our primary contribution is a new technical category for auditable clinical translation pipelines, combining advances in machine translation (NLP), cryptographic audit logging (crypto/security), and healthcare regulation (society). `cs.CL` is the best primary fit because the core technical innovations — verifier-backed translation, register-adaptive MT, and WER/COMET benchmarking — fall squarely within the NLP community's scope.

## Abstract (Formatted for arXiv)

We introduce **Auditable Clinical Translation Orchestration (ACTO)** as a new technical
category for real-time medical interpretation systems that combine automated speech
recognition, machine translation, and human-in-the-loop interpreters into a single
orchestrated pipeline whose every output is verified by deterministic outcome-based
tests and recorded in a cryptographically timestamped audit log.

We argue that the current generation of Video Remote Interpretation (VRI) services and
AI-only translation tools occupies opposite ends of a quality-cost trade-off without
addressing the legal, regulatory, and forensic requirements emerging in healthcare
systems across Latin America and the United States. We propose ACTO as a third category
that resolves the trade-off through a cooperative inference stack, a verifier-first
architecture, and a regulatory-grade audit primitive.

We describe the system architecture, the verifier-design methodology adapted from
agent-evaluation research, and a benchmark methodology for Word Error Rate on medical
terminology and translation quality on Spanish clinical text. Preliminary results on
a 500-utterance evaluation set spanning Emergency, Operating Room, and Pharmacy
specialties show Word Error Rates of 3.2–4.1%, COMET-22 scores of 0.87–0.89, and
verifier pass rates of 94.2–96.1%, with median latency under 1 second.

The paper concludes with a positioning thesis for ACTO as the necessary infrastructure
layer for any healthcare AI deployment subject to HIPAA, Peruvian Law 29733, Brazilian
LGPD, or EU GDPR, and issues a call to hospital procurement offices, clinical
informatics researchers, and system builders to adopt, benchmark, and extend the ACTO
category.

## Additional arXiv Metadata Fields

- **DOI:** (to be assigned upon publication)
- **Report number:** ORQ-TR-2026-001
- **ACM classification:** I.2.7 (Natural Language Processing), J.3 (Life and Medical Sciences), K.4.1 (Public Policy Issues — Privacy), K.6.5 (Security and Protection)
- **MSC classification:** 68T50 (Natural language processing), 94A60 (Cryptography), 92C50 (Medical applications)

## Cross-listing Justification

This paper should be cross-listed to `cs.CR` because the audit primitive (Section 3.5)
introduces a novel application of cryptographic timestamping (RFC 3161, OpenTimestamps)
to clinical NLP pipelines, which is relevant to the security community working on
tamper-evident logging and distributed trust. It should also be cross-listed to `cs.CY`
because Sections 1 and 6 provide a substantive legal-regulatory analysis of how
cryptographic audit trails map to HIPAA, GDPR, LGPD, and Peruvian data protection law,
which is directly relevant to the Computers and Society community.

## Submission Notes

- This paper proposes a **technical category**, not a product.
- The reference implementation (Orquor Clinical) is mentioned as a proof-of-concept only.
- Preliminary benchmark results are explicitly labeled as non-definitive; a full
  peer-reviewed benchmark is planned as a follow-up.
- All clinical data used in the evaluation set is de-identified. The public benchmark
  dataset will be released separately with IRB approval.
- The verifier suite (~60 verifiers) will be open-sourced within 12 months.
