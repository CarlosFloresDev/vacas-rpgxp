"""Láminas comparativas y escala real. Solo escribe diseno/capturas/arte."""
from pathlib import Path
import math,json
from PIL import Image,ImageDraw,ImageFont
from auditar_coherencia import ROOT,BACK,PROPS

OUT=ROOT/'diseno/capturas/arte'
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
BG='#282c30'

def label(im,xy,text,color='white'):ImageDraw.Draw(im).text(xy,text,fill=color,font=FONT)
def paste_fit(dst,src,box):
    src=src.copy().convert('RGBA');src.thumbnail((box[2],box[3]),Image.Resampling.NEAREST)
    dst.paste(src,(box[0]+(box[2]-src.width)//2,box[1]+(box[3]-src.height)//2),src)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    lab=Image.open(ROOT/'Graphics/Characters/vacas_laboratorio.png')
    lab.resize((lab.width*4,lab.height*4),Image.Resampling.NEAREST).save(OUT/'coherencia_laboratorio_detalle.png')
    for cat in sorted((ROOT/'Graphics').iterdir()):
        if not cat.is_dir():continue
        files=sorted(cat.glob('*.png')); cols=3;rowh=204;w=1080
        sheet=Image.new('RGB',(w,max(100,40+math.ceil(len(files)/cols)*rowh)),BG)
        label(sheet,(8,8),f'{cat.name} | ANTES izquierda / DESPUÉS derecha | todos los archivos, NEAREST; miniaturas de catálogo')
        if not files:label(sheet,(8,40),'Sin PNG locales en esta categoría.')
        for i,p in enumerate(files):
            x=i%cols*360;y=40+i//cols*rowh;b=BACK/p.relative_to(ROOT)
            label(sheet,(x+4,y),p.stem[:48])
            label(sheet,(x+4,y+16),'modificado' if b.exists() else ('nuevo' if p.stem.startswith('vacas_reserva') or p.stem=='vacas_luz_escalera' else 'conservado'),'#d8bb88')
            if b.exists():paste_fit(sheet,Image.open(b),(x+4,y+34,170,166))
            elif not (p.stem.startswith('vacas_reserva') or p.stem=='vacas_luz_escalera'):paste_fit(sheet,Image.open(p),(x+4,y+34,170,166))
            paste_fit(sheet,Image.open(p),(x+184,y+34,170,166))
        sheet.save(OUT/f'coherencia_{cat.name}.png')
        # Partes legibles sin reducción automática de láminas largas.
        if sheet.height>1400:
            for i,y in enumerate(range(0,sheet.height,1264)):
                sheet.crop((0,y,w,min(sheet.height,y+1264))).save(OUT/f'coherencia_{cat.name}_{i+1:02}.png')
    chars=[p for p in sorted((ROOT/'Graphics/Characters').glob('*.png')) if p.stem not in PROPS and p.stem!='vacas_furgoneta']
    plate=Image.new('RGB',(960,40+math.ceil(len(chars)/8)*140),BG)
    label(plate,(6,6),'ESCALA REAL 1:1 | frontal y lateral por identidad | referencia horizontal común: pies')
    for i,p in enumerate(chars):
        x=i%8*120;y=40+i//8*140;im=Image.open(p).convert('RGBA');cw,ch=im.width//4,im.height//4
        label(plate,(x+2,y),p.stem.replace('vacas_','')[:19])
        for n,row in enumerate((0,1)):
            cell=im.crop((0,row*ch,cw,(row+1)*ch));xx=x+(120-cw)//2;baseline=y+62+n*64
            ImageDraw.Draw(plate).line((x,baseline,x+116,baseline),fill='#657078')
            plate.paste(cell,(xx,baseline-ch),cell)
    plate.save(OUT/'coherencia_personajes_1x.png')
    plate.resize((plate.width*3,plate.height*3),Image.Resampling.NEAREST).save(OUT/'coherencia_personajes_3x.png')
    # Comprobación visual de identidad: sprite, todos los retratos y battlers vinculados.
    identities={'steven':['steven','steven_mente','enemigo_rey'],'madre':['madre','enemigo_madre'],'lucy':['lucy'],'cripps':['cripps','enemigo_sombra_cripps','enemigo_cripps_matarife'],'perro':['dog'],'guernsey4':['guernsey','enemigo_guernsey'],'junco':['junco'],'muesca':['muesca'],'obrero1':['benito'],'obrero2':['rubio','sierra'],'obrero3':['encarna'],'obrero4':['chato'],'carnicero':['molina'],'anselmo':['anselmo'],'remedios':['remedios'],'borracho':['borracho'],'reclutador':['reclutador'],'elena':['elena']}
    for char,names in identities.items():
        paths=[ROOT/'Graphics/Characters'/f'vacas_{char}.png']
        paths += [p for p in (ROOT/'Graphics/Pictures').glob('retrato_*.png') if any(p.stem.startswith('retrato_'+n+'_') for n in names)]
        paths += [p for p in (ROOT/'Graphics/Battlers').glob('*.png') if p.stem in names]
        # La Biblia exige contrastar también la referencia de producción.
        refname={'guernsey4':'guernsey','obrero1':'benito','obrero2':'rubio','obrero3':'encarna','obrero4':'chato','carnicero':'molina'}.get(char,char)
        reference=ROOT/'diseno/fuentes/arte_hd2d/referencias'/f'{refname}.png'
        if reference.exists():paths.append(reference)
        im=Image.new('RGB',(max(720,len(paths)*180),400),BG)
        label(im,(6,6),f'Identidad: {char} | sprite 3x; retratos y battlers reducidos solo para comparación')
        for i,p in enumerate(paths):
            src=Image.open(p).convert('RGBA')
            if i==0:
                src=src.crop((0,0,src.width//4,src.height//4));src=src.resize((src.width*3,src.height*3),Image.Resampling.NEAREST)
            paste_fit(im,src,(i*180,40,176,320));label(im,(i*180+3,370),p.stem[:26])
        im.save(OUT/f'coherencia_identidad_{char}.png')
    # Ventana segura: 640x360 central dentro del original 640x480.
    pics=[p for cat in ('Pictures','Battlebacks','Titles','Gameovers') for p in (ROOT/'Graphics'/cat).glob('*.png') if Image.open(p).size==(640,480)]
    for start in range(0,len(pics),12):
        im=Image.new('RGB',(1280,math.ceil(len(pics[start:start+12])/4)*264),BG)
        for i,p in enumerate(pics[start:start+12]):
            x=i%4*320;y=i//4*264;src=Image.open(p).convert('RGBA').resize((320,240),Image.Resampling.NEAREST)
            im.paste(src,(x,y+24),src);label(im,(x+3,y+3),p.stem)
            ImageDraw.Draw(im).rectangle((x,y+54,x+319,y+233),outline='#d0b46b',width=1)
        im.save(OUT/f'coherencia_encuadres_{start//12+1:02}.png')

if __name__=='__main__':main()
