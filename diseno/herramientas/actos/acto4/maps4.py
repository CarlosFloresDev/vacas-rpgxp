"""Alcantarillas compactas: volumen construido, corredores, agua no transitable."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import random,json
MAPAS=[(17,'Colector: la ultima escalera',20,15),(18,'Tuneles: nombres sin collar',22,15),(19,'Canal de retorno',20,15),(20,'La camara de la manada',20,15),(21,'Altar de las cosas salvadas',20,15)]
def crear():return [['create_map',dict(name=n,width=w,height=h,tilesetId=68,parentId=15,purpose='interior')] for mid,n,w,h in MAPAS]
def grid(mid,w,h):
    r=random.Random(mid);z=[[[399]*w for y in range(h)],[[0]*w for y in range(h)],[[0]*w for y in range(h)]]
    floor=set()
    def room(x1,y1,x2,y2):
        for y in range(y1,y2+1):
            for x in range(x1,x2+1):floor.add((x,y))
    if mid==17:
        room(3,8,8,12);room(5,5,16,8);room(10,9,14,11);room(14,4,17,6)
    if mid==18:
        room(2,9,18,12);room(3,4,6,10);room(5,3,18,5);room(15,5,18,11);room(8,5,11,10);room(11,6,15,8)
    if mid==19:
        room(2,9,17,12);room(3,4,6,10);room(5,4,16,6);room(12,6,17,10);room(7,7,10,10)
    if mid==20:
        room(3,9,17,12);room(4,4,16,9);room(3,6,6,10)
    if mid==21:
        room(3,8,16,11);room(5,4,12,9);room(12,5,16,7)
    for x,y in floor:
        z[0][y][x]=384+r.choices([0,1,2,3],[5,3,2,1])[0]
    # Fachadas de ladrillo: dos alturas visibles, roca negra detras.
    for x,y in sorted(floor,key=lambda p:p[1]):
        if (x,y-1) not in floor and y>1:
            z[0][y-1][x]=390
            if (x,y-2) not in floor:z[0][y-2][x]=389
    # Cuencas reales entre las pasarelas, nunca un suelo azul transitable.
    pools={17:[(9,9),(9,10)],18:[(12,9),(13,9),(14,9),(12,8),(13,8)],19:[(8,4),(9,4),(10,4),(8,5),(9,5),(10,5),(7,11),(8,11),(9,11),(10,11)],20:[(8,7),(9,7),(10,7),(11,7),(12,7),(8,8),(9,8),(10,8),(11,8),(12,8)],21:[]}
    for x,y in pools[mid]:
        if (x,y) in floor:z[0][y][x]=391;floor.remove((x,y))
    # Detalle incrustado en suelo: papeles, limo, paja y huellas sin bloquear ruta.
    for x,y in floor:
        if r.random()<.22:z[1][y][x]=r.choice([397,398,392])
        if (x+1,y) not in floor and r.random()<.38:z[2][y][x]=394
    return z
def pintura():return [['set_map_tiles',dict(mapId=mid,layer=l,x=0,y=0,grid=g)] for mid,n,w,h in MAPAS for l,g in enumerate(grid(mid,w,h))]
if __name__=='__main__':
    import sys
    json.dump(crear() if 'crear' in sys.argv else pintura(),open(str(_ROOT / 'diseno/archivo/lotes/b_mapas4.json'),'w',encoding='utf-8'),ensure_ascii=False)
