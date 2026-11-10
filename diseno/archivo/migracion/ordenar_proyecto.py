"""Migración puntual y trazable de carpetas; no modifica datos del motor."""
from pathlib import Path
import hashlib, json, re, shutil, os

ROOT = Path(__file__).resolve().parent.parent
def rel(p): return p.relative_to(ROOT).as_posix()
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
initial = {rel(p): digest(p) for folder in ('Data','Graphics','Audio') for p in (ROOT/folder).rglob('*') if p.is_file()}
for name in ('Vacas.cfg','Game.ini','Game.exe','Game.rxproj','RGSS104E.dll','Save1.rxdata'):
    if (ROOT/name).exists(): initial[name] = digest(ROOT/name)
inventory = {'raiz': sorted(p.name for p in ROOT.iterdir()), 'diseno': sorted(p.name for p in (ROOT/'diseno').iterdir()),
             'herramientas': sorted(p.name for p in (ROOT/'diseno/herramientas').iterdir()), 'archivos_motor_sha256': initial}
mapping = {}
def plan(src, dst):
    p = ROOT/src
    if p.is_dir():
        for f in p.rglob('*'):
            if f.is_file(): mapping[rel(f)] = dst+'/'+f.relative_to(p).as_posix()
    elif p.is_file(): mapping[src] = dst

for folder in ('audio_fuentes','arte_hd2d','arte_provisional','marca'):
    plan('diseno/'+folder, 'diseno/fuentes/'+folder)
for p in (ROOT/'diseno').glob('*.md'):
    n=p.name
    category = 'historia' if n.startswith('ACTO_') or n=='CINEMATICAS.md' else 'sistemas' if n in ('SISTEMAS.md','INTERFAZ.md','AUDIO.md') else 'arte' if n in ('ESTILO_ARTE.md','BIBLIA_PERSONAJES.md','REVISION_MAPAS.md','AUDITORIA_ARTE.md','AUDITORIA_ARTE_INICIAL.md') else ''
    plan(rel(p), 'diseno/docs/'+(category+'/' if category else '')+n)
plan('CREDITOS_AUDIO.md','diseno/docs/sistemas/CREDITOS_AUDIO.md')
plan('Vacas.cfg.bak','diseno/archivo/Vacas.cfg.bak')
plan('diseno/ui_carga.txt','diseno/archivo/ui_carga.txt')
for p in (ROOT/'diseno').iterdir():
    if p.is_file() and p.suffix!='.md' and rel(p) not in mapping and p.name!='ordenar_proyecto.py':
        dst='diseno/verificaciones/' if re.match(r'(verificacion|auditoria|validar|validacion|revision_mapas|balance_)',p.name) else 'diseno/fuentes/catalogos/'
        plan(rel(p),dst+p.name)
for p in (ROOT/'diseno/capturas').glob('*'):
    if p.is_file():
        category='interfaz' if p.name.startswith('ui_') else 'actos' if p.name.startswith(('acto','mapa')) else 'arte'
        plan(rel(p),'diseno/capturas/'+category+'/'+p.name)
for p in (ROOT/'diseno/herramientas').iterdir():
    if p.name=='__pycache__': continue
    if p.is_dir():
        plan(rel(p), 'diseno/verificaciones/scripts_motor' if p.name=='verificacion_scripts' else 'diseno/herramientas/arte/'+p.name)
        continue
    n=p.name
    if p.suffix in ('.py','.mjs','.rb'):
        m=re.search(r'acto([1-6])|(?:contenido|maps|db|capturas|ampliar_sistema)([2-6])(?=\.)',n)
        if m: group='actos/acto'+(m[1] or m[2])
        elif n in ('maps.py','contenido.py','db.py','build_events.py'): group='actos/acto1'
        elif n in ('gfx_acto2.py',): group='actos/acto2'
        elif n=='crear_prueba4.py': group='actos/acto4'
        elif 'audio' in n: group='audio'
        elif any(x in n for x in ('arte','muestra','escala','gfx_','revision','laminas')) and n!='adaptar_arte.py': group='arte'
        else: group='comun'
        plan(rel(p),'diseno/herramientas/'+group+'/'+n)
    elif n=='snapshot.json': plan(rel(p),'diseno/verificaciones/inventario/snapshot.json')
    elif n.startswith(('validar_','verificacion','auditoria')) or p.suffix in ('.log','.err'):
        plan(rel(p),'diseno/verificaciones/herramientas/'+n)
    elif n.startswith('maps') and n.endswith('_info.json'):
        plan(rel(p),'diseno/herramientas/actos/acto'+n[4]+'/'+n)
    elif n.startswith('b_'): plan(rel(p),'diseno/archivo/lotes/'+n)
    else: plan(rel(p),'diseno/archivo/herramientas/'+n)
