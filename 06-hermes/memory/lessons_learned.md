# Orquor Hermes — Lessons Learned

Cross-task patterns that have appeared in two or more contexts. New entries appended at top with date.

---

## 2026-05-24 — Initial seed lessons (carried over from OpenClaw Atlas discipline)

1. **Verifier suites must include at least one negative verifier.** A suite composed only of positive verifiers cannot detect leakage of disallowed content. This was reaffirmed during the design of `verify_no_excluded_names` and `verify_no_english_leakage`.

2. **Outcome-only is non-negotiable.** Any feedback that pushes Hermes toward trace-based evaluation ("verify the agent invoked tool X") is to be marked CONTESTED unless it can be reformulated as an outcome check.

3. **Composite verifiers obscure failure attribution.** A single check that bundles dosage + units + drug-name is impossible to debug. Split atomically into V1 (dosage), V2 (units), V3 (drug-name).

4. **Translation length should be a soft verifier, not hard.** Cultural-linguistic variance is real; a 1.8× length ratio in Spanish vs English is normal for clinical text. Weight V7 at +1, not +5.

5. **Ambient engagement before outreach.** From sales motion discipline: cold outreach without preceding ambient engagement is rejected by Sales-Bot's verifier.
