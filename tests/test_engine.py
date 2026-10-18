import json, tempfile, unittest
from pathlib import Path
from core.engine import compare_json, compare_csv, extract_placeholders, load_json, load_csv, DuplicateKeyError, validate_json_file

class LocalizationQATests(unittest.TestCase):
 def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
 def tearDown(self): self.tmp.cleanup()
 def write_json(self,n,d):
  p=self.root/n; p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8"); return str(p)
 def test_placeholder_extraction(self): self.assertEqual(extract_placeholders("Hi {name}, %s ${id}"),{"{name}":1,"%s":1,"${id}":1})
 def test_placeholder_mismatch(self):
  r=compare_json(self.write_json("a.json",{"x":"Hi {name}"}),self.write_json("b.json",{"x":"Salut {user}"}))
  self.assertTrue(any(f["rule_id"]=="LOC-PLACEHOLDER-001" for f in r["findings"]))
 def test_missing_key(self):
  r=compare_json(self.write_json("a.json",{"a":"A","b":"B"}),self.write_json("b.json",{"a":"Un"}))
  self.assertTrue(any(f["rule_id"]=="LOC-KEY-001" and f.get("key")=="b" for f in r["findings"]))
 def test_extra_key(self):
  r=compare_json(self.write_json("a.json",{"a":"A"}),self.write_json("b.json",{"a":"Un","x":"X"}))
  self.assertTrue(any(f["rule_id"]=="LOC-KEY-002" and f.get("key")=="x" for f in r["findings"]))
 def test_markup_mismatch(self):
  r=compare_json(self.write_json("a.json",{"x":"<b>Read</b>"}),self.write_json("b.json",{"x":"Lire"}))
  self.assertTrue(any(f["rule_id"]=="LOC-MARKUP-001" for f in r["findings"]))
 def test_empty_value(self):
  r=validate_json_file(self.write_json("a.json",{"x":" "}))
  self.assertTrue(any(f["rule_id"]=="LOC-EMPTY-001" for f in r["findings"]))
 def test_invalid_json_shape(self):
  p=self.root/"bad.json"; p.write_text('["no"]',encoding="utf-8")
  with self.assertRaises(ValueError): load_json(p)
 def test_csv_compare(self):
  p=self.root/"x.csv"; p.write_text("key,locale,value\nhello,en,Hello {name}\nhello,fr,Bonjour {name}\n",encoding="utf-8")
  r=compare_csv(str(p),"en","fr"); self.assertEqual(r["summary"]["errors"],0)
 def test_duplicate_csv_key(self):
  p=self.root/"x.csv"; p.write_text("key,locale,value\na,en,A\na,en,Again\n",encoding="utf-8")
  with self.assertRaises(DuplicateKeyError): load_csv(p)
 def test_unicode_replacement(self):
  r=validate_json_file(self.write_json("a.json",{"x":"bad\ufffdtext"}))
  self.assertTrue(any(f["rule_id"]=="LOC-UNICODE-001" for f in r["findings"]))
if __name__=="__main__": unittest.main()
