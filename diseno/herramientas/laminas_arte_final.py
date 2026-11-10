"""Láminas a escala1:1, solo composición de imágenes existentes."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];C=R/'diseno/capturas';B=R/'diseno/respaldos/antes_arte_final'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
def pairs(name,rows):
 out=Image.new('RGB',(1280,len(rows)*515),'#161c20');d=ImageDraw.Draw(out)
 for n,(label,before,after) in enumerate(rows):
  y=n*515;d.text((8,y+5),label+' | ANTES',font=font,fill='white');d.text((648,y+5),'DESPUÉS | píxel1:1',font=font,fill='white')
  for x,p in [(0,before),(640,after)]:
   im=Image.open(p).convert('RGBA')
   if im.size!=(640,480):
    im.thumbnail((640,480),Image.Resampling.BOX)
   out.paste(im,(x+(640-im.width)//2,y+30),im)
 out.save(C/name)
for start in range(22,33,2):
 pairs(f'arte_final_comparacion_{start:02}.png',[(f'Mapa {i:02}',C/f'arte_final_antes_{i:02}.png',C/f'arte_final_despues_{i:02}.png') for i in range(start,min(start+2,33))])
for start in (10,12):
 pairs(f'arte_final_sustos_{start}.png',[(f'Susto {i}',B/f'Graphics/Pictures/screamer_{i}.png',R/f'Graphics/Pictures/screamer_{i}.png') for i in (start,start+1)])
for n,keys in enumerate([['cine_piso','cine_matadero'],['cine_ciudad','cine_altar']]):
 pairs(f'arte_final_cinematicas_{n+1}.png',[(key,B/f'Graphics/Pictures/{key}.png',R/f'Graphics/Pictures/{key}.png') for key in keys])
keys=['turno_noche','res_cuenta','gancho_respira','cripps_matarife','censo_bocas','mesa_exige','rey_sin_rostro','numero_cadena','puerta_muerde']
out=Image.new('RGB',(960,990),'#242b2b');d=ImageDraw.Draw(out)
for n,key in enumerate(keys):
 x=n%3*320;y=n//3*330;d.text((x+4,y+4),key,font=font,fill='white')
 im=Image.open(R/f'Graphics/Battlers/enemigo_{key}.png');out.paste(im,(x,y+27),im)
out.save(C/'arte_final_enemigos.png')
names=['vacas_steven','vacas_madre','vacas_cripps','vacas_muesca','vacas_junco','vacas_guernsey4','vacas_perro']
out=Image.new('RGB',(896,600),'#353c3c');d=ImageDraw.Draw(out)
for n,name in enumerate(names):
 x=n%4*224;y=n//4*300;d.text((x+4,y+3),name,font=font,fill='white')
 im=Image.open(R/f'Graphics/Characters/{name}.png');out.paste(im,(x+4,y+30),im)
out.save(C/'arte_final_personajes.png')
out=Image.new('RGB',(720,380),'#303638');d=ImageDraw.Draw(out)
for x,path,label in [(0,R/'Graphics/Pictures/retrato_madre_neutral.png','Madre anterior'),(240,R/'Graphics/Pictures/retrato_madre_envejecida_neutral.png','Madre VI'),(480,R/'diseno/arte_hd2d/referencias/madre.png','Referencia aprobada')]:
 d.text((x+2,4),label,font=font,fill='white');im=Image.open(path);im.thumbnail((240,340),Image.Resampling.BOX);out.paste(im,(x,32),im)
out.save(C/'arte_final_madre.png')
# Versión con las máscaras de luz reales, además de las comparaciones sin máscara.
for i in range(22,33):
 im=Image.open(C/f'arte_final_despues_{i:02}.png').convert('RGBA')
 mask=R/'Graphics/Pictures'/f'acto{6 if i>=28 else 5}_luz{i:02}.png'
 im.alpha_composite(Image.open(mask).convert('RGBA'))
 im.convert('RGB').save(C/f'arte_final_luz_{i:02}.png')
print('6 láminas de mapas, 2 de sustos, 2 cinemáticas, enemigos, personajes, madre y11 vistas con luz.')

