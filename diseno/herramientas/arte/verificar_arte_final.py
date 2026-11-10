"""Verifica referencias, reproducción, escala y regresiones de paso sin ejecutar Game.exe."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json,hashlib,copy
from pathlib import Path
from PIL import Image
from instalar_arte_final import R,A,B
from adaptar_arte import adapt
import instalar_iconos_arte_final  # Registra paleta de inventario.
BASE=Path(__file__).resolve().parent
S=json.loads(((_ROOT / 'diseno/verificaciones/inventario/snapshot.json')).read_text(encoding='utf8'))
OLD=json.loads((B/'snapshot_inicial.json').read_text(encoding='utf8'))
errors=[];checks=0
def check(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
initial=json.loads((B/'hashes_iniciales.json').read_text(encoding='utf8'))
check(hashlib.sha256((R/'Vacas.cfg').read_bytes()).hexdigest()==initial['Vacas.cfg'],'Vacas.cfg intacto')
check(hashlib.sha256((R/'Data/Scripts.rxdata').read_bytes()).hexdigest()==initial['Data/Scripts.rxdata'],'Scripts.rxdata intacto')
manifest=json.loads((A/'manifest.json').read_text(encoding='utf8'))
for spec in manifest['assets']:
 dest,im=adapt(spec);actual=Image.open(dest)
 check(actual.size==im.size,'tamaño '+dest.name)
 check(actual.mode==im.mode and actual.tobytes()==im.tobytes(),'reproducción '+dest.name)
 if spec['type']=='battler' and dest.parent.name=='Battlers':check(actual.size==(320,300) and actual.getchannel('A').getextrema()==(0,255),'lienzo/alpha '+dest.name)
 if dest.parent.name=='Icons':check(actual.size==(24,24) and actual.getchannel('A').getbbox() is not None,'icono24/alpha '+dest.name)
 if 'retrato_' in dest.name:check(actual.size==(240,340),'retrato '+dest.name)
 if dest.name.startswith(('screamer_','cine_')):check(actual.size==(640,480),'pantalla '+dest.name)
for name in ('vacas_steven','vacas_steven_mono','vacas_madre','vacas_cripps','vacas_lucy','vacas_obrero1','vacas_obrero2','vacas_obrero3','vacas_obrero4'):
 p=R/f'Graphics/Characters/{name}.png'
 check(Image.open(p).size==(128,192),'humano32x48 '+name)
for name,size in [('vacas_guernsey4',(192,192)),('vacas_muesca',(192,192)),('vacas_junco',(192,192)),('vacas_perro',(160,160))]:
 check(Image.open(R/f'Graphics/Characters/{name}.png').size==size,'excepción animal '+name)
for eid in (18,19,20,21,33,34,35,36,37):
 a,b=OLD['Enemies'][eid],S['Enemies'][eid];expected=copy.deepcopy(a);expected.update(battler_name=b['battler_name'],battler_hue=0)
 check(expected==b,'estadísticas/enemigo '+str(eid))
 check(b['battler_hue']==0 and (R/f'Graphics/Battlers/{b["battler_name"]}.png').exists(),'PNG propio sin tinte '+str(eid))
for mid in range(22,33):
 before=copy.deepcopy(OLD[f'Map{mid:03}']);after=S[f'Map{mid:03}']
 before['data']=after['data']
 if mid==30:
  def replace(v):
   if isinstance(v,str):return v.replace('\\P[madre_neutral]','\\P[madre_envejecida_neutral]')
   if isinstance(v,dict):return {k:replace(x) for k,x in v.items()}
   if isinstance(v,list):return [replace(x) for x in v]
   return v
  before=replace(before)
 check(before==after,'eventos/dimensiones/transferencias conservados '+str(mid))
 ts=S['Tilesets'][after['tileset_id']];atlas=Image.open(R/f'Graphics/Tilesets/{ts["tileset_name"]}.png')
 for tid in after['data']['data']:
  if tid>=384:check(tid-384<atlas.width//32*(atlas.height//32) and tid<len(ts['passages']['data']),'tile existente '+str((mid,tid)))
 # Capas de terreno y decoración nativa inalteradas; solo compuestos de utilería.
 check(OLD[f'Map{mid:03}']['data']['data'][:600]==after['data']['data'][:600],'capas0/1 '+str(mid))
ns={'__file__':str((_ROOT / 'diseno/herramientas/comun/auditar_accesos.py'))}
exec(((_ROOT / 'diseno/herramientas/comun/auditar_accesos.py')).read_text(encoding='utf8').split('scenarios=')[0],ns)
regressions=[];step_checks=0
scenarios=[set(),{140,145,147,151,156},{140,142,150,151,171},{132,133,160,163,176,180},{132,134,161,163,176,180,181,182,185},{132,133,162,163,176,181,182,184,186,187,188}]
for sw in scenarios:
 for selfs in (False,True):
  for mid in range(22,33):
   ns['S']=OLD;before=ns['Grid'](mid,sw,{51:0,58:3,59:3},selfs)
   ns['S']=S;after=ns['Grid'](mid,sw,{51:0,58:3,59:3},selfs)
   for y in range(15):
    for x in range(20):
     for d in (2,4,6,8):
      step_checks+=1
      if before.step(x,y,d)!=after.step(x,y,d):regressions.append([mid,x,y,d,sorted(sw),selfs])
check(not regressions,'colisiones direccionales idénticas: '+str(len(regressions))+' diferencias')
for p in (R/'Data').glob('*.rxdata'):
 rel=str(p.relative_to(R)).replace('\\','/')
 if hashlib.sha256(p.read_bytes()).hexdigest()!=initial[rel]:
  check((B/rel).exists() and hashlib.sha256((B/rel).read_bytes()).hexdigest()==initial[rel],'respaldo original '+rel)
for p in (R/'Graphics').glob('*/*.png'):
 rel=str(p.relative_to(R)).replace('\\','/')
 if rel in initial and hashlib.sha256(p.read_bytes()).hexdigest()!=initial[rel]:
  check((B/rel).exists() and hashlib.sha256((B/rel).read_bytes()).hexdigest()==initial[rel],'respaldo PNG '+rel)
for rel in [str(_ROOT / 'diseno/herramientas/actos/acto5/contenido5.py'),str(_ROOT / 'diseno/herramientas/actos/acto6/contenido6.py'),str(_ROOT / 'diseno/herramientas/actos/acto5/build_acto5.py'),str(_ROOT / 'diseno/herramientas/actos/acto5/maps5.py'),str(_ROOT / 'diseno/herramientas/actos/acto6/maps6.py'),str(_ROOT / 'diseno/herramientas/arte/instalar_arte_final.py'),str(_ROOT / 'diseno/herramientas/arte/componer_arte_final.py'),str(_ROOT / 'diseno/herramientas/arte/auditoria_arte_final.py')]:
 p=BASE/rel
 try:compile(p.read_text(encoding='utf-8-sig'),str(p),'exec');check(True,'sintaxis '+rel)
 except SyntaxError:check(False,'sintaxis '+rel)
report=dict(checks=checks,directional_step_checks=step_checks,scenarios=12,maps=list(range(22,33)),errors=errors,collision_differences=regressions,scope='Comparación de pasos XP frente al estado inicial, eventos/estadísticas, PNG, reproducción, escala, respaldos e integridad. Sin ejecutar ni cerrar Game.exe.',visual_review='Láminas revisadas aparte; no sustituye partida humana con tono/niebla y transiciones.')
(R/'diseno/verificaciones/verificacion_arte_final.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(checks=checks,step_checks=step_checks,errors=errors[:15],differences=len(regressions)),ensure_ascii=False))
if errors:raise SystemExit(1)

