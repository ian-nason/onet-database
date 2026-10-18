# Review 05 provenance closure

The exact provenance payload is now explicitly an immutable pre-publication evidence snapshot, with its recording time. The existing build, source-lock, runtime and review sections, including their local-validation and upload status fields, are nested under `evidence_snapshot` unchanged. The top-level explanation makes every nested status historical, so future upload cannot falsify the record. Future public-host verification belongs in a separate release receipt rather than rewriting this audited snapshot.

Codex verified every nested field is identical to the previously reviewed file and no artifact, code, test result, README, card or consumer evidence changed. The optional redaction of local interpreter paths/session UUID was not taken: these non-credential identifiers retain exact environment/review reproducibility. No credentials or unrelated user data are present. The exact public file remains subject to the publication manifest's SHA-256.
