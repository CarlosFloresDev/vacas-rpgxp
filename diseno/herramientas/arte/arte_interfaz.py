"""Adaptacion tecnica de las diez fuentes image_gen a RGSS1; no genera arte."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json, shutil, hashlib
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter
ROOT=_ROOT
OUT=ROOT/'diseno/fuentes/arte_hd2d/interfaz'
rows=json.loads((OUT/'generaciones.json').read_text(encoding='utf-8'))
assets=[]
def spec(source,destination,size,**kw):
    assets.append(dict(source=str(source.relative_to(ROOT)).replace('\\','/'),
        destination=destination,type='picture',size=list(size),resample='lanczos',
        preserve_alpha=not kw.get('opaque',False),**kw))
for row in rows:
    dest=OUT/(row['key']+'_fuente.png')
    if not dest.exists(): shutil.copy2(row['source'],dest)
    row['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
    if row['key'] not in ('kit',):
        key='titulo' if row['key']=='title' else row['key']
        folder='Pictures' if key in ('titulo','gameover','menu') else 'Battlebacks'
        spec(dest,f'Graphics/{folder}/ui_{key}.png',(640,480),opaque=True)

kit=Image.open(OUT/'kit_fuente.png').convert('RGBA')
w,h=kit.size
def cell(x,y): return kit.crop((round(x*w/4),round(y*h/4),round((x+1)*w/4),round((y+1)*h/4)))
def save_source(name,im,folder='Pictures',size=None):
    source=OUT/(name+'_tecnico.png'); im.save(source)
    spec(source,f'Graphics/{folder}/{name}.png',size or im.size)
def keyed(im):
    im.putdata([(r,g,b,0 if max(r,g,b)<32 else a) for r,g,b,a in im.getdata()])
    return im
save_source('ui_cursor',keyed(cell(0,1)),size=(16,16))
diamond_glyph=keyed(cell(1,1))
diamond_glyph=diamond_glyph.crop(diamond_glyph.getbbox())
save_source('ui_avance',diamond_glyph,size=(14,14))
save_source('ui_target',diamond_glyph,size=(32,32))
for x,name in [(2,'vida'),(3,'cordura')]:
    im=cell(x,1); im=im.crop((int(im.width*.12),int(im.height*.46),int(im.width*.88),int(im.height*.54)))
    save_source('ui_bar_'+name,im,size=(256,8))
for x,name in [(0,'ui_estado_2'),(1,'ui_estado_3'),(2,'ui_estado_4'),(3,'ui_bateria')]:
    save_source(name,keyed(cell(x,2)),'Icons',(24,24))
for x,name in enumerate(['ui_nota','ui_objeto','ui_ajuste','ui_salir']):
    save_source(name,keyed(cell(x,3)),'Icons',(24,24))

# Windowskin XP: fondo128x128; frame64x64; cursor32x32; flechas/pausa.
skin=Image.new('RGBA',(192,128))
texture=cell(2,0).resize((128,128),Image.Resampling.LANCZOS)
texture=Image.blend(Image.new('RGBA',(128,128),'#0d1513'),texture,.12)
skin.paste(texture,(0,0))
frame=cell(0,0).resize((64,64),Image.Resampling.LANCZOS)
# Cuatro esquinas coherentes del mismo marco, centro transparente.
corner=frame.crop((0,0,16,16))
skin.paste(corner,(128,0)); skin.paste(ImageOps.mirror(corner),(176,0))
skin.paste(ImageOps.flip(corner),(128,48)); skin.paste(ImageOps.flip(ImageOps.mirror(corner)),(176,48))
edge=cell(1,0).crop((0,100,cell(1,0).width,155)).resize((32,6))
skin.paste(edge,(144,0)); skin.paste(edge,(144,58))
v=edge.rotate(90,expand=True).resize((6,32))
skin.paste(v,(128,16)); skin.paste(v,(186,16))
cursor=Image.new('RGBA',(32,32),(111,143,116,50))
cursor.paste(cell(3,0).resize((32,32)),(0,0))
cursor.putalpha(85); skin.paste(cursor,(128,64))
arrow=keyed(cell(0,1)).resize((16,16),Image.Resampling.LANCZOS)
for pos,rotation in [((160,64),90),((176,64),270),((160,80),180),((176,80),0)]:
    skin.paste(arrow.rotate(rotation),pos)
diamond=keyed(cell(1,1)).resize((16,16),Image.Resampling.LANCZOS)
for x in (160,176):
    for y in (96,112): skin.paste(diamond,(x,y))
skin.paste(diamond.resize((32,32)),(128,96))
save_source('ui_windowskin',skin,'Windowskins')
# Niebla: textura de luz del fondo generado, baja frecuencia y alpha tecnico.
fog=Image.open(OUT/'alcantarillas_fuente.png').convert('L').resize((256,256)).filter(ImageFilter.GaussianBlur(16))
mist=Image.new('RGBA',(256,256),(133,161,141,0));mist.putalpha(fog.point(lambda p:p//2))
save_source('ui_fog',mist)
(OUT/'manifest.json').write_text(json.dumps({'assets':assets},ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'generaciones.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('10 fuentes de nube; manifiesto:',len(assets),'recursos')
