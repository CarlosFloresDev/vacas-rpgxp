"""Comprobacion reproducible HD, sin abrir ejecutables de juego ni escribir partidas."""
from pathlib import Path
import hashlib,json,subprocess,os

ROOT=Path(__file__).resolve().parents[3]
RUBY=Path('D:/DevTools/ruby/rubyinstaller-3.3.6-1-x64/bin/ruby.exe')
COMMON=ROOT/'diseno/herramientas/comun'
os.chdir(ROOT)
report={'errores':[]}
config=json.loads((ROOT/'mkxp.json').read_text(encoding='utf8'))
report['configuracion']=config
assert config['rgssVersion']==1 and config['smoothScaling']==0
assert config['integerScalingActive'] and not config['integerScalingLastMile']
assert config['fixedAspectRatio'] and config['vsync']
assert 'customScript' not in config
report['sintaxis']=[]
for path in sorted((ROOT/'diseno/scripts').rglob('*.rb')):
    p=subprocess.run([str(RUBY),'-c',str(path)],capture_output=True,text=True)
    report['sintaxis'].append({'archivo':path.relative_to(ROOT).as_posix(),'ok':p.returncode==0})
    if p.returncode:report['errores'].append(p.stderr)
report['comprobaciones']={}
for name,args in [
    ('fuentes',['verificar_fuentes.rb']),('marshal',['verificar_marshal.rb']),
    ('simulacion_360',['simular_hd.rb']),('simulacion_480',['simular_hd.rb','clasico'])
]:
    p=subprocess.run([str(RUBY),str(COMMON/args[0])]+args[1:],capture_output=True,text=True,encoding='utf8',errors='replace')
    report['comprobaciones'][name]={'codigo':p.returncode,'salida':p.stdout,'stderr':p.stderr}
    if p.returncode:report['errores'].append(name)
files=['Vacas.exe','LICENSE-mkxp-z.txt','scripts/preload/ruby_classic_wrap.rb','stdlib/json.rb']
report['distribucion']={p:(ROOT/p).is_file() for p in files}
report['sha256_mkxp']=hashlib.sha256((ROOT/'Vacas.exe').read_bytes()).hexdigest()
if not all(report['distribucion'].values()):report['errores'].append('Distribucion incompleta')
report['integridad']=json.loads((ROOT/'diseno/verificaciones/hd_integridad.json').read_text())
for path,expected in report['integridad']['before'].items():
    if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=expected:report['errores'].append('Integridad '+path)
report['alcance']='Carga y geometria simuladas con datos Marshal reales. Renderer, audio, foco y capturas nativas pendientes por ausencia de dispositivo de audio.'
(ROOT/'diseno/verificaciones/hd_verificacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'sintaxis':len(report['sintaxis']),'errores':report['errores'],'informe':'diseno/verificaciones/hd_verificacion.json'},ensure_ascii=False))
raise SystemExit(bool(report['errores']))
