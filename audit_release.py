"""Independent read-only release invariants beyond row-preserving ingestion."""
import datetime,hashlib,importlib.metadata,inspect,json,pathlib,platform,re,subprocess,sys
import datapond_build
import datapond_build.metadata as helper
import onet
DB=onet.HERE/'releases/31.0-release-final/onet.duckdb'
def require(condition,label):
 if not condition:raise ValueError(label)
def aggregate_checks(con):
 month=onet.LOCK['release_month']
 require(bool(re.fullmatch(r'[0-9]{4}-(0[1-9]|1[0-2])',month)),'Invalid locked release month')
 queries={
 'complete category groups':"SELECT count(*) FROM (SELECT onet_soc_code,element_id,scale_id,count(*) n FROM work_context WHERE category IS NOT NULL GROUP BY ALL) WHERE n<>CASE WHEN scale_id='CXP' THEN 5 WHEN scale_id='CTP' THEN 3 ELSE -1 END",
 'category percentage rounding':"SELECT count(*) FROM (SELECT onet_soc_code,element_id,scale_id,sum(data_value) total FROM work_context WHERE category IS NOT NULL GROUP BY ALL) WHERE abs(total-100)>0.03",
 'occupation code format':"SELECT count(*) FROM occupation_data WHERE NOT regexp_full_match(onet_soc_code,'[0-9]{2}-[0-9]{4}\\.[0-9]{2}')",
 'job title source codes':"SELECT count(*) FROM (SELECT unnest(string_split(sources,',')) code FROM job_titles) WHERE trim(code) NOT IN ('01','02','03','04','07','08','09','10')",
 'reported title flags':"SELECT count(*) FROM sample_of_reported_titles WHERE shown_in_my_next_move NOT IN ('Y','N')",
 'skill scales':"SELECT count(*) FROM v_skills WHERE scale_id NOT IN ('IM','LV')",
 'rating domain sources':"SELECT count(*) FROM (SELECT domain_source FROM v_skills UNION ALL SELECT domain_source FROM work_context) WHERE domain_source NOT IN ('Analyst','Incumbent','Occupational Expert','Analyst - Transition')",
 'occupation metadata percentages':"SELECT count(*) FROM occupation_level_metadata WHERE percent<0 OR percent>100 OR n<0",
 'update month within release':f"SELECT count(*) FROM (SELECT update_date FROM v_skills UNION ALL SELECT update_date FROM work_context UNION ALL SELECT update_date FROM occupation_level_metadata) WHERE strptime(update_date,'%m/%Y')>DATE '{month}-01' OR strptime(update_date,'%m/%Y')<DATE '1998-01-01'",
 }
 result={}
 for label,sql in queries.items():
  result[label]=con.execute(sql).fetchone()[0]
  if result[label]:raise ValueError(f'{label}: {result[label]} violations')
 return result
def main():
 global DB
 if len(sys.argv)>1:DB=pathlib.Path(sys.argv[1])
 report=json.loads((DB.parent/'build-report.json').read_text());require(onet.sha(DB)==report['database_sha256'],'Artifact SHA changed')
 with onet.connection(DB,True) as con:
  result=aggregate_checks(con)
  for t,spec in onet.SCHEMA.items():
   actual=con.execute(f'DESCRIBE {t}').fetchall()
   require([(r[0],r[1]) for r in actual]==[(c['name'],c['type']) for c in spec['columns']],t+': schema')
   meta=con.execute('SELECT row_count,column_count,source_sha256,source_release,license FROM _metadata WHERE table_name=?',[t]).fetchone()
   require(meta==(spec['rows'],len(spec['columns']),spec['source_sha256'],onet.LOCK['release'],'CC-BY-4.0'),t+': metadata')
   for c in spec['columns']:
    stats=con.execute('SELECT data_type,source_file,null_pct,description,source_header FROM _columns WHERE table_name=? AND column_name=?',[t,c['name']]).fetchone()
    require(stats==(c['type'],spec['member'],round(report['source_comparison'][t]['null_counts'][c['name']]*100/spec['rows'],1),c['description'],c['source_header']),t+'.'+c['name']+': dictionary')
  require(con.execute('SELECT count(*) FROM v_skills').fetchone()[0]==63700,'Skills view count')
  require(con.execute('SELECT count(*) FROM v_work_context_means').fetchone()[0]==51927,'Mean view count')
  require(con.execute('SELECT count(*) FROM v_work_context_percentages').fetchone()[0]==253462,'Percentage view count')
 proof={'status':'passed','artifact_sha256':onet.sha(DB),'aggregate_violations':result,'all_schema_metadata_and_dictionary_fields_match':True,'views_match_expected_grain':True}
 pin=json.loads((onet.HERE/'helper-lock.json').read_text())
 modules={}
 for name in ['ensure_metadata','build_columns_table','export_dictionary']:
  function=getattr(datapond_build,name);path=pathlib.Path(inspect.getsourcefile(function))
  modules[name]={'module':function.__module__,'path':str(path),'sha256':onet.sha(path)}
  require(modules[name]['sha256']==pin['metadata_py_sha256'],'Imported helper function differs from pin: '+name)
 runtime={'python':platform.python_version(),'interpreter':sys.executable,'duckdb':onet.duckdb.__version__,'datapond_build_version':importlib.metadata.version('datapond-build'),'datapond_build_install_origin':json.loads(importlib.metadata.distribution('datapond-build').read_text('direct_url.json')),'metadata_helper_sha256':onet.sha(helper.__file__),'helper_source_pin':pin,'metadata_helper_matches_pin':onet.sha(helper.__file__)==pin['metadata_py_sha256'],'used_helper_function_modules':modules,'installed_packages':sorted([{'name':d.metadata['Name'],'version':d.version} for d in importlib.metadata.distributions()],key=lambda x:x['name'].lower()),'platform':platform.platform()}
 onet.save(onet.HERE/'evidence/release-audit.json',proof)
 onet.save(onet.HERE/'runtime.json',runtime);print(json.dumps(proof,indent=2))
if __name__=='__main__':main()
