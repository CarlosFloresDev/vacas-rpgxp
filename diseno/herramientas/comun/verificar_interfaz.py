"""Verifica assets reproducibles, sintaxis Ruby y alcance de Data. Sin red."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json, hashlib, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from adaptar_arte import adapt
ROOT=_ROOT
ART=ROOT/'diseno/fuentes/arte_hd2d/interfaz'
checks=[]
def check(ok,label):
    checks.append({'ok':bool(ok),'check':label})
for spec in json.loads((ART/'manifest.json').read_text(encoding='utf-8'))['assets']:
    dest,expected=adapt(spec)
    actual=Image.open(dest)
    check(actual.size==tuple(spec['size']),f'Tamano {dest.name}')
    check(actual.mode==expected.mode,f'Modo {dest.name}')
    check(actual.tobytes()==expected.tobytes(),f'Reproduccion {dest.name}')
    if spec.get('preserve_alpha'):
        check(actual.mode=='RGBA',f'Alpha RGSS1 {dest.name}')
rows=json.loads((ART/'generaciones.json').read_text(encoding='utf-8'))
for row in rows:
    p=ART/(row['key']+'_fuente.png')
    check(hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],'Fuente nube '+row['key'])
backup=Path((ROOT/'diseno/archivo/herramientas/respaldo_interfaz.txt').read_text(encoding='utf-8-sig').strip())/'Data'
for p in backup.glob('*'):
    if p.is_file() and p.name!='Scripts.rxdata':
        check(p.read_bytes()==(ROOT/'Data'/p.name).read_bytes(),'Data conservada '+p.name)
ruby=Path('D:/DevTools/ruby/rubyinstaller-3.3.6-1-x64/bin/ruby.exe')
snapshot=json.loads((ROOT/'diseno/verificaciones/inventario/snapshot.json').read_text(encoding='utf-8-sig'))
for script in snapshot['Scripts']:
    p=ROOT/'diseno/verificaciones/scripts_motor'/('%03d.rb'%script['index'])
    result=subprocess.run([str(ruby),'-c',str(p)],capture_output=True)
    check(result.returncode==0,'Sintaxis '+script['name'])
log=(ROOT/'diseno/verificaciones/verificacion_interfaz.txt').read_text(encoding='utf-8')
check('OK FIN INTERFAZ RGSS104E' in log and 'FALLO ' not in log,'Integracion real Game.exe')
check(sum('OK Combate acto' in l for l in log.splitlines())==8,'Ocho combates nativos completos')
vn_log=(ROOT/'diseno/verificaciones/verificacion_vn_interfaz.txt').read_text(encoding='utf-8')
check('OK FIN VN REAL' in vn_log and 'FALLO ' not in vn_log,'VN nativo y captura corregida')
for name,sentinel in [('verificacion_rgss.txt','OK FIN: comprobaciones completadas'),
        ('verificacion_rgss_acto3.txt','OK FIN: Acto III verificado'),
        ('verificacion_rgss_acto4.txt','OK FIN: Acto IV verificado')]:
    regression=(ROOT/'diseno'/name).read_text(encoding='utf-8')
    check(sentinel in regression and 'Hangup:' not in regression and 'FALLO ' not in regression,'Regresion '+name)
capt=ROOT/'diseno/capturas/interfaz'
for p in capt.glob('ui_*.bmp'):
    Image.open(p).convert('RGB').save(p.with_suffix('.png'))
names=['titulo','menu','ajustes','objetos','guardar','estado','notas','hud','vn',
    'combate_acto1_jefe','combate_acto2_jefe','combate_acto3_jefe','combate_acto4_jefe',
    'victoria','derrota','gameover']
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
sheet=Image.new('RGB',(1280,8*510),'#0c1513');d=ImageDraw.Draw(sheet)
for i,name in enumerate(names):
    p=capt/('ui_'+name+'.png');check(p.exists(),'Captura '+name)
    if p.exists():
        im=Image.open(p).convert('RGB');check(im.size==(640,480),'Cliente 640x480 '+name)
        check(len(im.getcolors(640*480) or [])>100,'Captura con contenido '+name)
        sheet.paste(im,(i%2*640,i//2*510+30))
        d.text((i%2*640+12,i//2*510+5),name.replace('_',' / '),font=font,fill='#e2d8bb')
sheet.save(capt/'ui_resumen.png')
bg=Image.new('RGB',(960,3*264),'#0c1513');d=ImageDraw.Draw(bg)
paths=list((ROOT/'Graphics/Battlebacks').glob('ui_*.png'))+list((ROOT/'Graphics/Pictures').glob('ui_*.png'))
paths=[p for p in paths if Image.open(p).size==(640,480)]
for i,p in enumerate(paths):
    bg.paste(Image.open(p).resize((320,240)),(i%3*320,i//3*264+24))
    d.text((i%3*320+5,i//3*264+3),p.stem,font=font,fill='#e2d8bb')
bg.save(capt/'ui_fondos.png')
errors=[c['check'] for c in checks if not c['ok']]
report={'checks':len(checks),'errors':errors,'assets':24,'cloud_sources':10,
    'ruby_scripts':len(snapshot['Scripts']),'game_checks':log.count('OK '),
    'scope':'RGSS104E real, entrada simulada, GDI del cliente; no partida manual completa.'}
(ROOT/'diseno/verificaciones/verificacion_interfaz.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
