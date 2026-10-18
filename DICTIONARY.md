# O*NET 31.0 subset data dictionary

Source: [O*NET 31.0 Database](https://www.onetcenter.org/database.html), USDOL/ETA, CC BY 4.0.
See README for attribution, modifications, grain, interpretation and limitations. Original MM/YYYY update dates remain strings.

## occupation_data

O*NET-SOC 2019 occupation codes, titles and descriptions; one row per occupation.

Source file: `db_31_0_csv/occupation_data.csv`
Rows: 1,016

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| onet_soc_code | VARCHAR | 0.0% | 11-1011.00 | Join occupation_data on the complete 10-character O*NET-SOC code; not a unique key in other tables. |
| title | VARCHAR | 0.0% | Accountants and Auditors |  |
| description | VARCHAR | 0.0% | Accommodate hotel, motel, and resort patrons by registering and assigning roo... |  |

## job_titles

Alternate job titles and original source codes; many titles per occupation.

Source file: `db_31_0_csv/job_titles.csv`
Rows: 54,269

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| onet_soc_code | VARCHAR | 0.0% | 11-1011.00 | Join occupation_data on the complete 10-character O*NET-SOC code; not a unique key in other tables. |
| title | VARCHAR | 0.0% | Accountants and Auditors |  |
| job_title | VARCHAR | 0.0% | .NET Programmer |  |
| short_title | VARCHAR | 91.8% | 3D Animator |  |
| sources | VARCHAR | 0.0% | 01 | Original comma-separated job-title source codes, including leading zeroes. See official dictionary. |

## sample_of_reported_titles

Sample job titles reported by workers, with My Next Move display flag.

Source file: `db_31_0_csv/sample_of_reported_titles.csv`
Rows: 8,189

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| onet_soc_code | VARCHAR | 0.0% | 11-1011.00 | Join occupation_data on the complete 10-character O*NET-SOC code; not a unique key in other tables. |
| title | VARCHAR | 0.0% | Accountants and Auditors |  |
| reported_job_title | VARCHAR | 0.0% | 3D Animator (Three-Dimensional Animator) |  |
| shown_in_my_next_move | VARCHAR | 0.0% | N |  |

## essential_skills

Essential-skill importance and level ratings with uncertainty, flags and update month.

Source file: `db_31_0_csv/essential_skills.csv`
Rows: 18,200

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| onet_soc_code | VARCHAR | 0.0% | 11-1011.00 | Join occupation_data on the complete 10-character O*NET-SOC code; not a unique key in other tables. |
| title | VARCHAR | 0.0% | Accountants and Auditors |  |
| element_id | VARCHAR | 0.0% | 2.A.1.a | Join content_model_reference; hierarchy codes remain text. |
| element_name | VARCHAR | 0.0% | Active Learning |  |
| scale_id | VARCHAR | 0.0% | IM | Join scales_reference; retain scale in rating keys. |
| scale_name | VARCHAR | 0.0% | Importance |  |
| data_value | DECIMAL(18,2) | 0.0% | 0.00 | Native scale rating or category percentage; not a worker-level observation. |
| n | INTEGER | 0.0% | 8 |  |
| standard_error | DECIMAL(18,4) | 0.0% | 0.0000 |  |
| lower_ci_bound | DECIMAL(18,4) | 0.0% | 0.0000 |  |
| upper_ci_bound | DECIMAL(18,4) | 0.0% | 0.0000 |  |
| recommend_suppress | VARCHAR | 0.0% | N | Y = low precision; retain source value but omit from substantive examples. |
| not_relevant | VARCHAR | 50.0% | N | Y = not relevant; NULL is not an explicit N. |
| update_date | VARCHAR | 0.0% | 06/2010 | Original MM/YYYY update month, not survey date, annual panel year or day-precision date. |
| domain_source | VARCHAR | 0.0% | Analyst |  |

## transferable_skills

Transferable-skill importance and level ratings with uncertainty, flags and update month.

Source file: `db_31_0_csv/transferable_skills.csv`
Rows: 45,500

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| onet_soc_code | VARCHAR | 0.0% | 11-1011.00 | Join occupation_data on the complete 10-character O*NET-SOC code; not a unique key in other tables. |
| title | VARCHAR | 0.0% | Accountants and Auditors |  |
| element_id | VARCHAR | 0.0% | 2.B.1.a | Join content_model_reference; hierarchy codes remain text. |
| element_name | VARCHAR | 0.0% | Complex Problem Solving |  |
| scale_id | VARCHAR | 0.0% | IM | Join scales_reference; retain scale in rating keys. |
| scale_name | VARCHAR | 0.0% | Importance |  |
| data_value | DECIMAL(18,2) | 0.0% | 0.00 | Native scale rating or category percentage; not a worker-level observation. |
| n | INTEGER | 0.0% | 8 |  |
| standard_error | DECIMAL(18,4) | 0.0% | 0.0000 |  |
| lower_ci_bound | DECIMAL(18,4) | 0.0% | 0.0000 |  |
| upper_ci_bound | DECIMAL(18,4) | 0.0% | 0.0000 |  |
| recommend_suppress | VARCHAR | 0.0% | N | Y = low precision; retain source value but omit from substantive examples. |
| not_relevant | VARCHAR | 50.0% | N | Y = not relevant; NULL is not an explicit N. |
| update_date | VARCHAR | 0.0% | 06/2010 | Original MM/YYYY update month, not survey date, annual panel year or day-precision date. |
| domain_source | VARCHAR | 0.0% | Analyst |  |

## work_context

Work-context scale means and separate response-category percentages; never pool scales/categories.

Source file: `db_31_0_csv/work_context.csv`
Rows: 305,389

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| onet_soc_code | VARCHAR | 0.0% | 11-1011.00 | Join occupation_data on the complete 10-character O*NET-SOC code; not a unique key in other tables. |
| title | VARCHAR | 0.0% | Accountants and Auditors |  |
| element_id | VARCHAR | 0.0% | 4.C.1.a.2.c | Join content_model_reference; hierarchy codes remain text. |
| element_name | VARCHAR | 0.0% | Conflict Situations |  |
| scale_id | VARCHAR | 0.0% | CT | Join scales_reference; retain scale in rating keys. |
| scale_name | VARCHAR | 0.0% | Context |  |
| category | INTEGER | 17.0% | 1 | Nullable: mean rows have no category; category distributions join work_context_categories on element_id, scale_id AND category. |
| data_value | DECIMAL(18,2) | 0.0% | 0.00 | Native scale rating or category percentage; not a worker-level observation. |
| n | INTEGER | 0.2% | 10 |  |
| standard_error | DECIMAL(18,4) | 27.6% | 0.0000 |  |
| lower_ci_bound | DECIMAL(18,4) | 41.7% | 0.0003 |  |
| upper_ci_bound | DECIMAL(18,4) | 41.7% | 0.0148 |  |
| recommend_suppress | VARCHAR | 27.5% | N | Y = low precision; retain source value but omit from substantive examples. |
| not_relevant | VARCHAR | 100.0% |  | Y = not relevant; NULL is not an explicit N. |
| update_date | VARCHAR | 0.0% | 06/2006 | Original MM/YYYY update month, not survey date, annual panel year or day-precision date. |
| domain_source | VARCHAR | 0.0% | Analyst - Transition |  |

## content_model_reference

Definitions of content-model elements, including hierarchy nodes beyond this subset.

Source file: `db_31_0_csv/content_model_reference.csv`
Rows: 3,006

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| element_id | VARCHAR | 0.0% | 1 | Join content_model_reference; hierarchy codes remain text. |
| element_name | VARCHAR | 0.0% | Abilities |  |
| description | VARCHAR | 80.5% | A statement of required or important duties performed by workers in an occupa... |  |

## scales_reference

Scale labels and native minimum/maximum values; no cross-scale normalization.

Source file: `db_31_0_csv/scales_reference.csv`
Rows: 33

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| scale_id | VARCHAR | 0.0% | AO | Join scales_reference; retain scale in rating keys. |
| scale_name | VARCHAR | 0.0% | % Time |  |
| minimum | INTEGER | 0.0% | -3 |  |
| maximum | INTEGER | 0.0% | 10 |  |

## level_scale_anchors

Illustrative descriptions for points on level scales; includes other O*NET domains.

Source file: `db_31_0_csv/level_scale_anchors.csv`
Rows: 483

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| element_id | VARCHAR | 0.0% | 1.A.1.a.1 | Join content_model_reference; hierarchy codes remain text. |
| element_name | VARCHAR | 0.0% | Active Learning |  |
| scale_id | VARCHAR | 0.0% | LV | Join scales_reference; retain scale in rating keys. |
| scale_name | VARCHAR | 0.0% | Level |  |
| anchor_value | INTEGER | 0.0% | 1 |  |
| anchor_description | VARCHAR | 0.0% | Act as general contractor for building a large industrial complex |  |

## work_context_categories

Labels keyed by element, scale and category for work-context response distributions.

Source file: `db_31_0_csv/work_context_categories.csv`
Rows: 281

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| element_id | VARCHAR | 0.0% | 4.C.1.a.2.c | Join content_model_reference; hierarchy codes remain text. |
| element_name | VARCHAR | 0.0% | Conflict Situations |  |
| scale_id | VARCHAR | 0.0% | CTP | Join scales_reference; retain scale in rating keys. |
| scale_name | VARCHAR | 0.0% | Context (Categories 1-3) |  |
| category | INTEGER | 0.0% | 1 | Nullable: mean rows have no category; category distributions join work_context_categories on element_id, scale_id AND category. |
| category_description | VARCHAR | 0.0% | 40 hours |  |

## occupation_level_metadata

Collection modes, response rates and demographics; not population microdata.

Source file: `db_31_0_csv/occupation_level_metadata.csv`
Rows: 32,280

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| onet_soc_code | VARCHAR | 0.0% | 11-1011.00 | Join occupation_data on the complete 10-character O*NET-SOC code; not a unique key in other tables. |
| title | VARCHAR | 0.0% | Accountants and Auditors |  |
| item | VARCHAR | 0.0% | Data Collection Mode |  |
| response | VARCHAR | 14.5% | 1-2 Years |  |
| n | INTEGER | 11.7% | 100 |  |
| percent | DECIMAL(18,1) | 2.8% | 0.0 |  |
| update_date | VARCHAR | 0.0% | 06/2006 | Original MM/YYYY update month, not survey date, annual panel year or day-precision date. |

## survey_booklet_locations

Survey question identifiers keyed by element and scale; includes other domains.

Source file: `db_31_0_csv/survey_booklet_locations.csv`
Rows: 211

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| element_id | VARCHAR | 0.0% | 2.C.1.a | Join content_model_reference; hierarchy codes remain text. |
| element_name | VARCHAR | 0.0% | Administration and Management |  |
| survey_item_number | VARCHAR | 0.0% | GW01 |  |
| scale_id | VARCHAR | 0.0% | AO | Join scales_reference; retain scale in rating keys. |
| scale_name | VARCHAR | 0.0% | % Time |  |

## Field definitions and source headers

### occupation_data

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/occupation_data.html)

