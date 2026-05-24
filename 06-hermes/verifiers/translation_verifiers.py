"""
Orquor Clinical — Translation Verifier Suite v1
================================================

Outcome-based pytest verifiers for the clinical translation pipeline.
Adapted from the OpenClaw Atlas methodology: each verifier checks one
property of the final translated output. Verifiers carry signed weights
in the docstring. The orchestrator weights them per the production policy.

To run:
    pytest verifiers/translation_verifiers.py -v
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

import pytest


# -----------------------------------------------------------------------------
# Verifier result type
# -----------------------------------------------------------------------------


@dataclass
class VerifierResult:
    passed: bool
    weight: int
    reason: str | None = None


# -----------------------------------------------------------------------------
# Helpers — small, deliberately simple. Production replaces with stronger NLU.
# -----------------------------------------------------------------------------


NUMERIC_DOSAGE_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(mg|mcg|g|ml|mL|cc|units?|UI|U)\b", re.IGNORECASE)
CONTROLLED_SUBSTANCES = {
    "morphine": "morfina",
    "fentanyl": "fentanilo",
    "oxycodone": "oxicodona",
    "midazolam": "midazolam",
    "ketamine": "ketamina",
    "propofol": "propofol",
}

# -----------------------------------------------------------------------------
# Clinical-domain constants for V9-V15 verifiers
# -----------------------------------------------------------------------------

NEGATION_EN_MARKERS = [
    r"\bdenies\b", r"\bno\s+history\s+of\b", r"\bwithout\b",
    r"\bdoes\s+not\s+have\b", r"\bnegative\s+for\b", r"\babsent\b",
    r"\bno\s+signs?\s+of\b", r"\bno\s+evidence\s+of\b",
]
NEGATION_ES_MARKERS = [
    r"\bniega\b", r"\bsin\b", r"\bno\s+(tiene|presenta|refiere|hay)\b",
    r"\bnegativo\s+(para|a)\b", r"\bausencia\s+de\b", r"\bno\s+hay\b",
]

ALLERGY_EN_MARKERS = [
    r"\ballergic\s+to\b", r"\ballergy\s+to\b", r"\bknown\s+allerg",
    r"\banaphyla", r"\bhypersensitivity\s+to\b",
]
ALLERGY_ES_MARKERS = [
    r"\balérgic[oa]\s+a\b", r"\balergia\s+a\b", r"\bhipersensibilidad\s+a\b",
    r"\banafilax", r"\breacción\s+alérgica\b",
]

MED_FREQ_EN = {
    r"\bonce\s+daily\b": r"\buna\s+vez\s+al\s+día\b",
    r"\btwice\s+daily\b": r"\bdos\s+veces\s+al\s+día\b",
    r"\bthree\s+times\s+daily\b": r"\btres\s+veces\s+al\s+día\b",
    r"\bBID\b": r"\b(cada\s+12\s+horas|dos\s+veces\s+al\s+día)\b",
    r"\bTID\b": r"\b(cada\s+8\s+horas|tres\s+veces\s+al\s+día)\b",
    r"\bQID\b": r"\b(cada\s+6\s+horas|cuatro\s+veces\s+al\s+día)\b",
    r"\bevery\s+(\d+)\s+hours?\b": r"\bcada\s+(\d+)\s+horas?\b",
    r"\bPRN\b": r"\b(según\s+necesidad|PRN|por\s+razón\s+necesaria)\b",
}

ANATOMY_EN = {
    "left arm": ["brazo izquierdo"],
    "right arm": ["brazo derecho"],
    "left leg": ["pierna izquierda"],
    "right leg": ["pierna derecha"],
    "chest": ["tórax", "pecho"],
    "abdomen": ["abdomen", "vientre"],
    "head": ["cabeza"],
    "neck": ["cuello"],
    "spine": ["columna"],
    "kidney": ["riñón"],
    "liver": ["hígado"],
    "lungs": ["pulmones"],
    "heart": ["corazón"],
}

SEVERITY_EN_MAP = {
    "mild": ["leve"],
    "moderate": ["moderado", "moderada"],
    "severe": ["grave", "severo", "severa", "intenso"],
    "critical": ["crítico", "crítica"],
}

CONTRAINDICATION_EN_MARKERS = [
    r"\bcontraindicated\b", r"\bcontraindication\b",
    r"\bdo\s+not\s+(use|administer|take)\b", r"\bshould\s+not\s+(be\s+used|receive)\b",
    r"\bnot\s+recommended\b", r"\bavoid\s+(use|in)\b",
]
CONTRAINDICATION_ES_MARKERS = [
    r"\bcontraindicad[oa]\b", r"\bcontraindicación\b",
    r"\bno\s+(usar|administrar|tomar|debe)\b", r"\bno\s+se\s+(recomienda|aconseja)\b",
    r"\bevitar\s+(el\s+)?uso\b",
]

INFORMED_CONSENT_EN = [
    r"\bI\s+understand\b", r"\brisks?\s+and\s+benefits?\b",
    r"\bvoluntaril\b", r"\bbefore\s+signing\b", r"\binformed\s+consent\b",
    r"\bI\s+have\s+been\s+informed\b", r"\bquestions?\s+have\s+been\s+answered\b",
]
INFORMED_CONSENT_ES = [
    r"\b(yo\s+)?(comprendo|entiendo)\b", r"\briesgos?\s+y\s+beneficios?\b",
    r"\bvoluntari[ao]\b", r"\bantes\s+de\s+firmar\b", r"\bconsentimiento\s+informado\b",
    r"\bhe\s+sido\s+informad[oa]\b", r"\bpreguntas?\s+han\s+sido\s+respondidas?\b",
]


def extract_numeric_dosages(text: str) -> set[tuple[str, str]]:
    """Return set of (value, unit) tuples found in the text."""
    return {(m.group(1), m.group(2).lower()) for m in NUMERIC_DOSAGE_RE.finditer(text)}


def classify_register(text: str) -> str:
    """
    Heuristic register classifier. Production replaces with a fine-tuned model.
    Returns one of: 'formal_clinical', 'simplified', 'legal'.
    """
    text_lower = text.lower()
    legal_markers = ["el paciente declara", "para efectos legales", "por la presente"]
    if any(m in text_lower for m in legal_markers):
        return "legal"
    formal_markers = ["administrar", "vía", "indicado", "diagnóstico"]
    if any(m in text_lower for m in formal_markers):
        return "formal_clinical"
    return "simplified"


# -----------------------------------------------------------------------------
# Verifier set V1 (representative — full production suite has ~60 of these)
# -----------------------------------------------------------------------------


def verify_dosage_preserved(source: str, translated: str) -> VerifierResult:
    """V1 — Numeric dosage in source must appear identically in translated. Weight: +5."""
    s = extract_numeric_dosages(source)
    t = extract_numeric_dosages(translated)
    missing = s - t
    if missing:
        return VerifierResult(False, 5, f"Dosage value(s) {missing} present in source but not in translation")
    return VerifierResult(True, 5)


def verify_unit_preserved(source: str, translated: str) -> VerifierResult:
    """V2 — Pharmacologic units in source must match those in translated. Weight: +5."""
    s_units = {u.lower() for _, u in extract_numeric_dosages(source)}
    t_units = {u.lower() for _, u in extract_numeric_dosages(translated)}
    missing = s_units - t_units
    if missing:
        return VerifierResult(False, 5, f"Unit(s) {missing} present in source but not in translation")
    return VerifierResult(True, 5)


def verify_controlled_substance_translated(source: str, translated: str) -> VerifierResult:
    """V3 — Controlled-substance names map to canonical Spanish term. Weight: +5."""
    source_lower = source.lower()
    translated_lower = translated.lower()
    for en, es in CONTROLLED_SUBSTANCES.items():
        if en in source_lower and es not in translated_lower:
            return VerifierResult(False, 5, f"Controlled substance '{en}' in source not represented as '{es}' in translation")
    return VerifierResult(True, 5)


def verify_no_excluded_names(translated: str, exclusion_list: list[str]) -> VerifierResult:
    """V4 (negative) — Translated must not contain names from exclusion list. Weight: -5."""
    found = [name for name in exclusion_list if name.lower() in translated.lower()]
    if found:
        return VerifierResult(False, -5, f"Excluded name(s) {found} appeared in translation")
    return VerifierResult(True, -5)


def verify_register_match(translated: str, requested_register: str) -> VerifierResult:
    """V5 — Detected register must match requested. Weight: +2."""
    detected = classify_register(translated)
    if detected != requested_register:
        return VerifierResult(False, 2, f"Requested register='{requested_register}', detected='{detected}'")
    return VerifierResult(True, 2)


def verify_translation_not_empty(translated: str) -> VerifierResult:
    """V6 — Translation must be non-empty. Weight: +5."""
    if not translated.strip():
        return VerifierResult(False, 5, "Empty translation output")
    return VerifierResult(True, 5)


def verify_translation_length_reasonable(source: str, translated: str) -> VerifierResult:
    """V7 — Translated length should be within 0.4×–2.5× source length (token-proxy by chars). Weight: +1."""
    if len(source) == 0:
        return VerifierResult(True, 1)
    ratio = len(translated) / len(source)
    if ratio < 0.4 or ratio > 2.5:
        return VerifierResult(False, 1, f"Length ratio {ratio:.2f} outside [0.4, 2.5]")
    return VerifierResult(True, 1)


def verify_no_english_leakage(translated: str) -> VerifierResult:
    """V8 — Spanish translation should not contain large untranslated English clauses. Weight: -3."""
    suspicious_words = [
        " the ", " patient is ", " administer ", " was given ", " presents with ",
        " complains of ", " denies ", " history of ", " allergic to ",
    ]
    found = [w.strip() for w in suspicious_words if w in translated.lower()]
    if len(found) >= 2:
        return VerifierResult(False, -3, f"English phrases detected in Spanish output: {found}")
    return VerifierResult(True, -3)


def verify_negation_preserved(source: str, translated: str) -> VerifierResult:
    """V9 — Clinical negations in source must appear in translation. Weight: +4."""
    source_lower = source.lower()
    translated_lower = translated.lower()
    has_en_negation = any(re.search(pat, source_lower) for pat in NEGATION_EN_MARKERS)
    if not has_en_negation:
        return VerifierResult(True, 4)  # Nothing to check
    has_es_negation = any(re.search(pat, translated_lower) for pat in NEGATION_ES_MARKERS)
    if not has_es_negation:
        return VerifierResult(False, 4, "Source contains clinical negation(s) not preserved in translation")
    return VerifierResult(True, 4)


def verify_allergy_detected(source: str, translated: str) -> VerifierResult:
    """V10 — Allergy mentions in source must be represented in translation. Weight: +5."""
    source_lower = source.lower()
    translated_lower = translated.lower()
    has_en_allergy = any(re.search(pat, source_lower) for pat in ALLERGY_EN_MARKERS)
    if not has_en_allergy:
        return VerifierResult(True, 5)
    has_es_allergy = any(re.search(pat, translated_lower) for pat in ALLERGY_ES_MARKERS)
    if not has_es_allergy:
        return VerifierResult(False, 5, "Source contains allergy reference(s) not preserved in translation")
    return VerifierResult(True, 5)


def verify_medication_frequency_preserved(source: str, translated: str) -> VerifierResult:
    """V11 — Medication frequency terms must be translated correctly. Weight: +4."""
    source_lower = source.lower()
    translated_lower = translated.lower()
    for en_pat, es_pat in MED_FREQ_EN.items():
        if re.search(en_pat, source_lower):
            if not re.search(es_pat, translated_lower):
                return VerifierResult(False, 4, f"Medication frequency '{en_pat}' in source not matched in translation")
    return VerifierResult(True, 4)


def verify_anatomical_terminology(source: str, translated: str) -> VerifierResult:
    """V12 — Anatomical terms must have canonical Spanish equivalent. Weight: +3."""
    source_lower = source.lower()
    translated_lower = translated.lower()
    for en_term, es_terms in ANATOMY_EN.items():
        if en_term in source_lower:
            if not any(es in translated_lower for es in es_terms):
                return VerifierResult(False, 3, f"Anatomical term '{en_term}' not found as any of {es_terms} in translation")
    return VerifierResult(True, 3)


def verify_symptom_severity_preserved(source: str, translated: str) -> VerifierResult:
    """V13 — Symptom severity adjectives must be preserved in translation. Weight: +4."""
    source_lower = source.lower()
    translated_lower = translated.lower()
    has_en_severity = any(re.search(rf"\b{kw}\b", source_lower) for kw in SEVERITY_EN_MAP)
    if not has_en_severity:
        return VerifierResult(True, 4)
    for en_kw, es_variants in SEVERITY_EN_MAP.items():
        if re.search(rf"\b{en_kw}\b", source_lower):
            if not any(re.search(rf"\b{v}\b", translated_lower) for v in es_variants):
                return VerifierResult(False, 4, f"Severity '{en_kw}' in source not matched by any of {es_variants} in translation")
    return VerifierResult(True, 4)


def verify_contraindications_preserved(source: str, translated: str) -> VerifierResult:
    """V14 — Contraindication language must carry over to translation. Weight: +5."""
    source_lower = source.lower()
    translated_lower = translated.lower()
    has_en_contra = any(re.search(pat, source_lower) for pat in CONTRAINDICATION_EN_MARKERS)
    if not has_en_contra:
        return VerifierResult(True, 5)
    has_es_contra = any(re.search(pat, translated_lower) for pat in CONTRAINDICATION_ES_MARKERS)
    if not has_es_contra:
        return VerifierResult(False, 5, "Source contains contraindication language not preserved in translation")
    return VerifierResult(True, 5)


def verify_informed_consent_language(source: str, translated: str) -> VerifierResult:
    """V15 — Informed consent phrasing must have Spanish equivalent present. Weight: +5."""
    source_lower = source.lower()
    translated_lower = translated.lower()
    has_en_consent = any(re.search(pat, source_lower) for pat in INFORMED_CONSENT_EN)
    if not has_en_consent:
        return VerifierResult(True, 5)
    has_es_consent = any(re.search(pat, translated_lower) for pat in INFORMED_CONSENT_ES)
    if not has_es_consent:
        return VerifierResult(False, 5, "Source contains informed-consent language not represented in translation")
    return VerifierResult(True, 5)


# -----------------------------------------------------------------------------
# Pytest functions — each one is a verifier test
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Administer 10 mg of morphine IV.", "Administrar 10 mg de morfina IV."),
        ("Patient receives 0.5 mg lorazepam.", "El paciente recibe 0.5 mg de lorazepam."),
    ],
)
def test_v1_dosage_preserved(source, translated):
    r = verify_dosage_preserved(source, translated)
    assert r.passed, r.reason


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Administer 10 mg of morphine IV.", "Administrar 10 mg de morfina IV."),
    ],
)
def test_v2_units_preserved(source, translated):
    r = verify_unit_preserved(source, translated)
    assert r.passed, r.reason


def test_v3_controlled_substance_morphine():
    r = verify_controlled_substance_translated(
        "Administer morphine 10 mg.",
        "Administrar morfina 10 mg.",
    )
    assert r.passed, r.reason


def test_v3_controlled_substance_missing_translation_fails():
    r = verify_controlled_substance_translated(
        "Administer morphine 10 mg.",
        "Administrar el medicamento 10 mg.",
    )
    assert not r.passed


def test_v4_no_excluded_names():
    r = verify_no_excluded_names(
        "El paciente reporta dolor.",
        exclusion_list=["Rosa", "Marisol", "Tomás"],
    )
    assert r.passed


def test_v4_excluded_name_triggers_failure():
    r = verify_no_excluded_names(
        "El paciente Rosa reporta dolor.",
        exclusion_list=["Rosa"],
    )
    assert not r.passed
    assert r.weight == -5


def test_v5_register_match_formal():
    r = verify_register_match("Administrar 10 mg de morfina vía IV.", "formal_clinical")
    assert r.passed


def test_v6_empty_translation_fails():
    r = verify_translation_not_empty("   ")
    assert not r.passed


def test_v7_length_ratio_ok():
    r = verify_translation_length_reasonable("Hello.", "Hola.")
    assert r.passed


def test_v7_length_ratio_too_short():
    r = verify_translation_length_reasonable(
        "The patient has a long medical history of hypertension and diabetes type 2.",
        "Hipertenso.",
    )
    assert not r.passed


def test_v8_english_leakage_detected():
    r = verify_no_english_leakage("El paciente presents with chest pain and is allergic to penicillin.")
    assert not r.passed


def test_v8_clean_spanish_passes():
    r = verify_no_english_leakage("El paciente presenta dolor torácico y es alérgico a la penicilina.")
    assert r.passed


# -----------------------------------------------------------------------------
# V9 — Negation of conditions
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Patient denies chest pain.", "El paciente niega dolor torácico."),
        ("No history of hypertension.", "Sin antecedentes de hipertensión."),
        ("Patient does not have fever.", "El paciente no presenta fiebre."),
        ("Negative for infection.", "Negativo para infección."),
        ("Absent bowel sounds.", "Ausencia de ruidos intestinales."),
        ("No signs of bleeding.", "No hay signos de sangrado."),
    ],
)
def test_v9_negation_preserved(source, translated):
    r = verify_negation_preserved(source, translated)
    assert r.passed, r.reason


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Patient denies chest pain.", "El paciente tiene dolor torácico."),
        ("No history of hypertension.", "Antecedentes de hipertensión."),
    ],
)
def test_v9_negation_missing_fails(source, translated):
    r = verify_negation_preserved(source, translated)
    assert not r.passed, f"Expected failure but passed: {r.reason}"


def test_v9_no_negation_in_source_passes():
    r = verify_negation_preserved("Patient has mild headache.", "El paciente tiene cefalea leve.")
    assert r.passed


# -----------------------------------------------------------------------------
# V10 — Allergy detection
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Patient is allergic to penicillin.", "El paciente es alérgico a la penicilina."),
        ("Known allergy to sulfa drugs.", "Alergia conocida a las sulfamidas."),
        ("Hypersensitivity to latex.", "Hipersensibilidad al látex."),
        ("Patient has anaphylaxis history.", "El paciente tiene antecedentes de anafilaxia."),
    ],
)
def test_v10_allergy_detected(source, translated):
    r = verify_allergy_detected(source, translated)
    assert r.passed, r.reason


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Patient is allergic to penicillin.", "El paciente recibe penicilina."),
        ("Known allergy to sulfa.", "El paciente tolera bien el medicamento."),
    ],
)
def test_v10_allergy_missing_fails(source, translated):
    r = verify_allergy_detected(source, translated)
    assert not r.passed, f"Expected failure but passed: {r.reason}"


def test_v10_no_allergy_in_source_passes():
    r = verify_allergy_detected("Patient takes aspirin daily.", "El paciente toma aspirina a diario.")
    assert r.passed


# -----------------------------------------------------------------------------
# V11 — Medication frequencies
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Take once daily with food.", "Tomar una vez al día con alimentos."),
        ("Administer twice daily.", "Administrar dos veces al día."),
        ("Take three times daily.", "Tomar tres veces al día."),
        ("Give BID for 7 days.", "Administrar cada 12 horas por 7 días."),
        ("Give TID as needed.", "Administrar cada 8 horas según necesidad."),
        ("Use QID for pain.", "Usar cada 6 horas para el dolor."),
        ("Take every 6 hours.", "Tomar cada 6 horas."),
        ("Use PRN for anxiety.", "Usar según necesidad para la ansiedad."),
    ],
)
def test_v11_medication_frequency_preserved(source, translated):
    r = verify_medication_frequency_preserved(source, translated)
    assert r.passed, r.reason


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Give BID for 7 days.", "Administrar una vez al día por 7 días."),
        ("Take three times daily.", "Tomar una vez al día."),
    ],
)
def test_v11_medication_frequency_missing_fails(source, translated):
    r = verify_medication_frequency_preserved(source, translated)
    assert not r.passed, f"Expected failure but passed: {r.reason}"


def test_v11_no_frequency_in_source_passes():
    r = verify_medication_frequency_preserved("Patient reports headache.", "El paciente reporta cefalea.")
    assert r.passed


# -----------------------------------------------------------------------------
# V12 — Anatomical terminology
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Pain in left arm.", "Dolor en el brazo izquierdo."),
        ("Injury to right leg.", "Lesión en la pierna derecha."),
        ("Patient has chest pain.", "El paciente tiene dolor en el tórax."),
        ("Abdomen is tender.", "El abdomen está sensible."),
        ("Pain radiates to left arm and neck.", "El dolor irradia al brazo izquierdo y al cuello."),
        ("Liver function tests abnormal.", "Pruebas de función hepática del hígado anormales."),
        ("Mass in right lung.", "Masa en el pulmón derecho."),
    ],
)
def test_v12_anatomical_terminology(source, translated):
    r = verify_anatomical_terminology(source, translated)
    assert r.passed, r.reason


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Pain in left arm.", "Dolor en la extremidad."),
        ("Patient has chest pain.", "El paciente tiene dolor."),
        ("Liver enzymes elevated.", "Enzimas elevadas."),  # "liver" not translated
    ],
)
def test_v12_anatomical_term_missing_fails(source, translated):
    r = verify_anatomical_terminology(source, translated)
    assert not r.passed, f"Expected failure but passed: {r.reason}"


def test_v12_no_anatomy_in_source_passes():
    r = verify_anatomical_terminology("Patient feels better today.", "El paciente se siente mejor hoy.")
    assert r.passed


# -----------------------------------------------------------------------------
# V13 — Symptom severity
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Mild headache.", "Cefalea leve."),
        ("Moderate abdominal pain.", "Dolor abdominal moderado."),
        ("Severe chest pain.", "Dolor torácico severo."),
        ("Critical condition.", "Condición crítica."),
        ("Mild to moderate nausea.", "Náuseas leves a moderadas."),
    ],
)
def test_v13_symptom_severity_preserved(source, translated):
    r = verify_symptom_severity_preserved(source, translated)
    assert r.passed, r.reason


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Severe chest pain.", "Dolor torácico leve."),
        ("Moderate headache.", "Cefalea."),
    ],
)
def test_v13_severity_mismatch_fails(source, translated):
    r = verify_symptom_severity_preserved(source, translated)
    assert not r.passed, f"Expected failure but passed: {r.reason}"


def test_v13_no_severity_in_source_passes():
    r = verify_symptom_severity_preserved("Patient reports headache.", "El paciente reporta cefalea.")
    assert r.passed


# -----------------------------------------------------------------------------
# V14 — Contraindications
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Contraindicated in pregnancy.", "Contraindicado en el embarazo."),
        ("Do not use if allergic to aspirin.", "No usar si es alérgico a la aspirina."),
        ("Do not administer to patients with liver disease.", "No administrar a pacientes con enfermedad hepática."),
        ("Not recommended for children under 12.", "No se recomienda para niños menores de 12 años."),
        ("Should not be used with MAOIs.", "No se debe usar con IMAOs."),
        ("Avoid use in renal impairment.", "Evitar el uso en insuficiencia renal."),
    ],
)
def test_v14_contraindications_preserved(source, translated):
    r = verify_contraindications_preserved(source, translated)
    assert r.passed, r.reason


@pytest.mark.parametrize(
    "source,translated",
    [
        ("Contraindicated in pregnancy.", "Puede usarse en el embarazo."),
        ("Do not use if allergic.", "Usar según indicaciones."),
    ],
)
def test_v14_contraindication_missing_fails(source, translated):
    r = verify_contraindications_preserved(source, translated)
    assert not r.passed, f"Expected failure but passed: {r.reason}"


def test_v14_no_contraindication_in_source_passes():
    r = verify_contraindications_preserved("Patient tolerates medication well.", "El paciente tolera bien el medicamento.")
    assert r.passed


# -----------------------------------------------------------------------------
# V15 — Informed consent
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,translated",
    [
        ("I understand the risks and benefits.", "Comprendo los riesgos y beneficios."),
        ("I voluntarily consent to treatment.", "Consiento voluntariamente al tratamiento."),
        ("Before signing, I confirm I have been informed.", "Antes de firmar, confirmo que he sido informado."),
        ("All my questions have been answered.", "Todas mis preguntas han sido respondidas."),
        (
            "This is an informed consent form.",
            "Este es un formulario de consentimiento informado.",
        ),
        (
            "I have been informed of the procedure.",
            "He sido informada del procedimiento.",
        ),
    ],
)
def test_v15_informed_consent_language(source, translated):
    r = verify_informed_consent_language(source, translated)
    assert r.passed, r.reason


@pytest.mark.parametrize(
    "source,translated",
    [
        ("I understand the risks and benefits.", "El paciente firma el formulario."),
        ("I voluntarily consent to treatment.", "Consentimiento para tratamiento."),
        ("All my questions have been answered.", "Sin preguntas."),
    ],
)
def test_v15_informed_consent_missing_fails(source, translated):
    r = verify_informed_consent_language(source, translated)
    assert not r.passed, f"Expected failure but passed: {r.reason}"


def test_v15_no_consent_language_in_source_passes():
    r = verify_informed_consent_language("Patient presents with fever.", "El paciente presenta fiebre.")
    assert r.passed
