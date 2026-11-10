"""Audita el lote nuevo sin alterar el informe histórico de fase 2."""
import json,hashlib,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'diseno/arte_hd2d/acto3'
manifest=json.loads((ART/'manifest.json').read_text(encoding='utf-8'))
errors=[];rows=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for a in manifest['assets']:
    p=ROOT/a['destination'];source=ROOT/a['source']
    im=Image.open(p);im.load()
    size=(128,192) if a['type']=='character' else (128,256) if a['type']=='indexed' else (240,340) if a['type']=='retrato' else (320,300) if a['type']=='battler' else (640,480)
    if im.size!=size:errors.append('Tamaño: '+str(p))
    if a['type'] in ['character','indexed','retrato','battler']:
        if im.mode!='RGBA' or im.getchannel('A').getextrema()[0]!=0:errors.append('Alpha: '+str(p))
    if a.get('preserve_canvas'):
        base=Image.open(ROOT/a['expression_base']).convert('RGBA')
        if ImageChops.difference(im.getchannel('A'),base.getchannel('A')).getbbox():errors.append('Máscara facial alpha: '+str(p))
        # Ropa y manos por debajo del rostro deben conservarse byte a byte.
        if im.crop((0,130,240,340)).tobytes()!=base.crop((0,130,240,340)).tobytes():errors.append('Ropa modificada en expresión: '+str(p))
    rows.append(dict(path=a['destination'],source=a['source'],size=im.size,mode=im.mode,sha256=sha(p),source_sha256=sha(source)))
historical=json.loads((ROOT/'diseno/arte_hd2d/verificacion_fase2.json').read_text(encoding='utf-8'))
for row in historical['checked']:
    p=ROOT/row['path']
    if sha(p)!=row['sha256']:errors.append('Arte previo modificado: '+row['path'])
refs=[]
for key in ['elena','tarro','factura','camilla','diagnostico']:
    p=ROOT/'diseno/arte_hd2d/referencias'/(key+'.png')
    refs.append(dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p)))
prompts=[dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p)) for p in sorted(ART.glob('*.prompt.txt'))]
report=dict(assets=rows,references=refs,prompts=prompts,cloud_generations=len(prompts),previous_assets_unchanged=len(historical['checked']),errors=errors,method='image_gen en nube; adaptación CPU con adaptar_arte.py; inspección view_image; sin GPU local')
(ART/'verificacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
# Lámina de revisión: composición de recursos existentes, sin generar arte nuevo.
sheet=Image.new('RGB',(1280,math.ceil(len(rows)/4)*400),'#30343A');draw=ImageDraw.Draw(sheet)
for n,row in enumerate(rows):
    x=(n%4)*320;y=(n//4)*400
    draw.text((x+6,y+6),Path(row['path']).name,fill='white')
    im=Image.open(ROOT/row['path']).convert('RGBA');im.thumbnail((308,365),Image.Resampling.LANCZOS)
    sheet.paste(im,(x+(320-im.width)//2,y+30),im)
sheet.save(ROOT/'diseno/capturas/acto3_arte.png')
print(json.dumps(dict(assets=len(rows),references=len(refs),prompts=len(prompts),old_unchanged=report['previous_assets_unchanged'],errors=errors),ensure_ascii=False))
if errors:raise SystemExit(1)