| Column | Original header | Definition |
|---|---|---|
| onet_soc_code | O*NET-SOC Code | O*NET-SOC Code |
| title | Title | O*NET-SOC Title |
| description | Description | O*NET-SOC Description |

### job_titles

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/job_titles.html)

| Column | Original header | Definition |
|---|---|---|
| onet_soc_code | O*NET-SOC Code | O*NET-SOC Code |
| title | Title | O*NET-SOC Title |
| job_title | Job Title | Alternate occupational title |
| short_title | Short Title | Short version of alternate title (if applicable) |
| sources | Source(s) | List of source codes — see below |

### sample_of_reported_titles

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/sample_of_reported_titles.html)

| Column | Original header | Definition |
|---|---|---|
| onet_soc_code | O*NET-SOC Code | O*NET-SOC Code |
| title | Title | O*NET-SOC Title |
| reported_job_title | Reported Job Title | Title from incumbents or occupational experts |
| shown_in_my_next_move | Shown in My Next Move | Whether title is shown on My Next Move career page (Y=yes, N=no) |

### essential_skills

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/essential_skills.html)

| Column | Original header | Definition |
|---|---|---|
| onet_soc_code | O*NET-SOC Code | O*NET-SOC Code |
| title | Title | O*NET-SOC Title |
| element_id | Element ID | Content Model Outline Position |
| element_name | Element Name | Content Model Element Name |
| scale_id | Scale ID | Scale ID |
| scale_name | Scale Name | Scale Name |
| data_value | Data Value | Rating associated with the O*NET-SOC occupation |
| n | N | Sample size |
| standard_error | Standard Error | Standard Error |
| lower_ci_bound | Lower CI Bound | Lower 95% confidence interval bound |
| upper_ci_bound | Upper CI Bound | Upper 95% confidence interval bound |
| recommend_suppress | Recommend Suppress | Low precision indicator (Y=yes, N=no) |
| not_relevant | Not Relevant | Not relevant for the occupation (Y=yes, N=no) |
| update_date | Date | Date when data was updated |
| domain_source | Domain Source | Source of the data |

