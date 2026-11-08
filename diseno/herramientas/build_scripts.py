import json
from pathlib import Path
BASE=Path(__file__).resolve().parent
s=json.loads((BASE/'snapshot.json').read_text(encoding='utf-8-sig'));ops=[]
for file,name in [('06_vn.rb','Vacas_VN'),('07_mente.rb','Vacas_Mente'),('08_accesos.rb','Vacas_Accesos')]:
 code=(BASE.parent/'scripts'/file).read_text(encoding='utf-8-sig')
 old=next((x for x in s['Scripts'] if x['name']==name),None)
 ops.append(['update_script',{'index':old['index'],'code':code,'name':name}] if old else ['create_script',{'name':name,'code':code}])
sc=next(x for x in s['Scripts'] if x['name']=='Scene_Battle 4');code=sc['code'].replace('set_text("Escape", 1)','set_text("Apartarse", 1)')
ops.append(['update_script',{'index':sc['index'],'code':code}])
(BASE/'b_sistemas_scripts.json').write_text(json.dumps(ops,ensure_ascii=False),encoding='utf-8')
