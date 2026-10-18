"""Negative regression fixtures exercise semantic failure modes, not just counts."""
import copy,csv,decimal,io,json,pathlib,tempfile,unittest,zipfile
from unittest.mock import patch
import onet

class Values(unittest.TestCase):
 def test_code_and_source_leading_zero_preserved(self):
  self.assertEqual(onet.typed('08',{'name':'sources','type':'VARCHAR','optional':False}),'08')
  self.assertEqual(onet.typed('11-1011.00',{'name':'onet_soc_code','type':'VARCHAR','optional':False}),'11-1011.00')
 def test_four_decimal_precision(self):
  c={'name':'standard_error','type':'DECIMAL(18,4)','optional':True}
  self.assertEqual(onet.typed('0.2851',c),decimal.Decimal('0.2851'))
  with self.assertRaises(ValueError):onet.typed('0.28511',c)
 def test_no_silent_numeric_coercion(self):
  for value in ['nan','inf','1e2',' 1.0','bad']:
   with self.subTest(value=value),self.assertRaises(ValueError):onet.typed(value,{'name':'x','type':'DECIMAL(18,2)','optional':True})
 def test_blank_is_not_zero(self):
  self.assertIsNone(onet.typed('',{'name':'n','type':'INTEGER','optional':True}))
  self.assertEqual(onet.typed('0',{'name':'n','type':'INTEGER','optional':True}),0)
  with self.assertRaises(ValueError):onet.typed('',{'name':'x','type':'VARCHAR','optional':False})
 def test_update_month_preserved_and_validated(self):
  c={'name':'update_date','type':'VARCHAR','optional':False}
  self.assertEqual(onet.typed('08/2023',c),'08/2023')
  for bad in ['13/2023','2023','08/32','2023-08-01']:
   with self.assertRaises(ValueError):onet.typed(bad,c)

