"""Última pasada de la migración (histórico, no ejecutar de nuevo)."""
from pathlib import Path
import json,re,os
root=next(p for p in Path(__file__).resolve().parents if (p/'Game.rxproj').exists())
m=json.loads((root/'diseno/verificaciones/traslados.json').read_text(encoding='utf8'))
scripts={Path(k).name:Path(v).name for k,v in m.items() if k.startswith('diseno/scripts/')}
pat=re.compile('|'.join(map(re.escape,scripts)))
old_of={v:k for k,v in m.items()}
for p in (root/'diseno').rglob('*'):
    if not p.is_file() or any(x in p.parts for x in ['respaldos','archivo','__pycache__']) or p.suffix not in ['.py','.mjs','.rb','.md']:continue
    if p.parent.name=='scripts':continue
    text=p.read_text(encoding='utf-8-sig');text=pat.sub(lambda x:scripts[x[0]],text)
    if p.suffix=='.mjs':
        text=re.sub(r'new URL\((_ruta\([^)]*\)),\s*import.meta.url\)',r'\1',text)
        text=text.replace("new URL(process.argv[2] || _ruta('diseno/herramientas/comun/prueba_interfaz.rb'),import.meta.url)","(process.argv[2] ? new URL(process.argv[2],import.meta.url) : _ruta('diseno/herramientas/comun/prueba_interfaz.rb'))")
    if p.suffix=='.md':
        old=old_of.get(p.relative_to(root).as_posix(),p.relative_to(root).as_posix())
        def inline(match):
            value=match[1]
            if value.startswith(('../','./')) and ' ' not in value:
                dest=Path(os.path.abspath((root/old).parent/value))
                if dest.is_relative_to(root):
                    key=dest.relative_to(root).as_posix();dest=root/m.get(key,key)
                    if dest.exists():return '`'+Path(os.path.relpath(dest,p.parent)).as_posix()+'`'
            return match[0]
        text=re.sub(r'`([^`\n]+)`',inline,text)
    p.write_text(text,encoding='utf8',newline='')
print('Nombres Ruby y URL de las herramientas ajustados')
