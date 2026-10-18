"""Local-only static artifacts and a fixed browser-results sink; not an application."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def do_POST(self):
  if self.path!='/browser-results':self.send_error(404);return
  size=int(self.headers.get('Content-Length','0'))
  if size>1000000:self.send_error(413);return
  value=json.loads(self.rfile.read(size));(ROOT/'results/browser_results.json').write_text(json.dumps(value,indent=2),encoding='utf-8');self.send_response(200);self.end_headers();self.wfile.write(b'ok')
if __name__=='__main__':
 print('Local experiment: http://127.0.0.1:8765/artifacts/review_exercise.html',flush=True)
 ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
