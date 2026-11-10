"""Referencias gráficas/audio de scripts y manifiestos, sin ejecutar Ruby."""
from pathlib import Path
import json, os, re
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Game.rxproj').exists())

def comprobar():
    snapshot=json.loads((ROOT/'diseno/verificaciones/inventario/snapshot.json').read_text(encoding='utf8'))
    rtp=Path(os.environ.get('RPGMAKER_RTP_PATH','D:/SteamLibrary/steamapps/common/RPGXP/rtp'))
    errors=[];references=set();manifest_paths=0
    folders={'picture':'Pictures','icon':'Icons','character':'Characters','battler':'Battlers','battleback':'Battlebacks','windowskin':'Windowskins','title':'Titles','gameover':'Gameovers','autotile':'Autotiles','tileset':'Tilesets','animation':'Animations','fog':'Fogs','panorama':'Panoramas','transition':'Transitions'}
    for entry in snapshot['Scripts']:
        code=entry['code']
        for kind,name in re.findall(r'RPG::Cache\.(\w+)\(\s*[\"\']([^\"\']+)[\"\']\s*(?=[,)])',code):
            if kind in folders:references.add('Graphics/'+folders[kind]+'/'+name)
        for kind,name in re.findall(r'=>\s*\[:(bgm|bgs|me|se),\s*[\"\']([^\"\']+)[\"\']',code):references.add('Audio/'+kind.upper()+'/'+name)
    def portraits(value):
        if isinstance(value,str):
            for name in re.findall(r'\\P\[([^\]]+)\]',value):
                if re.fullmatch(r'[a-zA-Z0-9_]+',name):references.add('Graphics/Pictures/retrato_'+name)
        elif isinstance(value,dict):
            for item in value.values():portraits(item)
        elif isinstance(value,list):
            for item in value:portraits(item)
    for key,value in snapshot.items():
        if key!='Scripts':portraits(value)
    # Familias de nombres calculados en los scripts instalados.
    references.update('Graphics/Pictures/revision_luz%02d'%i for i in range(1,17))
    references.update('Graphics/Pictures/acto5_luz%02d'%i for i in range(22,28))
    references.update('Graphics/Pictures/acto6_luz%02d'%i for i in range(28,33))
    references.update('Graphics/Pictures/screamer_%d'%i for i in range(1,14))
    references.update('Graphics/Battlebacks/mente_'+zone for zone in ('piso','matadero','tunel'))
    for reference in sorted(references):
        found=any(p.is_file() for base in (ROOT,rtp) for p in (base/Path(reference).parent).glob(Path(reference).name+'.*'))
        if not found and not (ROOT/reference).is_file():errors.append(reference)
    for manifest in (ROOT/'diseno/fuentes').rglob('manifest.json'):
        data=json.loads(manifest.read_text(encoding='utf-8-sig'))
        for entry in data if isinstance(data,list) else data.get('assets',[]):
            for key in ('source','destination','expression_base'):
                value=entry.get(key)
                if isinstance(value,str) and value.startswith(('diseno/','Graphics/','Audio/')):
                    manifest_paths+=1
                    if not (ROOT/value).is_file():errors.append(str(manifest.relative_to(ROOT))+': '+value)
    return {'referencias_scripts':len(references),'rutas_manifiestos':manifest_paths,'errores':errors,'alcance':'Literales Cache/audio, retratos de eventos y familias dinámicas propias; complementa validate_assets de datos. No ejecuta el juego.'}

if __name__=='__main__':
    report=comprobar();print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(report['errores']))
