"""Build auditable splits without consulting model outputs."""
from inspection import *
import pyarrow.parquet as pq
from collections import Counter,defaultdict

(ROOT/'data/images').mkdir(exist_ok=True)
(ROOT/'data/masks').mkdir(exist_ok=True)
records=[];thumbs=[];hashes=[]
for partition in ['train','test']:
 table=pq.read_table(ROOT/f'data/pcb1.{partition}.parquet')
 for ix,r in enumerate(table.to_pylist()):
  ident=f'{partition}_{ix:04d}';b=r['image']['bytes'];im=Image.open(io.BytesIO(b)).convert('RGB')
  path=f'data/images/{ident}.jpg';(ROOT/path).write_bytes(b)
  mask=None;values=[]
  if r['mask'] and r['mask']['bytes']:
   mask=f'data/masks/{ident}.png';(ROOT/mask).write_bytes(r['mask']['bytes']);values=np.unique(np.array(Image.open(io.BytesIO(r['mask']['bytes'])))).tolist()
  records.append({'id':ident,'source_partition':partition,'source_filename':r['image']['path'],'label':int(r['label']),'image':path,'mask':mask,'mask_values':values,'width':im.width,'height':im.height,'file_sha256':sha(b),'pixel_sha256':sha(str(im.size).encode()+np.array(im).tobytes())})
  thumbs.append(np.array(im.resize((64,64),Image.Resampling.BILINEAR),dtype=np.float32)/255);hashes.append(phash(im))
assert all(r['label']==0 for r in records if r['source_partition']=='train')
n=len(records);parent=list(range(n));pairs=[]
def find(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
def union(i,j):parent[find(j)]=find(i)
for i in range(n):
 for j in range(i):
  exact=records[i]['pixel_sha256']==records[j]['pixel_sha256']
  if exact or ((hashes[i]^hashes[j]).bit_count()<=2 and np.abs(thumbs[i]-thumbs[j]).mean()<=2/255):
   union(i,j);pairs.append({'a':records[j]['id'],'b':records[i]['id'],'exact':exact})
groups=defaultdict(list)
for i,r in enumerate(records):groups[find(i)].append(r)
train=[];bad=[];normal=[];excluded=[]
for members in groups.values():
 key=min(r['pixel_sha256'] for r in members);gid=sha(f'{SEED}:{key}'.encode())
 for r in members:r['group']=gid
 if len({r['label'] for r in members})>1:
  excluded.extend([{**r,'reason':'appearance_group_label_conflict'} for r in members]);continue
 tr=[r for r in members if r['source_partition']=='train']
 if tr:
  tr.sort(key=lambda r:r['id']);train.append(tr[0]);excluded.extend([{**r,'reason':'duplicate_group_reference_canonical'} for r in members if r['id']!=tr[0]['id']])
 else:
  members.sort(key=lambda r:r['id']);(bad if members[0]['label'] else normal).append(members[0]);excluded.extend([{**r,'reason':'duplicate_group_test_canonical'} for r in members[1:]])
train.sort(key=lambda r:r['group']);bad.sort(key=lambda r:r['group']);normal.sort(key=lambda r:r['group'])
assert len(train)>=200 and len(bad)>20
splits={'reference':train[:100],'calibration':train[100:200]+bad[:20],'test':normal+bad[20:],'unused':train[200:],'quarantined':excluded}
for key in ['reference','calibration','test']:
 for r in splits[key]:r['split']=key
sets=[{r['group'] for r in splits[k]} for k in ['reference','calibration','test']]
assert all(not sets[i]&sets[j] for i in range(3) for j in range(i))
dump('data/splits.json',splits);dump('data/all_records.json',records)
audit={'source_counts':dict(Counter(r['source_partition']+':'+str(r['label']) for r in records)),
 'split_counts':{k:dict(Counter(str(r['label']) for r in v)) for k,v in splits.items()},'duplicate_pairs':pairs,'quarantined':len(excluded),
 'physical_product_ids':'Unavailable. Filename is not a verified unique physical board identifier; physical-instance leakage remains possible.',
 'mask_values':sorted(set(v for r in records for v in r['mask_values'])),'protocol_sha256':sha((ROOT/'PROTOCOL.md').read_bytes()),'split_sha256':sha((ROOT/'data/splits.json').read_bytes())}
dump('results/leakage_audit.json',audit)
print(json.dumps(audit,indent=2),flush=True)
# Only reference images shown before inference. No final-test visual tuning.
sheet=Image.new('RGB',(5*224,2*224),'white')
for i,r in enumerate(splits['reference'][:10]):sheet.paste(get_image(r).resize((224,224)),((i%5)*224,(i//5)*224))
sheet.save(ROOT/'results/reference_contact_sheet.jpg')
