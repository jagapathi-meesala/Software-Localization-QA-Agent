---
name: localization-linguistic-qa
description: Interpret structural localization QA findings and separate objective errors from heuristic warnings requiring human review.
license: MIT
metadata:
  version: "1.0.0"
  category: localization
---

# Localization Linguistic QA

- Treat missing keys and placeholder/markup mismatches as structural errors.
- Treat exact source-target matches and whitespace concerns as warnings requiring context.
- Do not claim grammatical, semantic, cultural, or legal correctness from structural checks.
- Escalate pluralization, ICU MessageFormat, terminology, tone, accessibility, date/number formats, and UI fit to an appropriate reviewer.
