"""Download only pinned public PCB1 mirror files, original metadata and official weights."""
from pathlib import Path
import urllib.request, hashlib, json, time

ROOT = Path(__file__).resolve().parent
REV = 'd185c42584b49f1df81fe12bde627559ed88d483'
FILES = {
 'data/pcb1.train.parquet': f'https://huggingface.co/datasets/BrachioLab/visa/resolve/{REV}/data/pcb1.train-00000-of-00001.parquet',
 'data/pcb1.test.parquet': f'https://huggingface.co/datasets/BrachioLab/visa/resolve/{REV}/data/pcb1.test-00000-of-00001.parquet',
 'data/mirror_README.md': f'https://huggingface.co/datasets/BrachioLab/visa/raw/{REV}/README.md',
 'data/original_id2class.py.txt': 'https://raw.githubusercontent.com/amazon-science/spot-diff/main/utils/id2class.py',
 'data/original_README.md': 'https://raw.githubusercontent.com/amazon-science/spot-diff/main/README.md',
 'models/resnet18-f37072fd.pth': 'https://download.pytorch.org/models/resnet18-f37072fd.pth',
}
manifest=[]
for name,url in FILES.items():
 p=ROOT/name; p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():
  print('Downloading',name,flush=True)
  for attempt in range(3):
   try:
    with urllib.request.urlopen(url,timeout=120) as r, p.with_suffix(p.suffix+'.part').open('wb') as out:
     while chunk:=r.read(1024*1024): out.write(chunk)
    p.with_suffix(p.suffix+'.part').replace(p); break
   except Exception:
    if attempt==2: raise
    time.sleep(2)
 digest=hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
 if 'resnet18' in name: assert digest.startswith('f37072fd'),digest
 manifest.append({'path':name,'url':url,'bytes':p.stat().st_size,'sha256':digest})
 print(name,p.stat().st_size,digest[:12],flush=True)
(ROOT/'data/download_manifest.json').write_text(json.dumps(manifest,indent=2))
