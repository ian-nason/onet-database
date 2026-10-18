import datetime,hashlib,json,pathlib,re,sys
import onet
if not __debug__:raise RuntimeError('Run validation without Python optimization')
db=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else onet.HERE/'releases/31.0-release-final/onet.duckdb'
with onet.connection(db,True) as con:
 queries=re.sub(r'--[^\n]*','',(onet.HERE/'examples.sql').read_text()).split(';')
 results=[]
 for query in queries:
  if not query.strip():continue
  rows=con.execute(query).fetchall();assert rows
  results.append({'query':query.strip(),'columns':[c[0] for c in con.description],'rows':rows})
 date=con.execute("SELECT min(strptime(update_date,'%m/%Y')),max(strptime(update_date,'%m/%Y')) FROM v_skills UNION ALL SELECT min(strptime(update_date,'%m/%Y')),max(strptime(update_date,'%m/%Y')) FROM work_context UNION ALL SELECT min(strptime(update_date,'%m/%Y')),max(strptime(update_date,'%m/%Y')) FROM occupation_level_metadata").fetchall()
 sums=con.execute("SELECT scale_id,min(total),max(total),min(k),max(k),count(*),count(*) FILTER(WHERE abs(total-100)>0.03) FROM (SELECT onet_soc_code,element_id,scale_id,sum(data_value) total,count(*) k FROM work_context WHERE category IS NOT NULL GROUP BY ALL) GROUP BY scale_id").fetchall()
 coverage=con.execute('SELECT count(DISTINCT onet_soc_code),count(DISTINCT element_id) FROM essential_skills UNION ALL SELECT count(DISTINCT onet_soc_code),count(DISTINCT element_id) FROM transferable_skills UNION ALL SELECT count(DISTINCT onet_soc_code),count(DISTINCT element_id) FROM work_context').fetchall()
 flags={t:con.execute(f'SELECT recommend_suppress,not_relevant,count(*) FROM {t} GROUP BY ALL ORDER BY ALL').fetchall() for t in onet.RATINGS}
 report={'artifact_sha256':onet.sha(db),'examples':results,'month_ranges_skills_context_metadata':date,'percent_group_diagnostics':sums,'coverage_skills_transferable_context':coverage,'flags':flags,'status':'passed_local'}
 onet.save(onet.HERE/'evidence/examples.json',report)
 print(json.dumps({k:v for k,v in report.items() if k not in ['examples','flags']},indent=2,default=str))
