"""Produce the readable decision report from persisted measurements."""
from inspection import *
from pathlib import Path
summary=load('results/summary.json');audit=load('results/leakage_audit.json');env=load('results/environment.json');export=load('results/export_parity.json')
browser=load('results/browser_results.json') if (ROOT/'results/browser_results.json').exists() else None
lines=['# Validation experiment results — 17 October 2026','',
'- Decision: **NO-GO for a full hackathon MVP using this frozen detector configuration.** Conditional go for one limited follow-up after a clearer capture/defect scope and a new untouched holdout. This does not establish that all anomaly detection is unsuitable.',
'- No paid APIs, cloud inference, added hardware, factory integration, causal simulation, buyer contact, or full app. Actual CPU inference and local browser parity ran.',
'- Skills used: installed verification-before-completion and systematic-debugging workflows; hf-cli guidance for public dataset/model provenance; TDD for meaningful fictional accounting invariants. Disposable experiment authorization overrides a full product design/approval workflow.',
'- Recovered constraints: one Codex-assisted builder, later TypeScript preference, free services only, no added hardware, public data only. No representative phone photos, factory access, manufacturer/buyer contacts assumed. Idea November 15, prototype December 15, finale December 27, 2026; registration November 10. Team-size/student eligibility remains unresolved.',
'- Product: PCB1 ultrasonic sensor module board, one visible top face, with in-plane rotation/position variations already present in normal reference photographs. Bent/Melt/Scratch/Missing are original dataset labels, not reliably predicted classes. Mirror masks are binary, so no subtype recall is reported.',
'- Data supports only a custom benchmark baseline. It does not establish prescribed real-world capture conditions, actual product provenance, or field performance.',
'- Data: 904 source-training normals and 200 source-test images (100 normal/100 defective). Frozen custom split: 100 normal references; 100 normal +20 defective calibration; 100 normal +80 defective final test; 704 source-training normals unused. Deliberate adaptation of official split, not official VisA benchmark performance.',
'- Leakage audit: zero exact/conservative near-duplicate pairs detected using decoded SHA256 and pHash+appearance criteria; partition groups disjoint. No serial/physical-board identifiers: physical-instance leakage remains possible. Mirror bytes not independently compared to original archive.',
'- Thresholds selected using calibration only under <=10% accepted-normal FPR, maximizing calibration recall; persisted before final test scoring. No parameter or threshold tuning after final failures. Test prevalence is 80/180=44.44%, not a factory estimate.',
'- Provisional screening targets fixed before inference: all-defect flagging recall >=90%, accepted-normal FPR <=10%, image-analysis coverage >=90%, warm p95 <=5 seconds on available CPU. These are engineering screens, not industrial requirements.',
'']
for method in ['reference','padim']:
 m=summary[method]['test'];cal=summary[method]['calibration']
 lines += [f'## {method}',f"- Calibration: caught {cal['TP']}/{cal['defects']} defects, false flags {cal['FP']}/{cal['normals']} normals; threshold {load('results/frozen_thresholds.json')['thresholds'][method]}.",
 f"- Recall: {m['TP']}/{m['defects']} = {100*m['recall_all_defects']['rate']:.2f}%; missed {m['FN_unflagged_accepted']} accepted defects and {m['FN_abstained']} abstained defects. Wilson 95% interval {m['recall_all_defects']['wilson95']}.",
 f"- False-positive rate: {m['FP']}/{m['normals']} = {100*m['fpr_accepted_normals']['rate']:.2f}%. True normal/no-flag {m['TN']}. Precision {m['TP']}/{m['TP']+m['FP']} = {100*m['precision_observed']['rate']:.2f}% at observed 44.44% prevalence.",
 f"- Coverage {m['coverage']['numerator']}/{m['count']}; retake requests {m['retake_requests']}. Coverage means model-assessed images, not human-completed inspections.",
 f"- Decode/preprocess/gate/inference/score median {m['latency_ms']['median']:.2f}ms; p95 {m['latency_ms']['p95']:.2f}ms; aggregate processing {m['latency_ms']['total_processing_seconds']:.2f}s. Rendering/export, human review, capture and retakes not included.",
 f"- Provisional screen pass: {m['provisional_screen_pass']}. Human and total inspection time UNMEASURED; user's exercise pending."]
 for stress,m in summary[method]['synthetic_stress'].items():
  lines.append(f"- SYNTHETIC {stress}: caught {m['TP']}/80 defects, false flags {m['FP']}/100 normals, retakes {m['retake_requests']}/180. Paired transformed copies, not independent new products or real lighting captures.")
 lines.append('')
