"""One frozen experiment run. Do not change settings after inspecting final errors."""
from inspection import *
import platform,importlib.metadata,subprocess

def main():
 start=time.perf_counter();splits=load('data/splits.json')
 (ROOT/'results/maps').mkdir(parents=True,exist_ok=True)
 init=time.perf_counter(); refs=[rgb(get_image(r)) for r in splits['reference']]
 reference=Reference(refs); reference_fit=time.perf_counter()-init
 init=time.perf_counter();padim=Padim().eval();init_seconds=time.perf_counter()-init
 fit=time.perf_counter();padim.fit(refs);padim_fit=time.perf_counter()-fit
 torch.save(padim.state_dict(),ROOT/'models/padim.pt');np.save(ROOT/'models/reference_bank.npy',reference.bank)
 allresults={};thresholds={};summary={}
 # Calibration is complete and thresholds persisted before any test inference.
 for method,model in [('reference',reference),('padim',padim)]:
  for _ in range(3):
   if method=='reference':model.predict(refs[0])
   else:
    with torch.inference_mode():model(tensor(refs[0]))
  rows=evaluate(model,splits['calibration'],method)
  t=threshold(rows);thresholds[method]=t
  for r in rows:
   if r['accepted']:r['decision']='flag' if r['score']>t else 'no_flag'
  dump(f'results/{method}_calibration.json',rows)
  summary[method]={'calibration':metrics(rows)}
 dump('results/frozen_thresholds.json',{'thresholds':thresholds,'protocol_sha256':sha((ROOT/'PROTOCOL.md').read_bytes()),'split_sha256':sha((ROOT/'data/splits.json').read_bytes())})
 print('Thresholds frozen',thresholds,flush=True)
 for method,model in [('reference',reference),('padim',padim)]:
  print('Evaluating',method,flush=True)
  rows=evaluate(model,splits['test'],method,thresholds[method],save_maps=True)
  dump(f'results/{method}_test.json',rows);summary[method]['test']=metrics(rows)
  summary[method]['synthetic_stress']={}
  for stress in ['brightness_0.6','brightness_1.4','blur_2.0']:
   r=evaluate(model,splits['test'],method,thresholds[method],stress=stress)
   dump(f'results/{method}_{stress}.json',r);summary[method]['synthetic_stress'][stress]=metrics(r)
  print(method,json.dumps(summary[method]['test']),flush=True)
 versions={k:importlib.metadata.version(k) for k in ['torch','torchvision','numpy','pillow','scipy','opencv-python-headless','onnx','onnxruntime','pyarrow']}
 dump('results/environment.json',{'python':platform.python_version(),'platform':platform.platform(),'processor':platform.processor(),'logical_cpus':os.cpu_count(),'device':'CPU','torch_threads':torch.get_num_threads(),'packages':versions,'reference_fit_seconds':reference_fit,'padim_initialization_seconds':init_seconds,'padim_fit_seconds':padim_fit,'run_total_seconds':time.perf_counter()-start,'protocol_sha256':sha((ROOT/'PROTOCOL.md').read_bytes())})
 dump('results/summary.json',summary)
 # Export the SAME fitted model including normalisation, Gaussian parameters, scoring and map.
 export=time.perf_counter()
 try:
  torch.onnx.export(padim,tensor(refs[0]),str(ROOT/'models/padim.onnx'),input_names=['rgb'],output_names=['score','map'],opset_version=17,dynamo=False)
  import onnxruntime as ort
  options=ort.SessionOptions();options.intra_op_num_threads=4
  session=ort.InferenceSession(str(ROOT/'models/padim.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
  selected=splits['test'][:5]+[r for r in splits['test'] if r['label']][:5]
  fixtures=[]
  for r in selected:
   a=rgb(get_image(r));x=tensor(a)
   with torch.inference_mode():ps,pm=padim(x)
   ts=time.perf_counter();outs=session.run(None,{'rgb':x.numpy()});ms=(time.perf_counter()-ts)*1000
   fixture={'id':r['id'],'label':r['label'],'shape':list(x.shape),'native_score':float(ps[0]),'onnx_score':float(outs[0][0]),'score_abs_difference':abs(float(ps[0])-float(outs[0][0])),'map_max_abs_difference':float(np.max(np.abs(pm.numpy()-outs[1]))),'onnx_milliseconds':ms,'threshold':thresholds['padim'],'accepted':quality(get_image(r))[0]}
   fixtures.append(fixture)
   x.numpy().astype('<f4').tofile(ROOT/'results'/f"input_{r['id']}.bin")
   get_image(r).save(ROOT/'results'/f"browser_{r['id']}.png")
  dump('results/export_parity.json',{'export_seconds':time.perf_counter()-export,'model_bytes':(ROOT/'models/padim.onnx').stat().st_size,'fixtures':fixtures,'note':'Native ONNX CPU parity, not browser/phone evidence.'})
 except Exception as e:dump('results/export_parity.json',{'error':repr(e)})

if __name__=='__main__':main()