class SemanticChecks(unittest.TestCase):
 def setUp(self):
  self.con=onet.connection(':memory:')
  for table,spec in onet.SCHEMA.items():self.con.execute('CREATE TABLE '+table+'('+','.join(onet.q(c['name'])+' '+c['type'] for c in spec['columns'])+')')
  self.con.execute("INSERT INTO occupation_data VALUES ('11-1011.00','Chief Executives','Description')")
  self.con.execute("INSERT INTO content_model_reference VALUES ('e','Example','Description')")
  self.con.execute("INSERT INTO scales_reference VALUES ('CX','Context',1,5),('CXP','Categories 1-5',0,100),('CT','Context',1,3),('CTP','Categories 1-3',0,100)")
  self.con.execute("INSERT INTO work_context_categories VALUES ('e','Example','CXP','Categories 1-5',1,'Never'),('e','Example','CTP','Categories 1-3',1,'Low')")
 def tearDown(self):self.con.close()
 def context(self,scale='CX',category=None,value='3.07',flag='N',occupation='11-1011.00'):
  label={'CX':'Context','CT':'Context','CXP':'Categories 1-5','CTP':'Categories 1-3'}[scale]
  self.con.execute('INSERT INTO work_context VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[occupation,'Chief Executives','e','Example',scale,label,category,value,37,'0.2851','2.4923','3.6486',flag,None,'08/2023','Incumbent'])
 def test_both_category_scale_families_valid(self):
  self.context();self.context('CT',None,2);self.context('CXP',1,25);self.context('CTP',1,33)
  onet.checks(self.con)
 def test_duplicate_mean_without_category_rejected(self):
  self.context();self.context()
  with self.assertRaisesRegex(ValueError,'keys'):onet.checks(self.con)
 def test_category_omitted_rejected(self):
  self.context('CXP',None,25)
  with self.assertRaisesRegex(ValueError,'grain'):onet.checks(self.con)
 def test_wrong_category_dictionary_rejected(self):
  self.context('CTP',4,25)
  with self.assertRaisesRegex(ValueError,'category labels'):onet.checks(self.con)
 def test_mean_percentage_confusion_rejected(self):
  self.context('CX',None,75)
  with self.assertRaisesRegex(ValueError,'scales'):onet.checks(self.con)
 def test_orphan_occupation_rejected(self):
  self.context(occupation='99-9999.00')
  with self.assertRaisesRegex(ValueError,'occupation/title'):onet.checks(self.con)
 def test_suppressed_value_retained(self):
  self.context(flag='Y');onet.checks(self.con)
  self.assertEqual(self.con.execute('SELECT data_value FROM work_context').fetchone()[0],decimal.Decimal('3.07'))
 def test_unknown_flag_rejected(self):
  self.context(flag='?')
  with self.assertRaisesRegex(ValueError,'flags'):onet.checks(self.con)

class SourceAudit(unittest.TestCase):
 def test_typed_source_comparison_detects_modified_value(self):
  spec={'x':{'member':'x.csv','rows':1,'columns':[{'source_header':'Code','name':'code','type':'VARCHAR','optional':False}]}}
  with tempfile.TemporaryDirectory() as d,onet.connection(':memory:') as con:
   archive=pathlib.Path(d)/'source.zip'
   with zipfile.ZipFile(archive,'w') as z:z.writestr('x.csv','Code\n08\n')
   con.execute("CREATE TABLE x AS SELECT '8' AS code")
   with patch.object(onet,'SCHEMA',spec),self.assertRaisesRegex(ValueError,'Cell mismatch'):onet.audit_source(con,archive)
 def test_hash_mismatch_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   path=pathlib.Path(d)/'x.zip';path.write_bytes(b'not the source')
   with self.assertRaisesRegex(ValueError,'SHA mismatch'):onet.verify_archive(path)
 def test_existing_output_refused(self):
  with tempfile.TemporaryDirectory() as d,self.assertRaises(FileExistsError):onet.build(pathlib.Path('absent.zip'),pathlib.Path(d))
 def archive_fixture(self,variant):
  with tempfile.TemporaryDirectory() as d:
   path=pathlib.Path(d)/'x.zip'
   with zipfile.ZipFile(path,'w') as z:
    z.writestr('x.csv','Code\n08\n')
    if variant=='duplicate':z.writestr('x.csv','Code\n08\n')
   lock={'archive':{'bytes':path.stat().st_size,'sha256':onet.sha(path)}}
   spec={'x':{'member':'absent.csv' if variant=='missing' else 'x.csv','source_bytes':9 if variant=='size' else 8}}
   with patch.object(onet,'LOCK',lock),patch.object(onet,'SCHEMA',spec):
    if variant=='inflated':
     original=zipfile.ZipFile.infolist
     def large(z):
      rows=original(z);rows[0].file_size=257*1024**2;return rows
     with patch.object(zipfile.ZipFile,'infolist',large),self.assertRaisesRegex(ValueError,'inflated size'):onet.verify_archive(path)
    else:
     messages={'missing':'Missing selected ZIP member','duplicate':'Duplicate ZIP names','size':'Member size differs'}
     with self.assertRaisesRegex(ValueError,messages[variant]):onet.verify_archive(path)
 def test_missing_zip_member(self):self.archive_fixture('missing')
 def test_duplicate_zip_member(self):self.archive_fixture('duplicate')
 def test_wrong_zip_member_size(self):self.archive_fixture('size')
 def test_inflated_zip_size(self):self.archive_fixture('inflated')
 def test_partial_preserved_with_actionable_failure(self):
  with tempfile.TemporaryDirectory() as d:
   path=pathlib.Path(d)/'x.zip';partial=path.with_suffix('.partial');partial.write_bytes(b'failure evidence')
   with self.assertRaisesRegex(FileExistsError,'choose a new --archive path'):onet.download(path)
   self.assertEqual(partial.read_bytes(),b'failure evidence')

class DistributionChecks(unittest.TestCase):
 setUp=SemanticChecks.setUp
 tearDown=SemanticChecks.tearDown
 context=SemanticChecks.context
 def prepare(self):
  self.con.execute("CREATE VIEW v_skills AS SELECT 'essential' AS skill_domain,* FROM essential_skills UNION ALL SELECT 'transferable',* FROM transferable_skills")
  for category in range(1,6):self.context('CXP',category,20)
 def test_missing_category_rejected(self):
  from audit_release import aggregate_checks
  self.prepare();self.con.execute('DELETE FROM work_context WHERE category=5')
  with self.assertRaisesRegex(ValueError,'complete category'):aggregate_checks(self.con)
 def test_wrong_percentage_total_rejected(self):
  from audit_release import aggregate_checks
  self.prepare();self.con.execute('UPDATE work_context SET data_value=19 WHERE category=1')
  with self.assertRaisesRegex(ValueError,'percentage rounding'):aggregate_checks(self.con)
 def test_unknown_title_source_code_rejected(self):
  from audit_release import aggregate_checks
  self.prepare();self.con.execute("INSERT INTO job_titles VALUES ('11-1011.00','Chief Executives','Example',NULL,'99')")
  with self.assertRaisesRegex(ValueError,'source codes'):aggregate_checks(self.con)
if __name__=='__main__':unittest.main(verbosity=2)
