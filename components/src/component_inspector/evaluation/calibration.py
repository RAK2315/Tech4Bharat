"""Normal-only rank calibration and fixed equal-image display scaling."""
import math
import numpy as np


def calibrate(scores, alpha=.10):
    values=np.asarray(scores,dtype=np.float64)
    if values.ndim!=1 or not np.isfinite(values).all() or not 0<alpha<1:
        raise ValueError('Invalid calibration scores/alpha')
    n=len(values); k=math.ceil((1-alpha)*(n+1))
    if not n or k>n:
        raise ValueError('insufficient normal calibration samples')
    threshold=float(np.sort(values)[k-1])
    return {'threshold':threshold,'alpha':alpha,'n':n,'k':k,
            'comparison':'strict_greater','ties_at_threshold':int((values==threshold).sum()),
            'empirical_fpr':float((values>threshold).mean())}


def flag(score, record):
    if not np.isfinite(score) or not np.isfinite(record['threshold']):
        raise ValueError('Nonfinite score/threshold')
    return bool(score>record['threshold'])


def display_scale(valid_pixel_maps, seed=4217):
    rng=np.random.default_rng(seed);samples=[];weights=[]
    for pixels in valid_pixel_maps:
        values=np.asarray(pixels,dtype=np.float32).reshape(-1)
        if not len(values) or not np.isfinite(values).all() or values.min()<0:
            raise ValueError('Invalid calibration map')
        if len(values)>10000:
            values=values[rng.choice(len(values),10000,replace=False)]
        samples.append(values);weights.append(np.full(len(values),1/len(values)))
    if not samples:raise ValueError('No calibration maps')
    values=np.concatenate(samples);w=np.concatenate(weights)
    order=np.argsort(values,kind='stable');values=values[order];w=w[order]
    chosen=min(len(values)-1,int(np.searchsorted(np.cumsum(w),.995*w.sum(),side='left')))
    maximum=float(values[chosen]);degenerate=maximum<=1e-8
    return {'minimum':0.0,'maximum':max(maximum,1e-8),'degenerate':degenerate,
            'percentile':99.5,'weighting':'equal_image','pixel_sample_cap_per_image':10000,
            'seed':seed,'label':'anomaly intensity - not probability or severity'}
