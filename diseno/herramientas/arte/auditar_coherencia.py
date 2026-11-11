"""Auditoría reproducible de TODOS los PNG. Solo lee Graphics/Data.

python -X utf8 diseno/herramientas/arte/auditar_coherencia.py --inicial
python -X utf8 diseno/herramientas/arte/auditar_coherencia.py
Las métricas no certifican perspectiva, identidad ni calidad artística.
"""
from pathlib import Path
import argparse, collections, hashlib, json, os, re, subprocess
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'diseno/verificaciones'
BACK = ROOT/'diseno/respaldos/antes_coherencia_arte'
RTP = Path(os.environ.get('RPGMAKER_RTP_PATH', 'D:/SteamLibrary/steamapps/common/RPGXP/rtp'))/'Graphics'
PROPS = {'vacas_muebles','vacas_cosas','vacas_laboratorio','vacas_matadero','vacas_alcantarilla','vacas_tablon','vacas_puerta','vacas_vacio','185-Light02','vacas_luz_escalera'}
COWS = {'vacas_vaca','vacas_vaca_canela','vacas_guernsey4','vacas_junco','vacas_muesca'}
COWS |= {'vacas_guernsey4_80','vacas_junco_80','vacas_muesca_80'}
LEGACY_GENERATED={'Graphics/Autotiles/'+n+'.png' for n in ('002-G_Shadow01','003-G_Ground01','005-G_Road01','006-G_Road02','048-Water01','050-Roof02','052-Carpet02','053-Wall01')}|{'Graphics/Characters/185-Light02.png','Graphics/Fogs/002-Clouds01.png'}
FIELDS = dict(character_name='Characters',battler_name='Battlers',tileset_name='Tilesets',panorama_name='Panoramas',fog_name='Fogs',battleback_name='Battlebacks',windowskin_name='Windowskins',title_name='Titles',gameover_name='Gameovers',icon_name='Icons',animation_name='Animations')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')

def references():
    subprocess.run(['node',str(ROOT/'diseno/herramientas/arte/leer_usos_coherencia.mjs')],cwd=ROOT,check=True)
    data=json.loads((OUT/'coherencia_datos_lectura.json').read_text(encoding='utf8'))
    refs=collections.defaultdict(list)
    def add(cat,name,path,mapid=None):
        if isinstance(name,str) and name: refs[f'Graphics/{cat}/{name}.png'].append(dict(ruta=path,mapa=mapid))
    def walk(x,path,mapid=None):
        if isinstance(x,dict):
            for k,v in x.items():
                if k in FIELDS: add(FIELDS[k],v,path+'.'+k,mapid)
                if k=='autotile_names':
                    for i,n in enumerate(v): add('Autotiles',n,f'{path}.{k}[{i}]',mapid)
            code,p=x.get('code'),x.get('parameters',[])
            if x.get('_class')=='RPG::MoveCommand' and code==41 and p: add('Characters',p[0],path+'.parameters[0]',mapid)
            if x.get('_class')=='RPG::EventCommand':
                if code==231 and len(p)>1: add('Pictures',p[1],path+'.parameters[1]',mapid)
                if code==322 and len(p)>4:
                    add('Characters',p[1],path+'.parameters[1]',mapid); add('Battlers',p[3],path+'.parameters[3]',mapid)
                if code==204 and len(p)>1: add({0:'Panoramas',1:'Fogs',2:'Battlebacks'}.get(p[0],'Pictures'),p[1],path+'.parameters[1]',mapid)
            for k,v in x.items():
                if k not in ('data','passages','priorities','terrain_tags'): walk(v,path+'.'+k,mapid)
        elif isinstance(x,list):
            for i,v in enumerate(x): walk(v,f'{path}[{i}]',mapid)
        elif isinstance(x,str):
            for name in re.findall(r'\\P\[([^\]]+)\]',x,re.I): add('Pictures','retrato_'+name,path,mapid)
    for key,value in data.items():
        m=re.fullmatch(r'Map(\d+)',key); mid=int(m[1]) if m else None
        walk(value,key,mid)
        if mid: walk(data['Tilesets'][value['tileset_id']],f'{key}.Tilesets[{value["tileset_id"]}]',mid)
    # Fuentes Ruby de solo lectura; además se indican las referencias dinámicas no resolubles.
    for p in (ROOT/'diseno/scripts').rglob('*.rb'):
        s=p.read_text(encoding='utf8',errors='replace')
        for method,name in re.findall(r"Cache\.(picture|battler|character|battleback|windowskin|icon|fog|panorama|autotile|tileset|animation|title|gameover)\s*\(\s*['\"]([^'\"]+)['\"]",s):
            cat={'picture':'Pictures','character':'Characters','battler':'Battlers','battleback':'Battlebacks','windowskin':'Windowskins','icon':'Icons','fog':'Fogs','panorama':'Panoramas','autotile':'Autotiles','tileset':'Tilesets','animation':'Animations','title':'Titles','gameover':'Gameovers'}[method]
            add(cat,name,p.relative_to(ROOT).as_posix())
    dump(OUT/'coherencia_usos.json',refs)
    return refs

