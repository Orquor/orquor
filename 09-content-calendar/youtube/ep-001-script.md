# YouTube Episode 1 — "What is Auditable Clinical Translation Orchestration?"

**Length target**: 12 minutes · **Hook**: 0:00-0:15 · **Body**: 0:15-10:30 · **CTA**: 10:30-12:00

---

## [0:00–0:15] HOOK

*[Founder on camera, neutral background, eye contact]*

> "There is a category that should exist in healthcare AI and doesn't. The people building in it don't have a name for it. The people buying are paying for two products that pretend to be one market. In the next twelve minutes I'm going to walk you through what's broken and what should replace it."

## [0:15–0:45] OPENING — Who, what, why

> "I'm Freddy. I'm the founder of Orquor. We build verifier-backed multi-agent orchestration for healthcare and other regulated industries. Before Orquor I was an AI trainer for some of the most demanding agent-evaluation projects in the world — outcome-based rubric design, blocker injection, model-response evaluation. That's relevant because the category I'm about to describe applies the rigor of frontier eval research to clinical AI."

## [0:45–2:00] THE PROBLEM — the bifurcation

*[Cut to slide with the 7-axis comparison table]*

> "The medical-interpretation market in 2026 has split into two categories that both fail healthcare.
>
> Category one: video remote interpretation and over-the-phone interpretation. LanguageLine, Cloudbreak, Stratus, Voyce. Human interpreters on demand. Accurate but slow — fifteen to sixty seconds of latency just to connect. Expensive — $1.50 to $2.50 per minute. The audit trail is metadata only. The actual translation evaporates the moment the session ends.
>
> Category two: AI-only translation. Wordly, DeepL, hospitals hacking GPT or Claude themselves. Fast — under two seconds. Cheap — pennies per minute. But there's no audit trail. No verifier. No way for a hospital to defend a mistranslation in court when the patient's family lawyer subpoenas the records.
>
> Neither of these is the actual job. The actual job is fast enough for the OR, cheap enough for a Latin American budget, and defensible enough for an adverse-event review. That's a three-way trade-off. Today nobody is positioned to solve all three."

## [2:00–4:30] THE CATEGORY — define ACTO

*[Cut to slide titled "ACTO"]*

> "I propose a third category. We're calling it Auditable Clinical Translation Orchestration. ACTO.
>
> An ACTO system is defined by simultaneous performance on seven axes:
>
> One. Latency under two seconds to first token.
> Two. Cost between twenty cents and eighty cents per minute — order of magnitude below human VRI, order of magnitude above AI-only.
> Three. Medical word error rate at or below five percent.
> Four. Translation faithfulness measured by COMET-22 at or above 0.86.
> Five. Per-utterance audit log with cryptographic timestamping. RFC 3161 or OpenTimestamps. Not just metadata.
> Six. Specialty register adaptation. ER doesn't sound like Pharmacy doesn't sound like Psychiatry.
> Seven. Mathematical defensibility for HIPAA, Peruvian Law 29733, Brazilian LGPD, and GDPR.
>
> ACTO is not 'fast translation with extra features.' ACTO is a specific architecture: an orchestrator coordinating an ASR component, a register-adaptive translation component, a verifier suite, a cryptographic audit primitive, and a human interpreter pool. It's the synthesis that makes the trade-off go away."

## [4:30–7:00] THE VERIFIER LOOP — the technical heart

*[Show code on screen — the verify_dosage_preserved function]*

> "The verifier suite is the part that doesn't exist anywhere else. Let me show you what it looks like.
>
> *[reads code aloud]*
>
> This is a verifier. One Python function. It extracts the numeric dosages from the source utterance and the translated utterance. It compares them. If a dosage value present in the source is missing in the translation, it returns failure with a structured reason and a signed weight of plus-five — meaning catastrophic.
>
> When a translation reaches the screen, it has passed through sixty of these. Some positive — 'the controlled substance name is preserved.' Some negative — 'no names from the privacy exclusion list appeared.' Some stylistic — 'register matches the requested formal-clinical.'
>
> The orchestrator computes the weighted sum. If the score crosses the gating threshold, the translation is delivered. If not, the orchestrator either retries the translation with the failure signal as input or escalates to a human interpreter. The decision is logged. Every step is in the audit record."

## [7:00–9:00] THE AUDIT PRIMITIVE — the legal layer

> "Now the cryptographic part. Every utterance gets a log entry. The log entry contains the session ID, the utterance ID, a reference to the encrypted audio blob, the ASR transcript, the translation, the verifier result, and a timestamp from an external cryptographic timestamping authority — Bitcoin blockchain anchoring via OpenTimestamps, or a commercial RFC 3161 service.
>
> The log is append-only. The hardware-key signature is verifiable by any external party without trusting Orquor. That last part is the key.
>
> Five years from now, in an adverse-event review or a malpractice deposition or a regulator's audit, the hospital can produce its complete audit log. Their lawyer can hand it to an independent auditor. The auditor can verify against the Bitcoin blockchain anchor without ever needing Orquor to participate. The truth of what was said and translated is mathematically demonstrable.
>
> That's what 'defensible' means. It's not a marketing word. It's a cryptographic property."

## [9:00–10:30] WHY OPEN — strategy reveal

> "We're publishing the ACTO whitepaper on arXiv next Tuesday. We're not patenting the category. We're not trademarking the term.
>
> Why? Because the category should not be owned by any single vendor. The implementations should compete on quality. We will compete by being the best implementation. But the category exists for everyone — for hospitals that need it, for regulators who need to point to it, for other builders who want to do this work right.
>
> If we own the term, we get a defensible moat in marketing. If we open the term, we get a defensible position in the industry — we are the implementation that defined the category. That second thing is worth more."

## [10:30–12:00] CTA

> "Three things you can do.
>
> One. If you work in clinical informatics, hospital procurement, or healthcare law and you want the whitepaper the moment it drops — go to orquor.com slash whitepaper and join the waitlist.
>
> Two. If you are building anything adjacent to this — even if it's competing with us directly — get in touch. We'd rather the category emerge in a coordinated way than a fragmented one.
>
> Three. Subscribe. Episode two next week will be the deep dive on verifier design, with code, with examples, with how to apply the methodology to your own clinical-AI deployment.
>
> I'm Freddy. I built Orquor in Lima. We're operating across Latin America and serving healthcare networks that demand both speed and proof. See you next Tuesday."

*[End frame: Orquor logo + URL]*

---

## Production notes

- B-roll: terminal with verifier code running, A100 GPU dashboard, OpenTimestamps verification page, hospital exterior shot.
- Camera: iPhone 15 Pro main lens, 4K, locked focus on face.
- Audio: Rode Wireless ME clip mic. Verify mono channel, -16 LUFS.
- Lighting: key light Aputure MC at 5600K, fill from softbox window-left.
- Background: solid color (warm gray or matte black). No clutter.
- Editing: Descript. Auto-captions enabled. Brand lower-third intro: "Freddy | Founder, Orquor" for 4 seconds.

## Distribution

- YouTube main upload (16:9), publish Day 3 at 09:00 UTC-5
- 60-second vertical short cut from the [4:30–5:30] segment, publish Day 4 on TikTok + Reels + YouTube Shorts
- LinkedIn carousel of 5 slides summarizing key points, publish Day 5
- X thread (drafted in `x-twitter/dia-005.md`), publish Day 5
