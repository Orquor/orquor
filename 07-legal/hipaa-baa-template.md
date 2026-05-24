# BUSINESS ASSOCIATE AGREEMENT (BAA)

**Template — Orquor S.A.C.** · Version 2026-05. This template is provided for negotiation with US healthcare customers. **It must be reviewed by qualified US counsel licensed in the relevant state before signing.** Do not represent this template as legal advice.

---

This Business Associate Agreement (the "BAA") is entered into as of the date of last signature below (the "Effective Date") between:

**Covered Entity** ("CE")
[Hospital legal name]
[Address]

and

**Business Associate** ("BA")
**Orquor S.A.C.** (a société anonyme cerrada organized under the laws of the Republic of Peru, with US presence through [Orquor Inc., a Delaware corporation, if applicable])
[Address]

CE and BA are each individually a "Party" and collectively the "Parties."

## 1. Definitions

Terms used but not otherwise defined in this BAA shall have the meanings set forth in the Health Insurance Portability and Accountability Act of 1996 ("HIPAA") and its implementing regulations at 45 C.F.R. Parts 160 and 164, as amended (collectively, the "HIPAA Rules"), including the HITECH Act of 2009.

"PHI" means Protected Health Information as defined under the HIPAA Rules, limited to information BA creates, receives, maintains, or transmits on behalf of CE in connection with the services described in the Underlying Services Agreement.

## 2. Permitted Uses and Disclosures by BA

BA may use and disclose PHI solely:

(a) to perform the services described in the Underlying Services Agreement between the Parties (the "Services"), which include real-time speech recognition, machine translation, human interpreter orchestration, and cryptographically timestamped audit logging in connection with clinical encounters;

(b) for the proper management and administration of BA;

(c) to carry out BA's legal responsibilities, provided that any disclosure under this Section 2(b) or 2(c) is either (i) required by law or (ii) accompanied by reasonable assurances from the recipient that the PHI will be held confidentially and used or further disclosed only as required by law or for the purpose for which it was disclosed.

## 3. Obligations of BA

BA agrees to:

3.1 Not use or further disclose PHI other than as permitted or required by this BAA or as required by law.

3.2 Use appropriate safeguards, including administrative, physical, and technical safeguards required by the HIPAA Security Rule (45 C.F.R. §§ 164.308, 164.310, 164.312, 164.314, and 164.316), to prevent use or disclosure of PHI other than as provided by this BAA. Without limiting the foregoing, BA shall implement:

(a) encryption of PHI at rest using AES-256 or equivalent;
(b) encryption of PHI in transit using TLS 1.2 or higher;
(c) confidential computing for PHI processing (NVIDIA H100 confidential mode or equivalent) where technically available;
(d) cryptographic timestamping of audit log entries using RFC 3161 or equivalent;
(e) access controls implementing least-privilege principles and multi-factor authentication for all personnel with access to PHI.

3.3 Report to CE any use or disclosure of PHI not provided for by this BAA of which BA becomes aware, including breaches of unsecured PHI as required by 45 C.F.R. § 164.410. Reporting shall occur within **forty-eight (48) hours** of discovery for a breach of unsecured PHI and within **five (5) business days** for other reportable incidents.

3.4 Ensure that any subcontractors that create, receive, maintain, or transmit PHI on behalf of BA agree to the same restrictions and conditions that apply to BA with respect to such information, including the right of CE to terminate the subcontract for material breach.

3.5 Make available PHI in a designated record set to CE as necessary to satisfy CE's obligations under 45 C.F.R. § 164.524 within ten (10) business days of CE's request.

3.6 Make any amendment(s) to PHI in a designated record set as directed by CE pursuant to 45 C.F.R. § 164.526 within ten (10) business days.

3.7 Make available the information required to provide an accounting of disclosures of PHI in accordance with 45 C.F.R. § 164.528 within twenty (20) business days of CE's request.

