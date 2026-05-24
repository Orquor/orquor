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
