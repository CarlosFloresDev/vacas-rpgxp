"""Pasada 1–16: fuentes image_gen, composición CPU; jamás cambia índices de mapa.

prepare reconstruye y contrasta la distribución histórica solo en memoria.
install adapta arte generado y lo recorta en los índices ya existentes.
"""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import inspect, json, shutil, hashlib, sys
from pathlib import Path
from collections import deque
from PIL import Image, ImageChops, ImageFilter
from adaptar_arte import adapt, PALETTES, quantize

R = _ROOT
A = R/'diseno/fuentes/arte_hd2d/arte_mapas'
B = R/'diseno/respaldos/antes_arte_mapas'
RTP = Path('D:/SteamLibrary/steamapps/common/RPGXP/rtp/Graphics')
S = json.loads(((_ROOT / 'diseno/verificaciones/inventario/snapshot.json')).read_text(encoding='utf8'))
MANIFEST = {'assets': [], 'compositions': [], 'exceptions': []}
SPECS = []

def backup(p):
    rel = p.relative_to(R) if p.is_relative_to(R) else Path('RTP')/p.relative_to(RTP)
    q = B/rel
    if not q.exists():
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)
    return q

def zone(mid):
    return 'piso' if mid in (2,3,4,10,12) else 'matadero'

def prepare():
    import revision_mapas as rev
    placements = {}; floors = {}; afterprops = {}; captures = []
    def floor(mid, im): floors[mid] = im.copy()
    def prop(mid, kind, size, x, y):
        placements.setdefault(mid, []).append(dict(kind=kind,size=list(size),xy=[x,y]))
    def doneprops(mid, im): afterprops[mid] = im.copy()
    def capture(mid, sheet, md, art, baseheight):
        rel = Path('Graphics/Tilesets')/f'revision_mapa{mid:02}.png'
        old = Image.open(backup(R/rel)).convert('RGBA')
        assert sheet.size == old.size and sheet.tobytes() == old.tobytes(), f'Reconstrucción histórica distinta {mid}'
        assert md['data'] == S[f'Map{mid:03}']['data'], f'Índices distintos {mid}'
        floors[mid].save(A/f'floor_{mid:02}.png')
        afterprops[mid].save(A/f'props_old_{mid:02}.png')
        art.save(A/f'overlay_old_{mid:02}.png')
        captures.append(dict(map=mid,baseheight=baseheight,placements=placements.get(mid,[]),replay_exact=True))
    src = inspect.getsource(rev.main).split('        # Light mask')[0]
    src = src.replace('def main():','def replay():')
    src = src.replace('        protected=set()', '        record_floor(mid,art)\n        protected=set()')
    src = src.replace('            art.alpha_composite(im,(ox,oy));furniture+=1',
        '            record_prop(mid,k,im.size,ox,oy)\n            art.alpha_composite(im,(ox,oy));furniture+=1')
    src = src.replace('        # Low cables', '        record_doneprops(mid,art)\n        # Low cables')
    src = src.replace("sheet.save(ROOT/'Graphics/Tilesets'/(name+'.png'))", 'record_result(mid,sheet,m,art,baseim.height)')
    ns = dict(vars(rev),record_floor=floor,record_prop=prop,record_doneprops=doneprops,record_result=capture)
    exec(src, ns); ns['replay']()
    (A/'layout.json').write_text(json.dumps(captures,indent=2),encoding='utf8')
    for n in ['052-Carpet02','048-Water01','002-G_Shadow01','003-G_Ground01','005-G_Road01','006-G_Road02','050-Roof02']:
        backup(RTP/'Autotiles'/(n+'.png'))
    backup(RTP/'Characters/185-Light02.png')
    print('16 reconstrucciones idénticas, índices originales intactos; respaldos preparados.')

def adapted(spec):
    _, im = adapt(spec)
    SPECS.append(spec)
    return im

def components(im):
    alpha=im.getchannel('A'); w,h=im.size; pixels=alpha.load()
    pending={(x,y) for y in range(h) for x in range(w) if pixels[x,y]}
    while pending:
        x,y=pending.pop(); q=deque([(x,y)]); pts=[(x,y)]
        while q:
            x,y=q.popleft()
            for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)):
                p=(x+dx,y+dy)
                if p in pending:pending.remove(p);q.append(p);pts.append(p)
        yield min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts)+1,max(y for x,y in pts)+1

CACHE={}
KINDS={'archive':0,'rack':1,'shelf':2,'crate':3,'bench':4,'table':5,'gurney':6,'trash':7,
       'papers':8,'cable':9,'puddle':10,'blood':11,'lamp':12,'scraps':13,'bottles':14,'supply':15}

