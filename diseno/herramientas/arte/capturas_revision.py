"""Capturas completas y comparación desde los renders MCP, con máscara del motor."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
from revision_mapas import ROOT, B, LIGHTS
from PIL import Image, ImageDraw, ImageFont
import json
OUT=ROOT/'diseno/capturas/arte'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
names={1:'Prólogo',2:'El piso',3:'La escalera',4:'La calle',5:'Patio y vestíbulo',6:'Vestuarios',7:'Corrales',8:'Cadena',9:'Cámaras',10:'Oficina',11:'Pasillo',12:'Piso de Lucy',13:'Carnicería',14:'Depósito',15:'Hospital',16:'Laboratorio'}
report=json.loads((ROOT/'diseno/verificaciones/revision_mapas.json').read_text(encoding='utf-8'))
for i in range(1,17):
    im=Image.open(OUT/('revision_mapa%02d_base.png'%i)).convert('RGBA')
    im=Image.alpha_composite(im,Image.open(ROOT/'Graphics/Pictures'/('revision_luz%02d.png'%i)).convert('RGBA'))
    # Add a real 1:1 human scale reference, outside the playable capture.
    panel=Image.new('RGBA',(im.width,im.height+76),'#20282a');panel.alpha_composite(im)
    from revision_mapas import frame
    human=frame('vacas_steven',0);panel.alpha_composite(human,(14,im.height+8))
    d=ImageDraw.Draw(panel);d.text((70,im.height+13),f'{i:02d} {names[i]} | {im.width//32} x {im.height//32} baldosas',font=font,fill='white')
    d.text((70,im.height+40),'Referencia 1:1: celda humana 48 px. Luz del motor; tono narrativo y niebla animada no simulados.',font=small,fill='#bac7be')
    panel.convert('RGB').save(OUT/('revision_mapa%02d.png'%i))
    # Refresh legacy scene captures too, without the reference strip.
    targets=([f'acto2_mapa{i}.png',f'acto2_mapa{i}_eventos.png'] if 5<=i<=11 else [f'acto3_{i}.png'] if i>=12 else {1:[],2:['mapa2_el_piso.png'],3:['mapa3_la_escalera.png'],4:['mapa4_la_calle.png']}[i])
    for name in targets:im.convert('RGB').save(OUT/name)
    if i==2:im.crop((0,14*32,30*32,22*32)).resize((1920,512),Image.Resampling.NEAREST).convert('RGB').save(OUT/'mapa2_salon_y_cocina_x2.png')
# Each pair keeps the SAME pixel scale; lab reduction is visible without stretching.
cw,ch=650,530
sheet=Image.new('RGB',(cw*2,ch*16),'#182124');d=ImageDraw.Draw(sheet)
for row,entry in enumerate(report):
    i=entry['mapa'];y=row*ch
    for col,(label,p) in enumerate([('ANTES',B/'antes'/('mapa%02d.png'%i)),('DESPUÉS',OUT/('revision_mapa%02d.png'%i))]):
        im=Image.open(p).convert('RGB')
        if col==1:im=im.crop((0,0,im.width,im.height-76))
        old=Image.open(B/'antes'/('mapa%02d.png'%i))
        scale=min(625/old.width,460/old.height)
        im=im.resize((int(im.width*scale),int(im.height*scale)),Image.Resampling.LANCZOS)
        sheet.paste(im,(col*cw+12,y+48))
        size=entry['antes'] if col==0 else entry['despues']
        d.text((col*cw+12,y+12),f'{i:02d} {names[i]} / {label} / {size[0]}x{size[1]}',font=font,fill='white')
sheet.save(OUT/'revision_mapas.png')
for n in range(4):sheet.crop((0,n*ch*4,cw*2,(n+1)*ch*4)).save(OUT/f'revision_mapas_{n+1}.png')
print('16 capturas, capturas históricas y comparativa completa actualizadas.')
