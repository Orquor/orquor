# Orquor Newsletter — Edition 01

**Send date**: Day 14 · **Subject line**: "The category called ACTO" · **Preview text**: "Two weeks of building in public + the whitepaper drops next Tuesday."

---

Hello,

If you are reading this, you are in the first cohort of people who follow Orquor closely. There are 1,200 of you. That is not a lot, but every one of you opted in deliberately, which makes it the most useful audience I will ever have. Thank you.

Every two weeks I will send you one of these. No clickbait, no upsell, no fluff. The deal is straightforward: I give you the technical and strategic depth I cannot fit into a LinkedIn post or a tweet, and you tell me when something is wrong.

---

## What we shipped in the last 14 days

**The category drop.** We named what we are building. **Auditable Clinical Translation Orchestration — ACTO.** The technical specification of ACTO is what the whitepaper formalizes. The whitepaper is on arXiv as of Tuesday and the full text is also linked from blog.orquor.com.

We made one deliberate choice that some readers questioned: we are publishing the spec openly. We are not patenting the category. We are not trademarking the term.

The reasoning is this. If we patent ACTO, we get a defensible moat in marketing for about three years before someone routes around it. If we publish ACTO openly, we get a defensible position in the industry — we are the implementation that defined the category. The second moat compounds. The first moat decays.

**The first benchmarks.** Preliminary single-site numbers on a 500-utterance evaluation set:

- Medical Word Error Rate (ER): 4.1% — Whisper Large v3 baseline is 11.8%
- COMET-22 translation quality (clinical Spanish): 0.87
- Latency p50 to verified output: 0.9 seconds
- Verifier pass rate: 94.2%
- Human escalation rate: 5.8% of utterances

These are preliminary. The full peer-reviewed benchmark publishes in 2026. We invite independent replication and will provide the evaluation set under research collaboration license.

**The verifier discipline.** Sixty weighted outcome-based pytest tests now run before any translation reaches the screen. A representative subset is in Section 4 of the whitepaper. Sample code:

```python
def verify_dosage_preserved(source, translated):
    """Numeric dosage in source must appear identically in translated.
    Weight: +5 (catastrophic if violated)."""
    s = extract_numeric_dosages(source)
    t = extract_numeric_dosages(translated)
    missing = s - t
    if missing:
        return VerifierResult(False, 5, f"Dosage {missing} missing in translation")
    return VerifierResult(True, 5)
```

If you have built outcome-based rubrics in any AI evaluation context, this will feel familiar. The novel contribution is applying the discipline to clinical translation with cryptographic audit logging on top.

## What I changed my mind about this week

I was wrong about the speed of memetic propagation. Two competitors began using the term "audit log" in their own marketing within seven days of the whitepaper preview going live. I had budgeted 60 days for the vocabulary to escape containment. It escaped in seven.

The implication: the next term we coin should be more carefully timed. A category vocabulary is a one-shot weapon. Fire it once, fire it well, then defend with implementation quality.

The second thing I was wrong about: I assumed the first inbound pipeline would come from hospital CIOs. It came from regulators. The Indecopi office of personal data protection emailed asking for a briefing on the ACTO compliance posture. The same week, two state health authorities in different LATAM countries requested similar briefings.

Selling to regulators is not selling. It is briefing. But the relationships translate into procurement signal because hospital CIOs ask their compliance teams which vendors the regulator is paying attention to. It is a different game than direct hospital sales, and we are running both.

## What is next

- **Newsletter Edition 02** (in two weeks): a deeper dive on the verifier-design methodology with three more functions and the rationale for each weight.
- **YouTube Episode 03** (this Sunday): live walkthrough of an OpenTimestamps verification on a real Orquor Clinical audit log entry. If you have ever wondered what cryptographic timestamping looks like in practice, this is the episode.
- **First hospital pilot** (target end-of-month, currently under NDA): we will publish the case study once the pilot is in production and the customer has approved disclosure.
- **Orquor Academy applications** (opening Day 60): the first cohort of the AI Trainers program. If you want early access to the syllabus, reply to this email and I will send it.

## Reply with one of these

If you have time for a single sentence, reply with any one of these and it goes directly to me:

- "Disagreement on [X]" — the most valuable feedback
- "I want to pilot ACTO at [hospital name]"
- "I want to join Orquor Academy Cohort 01"
- "Send me the verifier suite under research license"

Thank you for being part of this from the beginning.

Freddy
Founder, Orquor
freddy@orquor.com · orquor.com
Lima, Peru

---

*You are receiving this because you subscribed at orquor.com/news. To stop receiving these, [unsubscribe here].*
