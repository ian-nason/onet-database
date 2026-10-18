-- Which occupations have the highest mean reported disease/infection exposure?
-- CX is a native 1-5 frequency scale. Explicit N precision flag only.
SELECT onet_soc_code,title,data_value AS mean_exposure,lower_ci_bound,upper_ci_bound,
       n,update_date,domain_source
FROM v_work_context_means
WHERE element_id='4.C.2.c.1.b' AND scale_id='CX' AND recommend_suppress='N'
ORDER BY data_value DESC,onet_soc_code LIMIT 15;

-- Physical demands of registered nurses: separate native means by element.
SELECT element_name,data_value,n,standard_error,recommend_suppress,update_date
FROM v_work_context_means
WHERE onet_soc_code='29-1141.00' AND scale_id='CX'
  AND element_id IN ('4.C.2.d.1.b','4.C.2.d.1.d','4.C.2.d.1.h')
ORDER BY element_id;

-- Distribution of standing time for registered nurses; not a percentage of US nurses.
SELECT category,category_description,data_value AS response_percent,
       recommend_suppress,update_date
FROM v_work_context_percentages
WHERE onet_soc_code='29-1141.00' AND element_id='4.C.2.d.1.b' AND scale_id='CXP'
ORDER BY category;

-- Highest importance skills for registered nurses, one scale only.
SELECT skill_domain,element_name,data_value AS importance,standard_error,
       lower_ci_bound,upper_ci_bound,update_date
FROM v_skills
WHERE onet_soc_code='29-1141.00' AND scale_id='IM' AND recommend_suppress='N'
ORDER BY data_value DESC,element_id LIMIT 10;

-- Compare skill importance and disease exposure without a many-to-many join.
-- Each CTE selects one element, one scale, one rating per occupation.
WITH skill AS (
 SELECT onet_soc_code,title,data_value AS social_perceptiveness_importance,update_date AS skill_updated
 FROM transferable_skills WHERE element_id='2.B.1.a' AND scale_id='IM' AND recommend_suppress='N'
), exposure AS (
 SELECT onet_soc_code,data_value AS disease_exposure,update_date AS context_updated
 FROM v_work_context_means WHERE element_id='4.C.2.c.1.b' AND scale_id='CX' AND recommend_suppress='N'
)
SELECT * FROM skill JOIN exposure USING(onet_soc_code)
ORDER BY disease_exposure DESC,onet_soc_code LIMIT 20;
