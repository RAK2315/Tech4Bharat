"""Fictional workflow accounting, independent of inspection accuracy."""
import unittest
from accounting import Ledger,fixture

class AccountingTests(unittest.TestCase):
 def test_duplicate_photo_does_not_inflate_products(self):
  l=Ledger(['A','B']);l.photo('A','hash1');l.photo('A','hash1')
  self.assertEqual(l.counts()['products'],2);self.assertEqual(l.counts()['unique_photos'],1)
 def test_cross_product_identical_photo_rejected(self):
  l=Ledger(['A','B']);l.photo('A','hash1')
  with self.assertRaises(ValueError):l.photo('B','hash1')
 def test_rework_retains_history_changes_current_disposition(self):
  l=Ledger(['A']);l.photo('A','hash1');l.inspect('A','defective','fictional-reviewer');l.rework('A');l.photo('A','hash2');l.inspect('A','acceptable','fictional-reviewer')
  self.assertEqual(l.counts()['current_acceptable'],1);self.assertEqual(l.counts()['historical_defect_events'],1);self.assertEqual(l.counts()['unique_inspected'],1);self.assertEqual(l.counts()['inspection_events'],2)
 def test_unresolved_is_not_complete_or_approved(self):
  l=Ledger(['A','B']);l.photo('A','hash1');l.inspect('A','cannot_determine','fictional-reviewer')
  self.assertEqual(l.counts()['uninspected'],1);self.assertEqual(l.counts()['unresolved'],1)
  with self.assertRaises(ValueError):l.approve('fictional-owner')
 def test_owner_approval_separate(self):
  l=Ledger(['A']);l.photo('A','hash1');l.inspect('A','acceptable','fictional-reviewer')
  self.assertIsNone(l.owner);l.approve('fictional-owner');self.assertEqual(l.owner,'fictional-owner')
 def test_unknown_product_rejected(self):
  with self.assertRaises(ValueError):Ledger(['A']).photo('Z','hash1')
 def test_fixture_exact_counts(self):
  l=fixture();self.assertEqual(l.counts(),{'products':6,'unique_photos':6,'duplicate_uploads':1,'inspection_events':5,'unique_inspected':4,'completed_current':3,'current_acceptable':2,'current_defective':1,'unresolved':1,'uninspected':2,'awaiting_reinspection':0,'historical_defect_events':2})

if __name__=='__main__':unittest.main()
