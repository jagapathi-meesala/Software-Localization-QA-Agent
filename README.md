# Software Localization QA Agent

A local-first, deterministic QA utility for JSON and CSV software localization resources.

## Features
- Compare source and target locale keys.
- Detect missing and extra keys.
- Detect duplicate keys in CSV.
- Compare common placeholder tokens (`{name}`, `{{name}}`, `%s`, `%1$s`, `%(name)s`, `${name}`, `:name`).
- Compare HTML-like tag counts.
- Flag empty translations, suspicious exact matches, whitespace differences, replacement characters, and selected control characters.
- Export a JSON report with severity, stable rule IDs, and evidence.
- No network calls, credentials, automatic translation, or file mutation.

## Supported formats
JSON is a flat object mapping message keys to string values. CSV requires `key`, `locale`, and `value` columns.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m core.cli validate examples/en.json
python -m core.cli compare examples/en.json examples/fr.json --source-locale en --target-locale fr --output qa-report.json
python -m core.cli compare examples/locales.csv --source-locale en --target-locale fr --output qa-report.csv.json
python -m unittest discover -s tests -v
python verification/readiness_audit.py
```

Exit codes: `0` no error-level findings; `1` error-level findings; `2` input/usage error.

Structural checks do not prove translation accuracy or cultural appropriateness. Heuristic exact-match warnings may be expected for brand names or approved terminology. Human review is required for linguistic quality and framework-specific plural/message syntax.

OpenGAP target: spec version `0.1.0`. Run `opengap validate` from the repository root. HiDevs validation is separate and must be run after pushing to a public GitHub repository.
