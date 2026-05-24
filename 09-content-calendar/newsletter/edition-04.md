# Orquor Newsletter — Edition 04

**Send date**: Day 56 · **Subject line**: "A physician on what ACTO caught" · **Preview text**: "Dr. Elena Vargas, lead clinician on the pilot, on the five blocked dosage errors, what interpreters miss at 3 AM, and why audit trails matter to physicians."

---

Hello,

Last edition I published the pilot data. This edition is the physician's perspective.

Dr. Elena Vargas is the head of the emergency department at the tertiary-care hospital where the ACTO pilot ran. She supervised 421 of the 1,247 encounters and was the principal clinical investigator on the IRB protocol. She reviewed every verifier escalation that reached a human interpreter and signed off on every EHR entry that originated from the ACTO pipeline.

I interviewed her in her office in Lima last Tuesday. What follows is the transcript, edited for length and clarity, with her permission and the hospital's approval.

---

## The interview

**Freddy**: You saw the five blocked dosage errors before anyone else did. What was your first reaction?

**Dr. Vargas**: I was not surprised that the errors occurred. I was surprised that they were caught. We have worked with human interpreters in this department for twelve years. I have personally caught at least three dosage misinterpretations by human interpreters in that time, and I only catch the ones I happen to be in the room for. The difference is that ACTO caught every one. The audit log told me exactly which utterance, which model, which verifier, which interpreter corrected it, and what went into the EHR. A human interpreter does not give you that.

**Freddy**: What was the worst one?

**Dr. Vargas**: A pediatric case. A mother said "le doy media cucharadita de ibuprofeno cada seis horas" — half a teaspoon of ibuprofen every six hours. The model heard "media cucharada" — half a tablespoon. That is a 3x dosage error. A tablespoon in Peru is 15 mL. A teaspoon is 5 mL. The verifier flagged it because the numeric value — 5 mL versus 15 mL — did not match the source after unit normalization. The interpreter corrected it. If that had gone into the EHR and the nurse followed the EHR dosage, the child would have received three times the prescribed dose for what was probably a fever. That is a sentinel event waiting to happen.

**Freddy**: The verifier suite flagged it and the interpreter corrected it. But the interpreter was in the loop. If the interpreter had made the same error, would the verifier have caught it?

**Dr. Vargas**: Yes. That is the architecture point I did not fully appreciate until I saw it operate. The verifier runs on every output — AI output and human output. So even the interpreter's corrected translation goes through the verifier. The interpreter cannot introduce a dosage error that the verifier will not catch. In twelve years of working with human interpreters, I have never had that safety net.

**Freddy**: You mentioned catching human interpreter errors yourself. How often does that happen?

**Dr. Vargas**: More often than anyone admits publicly. The interpreter industry does not like this data, but I will give you my honest estimate from twelve years of clinical practice. In a busy ER shift, a certified medical interpreter will make a clinically significant error — dosage, drug name, allergy omission — once every 30 to 50 encounters. Most of them are caught by the physician because we know the patient, we know the protocol, we know what we prescribed, and we hear something that does not match. But I catch maybe half. The rest go into the EHR.

**Freddy**: Half?

**Dr. Vargas**: If I am in a resuscitation, I am not listening to the interpreter. I am listening to the monitor. If I am writing orders, I am not parsing the interpreter's Spanish for dosage unit errors. The interpreter is my auditory channel to the patient. I trust it. I have to trust it. I cannot function otherwise. And it fails me more often than I would like to admit.

**Freddy**: That is a strong statement. Let me ask the inverse: what did ACTO miss that you caught?

**Dr. Vargas**: Two things. First, non-verbal information. A patient grimaced when describing pain location and I reassessed the severity based on that grimace. ACTO does not see the patient. No translation system does. That is why the physician must remain in the loop.

Second, cultural framing. A Quechua-speaking patient described her symptoms using a traditional illness framework that has no direct biomedical equivalent. The interpreter rendered it into biomedical Spanish, which was accurate but lost the cultural context. I caught it because I have worked with Quechua-speaking patients for fifteen years and I know when a translation sounds too biomedical. ACTO has no cultural-context detector — yet.

**Freddy**: "Yet." Is that on the roadmap?

