#!/usr/bin/env python3
"""Health check del sistema ORQUOR."""
import os, sys, subprocess

PROJECT = "/mnt/c/Users/frefe/OneDrive/Desktop/START UP/orquor"

checks = []

# 1. Proyecto existe
checks.append(("Proyecto existe", os.path.exists(PROJECT)))

# 2. Archivos core
core_files = ["README.md", "MANIFEST.md", "Makefile"]
all_core = all(os.path.exists(os.path.join(PROJECT, f)) for f in core_files)
checks.append(("Archivos core", all_core))

# 3. Verifiers pasan
result = subprocess.run(
    ["python3", "-m", "pytest", "verifiers/translation_verifiers.py", "-q"],
    cwd=os.path.join(PROJECT, "06-hermes"),
    capture_output=True, text=True, timeout=30
)
checks.append(("Verifiers (13 tests)", "13 passed" in result.stdout))

# 4. Pandoc disponible
checks.append(("Pandoc", subprocess.run(["which", "pandoc"], capture_output=True).returncode == 0))

# 5. Git repo
checks.append(("Git repo", os.path.exists(os.path.join(PROJECT, ".git"))))

# 6. Espacio en disco
stat = os.statvfs(PROJECT)
free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
checks.append((f"Espacio disco ({free_gb:.1f} GB libre)", free_gb > 1))

# Resultado
print("=== ORQUOR Health Check ===")
all_ok = True
for name, ok in checks:
    icon = "✅" if ok else "❌"
    print(f"  {icon} {name}")
    if not ok:
        all_ok = False

print(f"\nEstado: {'✅ TODO OK' if all_ok else '❌ HAY PROBLEMAS'}")
sys.exit(0 if all_ok else 1)
