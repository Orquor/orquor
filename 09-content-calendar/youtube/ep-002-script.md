# YouTube Episode 2 — "How Verifiers Work — Live Coding Session"

**Length target**: 10–12 minutes · **Hook**: 0:00–0:20 · **Body**: 0:20–9:30 · **CTA**: 9:30–11:00

---

## [0:00–0:20] HOOK

*[Founder on camera. Behind: laptop visible with code editor open.]*

> "Last week I told you ACTO is the category that should exist in healthcare AI. This week I am going to show you the actual code that makes ACTO work. We are going to write a verifier, run it against real translation output, watch it fail, fix the translation, and watch it pass. Ten minutes. No marketing. Just code."

## [0:20–1:00] CONTEXT

> "If you watched episode one, you know the verifier suite is the part of Orquor Clinical that distinguishes us from every other healthcare AI vendor. A verifier is a deterministic test that runs after the model produces a translation. It checks one specific property of that translation. Pass or fail. Structured reason. Signed weight.
>
> Today we are writing a real verifier. The kind that ships in production. The code on screen is the same code that runs before every translation reaches a clinician's screen at Orquor Clinical."

## [1:00–4:00] SCREEN SHARE — Writing the first verifier

*[Switch to screen share. Code editor open with VSCode, Python file `translation_verifiers.py`.]*

> "We are going to verify that when a doctor speaks a numeric dosage in English, that exact dosage appears in the Spanish translation. No dropped decimals. No converted units. Exact preservation.
>
> Step one — define the data type for what a verifier returns."

*[Types `@dataclass` definition for VerifierResult.]*

> "A VerifierResult has three fields: passed (boolean), weight (signed integer), and reason (optional string). The orchestrator sums weights across the entire suite to make the gating decision. The reason is for forensic audit later.
>
> Step two — the extraction helper. We need to pull numeric dosages out of arbitrary text. We use a regex."

*[Types the NUMERIC_DOSAGE_RE regex pattern.]*

> "The pattern matches numbers followed by pharmacological units — milligrams, micrograms, milliliters, units, IU. Case-insensitive. The number capture group preserves the decimal. The unit capture group normalizes to lowercase.
>
> Step three — the verifier function itself."

*[Types verify_dosage_preserved function. Shows docstring with `Weight: +5`.]*

> "The function takes source text and translated text. Extracts dosages from both. Computes the set difference. If the source has any dosage that is missing from the translation, the verifier fails with weight +5 — catastrophic — and a structured reason naming the missing dosage. If everything matches, it passes."

## [4:00–6:30] SCREEN SHARE — Running it

*[Run pytest in terminal.]*

```
$ pytest verifiers/translation_verifiers.py::test_v1_dosage_preserved -v
```

> "Two test cases. The first: 'Administer 10 mg of morphine IV.' translated as 'Administrar 10 mg de morfina IV.' The dosage 10 mg appears in both. The verifier passes.
>
> The second test case: 'Patient receives 0.5 mg lorazepam.' translated as 'El paciente recibe 0.5 mg de lorazepam.' Same thing. Decimal preserved. Verifier passes.
>
> Now let me show you what failure looks like. I am going to add a bad translation case."

*[Adds a test case where translation drops the decimal.]*

```python
def test_dosage_dropped_decimal_fails():
    r = verify_dosage_preserved(
        "Administer 0.1 mg of fentanyl IV.",
        "Administrar 1 mg de fentanilo IV.",  # decimal dropped
    )
    assert not r.passed
    assert r.weight == 5
```

> "Source says 0.1 mg of fentanyl. Translation says 1 mg of fentanyl. Ten times the dose. In a real OR, this is a life-ending error.
>
> Run pytest."

*[Pytest runs. Test passes — meaning the verifier correctly caught the failure.]*

> "Pytest is green because the test asserts the failure, and the verifier correctly returned failure with the dropped decimal in the reason field. Read the failure reason."

*[Reads aloud: "Dosage value(s) {('0.1', 'mg')} present in source but not in translation".]*

> "The reason is structured. It names the exact dosage that was lost. A forensic auditor reading the audit log five years from now can reconstruct exactly what failed. Not 'something went wrong'. 'Zero point one milligrams was lost.'"

## [6:30–8:30] SCREEN SHARE — The orchestrator integration

> "A single verifier is useful but not enough. In production we run sixty of them across nine clinical specialties. Let me show you what the orchestrator does with the results."

*[Shows the orchestrator.py and how it sums weights.]*

> "Every utterance produces a VerifierResult per verifier in the suite. The orchestrator collects them. Computes the weighted sum. If the sum is above the gating threshold, the translation is delivered. If below, the orchestrator either re-runs the MT with the failure as feedback, or escalates to a certified interpreter.
>
> The threshold is configured per specialty. The ER is stricter. The Pharmacy is stricter still. Admissions is more lenient."

## [8:30–9:30] AUDIT LOG ENTRY

> "And finally — the verifier result becomes part of the per-utterance audit log entry. Cryptographically timestamped. Signed. Append-only. The hospital can produce it on demand five years from now, and an independent auditor can verify it without trusting us."

*[Shows a JSON example of an audit log entry with verifier_results field populated.]*

## [9:30–11:00] CTA

> "Three things you can do.
>
> One. If you want the full sixty-verifier suite for your own research, email research@orquor.com. We share it under collaboration license.
>
> Two. If you build healthcare AI and want to apply this methodology to your own system — the whitepaper has the full design framework. Orquor.com slash whitepaper.
>
> Three. Subscribe. Episode three next week is the cryptographic audit log — what it actually looks like, how OpenTimestamps anchors to Bitcoin work, and how a hospital's lawyer verifies an audit log entry in court.
>
> I am Freddy. We are Orquor. We build orchestration you can audit. See you next week."

*[End frame.]*

---

## Production notes

- B-roll: terminal with code, pytest green, audit log JSON pretty-printed, OpenTimestamps verification web page
- Camera angle: lower-third overlay "Freddy | Founder, Orquor" for first 4 seconds
- Editing: Descript auto-captions ON. Lower-thirds for code references.
- Length tolerance: 10–12 min. Cut if exceeding.

## Distribution

- YouTube main publish, 09:00 UTC-5 on the scheduled day
- 90-second vertical clip from [4:00–5:30] (the test failing on dropped decimal — most viral moment)
- LinkedIn carousel of the verifier code, posted Day 11
- X thread (dia-011 in `x-twitter/`)
