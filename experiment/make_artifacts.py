"""Generate transparent report, failure gallery, and uncompleted human exercise."""
from inspection import *
from accounting import fixture
from PIL import ImageDraw
import html,random

out=ROOT/'artifacts';out.mkdir(exist_ok=True)
summary=load('results/summary.json');rows=load('results/padim_test.json');base=load('results/reference_test.json');byid={r['id']:r for r in base}
def overlay(r):
 im=get_image(r).resize((224,224));p=ROOT/'results/maps'/f"padim_{r['id']}.npy"
 if not p.exists():return im
 m=np.load(p);lo,hi=np.percentile(m,[5,99]);scaled=np.clip((m-lo)/(hi-lo+1e-8),0,1)
 heat=cv2.applyColorMap((scaled*255).astype(np.uint8),cv2.COLORMAP_JET)[:,:,::-1]
 return Image.fromarray((np.array(im)*.65+heat*.35).astype(np.uint8))

groups={
 'missed_defect':[r for r in rows if r['label']==1 and r['decision']!='flag'],
 'false_flag':[r for r in rows if r['label']==0 and r['decision']=='flag'],
 'caught_defect':[r for r in rows if r['label']==1 and r['decision']=='flag'],
 'normal_no_flag':[r for r in rows if r['label']==0 and r['decision']=='no_flag'],
 'retake':[r for r in rows if not r['accepted']],
}
examples=[]
for kind,rs in groups.items():
 for r in rs[:3]:
  canvas=Image.new('RGB',(224*3,260),'white');canvas.paste(get_image(r).resize((224,224)),(0,0));canvas.paste(overlay(r),(224,0))
  if r['mask']:canvas.paste(Image.open(ROOT/r['mask']).convert('RGB').resize((224,224)),(448,0))
  ImageDraw.Draw(canvas).text((5,230),f"{kind}: {r['id']} | score={r['score']} | reference={byid[r['id']]['decision']}",fill='black')
  name=f"{kind}_{r['id']}.jpg";canvas.save(out/name);examples.append({'kind':kind,'id':r['id'],'file':name,'score':r['score'],'label':r['label'],'reference_decision':byid[r['id']]['decision']})
dump('artifacts/failure_examples.json',examples)
gallery=''.join(f"<li><p>{html.escape(e['kind'])} — {e['id']}</p><img src='{e['file']}' width='672'></li>" for e in examples)
(out/'failure_gallery.html').write_text(f"<!doctype html><meta charset='utf-8'><title>Observed benchmark outcomes</title><h1>Observed outcomes — not factory evidence</h1><p>Original image | per-image-scaled anomaly heatmap (not probability) | dataset mask. Includes successes and failures. No post-test tuning.</p><ul>{gallery}</ul>",encoding='utf-8')

l=fixture();dump('artifacts/fictional_accounting.json',{'fictional':True,'events':l.events,'counts':l.counts(),'owner':l.owner})
sample=rows[:3]+[r for r in rows if r['label']][:3]
table=''.join(f"<tr><td>DEMO-{i+1}</td><td>{r['id']}</td><td>{r['decision']}</td><td>{r['score']}</td><td>{r['quality_reasons']}</td></tr>" for i,r in enumerate(sample))
counts=''.join(f'<li>{k}: {v}</li>' for k,v in l.counts().items())
body=f"""<!doctype html><meta charset='utf-8'><title>Sample batch report — fictional workflow</title>
<style>body{{font:16px system-ui;max-width:1000px;margin:40px auto;padding:20px}}table{{border-collapse:collapse}}td,th{{border:1px solid #aaa;padding:8px}}.warning{{background:#fff0cc;padding:16px}}</style>
<h1>Sample batch report: FICTIONAL-DEMO-001</h1><p class='warning'>NOT A QUALITY CERTIFICATE. Benchmark model observations below are real. Product/batch IDs, station context, reviewer decisions and rework events are fictional. These are two separate demonstrations and do not describe a real shipment.</p>
<h2>Real image-analysis observations</h2><p>Product: VisA PCB1. Model: configured PaDiM/ResNet18, CPU, frozen threshold {load('results/frozen_thresholds.json')['thresholds']['padim']}. Six dataset photographs mapped to fictional display IDs, not six verified physical products. No person has reviewed these six model observations. No hidden, functional or electrical checks.</p>
<table><tr><th>Fictional display ID</th><th>Dataset image ID</th><th>Model action</th><th>Score (not probability)</th><th>Retake reasons</th></tr>{table}</table>
<p>Model-assessed images: {len(sample)}; quality accepted: {sum(r['accepted'] for r in sample)}; human-completed inspections: 0. Product/lot coverage and real defect prevalence: unknown.</p>
<h2>Separate fictional human-workflow ledger</h2><p>Six declared products A–F. A accepted; B defective then reworked/reinspected acceptable; C unresolved; D defective; E photographed but uninspected; F unphotographed. All decisions attributed to FICTIONAL reviewer. Duplicate A upload counted once.</p><ul>{counts}</ul>
<p>Human-decision coverage: 4/6 have an inspection event; current resolved coverage: 3/6. Two uninspected, one unresolved. Historical defect events are not current defective products.</p>
<h2>Owner approval</h2><p>PENDING — no actual owner has signed. Fixture finalization blocked due to unresolved/uninspected products. No signature generated on the user's behalf.</p>
<h2>Limitations and provenance</h2><p>Public benchmark images; no factory/phone validation, no buyer acceptance, no calibrated defect probability, no causal diagnosis. Physical board IDs unavailable. VisA CC BY 4.0; Zou et al., SPot-the-Difference, ECCV 2022. Mirror revision d185c42584b49f1df81fe12bde627559ed88d483; original-byte equivalence unverified. Dataset license does not by itself establish all pretrained-weight training-data rights.</p>
<p>Protocol SHA256: {sha((ROOT/'PROTOCOL.md').read_bytes())}<br>Split SHA256: {sha((ROOT/'data/splits.json').read_bytes())}<br>Fitted native model SHA256: {sha((ROOT/'models/padim.pt').read_bytes())}<br>Frozen threshold file SHA256: {sha((ROOT/'results/frozen_thresholds.json').read_bytes())}</p>
"""
(out/'sample_batch_report.html').write_text(body,encoding='utf-8')

