# Codex implementation and verification review

Release artifact: `b7908bb82e50d4aa0310a6400e2193e2b11946a9d663ff2c8f1171037585c11b` (11,284,480 bytes). This is the primary Codex agent's implementation and verification review, not a claim that a separate Codex agent independently reran it.

**Data validation:** all 468,857 rows and typed cells were compared with strict Python CSV/Decimal reads of the pinned official ZIP, including after close/read-only reopen. Counts match versioned official dictionaries. Required fields, keys, occupation/element/scale labels, native ranges, flags, category completeness, code lists and category sums pass. Schema, metadata and every dictionary field agree. Source content is unchanged across independently executed builds.

**Ingestion code:** explicit schema and decimal types, strict parser, immutable source hashes, safe allowlisted extraction, existing-output refusal and failed-input preservation were inspected and exercised. ZIP/member/precision/duplicate/grain/orphan/null regressions pass. Source dates retain month precision. No hidden rescaling, suppression or imputation was found.

**Resources:** one worker; 256 MiB DuckDB memory, one thread, 128 MiB spill. The portable guard records its own hash and complete argv, 768 MiB RSS stop, 2 GiB isolated-workspace cap, 1.5 GiB available-memory floor and a 15-minute deadline. I found and repaired telemetry-exception orphaning. Its failure fixture now proves process termination. Final observed peak was 230.5 MiB RSS, with 14.29 seconds elapsed.

**Documentation/examples:** license and attribution checked against the official O*NET 31.0 license page. All 89 columns and original names are documented. Tables, limitations, occupations covered, update-month spans, scale/category grain and safe joins agree with observed data. All five useful example queries ran. The HF card uses the same validated facts, qualified SQL and explicit licensing; its proposed destination is not claimed live.

**Consumers:** existing installed Python with DuckDB 1.5.4 and R CRAN0.1.0/patched0.1.1 with DuckDB1.5.5 pass localhost HTTP range queries. Each R run has a fresh cache; all installed R package files are hashed. No software was installed. Actual public Hugging Face verification remains mandatory after authorized upload.

**Result:** 27 tests pass. No remaining local data, ingestion, documentation or example finding is identified by this Codex review. Limitations: no new dependency installation was tested; source-agency methodological accuracy and real public hosting are not established by local tests. Claude review 04 found no data/validation blocker. Its card-provenance and minor guard/README findings are closed in CLOSURE-FIXES.md; the exact closure payload is submitted for follow-up review.
