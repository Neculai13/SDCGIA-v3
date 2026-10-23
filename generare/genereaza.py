"""Optional local request replay. Never overwrites the historical dataset."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request,urlopen

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',required=True)
    parser.add_argument('--limit',type=int,default=1)
    parser.add_argument('--url')
    parser.add_argument('--run',action='store_true')
    args=parser.parse_args()
    if args.limit<1: parser.error('--limit must be positive')
    root=Path(__file__).resolve().parent
    rows=[json.loads(s) for s in (root/'prompturi.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
    selected=[r for r in rows if r['model']==args.model][:args.limit]
    if not selected: parser.error('Model absent; see modele_setari.json')
    for row in selected:
        print(row['id'],row['backend'],row['model'])
        if row['backend']=='chatgpt_web':
            print(row.get('system') or '')
            print(row.get('prompt') or '')
            if args.run: parser.error('Web requests require manual UI use. No numeric sampling parameters are assumed.')
            continue
        options=dict(row.get('request_options') or {})
        if not args.run: continue
        backend=row['backend']
        if backend not in {'ollama','llama.cpp'}: parser.error('Unsupported recorded backend')
        url=args.url or ('http://127.0.0.1:11434' if backend=='ollama' else None)
        if not url: parser.error('Provide --url for llama.cpp')
        parsed=urlparse(url)
        if parsed.scheme!='http' or parsed.hostname not in {'127.0.0.1','localhost','::1'} or parsed.username or parsed.password:
            parser.error('Only a local HTTP server without credentials is accepted')
        if backend=='ollama':
            body={'model':row['model'],'prompt':row['prompt'],'system':row.get('system') or '', 'stream':False,'options':options}
            if row.get('think') is not None: body['think']=row['think']
            route='/api/generate'
        else:
            body=dict(options,model=row['model'],stream=False,messages=[{'role':'system','content':row.get('system') or ''},{'role':'user','content':row['prompt']}])
            route='/v1/chat/completions'
        destination=root/'rezultate_noi'/(hashlib.sha256(row['id'].encode()).hexdigest()[:24]+'.json')
        if destination.exists():
            print('Already exists, skipping:',destination.name);continue
        req=Request(url.rstrip('/')+route,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
        with urlopen(req,timeout=1800) as response: result=json.load(response)
        text=result.get('response','') if backend=='ollama' else result['choices'][0]['message']['content']
        destination.parent.mkdir(exist_ok=True)
        with destination.open('x',encoding='utf-8') as f: json.dump({'request':row,'text':text,'raw_response':result},f,ensure_ascii=False,indent=2)
        print('Saved:',destination.name)

if __name__=='__main__': main()
