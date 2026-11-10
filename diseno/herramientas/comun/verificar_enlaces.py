"""Comprueba destinos y anclas Markdown locales; no modifica documentos."""
from pathlib import Path
from urllib.parse import unquote
import re, json, unicodedata
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'Game.rxproj').exists())

def slug(text):
    text = re.sub(r'[`*_]', '', text).strip().lower()
    return ''.join(c for c in text if c.isalnum() or c in ' _-').replace(' ', '-')

def comprobar():
    errors=[]; count=0; documents=0
    for p in ROOT.rglob('*.md'):
        if any(x in p.parts for x in ('.git','respaldos','.mcp-backup','archivo')): continue
        documents+=1
        text=p.read_text(encoding='utf-8-sig')
        text=re.sub(r'```.*?```','',text,flags=re.S)
        references=dict(re.findall(r'^\s*\[([^\]]+)\]:\s*(\S+)',text,re.M))
        targets=re.findall(r'!?\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)',text)
        targets += [references[key] for _,key in re.findall(r'(!?\[[^\]]*\])\[([^\]]+)\]',text) if key in references]
        for target in targets:
            target=unquote(target.strip('<>'))
            if re.match(r'\w+:|//',target):continue
            name,_,anchor=target.partition('#');count+=1
            dest=(ROOT/name.lstrip('/')) if name.startswith('/') else p.parent/name if name else p
            if not dest.exists():errors.append({'documento':str(p.relative_to(ROOT)),'destino':target,'error':'no existe'})
            elif anchor and dest.suffix.lower()=='.md':
                headings=re.findall(r'^#{1,6}\s+(.+?)\s*#*$',dest.read_text(encoding='utf-8-sig'),re.M)
                ids=[]
                for heading in headings:
                    base=slug(heading);n=ids.count(base);ids.append(base if not n else base+'-'+str(n))
                if anchor not in ids and not re.search(r'(?:id|name)=[\"\']'+re.escape(anchor),dest.read_text(encoding='utf-8-sig')):
                    errors.append({'documento':str(p.relative_to(ROOT)),'destino':target,'error':'ancla ausente'})
    return {'documentos':documents,'enlaces':count,'errores':errors,'excluidos':'Respaldos y archivo: documentos históricos, conservados tal cual.'}

if __name__=='__main__':
    result=comprobar();print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(result['errores']))
