"""Invariants for counts, thresholds and leakage. Does not tune model behavior."""
import unittest
from inspection import *

class EvaluationTests(unittest.TestCase):
 def test_abstention_never_becomes_caught_defect(self):
  rows=[{'label':1,'accepted':False,'decision':'retake','milliseconds':1},{'label':1,'accepted':True,'decision':'flag','milliseconds':1},{'label':0,'accepted':True,'decision':'flag','milliseconds':1},{'label':0,'accepted':True,'decision':'no_flag','milliseconds':1}]
  m=metrics(rows);self.assertEqual(m['recall_all_defects']['rate'],.5);self.assertEqual(m['precision_observed']['rate'],.5);self.assertEqual(m['fpr_accepted_normals']['rate'],.5);self.assertEqual(m['coverage']['rate'],.75)
 def test_frozen_thresholds_reproduce_from_calibration_only(self):
  frozen=load('results/frozen_thresholds.json')
  for method,t in frozen['thresholds'].items():
   cal=load(f'results/{method}_calibration.json');self.assertEqual(t,threshold(cal));self.assertLessEqual(metrics(cal)['fpr_accepted_normals']['rate'],.1)
  self.assertEqual(frozen['protocol_sha256'],sha((ROOT/'PROTOCOL.md').read_bytes()))
  self.assertEqual(frozen['split_sha256'],sha((ROOT/'data/splits.json').read_bytes()))
 def test_split_groups_and_exact_pixels_disjoint(self):
  s=load('data/splits.json')
  for field in ['group','pixel_sha256']:
   sets=[{r[field] for r in s[k]} for k in ['reference','calibration','test']]
   self.assertFalse(sets[0]&sets[1] or sets[0]&sets[2] or sets[1]&sets[2])
 def test_output_counts_match_untouched_split(self):
  s=load('data/splits.json')
  for method in ['reference','padim']:
   rows=load(f'results/{method}_test.json');self.assertEqual({r['id'] for r in rows},{r['id'] for r in s['test']});m=metrics(rows)
   self.assertEqual(m['TP']+m['FN_unflagged_accepted']+m['FN_abstained'],80)
   self.assertEqual(m['FP']+m['TN']+m['abstained_normals'],100)
 def test_export_parity(self):
  p=load('results/export_parity.json');self.assertNotIn('error',p)
  self.assertEqual(len(p['fixtures']),10)
  self.assertLess(max(r['score_abs_difference'] for r in p['fixtures']),1e-3)
 def test_no_claimed_human_timing(self):
  for m in load('results/summary.json').values():self.assertTrue(m['test']['total_inspection_time'].startswith('UNMEASURED'))

if __name__=='__main__':unittest.main()
