# Exact proposed O*NET publication

> Historical October 18, 2026 checkpoint: the text below is retained as the record of that stage, including its then-pending gates and earlier candidate hashes. It is not current availability or a new approval. Publication and catalog integration are now complete; see the [current README](README.md), [publication receipt](PUBLICATION.md) and [consumer guidance](docs/CONSUMERS.md).

These are proposed destinations on the verified existing accounts. No account,
credential, token scope or persistent access setting needs to change.

1. Create the public GitHub source repository `ian-nason/onet-database`, then push
   the reviewed source commit as its initial `main` branch. The working branch
   on HojosDojo remains `add/onet-31.0`. Publish only the files listed in
   `SOURCE-PAYLOAD.json`; no archives, database files, credentials, unrelated
   worktrees or FEC files are included in this source push.
2. Create the public Hugging Face dataset repository `Nason/onet-database`.
   Publish `onet.duckdb`, `README.md`, `DICTIONARY.md` and `sources-31.0.json` in
   one commit, using one upload worker. The database is 11,284,480 bytes with
   SHA-256 `b7908bb82e50d4aa0310a6400e2193e2b11946a9d663ff2c8f1171037585c11b`.
3. Verify the immutable Hugging Face commit's artifact size and SHA-256, then
   execute bounded Python/R/DuckDB queries against its actual public URL.
   Localhost success alone is not sufficient. Record that receipt before
   advertising public availability or opening a completed registry submission.
4. Push the O*NET-only `add/onet-31.0` registry branch to the already established
   `datapond-db/registry` destination and open a separate PR using the completed
   checklist. The patch currently adds one 20-line entry and preserves every
   existing byte outside that insertion. FEC PR #4 and its shared checkout
   remain under the FEC worker's ownership.

No PR merge, CRAN submission, unrelated dataset change, new account, permission
expansion, tracking or paid service is included. If approval review requires
exact new-repository authorization, use this single bundle for the request.

After this checkpoint, continue sequentially with QCEW 2025 annual, ATUS 2025,
then FARS 2024. Those datasets have not been ingested by this task yet.