# 24 disjoint images: 6 normal and 6 defective per condition. Balanced exercise prevalence is artificial.
rng=random.Random(SEED);selected={0:[],1:[]}
for label in [0,1]:
 pool=[r for r in rows if r['label']==label and r['accepted']];rng.shuffle(pool);selected[label]=pool[:12]
tasks=[];answers=[]
for condition in ['manual','assisted']:
 rs=selected[0][:6]+selected[1][:6] if condition=='manual' else selected[0][6:12]+selected[1][6:12]
 rng.shuffle(rs)
 for r in rs:
  name=f"review_{r['id']}.png";get_image(r).save(out/name)
  ov=f"overlay_{r['id']}.jpg";overlay(r).save(out/ov)
  tasks.append({'id':r['id'],'condition':condition,'image':name,'overlay':ov if condition=='assisted' else None,'flag':r['decision'] if condition=='assisted' else None})
  answers.append({'id':r['id'],'label':r['label'],'condition':condition})
assert len({t['id'] for t in tasks})==len(tasks)==24
dump('artifacts/review_answer_key.json',answers)
template="""<!doctype html><meta charset='utf-8'><title>Timed inspection exercise</title>
<style>body{font:18px system-ui;max-width:1050px;margin:30px auto}img{max-width:45%;max-height:65vh}button{font:inherit;padding:12px;margin:5px}.warn{background:#fff0cc;padding:15px}</style>
<h1>Disposable image-review exercise</h1><p class='warn'>UNCOMPLETED. Convenience usability exercise, not expert inspection. 24 different benchmark photos, manual then assisted; matched label counts but difficulty is not guaranteed equal. Artificial 50% defect prevalence. No repeated images. Order/learning effects remain. AI hints are precomputed, so this measures review/interaction time, not capture, retakes, live inference, total factory inspection time, or time savings in production.</p>
<p>Look for bent/melted/scratched/missing visible features. No electrical or hidden-defect decision. Original review photos are lossless PNG copies of decoded dataset images; assisted overlays are resized display transformations. Choose cannot determine whenever unsure. No correct answers are shown during the task.</p><details><summary>Normal reference examples</summary><img src='../results/reference_contact_sheet.jpg' style='max-width:100%'></details>
<button id='start'>Start exercise</button><div id='task'></div><div id='controls' hidden><button data-v='acceptable'>Acceptable</button><button data-v='defective'>Defective</button><button data-v='cannot_determine'>Cannot determine / retake</button></div><pre id='status'></pre>
<script>const tasks=TASKS;let i=0,responses=[],since=0,totalStart=0;const task=document.querySelector('#task'),controls=document.querySelector('#controls');
function show(){if(i>=tasks.length){controls.hidden=true;task.textContent='Exercise complete. Save responses; no efficacy result is claimed until graded.';const data={fictional_batch:true,participant_role:'self-report pending',started_at:new Date(totalStart).toISOString(),completed_at:new Date().toISOString(),total_wall_ms:Date.now()-totalStart,responses};const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));a.download='review_responses.json';a.textContent='Save review responses';task.appendChild(a);window.reviewResponses=data;return;}const t=tasks[i];task.innerHTML=`<h2>${i+1}/24 — ${t.condition}</h2><p>${t.flag?'Model: '+t.flag+' (not ground truth)':'No AI hint'}</p><img id='original' src='${t.image}'>${t.overlay?`<img src='${t.overlay}'>`:''}`;controls.hidden=true;const im=document.querySelector('#original');const ready=()=>{since=performance.now();controls.hidden=false;};if(im.complete)ready();else im.onload=ready;}
document.querySelector('#start').onclick=()=>{document.querySelector('#start').hidden=true;totalStart=Date.now();show();};document.querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>{responses.push({id:tasks[i].id,condition:tasks[i].condition,decision:b.dataset.v,review_ms:performance.now()-since});i++;show();});</script>"""
(out/'review_exercise.html').write_text(template.replace('TASKS',json.dumps(tasks)),encoding='utf-8')
print('Artifacts generated:',out,flush=True)
