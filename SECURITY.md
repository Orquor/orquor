# Security Policy

Orquor builds infrastructure for healthcare and regulated industries. Security is not a feature — it is the foundation. This document describes how to report vulnerabilities and what to expect in return.

---

## Supported versions

| Version | Supported |
|---|---|
| 0.1.x (current) | Yes — active development |
| Pre-0.1.0 | No |

Security patches are applied to the current minor release track. We do not backport fixes to earlier versions while the project is in pre-1.0 development.

---

## Scope

The security policy covers:

- **`06-hermes/`** — Orchestrator, sub-agents, verifiers, shared memory framework.
- **`04-web/`** — Marketing site, Academy landing page, and any deployed web surface at `orquor.com` and subdomains.
- **Repository infrastructure** — GitHub Actions, deployment scripts, `.env` handling.

The following are out of scope:

- The marketing content in `09-content-calendar/` (no runtime surface).
- Legal templates in `07-legal/` (provided as-is; counsel review required before use).
- Third-party services and APIs that Orquor does not control.

---

## Reporting a vulnerability

**Do not open a public issue.** Orquor handles security vulnerabilities through a private disclosure process.

Send your report to:

**`security@orquor.com`**

Include the following in your report:

1. **Affected component** — File path, module, or endpoint.
2. **Description** — What the vulnerability is and its potential impact.
3. **Reproduction steps** — How to trigger the vulnerability. Include code samples or curl commands if applicable.
4. **Environment** — OS, Python version, and any relevant configuration details.
5. **Suggested fix** — Optional. If you have a proposed patch, include it.

Encrypt sensitive reports with our PGP key if needed. Request the key by emailing `security@orquor.com` with subject "PGP key request".

---

## What to expect

| Timeline | Action |
|---|---|
| Within 48 hours | Acknowledgment of receipt. We will confirm we are investigating. |
| Within 7 days | Initial assessment. We will classify severity and provide an estimated fix timeline. |
| Within 30 days | Resolution. Most vulnerabilities will be patched within 30 days of acknowledgment. Critical vulnerabilities will be expedited. |

We will keep you informed of progress. Once a fix is released, we will credit you in the release notes unless you request anonymity. We do not offer monetary bounties at this stage.

---

## Severity classification

| Severity | Definition | Examples |
|---|---|---|
| **Critical** | Remote code execution, authentication bypass, exposure of production secrets or PII/PHI. | Unauthenticated RCE in orchestrator, leaked `.env` committed to public repo. |
| **High** | Data exfiltration path, verifier bypass that could mask clinical errors. | VerifierResult manipulated without detection, audit log injection. |
| **Medium** | Information disclosure, denial of service, dependency with known CVE (CVSS >= 7). | Unintended debug output in production, missing rate limiting. |
| **Low** | Defense-in-depth improvements, best-practice deviations without immediate exploit path. | Missing security headers on static pages, overly verbose error messages. |

---

## Responsible disclosure

We request that you:

- Give us reasonable time to investigate and patch before public disclosure.
- Do not access, modify, or delete data that does not belong to you.
- Do not degrade the service for other users while testing.

Orquor will not pursue legal action against researchers who follow this policy and act in good faith.

---

## Security design principles

Orquor's security posture is built on the following principles, consistent with the ACTO specification:

1. **Auditability over obscurity.** Every consequential action is logged with cryptographic timestamping. The system is designed to be forensically examined years after the fact.
2. **Deterministic verification.** All verifiers are deterministic and self-contained. No external API calls in the verification path. This eliminates entire classes of supply-chain and prompt-injection attacks at the verifier level.
3. **Least privilege.** Sub-agents operate with the minimum permissions required for their function. The orchestrator alone holds coordination authority.
4. **No PHI in open-source code.** This repository contains zero patient data, zero production credentials, and zero real clinical logs. All examples use synthetic data.

---

## Contact

- **Security vulnerabilities:** `security@orquor.com`
- **General inquiries:** `hello@orquor.com`
- **PGP key:** Available upon request at `security@orquor.com`

---

*Last updated: 2026-05-24*
