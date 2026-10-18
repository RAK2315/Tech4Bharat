"""Small fictional ledger. No claims about physical provenance or factory behavior."""
class Ledger:
 def __init__(self,ids):
  if len(set(ids))!=len(ids):raise ValueError('Duplicate product identifiers')
  self.products={i:{'photos':[],'current':None,'inspections':0} for i in ids};self.photos={};self.events=[];self.duplicates=0;self.owner=None
 def product(self,ident):
  if ident not in self.products:raise ValueError('Unknown product')
  if self.owner:raise ValueError('Approved ledger is immutable; create amendment')
  return self.products[ident]
 def photo(self,ident,digest):
  p=self.product(ident)
  if digest in self.photos:
   if self.photos[digest]!=ident:raise ValueError('Same photo assigned to another product')
   self.duplicates+=1;self.events.append({'type':'duplicate_photo','product':ident});return
  self.photos[digest]=ident;p['photos'].append(digest);self.events.append({'type':'photo','product':ident,'hash':digest})
 def inspect(self,ident,decision,reviewer):
  p=self.product(ident)
  if not p['photos']:raise ValueError('Inspection needs photo evidence')
  if decision not in ['acceptable','defective','cannot_determine'] or not reviewer:raise ValueError('Explicit human decision/reviewer required')
  p['current']=decision;p['inspections']+=1;self.events.append({'type':'inspection','product':ident,'decision':decision,'reviewer':reviewer})
 def rework(self,ident):
  p=self.product(ident)
  if p['current']!='defective':raise ValueError('Only confirmed defective products enter this rework fixture')
  p['current']='awaiting_reinspection';self.events.append({'type':'rework','product':ident})
 def approve(self,owner):
  if not owner or self.counts()['completed_current']!=len(self.products):raise ValueError('Uninspected/unresolved products block approval')
  self.owner=owner;self.events.append({'type':'approval','owner':owner})
 def counts(self):
  ps=list(self.products.values());ev=[e for e in self.events if e['type']=='inspection']
  return {'products':len(ps),'unique_photos':len(self.photos),'duplicate_uploads':self.duplicates,'inspection_events':len(ev),'unique_inspected':sum(p['inspections']>0 for p in ps),'completed_current':sum(p['current'] in ['acceptable','defective'] for p in ps),'current_acceptable':sum(p['current']=='acceptable' for p in ps),'current_defective':sum(p['current']=='defective' for p in ps),'unresolved':sum(p['current']=='cannot_determine' for p in ps),'uninspected':sum(p['inspections']==0 for p in ps),'awaiting_reinspection':sum(p['current']=='awaiting_reinspection' for p in ps),'historical_defect_events':sum(e['decision']=='defective' for e in ev)}
def fixture():
 l=Ledger(list('ABCDEF'))
 for ident in 'ABCDE':l.photo(ident,'fictional-'+ident+'-v1')
 l.photo('A','fictional-A-v1');l.inspect('A','acceptable','FICTIONAL reviewer')
 l.inspect('B','defective','FICTIONAL reviewer');l.rework('B');l.photo('B','fictional-B-v2');l.inspect('B','acceptable','FICTIONAL reviewer')
 l.inspect('C','cannot_determine','FICTIONAL reviewer');l.inspect('D','defective','FICTIONAL reviewer')
 return l
