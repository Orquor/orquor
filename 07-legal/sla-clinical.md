# Orquor Clinical — Service Level Agreement (SLA)

**Version 2026-05** · Applies to **Orquor Clinical** (clinical.orquor.com). This SLA is incorporated by reference into the B2B Terms of Service and the Order Form. Capitalized terms not defined here have the meaning given in the Terms of Service.

---

## 1. Definitions

| Term | Definition |
|---|---|
| **Service** | Orquor Clinical, the real-time medical translation orchestration platform accessed via clinical.orquor.com, its REST API, and WebSocket streaming endpoints. |
| **Monthly Uptime Percentage** | `(Total Minutes in Month − Downtime Minutes) / Total Minutes in Month × 100` |
| **Downtime** | Any period during which the Service fails to accept new sessions or process utterances due to an infrastructure fault within Orquor's direct control. Excludes Scheduled Maintenance, Force Majeure, Customer-caused incidents, and third-party internet failures outside Orquor's network edge. |
| **Scheduled Maintenance** | Planned maintenance announced at least 48 hours in advance via email and the status page. Capped at 4 hours per calendar month. |
| **Emergency Maintenance** | Urgent security or stability patches announced at least 2 hours in advance. Capped at 2 hours per calendar month. Counts toward Downtime. |
| **Latency** | Time from receipt of a complete audio utterance by the Service to delivery of the verified translation to the Customer endpoint, measured at p95 over the calendar month. |
| **Support Ticket** | A written request submitted through the Orquor Console support portal or via email to support@orquor.com. |
| **Service Credit** | A dollar credit applied to the next invoice, calculated as a percentage of the Monthly Fee attributable to the affected period. |

---

## 2. Uptime Commitment

| Tier | Monthly Uptime Percentage | Applies to |
|---|---|---|
| **Standard** | 99.5% | All Orquor Clinical customers on the standard pricing plan |
| **Premium** | 99.9% | Customers on an Enterprise Order Form with the Premium SLA addendum |

### 2.1 Measurement

Uptime is measured by Orquor's external monitoring probes (AWS CloudWatch Synthetics or equivalent) probing the Service health endpoint (`GET /health`) from at least three geographic regions at 60-second intervals. The Monthly Uptime Percentage is calculated at the end of each calendar month and published to the Customer's Orquor Console dashboard within 5 business days.

### 2.2 Exclusions

Downtime does not include periods where:

- The Customer's network, hardware, or client software causes the failure
- The Customer exceeds documented rate limits or concurrency caps
- A third-party service outside Orquor's control (e.g., the cryptographic timestamping authority) experiences an outage and the Service continues to process utterances, queuing timestamps for later application
- The failure is caused by Force Majeure as defined in the Terms of Service
- The Service is in Scheduled Maintenance and the maintenance window was announced within the required notice period

---

## 3. Latency Commitment

| Metric | Target (Standard) | Target (Premium) | Measurement |
|---|---|---|---|
| p50 latency (transcription + translation + verification) | ≤ 1.5 seconds | ≤ 1.0 second | Monthly aggregate |
| p95 latency | ≤ 3.0 seconds | ≤ 2.0 seconds | Monthly aggregate |
| p99 latency | ≤ 5.0 seconds | ≤ 3.5 seconds | Monthly aggregate |

Latency is measured server-side: from the moment the Service finishes receiving the audio utterance to the moment the verified translation is written to the output stream. Network transit time between Customer and Orquor edge is excluded. Latency excludes utterances escalated to a human interpreter (human-in-the-loop path has its own latency target of ≤ 45 seconds from escalation to interpreter availability).

### 3.1 Latency credits

If p95 latency exceeds the target in any calendar month, Customer is entitled to a Service Credit of 5% of the Monthly Fee for that month. If p95 latency exceeds 2× the target, the credit is 10%.

---

## 4. Support

### 4.1 Support tiers

| Tier | Hours | Initial Response | Channels | Included in |
|---|---|---|---|---|
| **Standard** | Business hours (Mon–Fri, 9:00–18:00 UTC−5) | ≤ 4 business hours | Email, Support Portal | Standard plan |
| **Premium** | 24×7×365 | ≤ 1 hour (Severity 1) | Email, Phone, Support Portal, Slack Connect | Enterprise plan |
| **Critical** | 24×7×365 | ≤ 15 minutes (Severity 1) | Dedicated Slack channel + Phone | Enterprise plan with Critical add-on |

### 4.2 Severity classifications

| Severity | Definition | Example |
|---|---|---|
| **Severity 1 — Critical** | Service is unavailable or a security breach is in progress. No workaround exists. | Clinical.orquor.com not accepting sessions for all customers; confirmed PHI breach |
| **Severity 2 — High** | Core feature is degraded or unavailable for a subset of customers. Workaround is impractical. | MT component returning empty translations for a specific language pair; verifier suite returning false negatives |
| **Severity 3 — Normal** | Partial impairment. Workaround exists. | Latency elevated but within 2× target; audit log export delayed |
| **Severity 4 — Low** | Cosmetic issues, documentation gaps, feature requests. | Dashboard UI glitch; API documentation typo |