# Los informes de fuentes también tienen un único lugar, salvo instantáneas de respaldos.
for old,new in list(mapping.items()):
    if old.startswith('diseno/arte_hd2d/') and re.match(r'(verificacion|auditoria|validar|validacion)',Path(old).name):
        mapping[old]='diseno/verificaciones/fuentes/'+old.removeprefix('diseno/arte_hd2d/')
# Falta Revision_Luces en las copias numeradas. Insertarla conserva el orden real.
for p in (ROOT/'diseno/scripts').glob('*.rb'):
    n=int(p.name[:2])
    if n>=10: plan(rel(p),'diseno/scripts/'+f'{n+1:02}'+p.name[2:])

destinations=list(mapping.values())
assert len(destinations)==len(set(destinations)), 'Destinos duplicados'
# Primero se leen todos los archivos; varios scripts cambian de número.
contents={old:(ROOT/old).read_bytes() for old in mapping}
for old in sorted(mapping,reverse=True):
    (ROOT/old).unlink()
for old,new in mapping.items():
    dst=ROOT/new;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(contents[old])
for folder in ('audio_fuentes','arte_hd2d','arte_provisional','marca'):
    p=ROOT/'diseno'/folder
    for d in sorted(p.rglob('*'),key=lambda x:len(x.parts),reverse=True):
        if d.is_dir() and not any(d.iterdir()): d.rmdir()
    if not any(p.iterdir()):p.rmdir()

prefixes={f'diseno/{n}':f'diseno/fuentes/{n}' for n in ('audio_fuentes','arte_hd2d','arte_provisional','marca')}
prefixes.update({'diseno/capturas':'diseno/capturas', 'diseno/herramientas/verificacion_scripts':'diseno/verificaciones/scripts_motor'})
replacements={**prefixes,**mapping}
pattern=re.compile('|'.join(re.escape(x) for x in sorted(replacements,key=len,reverse=True)))
def rewrite(text):
    def sub(m):
        # Los respaldos mantienen su estructura y sus rutas históricas internas.
        start=text.rfind("\n",0,m.start())+1
        before=text[start:m.start()]
        if 'diseno/respaldos/' in before or re.search(r"\bB\s*/\s*['\"]$",before):return m[0]
        return replacements[m[0]]
    return pattern.sub(sub,text)

