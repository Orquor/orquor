# ORQUOR — Makefile
# Comandos principales del proyecto

.PHONY: help verify test pdf deploy backup clean

help:
	@echo "ORQUOR — Comandos disponibles:"
	@echo "  make verify   — Verificar integridad del proyecto"
	@echo "  make test     — Ejecutar verifiers (pytest)"
	@echo "  make pdf      — Generar PDF del whitepaper"
	@echo "  make deploy   — Deploy a Hostinger (requiere .env)"
	@echo "  make backup   — Backup del proyecto"
	@echo "  make clean    — Limpiar cachés"

verify:
	python3 verify_integrity.py

test:
	cd 06-hermes && .venv/bin/python -m pytest verifiers/ -v

pdf:
	pandoc 03-whitepaper-acto/whitepaper-acto.md \
		-o 03-whitepaper-acto/whitepaper-acto.pdf \
		--pdf-engine=xelatex \
		-V mainfont="DejaVu Serif" \
		-V geometry:margin=1in

deploy:
	bash deploy-hostinger.sh

backup:
	bash backup.sh

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
