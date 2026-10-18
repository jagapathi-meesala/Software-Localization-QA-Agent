# Explainability and Decision Record

## Purpose
Detect structural and selected heuristic issues in software localization files, with evidence tied to locale and message key.

## Inputs and Data Sources
Inputs are local JSON objects mapping message keys to strings, or CSV files with `key`, `locale`, and `value` columns. No external source is queried.

## Decision and Reasoning
Checks include file shape, empty values, duplicate CSV keys, key parity, common placeholder-token parity, HTML-like tag parity, whitespace differences, suspicious exact matches, and selected Unicode control characters. Findings include a rule ID, severity, message, and key/locale evidence where available.

## Severity and Prioritization
- `error`: malformed input, duplicate keys, missing/extra keys, or placeholder/markup mismatches.
- `warning`: empty translations, suspicious exact source-target matches, whitespace differences, or unusual Unicode characters.
- `info`: checks completed and counts.
- Heuristic warnings are signals for review, not proof that a translation is wrong.

## Outputs and Evidence
The JSON report includes status, files inspected, checks executed, severity counts, findings, and limitations. Findings include stable rule IDs and key/locale fields when available.

## Human Review
A qualified reviewer must assess meaning, grammar, tone, cultural appropriateness, terminology, pluralization, date/number formatting, text expansion, UI fit, accessibility, and legal/product context.

## Limits and Constraints
The agent does not translate text, access external services, infer intended meaning, validate every framework-specific message format, or guarantee linguistic correctness. Placeholder syntax is recognized through common patterns and may need configuration for custom frameworks.

## Determinism and Reproducibility
Given identical input files and options, structural checks produce the same findings. Checks do not depend on network access or probabilistic inference.

## Safety and Data Handling
Files are processed locally. Reports avoid reproducing full values by default. Users should not include secrets in localization resources.

## Non-Goals
This agent is not a translation engine, a substitute for native-speaker review, or a release approval system.
