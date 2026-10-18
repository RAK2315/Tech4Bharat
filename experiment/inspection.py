"""Frozen CPU reference matching / compact PaDiM implementation. No online services."""
import os
os.environ.setdefault('OMP_NUM_THREADS','4')
os.environ.setdefault('MKL_NUM_THREADS','4')
from pathlib import Path
import hashlib, io, json, time
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import torch
from torch import nn
import torch.nn.functional as F
from torchvision.models import resnet18

ROOT=Path(__file__).resolve().parent
torch.set_num_threads(4)
torch.set_num_interop_threads(1)
cv2.setNumThreads(1)
SEED=4217
SIZE=224

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(path,obj):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(obj,indent=2,allow_nan=False),encoding='utf-8')
def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def rgb(im): return np.array(im.convert('RGB').resize((SIZE,SIZE),Image.Resampling.BILINEAR)).astype(np.float32)/255
def tensor(a): return torch.from_numpy(a.transpose(2,0,1).copy()).unsqueeze(0)
def quality(im):
 a=rgb(im); gray=cv2.cvtColor((a*255).round().astype(np.uint8),cv2.COLOR_RGB2GRAY)
 luma=gray.astype(np.float32)/255
 vals={'min_side':min(im.size),'luma_mean':float(luma.mean()),'clipped_fraction':float(((luma<.01)|(luma>.99)).mean()),'laplacian_variance':float(cv2.Laplacian(gray,cv2.CV_64F).var())}
 reasons=[]
 if vals['min_side']<224:reasons.append('image_too_small')
 if not .05<=vals['luma_mean']<=.95:reasons.append('mean_exposure')
 if vals['clipped_fraction']>.5:reasons.append('clipping')
 if vals['laplacian_variance']<20:reasons.append('blur')
 return not reasons,reasons,vals
def phash(im):
 g=np.array(im.convert('L').resize((32,32),Image.Resampling.BILINEAR),dtype=np.float32)
 d=cv2.dct(g)[:8,:8].reshape(-1); bits=d>np.median(d[1:]); bits[0]=False
 return sum(int(v)<<i for i,v in enumerate(bits))

class Features(nn.Module):
 def __init__(self,weights=True):
  super().__init__(); r=resnet18(weights=None)
  if weights:r.load_state_dict(torch.load(ROOT/'models/resnet18-f37072fd.pth',map_location='cpu',weights_only=True))
  self.stem=nn.Sequential(r.conv1,r.bn1,r.relu,r.maxpool)
  self.l1=r.layer1;self.l2=r.layer2;self.l3=r.layer3
  self.register_buffer('mean',torch.tensor([.485,.456,.406])[None,:,None,None])
  self.register_buffer('std',torch.tensor([.229,.224,.225])[None,:,None,None])
  self.register_buffer('channels',torch.tensor(np.random.default_rng(SEED).choice(448,50,replace=False)))
 def forward(self,x):
  a=self.l1(self.stem((x-self.mean)/self.std));b=self.l2(a);c=self.l3(b)
  e=torch.cat([a,F.interpolate(b,size=(56,56),mode='nearest'),F.interpolate(c,size=(56,56),mode='nearest')],dim=1)
  return e.index_select(1,self.channels)

class Padim(nn.Module):
 def __init__(self,features=None):
  super().__init__(); self.features=features if features is not None else Features()
  self.register_buffer('mu',torch.zeros(3136,50))
  self.register_buffer('inv',torch.zeros(3136,50,50))
  k=torch.arange(-12,13,dtype=torch.float32);g=torch.exp(-k*k/(2*4**2));g=g/g.sum()
  self.register_buffer('kernel_x',g[None,None,None,:]);self.register_buffer('kernel_y',g[None,None,:,None])
 def embed(self,x): return self.features(x).flatten(2).permute(0,2,1)
 def forward(self,x):
  d=self.embed(x)-self.mu[None]
  z=torch.einsum('bpd,pde,bpe->bp',d,self.inv,d).clamp_min(0).sqrt().reshape(-1,1,56,56)
  z=F.interpolate(z,size=(224,224),mode='bilinear',align_corners=False)
  z=F.conv2d(F.pad(z,(12,12,0,0),mode='reflect'),self.kernel_x)
  z=F.conv2d(F.pad(z,(0,0,12,12),mode='reflect'),self.kernel_y)
  return z.flatten(1).max(1).values,z
 @torch.inference_mode()
 def fit(self,arrays):
  e=torch.cat([self.embed(torch.cat([tensor(a) for a in arrays[i:i+8]])) for i in range(0,len(arrays),8)])
  mu=e.mean(0);d=e-mu[None];xp=d.permute(1,2,0)
  cov=torch.bmm(xp,xp.transpose(1,2))/(len(e)-1)+.01*torch.eye(50)[None]
  self.mu.copy_(mu);self.inv.copy_(torch.linalg.inv(cov));self.eval()

