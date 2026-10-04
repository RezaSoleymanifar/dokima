# Dokima

An agent runtime that uses GitHub Actions as its orchestrator. Python 3.12.

- Run the tests with `pytest -q`. Tests live in `tests/`.
- Never change `.github/workflows/`, `dokima/card.py` or `dokima/roles/` unless the issue explicitly asks.
- Keep changes small. Add no dependencies unless the issue asks.
- Dokima's design lives in `DESIGN.md`; read it before changing how Dokima works.
