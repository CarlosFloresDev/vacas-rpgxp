"""Manifiesto y adaptacion de fuentes image_gen recuperadas y nuevas. Sin GPU local."""
import json, math, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from adaptar_arte import adapt, save

ROOT=Path(__file__).resolve().parents[2]
if __name__=='__main__' and (ROOT/'diseno/arte_hd2d/arte_final/manifest.json').exists():
    raise SystemExit('Lote historico desactivado: restauraria Guernsey y sustos provisionales. Usar instalar_arte_final.py/componer_arte_final.py.')
ART=ROOT/'diseno/arte_hd2d/acto4'
assets=[]
def spec(source,destination,kind,**kw):
    assets.append(dict(source='diseno/arte_hd2d/acto4/'+source,destination='Graphics/'+destination,type=kind,resample='box',alpha_threshold=128,**kw))

# Layouts tecnicos: anclas y limites, no ilustraciones sustitutas.
Image.new('RGBA',(256,64),'white').save(ART/'layout_tiles.png')
Image.new('RGBA',(128,256),'white').save(ART/'layout_objetos.png')
spec('tiles_fuente.png','Tilesets/acto4_alcantarillas.png','indexed',size='256x64',cell='32x32',source_grid=[8,2],layout_source='diseno/arte_hd2d/acto4/layout_tiles.png',indexed_mode='resize',padding=0,key='#fafafa',key_tolerance=35,opaque_indices=list(range(8))+[9,11,12,15],zone='alcantarillas')
heights=[14,12,18,30,24,40,30,32,16,16,30,56,24,12,30,28]
im=Image.open(ART/'objetos_fuente.png').convert('RGBA')
rules={}
for n,h in enumerate(heights):
    x,y=n%4,n//4
    tile=im.crop((round(x*im.width/4),round(y*im.height/4),round((x+1)*im.width/4),round((y+1)*im.height/4)))
    tile.putalpha(tile.getchannel('A').point(lambda a:255 if a>=128 else 0))
    b=tile.getbbox()
    h=min(h,math.floor(31*(b[3]-b[1])/(b[2]-b[0])))
    rules[str(n)]={'height':h}
spec('objetos_fuente.png','Characters/vacas_alcantarilla.png','indexed',size='128x256',cell='32x64',layout_source='diseno/arte_hd2d/acto4/layout_objetos.png',cell_scale=rules)
for key in ['muesca','junco']:
    rows=[0,330,610,895,1248] if key=='muesca' else [0,350,570,825,1228]
    spec(key+'_sprite_fuente.png','Characters/vacas_'+key+'.png','character',cell='48x48',padding=2,pad_grid=True,source_rows=rows)
    spec(key+'_retrato_fuente.png','Pictures/retrato_'+key+'_neutral.png','retrato',size='240x340',padding=4)
# La Guernsey conserva su identidad aprobada: fuente de fase 2 readaptada a celda48.
g=json.loads((ROOT/'diseno/arte_hd2d/lote_vaca_canela.json').read_text(encoding='utf-8'))['assets'][0]
g.update(destination='Graphics/Characters/vacas_guernsey4.png',cell='48x48',padding=2)
assets.append(g)
for key in ['coro','pulmon']:
    spec(key+'_fuente.png','Battlers/enemigo_'+key+'.png','battler',size='320x300',max_height=300,padding=4)
for key,box in [('cencerro',[16,590,340,1230]),('pastor',[650,590,1000,1230])]:
    spec('referencia_visiones.png','Battlers/enemigo_'+key+'.png','battler',source_box=box,size='320x300',max_height=300,padding=4)
for n,key in [(10,'coro'),(11,'pulmon')]:
    spec(key+'_fuente.png','Pictures/screamer_'+str(n)+'.png','picture',size='640x480',background='#090f12',source_box=([250,40,1050,740] if n==10 else [220,70,1100,750]))
manifest={'generator':'image_gen en nube; fuentes originales conservadas, sin generacion local','assets':assets,'escala':{'baldosa':32,'celda_personajes':48,'objetos_pequenos':'10-16px; etiqueta12, pila14, botas16, mapa16','reglas_por_indice':rules},'nota':'Sustos: reencuadres de las visiones generadas. Cencerro/Pastor: vistas frontales de referencia_visiones. Guernsey: fuente aprobada de fase2.'}
(ART/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
for a in assets:
    dest,im=adapt(a);save(dest,im)
out=Image.new('RGB',(1000,1350),'#182420');d=ImageDraw.Draw(out)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
d.text((16,12),'ACTO IV | arte adaptado de fuentes image_gen | personajes y objetos 1:1',font=font,fill='white')
for i,a in enumerate(assets):
    im=Image.open(ROOT/a['destination']).convert('RGBA');im.thumbnail((310,285))
    x=12+i%3*330;y=50+i//3*250
    # Ultima fila se limita a su franja; sprites a escala real sin ampliacion.
    im.thumbnail((310,215))
    out.paste(im,(x,y),im)
    d.text((x,y+218),Path(a['destination']).name,font=font,fill='#ccd8bb')
out.save(ROOT/'diseno/capturas/acto4_arte.png')
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ART.glob('*.png')}
(ART/'fuentes_sha256.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
print(len(assets),'assets adaptados; manifiesto, hashes y lamina guardados.')
