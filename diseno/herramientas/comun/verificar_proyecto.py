"""Verificador general de solo lectura. --informe guarda únicamente el informe."""
from pathlib import Path
import argparse, ast, hashlib, json, os, re, shutil, subprocess, sys
from verificar_enlaces import comprobar
from verificar_assets_scripts import comprobar as comprobar_assets_scripts
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Game.rxproj').exists())
COMMON=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--informe',action='store_true');args=parser.parse_args()
    ruby=os.environ.get('VACAS_RUBY') or shutil.which('ruby') or 'D:/DevTools/ruby/rubyinstaller-3.3.6-1-x64/bin/ruby.exe'
    results={};errors=[]
    def run(label,command):
        p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf8',errors='replace')
        results[label]={'codigo':p.returncode,'salida':p.stdout.strip()}
        if p.returncode:errors.append(label+': '+p.stderr[-1500:]+p.stdout[-1500:])
    before=json.loads((ROOT/'diseno/verificaciones/inventario_antes.json').read_text(encoding='utf8'))['archivos_motor_sha256']
    changed=[n for n,h in before.items() if not (ROOT/n).is_file() or hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h]
    results['integridad']={'archivos':len(before),'cambiados':changed}
    if changed:errors.append('Motor/configuración/partidas modificados: '+str(changed))
    run('inventario',['node',str(COMMON/'inspeccionar.mjs'),'--solo-lectura'])
    run('sistemas',[sys.executable,str(COMMON/'verificar_sistemas.py')])
    run('marshal_ruby',[ruby,str(COMMON/'verificar_marshal.rb')])
    run('fuentes_vs_instalado',[ruby,str(COMMON/'verificar_fuentes.rb')])
    syntax=[]
    for p in sorted((ROOT/'diseno/scripts').glob('*.rb')):
        result=subprocess.run([ruby,'-c',str(p)],capture_output=True,text=True,encoding='utf8',errors='replace')
        syntax.append({'archivo':p.name,'ok':result.returncode==0})
        if result.returncode:errors.append(p.name+': '+result.stderr)
    results['sintaxis_ruby']=syntax
    for p in (ROOT/'diseno/herramientas').rglob('*.py'):
        try:ast.parse(p.read_text(encoding='utf-8-sig'))
        except SyntaxError as e:errors.append(str(p)+': '+str(e))
    for p in (ROOT/'diseno/herramientas').rglob('*.mjs'):
        result=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
        if result.returncode:errors.append(str(p)+': '+result.stderr)
    results['enlaces']=comprobar()
    errors.extend(results['enlaces']['errores'])
    results['assets_scripts']=comprobar_assets_scripts()
    errors.extend(results['assets_scripts']['errores'])
    run('assets',['node',str(COMMON/'rx.mjs'),'validate_assets',json.dumps({'includeMaps':True})])
    try:
        assets=json.loads(results['assets']['salida'])
        if assets.get('missing_count',0):errors.append(assets)
    except ValueError:errors.append('No se pudo interpretar el informe de assets')
    snapshot=json.loads((ROOT/'diseno/verificaciones/inventario/snapshot.json').read_text(encoding='utf8'))
    dependencies=[s['name'] for s in snapshot['Scripts'] if re.search(r'diseno[/\\]',s['code'],re.I)]
    results['dependencias_diseno_motor']=dependencies
    if dependencies:errors.append('El motor referencia diseno/: '+str(dependencies))
    results['errores']=errors
    if args.informe:
        (ROOT/'diseno/verificaciones/verificacion_organizacion.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(results,ensure_ascii=False,indent=2))
    return bool(errors)

if __name__=='__main__':raise SystemExit(main())