### transferable_skills

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/transferable_skills.html)

| Column | Original header | Definition |
|---|---|---|
| onet_soc_code | O*NET-SOC Code | O*NET-SOC Code |
| title | Title | O*NET-SOC Title |
| element_id | Element ID | Content Model Outline Position |
| element_name | Element Name | Content Model Element Name |
| scale_id | Scale ID | Scale ID |
| scale_name | Scale Name | Scale Name |
| data_value | Data Value | Rating associated with the O*NET-SOC occupation |
| n | N | Sample size |
| standard_error | Standard Error | Standard Error |
| lower_ci_bound | Lower CI Bound | Lower 95% confidence interval bound |
| upper_ci_bound | Upper CI Bound | Upper 95% confidence interval bound |
| recommend_suppress | Recommend Suppress | Low precision indicator (Y=yes, N=no) |
| not_relevant | Not Relevant | Not relevant for the occupation (Y=yes, N=no) |
| update_date | Date | Date when data was updated |
| domain_source | Domain Source | Source of the data |

### work_context

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/work_context.html)

| Column | Original header | Definition |
|---|---|---|
| onet_soc_code | O*NET-SOC Code | O*NET-SOC Code |
| title | Title | O*NET-SOC Title |
| element_id | Element ID | Content Model Outline Position |
| element_name | Element Name | Content Model Element Name |
| scale_id | Scale ID | Scale ID |
| scale_name | Scale Name | Scale Name |
| category | Category | Percent frequency category |
| data_value | Data Value | Rating associated with the O*NET-SOC occupation |
| n | N | Sample size |
| standard_error | Standard Error | Standard Error |
| lower_ci_bound | Lower CI Bound | Lower 95% confidence interval bound |
| upper_ci_bound | Upper CI Bound | Upper 95% confidence interval bound |
| recommend_suppress | Recommend Suppress | Low precision indicator (Y=yes, N=no) |
| not_relevant | Not Relevant | Not relevant for the occupation (Y=yes, N=no) |
| update_date | Date | Date when data was updated |
| domain_source | Domain Source | Source of the data |

