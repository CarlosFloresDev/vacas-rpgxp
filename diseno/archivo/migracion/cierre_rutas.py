"""Cierre de migración: rutas JSON de Windows y módulos comunes (una sola vez)."""
from pathlib import Path
import json,re,shutil
root=next(p for p in Path(__file__).resolve().parents if (p/'Game.rxproj').exists())
mapping=json.loads((root/'diseno/verificaciones/traslados.json').read_text(encoding='utf8'))
updated=[]
def relocate(value):
    normalized=value.replace('\\','/')
    absolute=normalized.lower().startswith(root.as_posix().lower()+'/')
    key=normalized[len(root.as_posix())+1:] if absolute else normalized
    if not key.startswith('diseno/') or key.startswith(('diseno/respaldos/','diseno/archivo/')):return value
    dest=mapping.get(key)
    if dest is None and key.startswith('diseno/capturas/') and len(Path(key).parts)==3:
        name=Path(key).name;theme='interfaz' if name.startswith('ui_') else 'actos' if name.startswith(('acto','mapa')) else 'arte'
        dest='diseno/capturas/'+theme+'/'+name
    if dest is None:
        for folder in ('arte_hd2d','arte_provisional','audio_fuentes','marca'):
            if key.startswith('diseno/'+folder+'/'):dest='diseno/fuentes/'+key.removeprefix('diseno/');break
    if dest is None:return value
    return (root/dest).as_posix() if absolute else dest
def walk(value):
    if isinstance(value,str):return relocate(value)
    if isinstance(value,list):return [walk(v) for v in value]
    if isinstance(value,dict):return {k:walk(v) for k,v in value.items()}
    return value
for p in (root/'diseno').rglob('*.json'):
    if 'respaldos' in p.parts or 'inventario' in p.parts or p.name in ('inventario_antes.json','traslados.json'):continue
    try:data=json.loads(p.read_text(encoding='utf-8-sig'))
    except (ValueError,UnicodeError):continue
    result=walk(data)
    if result!=data:
        p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');updated.append(p.relative_to(root).as_posix())
tools=root/'diseno/herramientas'
for p in tools.rglob('*.py'):
    text=p.read_text(encoding='utf8')
    if 'from rutas import preparar_imports' not in text:continue
    text=text.replace('from rutas import preparar_imports','from rutas import ROOT as _ROOT, preparar_imports')
    text=text.replace("next(p for p in Path(__file__).resolve().parents if (p / 'Game.rxproj').is_file())",'_ROOT')
    text=text.replace('_tools.parent.parent /','_ROOT /')
    if p.name=='verificar_audio.py':
        text=text.replace("File.binread('diseno/scripts/12_interfaz.rb'); puts 'OK'", "File.binread('diseno/scripts/12_interfaz.rb').sub(/\\A# === VACAS: FUENTE VIGENTE ===.*?# === FIN CABECERA ===\\n/m, ''); puts 'OK'")
    p.write_text(text,encoding='utf8',newline='')
# Solo cachés generadas; todos los destinos se comprueban dentro de herramientas.
for p in list(tools.rglob('__pycache__')):
    assert p.resolve().is_relative_to(tools.resolve())
    shutil.rmtree(p)
for p in sorted(tools.rglob('*'),key=lambda x:len(x.parts),reverse=True):
    if p.is_dir() and not any(p.iterdir()):p.rmdir()
(root/'diseno/verificaciones/rutas_json_actualizadas.json').write_text(json.dumps(updated,ensure_ascii=False,indent=2),encoding='utf8')
print('JSON con rutas Windows actualizadas:',len(updated))
