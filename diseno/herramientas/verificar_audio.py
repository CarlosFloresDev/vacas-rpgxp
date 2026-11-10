"""Verificacion estatica de audio. Ejecutar tras instalar y fuera del arnes RGSS."""
from pathlib import Path
import hashlib, json, re, subprocess, tempfile

root=Path(__file__).resolve().parents[2]
ruby=Path('D:/DevTools/ruby/rubyinstaller-3.3.6-1-x64/bin/ruby.exe')
catalog=json.loads((root/'diseno/audio_catalogo.json').read_text(encoding='utf8'))
snapshot=json.loads((root/'diseno/herramientas/snapshot.json').read_text(encoding='utf8'))
source=(root/'diseno/scripts/11_interfaz.rb').read_text(encoding='utf8')
report={'ruby':str(ruby),'errores':[]}
def error(message): report['errores'].append(message)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
table={}
for key,kind,name,vol in re.findall(r':(\w+)=>\[:(bgm|bgs|me|se),"([^"]+)",(\d+)',source):
    if key in table: error('Clave duplicada '+key)
    table[key]={'tipo':kind,'nombre':name,'volumen':int(vol)}
report['tabla']=table
report['archivos']=[]
report['copias_ogg_adicionales']=[]
for entry in catalog['entries']:
    dest=root/entry['destino']; src=root/'diseno/audio_fuentes'/entry['file']
    if dest.suffix!=src.suffix: src=src.with_suffix(dest.suffix)
    ok=dest.is_file() and src.is_file() and sha(dest)==sha(src)
    if not ok: error('Copia no coincide: '+entry['destino'])
    if entry['key'] not in table: error('Clave ausente: '+entry['key'])
    report['archivos'].append({'destino':entry['destino'],'copia_identica':ok,'sha256':sha(dest) if dest.exists() else None})
    original=root/'diseno/audio_fuentes'/entry['file']
    if original.suffix!=dest.suffix:
        extra=dest.with_suffix(original.suffix)
        ok=extra.is_file() and sha(extra)==sha(original)
        report['copias_ogg_adicionales'].append({'destino':str(extra.relative_to(root)),'copia_identica':ok})
        if not ok: error('Copia OGG adicional incorrecta '+str(extra))
for key,row in table.items():
    candidates=list((root/'Audio'/row['tipo'].upper()).glob(row['nombre']+'.*'))
    if not candidates: error('TABLE sin archivo '+key)
report['mapas']=catalog['maps']
if set(m['id'] for m in catalog['maps'])!=set(map(int,snapshot['MapInfos'])): error('Mapas sin cubrir')
for m in catalog['maps']:
    for kind in ['bgm','bgs']:
        if m[kind] not in table or table[m[kind]]['tipo']!=kind: error('Canal incorrecto en mapa '+str(m['id']))
report['referencias_datos']=[]
legacy=catalog['legacy']
def walk(obj,where):
    if isinstance(obj,dict):
        if obj.get('_class')=='RPG::AudioFile' and obj.get('name'):
            name=obj['name']; key=legacy.get(name)
            rows=[table[key]] if key in table else [r for r in table.values() if r['nombre']==name]
            ok=bool(rows)
            if not ok: error(where+': audio sin resolver '+name)
            report['referencias_datos'].append({'origen':where,'nombre':name,'clave':key,'resuelta':ok})
        for val in obj.values(): walk(val,where)
    elif isinstance(obj,list):
        for val in obj: walk(val,where)
for name,data in snapshot.items():
    if name!='Scripts': walk(data,name)
report['referencias_scripts']=[]
for script in snapshot['Scripts']:
    for name in re.findall(r'AudioFile.new\([\'\"]([^\'\"]+)',script['code']):
        ok=name in legacy or any(r['nombre']==name for r in table.values())
        report['referencias_scripts'].append({'script':script['name'],'nombre':name,'resuelta':ok})
        if not ok: error('Referencia en script '+name)
