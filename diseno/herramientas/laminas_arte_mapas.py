"""Comparativas reales a 1x y comprobaciones de gráficos / pasos direccionales."""
import json, hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
R=Path(__file__).resolve().parents[2]; A=R/'diseno/arte_hd2d/arte_mapas'; C=R/'diseno/capturas';B=R/'diseno/respaldos/antes_arte_mapas'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
current=json.loads((R/'diseno/herramientas/snapshot.json').read_text(encoding='utf8'))
before=json.loads((B/'snapshot.json').read_text(encoding='utf8'))
report={'errors':[],'maps':[],'autotiles':[],'directional_steps':0}
manifest=json.loads((A/'manifest.json').read_text(encoding='utf8'))
for mid in range(1,17):
    old=Image.open(C/f'arte_mapas_antes_{mid:02}.png').convert('RGBA')
    new=Image.open(C/f'arte_mapas_despues_{mid:02}.png').convert('RGBA')
    assert old.size==new.size
    sheet=Image.new('RGB',(old.width*2,old.height+30),'#182025');d=ImageDraw.Draw(sheet)
    d.text((8,6),f'Mapa {mid:02} | ANTES | 1x',font=font,fill='white')
    d.text((8+old.width,6),'DESPUÉS | 1x | mismos índices y eventos',font=font,fill='white')
    sheet.paste(old,(0,30),old);sheet.paste(new,(old.width,30),new)
    sheet.save(C/f'arte_mapas_comparacion_{mid:02}.png')
    # Las dos vistas reciben exactamente la misma máscara existente.
    light=Image.open(R/f'Graphics/Pictures/revision_luz{mid:02}.png').convert('RGBA')
    for tag,im in [('antes',old),('despues',new)]:
        im=im.copy();im.alpha_composite(light);im.save(C/f'arte_mapas_luz_{tag}_{mid:02}.png')
    ts=current['Tilesets'][current[f'Map{mid:03}']['tileset_id']]
    name=ts['tileset_name'];p=R/f'Graphics/Tilesets/{name}.png';q=B/p.relative_to(R)
    a,b=Image.open(q).convert('RGBA'),Image.open(p).convert('RGBA')
    assert a.size==b.size and b.width==256 and b.height%32==0
    assert current[f'Map{mid:03}']==before[f'Map{mid:03}']
    used=set(current[f'Map{mid:03}']['data']['data'])
    for e in current[f'Map{mid:03}']['events'].values():
        used.update(p['graphic']['tile_id'] for p in e['pages'])
    assert all(t<384 or t-384<b.width//32*(b.height//32) for t in used)
    report['maps'].append(dict(map=mid,tileset=name,size=list(b.size),same_map=True,used_tiles=len(used),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
for spec in manifest['assets']:
    if '/Autotiles/' not in spec['destination']:continue
    old=Image.open(R/spec['layout_source']).convert('RGBA');new=Image.open(R/spec['destination']).convert('RGBA')
    assert old.size==new.size and old.getchannel('A').tobytes()==new.getchannel('A').tobytes()
    # Comprueba las mismas clases geométricas de las cuatro aristas de cada cuarto.
    edges={};count=0
    for y in range(0,old.height,16):
        for x in range(0,old.width,16):
            for pts in [[(x+i,y) for i in range(16)],[(x+i,y+15) for i in range(16)],[(x,y+i) for i in range(16)],[(x+15,y+i) for i in range(16)]]:
                key=tuple(old.getpixel(p) for p in pts);v=tuple(new.getpixel(p) for p in pts)
                if key in edges:assert edges[key]==v;count+=1
                else:edges[key]=v
    report['autotiles'].append(dict(path=spec['destination'],same_alpha=True,same_size=True,matching_quarter_edges=count,frames=new.width//96))
ns={};src=(R/'diseno/herramientas/auditar_accesos.py').read_text(encoding='utf8').split('issues=set()')[0]
# Una sola tabla global por clase; cada Grid captura sus datos al construirse.
ns={'__file__':str(R/'diseno/herramientas/auditar_accesos.py')};exec(src,ns)
states=[('inicio',set(),{},False),('avanzado',set(range(1,151)),{i:100 for i in range(1,40)},False),('inicio_self',set(),{},True),('avanzado_self',set(range(1,151)),{i:100 for i in range(1,40)},True)]
for mid in range(1,17):
    for label,sw,var,self_on in states:
        ns['S']=before;a=ns['Grid'](mid,sw,var,self_on)
        ns['S']=current;b=ns['Grid'](mid,sw,var,self_on)
        for y in range(a.m['height']):
            for x in range(a.m['width']):
                for direction in (2,4,6,8):
                    assert a.step(x,y,direction)==b.step(x,y,direction),(mid,label,x,y,direction)
                    report['directional_steps']+=1
report['result']='OK'
(R/'diseno/verificacion_arte_mapas.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'maps':16,'autotiles':7,'directional_steps':report['directional_steps'],'errors':report['errors']}))
