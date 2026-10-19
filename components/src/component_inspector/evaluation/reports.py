"""Read-only reporting after original evaluation and paired stress complete."""
from html import escape
import json
from pathlib import Path

from component_inspector.evaluation.freeze import verify_freeze
from component_inspector.evaluation.runner import verify_completion


def gallery_html(gallery, prefix):
    chunks=['<p>Anomaly intensity, not probability or severity. Fixed calibration display scale.</p>']
    for case in ('TP','FN','FP','TN'):
        item=gallery.get(case,{})
        chunks.append(f'<h3>{case}</h3>')
        if 'original' not in item:
            chunks.append('<p>no example in this evaluated membership</p>');continue
        chunks.append(f'<p>{escape(item["id"])}</p>')
        for field in ('original','overlay','mask'):
            if item.get(field):
                path=escape(f'{prefix}/{item[field]}',quote=True)
                chunks.append(f'<a href="{path}"><img style="max-width:30%" src="{path}" alt="{field}"></a>')
    return '\n'.join(chunks)


def report(run):
    run=Path(run).resolve();snapshot=verify_freeze(run)
    evaluation=verify_completion(run,'evaluation');verify_completion(run,'calibration')
    stress=verify_completion(run,'stress')
    lines=['# Frozen research evaluation',f'\nDecision: **{evaluation["decision"]}**.',
        '\nLocal noncommercial research on identified supplied archives. Cable-gland early-review notice and unverified provider release identity remain disclosed.',
        '\nNo factory-readiness or human inspection-time saving is established. Quality warnings do not exclude images. Technical rejected defects count as misses.',
        '\nPrimary method was PaDiM before test access. Baseline-only success requires a scope decision. No holdout tuning or repeat evaluation is permitted.',
        '\n| Recipe / method | TP / FN / FP / TN | Recall | Accepted-normal FPR | Coverage | Warm p95 seconds | Peak tree RSS GiB | Screen |',
        '|---|---|---|---|---|---|---|---|']
    html=['<!doctype html><meta charset="utf-8"><title>Frozen failure gallery</title><h1>Frozen failure gallery</h1>']
    def pct(value):return 'undefined' if value is None else f'{100*value:.2f}%'
    for recipe in snapshot['details']['protocol']['recipes']:
        for method in ('reference','padim'):
            key=f'{recipe}_{method}';relative=f'evaluation/{key}/{key}.json'
            value=json.loads((run/relative).read_text(encoding='utf-8'));m=value['metrics'];c=m['counts']
            memory=evaluation['resources'][key]['peak_sampled_rss_bytes']/1024**3
            latency=value['warm_p95_pipeline_seconds'];latency='undefined' if latency is None else f'{latency:.4f}'
            lines.append(f'| {recipe} / {method} | {c["TP"]} / {c["FN"]} / {c["FP"]} / {c["TN"]} | {pct(m["recall"]["rate"])} | {pct(m["accepted_normal_fpr"]["rate"])} | {pct(m["coverage"]["rate"])} | {latency} | {memory:.3f} | {evaluation["screens"][recipe][method]["passed"]} |')
            html.append(f'<h2>{escape(key)}</h2>')
            html.append(gallery_html(value['gallery'],f'evaluation/{key}'))
    lines.extend(['\n## Paired stress (same test items; not independent validation)',
        '\n| Recipe / method / transform | Recall | Accepted-normal FPR | Coverage |',
        '|---|---|---|---|'])
    for recipe in snapshot['details']['protocol']['recipes']:
        for method in ('reference','padim'):
            key=f'{recipe}_{method}'
            value=json.loads((run/f'stress/{key}/{key}.json').read_text(encoding='utf-8'))
            for transform,data in value['transforms'].items():
                m=data['metrics']
                lines.append(f'| {recipe} / {method} / {transform} | {pct(m["recall"]["rate"])} | {pct(m["accepted_normal_fpr"]["rate"])} | {pct(m["coverage"]["rate"])} |')
    lines.extend(['\nFull per-method result JSON files contain Wilson 95% intervals, explicit numerators/denominators, precision, scored-subset AUROC/AP, technical rejects, warning diagnostics, cold/init timing and pixel diagnostics.',
        '\nPixel metric is macro per-anomalous-image pixel AUROC where defined; it is not pooled dataset pixel AUROC. Empty/constant truth masks have no defined AUROC.',
        '\nFit time, model bytes and feasibility resources are in the development summaries locked in freeze.json. Inference resources are conservative owned-process-tree RSS samples, including initialization.',
        '\nSee [failure gallery](gallery.html), freeze.json, calibration_complete.json, evaluation_complete.json and stress_complete.json for identities and hash-linked evidence. Missing gallery categories are explicitly marked.'])
    (run/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (run/'gallery.html').write_text('\n'.join(html),encoding='utf-8')
    return {'report':str(run/'REPORT.md'),'gallery':str(run/'gallery.html'),'decision':evaluation['decision']}
