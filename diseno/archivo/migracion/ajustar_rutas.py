from pathlib import Path
import json, re, os
ROOT=Path(__file__).resolve().parent.parent
mapping=json.loads((ROOT/'diseno/verificaciones/traslados.json').read_text(encoding='utf8'))
tools={Path(k).name:v for k,v in mapping.items() if k.startswith('diseno/herramientas/') and len(Path(k).parts)==3}
for p in (ROOT/'diseno/herramientas').rglob('*'):
    if not p.is_file() or p.suffix not in ('.py','.mjs','.rb') or p.name in ('rutas.py','proyecto.mjs','verificar_enlaces.py','verificar_marshal.rb'):continue
    text=p.read_text(encoding='utf-8-sig')
    if p.suffix=='.py':
        # Literales de archivo usados por subprocess, listas dinámicas y accesos BASE/rel.
        for name,dest in tools.items():
            text=re.sub(r"(?<![\w])(['\"])"+re.escape(name)+r'\1',lambda m:"str(_tools.parent.parent / "+repr(dest)+")",text)
        text=re.sub(r"BASE\.parent\s*/\s*(['\"])scripts/([^'\"]+)\1",lambda m:"(_tools.parent / 'scripts' / "+repr(m[2])+")",text)
        text=text.replace("BASE/'verificacion_scripts'","_tools.parent/'verificaciones/scripts_motor'")
        text=text.replace("'diseno', 'marca'","'diseno', 'fuentes', 'marca'")
        # Las herramientas que producen nombres dinámicos también escriben en su tema.
        category='actos' if 'actos' in p.parts else 'interfaz' if any(n in p.name for n in ('interfaz','intro_feka','gfx_ui')) else 'arte'
        text=text.replace("'diseno/capturas'",repr('diseno/capturas/'+category))
        # adaptar_arte permite cualquier subcarpeta de capturas en la validación.
        if p.name=='adaptar_arte.py':text=text.replace("dest.relative_to(ROOT / 'diseno/capturas/arte')","dest.relative_to(ROOT / 'diseno/capturas')")
    if p.suffix=='.mjs' and p.name not in ('inspeccionar.mjs',):
        common=Path(os.path.relpath(ROOT/'diseno/herramientas/comun/proyecto.mjs',p.parent)).as_posix()
        if not common.startswith('.'):common='./'+common
        text="import {raiz as _raiz, ruta as _ruta} from "+repr(common)+";\nprocess.chdir(_raiz);\n"+text
        text=text.replace("path.resolve('.')","_raiz")
        # Los antiguos ../../Data eran relativos al cwd de herramientas.
        text=re.sub(r"(['\"])\.\./\.\./Data/([^'\"]+)\1",lambda m:repr('Data/'+m[2]),text)
        # new URL ya fue recalculado en la migración; los literales restantes son rutas de archivos.
        for name,dest in tools.items():
            text=re.sub(r"(?<![\w])(['\"])"+re.escape(name)+r'\1',lambda m:'_ruta('+repr(dest)+')',text)
    p.write_text(text,encoding='utf8',newline='')
# Archivo compartido y rutas para renderizar desde cualquier cwd.
# Se conserva el código original de luces; la copia numerada se añadirá desde Marshal.
for name in ('ordenar_proyecto.py','ajustar_rutas.py'):
    src=ROOT/'diseno'/name;dst=ROOT/'diseno/archivo/migracion'/name
    dst.parent.mkdir(parents=True,exist_ok=True)
    src.rename(dst)
print('Rutas dinámicas, importaciones y comandos de herramientas actualizados.')
