# Verified public release

Published October 18, 2026. [Dataset](https://huggingface.co/datasets/Nason/onet-database) and [immutable dataset commit](https://huggingface.co/datasets/Nason/onet-database/commit/d0e84bacef02d4477423edbf7468cc3ec8fb79c2). The corresponding registry submission is a draft PR; global datapond discovery is not claimed until that PR is merged.

Artifact: `onet.duckdb`, 11,284,480 bytes, SHA-256 `b7908bb82e50d4aa0310a6400e2193e2b11946a9d663ff2c8f1171037585c11b`. All four uploaded files were streamed anonymously from the immutable public commit and matched their frozen sizes/checksums. A 4096-byte range request returned HTTP 206 with the exact Content-Range and original bytes. See publication/public-byte-verification.json.

```sql
LOAD httpfs;
ATTACH 'https://huggingface.co/datasets/Nason/onet-database/resolve/d0e84bacef02d4477423edbf7468cc3ec8fb79c2/onet.duckdb' AS onet (READ_ONLY);
SELECT table_name,row_count,column_count FROM onet._metadata ORDER BY table_name;
```

Installed datapond Python (0.1.1, DuckDB 1.5.4) and R datapond 0.1.0/0.1.1 (DuckDB 1.5.5) passed actual public-HTTPS metadata, row-count and meaningful semantic queries. Python also executed all 5 audited example queries. Before registry merge, tests use a local registry override whose attach_url is the immutable public URL above. Existing httpfs was loaded; no software was installed. Test constructors were bounded to 128 MiB, one thread and no spill, under the 768 MiB group guard. Exact installed package identities and outputs are retained in publication/.

The audited local source snapshot is `f3d8cfd8c1d665975251aa52497b591af6701e4b`; the public source export starts at `cc168a8c4c4e94aa8127b44508e2e87d83d45a98`. PUBLICATION-EXPORT.json maps byte-identical audited source files and any private exclusions. A fresh public history prevents accidental publication of private historical material. This commit adds hosting evidence and a publication-status notice to README; it changes no ingestion code, audited database, dictionaries or source data. Original audit/source manifests and historical pre-publication status text remain intact as evidence.

Independent Claude reviews covered supplied code/documentation/evidence, not independent execution or hash recomputation. Public-host checks were subsequently executed by Codex. All audit findings were resolved before upload. No registry PR merge or CRAN submission is included.
