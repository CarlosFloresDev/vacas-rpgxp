
# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json
from pathlib import Path
BASE=Path(__file__).resolve().parent
s=json.loads(((_ROOT / 'diseno/verificaciones/inventario/snapshot.json')).read_text(encoding='utf-8-sig'));ops=[]
for file,name in [('06_vn.rb','Vacas_VN'),('07_mente.rb','Vacas_Mente'),('08_accesos.rb','Vacas_Accesos')]:
 code=((_ROOT / 'diseno/scripts')/file).read_text(encoding='utf-8-sig')
 old=next((x for x in s['Scripts'] if x['name']==name),None)
 ops.append(['update_script',{'index':old['index'],'code':code,'name':name}] if old else ['create_script',{'name':name,'code':code}])
sc=next(x for x in s['Scripts'] if x['name']=='Scene_Battle 4');code=sc['code'].replace('set_text("Escape", 1)','set_text("Apartarse", 1)')
ops.append(['update_script',{'index':sc['index'],'code':code}])
((_ROOT / 'diseno/archivo/lotes/b_sistemas_scripts.json')).write_text(json.dumps(ops,ensure_ascii=False),encoding='utf-8')
