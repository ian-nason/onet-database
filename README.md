# O*NET 31.0 Occupations, Skills and Work Context

A version-pinned, queryable DuckDB subset of the [O*NET 31.0 Database](https://www.onetcenter.org/database.html): **468,857 rows across 12 tables (89 columns)**, three convenience views, datapond metadata and a column dictionary.

Use it for descriptive questions about what occupations require and what their work is like: skill importance and level, how often workers stand, bend or are exposed to disease, and the alternate titles an occupation goes by. It does not contain wages, employment counts, health outcomes or any person-level records.

Download/query the [Hugging Face dataset](https://huggingface.co/datasets/Nason/onet-database). Published to Hugging Face on 2026-10-18. The dataset is included in the public datapond catalog as `onet`. Use normal package discovery and connections, or the immutable direct URL below.

[Quick start](#quick-start) · [Tables](#tables) · [Views](#pre-built-views) · [Examples](#example-queries) · [Caveats](#researcher-caveats) · [Source](#data-source-and-version) · [License](#license-and-attribution) · [Build](#build-from-source) · [Changelog](#changelog)

## Quick Start

Choose one route: the [datapond package](#datapond-package) finds the database by catalog ID; the direct [Python](#python-duckdb), [R](#r-with-dbi-and-duckdb) and SQL examples use a fixed artifact URL. These are alternatives, not steps that must all be run. The SQL block requires a DuckDB SQL client.

### DuckDB CLI

```sql
SET memory_limit = '128MiB';
SET threads = 1;
SET max_temp_directory_size = '0B';
INSTALL httpfs;
LOAD httpfs;
ATTACH 'https://huggingface.co/datasets/Nason/onet-database/resolve/d0e84bacef02d4477423edbf7468cc3ec8fb79c2/onet.duckdb' AS onet (READ_ONLY);

-- Occupations with the highest mean reported exposure to disease or infection
SELECT onet_soc_code, title, data_value AS mean_exposure, lower_ci_bound, upper_ci_bound, n, update_date
FROM onet.v_work_context_means
WHERE element_id = '4.C.2.c.1.b' AND scale_id = 'CX' AND recommend_suppress = 'N'
ORDER BY data_value DESC, onet_soc_code
LIMIT 15;
```

The database file is 10.8 MiB. DuckDB fetches byte ranges as needed; transfer volume depends on the query. File size is disk storage, not a RAM estimate. Remote queries still run on your machine and can transfer much of the file. A filter or `LIMIT` after a join or aggregate does not guarantee a small scan. The 128 MiB setting limits DuckDB's buffer pool, not the whole Python/R process; with spill disabled, a larger query can fail at that limit. Download only if you have room for the file, temporary download bytes and any existing copy.

The examples use this immutable artifact URL:

```
https://huggingface.co/datasets/Nason/onet-database/resolve/d0e84bacef02d4477423edbf7468cc3ec8fb79c2/onet.duckdb
```

### Python (duckdb)

Install the Python dependency once in the environment that runs your query: `python -m pip install duckdb`.

```python
import duckdb
con = duckdb.connect(config={"memory_limit": "128MiB", "threads": "1", "max_temp_directory_size": "0B"})
con.sql("INSTALL httpfs; LOAD httpfs;")
con.sql("ATTACH 'https://huggingface.co/datasets/Nason/onet-database/resolve/d0e84bacef02d4477423edbf7468cc3ec8fb79c2/onet.duckdb' AS onet (READ_ONLY)")
con.sql("SELECT * FROM onet._metadata").show()
con.sql("""
    SELECT skill_domain, element_name, data_value AS importance, lower_ci_bound, upper_ci_bound
    FROM onet.v_skills
    WHERE onet_soc_code = '29-1141.00' AND scale_id = 'IM' AND recommend_suppress = 'N'
    ORDER BY data_value DESC, element_id LIMIT 10
""").show()
con.close()
```

### R with DBI and duckdb

Install the R dependencies once: `install.packages(c("DBI", "duckdb"))`.

```r
library(DBI)
con <- dbConnect(duckdb::duckdb(config = list(memory_limit = "128MiB", threads = "1", max_temp_directory_size = "0B")))
dbExecute(con, "INSTALL httpfs")
dbExecute(con, "LOAD httpfs")
dbExecute(con, "ATTACH 'https://huggingface.co/datasets/Nason/onet-database/resolve/d0e84bacef02d4477423edbf7468cc3ec8fb79c2/onet.duckdb' AS onet (READ_ONLY)")
dbGetQuery(con, "SELECT onet_soc_code, title FROM onet.occupation_data ORDER BY onet_soc_code LIMIT 5")
dbDisconnect(con, shutdown = TRUE)
```

In the tested R DuckDB 1.5.5 configuration, BIGINT and DECIMAL results are exposed as doubles. Counts here are exactly representable; decimal ratings and confidence bounds may be approximate in R even though the stored DECIMAL values are exact.

### datapond package

Install or upgrade the Python client with `python -m pip install --upgrade datapond`, or install the released R client from [CRAN](https://cran.r-project.org/package=datapond) with `install.packages("datapond")`. Remote examples are tested with Python datapond 0.1.5 (DuckDB 1.5.4) and CRAN R datapond 0.1.0 (DuckDB 1.5.5); older DuckDB reader versions are not verified here. R 0.1.1 is a separate development version, not the CRAN release.

The examples below use the public default catalog. For limits set before attachment, use the direct DuckDB examples above; package examples here set limits immediately after connecting:

```python
import datapond
print(datapond.list())
datapond.describe('onet', table='work_context')
con = datapond.connect('onet')
con.execute("SET memory_limit='128MiB'; SET threads=1; SET max_temp_directory_size='0B'")
con.sql('SELECT onet_soc_code, title FROM occupation_data ORDER BY onet_soc_code LIMIT 5').show()
con.close()
```

```r
library(datapond)
dp_list()
con <- dp_connect('onet')
DBI::dbExecute(con, "SET memory_limit='128MiB'; SET threads=1; SET max_temp_directory_size='0B'")
dp_describe(con, table = 'work_context')
DBI::dbGetQuery(con, "SELECT onet_soc_code, title FROM occupation_data ORDER BY onet_soc_code LIMIT 5")
dp_disconnect(con)
```

For repeated scans, download once and connect locally:

```python
import datapond
datapond.download('onet')
con = datapond.connect('onet', local=True)
con.sql('SELECT onet_soc_code, title FROM occupation_data ORDER BY onet_soc_code LIMIT 5').show()
con.close()
```

```r
library(datapond)
dp_download('onet')
con <- dp_connect('onet', local = TRUE)
DBI::dbGetQuery(con, "SELECT onet_soc_code, title FROM occupation_data ORDER BY onet_soc_code LIMIT 5")
dp_disconnect(con)
```

Verify the recorded artifact SHA-256 after downloading. In Python datapond 0.1.5 as well as 0.1.1, the optional `huggingface_hub` download path follows the repository default branch rather than the pinned URL. For an exact-version copy, download the immutable URL shown above and verify its checksum; see [consumer verification](https://github.com/ian-nason/onet-database/blob/main/docs/CONSUMERS.md) for the tested configuration.

Default-catalog discovery and representative remote queries were verified after the registry merge. Earlier full-download checks used an isolated candidate registry. See [consumer verification](https://github.com/ian-nason/onet-database/blob/main/docs/CONSUMERS.md) for exact client versions, paths, resource limits and download behavior. The direct URL examples above work independently of the catalog. The SQL examples below use the `onet` catalog alias from the direct-URL quick start.


## Tables

A rating row describes one occupation, one element and one scale; work-context distributions also have a response category. Occupation records, alternate titles and reference tables have different units, listed below. Rating update months vary within this single release.

| Table | Description | Rows | Columns |
|---|---|---:|---:|
| `work_context` | Work-context scale means and separate response-category percentages; never pool scales/categories | 305,389 | 16 |
| `job_titles` | Alternate job titles and original source codes; many titles per occupation | 54,269 | 5 |
| `transferable_skills` | Transferable-skill importance and level ratings with uncertainty, flags and update month | 45,500 | 15 |
| `occupation_level_metadata` | Collection modes, response rates and demographics; not population microdata | 32,280 | 7 |
| `essential_skills` | Essential-skill importance and level ratings with uncertainty, flags and update month | 18,200 | 15 |
| `sample_of_reported_titles` | Sample job titles reported by workers, with My Next Move display flag | 8,189 | 4 |
| `content_model_reference` | Definitions of content-model elements, including hierarchy nodes beyond this subset | 3,006 | 3 |
| `occupation_data` | O*NET-SOC 2019 occupation codes, titles and descriptions; one row per occupation | 1,016 | 3 |
| `level_scale_anchors` | Illustrative descriptions for points on level scales; includes other O*NET domains | 483 | 6 |
| `work_context_categories` | Labels keyed by element, scale and category for work-context response distributions | 281 | 6 |
| `survey_booklet_locations` | Survey question identifiers keyed by element and scale; includes other domains | 211 | 5 |
| `scales_reference` | Scale labels and native minimum/maximum values; no cross-scale normalization | 33 | 4 |

Skill coverage is 910 occupations with 10 essential and 25 transferable elements. Work-context coverage is 911 occupations and 57 elements; distributions cover 902. The 1,016 occupation records are not all rated in each domain. Other 31.0 files (abilities, knowledge, software skills, tasks, crosswalks) are not loaded. `_metadata` has one row per data table; `_columns` carries original headers and descriptions.

## Pre-built Views

| View | What it does |
|---|---|
| `v_skills` | Union of `essential_skills` and `transferable_skills` with a `skill_domain` column; the two domains are disjoint |
| `v_work_context_means` | `work_context` rows with no category: the CX (1 to 5) and CT (1 to 3) means |
| `v_work_context_percentages` | CXP and CTP category percentages joined to their labels on the full `(element_id, scale_id, category)` key |

No view drops suppressed or low-precision ratings; filter on `recommend_suppress` yourself. Views are not counted in the row and table totals above.

## Example Queries

Physical demands of registered nurses, one native mean per element:

```sql
SELECT element_name, data_value, n, standard_error, recommend_suppress, update_date
FROM onet.v_work_context_means
WHERE onet_soc_code = '29-1141.00' AND scale_id = 'CX'
  AND element_id IN ('4.C.2.d.1.b', '4.C.2.d.1.d', '4.C.2.d.1.h')
ORDER BY element_id;
```

How nurses' standing time is distributed across response categories (percent of ratings, not of U.S. nurses):

```sql
SELECT category, category_description, data_value AS response_percent, recommend_suppress, update_date
FROM onet.v_work_context_percentages
WHERE onet_soc_code = '29-1141.00' AND element_id = '4.C.2.d.1.b' AND scale_id = 'CXP'
ORDER BY category;
```

Compare one skill with one context rating without a many-to-many join:

```sql
WITH skill AS (
  SELECT onet_soc_code, title, data_value AS social_perceptiveness_importance
  FROM onet.transferable_skills
  WHERE element_id = '2.B.1.a' AND scale_id = 'IM' AND recommend_suppress = 'N'
), exposure AS (
  SELECT onet_soc_code, data_value AS disease_exposure
  FROM onet.v_work_context_means
  WHERE element_id = '4.C.2.c.1.b' AND scale_id = 'CX' AND recommend_suppress = 'N'
)
SELECT * FROM skill JOIN exposure USING (onet_soc_code)
ORDER BY disease_exposure DESC, onet_soc_code LIMIT 20;
```

The full set is in [examples.sql](https://github.com/ian-nason/onet-database/blob/main/examples.sql); saved results are bound to the artifact hash.

## Researcher Caveats

1. **Scales are not interchangeable.** `IM` is importance (1 to 5), `LV` is level (0 to 7), `CX` is a 1 to 5 mean, `CT` a 1 to 3 mean, and `CXP`/`CTP` are category percentages (0 to 100). Never pool `data_value` across scales; use `scales_reference`, `level_scale_anchors` and `work_context_categories` for meaning.
2. **Suppression and relevance flags.** `recommend_suppress='Y'` marks low precision; values are retained exactly. For rankings, require an explicit `'N'`, which also excludes rows where the flag is missing. `not_relevant='Y'` is a separate flag; a missing value is not an explicit `'N'`.
3. **Uncertainty is per rating.** `n` is the rating sample size, not employment. Standard errors and confidence bounds come from the analyst, incumbent, occupational-expert or transition methods documented by O*NET; do not pool ratings as if independent. See the official [analyst](https://www.onetcenter.org/dictionary/31.0/csv/appendix_analyst.html) and [incumbent/expert](https://www.onetcenter.org/dictionary/31.0/csv/appendix_incumbent.html) notes.
4. **One snapshot, not a panel.** `update_date` keeps the source `MM/YYYY` string; selected ratings span December 2005 to August 2026 and skills span June 2010 to August 2026. Parsing with `strptime(update_date, '%m/%Y')` is for ordering only.
5. **O*NET-SOC codes are ten characters.** Several detailed occupations share a six-digit SOC parent, so a crosswalk is not necessarily one-to-one. No SOC, NAICS, QCEW or ATUS crosswalk is included.
6. **Joins can multiply rows.** An occupation has many titles, skills and context rows. Select or aggregate each table to one row per occupation before joining, as the comparison example does.
7. **Percentages describe ratings.** Category percentages sum to about 100 after source rounding and are not worker counts. Exposure scores describe reported work context, not infection incidence or individual risk.

## Data Source and Version

O*NET 31.0 Database, U.S. Department of Labor, Employment and Training Administration, developed by the National Center for O*NET Development. The pinned source ZIP is 16,237,378 bytes, SHA-256 `55033fc68b4c13ec23e7f74dc6378660f6e854e75d55d6e333ae0a761d3987cd`; 12 of its files are loaded. O*NET publishes quarterly with a primary third-quarter update; this repository does not promise an automatic refresh.

Artifact: `onet.duckdb`, 11,284,480 bytes, SHA-256 `b7908bb82e50d4aa0310a6400e2193e2b11946a9d663ff2c8f1171037585c11b`, dataset commit `d0e84bacef02d4477423edbf7468cc3ec8fb79c2`.

## License and Attribution

This product uses the **O*NET 31.0 Database**, produced by the **U.S. Department of Labor, Employment and Training Administration (USDOL/ETA)** and developed by the National Center for O*NET Development, under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). See the [official database license](https://www.onetcenter.org/license_db.html). O*NET® is a trademark of USDOL/ETA.

Datapond has modified the representation: selected 12 files; renamed columns to snake_case (`Date` → `update_date`); converted exact decimal/integer fields and empty fields to SQL types/NULL; added three views, metadata, dictionary, validation and examples. No source ratings, occupation titles, date tokens, flags or nonblank text values were revised, rescaled, imputed or suppressed. USDOL/ETA has not approved, endorsed or tested these modifications. The scripts and documentation describe every transformation. The database content license is CC BY 4.0; no public-domain claim is made. O*NET career exploration tools are outside this subset and this license statement.

For citation, include O*NET release 31.0, USDOL/ETA, the CC BY 4.0 license link, this derivative's artifact SHA-256 and the recorded build date. Public-host verification is recorded in [PUBLICATION.md](https://github.com/ian-nason/onet-database/blob/main/PUBLICATION.md); the dataset is now included in the public datapond catalog.

## Build from Source

The audited build uses Python 3.12 and DuckDB 1.5.5; dependency and helper revisions are pinned in `pyproject.toml` and `helper-lock.json`.

```sh
python -m unittest -v test_onet test_guard
python run_guarded.py evidence/new-build python onet.py --download --output releases/new-candidate
python run_guarded.py evidence/new-audit python audit_release.py releases/new-candidate/onet.duckdb
```

Use a fresh isolated checkout and output directory. The supervisor bounds memory, disk and runtime; source hashes fail closed. Every typed source cell is compared before checkpoint and after read-only reopen, and 27 regression fixtures cover failure cases. See [build, validation and update details](docs/REPRODUCE.md) for prerequisites, exact limits, source provenance, retained partials, measured resource use and the update procedure. See [the detailed researcher guide](docs/RESEARCHER-GUIDE.md) for the complete original interpretation and code notes.

## GitHub, Dictionary and Website

[Detailed researcher guide](https://github.com/ian-nason/onet-database/blob/main/docs/RESEARCHER-GUIDE.md) · [Build and update instructions](https://github.com/ian-nason/onet-database/blob/main/docs/REPRODUCE.md) · [Verified publication](https://github.com/ian-nason/onet-database/blob/main/PUBLICATION.md)

- Source, build scripts, tests and evidence: [github.com/ian-nason/onet-database](https://github.com/ian-nason/onet-database)
- Column dictionary (every column, original header, type, NULL share, join hint): [DICTIONARY.md](https://github.com/ian-nason/onet-database/blob/main/DICTIONARY.md)
- Catalog: [datapond registry](https://github.com/datapond-db/registry); `onet` is included in the public catalog and on the [datapond website](https://datapond-db.github.io/website/).

## Changelog

### 2026-10-18 — Documentation refresh

- Added Python/R quick starts, table descriptions and column counts, view guidance, navigation, and clearer researcher caveats.
- Database bytes, schema, source locks and validated query results are unchanged. Catalog integration was pending at this documentation checkpoint; it is now complete.

### 2026-10-18 — Initial release

- O*NET 31.0 subset: 468,857 rows across 12 tables (89 columns) and 3 views. Artifact 11,284,480 bytes, SHA-256 `b7908bb8…85c11b`, commit `d0e84bac`.
- Every typed cell verified against an independent read of the pinned source ZIP; public immutable URL, HTTP range requests and the installed Python and R clients tested after upload.
- Registry entry initially opened as a draft pull request; later merged after integration review.
