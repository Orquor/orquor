# Email — Follow-up Post-Reunión con Prospect

**Trigger**: Sales-Bot detects a completed discovery/demo meeting in calendar.
**From**: `freddy@orquor.com`
**Subject**: After our conversation — three things

---

Hi [First Name],

Thank you for the time today. Three things from our conversation, in the order they came up:

**1. The specific question you asked about [topic from meeting notes].**

Here is the technical answer you asked for: [direct answer, no marketing tone, with specifics — number, citation, or pointer to whitepaper section].

If you want to go deeper, [Whitepaper Section X / link to specific blog post / link to a verifier code sample].

**2. The concern about [specific concern raised].**

You are right that this is non-trivial. Here is exactly how we address it: [specific mechanism — a verifier, an architectural choice, a regulatory mapping]. If your team wants to see the implementation, I will set up a 30-minute technical deep dive with our engineering team next week.

**3. The next step you proposed.**

[Restate the proposed next step in their words. If they did not propose one, suggest the smallest possible commitment — typically a 30-minute follow-up with a specific person on their team, or sharing the whitepaper with one named colleague.]

Calendly link, if useful: [link]

A small thing that may help your internal conversation: I attached the one-page summary of our ACTO architecture. It is what I would hand to your CMO or CIO if I were you and wanted to bring them along without forcing a meeting.

I am at freddy@orquor.com or directly on Signal at [number]. Whatever cadence works for you, works for me.

Freddy
Founder, Orquor
freddy@orquor.com · orquor.com
Lima, Peru

---

**Notes for Hermes Sales-Bot**

Sales-Bot drafts this template from the meeting notes captured by Ops-Monitor-Bot (which transcribes the recording into the prospect's record in the prospect database). The bot fills the three bracketed sections from:

1. The first technical question or skeptical statement in the meeting transcript
2. The first explicit concern or objection in the transcript
3. The last commit ("we will follow up", "let me think about it", "send me X") in the transcript

Human review is mandatory before sending. The bot drafts; the founder edits and sends. Average human edit time should be under 5 minutes per draft once Sales-Bot is well-tuned.

Attach the one-page ACTO summary PDF (in `/02-brand/` once produced, currently the abstract section of the whitepaper as a standalone page).
