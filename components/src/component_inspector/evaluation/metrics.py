"""Count all expected defects, including technical rejects, as specified."""
import math
import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score


def rate(numerator, denominator):
    if not denominator:
        return {'numerator':numerator,'denominator':0,'rate':None,'wilson_95':None}
    p=numerator/denominator;z=1.959963984540054
    normalizer=1+z*z/denominator
    center=(p+z*z/(2*denominator))/normalizer
    half=z*math.sqrt(p*(1-p)/denominator+z*z/(4*denominator**2))/normalizer
    return {'numerator':numerator,'denominator':denominator,'rate':p,
            'wilson_95':[max(0,center-half),min(1,center+half)]}


def evaluate(predictions, labels_and_masks):
    labels=labels_and_masks
    if any(x not in (0,1) for x in labels.values()):raise ValueError('Unknown truth label')
    if len({p['id'] for p in predictions})!=len(predictions):raise ValueError('Duplicate prediction ID')
    if any(p['id'] not in labels for p in predictions):raise ValueError('Unexpected prediction ID')
    by_id={p['id']:p for p in predictions}
    counts={'TP':0,'FN':0,'FP':0,'TN':0,'rejected_anomalies':0,'rejected_normals':0}
    y,scores=[],[]
    accepted_anomalies=accepted_normals=0
    for identity,label in labels.items():
        p=by_id.get(identity,{'status':'not_scored','score':None,'flagged':None})
        if p['status']!='scored':
            if p.get('score') is not None or p.get('flagged') is not None:
                raise ValueError('Rejected prediction carries a false score/flag')
            counts['rejected_anomalies' if label else 'rejected_normals']+=1
            if label:counts['FN']+=1
            continue
        if p.get('flagged') not in (True,False) or not np.isfinite(p.get('score',float('nan'))):
            raise ValueError('Invalid scored prediction')
        y.append(label);scores.append(p['score'])
        if label:
            accepted_anomalies+=1;counts['TP' if p['flagged'] else 'FN']+=1
        else:
            accepted_normals+=1;counts['FP' if p['flagged'] else 'TN']+=1
    positives=sum(labels.values());negatives=len(labels)-positives
    ranking={'n':len(y),'auroc':None,'average_precision':None,'population':'scored subset only'}
    if len(set(y))==2:
        ranking.update(auroc=float(roc_auc_score(y,scores)),average_precision=float(average_precision_score(y,scores)))
    return {'counts':counts,'recall':rate(counts['TP'],positives),
        'accepted_normal_fpr':rate(counts['FP'],accepted_normals),
        'false_flags_all_normals':rate(counts['FP'],negatives),
        'precision':rate(counts['TP'],counts['TP']+counts['FP']),
        'coverage':rate(len(y),len(labels)),
        'anomaly_coverage':rate(accepted_anomalies,positives),'normal_coverage':rate(accepted_normals,negatives),
        'observed_prevalence':rate(positives,len(labels)),'ranking_scored_only':ranking}
