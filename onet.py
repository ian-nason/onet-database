"""Pinned, bounded O*NET 31.0 ingestion. No source values are silently coerced."""
from __future__ import annotations
import argparse, csv, datetime, decimal, hashlib, io, json, os, pathlib, re, shutil, urllib.request, zipfile
import duckdb
from datapond_build import ensure_metadata, build_columns_table, export_dictionary

HERE = pathlib.Path(__file__).resolve().parent
SCHEMA = json.loads((HERE/'schema.json').read_text())
LOCK = json.loads((HERE/'source-lock.json').read_text())
RATINGS = ('essential_skills','transferable_skills','work_context')
KEYS = {
 'occupation_data':['onet_soc_code'], 'job_titles':['onet_soc_code','job_title'],
 'sample_of_reported_titles':['onet_soc_code','reported_job_title'],
 'essential_skills':['onet_soc_code','element_id','scale_id'],
 'transferable_skills':['onet_soc_code','element_id','scale_id'],
 'work_context':['onet_soc_code','element_id','scale_id','category'],
 'content_model_reference':['element_id'], 'scales_reference':['scale_id'],
 'level_scale_anchors':['element_id','scale_id','anchor_value'],
 'work_context_categories':['element_id','scale_id','category'],
 'occupation_level_metadata':['onet_soc_code','item','response'],
 'survey_booklet_locations':['element_id','scale_id','survey_item_number'],
}
DESCRIPTIONS = {
 'occupation_data':'O*NET-SOC 2019 occupation codes, titles and descriptions; one row per occupation.',
 'job_titles':'Alternate job titles and original source codes; many titles per occupation.',
 'sample_of_reported_titles':'Sample job titles reported by workers, with My Next Move display flag.',
 'essential_skills':'Essential-skill importance and level ratings with uncertainty, flags and update month.',
 'transferable_skills':'Transferable-skill importance and level ratings with uncertainty, flags and update month.',
 'work_context':'Work-context scale means and separate response-category percentages; never pool scales/categories.',
 'content_model_reference':'Definitions of content-model elements, including hierarchy nodes beyond this subset.',
 'scales_reference':'Scale labels and native minimum/maximum values; no cross-scale normalization.',
 'level_scale_anchors':'Illustrative descriptions for points on level scales; includes other O*NET domains.',
 'work_context_categories':'Labels keyed by element, scale and category for work-context response distributions.',
 'occupation_level_metadata':'Collection modes, response rates and demographics; not population microdata.',
 'survey_booklet_locations':'Survey question identifiers keyed by element and scale; includes other domains.',
}
HINTS = {
 'onet_soc_code':'Join occupation_data on the complete 10-character O*NET-SOC code; not a unique key in other tables.',
 'element_id':'Join content_model_reference; hierarchy codes remain text.',
 'scale_id':'Join scales_reference; retain scale in rating keys.',
 'category':'Nullable: mean rows have no category; category distributions join work_context_categories on element_id, scale_id AND category.',
 'data_value':'Native scale rating or category percentage; not a worker-level observation.',
 'recommend_suppress':'Y = low precision; retain source value but omit from substantive examples.',
 'not_relevant':'Y = not relevant; NULL is not an explicit N.',
 'update_date':'Original MM/YYYY update month, not survey date, annual panel year or day-precision date.',
 'sources':'Original comma-separated job-title source codes, including leading zeroes. See official dictionary.',
}
def q(s): return '"'+s.replace('"','""')+'"'
def lit(s): return "'"+str(s).replace("'","''")+"'"
def sha(path):
 h=hashlib.sha256()
 with pathlib.Path(path).open('rb') as f:
  while chunk:=f.read(1024*1024):h.update(chunk)
 return h.hexdigest()
