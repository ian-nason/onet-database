---
license: cc-by-4.0
pretty_name: O*NET 31.0 Occupations, Skills and Work Context
tags: [onet, occupations, skills, labor, work-context, duckdb]
size_categories: [100K<n<1M]
---

# O*NET® 31.0 occupations, skills and work context

A version-pinned, queryable subset of the [O*NET 31.0 Database](https://www.onetcenter.org/database.html): **468,857 source rows, 12 data tables, 3 convenience views**, plus datapond metadata and an 89-column dictionary.

This addition supports occupational questions about standing, bending, exposure to disease or infections, and skill requirements. It complements datapond's administrative datasets with descriptions of work. It does not measure illness, wages, employment counts or causal effects. QCEW industry employment and ATUS time use can supply different perspectives in separate analyses; they do not share a ready-made person or occupation key with these tables. There is no evidence of user demand or adoption implied by this selection.

## Scope and grain

| Table | Rows | Grain |
|---|---:|---|
| occupation_data | 1,016 | One O*NET-SOC 2019 occupation |
| job_titles | 54,269 | Occupation × alternate title |
| sample_of_reported_titles | 8,189 | Occupation × reported title |
| essential_skills | 18,200 | Occupation × element × scale |
| transferable_skills | 45,500 | Occupation × element × scale |
| work_context | 305,389 | Occupation × element × scale × nullable category |
| content_model_reference | 3,006 | Content-model element, including hierarchy nodes |
| scales_reference | 33 | Scale ID |
| level_scale_anchors | 483 | Element × scale × anchor value |
| work_context_categories | 281 | Element × scale × category |
| occupation_level_metadata | 32,280 | Occupation × item × response |
| survey_booklet_locations | 211 | Element × scale × survey question |

Skill coverage is 910 occupations, with 10 essential and 25 transferable elements. Work-context coverage is 911 occupations and 57 elements. The 1,016 occupation records are not all rated in each domain. Reference tables intentionally include elements outside this subset. Other 31.0 files, including abilities, knowledge, software skills, tasks and crosswalks, are omitted. The full archive is retained as the pinned input, not represented as a full-database ingestion.

`v_skills` combines the two disjoint skill domains and adds `skill_domain`. `v_work_context_means` selects rows with no category; `v_work_context_percentages` joins category labels on the complete `(element_id, scale_id, category)` key. Neither view drops suppressed or missing-precision ratings. Views do not contribute to the registry row/table totals.

## Interpretation and joins

* Preserve the full ten-character `onet_soc_code`. Its detailed occupations may share a six-digit SOC parent; a crosswalk is not necessarily one-to-one. No SOC, NAICS, QCEW or ATUS crosswalk is included or implied.
* `IM` is importance (1–5), `LV` is level (0–7). Work-context `CX` is a 1–5 mean and `CT` a 1–3 mean. `CXP` and `CTP` contain separate category percentages (0–100). Never pool their `data_value` values. Use the element-specific category labels and level anchors.
* `recommend_suppress='Y'` marks low precision. Values are retained exactly; substantive ranking examples require explicit `'N'`, excluding missing flags as well. A missing flag does not mean reliable. `not_relevant='Y'` is a separate flag; a missing relevance flag is not an explicit `'N'`. For level comparisons, require explicit relevant and unsuppressed values.
* Confidence bounds and standard errors preserve four decimal places. `n` is the source's rating sample size, not national employment. Analyst, incumbent, occupational-expert and transition sources have different methods. See the official [analyst](https://www.onetcenter.org/dictionary/31.0/csv/appendix_analyst.html) and [incumbent/expert](https://www.onetcenter.org/dictionary/31.0/csv/appendix_incumbent.html) statistics documentation. Do not infer independence or population confidence intervals by pooling ratings.
* `update_date` retains the original `MM/YYYY` string. It is the month data were updated, not a uniformly observed year or collection day. The selected ratings span update months **December 2005–August 2026**; skills span June 2010–August 2026. This is one release snapshot, not an annual panel. Parsing with `strptime(update_date,'%m/%Y')` is useful for ordering only; the resulting first day is a computational placeholder.
* An occupation has many titles, skills and context rows. Joining those tables without selecting/aggregating their grains multiplies rows. The final example first selects one skill and one context rating per occupation.
* Category percentages sum to approximately 100 after source rounding, not to employee counts. Means cover 911 occupations; distributions cover 902. Preserve both and do not invent missing categories or estimates. The source's distributions all have their complete three or five categories in this release.
* Exposure scores describe the occupation's reported work context. They do not measure infection incidence or individual health risk. No population denominator, causal model or personal inference is supplied.

## Concrete queries

Open the locally built artifact read-only:

```python
import duckdb
con = duckdb.connect('releases/31.0-release-final/onet.duckdb', read_only=True)
con.sql("SELECT * FROM _metadata").show()
```

Which occupations have the highest reported exposure frequency, retaining uncertainty and update month?

```sql
SELECT onet_soc_code,title,data_value AS mean_exposure,
       lower_ci_bound,upper_ci_bound,n,update_date,domain_source
FROM v_work_context_means
WHERE element_id='4.C.2.c.1.b' AND scale_id='CX'
  AND recommend_suppress='N'
ORDER BY data_value DESC,onet_soc_code LIMIT 15;
```

Which skills have the highest importance for registered nurses?

```sql
SELECT skill_domain,element_name,data_value AS importance,
       standard_error,lower_ci_bound,upper_ci_bound,update_date
FROM v_skills
WHERE onet_soc_code='29-1141.00' AND scale_id='IM'
  AND recommend_suppress='N'
ORDER BY data_value DESC,element_id LIMIT 10;
```

[examples.sql](examples.sql) also reports nurses' standing/walking/bending means, their standing-time response distribution, and a grain-safe comparison of social perceptiveness with disease exposure. Example results are saved with the artifact hash; rankings are descriptive and small differences should not be overinterpreted.

## Reproduce and update

The build uses Python 3.12, DuckDB 1.5.5 and the existing datapond-build helper from the already provisioned FJC judges virtual environment. `runtime.json` records the interpreter, every installed package/version, and the source module/hash of each used helper function. No software was installed for this candidate. In a separately provisioned environment, use the declared dependencies in `pyproject.toml`.

```sh
python -m unittest -v test_onet test_guard
python onet.py --download --output releases/new-candidate
```

The downloader requires exact byte size and SHA-256 from `source-lock.json`; a changed upstream file fails closed. Recorded ETag/Last-Modified values are provenance, not substitutes for content hashes; a header-only change does not reject identical bytes. The source ZIP is 16,237,378 bytes, SHA-256 `55033fc68b4c13ec23e7f74dc6378660f6e854e75d55d6e333ae0a761d3987cd`. `schema.json` pins selected CSV members, their byte counts, SHA-256s, official row counts, headers, data types and dictionary links. An existing output directory is refused. Failures are retained for inspection; use a new candidate directory. A retained `.partial` source is never silently deleted; inspect it and choose a new `--archive` path to retry.

The builder sets 256 MiB DuckDB memory, one thread, 128 MiB spill, strict CSV parsing and explicit decimal/text types. It checks 10 GiB free disk before building. On Linux use `python run_guarded.py evidence/new-run python onet.py --download --output releases/new-candidate` for the additional 768 MiB process-group RSS stop, 2 GiB cap over all files in this isolated repository (including retained attempts and Git files), 1.5 GiB available-memory floor and 15-minute deadline. Engine memory limits alone do not cap process RSS. The release build took about 14.3 seconds, with 230.5 MiB sampled peak process-group RSS; the artifact is 11,284,480 bytes. The guard receipt records its executable hash and complete command. Measurements are observations, not estimates inferred from ZIP size.

Every row and typed cell is compared against an independent Python `csv`/`Decimal` pass through the original ZIP, including source order, both before checkpoint and after closing and reopening the persisted file read-only. Validation also checks keys, foreign references and labels, required fields, native scale ranges, flags, uncertainty, category grain, official counts, metadata and dictionary coverage. Category percentage sums must be within 0.03 percentage points of 100. Record-level examples, NULL counts and per-table typed fingerprints are retained in the build report. Source order is an audit device, not a stable query ordering contract; always specify `ORDER BY` for analytical output. ZIP members are streamed to fixed allowlisted filenames; no archive paths are extracted directly.

The actual imported metadata helper is hashed and checked against `helper-lock.json`, derived from the source commit pinned in `pyproject.toml`. The build machine's installed distribution metadata still identifies v0.1.1; the used metadata implementation exactly matches the pinned source file, as computed in `runtime.json`. This is not a claim that a fresh dependency installation was tested.

Run `python audit_release.py path/to/onet.duckdb` and `python validate_examples.py path/to/onet.duckdb` for release checks. The optional consumer harness accepts `--artifact`, `--rscript` and `--r-lib-root`; the latter points to existing `cran/datapond` and `patched/datapond` R libraries. It records installed R package file hashes, uses isolated caches, and loads only preinstalled httpfs. No packages are installed by these checks. The included local evidence tests Python DuckDB 1.5.4 and R DuckDB 1.5.5; public hosting must still be verified after publication.

To update: select a specific upstream release; independently verify license and source URLs; create a new branch and lock/schema files from that release's dictionaries; review renamed tables, changed taxonomy and scale definitions; rebuild in a new directory under the supervisor; run all tests, all-cell comparison, example and Python/R HTTP consumer checks; obtain an independent Claude audit and resolve findings. Only then publish to the approved repository, verify the immutable remote artifact hash and real consumer queries, and open a separate registry PR. O*NET publishes quarterly with a primary third-quarter update; this repository does not claim an automated refresh schedule. Metadata timestamps make rebuild bytes non-identical; source identities and typed table fingerprints establish logical reproducibility.

## Dictionary and codes

[DICTIONARY.md](DICTIONARY.md) lists every column, original header, type, source file, NULL proportion, example and join hint. `_metadata` has one row per data table; `_columns` also stores original headers and descriptions. Original CSV empty fields map to SQL NULL, with no other string trimming or replacement. Numeric zeros stay zero. Invalid numeric/date tokens and excess decimal precision cause audit failure.

Job-title `sources` retains comma-delimited string codes: `01` professional associations; `02` incumbents/occupational experts; `03` occupational code assignment; `04` SOC references; `07` government agencies; `08` USDOL/ETA and O*NET Center; `09` user input/web applications; `10` employer job postings. `shown_in_my_next_move` is the original Y/N display flag. Occupation-level `item` and `response` are source labels/codes describing collection and respondent composition, not attributes of every worker in the occupation; consult the versioned [occupation metadata dictionary](https://www.onetcenter.org/dictionary/31.0/csv/occupation_level_metadata.html) and its linked appendix for each item. No weights or person-level records are added.

## Attribution, license and modifications

This product uses the **O*NET 31.0 Database**, produced by the **U.S. Department of Labor, Employment and Training Administration (USDOL/ETA)** and developed by the National Center for O*NET Development, under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). See the [official database license](https://www.onetcenter.org/license_db.html). O*NET® is a trademark of USDOL/ETA.

Datapond has modified the representation: selected 12 files; renamed columns to snake_case (`Date` → `update_date`); converted exact decimal/integer fields and empty fields to SQL types/NULL; added three views, metadata, dictionary, validation and examples. No source ratings, occupation titles, date tokens, flags or nonblank text values were revised, rescaled, imputed or suppressed. USDOL/ETA has not approved, endorsed or tested these modifications. The scripts and documentation describe every transformation. The database content license is CC BY 4.0; no public-domain claim is made. O*NET career exploration tools are outside this subset and this license statement.

For citation, include O*NET release 31.0, USDOL/ETA, the CC BY 4.0 license link, this derivative's artifact SHA-256 and the recorded build date. Registry inclusion and public-host verification remain separate release gates.
