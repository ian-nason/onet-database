# O*NET 31.0 release checkpoint

**Locally complete; not uploaded, registered or merged.** The proposed new repositories do not exist yet.

Artifact: **468,857 rows / 12 data tables / 3 views / 89 dictionary columns**, **11,284,480 bytes**. SHA-256: `b7908bb82e50d4aa0310a6400e2193e2b11946a9d663ff2c8f1171037585c11b`. Source ZIP SHA-256: `55033fc68b4c13ec23e7f74dc6378660f6e854e75d55d6e333ae0a761d3987cd`.

Every typed cell matches the original CSVs before checkpoint and after read-only reopen. Official counts, keys/labels, schemas, precision/relevance flags, scale/category grain, codelists, percentage sums, missingness, dictionary statistics and metadata pass. Repeated builds reproduce every typed row fingerprint, NULL count and dictionary byte; build timestamps explain changing file hashes. **27 tests pass**, including an injected supervisor failure that proves worker termination and both worker-exit races during shutdown.

The final build took 14.29 seconds and peaked at **230.5 MiB sampled process-group RSS** under 256 MiB DuckDB memory/one thread/128 MiB spill. Outer limits are 768 MiB RSS, 2 GiB all-files-in-isolated-repository cap, 1.5 GiB available-memory floor and 15 minutes. Prior attempts and evidence are retained; total workspace use is approximately 570 MiB. No FEC files or shared registry checkout were modified.

Installed Python/DuckDB 1.5.4 and R CRAN datapond0.1.0 plus the existing patched0.1.1 client on R DuckDB1.5.5 pass localhost HTTP range queries. R caches are fresh per run and installed R package files are hashed. **Actual public-host hashes/range queries/Python/R checks remain a post-upload gate.** No clean dependency installation was performed or claimed.

## Reviews

`CODEX-REVIEW.md` records Codex's implementation/validation/code/documentation/example review and the supervisor finding it repaired. It is not presented as a separate independent Codex agent. The independent Claude audit used the existing authenticated Max account, safe mode, tools/MCP disabled and paid usage credits off. Persistent session: **`3320c216-da6d-407e-8235-8c264acb3426`**.

The initial and completed follow-up reviews are preserved. All eight initial and six later findings were addressed. Review 04 found no data/validation blocker and raised three closure items: the exact provenance file, durable README examples and guard shutdown races. These are resolved in `CLOSURE-FIXES.md`. Review 05 closed them and requested historical framing for provenance statuses; `PROVENANCE-FIX.md` records that correction, closed by final `claude-evidence/06-provenance-review.txt`. Its exact submitted scope is recorded in adjacent metadata; full prompts/raw outputs remain in the local `claude-evidence/` folder and are excluded from the proposed public source. Closure prompt SHA-256: **`1301dbdac7e14c5d26f898d34f9452a0d02b2a34f344bf772cb93a6b5970f8ae`**. Submitted `2026-10-18T13:56:08.276854+00:00`; completed `2026-10-18T13:56:28.850181+00:00`. Ian's explicit 13:38:41 UTC approval authorized the final submissions. No credentials, unrelated files or HTE data were sent. Claude reviewed supplied source/evidence; it did not execute the tests or independently recompute hashes. `evidence/release-review-binding.json` proves the combined review-04/05/06 current files still match. The artifact build retains its original supervisor receipt; the later race-only guard change was tested without changing the data artifact.

The earlier workspace-trust action was rejected by automatic approval review; no trust was granted. A safer tools-disabled review used a previously trusted workspace. An interrupted follow-up containing stale localhost evidence is retained as failed, not approval. No Claude request was initiated during the parent's hold; the final review started after explicit authorization.

## Remaining action

The exact destination request is in `PUBLICATION-APPROVAL.md` in the delivered bundle: create public GitHub **ian-nason/onet-database**, create public Hugging Face dataset **Nason/onet-database**, publish the specified source/four-file artifact payload, perform immutable public-host verification, then open the separate **datapond-db/registry** PR from **add/onet-31.0**. No merge or CRAN submission. Source and registry changes are already committed on isolated branches; FEC PR4 remains separately owned.

Next: QCEW 2025 annual, ATUS 2025, then FARS 2024. None has been ingested in this task yet. The first addition is ready for the bundled new-destination authorization; the original multi-dataset objective remains open.
