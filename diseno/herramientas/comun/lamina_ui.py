"""Compone exclusivamente PNG nativos enumerados en la auditoría actual."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[3]
report = json.loads((root / 'diseno/verificaciones/auditoria_ui.json').read_text(encoding='utf-8'))
if not report.get('motor_real'):
    raise SystemExit('Sin capturas nativas: no se fabrica una lámina simulada.')
screens = report['pantallas']
sheet = Image.new('RGB', (1280, ((len(screens)+2)//3)*270), '#131919')
draw = ImageDraw.Draw(sheet)
for i, screen in enumerate(screens):
    image = Image.open(root / screen['png']).convert('RGB')
    image.thumbnail((420, 240))
    x, y = (i % 3)*426, (i // 3)*270
    sheet.paste(image, (x, y+24))
    draw.text((x+5, y+5), screen['nombre'], fill='#e2d8bb')
target = root / ('diseno/capturas/interfaz/ui_%s_lamina.png' % report['lienzo'][1])
sheet.save(target)
print(target)
