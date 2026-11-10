"""Recorta dos atlas image_gen en40 objetos y10 habilidades XP24x24."""
import json
from PIL import Image,ImageDraw,ImageFont
from instalar_arte_final import R,A,write_image
from adaptar_arte import adapt,PALETTES
PALETTES['inventario']=list(dict.fromkeys(PALETTES['piso']+PALETTES['matadero']+PALETTES['alcantarillas']+['#163049','#245779','#4588B0','#86BBCF']))
def bounds(im,axis,count):
 alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0)
 pixels=alpha.load();length=im.width if axis==0 else im.height;other=im.height if axis==0 else im.width
 density=[sum(pixels[i,j] if axis==0 else pixels[j,i] for j in range(other)) for i in range(length)]
 result=[0]
 for k in range(1,count):
  target=k*length/count;radius=length/count*.18
  lo,hi=round(target-radius),round(target+radius)
  result.append(min(range(lo,hi),key=lambda i:density[i]+abs(i-target)*0.01))
 return result+[length]
def run():
 specs=[];sheets={}
 for n in range(50):
  page=n//25;cell=n%25;source=A/f'iconos_{page}_fuente.png'
  if page not in sheets:
   im=Image.open(source).convert('RGBA');sheets[page]=(bounds(im,0,5),bounds(im,1,5))
  xs,ys=sheets[page]
  box=[xs[cell%5],ys[cell//5],xs[cell%5+1],ys[cell//5+1]]
  dest=f'Graphics/Icons/vacas_item_{n+1:02}.png' if n<40 else f'Graphics/Icons/vacas_habilidad_{n+21:02}.png'
  spec=dict(source=str(source.relative_to(R)).replace('\\','/'),destination=dest,type='battler',size='24x24',max_height=24,padding=1,resample='box',alpha_threshold=128,zone='inventario',source_box=box)
  if n==42:
   spec['source']='diseno/arte_hd2d/arte_final/icono_perro_fuente.png';spec.pop('source_box')
  specs.append(spec)
 for spec in specs:
  p,im=adapt(spec);write_image(p,im)
 manifest=json.loads((A/'manifest.json').read_text(encoding='utf8'))
 destinations={a['destination'] for a in specs}
 manifest['assets']=[a for a in manifest['assets'] if a['destination'] not in destinations]+specs
 manifest['inventory_palette']=PALETTES['inventario']
 manifest['inventory_reproduction']='Importar instalar_iconos_arte_final registra la paleta inventario; adaptar_arte.py realiza recorte/ajuste/cuantización sin dithering.'
 (A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
 sheet=Image.new('RGB',(800,700),'#293233');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
 for n,spec in enumerate(specs):
  x=n%10*80;y=n//10*140;im=Image.open(R/spec['destination'])
  sheet.paste(im,(x+4,y+5),im);big=im.resize((72,72),Image.Resampling.NEAREST);sheet.paste(big,(x+4,y+35),big);d.text((x+3,y+111),('OBJ '+str(n+1)) if n<40 else ('HAB '+str(n+21)),font=font,fill='white')
 sheet.save(R/'diseno/capturas/arte_final_iconos.png')
 print('50 iconos propios24x24 instalados; lámina1x/3x.')
if __name__=='__main__':run()