lines += ['## Interpretation and failures',
'- Learned method flags more defects than simple matching, but neither approaches the required recall screen; learned model also exceeds the FPR screen. Detection tradeoff dominates runtime: laptop execution is fast enough, inspection usefulness is not established.',
'- Both methods miss test_0070, test_0025 and test_0037. PaDiM falsely flags dataset-normal test_0125, test_0194 and test_0119. Original/map/mask examples in failure_gallery.html. Per-image heatmap scaling is a display aid, not probability/severity. Binary masks cannot support cause or subtype conclusions.',
'- No quality-gate rejection even on the chosen brightness/blur transformations. The limited gate does not establish image suitability; bright stress increases PaDiM false flags to 27/100. These transformations do not reproduce physical shadows, glare, or changed optical visibility.',
'- Potential explanations requiring new experiments: orientation/position variation challenges spatial reference methods; full-frame 224px resize can reduce small-defect visibility; 50-channel compact PaDiM and 100 references may not model normal variability. These are hypotheses, not diagnosed causes. Do not tune and then re-label this same final holdout as untouched.',
'- HYPOTHETICAL 1% defect prevalence, assuming unchanged sensitivity/specificity: PaDiM flags approximately 5.625 true and 148.5 false items per 1,000, precision about 3.65%; reference matching approximately 1.875 true and 9.9 false, precision about 15.92%. Fractional values are expected counts, not observations. No real factory prevalence is known.',
'', '## Runtime and browser',
f"- CPU-only {env['python']}, {env['logical_cpus']} logical cores, four Torch threads. PaDiM fitting {env['padim_fit_seconds']:.2f}s after feature/model initialization; recorded native run {env['run_total_seconds']:.2f}s before export, excluding downloads, environment setup and artifact generation. Package versions in results/environment.json.",
f"- Exported model {export.get('model_bytes')} bytes; native ONNX comparison on ten fixtures, maximum score difference {max(r['score_abs_difference'] for r in export['fixtures']):.8f}. No unexplained decision changes on those fixtures."]
if browser and browser.get('complete'):
 rs=browser['fixtures'];times=[r['decode_resize_inference_ms'] for r in rs]
 lines += [f"- Actual browser: {browser['userAgent']}; WASM one thread, {len(rs)} selected fixtures. Same-tensor maximum score delta {max(abs(r['native_score']-r['browser_exact_tensor_score']) for r in rs):.8f}; independent resize raw-image maximum score delta {max(abs(r['native_score']-r['browser_raw_image_score']) for r in rs):.8f}; flag agreement {sum(r['native_flag']==r['browser_flag'] for r in rs)}/{len(rs)}.",
 f"- Local model fetch {browser['model_fetch_ms']:.2f}ms; session initialization {browser['session_initialization_ms']:.2f}ms; selected-fixture raw decode/resize/inference median {np.median(times):.2f}ms, p95 {np.percentile(times,95):.2f}ms. Localhost is not an internet/mobile download measurement. Resize max pixel discrepancy about 1/255, not bit-identical; normalization is embedded in the same ONNX graph.",
 '- Browser runtime initially failed on relative WASM module URL; fixed asset URL only, retained first failure. Full quality-gate port, all-test browser accuracy, sustained load, phone compatibility and low-memory operation remain untested. Model alone exceeds the previously checked 25MiB static-host asset limit; deployment packaging is unresolved.']
else:lines.append('- Browser not successfully completed; see results/browser_results.json if present.')
lines += ['', '## Software accounting and sample report',
'- Separate fictional fixture: six product IDs; six distinct photos including B rework photo; one duplicate upload; five inspection events on four unique inspected products; three currently resolved products (two acceptable/one defective), one unresolved, two uninspected; two historical defect events; owner approval pending/blocked. Fictional events are not observations about a factory.',
'- 13 tests passed: duplicate/cross-product photo handling, unknown IDs, rework/history, unresolved approvals, fixture counts; plus abstention denominators, calibration-only thresholds, split disjointness, output accounting, native export parity, and no fabricated human timing. This is a small fixture ledger, not production-ready provenance/security software.',
'- sample_batch_report.html separates six real model observations mapped to fictional display IDs from the fictional human ledger; shows missing actual human review and pending owner approval. No actual owner signature or buyer acceptance.',
'', '## What passed, failed, or remains unknown',
'- Passed in limited scope: free local data/model access; actual CPU inference; count/split/threshold invariants; ten-fixture laptop browser parity; preparation of user review and feedback materials.',
'- Failed: frozen accuracy screens for both methods; robustness screen is not established by basic exposure/focus gate; no evidence to permit skipping unflagged products.',
'- Unknown: human assistance/time benefit, label agreement with experts, capture workload, real phone performance, new manufacturer transfer, true physical-product leakage, real defect prevalence, buyer usefulness and willingness to adopt.',
'', '## Next decision',
'- NO-GO on the full MVP with this configuration. No supported full-MVP effort estimate: the detection prerequisite failed, so the previous 60–90h estimate is withdrawn.',
'- Cheapest next step: complete the prepared 24-image manual/assisted exercise, then diagnose misses using existing failure gallery. The exercise measures a self-recorded convenience review task, not industrial efficacy.',
'- If continuing, timebox a follow-up to 1–2 working days (budget limit, not forecast): fix one capture orientation/view and a clearly visible defect subset, compare simple alignment/cropped inspection against the same established approach using calibration only; reserve a NEW holdout. Do not promise higher accuracy before measurement.',
'- Reconsider a smallest MVP only after accuracy and human workload gates pass: upload, one recipe, review/abstain, accurate coverage, owner-approved report. Excluded: 3D twin, causal diagnosis, live machines and production/buyer claims.',
'', '## Reproduce and review',
'- Instructions and pinned dependencies: ../README.md and ../requirements-lock.txt. Native entrypoints: download.py, prepare.py, run.py, make_artifacts.py; server: serve.py; review grading: grade_review.py with actual participant response file.',
'- Frozen protocol ../PROTOCOL.md; raw metrics ../results/summary.json; split audit ../results/leakage_audit.json; complete per-image records ../results/*_test.json; checksums ../data/download_manifest.json.',
'- Source attribution and licensing in ../README.md. Manufacturer/buyer exercise in ../feedback.md; no external contact or feedback invented.']
(ROOT/'artifacts/EXPERIMENT_REPORT.md').write_text('\n\n'.join(lines),encoding='utf-8')
files=['PROTOCOL.md','inspection.py','prepare.py','run.py','download.py','accounting.py','test_accounting.py','test_evaluation.py','make_artifacts.py','summarize.py','browser/index.html','requirements-lock.txt']
dump('results/source_checksums.json',{f:sha((ROOT/f).read_bytes()) for f in files})
print('Report saved',ROOT/'artifacts/EXPERIMENT_REPORT.md')
