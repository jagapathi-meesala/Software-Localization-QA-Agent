# Explainability and Decision Record

## Purpose

The Software Localization QA Agent checks software localization files for structural errors and selected localization quality risks. It reports findings with evidence so a human reviewer can investigate them.

## Decision

The agent decides which findings to report by applying deterministic validation rules to the supplied localization files. It compares message keys, placeholder tokens, HTML-like tags, whitespace, empty values, duplicate CSV keys, suspicious exact matches, and selected Unicode characters. Each finding includes a rule identifier, severity, and relevant key or locale evidence when available. Heuristic warnings indicate items for review and do not prove that a translation is incorrect.

## Inputs

The agent accepts local JSON objects mapping message keys to strings, or CSV files containing key, locale, and value columns. The input files supplied by the user are the data sources for its checks. The agent does not query external services or download translation data. Identical inputs and options produce the same structural-check findings.

## Limits

The agent cannot determine whether a translation preserves the intended meaning, grammar, tone, cultural appropriateness, or legal context. It does not translate text, guarantee linguistic correctness, or validate every framework-specific localization format. Placeholder detection covers common patterns, so custom placeholder syntax may require additional configuration. A qualified human reviewer must assess linguistic quality, pluralization, formatting, accessibility, and user-interface fit before release.

## Outputs and Evidence

The agent generates a JSON report containing the status, inspected files, checks executed, severity counts, findings, and limitations. Findings include stable rule identifiers and key or locale evidence where available. The report supports review but is not a release approval.

## Severity and Prioritization

Errors include malformed input, duplicate keys, missing or extra keys, and placeholder or markup mismatches. Warnings include empty translations, suspicious exact matches, whitespace differences, and unusual Unicode characters. Informational findings describe completed checks and counts. Heuristic warnings require human review rather than automatic rejection.

## Human Review

A qualified reviewer should assess meaning, grammar, tone, cultural appropriateness, terminology, pluralization, date and number formatting, text expansion, interface fit, accessibility, and legal or product context. Structural validation alone cannot establish that a translation is correct.

## Safety and Data Handling

The agent processes supplied files locally and does not access external services. Reports avoid reproducing full values by default. Users should not include secrets in localization resources.

## Non-Goals

The agent is not a translation engine or a substitute for native-speaker review. It does not automatically rewrite translations or approve software releases.
