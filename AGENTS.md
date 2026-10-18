# Agent Instructions

1. Identify file format, source locale, target locale(s), and requested checks.
2. Validate data shape before comparing strings.
3. Report deterministic checks with key-level evidence and severity.
4. Treat heuristics as warnings, not proof of mistranslation.
5. Do not send strings to external services or call external APIs.
6. Do not overwrite user files during QA; write reports only to an explicitly requested output path.
7. State limitations and recommend native-speaker review for linguistic, cultural, legal, and product-context questions.
