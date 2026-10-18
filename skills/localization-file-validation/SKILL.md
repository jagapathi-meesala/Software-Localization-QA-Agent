---
name: localization-file-validation
description: Validate local JSON and CSV localization files for shape, keys, duplicate entries, and encoding-related issues.
license: MIT
metadata:
  version: "1.0.0"
  category: quality-assurance
---

# Localization File Validation

1. Identify flat JSON dictionaries or CSV locale tables.
2. For JSON, require an object mapping string keys to string values.
3. For CSV, require `key`, `locale`, and `value` columns and detect duplicate key/locale pairs.
4. Report malformed inputs as input errors; do not silently repair them.
5. Preserve original files and report only evidence supported by the data.