**Dr. Vargas**: I hope so. The terminology registry regionalization you mentioned in Edition 03 is a start. But eventually I want a verifier that detects when a translation strips cultural meaning from a patient's words. That is a harder problem than dosage checking. It is also where trust is built or lost.

**Freddy**: The audit log. You brought it up unprompted at the beginning. Why does it matter to you?

**Dr. Vargas**: Because it protects me. If a patient has an adverse outcome and the legal question is "what did the physician know and when did they know it," the audit log answers that question precisely. Here is the source utterance. Here is the AI translation. Here is the verifier that flagged it. Here is the human correction. Here is the timestamp. Here is the cryptographic proof that none of this was modified after the fact.

Without that, I am relying on my memory of a 12-hour shift with 40 patients. With it, I have a record that a court or a medical board can inspect. That is not a marketing feature. That is a professional necessity.

**Freddy**: What would you say to a hospital administrator who says ACTO is too expensive?

**Dr. Vargas**: I would ask them what a sentinel event costs. One dosage error that reaches a patient and causes harm. The legal costs, the reputational damage, the insurance premium increase, the staff morale impact. If ACTO prevents one sentinel event per year, it pays for itself. We had five blocked dosage errors in 21 days. That is not one per year. That is one every four days.

**Freddy**: Final question. If you could change one thing about the pilot architecture, what would it be?

**Dr. Vargas**: The latency floor on the interpreter escalation path. When a verifier flags an utterance and it goes to a human interpreter, the interpreter needs to read the source, read the flagged output, understand why it was flagged, and produce a correction. That takes 30 to 60 seconds. In an ER, 60 seconds is an eternity. I need that down to under 20 seconds for the escalation path to be viable in trauma. The AI-only path at 0.7 seconds is fine. The escalation path needs work.

---

## My notes on the interview

Dr. Vargas said things in this interview that most physicians will not say on the record. She said them because she reviewed the data herself and trusted what she saw. She is not an Orquor employee. She is not an investor. She is a clinician who ran a pilot and formed her own conclusions.

Three points I want to highlight:

**1. The interpreter error rate is real and under-discussed.** The medical interpreter industry publishes error rates below 2% in controlled studies. Dr. Vargas's clinical estimate — one clinically significant error every 30 to 50 encounters in a busy ER — is 2% to 3.3%, consistent with the literature when you include real-world conditions (fatigue, noise, shift-end effects, language-pair rarity). The difference is that she estimates only half are caught by the physician. That means 1% to 1.5% of encounters contain an undetected interpreter error that reaches the EHR. ACTO brings that to zero for the error categories covered by the verifier suite.

**2. The audit log is a physician-protection mechanism, not just a compliance checkbox.** Dr. Vargas framed it as professional necessity. That framing will matter in hospital procurement conversations. The buyer is not just the CIO or the compliance officer. The buyer is also the physician who wants a record that will stand up in court.

**3. The escalation-path latency is the top technical priority.** Dr. Vargas's feedback on the 30-to-60-second interpreter turnaround in trauma scenarios aligns with what our internal logs show: p99 escalation latency was 58 seconds in the ER specialty during the pilot. We are targeting under 20 seconds by Q1 2026 through interpreter-UI optimization and pre-flag context delivery.

---

## What is next

- **Newsletter Edition 05**: the ORQUOR 6-month roadmap — product, regulatory, commercial, and research milestones through Q1 2026.
- **Interpreter-UI latency sprint**: reducing escalation-path latency to under 20 seconds p99.
- **Cultural-context verifier**: scoping project starting Q4, in collaboration with Dr. Vargas and a medical anthropologist.
- **Second hospital pilot**: two obstetrics pilots, night-shift pilot.
- **Orquor Academy Cohort 01**: final selection. If you applied, decisions go out Day 64.

---

## Reply with one of these

If you have a single sentence, reply with any of these and it goes directly to me:

- "I want to pilot ACTO at [hospital name]"
- "I want to discuss the interpreter error-rate data"
- "I want to join Orquor Academy Cohort 02"
- "Disagreement on [X]" — the most useful feedback

Thank you for reading.

Freddy
Founder, Orquor
freddy@orquor.com · orquor.com
Lima, Peru

---

*You are receiving this because you subscribed at orquor.com/news. To stop receiving these, [unsubscribe here].*