tool_files={Path(old).name:new for old,new in mapping.items() if old.startswith('diseno/herramientas/') and len(Path(old).parts)==3}
for p in (ROOT/'diseno').rglob('*'):
    if not p.is_file() or 'respaldos' in p.parts or p.name=='ordenar_proyecto.py' or '__pycache__' in p.parts:continue
    if p.suffix.lower() not in ('.py','.rb','.mjs','.json','.md','.txt','.tsv','.svg','.log','.err'):continue
    try: text=p.read_bytes().decode('utf-8-sig')
    except UnicodeDecodeError:continue
    original=text
    old=next((k for k,v in mapping.items() if v==rel(p)),rel(p))
    # Enlaces Markdown relativos a su ubicación original.
    if p.suffix=='.md':
        def link(m):
            target=m[2];path,sep,anchor=target.partition('#')
            if not path or re.match(r'\w+:|//',path):return m[0]
            dest=(ROOT/old).parent/path
            dest=Path(os.path.abspath(dest))
            if dest.is_relative_to(ROOT):
                key=rel(dest);dest=ROOT/mapping.get(key,key)
                if dest.exists():return m[1]+Path(os.path.relpath(dest,p.parent)).as_posix()+(sep+anchor if sep else '')+m[3]
            return m[0]
        text=re.sub(r'(!?\[[^\]]*\]\()([^\s)]+)(\))',link,text)
    text=rewrite(text)
    if p.suffix=='.py' and 'herramientas' in p.parts:
        # La raíz se busca por Game.rxproj: no depende de la profundidad del acto.
        root_expr="next(p for p in Path(__file__).resolve().parents if (p / 'Game.rxproj').is_file())"
        text=re.sub(r'Path\(__file__\)\.resolve\(\)\.parents\[2\]',root_expr,text)
        text=re.sub(r'(ROOT|root)\s*=\s*(BASE|B)\.parents\[1\]',lambda m:m[1]+'='+root_expr,text)
        text=text.replace("Path(__file__).resolve().parents[1]/'arte_hd2d'",root_expr+"/'diseno/fuentes/arte_hd2d'")
        text=text.replace("os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))", "str("+root_expr+")")
        # BASE/B significaban la antigua carpeta plana: cada acceso ahora es explícito.
        for name,dst in tool_files.items():
            text=re.sub(r"\b(?:BASE|B)\s*/\s*(['\"])"+re.escape(name)+r'\1',lambda m:"("+root_expr+" / "+repr(dst)+")",text)
        text=re.sub(r"BASE\.parent\s*/\s*(['\"])scripts/?\1", "("+root_expr+" / 'diseno/scripts')",text)
        for oldpath,newpath in mapping.items():
            if len(Path(oldpath).parts)==2 and oldpath.startswith('diseno/'):
                text=re.sub(r"BASE\.parent\s*/\s*(['\"])"+re.escape(Path(oldpath).name)+r'\1',lambda m:"("+root_expr+" / "+repr(newpath)+")",text)
        # Importaciones entre actos: una sola definición del recorrido de módulos.
        bootstrap="\n# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.\nimport sys as _sys\nfrom pathlib import Path as _Path\n_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')\n_sys.path.insert(0, str(_tools / 'comun'))\nfrom rutas import preparar_imports\npreparar_imports()\n"
        lines=text.splitlines(keepends=True)
        # Respetar docstring y futuras importaciones.
        import ast
        tree=ast.parse(text);at=0
        for node in tree.body:
            if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str) or isinstance(node,ast.ImportFrom) and node.module=='__future__':at=node.end_lineno
            else:break
        lines.insert(at,bootstrap);text=''.join(lines)
        if "os.path.dirname(__file__)" in original and 'from pathlib import Path' not in original:text='from pathlib import Path\n'+text
    if p.suffix=='.mjs' and 'herramientas' in p.parts:
        depth=len(p.parent.relative_to(ROOT).parts)
        # URL relativas al archivo: recalcular desde su nueva carpeta.
        def url(m):
            value=m[2]
            if value.startswith('../../'):
                value='../'*depth+value[6:]
            elif value in tool_files:
                value=Path(os.path.relpath(ROOT/tool_files[value],p.parent)).as_posix()
            return m[1]+value+m[3]
        text=re.sub(r"(new URL\(['\"])([^'\"]+)(['\"],\s*import.meta.url\))",url,text)
    if p.suffix=='.rb' and 'herramientas' in p.parts:
        depth=len(p.parent.relative_to(ROOT).parts)
        text=text.replace("File.expand_path('../..',File.dirname(__FILE__))",f"File.expand_path('{('/'.join(['..']*depth))}',File.dirname(__FILE__))")
    if text!=original:p.write_bytes(text.encode('utf-8'))

out=ROOT/'diseno/verificaciones';out.mkdir(exist_ok=True)
(out/'inventario_antes.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'traslados.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(mapping)} archivos reubicados. Motor: {len(initial)} hashes conservados para comparar.')
