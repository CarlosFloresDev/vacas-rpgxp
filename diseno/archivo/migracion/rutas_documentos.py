"""Actualiza también referencias de archivo escritas como código en Markdown."""
from pathlib import Path
import json,re,os,collections
root=next(p for p in Path(__file__).resolve().parents if (p/'Game.rxproj').exists())
mapping=json.loads((root/'diseno/verificaciones/traslados.json').read_text(encoding='utf8'))
old_of={v:k for k,v in mapping.items()}
by_name=collections.defaultdict(list)
for old,new in mapping.items():by_name[Path(old).name].append(new)
for p in (root/'diseno').rglob('*.md'):
    if any(n in p.parts for n in ('respaldos','archivo')) or p.name in ('ORGANIZACION.md',) or p==root/'diseno/README.md':continue
    original=p.read_text(encoding='utf8')
    old=old_of.get(p.relative_to(root).as_posix(),p.relative_to(root).as_posix())
    def replace(match):
        value=match[1]
        if '\n' in value or ' ' in value:return match[0]
        if value.startswith('diseno/capturas/') and len(Path(value).parts)==3:
            name=Path(value).name;theme='actos' if name.startswith(('acto','mapa')) else 'interfaz' if name.startswith('ui_') else 'arte'
            return '`diseno/capturas/'+theme+'/'+name+'`'
        dest=Path(os.path.abspath((root/old).parent/value))
        key=dest.relative_to(root).as_posix() if dest.is_relative_to(root) else ''
        new=mapping.get(key) or mapping.get('diseno/'+value)
        if not new and '/' not in value and len(by_name[value])==1:new=by_name[value][0]
        if new and (root/new).exists():return '`'+Path(os.path.relpath(root/new,p.parent)).as_posix()+'`'
        if value.startswith('capturas/'):
            name=value.removeprefix('capturas/');theme='interfaz' if name.startswith('ui_') else 'actos' if name.startswith(('acto','mapa')) else 'arte'
            return '`'+Path(os.path.relpath(root/'diseno/capturas'/theme/name,p.parent)).as_posix()+'`'
        return match[0]
    result=re.sub(r'`([^`\n]+)`',replace,original)
    if result!=original:p.write_text(result,encoding='utf8',newline='')
print('Referencias en código Markdown actualizadas.')
