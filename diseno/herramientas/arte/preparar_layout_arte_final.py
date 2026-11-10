
# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import sys,json,random,copy
from pathlib import Path
from PIL import Image,ImageDraw
sys.path.insert(0,'diseno/herramientas')
import maps5 as m
v=copy.deepcopy(m.M)
k=set(p[1] for a in v.values() for p in a['props'])
import maps6
k.update(p[1] for a in m.M.values() for p in a['props'])
k=sorted(k-set(['carcass0','carcass1','carcass2','hook','panelreloj','bucket','meatbox','dung','note','bottles','meat','tile:rail','tile:rail_gancho','tile:lampara','bed','cabinet','stove','tv']))
out=Path('diseno/fuentes/arte_hd2d/arte_final')
(out/'props_indices.json').write_text(json.dumps(k,indent=2),encoding='utf8')
for page in range((len(k)+15)//16):
 im=Image.new('RGBA',(768,768));d=ImageDraw.Draw(im)
 for n,kind in enumerate(k[page*16:(page+1)*16]):
  a=m.draw(kind,random.Random(0));a.thumbnail((160,160),Image.Resampling.NEAREST)
  if max(a.size)<150:a=a.resize((a.width*min(3,150//max(a.size)),a.height*min(3,150//max(a.size))),Image.Resampling.NEAREST)
  x=n%4*192;y=n//4*192
  im.alpha_composite(a,(x+(192-a.width)//2,y+(192-a.height)//2))
 im.save(out/f'props_layout_{page}.png')
print(k)

