"""Grade a user-exported exercise response; never invent participant responses."""
import argparse,json
from pathlib import Path
from collections import Counter
p=argparse.ArgumentParser();p.add_argument('responses',type=Path);args=p.parse_args()
root=Path(__file__).resolve().parent
answers={r['id']:r for r in json.loads((root/'artifacts/review_answer_key.json').read_text())}
data=json.loads(args.responses.read_text());seen=set();report={}
for condition in ['manual','assisted']:
 rs=[r for r in data['responses'] if r['condition']==condition]
 for r in rs:
  assert r['id'] in answers and r['id'] not in seen;seen.add(r['id']);assert answers[r['id']]['condition']==condition;assert r['review_ms']>=0
 tp=sum(answers[r['id']]['label']==1 and r['decision']=='defective' for r in rs)
 positives=sum(answers[r['id']]['label'] for r in rs)
 report[condition]={'responses':len(rs),'defects':positives,'caught':tp,'misses_including_cannot_determine':positives-tp,'false_flags':sum(answers[r['id']]['label']==0 and r['decision']=='defective' for r in rs),'cannot_determine':sum(r['decision']=='cannot_determine' for r in rs),'summed_review_seconds':sum(r['review_ms'] for r in rs)/1000}
report['limitations']='Self-recorded convenience exercise, artificial prevalence, unmatched difficulty/order effects; precomputed AI, no capture or physical inspection time. Not proof of time savings.'
target=root/'results/human_review_results.json';target.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