class Reference:
 def __init__(self,arrays):self.bank=np.stack([self.norm(a) for a in arrays])
 @staticmethod
 def norm(a): return a-a.mean((0,1),keepdims=True)+.5
 def predict(self,a):
  x=self.norm(a);res=((self.bank-x[None])**2).mean(3)
  ix=int(np.argmin(res.mean((1,2))))
  m=cv2.GaussianBlur(res[ix],(0,0),1)
  s=float(np.sort(m.reshape(-1))[-max(1,int(m.size*.01)):].mean())
  return s,m

def threshold(rows):
 valid=[r for r in rows if r['accepted']]
 assert any(r['label']==0 for r in valid) and any(r['label']==1 for r in valid)
 scores=sorted(set(r['score'] for r in valid)); candidates=[float(np.nextafter(scores[0],-np.inf))]+scores
 n=sum(r['label']==0 for r in valid);p=sum(r['label']==1 for r in valid)
 choices=[]
 for t in candidates:
  fp=sum(r['label']==0 and r['score']>t for r in valid);tp=sum(r['label']==1 and r['score']>t for r in valid)
  if fp/n<=.1:choices.append((tp/p,-fp,t))
 return max(choices)[2]

def wilson(k,n):
 if n==0:return None
 z=1.96;p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return [float(max(0,center-half)),float(min(1,center+half))]
def rate(k,n):return {'numerator':int(k),'denominator':int(n),'rate':float(k/n) if n else None,'wilson95':wilson(k,n)}
def metrics(rows):
 tp=sum(r['label']==1 and r['decision']=='flag' for r in rows);fp=sum(r['label']==0 and r['decision']=='flag' for r in rows)
 p=sum(r['label']==1 for r in rows);n=len(rows)-p
 ap=sum(r['label']==1 and r['accepted'] for r in rows);an=sum(r['label']==0 and r['accepted'] for r in rows)
 times=[r['milliseconds'] for r in rows]; accepted_times=[r['milliseconds'] for r in rows if r['accepted']]
 recall=rate(tp,p);fpr=rate(fp,an);coverage=rate(ap+an,len(rows))
 result={'count':len(rows),'defects':p,'normals':n,'TP':tp,'FN_unflagged_accepted':ap-tp,'FN_abstained':p-ap,'FP':fp,'TN':an-fp,'abstained_normals':n-an,
 'recall_all_defects':recall,'recall_accepted_defects':rate(tp,ap),'fpr_accepted_normals':fpr,'fp_all_normals':rate(fp,n),'precision_observed':rate(tp,tp+fp),
 'observed_prevalence':rate(p,len(rows)),'coverage':coverage,'retake_requests':len(rows)-ap-an,
 'latency_ms':{'median':float(np.median(times)) if times else None,'p95':float(np.percentile(times,95)) if times else None,'accepted_p95':float(np.percentile(accepted_times,95)) if accepted_times else None,'total_processing_seconds':sum(times)/1000},
 'human_review_time':'UNMEASURED; timed exercise pending','capture_time':'UNMEASURED','total_inspection_time':'UNMEASURED'}
 result['provisional_screen_pass']=bool(recall['rate'] is not None and recall['rate']>=.9 and fpr['rate'] is not None and fpr['rate']<=.1 and coverage['rate'] is not None and coverage['rate']>=.9 and accepted_times and np.percentile(accepted_times,95)<=5000)
 return result

def get_image(row):return Image.open(ROOT/row['image']).convert('RGB')
@torch.inference_mode()
def evaluate(model,rows,method,t=None,stress=None,save_maps=False):
 output=[]
 for r in rows:
  start=time.perf_counter(); im=get_image(r)
  if stress=='brightness_0.6':im=ImageEnhance.Brightness(im).enhance(.6)
  elif stress=='brightness_1.4':im=ImageEnhance.Brightness(im).enhance(1.4)
  elif stress=='blur_2.0':im=im.filter(ImageFilter.GaussianBlur(2))
  ok,reasons,q=quality(im);s=None;m=None
  if ok:
   a=rgb(im)
   if method=='reference':s,m=model.predict(a)
   else:
    score,am=model(tensor(a));s=float(score[0]);m=am[0,0].numpy()
  elapsed=(time.perf_counter()-start)*1000
  o={**r,'method':method,'stress':stress,'accepted':ok,'quality_reasons':reasons,'quality':q,'score':s,'milliseconds':elapsed,'decision':'retake' if not ok else ('unthresholded' if t is None else ('flag' if s>t else 'no_flag'))}
  output.append(o)
  if save_maps and m is not None:np.save(ROOT/'results/maps'/f"{method}_{r['id']}.npy",m)
 return output