def prop(kind, size, z):
    key=(kind,tuple(size),z)
    if key in CACHE:return CACHE[key].copy()
    n=KINDS[kind]; src=Image.open(A/'props_fuente.png').convert('RGBA'); w,h=src.size
    box=[round(n%4*w/4),round(n//4*h/4),round((n%4+1)*w/4),round((n//4+1)*h/4)]
    if kind=='gurney':
        # Camilla aprobada de fase2: se sustituye solo su mancha PIL. La nueva
        # camilla horizontal girada perdía la lectura de cabecero y ruedas.
        source='Graphics/Characters/vacas_laboratorio.png'
        approved=Image.open(R/source);box=[0,0,approved.width//4,approved.height//4]
    else: source='diseno/fuentes/arte_hd2d/arte_mapas/props_fuente.png'
    if kind=='bench':
        # La generación nueva produjo un sofá. Se conserva la identidad banco
        # con el banco image_gen aprobado en la pasada 22–32.
        source='diseno/fuentes/arte_hd2d/arte_final/props_0_fuente.png'
        previous=Image.open(R/source);pw,ph=previous.size;box=[0,round(ph/4),round(pw/4),round(ph/2)]
    spec=dict(source=source,destination='Graphics/Characters/arte_mapas_intermedio.png',type='battler',size=list(size),
              max_height=max(size[1],1),padding=0,alpha_threshold=128,resample='box',zone=z)
    if box:spec['source_box']=box
    im=adapted(spec)
    if kind=='gurney':im.alpha_composite(prop('blood',(12,9),z),(10,23))
    CACHE[key]=im.copy()
    q=A/'adaptados'/z/f'{kind}_{size[0]}x{size[1]}.png';q.parent.mkdir(parents=True,exist_ok=True);im.save(q)
    return im

def scatter(old,z):
    result=Image.new('RGBA',old.size)
    for box in components(old):
        x,y,x1,y1=box; patch=old.crop(box); size=patch.size
        # El alfa antiguo clasifica papel (190), grietas (100) y humedad (50).
        values=list(patch.getdata()); occupied=[v for v in values if v[3]]
        mx=max(v[3] for v in occupied)
        kind='papers' if mx>=180 else 'cable' if mx>=90 else 'puddle'
        im=prop(kind,size,z)
        # Patina baja no compite con objetos interactivos ni aumenta su huella.
        if kind!='papers': im.putalpha(im.getchannel('A').point(lambda a:a//3))
        result.alpha_composite(im,(x,y))
    return result

def atlas_base(name, pages, size, z):
    layout=Image.open(B/'Graphics/Tilesets'/f'revision_mapa{2 if name=="hogar" else 4:02}.png').convert('RGBA').crop((0,0,*size))
    out=Image.new('RGBA',size)
    for label, top, bottom in pages:
        q=A/f'{name}_{label}_layout_native.png';layout.crop((0,top,size[0],bottom)).save(q)
        spec=dict(source=f'diseno/fuentes/arte_hd2d/arte_mapas/{name}_{label}_fuente.png',destination=f'Graphics/Tilesets/arte_mapas_{name}.png',
                  type='indexed',size=[size[0],bottom-top],cell='32x32',layout_source=str(q.relative_to(R)),
                  indexed_mode='resize',preserve_alpha=True,resample='box',padding=0,zone=z)
        if name=='calle' and label=='a':
            # La generación separó las bandas de materiales con alturas distintas.
            # Anclas vistas en la fuente: suelo0, muro440, canal616, mosaico880,
            # farol1165, base1430. La última banda pertenece a la página B.
            spec['source_box']=[0,0,1024,1430]
            spec['source_rows']=[0,112,225,332,440,528,616,704,792,880,975,1070,1165,1250,1335,1430]
        out.alpha_composite(adapted(spec),(0,top))
    return out

def lock_quarter_edges(old, new, z):
    """Iguala las aristas que ya eran idénticas en la topología original RGSS.

    No toma colores RTP: solo sus clases de equivalencia geométrica y su alfa.
    """
    w,h=old.size; parent={}; groups={}
    def find(a):
        parent.setdefault(a,a)
        if parent[a]!=a:parent[a]=find(parent[a])
        return parent[a]
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[b]=a
    for y in range(0,h,16):
        for x in range(0,w,16):
            for edge in ([(x+i,y) for i in range(16)],[(x+i,y+15) for i in range(16)],
                         [(x,y+i) for i in range(16)],[(x+15,y+i) for i in range(16)]):
                k=tuple(old.getpixel(p) for p in edge)
                if k in groups:
                    for a,b in zip(edge,groups[k]):union(a,b)
                else:groups[k]=edge
    sets={}
    for p in parent:sets.setdefault(find(p),[]).append(p)
    for points in sets.values():
        colors=[new.getpixel(p) for p in points]
        rgb=tuple(round(sum(c[k] for c in colors)/len(colors)) for k in range(3))
        for p in points:new.putpixel(p,(*rgb,old.getpixel(p)[3]))
    new=quantize(new,z)
    for y in range(0,h,16):
        for x in range(0,w,16):
            for edge in ([(x+i,y) for i in range(16)],[(x+i,y+15) for i in range(16)],
                         [(x,y+i) for i in range(16)],[(x+15,y+i) for i in range(16)]):
                k=tuple(old.getpixel(p) for p in edge)
                assert [new.getpixel(p) for p in edge]==[new.getpixel(p) for p in groups[k]]
    return new,len(sets)

def extras():
    global MANIFEST
    MANIFEST=json.loads((A/'manifest.json').read_text(encoding='utf8'))
    src=Image.open(A/'autotiles_fuente.png').convert('RGBA');w,h=src.size
    names=['052-Carpet02','048-Water01','002-G_Shadow01','003-G_Ground01','005-G_Road01','006-G_Road02','050-Roof02']
    for n,name in enumerate(names):
        layout=B/'RTP/Autotiles'/(name+'.png');old=Image.open(layout).convert('RGBA');z='piso'
        source=src.crop((round(n%4*w/4),round(n//4*h/2),round((n%4+1)*w/4),round((n//4+1)*h/2)))
        source=source.resize((96,128),Image.Resampling.BOX)
        if name=='048-Water01':
            animated=Image.new('RGBA',old.size)
            for frame,offset in enumerate([0,1,2,1]):
                v=source.copy();inner=source.crop((17,33,79,111));v.paste(ImageChops.offset(inner,offset,0),(17,33));animated.paste(v,(frame*96,0))
            source=animated
        q=A/(name+'_fuente_recortada.png');source.save(q)
        spec=dict(source=str(q.relative_to(R)).replace('\\','/'),destination=f'Graphics/Autotiles/{name}.png',
                  type='indexed',size=list(old.size),cell='16x16',layout_source=str(layout.relative_to(R)).replace('\\','/'),
                  indexed_mode='resize',preserve_alpha=True,padding=0,resample='box',zone=z)
        im=adapted(spec);im,classes=lock_quarter_edges(old,im,z)
        out=R/spec['destination'];out.parent.mkdir(parents=True,exist_ok=True);im.save(out)
        MANIFEST['assets']=[x for x in MANIFEST['assets'] if x['destination']!=spec['destination']]+[dict(spec,edge_equivalence_classes=classes,original_frames=old.width//96,source_atlas='diseno/fuentes/arte_hd2d/arte_mapas/autotiles_fuente.png')]
    old=B/'RTP/Characters/185-Light02.png'
    spec=dict(source='diseno/fuentes/arte_hd2d/arte_mapas/luz_fuente.png',destination='Graphics/Characters/185-Light02.png',
              type='indexed',size='128x256',cell='32x64',layout_source=str(old.relative_to(R)).replace('\\','/'),
              indexed_mode='fit',resample='box',padding=0,zone='piso')
    im=adapted(spec);(R/spec['destination']).parent.mkdir(parents=True,exist_ok=True);im.save(R/spec['destination'])
    MANIFEST['assets']=[x for x in MANIFEST['assets'] if x['destination']!=spec['destination']]+[spec]
    (A/'manifest.json').write_text(json.dumps(MANIFEST,ensure_ascii=False,indent=2),encoding='utf8')
    print('7 autotiles con alfa y equivalencias de aristas conservadas; bombilla 4x4 adaptada.')

def floors():
    manifest=json.loads((A/'manifest.json').read_text(encoding='utf8'))
    src=Image.open(A/'suelos_fuente.png');w,h=src.size
    tiles=[]
    for n in range(4):
        spec=dict(source='diseno/fuentes/arte_hd2d/arte_mapas/suelos_fuente.png',destination='Graphics/Tilesets/arte_mapas_intermedio.png',
                  source_box=[round(n%2*w/2),round(n//2*h/2),round((n%2+1)*w/2),round((n//2+1)*h/2)],
                  type='picture',size='32x32',resample='box',zone_direction='piso')
        im=adapted(spec).convert('RGBA')
        # Dos pares de bordes compartidos; mismo píxel en las cuatro esquinas.
        for i in range(32):
            for a,b in [((0,i),(31,i)),((i,0),(i,31))]:
                c=tuple(round((im.getpixel(a)[k]+im.getpixel(b)[k])/2) for k in range(3))+(255,)
                im.putpixel(a,c);im.putpixel(b,c)
        c=im.getpixel((0,0))
        for p in [(0,31),(31,0),(31,31)]:im.putpixel(p,c)
        # Rampas propias dirigidas por prompt: la paleta estricta de16 colores
        # convertía grises en motas ocres y borraba las juntas de las tablas.
        alpha=im.getchannel('A')
        im=im.convert('RGB').quantize(colors=32,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
        tiles.append(im)
        im.save(A/f'suelo_{n}.png')
    for mid,indices in [(2,{384:1,385:1,387:0,388:0}),(3,{384:1,385:1}),(4,{385:3,393:3,465:2})]:
        p=R/f'Graphics/Tilesets/revision_mapa{mid:02}.png';im=Image.open(p).convert('RGBA')
        for tid,n in indices.items():im.paste(tiles[n],((tid-384)%8*32,(tid-384)//8*32))
        im.save(p)
        entry=next(x for x in manifest['compositions'] if x['maps']==[mid])
        if 'diseno/fuentes/arte_hd2d/arte_mapas/suelos_fuente.png' not in entry['sources']:entry['sources'].append('diseno/fuentes/arte_hd2d/arte_mapas/suelos_fuente.png')
        entry['floor_corrections']={str(k):v for k,v in indices.items()}
    manifest['floor_adaptations']=SPECS
    (A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    print('9 índices de suelo corregidos: texturas sobrias con bordes opuestos idénticos.')

def corrections():
    manifest=json.loads((A/'manifest.json').read_text(encoding='utf8'))
    layouts=json.loads((A/'layout.json').read_text(encoding='utf8'))
    def paint(mid,atlas,image,xy,clear=False):
        md=S[f'Map{mid:03}'];w,h=md['width'],md['height'];ox,oy=xy
        for y in range(max(0,oy//32),min(h,(oy+image.height+31)//32)):
            for x in range(max(0,ox//32),min(w,(ox+image.width+31)//32)):
                tid=md['data']['data'][x+y*w+w*h]
                # La huella rectangular incluye celdas vacías omitidas por la
                # composición histórica; nunca se les asigna un índice nuevo.
                if tid<384+row['baseheight']//32*8:continue
                tx=(tid-384)%8*32;ty=(tid-384)//8*32
                tile=atlas.crop((tx,ty,tx+32,ty+32))
                x0,y0=max(ox,x*32),max(oy,y*32);x1,y1=min(ox+image.width,(x+1)*32),min(oy+image.height,(y+1)*32)
                patch=image.crop((x0-ox,y0-oy,x1-ox,y1-oy))
                if clear:tile.paste((0,0,0,0),(x0-x*32,y0-y*32,x1-x*32,y1-y*32))
                tile.alpha_composite(patch,(x0-x*32,y0-y*32));atlas.paste(tile,(tx,ty))
    for row in layouts:
        mid=row['map']
        if not any(p['kind']=='gurney' for p in row['placements']) and mid!=16:continue
        path=R/f'Graphics/Tilesets/revision_mapa{mid:02}.png';atlas=Image.open(path).convert('RGBA')
        for p in row['placements']:
            if p['kind']=='gurney':paint(mid,atlas,prop('gurney',p['size'],zone(mid)),p['xy'],True)
        if mid==16:
            raw=Image.open(A/'props_fuente.png');w,h=raw.size
            spec=dict(source='diseno/fuentes/arte_hd2d/arte_mapas/props_fuente.png',destination='Graphics/Characters/arte_mapas_intermedio.png',
                      source_box=[round(w*.067),round(h*.855),round(w*.19),round(h*.94)],
                      type='battler',size=[14,10],max_height=10,resample='box',padding=0,alpha_threshold=128,zone='matadero')
            shade=adapted(spec)
            for x,y in [(4,5),(9,5),(14,5)]:paint(mid,atlas,shade,(x*32+9,y*32-21))
        atlas.save(path)
        entry=next(e for e in manifest['compositions'] if e['maps']==[mid])
        if 'Graphics/Characters/vacas_laboratorio.png' not in entry['sources']:entry['sources'].append('Graphics/Characters/vacas_laboratorio.png')
    manifest['review_corrections']+=['Camilla girada descartada: se conserva camilla image_gen fase2 y se sustituye mancha PIL por sangre generada.',
        'Tres pantallas de lámpara generadas del laboratorio colocadas en la huella original; conducciones ancladas.']
    manifest['correction_adaptations']=SPECS
    (A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    print('Camillas legibles y tres lámparas corregidas en sus índices originales.')

def install():
    layouts=json.loads((A/'layout.json').read_text(encoding='utf8'))
    home=atlas_base('hogar',[('a',0,416),('b',416,832)],(256,832),'piso')
    street=atlas_base('calle',[('a',0,480),('b',480,960)],(256,960),'piso')
    stats=[]
    for row in layouts:
        mid=row['map']; md=S[f'Map{mid:03}']; w,h=md['width'],md['height'];z=zone(mid)
        path=R/f'Graphics/Tilesets/revision_mapa{mid:02}.png'; old=Image.open(backup(path)).convert('RGBA');out=old.copy()
        if mid in (2,3):out.paste(home,(0,0))
        if mid==4:out.paste(street,(0,0))
        bg=Image.open(A/f'floor_{mid:02}.png').convert('RGBA'); new=scatter(bg,z)
        for p in row['placements']:new.alpha_composite(prop(p['kind'],p['size'],z),tuple(p['xy']))
        before=Image.open(A/f'props_old_{mid:02}.png').convert('RGBA')
        after=Image.open(A/f'overlay_old_{mid:02}.png').convert('RGBA')
        delta=ImageChops.difference(before,after); mask=delta.convert('RGB').convert('L').point(lambda v:255 if v else 0)
        # Conducciones/cables conservan su geometría; superficie obtenida de la fuente generada.
        for box in components(Image.merge('RGBA',(*delta.split()[:3],mask))):
            patch=after.crop(box); x,y,x1,y1=box
            material=prop('blood' if max(patch.getdata(),key=lambda p:p[0])[0]>70 and y>h*16 else 'cable',patch.size,z)
            material=material.resize(patch.size,Image.Resampling.NEAREST)
            # Material opaco extendido: no convertir cables finos en halos negros.
            rgb=material.convert('RGB');fill=rgb.filter(ImageFilter.MaxFilter(3)).convert('RGBA')
            fill.putalpha(mask.crop(box)); new.alpha_composite(fill,(x,y))
        baseend=384+row['baseheight']//32*8; changed=0
        for y in range(h):
            for x in range(w):
                tid=md['data']['data'][x+y*w+w*h]
                if tid<baseend:continue
                tile=new.crop((x*32,y*32,x*32+32,y*32+32));tx=(tid-384)%8*32;ty=(tid-384)//8*32
                out.paste(tile,(tx,ty));changed+=1
        out.save(path)
        stats.append(dict(map=mid,replaced_overlay_tiles=changed,generated_props=len(row['placements']),base='home' if mid in (2,3) else 'street' if mid==4 else 'approved_industrial_preserved'))
        MANIFEST['compositions'].append(dict(destination=str(path.relative_to(R)).replace('\\','/'),sources=['diseno/fuentes/arte_hd2d/arte_mapas/props_fuente.png']+(['diseno/fuentes/arte_hd2d/arte_mapas/hogar_a_fuente.png','diseno/fuentes/arte_hd2d/arte_mapas/hogar_b_fuente.png'] if mid in (2,3) else ['diseno/fuentes/arte_hd2d/arte_mapas/calle_a_fuente.png','diseno/fuentes/arte_hd2d/arte_mapas/calle_b_fuente.png'] if mid==4 else ['Graphics/Tilesets/vacas_matadero.png']),method='arte_mapas.py: adaptación de objetos a huellas históricas; recorte a los índices exactos ya existentes',maps=[mid]))
    MANIFEST['stats']=stats
    for entry,row in zip(MANIFEST['compositions'],layouts):
        if any(p['kind']=='bench' for p in row['placements']):entry['sources'].append('diseno/fuentes/arte_hd2d/arte_final/props_0_fuente.png')
    MANIFEST['review_corrections']=['Sofá nuevo descartado para bancos: se usa el banco image_gen aprobado de22–32.',
        'Bandas del atlas calle A ancladas explícitamente; sin desplazar índices.',
        'Suelo de2–4 readaptado con rampas de32 colores sin dithering para conservar juntas y grises.']
    (A/'manifest.json').write_text(json.dumps(MANIFEST,ensure_ascii=False,indent=2),encoding='utf8')
    (A/'adaptaciones.json').write_text(json.dumps(SPECS,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(stats))

if __name__=='__main__':
    {'prepare':prepare,'install':install,'extras':extras,'floors':floors,'corrections':corrections}[sys.argv[1]]()