3.8 Make BA's internal practices, books, and records relating to the use and disclosure of PHI received from, or created or received by BA on behalf of, CE available to the Secretary of HHS for purposes of determining CE's compliance with the HIPAA Rules.

## 4. Obligations of CE

4.1 CE shall notify BA of any limitations in CE's Notice of Privacy Practices that may affect BA's use or disclosure of PHI.

4.2 CE shall notify BA of any changes in, or revocation of, individual permission to use or disclose PHI.

4.3 CE shall not request BA to use or disclose PHI in any manner that would not be permissible under the HIPAA Rules if done by CE.

## 5. Term and Termination

5.1 **Term.** This BAA shall be effective as of the Effective Date and shall terminate on the termination of the Underlying Services Agreement, or sooner as provided herein.

5.2 **Termination for Cause.** Upon CE's knowledge of a material breach by BA, CE shall provide BA an opportunity to cure the breach within thirty (30) days. If BA does not cure within the cure period, CE may terminate this BAA and the Underlying Services Agreement immediately.

5.3 **Return or Destruction of PHI Upon Termination.** Upon termination of this BAA, BA shall return or, with CE's written authorization, destroy all PHI received from CE or created or received by BA on behalf of CE. BA shall retain no copies, except as required by law. Where return or destruction is infeasible, BA shall extend the protections of this BAA to the PHI and limit further uses and disclosures to those purposes that make return or destruction infeasible.

## 6. Audit Logs and Forensic Cooperation

6.1 BA maintains a per-utterance cryptographically timestamped audit log of all PHI processing operations performed in connection with the Services.

6.2 Upon CE's request, BA shall provide CE with the complete audit log for any session within five (5) business days, in a format that an independent third-party auditor can verify against the underlying cryptographic timestamping authority without trust in BA.

6.3 BA shall cooperate with CE in good faith in connection with any breach investigation, adverse-event review, or regulatory inquiry that relates to the Services.

## 7. Miscellaneous

7.1 **Regulatory References.** A reference in this BAA to a section in the HIPAA Rules means the section as in effect or as amended.

7.2 **Amendment.** The Parties agree to take such action as is necessary to amend this BAA from time to time as is necessary for the Parties to comply with the requirements of the HIPAA Rules.

7.3 **Interpretation.** Any ambiguity in this BAA shall be resolved to permit the Parties to comply with the HIPAA Rules.

7.4 **Survival.** The obligations of BA under Sections 2, 3, 5.3, 6, and this Section 7 shall survive the termination of this BAA.

7.5 **Governing Law.** This BAA shall be governed by and construed in accordance with the laws of [the State of Delaware / the relevant state of CE], without giving effect to its choice of law rules. Any dispute shall be resolved exclusively in the state or federal courts located in [Delaware / state].

7.6 **Entire Agreement.** This BAA, together with the Underlying Services Agreement, constitutes the entire agreement between the Parties with respect to the subject matter hereof. In the event of conflict between this BAA and the Underlying Services Agreement on matters governed by HIPAA, this BAA controls.

## 8. Signatures

**Covered Entity:**

By: ________________________________ Date: __________
Name: ______________________________
Title: ______________________________

**Business Associate — Orquor S.A.C.:**

By: ________________________________ Date: __________
Name: Freddy [Apellido]
Title: Chief Executive Officer

---

**Notes for internal Orquor review (not part of the agreement):**

- This template aligns with HHS sample BAA language updated for the 2026 regulatory environment.
- Sections 3.2(c) and 3.2(d) are Orquor-specific commitments and represent material differentiators against competitors who cannot match them.
- Section 6 establishes Orquor as the source of audit truth — this is the defensibility argument for ACTO.
- Negotiation latitude: most CEs will accept this template with minor modifications. Counsel-mandated red lines are typically around indemnification (negotiated separately in MSA) and notification windows in Section 3.3.
- Operate this template under attorney-client privilege review before each new customer.
