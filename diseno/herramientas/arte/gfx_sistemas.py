"""Arte provisional reproducible con Pillow. No requiere instalar dependencias."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, json
ROOT=_ROOT
FONT='C:/Windows/Fonts/arial.ttf'
manifest=[]
def save(im,folder,name,look):
 p=ROOT/'Graphics'/folder/(name+'.png');p.parent.mkdir(exist_ok=True);im.save(p)
 manifest.append({'archivo':str(p.relative_to(ROOT)).replace('\\','/'),'aspecto':look})
def label(d,text,w,y):
 d.rectangle((0,y,w,y+24),fill=(17,20,22,220));d.text((9,y+4),'PROVISIONAL / '+text,font=ImageFont.truetype(FONT,12),fill=(184,169,134))
people={
 'steven':('Steven',(148,147,131),'Joven exhausto, pelo oscuro, ropa gris, ojos hundidos.'),
 'madre':('Madre',(158,136,112),'Figura ancha, bata mostaza, rostro dominante bajo luz de nicotina.'),
 'lucy':('Lucy',(161,169,155),'Pelo claro recogido, bata pálida, tarro vacío y mirada inquieta.'),
 'cripps':('Cripps',(147,117,105),'Capataz corpulento, cabeza rapada, delantal de trabajo.'),
 'dog':('Perro',(143,127,101),'Perro mestizo tumbado, orejas caídas, mirada cálida.'),
 'guernsey':('La Guernsey',(162,123,90),'Vaca canela, cuernos curvos y un ojo castaño a través de una rejilla.'),
 'benito':('Benito',(147,145,129),'Obrero veterano con canas y mono gastado.'),
 'encarna':('Encarna',(151,151,140),'Obrera de pelo recogido y mono blanco.'),
 'rubio':('El Rubio',(164,149,111),'Obrero de cabello rubio y guantes oscuros.'),
 'chato':('El Chato',(148,132,115),'Obrero bajo, rostro ancho y nariz achatada.'),
 'sierra':('Obrero de la sierra',(137,142,134),'Obrero con máscara protectora y casco.'),
 'remedios':('Doña Remedios',(151,143,124),'Vecina anciana con pelo blanco y chal oscuro.'),
 'anselmo':('Señor Anselmo',(137,146,141),'Vecino anciano con bigote gris y chaqueta.'),
 'molina':('Molina',(160,137,126),'Carnicero con bigote y delantal rojizo.'),
 'borracho':('Borracho',(142,122,117),'Hombre desaliñado con abrigo y nariz roja.'),
 'reclutador':('Hombre del matadero',(139,149,141),'Conductor con gorra, chaqueta y carpeta de contratación.')}
for idx,(key,(name,col,look)) in enumerate(people.items()):
 for expression in (['neutral','miedo'] if key in ['steven','dog'] else ['neutral','ira'] if key in ['madre','cripps'] else ['neutral','susurro'] if key in ['lucy','guernsey'] else ['neutral']):
  im=Image.new('RGBA',(240,340));d=ImageDraw.Draw(im)
  # Silueta dibujada en capas; transparencia fuera del busto.
  coat=tuple(max(20,c//3) for c in col)+(255,)
  if key in ['dog','guernsey']:
   d.ellipse((30,155,225,329),fill=coat,outline=col)
   d.polygon([(48,112),(20,48),(87,92)],fill=coat,outline=col)
   d.polygon([(153,92),(218,48),(191,133)],fill=coat,outline=col)
   d.ellipse((47,70,195,237),fill=col)
   d.ellipse((64,166,183,242),fill=tuple(c-30 for c in col))
   d.ellipse((91,183,150,216),fill=(32,29,27))
   if key=='guernsey':
    d.arc((8,12,89,101),20,180,fill=(212,202,160),width=12);d.arc((158,12,231,101),0,160,fill=(212,202,160),width=12)
  else:
   wide=20 if key in ['madre','cripps'] else 0
   d.polygon([(17-wide,340),(29-wide,228),(84,202),(162,202),(218+wide,237),(238+wide,340)],fill=coat,outline=col)
   d.rectangle((98,174,143,235),fill=col)
   d.ellipse((61-wide//2,42,184+wide//2,213),fill=col,outline=(30,31,29),width=3)
   hair=(196,189,161) if key in ['lucy','rubio','remedios','anselmo'] else (37,35,32)
   d.pieslice((55,28,190,130),180,358,fill=hair)
   d.line((123,114,116,159,134,164),fill=(69,65,57),width=3)
   d.line((88,179,149,179+(8 if expression in ['miedo','ira'] else 0)),fill=(68,54,49),width=3)
   if key=='madre':d.polygon([(29,238),(79,208),(116,340),(21,340)],fill=(103,89,49))
   if key in ['cripps','molina']:d.polygon([(81,223),(158,223),(191,340),(51,340)],fill=(105,91,81))
   if key=='lucy':d.rectangle((170,269,208,321),outline=(194,209,198),width=3)
   if key in ['reclutador','sierra']:d.rectangle((55,60,191,86),fill=(46,53,50))
  for x in (86,153):
   d.ellipse((x-12,118,x+12,130),fill=(36,32,30));d.ellipse((x-2,120,x+3,127),fill=(220,201,158) if expression not in ['ira','miedo'] else (220,117,91))
  # Rasgos legibles incluso al reducir el retrato.
  if key not in ['dog','guernsey']:
   if key in ['anselmo','molina']:
    d.polygon([(91,164),(120,158),(151,164),(147,174),(123,168),(96,175)],fill=(54,51,46))
   if key in ['lucy','encarna','remedios','madre']:
    d.ellipse((49,41,83,95),fill=hair)
    d.ellipse((158,40,194,94),fill=hair)
   if key=='cripps':
    d.line((70,86,177,86),fill=(57,44,40),width=5)
    d.line((157,137,172,165),fill=(97,60,53),width=2)
   if key=='sierra':d.rectangle((76,137,168,183),fill=(72,84,79),outline=(153,164,143),width=3)
  if expression=='ira':
   d.line((72,105,105,116),fill=(42,34,30),width=5)
   d.line((140,116,171,104),fill=(42,34,30),width=5)
  if expression in ['miedo','susurro']:
   d.line((72,109,103,101),fill=(63,55,47),width=3)
   d.line((139,101,169,109),fill=(63,55,47),width=3)
   if key not in ['dog','guernsey']:d.ellipse((109,176,135,197),fill=(52,39,34))
  rng=random.Random(idx)
  for i in range(130):
   x=rng.randrange(45,196);y=rng.randrange(90,305)
   if im.getpixel((x,y))[3]:d.point((x,y),fill=(70,65,56,100))
  label(d,name+' / '+expression,240,316)
  save(im,'Pictures','retrato_'+key+'_'+expression,look+' Expresión: '+expression+'. Busto transparente 240×340.')
enemies=[('vaca','La Vaca que habla','Cabeza bovina suspendida, lengua como cinta de tele.'),('madre','La Madre de yeso','Bata vacía, rostro agrietado y manos enormes.'),('tunel','Lo del túnel','Forma alargada sin rostro, ojos al fondo de un conducto.'),('sombra_cripps','Sombra de Cripps','Silueta de capataz deformada por ganchos.'),('moscas','Enjambre de moscas','Nube de moscas formando una cara.'),('guernsey','Guernsey de humo','Vaca canela espectral, cuernos de tubería.'),('canal','Canal en el gancho','Carcasa abstracta colgada, costillas como barrotes.'),('televisor','La Familia de nieve','Televisor de los cincuenta con rostros de estática.'),('rey','El Rey del cajón','Jefe: Steven coronado con ganchos, reflejo del verdugo.')]
for idx,(key,name,look) in enumerate(enemies):
 im=Image.new('RGBA',(320,300));d=ImageDraw.Draw(im);rng=random.Random(idx+70);c=(104+idx*5,79+idx*3,69+idx*2)
 if key=='moscas':
  for _ in range(240):
   x=int(rng.gauss(160,53));y=int(rng.gauss(142,51));d.ellipse((x,y,x+4,y+3),fill=(140,145,116));d.line((x-2,y-2,x+7,y+4),fill=(85,94,83))
 elif key=='televisor':
  d.rounded_rectangle((42,62,278,262),15,fill=(73,62,46),outline=c,width=4);d.rounded_rectangle((58,77,240,229),20,fill=(36,46,43))
  for _ in range(2300):
   x=rng.randrange(64,234);y=rng.randrange(84,224);g=rng.randrange(50,160);d.point((x,y),fill=(g,g,g))
  d.ellipse((105,125,127,145),fill=(210,211,180));d.ellipse((177,125,199,145),fill=(210,211,180))
 else:
  d.polygon([(52,283),(73,182),(115,148),(119,64),(196,54),(209,151),(253,183),(281,283)],fill=(35,39,37),outline=c,width=4)
  d.ellipse((108,48,214,175),fill=c)
  if key in ['vaca','guernsey']:
   d.polygon([(111,80),(50,24),(84,111)],fill=(188,178,143));d.polygon([(207,80),(274,24),(236,110)],fill=(188,178,143));d.ellipse((111,130,216,188),fill=(70,54,46))
  if key in ['canal','rey','sombra_cripps']:
   d.line((160,0,160,54),fill=(173,169,152),width=4)
   for y in range(187,260,14):d.line((102,y,221,y+5),fill=(159,145,121),width=4)
  if key=='tunel':d.ellipse((110,48,215,187),fill=(5,9,10))
  if key=='rey':
   d.line((101,65,118,19,142,52,164,9,184,49,218,16,221,72),fill=(204,183,125),width=6)
  for x in [133,185]:d.ellipse((x,91,x+12,99),fill=(238,184,122))
 label(d,name,320,276);save(im,'Battlers','enemigo_'+key,look+' Silueta transparente 320×300.')
# Steven para el combate frontal de XP.
im=Image.open(ROOT/'Graphics/Pictures/retrato_steven_miedo.png').convert('RGBA');save(im,'Battlers','steven_mente','Steven pequeño frente a sus alucinaciones. Sustituir por figura completa 240×340.')
for idx,key in enumerate(['piso','matadero','tunel']):
 im=Image.new('RGB',(640,480));d=ImageDraw.Draw(im);rng=random.Random(idx)
 for y in range(480):
  c=(12+y//35,15+y//30,17+y//35) if idx else (22+y//30,19+y//38,14+y//50);d.line((0,y,640,y),fill=c)
 for x in range(-160,801,80):d.line((320,175,x,480),fill=(42,43,38))
 for y in range(180,480,32):d.line((0,y,640,y),fill=(36,39,35))
 for x in [60,180,460,580]:
  d.line((x,0,x,170),fill=(60,65,56),width=3);d.arc((x-10,159,x+10,187),0,225,fill=(95,89,68),width=3)
 if idx==2:
  for k in range(8):d.ellipse((80+k*22,20+k*13,560-k*22,390-k*13),outline=(32+k*2,43+k*2,38+k),width=4)
 label(d,key,640,456);save(im,'Battlebacks','mente_'+key,'Espacio mental de '+key+': perspectiva opresiva, sombras verdes/negras, luz central mínima. 640×480.')
for idx,look in enumerate(['Ojo de madre al otro lado del espejo.','Familia de televisión con bocas de estática.','Hocico bovino pegado al cristal del camión.','Rostro sustituido por un sumidero.','Ojo castaño tras la rejilla.','Sombra del capataz entre ganchos.','Corona de ganchos sobre el reflejo de Steven.'],1):
 im=Image.new('RGB',(640,480),(9,11,10));d=ImageDraw.Draw(im);rng=random.Random(idx)
 d.ellipse((-35,-105,675,620),fill=(92+idx*8,83,64));d.polygon([(0,0),(640,0),(640,110),(0,220)],fill=(22,26,22))
 for x in [170,460]:
  d.ellipse((x-90,150,x+90,240),fill=(216,205,159));d.ellipse((x-22,148,x+18,242),fill=(5,8,7))
 d.ellipse((200,290,445,530),fill=(12,9,8))
 for _ in range(13000):
  x=rng.randrange(640);y=rng.randrange(480);g=rng.randrange(60);d.point((x,y),fill=(g+20,g,g))
 label(d,'SUSTO '+str(idx),640,456);save(im,'Pictures','screamer_'+str(idx),look+' Imagen repentina a pantalla completa 640×480.')
(ROOT/'diseno/fuentes/catalogos/arte_provisional.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(manifest),'imágenes provisionales')
