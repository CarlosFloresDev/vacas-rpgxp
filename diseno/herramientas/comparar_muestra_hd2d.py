"""Lámina de revisión antes/después; no modifica assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[2]
selected=['Graphics/Characters/vacas_steven.png','Graphics/Pictures/retrato_steven_neutral.png','Graphics/Battlers/enemigo_vaca.png','Graphics/Pictures/screamer_3.png']
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
canvas=Image.new('RGB',(3920,6500),(18,20,24)); d=ImageDraw.Draw(canvas)
d.text((30,24),'VACAS / FASE 1 — ANTES (SD v1) Y DESPUÉS (image_gen + adaptación CPU)',font=font,fill='#e8d9aa')
y=100
for name in selected:
    old=Image.open(ROOT/'diseno/arte_provisional/sd_v1'/name).convert('RGBA')
    new=Image.open(ROOT/name).convert('RGBA')
    d.text((30,y),name,font=font,fill='#e8d9aa'); y+=45
    for scale in (1,3):
        for column,im in enumerate((old,new)):
            x=30+column*1950
            d.text((x,y),('ANTES' if column==0 else 'DESPUÉS')+f' / {scale}x / {im.width}×{im.height} px',font=small,fill='#adc0bd')
            enlarged=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
            tile=Image.new('RGB',enlarged.size,(62,65,69)); td=ImageDraw.Draw(tile)
            for cy in range(0,tile.height,16):
                for cx in range(0,tile.width,16):
                    if (cx//16+cy//16)%2: td.rectangle((cx,cy,cx+15,cy+15),fill=(70,73,77))
            tile.paste(enlarged,(0,0),enlarged); canvas.paste(tile,(x,y+35))
        y+=new.height*scale+65
    y+=20
canvas=canvas.crop((0,0,3920,y))
canvas.save(ROOT/'diseno/capturas/muestra_hd2d.png')
canvas.thumbnail((980,1800)); canvas.save(ROOT/'diseno/capturas/muestra_hd2d_resumen.png')
print('Comparativa creada; altura:',y)
