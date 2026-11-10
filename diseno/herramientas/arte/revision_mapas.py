"""Rediseño reproducible desde el respaldo; tiles nativos XP, sin regenerar eventos."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json, random, math, copy
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
ROOT=_ROOT
B=ROOT/(ROOT/'diseno/archivo/herramientas/respaldo_revision.txt').read_text().strip()
S=json.loads(((_ROOT / 'diseno/verificaciones/inventario/snapshot.json')).read_text(encoding='utf-8'))
RTP=Path('D:/SteamLibrary/steamapps/common/RPGXP/rtp/Graphics')
OUT=ROOT/'diseno/capturas/arte'
def asset(folder,name):
    p=ROOT/'Graphics'/folder/(name+'.png')
    return Image.open(p if p.exists() else RTP/folder/(name+'.png')).convert('RGBA')
def frame(name,n):
    im=asset('Characters',name);w,h=im.width//4,im.height//4
    return im.crop((n%4*w,n//4*h,(n%4+1)*w,(n//4+1)*h))
def prop(kind,seed):
    r=random.Random(seed)
    if kind in ['shelf','archive','rack']:
        im=Image.new('RGBA',(64,64));d=ImageDraw.Draw(im)
        wood=kind=='archive';c=(78,62,43) if wood else (64,78,73)
        d.rectangle((2,3,61,58),fill=(22,30,28,255),outline=(15,20,19))
        for x in [3,59]:d.rectangle((x,3,x+2,62),fill=c)
        for y in [20,38,57]:
            for x in range(7,56,11):
                h=r.randint(9,14)
                if wood:
                    d.rectangle((x,y-h,x+7,y-2),fill=r.choice(['#8f8061','#6f735d','#9d9172']))
                    d.line((x+1,y-h+3,x+6,y-h+3),fill='#323c34')
                else:
                    d.rounded_rectangle((x,y-h,x+7,y-2),radius=2,fill=r.choice(['#5e7e68','#738764','#9b885a']),outline='#263c33')
                    d.rectangle((x,y-h,x+7,y-h+2),fill='#9a9a80')
                    d.rectangle((x+2,y-8,x+6,y-5),fill='#b5b498')
            d.rectangle((3,y,61,y+3),fill=c);d.line((4,y,60,y),fill='#9a9e84')
        return im.resize((64,56),Image.Resampling.NEAREST)
    if kind=='crate':
        im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
        d.rectangle((3,7,28,29),fill='#70563b',outline='#252b24')
        d.polygon([(3,7),(11,3),(30,5),(28,9)],fill='#9a7b52')
        for y in [13,21,27]:d.line((4,y,27,y),fill='#3b352a')
        d.line((7,9,23,28),fill='#ad9063',width=3)
        return im
    if kind=='bench':
        im=Image.new('RGBA',(64,32));d=ImageDraw.Draw(im)
        d.rectangle((4,8,59,21),fill='#65533e',outline='#282e29')
        d.line((6,11,57,11),fill='#a58b5c');d.rectangle((8,22,12,29),fill='#343d36');d.rectangle((50,22,54,29),fill='#343d36')
        return im
    if kind=='table':
        im=Image.new('RGBA',(64,48));d=ImageDraw.Draw(im)
        d.rectangle((6,31,10,46),fill='#333e38');d.rectangle((51,31,55,46),fill='#333e38')
        d.rectangle((2,13,61,32),fill='#8d9990',outline='#303b35');d.line((4,15,60,15),fill='#c6c8ae')
        d.rectangle((10,16,25,26),fill='#b1b09b');d.line((13,19,22,20),fill='#5a6151')
        jar=frame('vacas_laboratorio',3);im.alpha_composite(jar,(25,-35))
        return im
    if kind=='gurney':
        im=frame('vacas_laboratorio',0)
        d=ImageDraw.Draw(im);d.ellipse((10,23,22,31),fill=(85,49,37,190));d.line((19,28,23,43),fill=(99,67,43,190),width=2)
        return im
    if kind=='trash':
        im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
        for _ in range(9):
            x,y=r.randint(3,25),r.randint(10,28)
            d.polygon([(x,y),(x+5,y-2),(x+7,y+2),(x+1,y+4)],fill=r.choice(['#73755b','#9c987b','#565a47']))
        return im
    raise ValueError(kind)

# Anchor positions use deliberately uneven offsets inside each tile.
LAYOUT={
1:[(2,3,'crate'),(3,4,'crate'),(15,9,'crate'),(3,10,'bench'),(14,4,'rack'),(15,5,'trash')],
2:[(2,6,'archive'),(17,7,'crate'),(26,8,'trash'),(1,17,'crate'),(10,19,'bench'),(19,19,'trash'),(11,12,'crate')],
3:[(1,5,'archive'),(15,8,'crate'),(16,9,'crate'),(1,9,'bench'),(10,10,'trash'),(8,3,'trash')],
4:[(2,7,'crate'),(3,8,'trash'),(11,6,'bench'),(24,7,'crate'),(25,8,'trash'),(36,14,'crate'),(29,15,'trash'),(7,14,'trash')],
5:[(2,4,'archive'),(19,5,'bench'),(25,6,'crate'),(26,7,'crate'),(2,12,'crate'),(5,18,'trash'),(24,18,'crate'),(25,19,'trash')],
6:[(1,5,'rack'),(10,5,'bench'),(17,5,'rack'),(3,10,'crate'),(16,11,'trash'),(6,6,'trash')],
7:[(1,3,'crate'),(9,4,'crate'),(19,4,'crate'),(27,15,'crate'),(8,16,'trash'),(17,16,'trash')],
8:[(7,3,'table'),(19,3,'rack'),(28,3,'crate'),(2,18,'crate'),(9,19,'trash'),(14,20,'crate'),(28,19,'table'),(35,19,'crate')],
9:[(7,3,'crate'),(17,3,'crate'),(27,3,'rack'),(2,12,'trash'),(11,12,'trash'),(23,12,'trash'),(25,17,'crate')],
10:[(1,3,'archive'),(11,4,'archive'),(1,10,'crate'),(14,8,'table'),(15,11,'crate'),(7,9,'trash'),(8,3,'bench')],
11:[(4,3,'rack'),(17,3,'rack'),(11,10,'crate'),(12,11,'crate'),(25,11,'trash'),(5,10,'trash')],
12:[(1,4,'archive'),(9,4,'bench'),(1,7,'crate'),(5,8,'trash'),(10,12,'archive'),(16,6,'shelf'),(20,7,'table'),(16,13,'bench'),(21,16,'crate'),(3,15,'table')],
13:[(1,3,'shelf'),(15,5,'rack'),(15,8,'table'),(2,10,'crate'),(3,11,'crate'),(11,10,'trash'),(7,3,'shelf')],
14:[(1,5,'rack'),(15,10,'crate'),(16,11,'trash'),(9,3,'shelf'),(4,6,'trash')],
15:[(1,4,'archive'),(8,7,'bench'),(1,7,'crate'),(3,13,'archive'),(9,14,'table'),(15,4,'shelf'),(15,10,'gurney'),(20,10,'rack'),(18,15,'trash'),(3,17,'trash')],
16:[(1,3,'shelf'),(8,3,'shelf'),(12,3,'shelf'),(1,7,'gurney'),(3,4,'table'),(8,4,'table'),(14,4,'table'),(16,6,'shelf'),(5,8,'table'),(11,9,'table'),(16,11,'crate'),(17,12,'trash'),(3,11,'crate'),(4,12,'trash'),(1,11,'shelf'),(11,12,'crate'),(12,12,'crate'),(16,8,'crate'),(2,9,'trash'),(7,7,'trash')]
}
LIGHTS={1:[(9,7)],2:[(4,5),(23,5),(7,17),(23,18),(15,12)],3:[(9,6),(17,3)],4:[(7,6),(18,7),(31,10)],5:[(6,4),(23,4),(14,16)],6:[(5,4),(15,5)],7:[(5,5),(23,5)],8:[(4,5),(15,8),(26,8),(20,17),(34,19)],9:[(5,4),(15,4),(24,4)],10:[(5,6),(15,4)],11:[(8,5),(22,5)],12:[(8,6),(19,6),(5,13),(19,14)],13:[(6,5),(12,8)],14:[(8,5),(15,8)],15:[(7,5),(18,6),(7,13)],16:[(4,5),(9,5),(14,5),(16,10)]}
def main():
    patches={};report=[]
    
    for mid in range(1,17):
        m=copy.deepcopy(S['Map%03d'%mid]);old=(m['width'],m['height']);w,h=old
        if mid==1:
            # The prologue was an unbuilt grass placeholder. A confined service
            # courtyard now supports its narration; autorun and timing stay intact.
            m['tileset_id']=51
            m['data']['data']=[0]*(w*h*3)
            for y in range(h):
                for x in range(w):
                    m['data']['data'][x+y*w]=394 if x in [0,w-1] or y in [0,h-1] else 396 if y==1 else 397 if y==2 else 388
        if mid==16:
            w,h=20,15;m['width'],m['height']=w,h
            data=[0]*(w*h*3)
            for y in range(h):
                for x in range(w):data[x+y*w]=394 if x in [0,w-1] or y in [0,h-1] else 396 if y==1 else 397 if y==2 else 384
            data[10+(h-1)*w]=384
            for x,y in [(6,4),(6,5),(11,4),(11,5)]:data[x+y*w]=397
            m['data'].update(xsize=w,ysize=h,data=data)
            coords={1:(0,0),2:(10,13),3:(4,6),4:(9,6),5:(14,6),6:(5,10),7:(9,9),8:(15,11),9:(7,10),10:(17,9),11:(14,9)}
            for e in m['events'].values():e['x'],e['y']=coords[e['id']]
            tone=m['events']['1']['pages'][0]['list']
            for c in tone:
                if c['code']==223:c['parameters'][0].update(red=-38,green=-16,blue=-42,alpha=35)
        tileset=copy.deepcopy(S['Tilesets'][m['tileset_id']]);baseim=asset('Tilesets',tileset['tileset_name'])
        r=random.Random(5200+mid);art=Image.new('RGBA',(w*32,h*32));draw=ImageDraw.Draw(art)
        # Floor material: grouped chips, damp, litter and tracks rather than uniform noise.
        def floor(x,y):
            t=m['data']['data'][x+y*w]
            return t>=384 and not (tileset['passages']['data'][t]&15) and not m['data']['data'][x+y*w+w*h]
        for y in range(3,h-1):
            for x in range(1,w-1):
                if not floor(x,y):continue
                edge=x in [1,2,w-3,w-2] or y in [3,h-2]
                if r.random() < (.62 if edge else .15):
                    px,py=x*32+r.randint(0,18),y*32+r.randint(4,24)
                    draw.ellipse((px,py,px+r.randint(8,27),py+r.randint(2,7)),fill=(43,44,29,50))
                    if r.random()<.6:
                        draw.line([(px,py),(px+6,py-3),(px+10,py+3),(px+17,py+1)],fill=(32,41,33,100),width=1)
                if r.random()<(.13 if mid>=12 else .07):
                    px,py=x*32+r.randint(2,18),y*32+r.randint(3,19)
                    paper=Image.new('RGBA',(14,12));pd=ImageDraw.Draw(paper)
                    pd.rectangle((1,1,12,10),fill=(156,150,116,190));pd.line((3,4,10,4),fill='#626a55');pd.line((3,7,8,7),fill='#626a55')
                    art.alpha_composite(paper.rotate(r.randint(-32,32),expand=True),(px,py))
        protected=set()
        for e in m['events'].values():
            for dx,dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:protected.add((e['x']+dx,e['y']+dy))
        # All entry points, including invisible story transfers, stay free.
        for j in range(1,17):
            for e in S['Map%03d'%j]['events'].values():
                for p in e['pages']:
                    for c in p['list']:
                        if c['code']==201 and c['parameters'][1]==mid:
                            x,y=c['parameters'][2:4]
                            if mid==16:x,y=10,12
                            for dx in range(-1,2):
                                for dy in range(-1,2):protected.add((x+dx,y+dy))
        # No new collision is introduced on chase maps; their floor clutter remains low.
        blocks=set();furniture=0
        for n,(x,y,k) in enumerate(LAYOUT[mid]):
            im=prop(k,mid*100+n);ox=x*32+r.choice([1,3,5]);oy=y*32-im.height+32-r.choice([0,2,5])
            occupied=[(xx,yy) for yy in range(max(0,oy//32),min(h,(oy+im.height+31)//32)) for xx in range(x,min(w,(ox+im.width+31)//32))]
            # Decorations may sit against walls, but never mask an interactive sprite.
            if any((e['x']*32-12 < ox+im.width and e['x']*32+28 > ox and e['y']*32-12 < oy+im.height and e['y']*32+30 > oy) for e in m['events'].values() if e['x']>0 and e['y']>1):continue
            art.alpha_composite(im,(ox,oy));furniture+=1
            if mid not in [1,2,7,8,9,14]:
                for xx in range(x,min(w-1,x+max(1,im.width//32))):
                    if (xx,y) not in protected and floor(xx,y):blocks.add((xx,y))
        # Low cables follow the work areas; stains lead toward drain / gurney.
        if mid>=5:
            for x,y in LIGHTS[mid]:
                px,py=x*32+9,y*32+17
                draw.line([(px,py),(px+13,py+8),(px+19,py+6),(px+27,py+18)],fill=(23,35,28,200),width=2)
        if mid==16:
            # Exposed conduits and suspended task lamps connect improvised stations.
            draw.line([(24,91),(24,67),(569,67),(569,230)],fill='#465b4b',width=3)
            draw.line([(27,91),(27,70),(566,70),(566,223)],fill='#93997a',width=1)
            for x,y in LIGHTS[mid][:3]:
                px,py=x*32+16,y*32-20
                draw.line((px,70,px,py),fill='#273c2d',width=2)
                draw.polygon([(px-7,py+6),(px-4,py),(px+4,py),(px+7,py+6)],fill='#485d44',outline='#172d21')
                draw.line((px-6,py+7,px+6,py+7),fill='#d4deb0',width=2)
            draw.line([(77,221),(95,237),(91,256),(118,266)],fill='#647960',width=3)
        if mid in [8,11,14,15,16]:
            x,y=(3,8) if mid==16 else (w-5,h-5)
            for n in range(11):
                px=x*32+r.randint(-8,26);py=y*32+r.randint(-12,24)
                draw.ellipse((px,py,px+r.randint(2,13),py+r.randint(2,5)),fill=(79,39,25,135))
        # Append composed tiles to a map-specific copy, preserving original sheets.
        additions=[];ground={};upper={}
        for y in range(h):
            for x in range(w):
                im=art.crop((x*32,y*32,x*32+32,y*32+32))
                if not im.getbbox():continue
                idx=x+y*w
                if (x,y) in blocks:
                    # furniture footprints collide; its upper extent is drawn normally.
                    pass
                # Composite floor-only cells into ground; object silhouettes use layer 1.
                original=m['data']['data'][idx+w*h]
                if original or m['data']['data'][idx+2*w*h]:
                    # Preserve all old furniture / overhead. Only ground patina is added.
                    continue
                tid=384+baseim.width//32*(baseim.height//32)+len(additions)
                additions.append((im,15 if (x,y) in blocks else 0,0 if (x,y) in blocks else 1))
                m['data']['data'][idx+w*h]=tid
        total=baseim.height+math.ceil(len(additions)/8)*32
        sheet=Image.new('RGBA',(256,total));sheet.alpha_composite(baseim)
        first=384+baseim.height//32*8
        for n,(im,p,pri) in enumerate(additions):sheet.alpha_composite(im,((n%8)*32,baseim.height+n//8*32))
        name='revision_mapa%02d'%mid
        (ROOT/'Graphics/Tilesets').mkdir(exist_ok=True);sheet.save(ROOT/'Graphics/Tilesets'/(name+'.png'))
        for key in ['passages','priorities','terrain_tags']:
            t=tileset[key];vals=t['data'][:first]+[0]*max(0,first-len(t['data']))
            vals += [p if key=='passages' else pri if key=='priorities' else 0 for _,p,pri in additions]
            t.update(xsize=len(vals),data=vals)
        tileset.update(id=51+mid,name='Revisión '+str(mid),tileset_name=name)
        m['tileset_id']=51+mid
        if mid>=12:tileset.update(fog_name='002-Clouds01',fog_opacity=14 if mid!=16 else 20,fog_zoom=200,fog_sx=1,fog_sy=0)
        patches['Map%03d'%mid]=m;patches['Tileset'+str(51+mid)]=tileset
        # Light mask is a world-anchored engine sprite, and is also used in previews.
        mask=Image.new('RGBA',(w*32,h*32));pix=mask.load()
        cold=mid in [6,7,8,9,11,13,14,15,16]
        for py in range(h*32):
            for px in range(w*32):
                glow=max(math.exp(-(((px-(x*32+16))/74)**2+((py-(y*32+18))/68)**2)/2) for x,y in LIGHTS[mid])
                edge=min(px,py,w*32-1-px,h*32-1-py)
                a=int((140 if mid==16 else 85)+max(0,28-edge)*1.2-(120 if mid==16 else 85)*glow)
                pix[px,py]=((7,24,17) if cold else (22,18,10))+ (max(0,min(150,a)),)
        mask.save(ROOT/'Graphics/Pictures'/('revision_luz%02d.png'%mid))
        report.append(dict(mapa=mid,antes=old,despues=[w,h],muebles=furniture,bloqueos=sorted(blocks),tiles=len(additions)))
    # Update every static inbound transfer to resized lab.
    for key,m in patches.items():
        if not key.startswith('Map'):continue
        for e in m['events'].values():
            for p in e['pages']:
                for c in p['list']:
                    if c['code']==201 and c['parameters'][1]==16:c['parameters'][2:4]=[10,12]
    (ROOT/'diseno/archivo/herramientas/revision_patch.json').write_text(json.dumps(patches,ensure_ascii=False),encoding='utf-8')
    (ROOT/'diseno/verificaciones/revision_mapas.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('16 mapas preparados; hojas originales conservadas. Laboratorio 500 -> 300 baldosas.')

if __name__ == "__main__":
    main()
