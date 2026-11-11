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
    # Data es contenido editable, y configuración/partidas cambian al jugar.
    # Su comparación con una foto histórica no puede invalidar una corrección.
    mutable=lambda n: n.startswith('Data/') or n=='Vacas.cfg' or bool(re.match(r'Save\d+\.rxdata$',n))
    # Arte ya intervenido: exigir el hash documentado, no aceptar cualquier cambio.
    art_manifest=ROOT/'diseno/fuentes/coherencia_arte/manifest.json'
    documented={e['archivo']:e['sha256'] for e in json.loads(art_manifest.read_text(encoding='utf8'))['cambios']} if art_manifest.exists() else {}
    accepted_art=[n for n in changed if n.startswith('Graphics/') and n in documented and (ROOT/n).is_file() and hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==documented[n]]
    immutable_changed=[n for n in changed if not mutable(n) and n not in accepted_art]
    protected={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in before if (ROOT/n).is_file()}
    results['integridad']={'archivos':len(before),'diferencias_historicas':changed,'motor_modificado':immutable_changed}
    results['integridad']['arte_con_hash_documentado']=accepted_art
    if immutable_changed:errors.append('Motor modificado: '+str(immutable_changed))
    run('inventario',['node',str(COMMON/'inspeccionar.mjs'),'--solo-lectura'])
    run('sistemas',[sys.executable,str(COMMON/'verificar_sistemas.py')])
    run('marshal_ruby',[ruby,str(COMMON/'verificar_marshal.rb')])
    run('fuentes_vs_instalado',[ruby,str(COMMON/'verificar_fuentes.rb')])
    run('jugabilidad',['node',str(COMMON/'auditar_jugabilidad.mjs')])
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
    modified_during=[n for n,h in protected.items() if not (ROOT/n).is_file() or hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h]
    results['integridad']['modificados_durante_verificacion']=modified_during
    if modified_during:errors.append('La verificación modificó archivos protegidos: '+str(modified_during))
    results['errores']=errors
    if args.informe:
        (ROOT/'diseno/verificaciones/verificacion_organizacion.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(results,ensure_ascii=False,indent=2))
    return bool(errors)

if __name__=='__main__':raise SystemExit(main())
