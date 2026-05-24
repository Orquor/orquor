# Orquor Clinical — REST API Reference

**Version 1.0** · 2026-05 · Base URL: `https://clinical.orquor.com/api/v1`

---

## Table of Contents

1. [Overview](#1-overview)
2. [Authentication](#2-authentication)
3. [Sessions](#3-sessions)
4. [Real-Time Translation (WebSocket)](#4-real-time-translation-websocket)
5. [Audit Logs](#5-audit-logs)
6. [Configuration](#6-configuration)
7. [Webhooks](#7-webhooks)
8. [Common Types](#8-common-types)
9. [Error Codes](#9-error-codes)
10. [Rate Limits](#10-rate-limits)
11. [Pagination](#11-pagination)
12. [Changelog](#12-changelog)

---

## 1. Overview

The Orquor Clinical API provides programmatic access to the ACTO translation orchestration platform. Use it to initiate clinical translation sessions, stream audio for real-time translation, retrieve cryptographically timestamped audit logs, and manage account configuration.

### Base URL

```
https://clinical.orquor.com/api/v1
```

### Content type

All requests and responses use `application/json` unless otherwise noted. WebSocket connections use binary frames for audio and JSON text frames for control messages.

### Idempotency

POST and PATCH endpoints support idempotency keys via the `Idempotency-Key` header. Supply a unique UUID per operation. Duplicate requests with the same key return the original response without side effects. Idempotency keys expire after 24 hours.

### Request IDs

Every response includes an `X-Request-Id` header with a unique identifier. Include this when reporting issues.

---

## 2. Authentication

All API requests require authentication via API key.

### API key

Include your API key in the `Authorization` header:

```
Authorization: Bearer orq_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

API keys are scoped to a Customer account and carry role-based permissions. Manage keys via the [Orquor Console](https://console.orquor.com).

### Key types

| Prefix | Description |
|---|---|
| `orq_live_` | Production API key. Full access to translation sessions and audit logs. |
| `orq_test_` | Sandbox API key. Access to test environment only. No real audio processing. Rate-limited. |
| `orq_readonly_` | Read-only API key. Can retrieve audit logs and session metadata. Cannot create sessions. |

### HMAC request signing (Enterprise)

Enterprise customers may additionally sign requests using HMAC-SHA256. The signature is computed over:

```
HTTP_METHOD + "\n" + REQUEST_PATH + "\n" + TIMESTAMP + "\n" + BODY_SHA256
```

Included in headers:

```
X-Orq-Signature: t=1700000000,v1=abcdef123456...
X-Orq-Key-Id: ork_sign_2026_001
```

Replay protection: timestamps must be within ±5 minutes of server time.

### WebSocket authentication

Include the API key as a query parameter on the WebSocket upgrade request:

```
wss://clinical.orquor.com/api/v1/ws/translate?token=orq_live_xxx
```

Or pass it in the first JSON frame after connection:

```json
{"type": "auth", "api_key": "orq_live_xxx"}
```

---

## 3. Sessions

A Session represents a single clinical encounter. It groups utterances, translations, and audit log entries under a unique session ID.

### 3.1 Create Session

```
POST /sessions
```

Initiates a new translation session with metadata.

**Request body:**

```json
{
  "customer_id": "cust_abc123",
  "department": "emergency",
  "source_language": "en",
  "target_language": "es",
  "register": "formal_clinical",
  "patient_id": "pat_hashed_xyz",
  "clinician_id": "clin_hashed_abc",
  "consent_verified": true,
  "consent_method": "verbal_recorded",
  "metadata": {
    "room": "ER-3",
    "case_type": "trauma"
  },
  "webhook_url": "https://hospital.example.com/orquor-events",
  "idempotency_key": "uuid-v4"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `customer_id` | string | Yes | Your Orquor Customer ID (from Console) |
| `department` | string | Yes | One of: `emergency`, `operating_room`, `icu`, `pharmacy`, `pediatrics`, `psychiatry`, `admissions`, `general` |
| `source_language` | string | Yes | ISO 639-1 code. Supported: `en`, `es` |
| `target_language` | string | Yes | ISO 639-1 code. Supported: `en`, `es`. Must differ from source. |
| `register` | string | Yes | One of: `formal_clinical`, `simplified`, `legal` |
| `patient_id` | string | No | Opaque identifier for the patient. Hashed before storage. |
| `clinician_id` | string | No | Opaque identifier for the clinician. Hashed before storage. |
| `consent_verified` | boolean | Yes | Whether consent for recording and AI processing has been verified |
| `consent_method` | string | No | `verbal_recorded`, `written_form`, `implied_emergency` |
| `metadata` | object | No | Arbitrary key-value pairs (string values only). Included in audit log. |
| `webhook_url` | string | No | HTTPS endpoint for session event webhooks |
| `idempotency_key` | string | No | UUID v4 for idempotent session creation |

**Response: 201 Created**

```json
{
  "session_id": "sess_a1b2c3d4e5f6",
  "status": "ready",
  "ws_endpoint": "wss://clinical.orquor.com/api/v1/ws/translate?session=sess_a1b2c3d4e5f6",
  "department": "emergency",
  "source_language": "en",
  "target_language": "es",
  "register": "formal_clinical",
  "created_at": "2026-05-24T14:30:00Z",
  "expires_at": "2026-05-24T18:30:00Z"
}
```

| Field | Type | Description |
|---|---|---|
| `session_id` | string | Unique session identifier (prefix `sess_`) |
| `status` | string | `ready` (awaiting audio), `active` (audio streaming), `closed` |
| `ws_endpoint` | string | WebSocket URL for streaming audio and receiving translations |
| `expires_at` | string | ISO 8601. Sessions auto-close after 4 hours of inactivity |

### 3.2 Get Session

```
GET /sessions/{session_id}
```

Retrieve session metadata and current status.

**Response: 200 OK**

```json
{
  "session_id": "sess_a1b2c3d4e5f6",
  "status": "active",
  "department": "emergency",
  "source_language": "en",
  "target_language": "es",
  "register": "formal_clinical",
  "utterance_count": 47,
  "escalation_count": 3,
  "created_at": "2026-05-24T14:30:00Z",
  "started_at": "2026-05-24T14:30:12Z",
  "last_activity_at": "2026-05-24T14:42:33Z",
  "expires_at": "2026-05-24T18:30:00Z"
}
```

### 3.3 Close Session

```
POST /sessions/{session_id}/close
```

Closes an active session. Finalizes the audit log. No further audio accepted.

**Response: 200 OK**

```json
{
  "session_id": "sess_a1b2c3d4e5f6",
  "status": "closed",
  "closed_at": "2026-05-24T14:45:00Z",
  "total_utterances": 52,
  "total_escalations": 3,
  "audit_log_snapshot": {
    "entries": 52,
    "verifiable": true,
    "tsa": "rfc3161"
  }
}
```

### 3.4 List Sessions

```
GET /sessions?status=active&department=emergency&limit=20&from=2026-05-24T00:00:00Z
```

**Query parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `status` | string | — | Filter: `ready`, `active`, `closed` |
| `department` | string | — | Filter by department |
| `from` | string | — | ISO 8601. Sessions created after this time. |
| `to` | string | — | ISO 8601. Sessions created before this time. |
| `limit` | integer | 20 | Max 100 |
| `cursor` | string | — | Pagination cursor from previous response |

**Response: 200 OK**

```json
{
  "data": [ /* array of session objects */ ],
  "has_more": true,
  "next_cursor": "sess_xyz789"
}
```

### 3.5 Update Session Register

```
PATCH /sessions/{session_id}/register
```

Change the translation register mid-session.

**Request body:**

```json
{
  "register": "simplified"
}
```

**Response: 200 OK**

```json
{
  "session_id": "sess_a1b2c3d4e5f6",
  "register": "simplified",
  "changed_at": "2026-05-24T14:38:00Z"
}
```

Register changes take effect for all subsequent utterances. In-flight utterances complete with the previous register.

---

## 4. Real-Time Translation (WebSocket)

The WebSocket endpoint `wss://clinical.orquor.com/api/v1/ws/translate` provides the real-time translation channel.

### 4.1 Connection

Connect with the session ID as a query parameter and authenticate with your API key:

```
wss://clinical.orquor.com/api/v1/ws/translate?session=sess_a1b2c3d4e5f6&token=orq_live_xxx
```

Or authenticate in the first frame if you opened the socket without query parameters:

```json
{"type": "auth", "api_key": "orq_live_xxx", "session_id": "sess_a1b2c3d4e5f6"}
```

### 4.2 Client → Server frames

| Frame type | Format | Description |
|---|---|---|
| Audio | Binary (Opus-encoded) | Audio chunk. Max 20ms of audio per frame. |
| Control | JSON text | Session control messages (see below) |
| Ping | — | WebSocket ping frame every 30 seconds to keep connection alive |

**Control message: change register**

```json
{
  "type": "register_change",
  "register": "simplified"
}
```

**Control message: pause/resume**

```json
{
  "type": "pause"
}
```

```json
{
  "type": "resume"
}
```

The server responds with `{"type": "paused"}` or `{"type": "resumed"}`. While paused, audio is not processed but the session remains active.

**Control message: end session**

```json
{
  "type": "end_session"
}
```

Equivalent to `POST /sessions/{id}/close`.

### 4.3 Server → Client frames

| Frame type | Format | Description |
|---|---|---|
| Translation | JSON text | Verified translation for a completed utterance |
| Partial | JSON text | Intermediate ASR result (before utterance boundary) |
| Event | JSON text | Session lifecycle events |
| Error | JSON text | Processing errors |

**Translation frame:**

```json
{
  "type": "translation",
  "utterance_id": 42,
  "source_transcript": "Administer 10 mg of morphine IV.",
  "translation": "Administrar 10 mg de morfina IV.",
  "register": "formal_clinical",
  "verified": true,
  "verifier_score": 17,
  "escalated": false,
  "latency_ms": 620,
  "timestamp": "2026-05-24T14:30:05.123Z"
}
```

| Field | Type | Description |
|---|---|---|
| `utterance_id` | integer | Sequential within session |
| `source_transcript` | string | ASR transcription of the source audio |
| `translation` | string | Verified translation in the target language |
| `register` | string | Register used for this translation |
| `verified` | boolean | Whether all verifiers passed |
| `verifier_score` | integer | Weighted sum of verifier results |
| `escalated` | boolean | Whether this utterance was escalated to a human interpreter |
| `latency_ms` | integer | End-to-end pipeline latency for this utterance |
| `timestamp` | string | ISO 8601 with millisecond precision |

**Partial frame (intermediate ASR, before utterance boundary):**

```json
{
  "type": "partial",
  "utterance_id": 42,
  "partial_transcript": "Administer 10 mg of...",
  "confidence": 0.91,
  "timestamp": "2026-05-24T14:30:04.800Z"
}
```

**Event frames:**

```json
{"type": "event", "event": "session_started", "timestamp": "..."}
```

```json
{"type": "event", "event": "session_closed", "timestamp": "...", "total_utterances": 52}
```

```json
{"type": "event", "event": "escalated", "utterance_id": 42, "reason": "verifier_failure"}
```

```json
{"type": "event", "event": "interpreter_assigned", "utterance_id": 42, "eta_seconds": 12}
```

```json
{"type": "event", "event": "interpreter_translation", "utterance_id": 42}
```

**Error frame:**

```json
{
  "type": "error",
  "code": "audio_format_invalid",
  "message": "Unsupported audio codec. Expected Opus.",
  "utterance_id": null,
  "timestamp": "2026-05-24T14:30:06.000Z"
}
```

### 4.4 Audio format requirements

| Property | Requirement |
|---|---|
| Codec | Opus |
| Sample rate | 16 kHz or 48 kHz |
| Channels | 1 (mono) |
| Frame size | 20 ms (recommended) |
| Bitrate | 32 kbps (recommended for voice) |

The server sends `audio_format_invalid` error if the codec or sample rate is not supported. Audio frames exceeding 20ms may be split internally, increasing latency.

---

## 5. Audit Logs

### 5.1 Get Session Audit Log

```
GET /sessions/{session_id}/audit-log
```

Retrieve the complete audit log for a session.

**Query parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `format` | string | `jsonl` | `jsonl` (JSON Lines, one object per line) or `json` (JSON array) |
| `include_audio_refs` | boolean | `false` | Include source audio S3 references |
| `limit` | integer | 1000 | Max entries per page |
| `cursor` | string | — | Pagination cursor |

**Response: 200 OK**

Content-Type: `application/x-jsonlines`

```
{"session_id":"sess_a1b2c3d4e5f6","utterance_id":1,"timestamp":"...","asr":{...},"mt":{...},"verifier":{...},"crypto":{...}}
{"session_id":"sess_a1b2c3d4e5f6","utterance_id":2,"timestamp":"...","asr":{...},"mt":{...},"verifier":{...},"crypto":{...}}
...
```

Response headers include:

| Header | Description |
|---|---|
| `X-Audit-Log-Entries` | Total number of entries |
| `X-Audit-Log-Suite-Version` | Verifier suite version used |
| `X-Audit-Log-TSA` | Cryptographic timestamp authority used |
| `X-Audit-Log-Manifest-Hash` | SHA-256 of the Merkle tree root of all entry hashes |

### 5.2 Get Audit Log Manifest

```
GET /sessions/{session_id}/audit-log/manifest
```

Returns the verifiable manifest for the session's audit log. Use this for independent verification against the TSA without trusting Orquor.

**Response: 200 OK**

```json
{
  "session_id": "sess_a1b2c3d4e5f6",
  "total_entries": 52,
  "merkle_root": "abcdef1234567890...",
  "tsa": "rfc3161",
  "tsa_certificate_fingerprint": "SHA256:abcdef...",
  "first_timestamp": "2026-05-24T14:30:05.000Z",
  "last_timestamp": "2026-05-24T14:44:58.000Z",
  "entry_hashes": [
    {"utterance_id": 1, "hash": "SHA256:abc123..."},
    {"utterance_id": 2, "hash": "SHA256:def456..."}
  ],
  "orchestrator_key_id": "ork-sign-2026-001",
  "verification_instructions": "Verify each entry's timestamp_token against the TSA public certificate. Verify the merkle_root against the ordered entry_hashes. Verify the orchestrator_signature on each entry against orchestrator_key_id."
}
```

### 5.3 Export Audit Logs (Batch)

```
POST /audit-logs/export
```

Request a batch export of audit logs across multiple sessions.

**Request body:**

```json
{
  "session_ids": ["sess_abc", "sess_def"],
  "date_range": {
    "from": "2026-05-01T00:00:00Z",
    "to": "2026-05-31T23:59:59Z"
  },
  "format": "jsonl",
  "notification_email": "compliance@hospital.example.com"
}
```

Either `session_ids` or `date_range` is required (both may be supplied for intersection).

**Response: 202 Accepted**

```json
{
  "export_id": "exp_a1b2c3d4",
  "status": "processing",
  "estimated_entries": 1240,
  "estimated_completion": "2026-05-24T14:50:00Z",
  "download_url": null
}
```

Check status:

```
GET /audit-logs/exports/{export_id}
```

**Response when complete:**

```json
{
  "export_id": "exp_a1b2c3d4",
  "status": "complete",
  "total_entries": 1240,
  "size_bytes": 524288,
  "download_url": "https://clinical.orquor.com/api/v1/audit-logs/exports/exp_a1b2c3d4/download?token=...",
  "download_expires_at": "2026-05-31T14:50:00Z",
  "manifest_hash": "SHA256:abcdef..."
}
```

Download URLs are pre-signed, valid for 7 days, and require the same API key for access.

---

## 6. Configuration

### 6.1 Get Account Configuration

```
GET /account
```

**Response: 200 OK**

```json
{
  "customer_id": "cust_abc123",
  "plan": "enterprise",
  "features": {
    "mtls": true,
    "custom_models": false,
    "single_tenant": false,
    "webhooks": true,
    "slack_support": true
  },
  "limits": {
    "max_concurrent_sessions": 50,
    "max_session_duration_minutes": 240,
    "audio_retention_days": 30,
    "audit_log_retention_years": 7
  },
  "webhook_url": "https://hospital.example.com/orquor-events",
  "webhook_secret": "whsec_..." ,
  "created_at": "2026-01-15T00:00:00Z"
}
```

### 6.2 Update Webhook Configuration

```
PATCH /account/webhooks
```

**Request body:**

```json
{
  "webhook_url": "https://hospital.example.com/orquor-events-v2",
  "enabled_events": [
    "session.started",
    "session.closed",
    "translation.verified",
    "translation.escalated",
    "translation.interpreter_correction"
  ]
}
```

**Response: 200 OK**

Returns updated account configuration.

### 6.3 Rotate API Key

```
POST /account/api-keys/rotate
```

**Request body:**

```json
{
  "key_id": "ork_sign_2026_001"
}
```

**Response: 200 OK**

```json
{
  "key_id": "ork_sign_2026_002",
  "api_key": "orq_live_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
  "expires_at": "2027-05-24T00:00:00Z",
  "previous_key_expires_at": "2026-05-31T00:00:00Z"
}
```

Previous key remains valid for 7 days to allow transition.

---

## 7. Webhooks

Orquor Clinical sends HTTP POST requests to your configured webhook URL when events occur.

### 7.1 Webhook signature

Every webhook includes an `X-Orq-Webhook-Signature` header for verification:

```
X-Orq-Webhook-Signature: t=1700000000,v1=abcdef123456...
```

Verify using HMAC-SHA256 with your webhook secret (available in Console):

```
HMAC-SHA256(timestamp + "." + body, webhook_secret)
```

### 7.2 Event types

| Event | Description | Payload |
|---|---|---|
| `session.started` | Session begins processing audio | `session_id`, `department`, `timestamp` |
| `session.closed` | Session terminated | `session_id`, `total_utterances`, `total_escalations`, `timestamp` |
| `translation.verified` | Translation passed all verifiers | `session_id`, `utterance_id`, `source_transcript`, `translation`, `verifier_score`, `latency_ms`, `timestamp` |
| `translation.escalated` | Utterance escalated to human | `session_id`, `utterance_id`, `verifier_failures`, `reason`, `timestamp` |
| `translation.interpreter_correction` | Interpreter corrected the translation | `session_id`, `utterance_id`, `original_translation`, `corrected_translation`, `interpreter_id`, `timestamp` |
| `session.error` | Non-recoverable session error | `session_id`, `error_code`, `message`, `timestamp` |

### 7.3 Retry policy

Failed webhook deliveries are retried with exponential backoff: 1s, 5s, 25s, 125s, 625s (5 attempts total). After final failure, the event is logged and available via the Events API. Webhooks that return 2xx are considered delivered. Webhooks that return 410 Gone are not retried (endpoint deliberately removed).

---

## 8. Common Types

### 8.1 Language codes

| Code | Language |
|---|---|
| `en` | English |
| `es` | Spanish |

Additional language pairs (Portuguese, French, Mandarin, Arabic) are on the roadmap. Contact sales@orquor.com for early access.

### 8.2 Department codes

| Code | Description |
|---|---|
| `emergency` | Emergency Department |
| `operating_room` | Operating Room / Surgery |
| `icu` | Intensive Care Unit |
| `pharmacy` | Pharmacy |
| `pediatrics` | Pediatrics |
| `psychiatry` | Psychiatry / Mental Health |
| `admissions` | Patient Admissions / Registration |
| `general` | General practice / unspecified |

### 8.3 Register codes

| Code | Description |
|---|---|
| `formal_clinical` | Technical medical register. Physician-to-physician, clinical documentation. |
| `simplified` | Plain-language register. Patient-facing, discharge instructions, informed consent. |
| `legal` | Legal register. Medico-legal documentation, court-admissible. |

### 8.4 Consent methods

| Code | Description |
|---|---|
| `verbal_recorded` | Consent captured in the audio recording |
| `written_form` | Signed consent form on file |
| `implied_emergency` | Emergency exception — consent not obtainable |

---

## 9. Error Codes

The API uses standard HTTP status codes and returns JSON error bodies.

### HTTP status codes

| Status | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 202 | Accepted (async operation) |
| 204 | No Content (successful deletion) |
| 400 | Bad Request — malformed input |
| 401 | Unauthorized — missing or invalid API key |
| 403 | Forbidden — valid key but insufficient permissions |
| 404 | Not Found — session or resource does not exist |
| 409 | Conflict — resource state prevents operation (e.g., closing an already-closed session) |
| 429 | Too Many Requests — rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable — maintenance or overload |

### Error body

```json
{
  "error": {
    "code": "session_not_found",
    "message": "Session sess_xyz does not exist or has expired.",
    "request_id": "req_a1b2c3d4",
    "documentation_url": "https://docs.orquor.com/api/errors#session_not_found"
  }
}
```

### Error code reference

| Code | HTTP | Description |
|---|---|---|
| `invalid_request` | 400 | Request body does not match schema |
| `missing_required_field` | 400 | Required field not provided |
| `invalid_field_value` | 400 | Field value fails validation (e.g., unsupported language) |
| `invalid_idempotency_key` | 400 | Idempotency key reuse with different body |
| `authentication_required` | 401 | No API key provided |
| `invalid_api_key` | 401 | API key is invalid, expired, or revoked |
| `insufficient_permissions` | 403 | API key lacks required permission |
| `session_not_found` | 404 | Session ID does not exist |
| `session_expired` | 404 | Session has expired (4-hour inactivity timeout) |
| `session_already_closed` | 409 | Session is already closed |
| `session_limit_exceeded` | 429 | Concurrent session limit reached |
| `audio_format_invalid` | 400 | WebSocket audio format not supported |
| `audio_frame_too_large` | 400 | WebSocket audio frame exceeds 20ms |
| `rate_limit_exceeded` | 429 | Request rate limit exceeded |
| `internal_error` | 500 | Unexpected server error |
| `service_unavailable` | 503 | Service in maintenance or degraded |
| `export_not_ready` | 404 | Audit log export is still processing |
| `export_expired` | 404 | Audit log export download link expired |

---

## 10. Rate Limits

| Endpoint category | Rate limit | Window |
|---|---|---|
| Session management (create, close, list) | 60 requests | Per minute |
| Audit log retrieval | 30 requests | Per minute |
| Audit log export | 10 requests | Per hour |
| Account configuration | 20 requests | Per minute |
| WebSocket connections | 10 connections | Per minute |

Rate limits are per API key. Exceeded limits return `429 Too Many Requests` with a `Retry-After` header. Enterprise customers may request higher limits via support@orquor.com.

Rate limit response headers:

| Header | Description |
|---|---|
| `X-RateLimit-Limit` | Request limit per window |
| `X-RateLimit-Remaining` | Remaining requests in current window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |

---

## 11. Pagination

List endpoints use cursor-based pagination.

**Request:**

```
GET /sessions?limit=20&cursor=sess_abc123
```

**Response:**

```json
{
  "data": [ /* array of resources */ ],
  "has_more": true,
  "next_cursor": "sess_xyz789"
}
```

- `limit`: Maximum items per page (1–100, default 20)
- `cursor`: Opaque string from `next_cursor` in previous response. Omit for first page.
- `has_more`: `true` if more items exist
- `next_cursor`: Cursor for the next page. `null` if `has_more` is `false`

Cursors are opaque and may change format. Do not construct or decode them.

---

## 12. Changelog

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05 | Initial API reference. Sessions, WebSocket, audit logs, webhooks, account config. |

---

## Appendix A: Quick Start — cURL

```bash
# Set your API key
export ORQ_KEY="orq_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Create a session
curl -X POST https://clinical.orquor.com/api/v1/sessions \
  -H "Authorization: Bearer $ORQ_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{
    "customer_id": "cust_abc123",
    "department": "emergency",
    "source_language": "en",
    "target_language": "es",
    "register": "formal_clinical",
    "consent_verified": true
  }'

# Get session status
curl https://clinical.orquor.com/api/v1/sessions/sess_a1b2c3d4e5f6 \
  -H "Authorization: Bearer $ORQ_KEY"

# Get audit log
curl https://clinical.orquor.com/api/v1/sessions/sess_a1b2c3d4e5f6/audit-log \
  -H "Authorization: Bearer $ORQ_KEY" \
  -o audit_log.jsonl

# Close session
curl -X POST https://clinical.orquor.com/api/v1/sessions/sess_a1b2c3d4e5f6/close \
  -H "Authorization: Bearer $ORQ_KEY"
```

## Appendix B: Quick Start — WebSocket (wscat)

```bash
# Connect to translation session
wscat -c "wss://clinical.orquor.com/api/v1/ws/translate?session=sess_a1b2c3d4e5f6&token=$ORQ_KEY"

# In the wscat session, send a control message:
> {"type": "register_change", "register": "simplified"}

# Audio is sent as binary frames via the WebSocket API client library of your choice.
# See SDK examples at https://docs.orquor.com/sdks
```

---

**Questions?** API support: support@orquor.com · Documentation: https://docs.orquor.com · Status: https://status.orquor.com