def save(path,obj):path.write_text(json.dumps(obj,indent=2,default=str)+'\n')
def typed(value,col):
 if value=='':
  if not col['optional']:raise ValueError('Blank required field: '+col['name'])
  return None
 typ=col['type']
 if typ=='VARCHAR':
  if col['name']=='update_date' and not re.fullmatch(r'(0[1-9]|1[0-2])/[12][0-9]{3}',value):raise ValueError('Invalid update month')
  return value
 if typ=='INTEGER':
  if not re.fullmatch(r'-?\d+',value):raise ValueError('Invalid integer')
  return int(value)
 if typ.startswith('DECIMAL'):
  scale=int(typ.split(',')[1][:-1])
  if not re.fullmatch(r'-?\d+(\.\d{1,'+str(scale)+r'})?',value):raise ValueError('Invalid or overprecision decimal')
  return decimal.Decimal(value)
 raise ValueError(typ)
def verify_archive(path):
 if path.stat().st_size!=LOCK['archive']['bytes'] or sha(path)!=LOCK['archive']['sha256']:raise ValueError('Archive size/SHA mismatch')
 with zipfile.ZipFile(path) as z:
  members=z.infolist()
  if len({i.filename for i in members})!=len(members):raise ValueError('Duplicate ZIP names')
  if sum(i.file_size for i in members)>256*1024**2:raise ValueError('ZIP inflated size exceeds 256 MiB')
  for spec in SCHEMA.values():
   try:info=z.getinfo(spec['member'])
   except KeyError as e:raise ValueError('Missing selected ZIP member: '+spec['member']) from e
   if info.file_size!=spec['source_bytes']:raise ValueError('Member size differs')
def download(path):
 if path.exists():verify_archive(path);return
 path.parent.mkdir(parents=True,exist_ok=True)
 partial=path.with_suffix('.partial')
 if partial.exists():raise FileExistsError(f'Retained incomplete source: {partial}. Inspect it, then choose a new --archive path; no source or failure evidence is overwritten.')
 with urllib.request.urlopen(LOCK['archive']['url'],timeout=45) as r, partial.open('xb') as f:
  size=0
  while b:=r.read(1024*1024):
   size+=len(b)
   if size>LOCK['archive']['bytes']:raise ValueError('Download exceeds pinned size')
   f.write(b)
 verify_archive(partial);partial.rename(path)
def connection(path,readonly=False):
 return duckdb.connect(str(path),read_only=readonly,config={'memory_limit':'256MiB','threads':'1','max_temp_directory_size':'128MiB','preserve_insertion_order':'true'})
def checks(con):
 results={}
 def zero(label,sql):
  n=con.execute(sql).fetchone()[0];results[label]=n
  if n:raise ValueError(f'{label}: {n} violations')
 for t,spec in SCHEMA.items():
  names={c['name'] for c in spec['columns']};key=','.join(q(c) for c in KEYS[t])
  zero(t+': keys',f'SELECT count(*)-count(DISTINCT ({key})) FROM {q(t)}')
  for col in spec['columns']:
   if not col['optional']:zero(t+': required '+col['name'],f'SELECT count(*) FROM {q(t)} WHERE {q(col["name"])} IS NULL')
  if 'onet_soc_code' in names and t!='occupation_data':
   zero(t+': occupation/title',f'SELECT count(*) FROM {q(t)} x LEFT JOIN occupation_data d USING(onet_soc_code) WHERE d.onet_soc_code IS NULL OR x.title<>d.title')
  for ident,label,ref in [('element_id','element_name','content_model_reference'),('scale_id','scale_name','scales_reference')]:
   if ident in names and t!=ref:
    zero(t+': '+ident,f'SELECT count(*) FROM {q(t)} x LEFT JOIN {ref} d USING({ident}) WHERE d.{ident} IS NULL OR x.{label}<>d.{label}')
 for t in RATINGS:
  zero(t+': scales',f'SELECT count(*) FROM {t} x JOIN scales_reference s USING(scale_id) WHERE data_value<s.minimum OR data_value>s.maximum')
  zero(t+': flags',f"SELECT count(*) FROM {t} WHERE recommend_suppress NOT IN ('Y','N') OR not_relevant NOT IN ('Y','N')")
  zero(t+': uncertainty',f'SELECT count(*) FROM {t} WHERE n<0 OR standard_error<0 OR lower_ci_bound>upper_ci_bound')
 zero('context category labels','SELECT count(*) FROM work_context x LEFT JOIN work_context_categories c USING(element_id,scale_id,category) WHERE x.category IS NOT NULL AND c.category IS NULL')
 zero('context grain',"SELECT count(*) FROM work_context WHERE scale_id NOT IN ('CT','CX','CTP','CXP') OR (scale_id IN ('CTP','CXP'))<>(category IS NOT NULL)")
 zero('skill domain overlap','SELECT count(*) FROM (SELECT DISTINCT element_id FROM essential_skills INTERSECT SELECT DISTINCT element_id FROM transferable_skills)')
 return results