# Compilar todas las secciones extraidas; verificar cada fuente editada y arnes.
files=sorted((root/'diseno/herramientas/verificacion_scripts').glob('*.rb'))
files+=sorted((root/'diseno/scripts').glob('*.rb'))
files+=[root/'diseno/herramientas/instalar_audio.rb',root/'diseno/herramientas/prueba_audio.rb']
report['sintaxis']=[]
for file in files:
    result=subprocess.run([str(ruby),'--disable-gems','-c',str(file)],capture_output=True,text=True)
    report['sintaxis'].append({'archivo':str(file.relative_to(root)),'ok':result.returncode==0,'salida':result.stdout.strip(),'avisos':result.stderr.strip()})
    if result.returncode or 'duplicated' in result.stderr: error('Sintaxis/clave duplicada '+str(file))
check="require 'zlib'; a=Marshal.load(File.binread('Data/Scripts.rxdata')); a.each { |r| Zlib::Inflate.inflate(r[2]) }; puts a.size"
result=subprocess.run([str(ruby),'--disable-gems','-e',check],cwd=root,capture_output=True,text=True)
report['scripts_marshal']={'ok':result.returncode==0,'secciones':result.stdout.strip(),'error':result.stderr.strip()}
if result.returncode: error('Scripts.rxdata no carga')
backup=Path(catalog['backup'])
check="require 'zlib'; a=Marshal.load(File.binread(ARGV[0])); b=Marshal.load(File.binread(ARGV[1])); raise unless a.size==b.size; a.zip(b).each { |x,y| raise x[1] unless x[1]=='Vacas_Interfaz' || x==y }; r=a.find { |x| x[1]=='Vacas_Interfaz' }; raise unless Zlib::Inflate.inflate(r[2])==File.binread('diseno/scripts/11_interfaz.rb'); puts 'OK'"
result=subprocess.run([str(ruby),'--disable-gems','-e',check,'Data/Scripts.rxdata',str(backup/'Data/Scripts.rxdata')],cwd=root,capture_output=True,text=True)
report['solo_interfaz_modificada']=result.returncode==0
if result.returncode: error('Secciones modificadas fuera de interfaz o fuente no instalada')
credits=(root/'diseno/audio_fuentes/CREDITOS.md').read_text(encoding='utf8').splitlines()
report['creditos']={'lineas':len(credits),'copia_distribuible':(root/'CREDITOS_AUDIO.md').read_text(encoding='utf8').splitlines()==credits,
    'incorporados':all(json.dumps(l.replace('`',''),ensure_ascii=False) in source for l in credits)}
display=re.search(r'  CREDITS_LINES = (\[.*?\])\nend',source,re.S)
display=json.loads(display.group(1)) if display else []
normalize=lambda text:re.sub(r'\s+','',text)
raw=''.join(re.sub(r'^#+ ','',l.replace('`','')) for l in credits)
report['creditos']['texto_visible_completo']=normalize(''.join(display))==normalize(raw)
report['creditos']['lineas_visibles']=len(display)
if not report['creditos']['texto_visible_completo']: error('El texto de creditos visible no coincide')
if not all([report['creditos']['copia_distribuible'],report['creditos']['incorporados']]): error('Creditos incompletos')
engine=root/'diseno/verificacion_audio_motor.txt'
text=engine.read_text(encoding='utf8') if engine.exists() else ''
report['motor']={'ok':'OK FIN AUDIO RGSS104E' in text and 'FALLO ' not in text,'comprobaciones':sum(l.startswith('OK ') for l in text.splitlines()),'log':str(engine.relative_to(root))}
if not report['motor']['ok']: error('Prueba de motor pendiente o fallida')
report['ok']=not report['errores']
(root/'diseno/verificacion_audio.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'ok':report['ok'],'archivos':len(report['archivos']),'claves':len(table),'scripts':report['scripts_marshal'],'motor':report['motor'],'errores':report['errores']},ensure_ascii=False))
raise SystemExit(0 if report['ok'] else 1)
