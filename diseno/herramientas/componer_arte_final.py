"""Compone hojas con arte generado; PIL solo recorta, escala y compone, no dibuja utilería."""
import json,copy,random,math
from PIL import Image
from instalar_arte_final import R,A,B,backup,write_image
from adaptar_arte import adapt
import maps5 as m
old_draw=m.draw
maps=copy.deepcopy(m.M)
import maps6
maps.update(copy.deepcopy(m.M))
base_draw=m.draw
initial=B/'snapshot_inicial.json'
if not initial.exists():initial.write_bytes((R/'diseno/herramientas/snapshot.json').read_bytes())
S=json.loads(initial.read_text(encoding='utf8'))
kinds=json.loads((A/'props_indices.json').read_text(encoding='utf8'))
intermediates=[]
cache={}
def generated(kind,size,zone):
 key=(kind,size,zone)
 if key in cache:return cache[key].copy()
 if kind=='throne':
  source=A/'trono_fuente.png';box=None
 elif kind in ('bed','cabinet','stove','tv'):
  source=A/'hogar_fuente.png';n=['bed','cabinet','stove','tv'].index(kind);im=Image.open(source);cw,ch=im.width/2,im.height/2
  box=[round(n%2*cw),round(n//2*ch),round((n%2+1)*cw),round((n//2+1)*ch)]
 else:
  n=kinds.index(kind);source=A/f'props_{n//16}_fuente.png';n%=16;im=Image.open(source);cw,ch=im.width/4,im.height/4
  box=[round(n%4*cw),round(n//4*ch),round((n%4+1)*cw),round((n//4+1)*ch)]
 spec=dict(source=str(source.relative_to(R)),destination='Graphics/Characters/arte_final_intermedio.png',type='battler',size=list(size),max_height=size[1],padding=0,alpha_threshold=128,resample='box',zone=zone)
 if box:spec['source_box']=box
 _,im=adapt(spec)
 cache[key]=im
 out=A/'objetos_adaptados'/zone/(kind+'.png');out.parent.mkdir(parents=True,exist_ok=True);im.save(out)
 intermediates.append(dict(kind=kind,size=list(size),zone=zone,adapter_spec=spec,output=str(out.relative_to(R)).replace('\\','/')))
 return im.copy()
patches={}
stats=[]
for tsid,ids in [(69,range(22,28)),(70,range(28,33))]:
 ts=copy.deepcopy(S['Tilesets'][tsid]);path=R/'Graphics/Tilesets'/(ts['tileset_name']+'.png')
 backup(path)
 atlas=Image.open(B/path.relative_to(R)).convert('RGBA')
 tiles=[atlas.crop((x*32,y*32,x*32+32,y*32+32)) for y in range(atlas.height//32) for x in range(8)]
 first={};variants={};added=0;changes=0
 for mid in ids:
  md=copy.deepcopy(S[f'Map{mid:03}']);props=maps[mid]['props'];layers=[Image.new('RGBA',(640,480)) for _ in range(3)]
  for n,(typ,kind,x,y,dx,dy,block,flip) in enumerate(props):
   # Original draw evaluated only for historical dimensions, never saved as new art.
   old=base_draw(kind,random.Random(mid*1000+n));size=old.size;zone='piso' if mid in (26,30) else 'alcantarillas' if mid in (28,31,32) else 'matadero'
   newkind='throne' if mid==32 and kind=='sofa' and x==9 and y==5 else kind
   if newkind=='throne':size=(60,64)
   if newkind in kinds or newkind in ('throne','bed','cabinet','stove','tv'):
    im=generated(newkind,size,zone)
   else:im=old  # Objetos con fuente image_gen aprobada, nunca sustitutos geométricos.
   if flip:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   px=x*32+dx+(max(0,(32-im.width)//2) if im.width<32 else 0);py=y*32+32-im.height+dy
   if typ=='O':px,py=x*32+dx,y*32+dy
   px=max(0,min(640-im.width,px));py=max(0,min(480-im.height,py))
   layers[0 if typ=='D' else 2 if typ=='O' else 1].alpha_composite(im,(px,py))
  composed=layers[0];composed.alpha_composite(layers[1]);composed.alpha_composite(layers[2])
  for y in range(15):
   for x in range(20):
    idx=x+y*20+600;oldid=md['data']['data'][idx];im=composed.crop((x*32,y*32,x*32+32,y*32+32))
    if oldid==0 and not im.getchannel('A').getbbox():continue
    if oldid and oldid<448:raise ValueError('L2 inesperada '+str((mid,x,y,oldid)))
    b=im.tobytes();key=(oldid,b)
    if key in variants:newid=variants[key]
    elif oldid and oldid not in first:
     first[oldid]=b;tiles[oldid-384]=im;newid=oldid;variants[key]=newid
    else:
     newid=384+len(tiles);tiles.append(im);added+=1;variants[key]=newid
     for field,value in [('passages',ts['passages']['data'][oldid] if oldid else 0),('priorities',ts['priorities']['data'][oldid] if oldid else 1),('terrain_tags',ts['terrain_tags']['data'][oldid] if oldid else 0)]:
      table=ts[field];table['data'].extend([0]*(newid+1-len(table['data'])));table['data'][newid]=value;table['xsize']=len(table['data'])
    if newid!=oldid:md['data']['data'][idx]=newid;changes+=1
  patches[f'Map{mid:03}']=md
 out=Image.new('RGBA',(256,math.ceil(len(tiles)/8)*32))
 for i,tile in enumerate(tiles):out.alpha_composite(tile,(i%8*32,i//8*32))
 write_image(path,out);patches[f'Tileset{tsid}']=ts
 stats.append(dict(tileset=tsid,appended_tiles=added,changed_map_cells=changes,size=list(out.size)))
# Autotile propio con máscara/topología RGSS heredada, no texturas RTP.
wall=dict(source='diseno/arte_hd2d/arte_final/pared_autotile_fuente.png',destination='Graphics/Autotiles/053-Wall01.png',type='indexed',size='96x128',cell='32x32',source_grid=[3,4],layout_source='D:/SteamLibrary/steamapps/common/RPGXP/rtp/Graphics/Autotiles/053-Wall01.png',indexed_mode='resize',padding=0,alpha_threshold=128,resample='box',zone='alcantarillas')
p,im=adapt(wall);write_image(p,im)
(A/'objetos_adaptaciones.json').write_text(json.dumps(dict(adaptations=intermediates,stats=stats),ensure_ascii=False,indent=2),encoding='utf8')
manifest=json.loads((A/'manifest.json').read_text(encoding='utf8'))
manifest['assets']=[a for a in manifest['assets'] if a['destination']!=wall['destination']]+[wall]
manifest['compositions']=[dict(destination=f'Graphics/Tilesets/{S["Tilesets"][tsid]["tileset_name"]}.png',sources=['Graphics/Tilesets/vacas_matadero.png']+[str(p.relative_to(R)).replace('\\','/') for p in A.glob('props_*fuente.png')]+['diseno/arte_hd2d/arte_final/hogar_fuente.png','diseno/arte_hd2d/arte_final/trono_fuente.png'],method='componer_arte_final.py; objetos adaptados con adaptar_arte.py; preserve tile flags',maps=list(ids)) for tsid,ids in [(69,range(22,28)),(70,range(28,33))]]
(A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
(R/'diseno/herramientas/arte_final_patch.json').write_text(json.dumps(patches,ensure_ascii=False),encoding='utf8')
print(json.dumps(stats))