def audit_source(con,archive):
 """Independent Python CSV/Decimal pass compares EVERY typed cell with DuckDB rows."""
 reports={}
 with zipfile.ZipFile(archive) as z:
  for t,spec in SCHEMA.items():
   cursor=con.execute(f'SELECT * FROM {q(t)} ORDER BY rowid')
   with z.open(spec['member']) as raw:
    reader=csv.reader(io.TextIOWrapper(raw,encoding='utf-8-sig',newline=''),strict=True)
    if next(reader)!=[c['source_header'] for c in spec['columns']]:raise ValueError('Header changed')
    n=0;digest=hashlib.sha256();samples=[];nulls=[0]*len(spec['columns'])
    for batch in iter(lambda:cursor.fetchmany(1024),[]):
     for actual in batch:
      row=next(reader,None)
      if row is None or len(row)!=len(spec['columns']):raise ValueError('Source/table row width or count differs')
      expected=tuple(typed(v,c) for v,c in zip(row,spec['columns']))
      if actual!=expected:raise ValueError(f'Cell mismatch: {t} source record {n+1}: {expected} != {actual}')
      n+=1
      nulls=[a+int(v is None) for a,v in zip(nulls,actual)]
      digest.update(json.dumps(actual,ensure_ascii=False,default=str,separators=(',',':')).encode()+b'\n')
      if n in [1,spec['rows']//2,spec['rows']]:samples.append({'record':n,'source':row,'typed':actual})
    if next(reader,None) is not None or n!=spec['rows']:raise ValueError('Official/source/table count differs')
   reports[t]={'rows':n,'all_cells_equal':True,'typed_rows_sha256':digest.hexdigest(),'null_counts':dict(zip([c['name'] for c in spec['columns']],nulls)),'samples':samples}
 return reports
def build(archive,out):
 if out.exists():raise FileExistsError('Use a new output directory; failed artifacts are retained')
 verify_archive(archive)
 parent=out.parent
 while not parent.exists():parent=parent.parent
 if shutil.disk_usage(parent).free<10*1024**3:raise RuntimeError('Need 10 GiB free disk')
 out.mkdir(parents=True);rawdir=out/'raw';rawdir.mkdir()
 with zipfile.ZipFile(archive) as z:
  for t,spec in SCHEMA.items():
   path=rawdir/(t+'.csv')
   with z.open(spec['member']) as src,path.open('xb') as dst:shutil.copyfileobj(src,dst,1024*1024)
   if sha(path)!=spec['source_sha256']:raise ValueError('Member SHA mismatch')
 con=connection(out/'onet.duckdb')
 try:
  for t,spec in SCHEMA.items():
   fields=','.join(lit(c['source_header'])+":'VARCHAR'" for c in spec['columns'])
   exprs=','.join(f'CAST({q(c["source_header"])} AS {c["type"]}) AS {q(c["name"])}' for c in spec['columns'])
   con.execute(f"CREATE TABLE {q(t)} AS SELECT {exprs} FROM read_csv({lit(rawdir/(t+'.csv'))}, columns={{{fields}}}, header=true, nullstr='', parallel=false, strict_mode=true, ignore_errors=false)")
   print(t,con.execute(f'SELECT count(*) FROM {q(t)}').fetchone()[0],flush=True)
  validation=checks(con);proof=audit_source(con,archive)
  con.execute("CREATE VIEW v_skills AS SELECT 'essential' AS skill_domain,* FROM essential_skills UNION ALL SELECT 'transferable' AS skill_domain,* FROM transferable_skills")
  con.execute("CREATE VIEW v_work_context_means AS SELECT * FROM work_context WHERE category IS NULL")
  con.execute("CREATE VIEW v_work_context_percentages AS SELECT x.*,c.category_description FROM work_context x JOIN work_context_categories c USING(element_id,scale_id,category)")
  ensure_metadata(con,descriptions=DESCRIPTIONS,tables=list(SCHEMA),source_url=LOCK['archive']['url'],license='CC-BY-4.0',replace=True)
  con.execute('ALTER TABLE _metadata ADD COLUMN source_file VARCHAR');con.execute('ALTER TABLE _metadata ADD COLUMN source_sha256 VARCHAR');con.execute('ALTER TABLE _metadata ADD COLUMN source_release VARCHAR')
  for t,spec in SCHEMA.items():con.execute('UPDATE _metadata SET source_file=?,source_sha256=?,source_release=? WHERE table_name=?',[spec['member'],spec['source_sha256'],LOCK['release'],t])
  build_columns_table(con,tables=list(SCHEMA),join_hints=HINTS)
  con.execute('ALTER TABLE _columns ADD COLUMN description VARCHAR');con.execute('ALTER TABLE _columns ADD COLUMN source_header VARCHAR')
  for t,spec in SCHEMA.items():
   for col in spec['columns']:con.execute('UPDATE _columns SET description=?,source_header=? WHERE table_name=? AND column_name=?',[col['description'],col['source_header'],t,col['name']])
  export_dictionary(con,out/'DICTIONARY.md',title='O*NET 31.0 subset data dictionary',tables=list(SCHEMA),intro=['Source: [O*NET 31.0 Database](https://www.onetcenter.org/database.html), USDOL/ETA, CC BY 4.0.','See README for attribution, modifications, grain, interpretation and limitations. Original MM/YYYY update dates remain strings.'])
  with (out/'DICTIONARY.md').open('a') as f:
   f.write('\n## Field definitions and source headers\n\n')
   for t,spec in SCHEMA.items():
    f.write(f'### {t}\n\n[Official dictionary]({spec["dictionary_url"]})\n\n| Column | Original header | Definition |\n|---|---|---|\n')
    for c in spec['columns']:f.write('| '+c['name']+' | '+c['source_header']+' | '+c['description'].replace('|','\\|')+' |\n')
    f.write('\n')
   f.write('### Job-title source code legend\n\nThe source description “see below” refers to this legend: 01 professional associations; 02 incumbent/occupational expert; 03 occupational code assignment; 04 SOC references; 07 government agencies; 08 USDOL/ETA and O*NET Center; 09 user input/web applications; 10 employer job postings. Multiple codes remain comma-delimited strings.\n')
  con.execute('CHECKPOINT')
 finally:con.close()
 with connection(out/'onet.duckdb',True) as con:
  validation.update(checks(con))
  persisted_proof=audit_source(con,archive)
  if persisted_proof!=proof:raise ValueError('Persisted typed data differ from pre-checkpoint audit')
  metadata=con.execute('SELECT count(*),sum(row_count),sum(column_count) FROM _metadata').fetchone()
  if metadata[0]!=len(SCHEMA) or metadata[1]!=sum(s['rows'] for s in SCHEMA.values()) or metadata[2]!=con.execute('SELECT count(*) FROM _columns').fetchone()[0]:raise ValueError('Metadata mismatch')
 report={'status':'validated_local_not_published','release':LOCK['release'],'built_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'duckdb':duckdb.__version__,'archive':LOCK['archive'],'database_bytes':(out/'onet.duckdb').stat().st_size,'database_sha256':sha(out/'onet.duckdb'),'rows':metadata[1],'data_tables':metadata[0],'dictionary_columns':metadata[2],'validation':validation,'source_comparison':persisted_proof,'all_cells_reverified_after_read_only_reopen':True,'build_input_sha256':{name:sha(HERE/name) for name in ['onet.py','schema.json','source-lock.json','pyproject.toml']}}
 save(out/'build-report.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ['validation','source_comparison','archive']},indent=2),flush=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=pathlib.Path,default=HERE/'data/db_31_0_csv.zip');p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--download',action='store_true');a=p.parse_args()
 if a.download:download(a.archive)
 build(a.archive,a.output)
if __name__=='__main__':main()