### 4.3 Support response targets

| Severity | Standard (business hours) | Premium (24×7) |
|---|---|---|
| 1 — Critical | ≤ 2 business hours | ≤ 1 hour |
| 2 — High | ≤ 4 business hours | ≤ 2 hours |
| 3 — Normal | ≤ 8 business hours | ≤ 4 hours |
| 4 — Low | ≤ 2 business days | ≤ 8 business hours |

Response time is measured from ticket creation to first human response (not automated acknowledgment).

---

## 5. Service Credits and Penalties

### 5.1 Uptime credits

| Monthly Uptime Percentage (Standard) | Service Credit (% of Monthly Fee) |
|---|---|
| 99.0% – 99.49% | 10% |
| 95.0% – 98.99% | 25% |
| < 95.0% | 50% |

| Monthly Uptime Percentage (Premium) | Service Credit (% of Monthly Fee) |
|---|---|
| 99.5% – 99.89% | 10% |
| 99.0% – 99.49% | 25% |
| < 99.0% | 50% |

### 5.2 Claim process

Customer must request a Service Credit in writing within 30 calendar days of the month in which the SLA breach occurred. Orquor will verify the claim against its monitoring data and apply the credit to the next invoice within 15 business days. If the claim is denied, Orquor will provide the monitoring data supporting the denial.

### 5.3 Maximum credits

Total Service Credits in any calendar month are capped at 50% of the Monthly Fee for that month. Credits are the sole and exclusive remedy for SLA breaches. Credits do not constitute a refund and are not transferable.

### 5.4 Termination right

If the Service fails to meet the Monthly Uptime Percentage in three (3) consecutive months or in any four (4) months within a rolling twelve-month period, Customer may terminate the Order Form without penalty upon 30 days written notice, and Orquor will refund any prepaid fees for unused months.

---

## 6. Audit Log SLA

Orquor commits to:

- **Availability**: Audit log entries are available for export within 1 hour of session completion.
- **Integrity**: Every audit log entry is cryptographically timestamped via RFC 3161 (or OpenTimestamps) and signed by the orchestrator's hardware key. Tampering is detectable through independent verification without trust in Orquor.
- **Retention**: Audit logs are retained for 7 years from session date (aligned to clinical record retention requirements under HIPAA and equivalent frameworks).
- **Export format**: JSON Lines (`.jsonl`) with a verifiable manifest. Export is self-service via the Orquor Console or programmatic via the API.

If audit log export fails for more than 24 hours beyond the 1-hour window, Customer is entitled to a Service Credit of 5% of the Monthly Fee.

---

## 7. Security Commitments

- **Encryption in transit**: TLS 1.2+ for all API and WebSocket connections. mTLS available for Enterprise customers.
- **Encryption at rest**: AES-256 for all stored Customer Data, including audio recordings, transcripts, and audit logs.
- **Confidential computing**: PHI processing occurs in confidential compute environments (NVIDIA H100 confidential mode or equivalent) where technically available.
- **Breach notification**: Orquor will notify Customer within 48 hours of confirming a breach involving Customer Data, and in any case within the timeframe required by applicable law (72 hours under GDPR, without unreasonable delay under HIPAA).
- **Penetration testing**: Annual third-party penetration test. Summary report available to Enterprise customers under NDA.
- **SOC 2 Type II**: Target completion Q1 2027. Orquor will provide a bridge letter and attestation of controls in the interim.

---

## 8. Disaster Recovery

| Metric | Target |
|---|---|
| Recovery Time Objective (RTO) | ≤ 4 hours |
| Recovery Point Objective (RPO) | ≤ 15 minutes |
| Geographic failover | Cross-region (primary: Lima/LATAM, secondary: US East) |
| DR test frequency | Quarterly |

In the event of a disaster declaration, Orquor will activate the secondary region. Sessions in progress at the time of failure will be recoverable from the audit log (last committed state) but may not resume seamlessly; this is communicated in the session metadata for Customer workflow handling.

---

## 9. Changes to this SLA

Orquor may update this SLA upon 60 days written notice to Customer. Material reductions in SLA targets during a committed subscription term require Customer's written consent. If Customer does not consent, the prior SLA terms remain in effect for the remainder of the current term.

---

## 10. Contact

For SLA claims, support escalations, or questions:

- **Support**: support@orquor.com
- **SLA claims**: sla@orquor.com
- **Security incidents**: security@orquor.com
- **Legal**: legal@orquor.com

---

**Last updated**: 2026-05

*This SLA is provided as part of the Orquor Clinical service. It must be reviewed by qualified counsel before incorporation into a binding agreement with a specific customer. SLAs for regulated healthcare customers may include additional jurisdiction-specific commitments not reflected in this general template.*
