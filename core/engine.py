"""Deterministic localization QA checks."""
import csv, json, re
from pathlib import Path
from collections import Counter

PLACEHOLDER_PATTERNS = [
    re.compile(r"\$\{[^}]+\}"),             # ${name}, before generic braces
    re.compile(r"\{\{[^{}]+\}\}"),
    re.compile(r"\{[A-Za-z_][\w.-]*\}"),
    re.compile(r"%\([^)]+\)[#0 +\-]?(?:\d+)?(?:\.\d+)?[diouxXeEfFgGcrsa]"),
    re.compile(r"%(?:\d+\$)?[-+#0 ]*(?:\d+|\*)?(?:\.\d+|\.\*)?[diouxXeEfFgGcrsa]"),
    re.compile(r"(?<!\w):[A-Za-z_][\w]*"),
]
TAG_RE = re.compile(r"</?[A-Za-z][^>]*?>")
class DuplicateKeyError(ValueError): pass

def extract_placeholders(text):
    found, masked = [], text
    for pattern in PLACEHOLDER_PATTERNS:
        matches = list(pattern.finditer(masked))
        found.extend(m.group(0) for m in matches)
        chars = list(masked)
        for m in matches:
            for i in range(m.start(), m.end()): chars[i] = " "
        masked = "".join(chars)
    return Counter(found)

def load_json(path):
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k,v in data.items()):
        raise ValueError(f"{p}: JSON root must map string keys to string values")
    return data

def load_csv(path):
    p, locales = Path(path), {}
    with p.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not {"key","locale","value"}.issubset(reader.fieldnames):
            raise ValueError(f"{p}: CSV requires columns key, locale, value")
        for n,row in enumerate(reader, start=2):
            key, locale, value = row.get("key"), row.get("locale"), row.get("value")
            if not key or not locale or value is None: raise ValueError(f"{p}: row {n} has empty key/locale or missing value")
            lm = locales.setdefault(locale, {})
            if key in lm: raise DuplicateKeyError(f"{p}: duplicate key {key!r} for locale {locale!r} at row {n}")
            lm[key] = value
    return locales

def finding(rule_id, severity, message, key=None, locale=None, evidence=None):
    d = {"rule_id":rule_id, "severity":severity, "message":message}
    if key is not None: d["key"] = key
    if locale is not None: d["locale"] = locale
    if evidence: d["evidence"] = evidence
    return d

def validate_dictionary(data, locale="unknown", source=None):
    out = []
    for key in sorted(data):
        value = data[key]
        if not value.strip(): out.append(finding("LOC-EMPTY-001","warning","Translation is empty or whitespace-only.",key,locale))
        if "\ufffd" in value: out.append(finding("LOC-UNICODE-001","warning","Unicode replacement character found; verify encoding.",key,locale))
        if any((ord(c)<32 and c not in "\t\n\r") or 0x7f<=ord(c)<=0x9f for c in value):
            out.append(finding("LOC-UNICODE-002","warning","Unexpected control character found.",key,locale))
        if value != value.strip(): out.append(finding("LOC-WHITESPACE-001","warning","Leading or trailing whitespace found.",key,locale))
        if source is not None and key in source:
            src = source[key]
            a,b = extract_placeholders(src), extract_placeholders(value)
            if a != b: out.append(finding("LOC-PLACEHOLDER-001","error","Placeholder tokens differ from source.",key,locale,{"source":dict(a),"target":dict(b)}))
            a,b = Counter(TAG_RE.findall(src)),Counter(TAG_RE.findall(value))
            if a != b: out.append(finding("LOC-MARKUP-001","error","HTML-like tags differ from source.",key,locale,{"source":dict(a),"target":dict(b)}))
            if src and value and src.strip()==value.strip() and len(src.strip())>=4 and src.strip().isalnum():
                out.append(finding("LOC-EXACT-MATCH-001","warning","Target is identical to source; verify whether intentional.",key,locale))
            if src[:1].isspace()!=value[:1].isspace() or src[-1:].isspace()!=value[-1:].isspace():
                out.append(finding("LOC-WHITESPACE-002","warning","Leading/trailing whitespace pattern differs from source.",key,locale))
    if source is not None:
        for key in sorted(set(source)-set(data)): out.append(finding("LOC-KEY-001","error","Source key is missing from target locale.",key,locale))
        for key in sorted(set(data)-set(source)): out.append(finding("LOC-KEY-002","error","Target contains a key absent from source locale.",key,locale))
    return out

def build_report(findings, files, checks):
    counts=Counter(x["severity"] for x in findings)
    return {"agent":"software-localization-qa-agent","status":"review_required" if findings else "passed",
      "files_inspected":files,"checks_executed":checks,
      "summary":{"total_findings":len(findings),"errors":counts["error"],"warnings":counts["warning"],"info":counts["info"]},
      "findings":findings,"limitations":["Structural checks do not prove translation accuracy or cultural appropriateness.",
      "Placeholder recognition covers common patterns and may not cover custom frameworks.",
      "Pluralization, ICU MessageFormat semantics, UI fit, and terminology require dedicated checks or human review."]}

def compare_json(source_path,target_path,source_locale="source",target_locale="target"):
    source,target=load_json(source_path),load_json(target_path)
    return build_report(validate_dictionary(target,target_locale,source),[source_path,target_path],
      ["json_shape","key_parity","placeholder_parity","html_tag_parity","whitespace","empty_values","unicode_controls","exact_match_heuristic"])

def compare_csv(path,source_locale,target_locale):
    locales=load_csv(path)
    if source_locale not in locales: raise ValueError(f"Source locale {source_locale!r} not found; found: {', '.join(sorted(locales))}")
    if target_locale not in locales: raise ValueError(f"Target locale {target_locale!r} not found; found: {', '.join(sorted(locales))}")
    return build_report(validate_dictionary(locales[target_locale],target_locale,locales[source_locale]),[path],
      ["csv_shape","duplicate_key_check","key_parity","placeholder_parity","html_tag_parity","whitespace","empty_values","unicode_controls","exact_match_heuristic"])

def validate_json_file(path,locale="unknown"):
    data=load_json(path)
    return build_report(validate_dictionary(data,locale),[path],["json_shape","empty_values","whitespace","unicode_controls"])
