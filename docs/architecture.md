# Orquor Clinical — Technical Architecture

**Version 1.0** · 2026-05 · Target audience: engineers integrating with Orquor Clinical, hospital IT teams conducting architectural review, and researchers evaluating the ACTO reference implementation.

---

## Table of Contents

1. [Architectural Overview](#1-architectural-overview)
2. [System Components](#2-system-components)
   - [2.1 Clinical Orchestrator](#21-clinical-orchestrator)
   - [2.2 ASR Component (Automated Speech Recognition)](#22-asr-component-automated-speech-recognition)
   - [2.3 MT Component (Machine Translation)](#23-mt-component-machine-translation)
   - [2.4 Verifier Suite](#24-verifier-suite)
   - [2.5 Human Interpreter Bridge](#25-human-interpreter-bridge)
   - [2.6 Audit Log](#26-audit-log)
3. [Data Flow](#3-data-flow)
4. [Deployment Topology](#4-deployment-topology)
5. [Security Architecture](#5-security-architecture)
6. [Integration Points](#6-integration-points)
7. [Observability](#7-observability)
8. [Compliance Posture](#8-compliance-posture)

---

## 1. Architectural Overview

Orquor Clinical implements the **ACTO (Auditable Clinical Translation Orchestration)** category defined in the [Orquor whitepaper](../03-whitepaper-acto/whitepaper-acto.md). It is a real-time medical interpretation system composed of five cooperating components arranged in a pipeline under a central orchestrator. Every translation output is verified by an outcome-based test suite before delivery. Every session is logged with cryptographic timestamping. Every consequential decision is auditable.

### High-level system diagram

```
                   ┌─────────────────────────────────────────────┐
                   │             CLINICAL ORCHESTRATOR            │
                   │  (Session life-cycle, routing, verification, │
                   │   escalation, audit log coordination)        │
                   └──────┬──────────┬──────────┬────────────────┘
                          │          │          │
              ┌───────────▼──┐ ┌─────▼──────┐ ┌─▼──────────────┐
              │  ASR Engine  │ │ MT Engine  │ │ Verifier Suite │
              │ (Whisper +   │ │ (NLLB-200  │ │  (~60 outcome- │
              │  medical FT) │ │  + medical │ │   based tests) │
              └──────────────┘ │  FT)       │ └────────────────┘
                               └────────────┘
              ┌──────────────────────────────────────────────────┐
              │              HUMAN INTERPRETER BRIDGE             │
              │  (Escalation queue, VRI handoff, interpreter UI)  │
              └──────────────────────────────────────────────────┘
              ┌──────────────────────────────────────────────────┐
              │                   AUDIT LOG                      │
              │  (Per-utterance, RFC 3161 timestamped, append-   │
              │   only, independently verifiable without trust)   │
              └──────────────────────────────────────────────────┘
```

---

## 2. System Components

### 2.1 Clinical Orchestrator

The Clinical Orchestrator is the central coordinating process. It is distinct from the Hermes business-operations orchestrator (`06-hermes/orchestrator.py`). The Clinical Orchestrator manages the real-time translation session lifecycle.

#### Responsibilities

- **Session life-cycle**: Accept session initiation requests with metadata (department, language pair, register, patient identifier, clinician identifier, consent flags). Create session. Manage session state through termination.
- **Audio ingestion**: Accept streaming audio via WebSocket. Segment into utterances using voice activity detection (VAD). Buffer and deduplicate.
- **Pipeline orchestration**: Route each utterance through ASR → MT → Verifier. Collect results. Make escalation decisions.
- **Escalation logic**: If verifier weighted sum exceeds a configurable threshold, re-route the utterance to a human interpreter. If the human interpreter is unavailable, retry with temperature-adjusted MT or flag for post-session review.
- **Output delivery**: Stream verified translations to the Customer endpoint in real time via WebSocket.
- **Deterministic replay**: Given identical audio and metadata, the orchestrator produces a bit-identical audit log (requires temperature=0 and seed pinning for all stochastic components).

#### Technical characteristics

| Property | Value |
|---|---|
| Language | Python 3.12+ |
| Concurrency model | asyncio (single-process, coroutine-per-session) |
| Session capacity | Up to 200 concurrent sessions per orchestrator instance (scale horizontally) |
| State management | In-memory session state; audit log entries written to persistent store on every utterance boundary |
| Configuration | YAML-based; hot-reloadable for verifier weights, threshold policies, and register mappings |

#### Session metadata schema

```json
{
  "session_id": "uuid-v4",
  "customer_id": "cust_abc123",
  "department": "emergency",
  "source_language": "en",
  "target_language": "es",
  "register": "formal_clinical",
  "patient_id": "pat_hashed_xyz",
  "clinician_id": "clin_hashed_abc",
  "consent_verified": true,
  "consent_method": "verbal_recorded",
  "created_at": "2026-05-24T14:30:00Z",
  "timezone": "America/Lima"
}
```

---

### 2.2 ASR Component (Automated Speech Recognition)

The ASR component transcribes source-language audio to text with per-token confidence scores.

#### Implementation

| Property | Value |
|---|---|
| Base model | Whisper Large v3 (OpenAI) |
| Fine-tuning | Medical-domain corpus (English and Spanish clinical encounters, de-identified) |
| Word Error Rate (medical) | Target ≤ 5% (current: 3.2–4.1% across Emergency, OR, Pharmacy) |
| Output | Transcript text + per-token confidence scores + latency metadata |
| Batch mode | Streaming (intermediate results emitted before utterance completion for latency optimization) |

#### Confidence scoring

Each token carries a confidence score in [0.0, 1.0]. The orchestrator uses the utterance-level mean confidence as the primary escalation signal. Low-confidence utterances (mean confidence < 0.85) trigger:

1. Re-run ASR with a different beam width or temperature setting
2. If still low, flag for verifier scrutiny (verifiers apply stricter thresholds on low-confidence inputs)
3. If verifier fails, escalate to human interpreter

#### Medical vocabulary

The ASR is fine-tuned on domain-specific vocabulary including:

- Drug names (brand and generic, EN and ES)
- Dosage patterns (numeric + unit)
- Anatomical terminology
- Procedure names
- ICD-10 and SNOMED-CT coded terms (recognition, not coding)
- Controlled substance nomenclature

---

### 2.3 MT Component (Machine Translation)

The MT component translates source-language transcripts into target-language clinical text with register adaptation.

#### Implementation

| Property | Value |
|---|---|
| Base architecture | Sequence-to-sequence transformer initialized from NLLB-200 (Meta AI, 3.3B parameters) |
| Fine-tuning | Paired clinical corpora (EN↔ES, medical domain), domain-adaptive pretraining |
| COMET-22 score | ≥ 0.86 target (current: 0.87–0.89) |
| Register adaptation | Three registers: `formal_clinical`, `simplified`, `legal` |
| Fallback | Prompted LLM (Claude Sonnet 4.5 or GPT-5) with verifier feedback loop |

#### Register system

| Register | Use case | Vocabulary characteristics |
|---|---|---|
| `formal_clinical` | Physician-to-physician, nurse-to-nurse, clinical documentation | Technical terminology, Latin-derived pharmacological terms, standard abbreviations |
| `simplified` | Clinician-to-patient, discharge instructions, informed consent | Plain language, explanations of medical terms, shorter sentences |
| `legal` | Medical-legal documentation, adverse-event reports, court-admissible records | Formal register, precise terminology, no colloquialisms, structured phrasing |

Register is specified per session and can be changed mid-session by the clinician via a control message.

#### Translation pipeline

```
Source transcript → Register tag injection → NLLB-200 (medical FT) →
  Register classifier check → Output
```

If the register classifier detects a mismatch, the MT re-generates with an explicit register prompt. If mismatch persists, the utterance is flagged for the verifier.

---

### 2.4 Verifier Suite

The verifier suite is the distinguishing component of the ACTO architecture. Before any translated output reaches the clinician's screen, it passes through a deterministic test suite.

#### Design principles (from the ACTO whitepaper)

1. **Verifiers evaluate outcomes, not traces.** A verifier checks the final output, not intermediate steps.
2. **Verifiers are atomic.** Each verifier tests exactly one property.
3. **Verifiers are weighted.** Weights reflect failure severity: ±5 catastrophic, ±3 moderate, ±1 stylistic.
4. **Negative verifiers are required.** The suite includes tests for properties that must *not* be present (e.g., excluded names, English leakage into Spanish output).
5. **Verifiers are versioned.** Suite version recorded in the audit log per utterance.

#### Verifier categories

| Category | Count (~60 total) | Example |
|---|---|---|
| Dosage safety | 2 | Numeric dosage preserved, pharmacologic units preserved |
| Controlled substances | 1 | Controlled substance names map to canonical target-language term |
| Privacy / PHI leakage | 3 | No excluded names, no unmasked identifiers, no PHI in non-clinical register |
| Register fidelity | 2 | Register classifier matches requested register, no register mixing |
| Translation completeness | 3 | Non-empty output, length ratio within bounds, no truncation |
| Language integrity | 2 | No English leakage into Spanish output, no code-switching beyond clinical norms |
| Clinical terminology | 5 | Drug name preservation, anatomical term accuracy, procedure name mapping |
| Negation handling | 2 | Negation preserved, polarity not flipped |
| Numeric accuracy | 3 | Numeric values preserved, unit conversion consistency, range preservation |
| Structural integrity | 2 | Sentence boundaries preserved, paragraph structure maintained |
| Specialty-specific | ~15 | Emergency-specific terms, OR-specific terms, ICU-specific terms, Pharmacy, Pediatrics, Psychiatry, etc. |
| Legal / consent | 3 | Consent language verified, legal boilerplate present when requested, disclaimer language correct |

#### Escalation logic

The orchestrator computes a weighted pass/fail sum for each utterance:

```
score = sum(v.weight for v in verifiers where v.passed)
```

| Score range | Action |
|---|---|
| All pass | Deliver immediately |
| Failures with total weight ≤ −5 | Re-run MT with failure signals as context; if passes on retry, deliver with `retry_count=1` in audit log |
| Failures with total weight ≤ −15 | Escalate to human interpreter |
| Failures with total weight > −15 | Escalate immediately; mark session for post-session review |

#### Verifier latency budget

Verifiers must complete in ≤ 100ms per utterance (p95). All verifiers are implemented as in-process Python functions with no external API calls. Heavier semantic checks (COMET scoring, full register classification) run asynchronously post-delivery and flag utterances for retroactive review if they fail; they do not block the real-time path.

---

### 2.5 Human Interpreter Bridge

The Human Interpreter Bridge is the interface between the automated pipeline and the human interpreter. It is activated when the orchestrator escalates an utterance.

#### Components

- **Escalation queue**: Priority queue of utterances requiring human interpretation. Ordered by severity (weighted verifier failure score) and session priority.
- **Interpreter UI**: Web-based interface for certified medical interpreters. Displays source audio, ASR transcript, MT candidate translation, and verifier failure reasons. The interpreter can accept the MT output, edit it, or retranslate from scratch.
- **VRI handoff**: Optional integration with Video Remote Interpretation services for sessions that require visual context.
- **Interpreter feedback loop**: Interpreter corrections are recorded and fed back into the MT fine-tuning pipeline (subject to data-processing consent).

#### Latency target

| Stage | Target |
|---|---|
| Utterance escalation to interpreter notification | ≤ 2 seconds |
| Interpreter availability (business hours) | ≤ 15 seconds |
| Interpreter availability (after hours) | ≤ 45 seconds |
| Interpreter response time (from accepting to delivering translation) | ≤ 30 seconds |

---

### 2.6 Audit Log

The audit log is the regulatory-grade primitive that makes ACTO defensible. It records every utterance in every session with sufficient detail for independent forensic verification.

#### Schema per utterance

```json
{
  "session_id": "uuid-v4",
  "utterance_id": 42,
  "timestamp": "2026-05-24T14:30:05.123Z",
  "source_audio_ref": "s3://orquor-clinical-audio/enc/...",
  "asr": {
    "transcript": "Administer 10 mg of morphine IV.",
    "confidence": 0.94,
    "tokens": [
      {"token": "Administer", "confidence": 0.97},
      {"token": "10", "confidence": 0.99},
      {"token": "mg", "confidence": 0.99},
      {"token": "of", "confidence": 0.95},
      {"token": "morphine", "confidence": 0.88},
      {"token": "IV", "confidence": 0.91}
    ],
    "latency_ms": 340
  },
  "mt": {
    "translation": "Administrar 10 mg de morfina IV.",
    "register": "formal_clinical",
    "model": "nllb-200-medical-v2",
    "latency_ms": 180
  },
  "verifier": {
    "suite_version": "v1.3",
    "results": [
      {"verifier": "v1_dosage_preserved", "passed": true, "weight": 5},
      {"verifier": "v2_units_preserved", "passed": true, "weight": 5},
      {"verifier": "v3_controlled_substance", "passed": true, "weight": 5},
      {"verifier": "v5_register_match", "passed": true, "weight": 2}
    ],
    "score": 17,
    "escalated": false
  },
  "human_interpreter": null,
  "crypto": {
    "timestamp_authority": "rfc3161",
    "timestamp_token": "MIIFbwYJKoZIhvcNAQcCo...",
    "orchestrator_signature": "MEUCIQDx...",
    "orchestrator_key_id": "ork-sign-2026-001"
  }
}
```

#### Properties

- **Append-only**: Once written, log entries are never modified. Any modification is detectable via signature verification.
- **Cryptographic timestamping**: Every entry is timestamped via an RFC 3161 Time-Stamp Authority (TSA) or OpenTimestamps. The timestamp proves the entry existed at a specific moment without trusting Orquor.
- **Independently verifiable**: An external auditor can verify the entire audit log against the TSA's public certificate. No trust in Orquor is required.
- **Portable**: The Customer can request and receive the complete audit log in JSON Lines format at any time. The log includes a verifiable manifest (Merkle tree of entry hashes).
- **Retention**: 7 years from session date. Deletion after retention period is cryptographically verifiable (deletion certificates issued).

---

## 3. Data Flow

### Session life-cycle

```
1. INITIATE  → Customer POST /sessions with metadata → Orchestrator creates session
2. STREAMING → Customer opens WebSocket → Audio flows → VAD segments into utterances
3. PIPELINE  → For each utterance:
   a. ASR: Audio → Transcript + confidence
   b. MT:  Transcript → Translation (register-adapted)
   c. VR:  Translation → Verifier results + score
   d. ESC: Score triggers deliver / retry / escalate-to-human
   e. LOG: Utterance result written to audit log with cryptographic timestamp
4. DELIVER   → Verified translation streamed to Customer WebSocket
5. TERMINATE → Customer POST /sessions/{id}/close → Final audit log entry written
```

### Escalation flow

```
Verifier score < threshold
  → Orchestrator places utterance in escalation queue
  → Interpreter notified (WebSocket push to interpreter UI)
  → Interpreter reviews: source audio + ASR transcript + MT candidate + verifier failures
  → Interpreter delivers corrected translation
  → Corrected translation routed back through verifier suite (human output is also verified)
  → Verified corrected translation delivered to Customer
  → Audit log records: original MT output, verifier failures, interpreter correction, corrected verifier results
```

---

## 4. Deployment Topology

### Production environment

```
┌────────────────────────────────────────────────────────────┐
│                      CLOUDFLARE                            │
│    (DNS, DDoS protection, WAF, mTLS termination)           │
└──────────────────────┬─────────────────────────────────────┘
                       │
┌──────────────────────▼─────────────────────────────────────┐
│                 HOSTINGER / AWS (primary)                   │
│                                                             │
│  ┌─────────────────────┐   ┌──────────────────────────┐    │
│  │  Orchestrator Pool  │   │   ASR/MT Inference Pool  │    │
│  │  (t3.xlarge × 3)    │   │   (g5.xlarge × 2,        │    │
│  │                      │   │    A10G GPUs)             │    │
│  └─────────┬────────────┘   └────────────┬─────────────┘    │
│            │                              │                  │
│  ┌─────────▼──────────────────────────────▼─────────────┐  │
│  │                   PostgreSQL 15                        │  │
│  │    (Audit log, session metadata, Customer config)      │  │
│  └────────────────────────────┬──────────────────────────┘  │
│                               │                              │
│  ┌────────────────────────────▼──────────────────────────┐  │
│  │              S3-compatible object store                 │  │
│  │    (Encrypted audio blobs, audit log archives)          │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼─────────────────────────────────────┐
│                 AWS US-EAST-1 (DR/failover)                 │
│    (Warm standby: orchestrator pool, PostgreSQL read        │
│     replica, object store replication)                      │
└─────────────────────────────────────────────────────────────┘
```

### Edge presence

- **Primary**: Lima, Peru (Hostinger / local cloud)
- **DR/Failover**: AWS us-east-1 (Northern Virginia)
- **API edge**: Cloudflare CDN with Argo Smart Routing for reduced latency to LATAM and US customers

### Scaling characteristics

| Component | Scaling strategy | Limit per instance |
|---|---|---|
| Orchestrator | Horizontal (stateless except session affinity) | 200 concurrent sessions |
| ASR | Horizontal + GPU autoscaling | 40 concurrent transcriptions per GPU |
| MT | Horizontal + GPU autoscaling | 80 concurrent translations per GPU |
| Verifier suite | In-process (no scaling needed; CPU-bound, < 1ms per verifier) | N/A |
| PostgreSQL | Vertical (RDS / managed) + read replicas for audit log queries | N/A |

---

## 5. Security Architecture

### Data protection

| Layer | Mechanism |
|---|---|
| **In transit** | TLS 1.3 (enforced). mTLS available for Enterprise customers. HSTS preloaded. |
| **At rest — audio** | AES-256-GCM. Customer-specific encryption keys (KMS). Audio deleted after 30 days unless Customer opts for extended retention. |
| **At rest — audit log** | AES-256-GCM. Append-only. Cryptographic signatures on every entry. |
| **At rest — transcripts** | AES-256-GCM. Retained per Customer's data retention policy. |
| **Inference** | Confidential computing (NVIDIA H100 confidential mode) where available. Memory encryption. |
| **Key management** | AWS KMS / HashiCorp Vault. Keys rotated every 90 days. Customer-managed keys (CMK) available for Enterprise. |

### Access control

- **Orchestrator API**: API key + HMAC signature per request. Keys are Customer-scoped. Rotatable via Console.
- **Interpreter UI**: SAML/OIDC SSO. MFA required. Role-based: interpreter, supervisor, administrator.
- **Internal access**: Break-glass procedure. All access logged to separate admin audit log. No standing access for operational staff.
- **Customer data isolation**: Logical separation at the application layer (tenant ID on every query). Dedicated infrastructure available for Enterprise (single-tenant deployment).

### Threat model summary

| Threat | Mitigation |
|---|---|
| Unauthorized access to PHI | mTLS + API keys + MFA + least-privilege IAM + confidential computing |
| Audit log tampering | Cryptographic signatures + append-only storage + external timestamping |
| Model inversion / extraction | Rate limiting + input/output filtering + differential privacy for training data |
| Denial of service | Cloudflare DDoS protection + rate limiting + horizontal scaling |
| Supply chain compromise | Signed container images + SBOM + dependency scanning (Dependabot / Snyk) |
| Insider threat | No standing access + break-glass audit + separation of duties + admin audit log |

---

## 6. Integration Points

### Customer-facing APIs

| Interface | Protocol | Purpose |
|---|---|---|
| REST API | HTTPS (TLS 1.3) | Session management, audit log export, account configuration |
| WebSocket | WSS | Real-time audio streaming and translation delivery |
| Webhooks | HTTPS | Session events, verifier alerts, billing events (Customer-configured) |

Full API reference: [api-reference.md](api-reference.md)

### Internal integration points

| Interface | Protocol | Purpose |
|---|---|---|
| ASR service | gRPC (internal) | Audio → transcript with confidence |
| MT service | gRPC (internal) | Transcript → translation with register |
| TSA (timestamp authority) | RFC 3161 HTTP | Cryptographic timestamping of audit log entries |
| Interpreter UI | WebSocket + REST | Escalation queue, interpreter feedback |
| Monitoring | Prometheus metrics + OpenTelemetry traces | Observability pipeline |

### EHR/EMR integration (roadmap)

- **HL7 FHIR R4**: Session metadata and verified translations pushed to EHR as `DocumentReference` resources (Q4 2026)
- **HL7 v2**: ADT feed for automatic session initiation on patient admission (Q1 2027)
- **DICOMweb**: Integration for radiology-specific translation workflows (research phase)

---

## 7. Observability

### Metrics (Prometheus + Grafana)

| Metric | Description | Alert threshold |
|---|---|---|
| `session_active_total` | Concurrent active sessions | > 180 per orchestrator |
| `utterance_latency_p95` | p95 pipeline latency | > 3.0s for 5 minutes |
| `asr_confidence_mean` | Mean ASR confidence across all utterances | < 0.85 for 15 minutes |
| `verifier_fail_rate` | Percentage of utterances failing ≥ 1 verifier | > 10% for 15 minutes |
| `escalation_rate` | Percentage of utterances escalated to human | > 15% for 1 hour |
| `audit_log_write_latency_p99` | p99 time to write audit log entry | > 500ms for 5 minutes |
| `api_error_rate_5xx` | 5xx error rate on REST API | > 0.1% for 5 minutes |

### Tracing (OpenTelemetry)

Every utterance carries a trace context through the pipeline: ASR → MT → Verifier → Audit Log. Traces are exported to a Customer-accessible dashboard (Enterprise tier) for latency debugging and compliance verification.

### Logging

- **Service logs**: Structured JSON to stdout/stderr → Fluentd → Elasticsearch (retained 90 days)
- **Audit logs**: Separate pipeline. Not mixed with service logs. Append-only store. 7-year retention.
- **Admin audit logs**: All internal access. Immutable. Retained 7 years.

---

## 8. Compliance Posture

Orquor Clinical is designed to support compliance with the following frameworks. The architecture provides the technical primitives; the compliance program is the Customer's responsibility.

| Framework | How the architecture supports it |
|---|---|
| **HIPAA** (US) | BAA template in `07-legal/hipaa-baa-template.md`. Audit log satisfies § 164.312(b) (access controls + audit controls) and § 164.312(c) (integrity controls). Encryption satisfies Security Rule. Breach notification within 48 hours. |
| **Ley 29733** (Peru) | Data subject rights (access, rectification, opposition) supported by audit log export and session data deletion APIs. Registration with ANPDP pending. |
| **LGPD** (Brazil) | Legal basis: legitimate interest (Art. 7, IX) + explicit consent. Audit log supports portability (Art. 18, V). Data Protection Officer: dpo@orquor.com. |
| **GDPR** (EU) | Data minimization (Art. 5(1)(c)). Storage limitation (Art. 5(1)(e)). Integrity and confidentiality (Art. 5(1)(f)). SCCs for international transfers. Representative in the EU: to be appointed. |
| **SOC 2 Type II** | Target Q1 2027. Controls mapped. Bridge letter available on request. |

---

## Version history

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05 | Initial architecture document. Reflects Orquor Clinical v1. |

---

**Questions about the architecture?** Contact research@orquor.com for technical collaboration. For security review, contact security@orquor.com.