def measure(p,refs):
    rel=p.relative_to(ROOT).as_posix(); cat=p.parent.name
    im=Image.open(p).convert('RGBA'); a=np.array(im); mask=a[:,:,3]>127
    pix=a[:,:,:3][mask].astype(float); warnings=[]
    if len(pix):
        hi=pix.max(1); lo=pix.min(1)
        sat=np.divide(hi-lo,hi,out=np.zeros_like(hi),where=hi!=0)
        bright=pix@np.array([.2126,.7152,.0722])/255
        # Colores empaquetados: evita millones de tuplas Python en atlas grandes.
        rgb=pix.astype(np.uint32)
        packed=(rgb[:,0]<<16)|(rgb[:,1]<<8)|rgb[:,2]
        colors,counts=np.unique(packed,return_counts=True)
        order=np.lexsort((colors,-counts))[:16]
        stats=dict(colores=len(colors),saturacion_media=round(float(sat.mean()),4),brillo_medio=round(float(bright.mean()),4),paleta_principal=[{'hex':'#%06x'%int(colors[i]),'pixeles':int(counts[i])} for i in order])
    else: stats=dict(colores=0,saturacion_media=0,brillo_medio=0,paleta_principal=[])
    semi=(a[:,:,3]>0)&(a[:,:,3]<255)
    stats['semitransparentes']=int(semi.sum());stats['fraccion_semitransparente']=round(float(semi.sum()/max(1,(a[:,:,3]>0).sum())),5)
    frames=[];grid=None
    if cat=='Characters': grid=(4,4)
    elif cat=='Tilesets': grid=(8,im.height//32)
    elif cat=='Icons': grid=(1,1)
    elif cat=='Animations': grid=(5,im.height//192)
    elif cat=='Autotiles': grid=(im.width//32,im.height//32)
    if grid and all(grid):
        cols,rows=grid; cw,ch=im.width//cols,im.height//rows
        if cat=='Animations':cw=ch=192
        if im.width%cols or im.height%rows: warnings.append('rejilla_no_entera')
        for y in range(rows):
            for x in range(cols):
                cell=Image.fromarray((mask[y*ch:(y+1)*ch,x*cw:(x+1)*cw]*255).astype('uint8')); b=cell.getbbox()
                frames.append(dict(indice=y*cols+x,fila=y,columna=x,bbox=b,ancho=b[2]-b[0] if b else 0,altura=b[3]-b[1] if b else 0,margen_inferior=ch-b[3] if b else None))
    if cat=='Tilesets' and (im.width!=256 or im.height%32):warnings.append('geometria_tileset')
    if cat=='Autotiles' and not ((im.height==128 and im.width%96==0) or im.size==(32,32)):warnings.append('geometria_autotile')
    if cat=='Animations' and (im.width!=960 or im.height%192):warnings.append('geometria_animacion')
    is_human=cat=='Characters' and p.stem not in PROPS|COWS|{'vacas_furgoneta','vacas_perro'}
    if is_human and any(f['altura'] and not 34<=f['altura']<=48 for f in frames):warnings.append('altura_humana_fuera_34_48')
    if cat=='Characters' and p.stem in COWS:
        if any(f['altura']>52 or f['ancho']>68 for f in frames):warnings.append('bovino_excede_68x52')
        if any(f['ancho'] and f['ancho']<54 for f in frames if f['fila'] in (1,2)):
            warnings.append('bovino_longitud_adulta_menor_54_pendiente_DATA')
    if cat in ('Characters','Tilesets','Icons','Autotiles') and stats['fraccion_semitransparente']>.01 and p.stem not in ('185-Light02','vacas_luz_escalera'):warnings.append('alpha_parcial_en_pixel_art')
    if cat in ('Characters','Tilesets','Autotiles','Icons') and stats['saturacion_media']>.55:warnings.append('saturacion_media_mayor_055')
    rtp=RTP/cat/p.name
    rtp_exact=rtp.exists() and sha(p)==sha(rtp)
    rtp_derived=p.stem.startswith('vacas_rejilla_')
    probable=bool(re.match(r'^\d{3}-',p.stem))
    if rtp_exact or (probable and rel not in LEGACY_GENERATED):warnings.append('RTP_original' if rtp_exact else 'nombre_RTP_revisar_procedencia')
    if rtp_derived:warnings.append('RTP_derivado_geometria_corregida')
    backup=BACK/rel
    if backup.exists() and Image.open(backup).size!=im.size:warnings.append('dimension_reemplazo_alterada')
    if cat=='Characters' and backup.exists() and Image.open(backup).size==im.size:
        old=Image.open(backup).convert('RGBA');cw,ch=im.width//4,im.height//4
        for f in frames:
            x,y=f['columna']*cw,f['fila']*ch
            b=old.crop((x,y,x+cw,y+ch)).getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
            f['ancla_original']=b[3] if b else None
            f['ancla_actual']=f['bbox'][3] if f['bbox'] else None
        if any(f['ancla_original']!=f['ancla_actual'] for f in frames):warnings.append('ancla_original_alterada')
    if cat=='Characters' and p.stem not in PROPS and frames:
        cw,ch=im.width//4,im.height//4
        rowframes=[im.crop((0,y*ch,cw,(y+1)*ch)).tobytes() for y in range(4)]
        if len(set(rowframes))<4:warnings.append('direcciones_identicas')
    return dict(archivo=rel,tamano=list(im.size),sha256=sha(p),rejilla=list(grid) if grid else None,celda=([192,192] if cat=='Animations' else [im.width//grid[0],im.height//grid[1]]) if grid and all(grid) else None,frames=frames,metricas=stats,rtp=dict(hash_identico=rtp_exact,nombre_convencional=probable,derivado=rtp_derived,arte_propio_nombre_heredado=rel in LEGACY_GENERATED),usos=refs.get(rel,[]),avisos=warnings,estado='REVISAR' if warnings else 'METRICAS_OK',validacion_visual='No inferible de métricas; consultar COHERENCIA_ARTE.md')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inicial',action='store_true');args=parser.parse_args()
    refs=references();files=[measure(p,refs) for p in sorted((ROOT/'Graphics').rglob('*.png'))]
    report=dict(alcance='Todos los PNG locales; Marshal actual en solo lectura. Referencias dinámicas pueden requerir revisión en motor.',reglas=dict(humano_altura=[34,48],bovino_maximo=[68,52],bovino_longitud_lateral_minima=54,saturacion_pixelart_max=.55,alpha_pixelart_max=.01),total=len(files),con_avisos=sum(bool(x['avisos']) for x in files),archivos=files)
    dest=OUT/('auditoria_coherencia_arte_antes.json' if args.inicial else 'auditoria_coherencia_arte.json')
    if args.inicial and dest.exists(): raise SystemExit('Ya existe auditoría inicial; no se sobrescribe.')
    dump(dest,report)
    print(json.dumps({'total':report['total'],'con_avisos':report['con_avisos'],'avisos':dict(collections.Counter(w for f in files for w in f['avisos']))},ensure_ascii=False))

if __name__=='__main__':main()