### content_model_reference

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/content_model_reference.html)

| Column | Original header | Definition |
|---|---|---|
| element_id | Element ID | Content Model Outline Position |
| element_name | Element Name | Content Model Element Name |
| description | Description | Content Model Element Description |

### scales_reference

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/scales_reference.html)

| Column | Original header | Definition |
|---|---|---|
| scale_id | Scale ID | Scale ID |
| scale_name | Scale Name | Scale Name |
| minimum | Minimum | Scale Minimum |
| maximum | Maximum | Scale Maximum |

### level_scale_anchors

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/level_scale_anchors.html)

| Column | Original header | Definition |
|---|---|---|
| element_id | Element ID | Content Model Outline Position |
| element_name | Element Name | Content Model Element Name |
| scale_id | Scale ID | Scale ID |
| scale_name | Scale Name | Scale Name |
| anchor_value | Anchor Value | Anchor value associated with element |
| anchor_description | Anchor Description | Detail description of anchor associated with element |

### work_context_categories

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/work_context_categories.html)

| Column | Original header | Definition |
|---|---|---|
| element_id | Element ID | Content Model Outline Position |
| element_name | Element Name | Content Model Element Name |
| scale_id | Scale ID | Scale ID |
| scale_name | Scale Name | Scale Name |
| category | Category | Category value associated with element |
| category_description | Category Description | Detail description of category associated with element |

### occupation_level_metadata

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/occupation_level_metadata.html)

| Column | Original header | Definition |
|---|---|---|
| onet_soc_code | O*NET-SOC Code | O*NET-SOC Code |
| title | Title | O*NET-SOC Title |
| item | Item | Occupation level statistics |
| response | Response | Type of response |
| n | N | Sample size for occupation |
| percent | Percent | Percentage of responses |
| update_date | Date | Date when data was updated |

### survey_booklet_locations

[Official dictionary](https://www.onetcenter.org/dictionary/31.0/csv/survey_booklet_locations.html)

| Column | Original header | Definition |
|---|---|---|
| element_id | Element ID | Content Model Outline Position |
| element_name | Element Name | Content Model Element Name |
| survey_item_number | Survey Item Number | Survey Booklet Location Number |
| scale_id | Scale ID | Scale ID |
| scale_name | Scale Name | Scale Name |

### Job-title source code legend

The source description “see below” refers to this legend: 01 professional associations; 02 incumbent/occupational expert; 03 occupational code assignment; 04 SOC references; 07 government agencies; 08 USDOL/ETA and O*NET Center; 09 user input/web applications; 10 employer job postings. Multiple codes remain comma-delimited strings.
