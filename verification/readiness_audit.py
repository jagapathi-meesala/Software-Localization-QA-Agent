from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
required=["agent.yaml","SOUL.md","README.md","AGENTS.md","RULES.md","DUTIES.md","EXPLAINABILITY.md","requirements.txt","config/default.yaml","contracts/localization-file.schema.json","core/engine.py","core/cli.py","tools/validate-localization-files.yaml","tools/compare-locales.yaml","tools/generate-qa-report.yaml","skills/localization-file-validation/SKILL.md","skills/localization-linguistic-qa/SKILL.md","skills/localization-reporting/SKILL.md","tests/test_engine.py","examples/en.json","examples/fr.json"]
missing=[p for p in required if not (ROOT/p).is_file()]
manifest=(ROOT/"agent.yaml").read_text(encoding="utf-8")
explain=(ROOT/"EXPLAINABILITY.md").read_text(encoding="utf-8")
name_ok=bool(re.search(r"(?m)^name:\s*software-localization-qa-agent\s*$",manifest))
headings_ok=all(h in explain for h in ["## Inputs and Data Sources","## Decision and Reasoning","## Limits and Constraints"])
print(f"Required files: {len(required)-len(missing)}/{len(required)}")
if missing: print("Missing:",", ".join(missing))
print("Agent name valid:","PASS" if name_ok else "FAIL")
print("Explainability sections:","PASS" if headings_ok else "FAIL")
if missing or not name_ok or not headings_ok: sys.exit(1)
