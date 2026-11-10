"""Render de los cinco mapas con eventos y máscaras idénticas al juego."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parent;ROOT=_ROOT;CAP=ROOT/'diseno/capturas/actos'
ops=[['render_map',dict(mapId=i,drawEvents=True,outPath=str(CAP/('acto6_%d_base.png'%i)))] for i in range(28,33)]
((_ROOT / 'diseno/archivo/lotes/b_render6.json')).write_text(json.dumps(ops),encoding='utf8')
r=subprocess.run(['node',str(_ROOT / 'diseno/herramientas/comun/rx.mjs'),'--batch',str(_ROOT / 'diseno/archivo/lotes/b_render6.json')],cwd=BASE,capture_output=True,text=True,encoding='utf8')
((_ROOT / 'diseno/verificaciones/herramientas/render_acto6.log')).write_text(r.stdout+r.stderr,encoding='utf8')
if r.returncode:raise SystemExit(r.stderr)
sheet=Image.new('RGB',(1280,1440),'#151917')
for n,i in enumerate(range(28,33)):
    a=Image.open(CAP/('acto6_%d_base.png'%i)).convert('RGBA')
    a.alpha_composite(Image.open(ROOT/'Graphics/Pictures'/('acto6_luz%02d.png'%i)))
    a.convert('RGB').save(CAP/('acto6_%d.png'%i))
    sheet.paste(a.convert('RGB'),((n%2)*640,(n//2)*480))
sheet.save(CAP/'acto6_lamina.png')
print('5 capturas y lámina listas.')
