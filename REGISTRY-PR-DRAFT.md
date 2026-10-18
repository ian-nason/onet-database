# Add O*NET 31.0 occupations, skills and work context

Adds `onet`: 468,857 rows in 12 data tables, with three convenience views,
89 documented columns, and an 11,284,480-byte DuckDB artifact. This versioned
subset supports occupational skills and work-context research, including
physical demands and disease/infection exposure. It retains native scales,
category grain, uncertainty, precision/relevance flags and update months.
It is one release snapshot with mixed update dates, not an annual panel.

This proposal is prepared locally. New GitHub/Hugging Face destinations and
actual public-host verification are pending; do not open this PR as a
completed publication until those gates pass. No other registry entry changes.
FEC's registry PR #4 is owned by its separate worker and is not modified.

Validation checklist:

- [x] Local DuckDB opens read-only and all source counts match.
- [x] Every typed cell agrees with the pinned source ZIP in an independent CSV/Decimal pass.
- [x] `_metadata` has one row per data table; `_columns` covers all 89 columns.
- [x] Schemas, keys, references, scales, flags, categories and source-code lists pass.
- [x] Full rebuild reproduces typed fingerprints, NULL counts and dictionary bytes.
- [x] 27 regression tests pass.
- [x] Python `datapond.describe('onet')` works with a local registry override.
- [x] Existing Python and R clients query the candidate over localhost HTTP ranges.
- [x] Registry counts exclude views and metadata; update-month range is disclosed.
- [x] Reproducible scripts, SQL examples, attribution and CC BY 4.0 license are present.
- [x] Independent Claude findings resolved and final reviewed source hashes verified.
- [ ] Approved source repository initialized and published source commit verified.
- [ ] Approved Hugging Face artifact commit and remote SHA-256 verified.
- [ ] Python/R/DuckDB public-host queries pass against the immutable release URL.

Registry base: `f584d1c0020ae8600d8ef766a6ee2ab5ee9544f1`.
Source ZIP SHA-256: `55033fc68b4c13ec23e7f74dc6378660f6e854e75d55d6e333ae0a761d3987cd`.
Candidate SHA-256: `b7908bb82e50d4aa0310a6400e2193e2b11946a9d663ff2c8f1171037585c11b`.

No PR merge or CRAN submission is included.
