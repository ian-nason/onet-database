# Closure of review 04 findings

The artifact remains b7908bb82e50d4aa0310a6400e2193e2b11946a9d663ff2c8f1171037585c11b. No ingestion, schema, source lock, dependency or artifact bytes changed after review 04.

1. The exact `sources-31.0.json` intended for Hugging Face is now materialized and supplied for review, together with the card that links it. It includes build/source/runtime identities and accurately scopes review 04; later closure receipts live in the source repository. Final packaging must COPY this file unchanged, not generate new unreviewed claims or insert a future source-commit hash. The publication manifest separately records the final source commit.
2. The source README is now durable: its Python example explicitly opens a locally built artifact and does not promise a future URL replacement. Public-host checks and the exact public payload remain separately gated, without asserting publication has happened.
3. `stop()` catches ProcessLookupError at both TERM and KILL, then reaps the worker. Two targeted regression fixtures reproduce each race. The artifact was built with the previous supervisor hash recorded in release-final-build/resources.json; the new supervisor changed shutdown handling only, not artifact production. The 27-test run uses the final supervisor and records its new hash. No needless rebuild or consumer rerun was made because ingestion and artifact bytes did not change.

Codex inspected these fixes, reran all 27 tests, and checked the original build inputs and artifact/evidence hashes. The review checks supplied files; it is not an independent execution by Claude. Destination authorization and real public-host verification remain open.
