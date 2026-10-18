---
license: cc-by-4.0
pretty_name: O*NET 31.0 Occupations, Skills and Work Context
tags: [onet, occupations, skills, labor, work-context, duckdb]
size_categories: [100K<n<1M]
---

# O*NET® 31.0 occupations, skills and work context

A version-pinned subset of the [O*NET 31.0 Database](https://www.onetcenter.org/database.html): **468,857 rows in 12 data tables**, three convenience views, and an 89-column dictionary. The DuckDB file is **11,284,480 bytes**.

Use it to explore occupational skill requirements, physical demands and reported disease/infection exposure. It describes occupations, not individual health, illness incidence, wages or employment counts. It is one mixed-date release snapshot, not an annual panel or evidence of causal effects.

| Table | Rows |
|---|---:|
| occupation_data | 1,016 |
| job_titles | 54,269 |
| sample_of_reported_titles | 8,189 |
| essential_skills | 18,200 |
| transferable_skills | 45,500 |
| work_context | 305,389 |
| content_model_reference | 3,006 |
| scales_reference | 33 |
| level_scale_anchors | 483 |
| work_context_categories | 281 |
| occupation_level_metadata | 32,280 |
| survey_booklet_locations | 211 |

## Query directly

With DuckDB and an available httpfs extension:

```sql
LOAD httpfs;
ATTACH 'https://huggingface.co/datasets/Nason/onet-database/resolve/main/onet.duckdb'
  AS onet (READ_ONLY);
SELECT onet_soc_code,title,data_value AS mean_exposure,
       lower_ci_bound,upper_ci_bound,n,update_date,domain_source
FROM onet.v_work_context_means
WHERE element_id='4.C.2.c.1.b' AND scale_id='CX'
  AND recommend_suppress='N'
ORDER BY data_value DESC,onet_soc_code LIMIT 15;
```

Pin the Hugging Face commit in place of `main` for reproducibility. Registry inclusion is a separate PR; `datapond.connect('onet')` and R `dp_connect('onet')` require that entry or a local registry override.

## Interpretation

Retain full O*NET-SOC codes and every part of each table's grain. Joining titles, skills and contexts without preselection or aggregation multiplies rows. SOC crosswalks are not necessarily one-to-one; there is no supplied QCEW, ATUS or NAICS crosswalk.

`IM` (1–5 importance) and `LV` (0–7 level) are different scales. Work-context `CX` and `CT` are native means; `CXP` and `CTP` are percentages of three/five response categories. Never pool them. `v_work_context_means` has 51,927 rows for 911 occupations; category distributions cover 902 occupations and have 253,462 rows in `v_work_context_percentages`. Missing distributions are not imputed. `v_skills` combines disjoint essential/transferable domains with an explicit domain label.

Low-precision `recommend_suppress='Y'` and not-relevant flags remain intact, along with all ratings, sample sizes, standard errors and confidence bounds. A missing flag is not an explicit `N`. Examples rank only explicit unsuppressed ratings. Sample size is not national employment, and ratings from different source methods or update months should not be treated as independent population observations.

Update dates retain original `MM/YYYY` precision. Selected rating update months run December 2005–August 2026; skill months run June 2010–August 2026. This does not imply uniform annual measurement. Scale dictionaries and category/anchor labels accompany the ratings. Other 31.0 domains are omitted.

## Provenance and validation

Artifact SHA-256: `b7908bb82e50d4aa0310a6400e2193e2b11946a9d663ff2c8f1171037585c11b`.
Source ZIP SHA-256: `55033fc68b4c13ec23e7f74dc6378660f6e854e75d55d6e333ae0a761d3987cd`.

[sources-31.0.json](sources-31.0.json) contains pinned source identities, build proof, runtime identity and the independent review's scope. Every typed cell was compared against Python CSV/Decimal reads of the original ZIP both before checkpoint and after read-only reopen. Counts, schemas, keys, references, scales, flags, codelists, category sums and dictionary statistics were checked; 27 regressions passed, including an injected supervisor failure and both worker-exit races. A second build reproduced typed fingerprints and dictionary bytes. Localhost HTTP checks passed in installed Python and R clients; these do not by themselves establish public-host verification.

The final independent Claude review examined supplied code and test evidence, not independently rerun computations. See the [source repository](https://github.com/ian-nason/onet-database) for scripts, detailed limitations, physical-demands/skills examples and audit records; [DICTIONARY.md](DICTIONARY.md) describes every field. O*NET publishes quarterly; this derivative uses manual, version-pinned rebuilds.

## Attribution and changes

This product uses the **O*NET 31.0 Database**, produced by the **U.S. Department of Labor, Employment and Training Administration (USDOL/ETA)** and developed by the National Center for O*NET Development, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [Official database license](https://www.onetcenter.org/license_db.html). O*NET® is a trademark of USDOL/ETA.

Datapond selected 12 files, renamed columns to snake_case (`Date` to `update_date`), converted numeric fields to exact SQL types and source empty fields to NULL, and added views, metadata, dictionary, validation and examples. No nonblank source text, ratings, flags or update tokens were revised, rescaled, imputed or suppressed. USDOL/ETA has not approved, endorsed or tested these modifications. Other O*NET products and career exploration tools are outside this subset and license statement. Cite release 31.0, USDOL/ETA, CC BY 4.0 and the artifact hash.
