# Contributing to Orquor

Thank you for your interest. This document describes how to contribute to the open components of the Orquor project.

## Scope of contributions

We welcome contributions to:

- **`06-hermes/`** — The Hermes multi-agent orchestration platform. Sub-agents, verifiers, shared memory framework, orchestrator.
- **`03-whitepaper-acto/`** — Corrections, clarifications, additional references, or benchmark proposals for the ACTO specification.
- **`02-brand/`** — Logo concept refinements (design contributions require portfolio or prior work).
- **`04-web/`** — Accessibility fixes, performance improvements, and corrections to the marketing site and Academy landing page.

The following directories are internal operational artifacts and are not open for external contributions:

- `01-action-board/`, `05-pitch-deck/`, `07-legal/`, `08-prospects/`, `09-content-calendar/`, `10-migration-runbook/`

## Before you start

1. **Read the ACTO whitepaper** ([`03-whitepaper-acto/whitepaper-acto.md`](03-whitepaper-acto/whitepaper-acto.md)). Understanding the category definition is required before contributing verifiers or architectural changes.
2. **Check existing issues and discussions.** We track work publicly on GitHub Issues. If you are proposing something large, open an issue first.
3. **Read the brand guidelines** ([`02-brand/BRAND_IDENTITY.md`](02-brand/BRAND_IDENTITY.md)). Any copy or design contribution must align with Orquor's voice and visual identity.

## Development setup

```bash
git clone https://github.com/orquor/orquor.git
cd orquor

# Hermes platform
cd 06-hermes
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest verifiers/ -v
```

## Verifier contributions

The verifier suite is the core of the open platform. To contribute a new verifier:

1. **One outcome per verifier.** Each verifier checks exactly one property. Do not bundle multiple checks.
2. **Weight the verifier.** Assign a severity weight (1–5) and justify it in the docstring.
3. **Include passing and failing test cases.** Minimum one of each.
4. **Do not use external APIs.** Verifiers must be deterministic and self-contained.
5. **Follow the `VerifierResult` contract.** See existing verifiers in `06-hermes/verifiers/translation_verifiers.py` for the pattern.

Example structure:

```python
def verify_example_property(source: str, translated: str) -> VerifierResult:
    """V-N — Short description of what this checks.
    Weight: +3 (justification for the weight)."""
    # Deterministic check logic
    if condition_failed:
        return VerifierResult(False, 3, "Description of the failure")
    return VerifierResult(True, 3)
```

## Pull request process

1. Fork the repository.
2. Create a branch named `feature/description` or `fix/description`.
3. Make changes. Keep commits atomic — one logical change per commit.
4. Run `pytest verifiers/ -v` and confirm all 13+ tests pass. **Broken tests block merge.**
5. Open a pull request against `main`. Include:
   - What the change does
   - Why it belongs in the public subset
   - Evidence that existing tests pass
6. A maintainer will review within one week. We may request changes or ask clarifying questions.

## Code style

- **Python:** Follow the existing style in `06-hermes/`. Type hints where practical. Docstrings for public functions.
- **Markdown:** One sentence per line (semantic line breaks). No trailing whitespace.
- **HTML/CSS:** Follow the design tokens defined in `04-web/index.html`. No new colors. No gradients. No box shadows.

## Communication

- **Technical discussions:** GitHub Issues
- **Security disclosures:** `security@orquor.com` — do not open a public issue for vulnerabilities
- **General inquiries:** `hello@orquor.com`

## License

By contributing code to this repository, you agree that your contribution will be licensed under the MIT License ([`LICENSE`](LICENSE)). Whitepaper contributions are licensed under CC BY 4.0.
