#!/usr/bin/env python3
"""Verifica la integridad del proyecto ORQUOR."""
import os, sys

PROJECT = "/mnt/c/Users/frefe/OneDrive/Desktop/START UP/orquor"

EXPECTED = {
    "README.md": "raiz",
    "MANIFEST.md": "raiz",
    "01-action-board/ACTION_BOARD.md": "action",
    "02-brand/BRAND_IDENTITY.md": "brand",
    "02-brand/logo-concepts.svg": "brand",
    "03-whitepaper-acto/whitepaper-acto.md": "whitepaper",
    "04-web/index.html": "web",
    "05-pitch-deck/pitch-deck.html": "pitch",
    "06-hermes/orchestrator.py": "hermes",
    "06-hermes/shared_memory.py": "hermes",
    "06-hermes/requirements.txt": "hermes",
    "06-hermes/verifiers/translation_verifiers.py": "hermes",
    "07-legal/hipaa-baa-template.md": "legal",
    "07-legal/nda-template.md": "legal",
    "07-legal/privacy-policy-ley-29733.md": "legal",
    "08-prospects/PROSPECTS_MASTER.md": "prospects",
    "09-content-calendar/CALENDAR.md": "content",
    "10-migration-runbook/RUNBOOK.md": "migration",
}

ok = 0
missing = 0

for path, section in EXPECTED.items():
    full = os.path.join(PROJECT, path)
    if os.path.exists(full):
        size = os.path.getsize(full)
        print(f"  ✅ {path} ({size:,} bytes)")
        ok += 1
    else:
        print(f"  ❌ FALTA: {path} [{section}]")
        missing += 1

# Contar archivos totales
total = 0
for root, dirs, files in os.walk(PROJECT):
    for f in files:
        if not any(skip in root for skip in ['__pycache__', '.git', '.pytest_cache']):
            if not f.startswith('.bridge') and f != '.screen.png':
                total += 1

print(f"\n=== RESULTADO ===")
print(f"Archivos requeridos: {ok}/{ok+missing} presentes")
print(f"Archivos totales: ~{total}")
print(f"Estado: {'✅ OK' if missing == 0 else '❌ FALTAN ARCHIVOS'}")
sys.exit(0 if missing == 0 else 1)
