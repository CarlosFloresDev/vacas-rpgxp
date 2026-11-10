"""Renderiza 22-27 con el MCP, aplica la mascara de luz y compone laminas de revision."""
import json,subprocess,sys
from pathlib import Path
from PIL import Image
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[1];CAP=ROOT/'diseno/capturas'
ev='eventos' in sys.argv
ops=[['render_map',dict(mapId=i,drawEvents=ev,outPath=str(CAP/('acto5_%d_base.png'%i)))] for i in range(22,28)]
(BASE/'b_render5.json').write_text(json.dumps(ops))
out=subprocess.run(['node','rx.mjs','--batch','b_render5.json'],cwd=BASE,capture_output=True,text=True,encoding='utf-8')
(BASE/'render_acto5.log').write_text(out.stdout+out.stderr,encoding='utf-8')
ims=[]
for i in range(22,28):
    a=Image.open(CAP/('acto5_%d_base.png'%i)).convert('RGBA')
    plain=a.copy()
    a.alpha_composite(Image.open(ROOT/'Graphics/Pictures'/('acto5_luz%02d.png'%i)))
    a.convert('RGB').save(CAP/('acto5_%d.png'%i));ims.append((plain,a))
    (CAP/('acto5_%d_base.png'%i)).unlink()
for n in range(3):
    sheet=Image.new('RGB',(1280,960))
    for k in range(2):
        plain,lit=ims[n*2+k]
        sheet.paste(plain.convert('RGB'),(0,k*480));sheet.paste(lit.convert('RGB'),(640,k*480))
    sheet.save(CAP/('acto5_lamina_%d.png'%(n+1)))
print('capturas listas')
