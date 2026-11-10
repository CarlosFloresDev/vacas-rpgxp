"""Audita escalas y regenera capturas con referencias 1:1, sin escribir Data.

python diseno/herramientas/arte/verificar_escala.py --render
Las fuentes y medidas reproducibles están en arte_hd2d/lote_escala.json.
"""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont
from adaptar_arte import adapt

ROOT = _ROOT
BACKUP = ROOT / 'diseno/respaldos/antes_escala_20261109'
CAPTURES = ROOT / 'diseno/capturas/arte'
ART = ROOT / 'diseno/fuentes/arte_hd2d'
OBJECTS = ['laboratorio', 'muebles', 'cosas', 'matadero', 'tablon', 'puerta', 'furgoneta']
CHANGED = {'vacas_laboratorio', 'vacas_muebles', 'vacas_cosas', 'vacas_matadero'}
FONT = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 12)


def bounds(im):
    b = im.getchannel('A').getbbox()
    return [b[2]-b[0], b[3]-b[1]] if b else None


def frame(name, n, original=False):
    p = Path('Graphics/Characters') / (name+'.png')
    im = Image.open((BACKUP if original else ROOT)/p).convert('RGBA')
    w, h = im.width//4, im.height//4
    return im.crop((n % 4*w, n//4*h, (n % 4+1)*w, (n//4+1)*h))


def reference_band(width, slots):
    """Mismo tamaño de píxel para personajes y objetos; suelo compartido."""
    entries = [('vacas_lucy', 0), ('vacas_steven', 0)]+sorted(slots)
    step, rowh = 112, 106
    cols = max(1, width//step)
    out = Image.new('RGBA', (width, 26+rowh*((len(entries)+cols-1)//cols)), '#25282D')
    d = ImageDraw.Draw(out)
    d.text((8, 5), 'ESCALA 1:1 | celda humana 48 px; silueta Lucy/Steven 40 px | indice: ancho x alto visibles', font=FONT, fill='white')
    for i, (name, n) in enumerate(entries):
        x, y = (i % cols)*step, 26+(i//cols)*rowh
        im = frame(name, n)
        baseline = y+66
        d.line((x, baseline, x+step-4, baseline), fill='#7C858B')
        out.alpha_composite(im, (x+(step-im.width)//2, baseline-im.height))
        d.text((x+4, y+70), name.removeprefix('vacas_'), font=FONT, fill='white')
        size = bounds(im)
        d.text((x+4, y+85), f'{n}: {size[0]} x {size[1]} px', font=FONT, fill='#CCD9DC')
    return out


def map_context():
    # Leer directamente los mapas usados por el renderer; no depender de un snapshot antiguo.
    module = 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js'
    code = f"""import {{readRxdataFile}} from '{module}';
    const maps={{}};
    for(let i=1;i<=16;i++) maps[i]=await readRxdataFile('Data/Map'+String(i).padStart(3,'0')+'.rxdata');
    console.log(JSON.stringify(maps));"""
    return json.loads(subprocess.check_output(['node', '--input-type=module', '-e', code], cwd=ROOT, encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--permitir-data-modificada', action='store_true', help='Auditar hojas tras un rediseño autorizado de mapas; conservar el informe histórico.')
    args = parser.parse_args()
    report = {'rule': 'Celda humana 48 px, silueta real 40 px; frascos 10-16, microscopio 24 sobre mesa, lampara 38, sillas 26-28.', 'sheets': [], 'captures': []}
    scale_specs = json.loads((ART/'lote_escala.json').read_text(encoding='utf-8'))['assets']
    for spec in scale_specs:
        dest, reproduced = adapt(spec)
        installed = Image.open(dest).convert('RGBA')
        assert reproduced.tobytes() == installed.tobytes(), (dest, 'reproducibilidad')
        cw, ch = map(int, spec['cell'].split('x'))
        for index, rule in spec['cell_scale'].items():
            tile = frame(dest.stem, int(index))
            assert tile.getbbox()[3] == ch, (dest, index, 'apoyo inferior')
            expected = max(part['height']+part.get('bottom',0) for part in rule.get('parts',[rule]))
            assert bounds(tile)[1] == expected, (dest, index, 'altura')
    for short in OBJECTS:
        name = 'vacas_'+short
        path = Path('Graphics/Characters')/(name+'.png')
        before, after = Image.open(BACKUP/path), Image.open(ROOT/path)
        assert before.size == after.size, name
        cells = []
        for n in range(16):
            a, b = frame(name, n, True), frame(name, n)
            assert bool(bounds(a)) == bool(bounds(b)), (name, n, 'ocupacion')
            cells.append({'index': n, 'before': bounds(a), 'after': bounds(b), 'changed': a.tobytes() != b.tobytes()})
        report['sheets'].append({'name': name, 'size': after.size, 'cell': [after.width//4, after.height//4], 'cells': cells,
                                'before_sha256':hashlib.sha256((BACKUP/path).read_bytes()).hexdigest(),
                                'after_sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()})
    # Lámina completa: antes/después y ambos personajes junto a cada celda.
    rows = [(s['name'], c) for s in report['sheets'] for c in s['cells'] if c['before']]
    gallery = Image.new('RGBA', (960, ((len(rows)+3)//4)*126), '#30343A')
    d = ImageDraw.Draw(gallery)
    for i, (name, c) in enumerate(rows):
        x, y = i % 4*240, i//4*126
        d.text((x+5, y+3), f'{name} [{c["index"]}]', font=FONT, fill='white')
        baseline = y+84
        for xx, im in [(x+8, frame(name,c['index'],True)), (x+110, frame(name,c['index'])), (x+204, frame('vacas_lucy',0))]:
            gallery.alpha_composite(im,(xx,baseline-im.height))
        d.line((x+4,baseline,x+236,baseline),fill='#8A969A')
        d.text((x+5,y+91),f'Antes {c["before"]} > ahora {c["after"]}',font=FONT,fill='white')
        d.text((x+5,y+108),'pixeles 1:1; Lucy a la derecha',font=FONT,fill='#C2CDD0')
    gallery.convert('RGB').save(CAPTURES/'escala_auditoria_completa.png')
    for n,y in enumerate(range(0,gallery.height,882)):
        gallery.crop((0,y,gallery.width,min(y+882,gallery.height))).convert('RGB').save(CAPTURES/f'escala_auditoria_{n+1}.png')
    if args.render:
        maps = map_context()
        specs, slots_by_id = [], {}
        for key, m in maps.items():
            mid = int(key)
            slots = set()
            all_names = set()
            for e in m['events'].values():
                for p in e['pages']:
                    g = p['graphic']; name = g.get('character_name')
                    all_names.add(name)
                    if name in {'vacas_'+s for s in OBJECTS}:
                        slots.add((name, (g['direction']//2-1)*4+g['pattern']))
            if mid < 12 and not (all_names & CHANGED):
                continue
            name = f'acto3_{mid}.png' if mid >= 12 else {2:'mapa2_el_piso.png',3:'mapa3_la_escalera.png',4:'mapa4_la_calle.png'}.get(mid, f'acto2_mapa{mid}_eventos.png')
            specs.append(['render_map', {'mapId': mid, 'drawEvents': True, 'outPath': str(CAPTURES/name)}])
            slots_by_id[mid] = (name, slots)
        batch = ROOT/'diseno/archivo/lotes/b_render_escala.json'
        batch.write_text(json.dumps(specs,ensure_ascii=False,indent=2),encoding='utf-8')
        with (ROOT/'diseno/verificaciones/herramientas/render_escala.log').open('w',encoding='utf-8') as log:
            subprocess.run(['node',str(ROOT/'diseno/herramientas/comun/rx.mjs'),'--batch',str(batch)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
        for mid, (name, slots) in slots_by_id.items():
            path = CAPTURES/name
            im = Image.open(path).convert('RGBA')
            if mid == 2:
                detail = im.crop((0,448,960,704)).resize((1920,512),Image.Resampling.NEAREST)
                band = reference_band(960,slots)
                band = band.resize((band.width*2,band.height*2),Image.Resampling.NEAREST)
                out = Image.new('RGBA',(1920,detail.height+band.height))
                out.alpha_composite(detail);out.alpha_composite(band,(0,detail.height))
                out.convert('RGB').save(CAPTURES/'mapa2_salon_y_cocina_x2.png')
                report['captures'].append('mapa2_salon_y_cocina_x2.png')
            band = reference_band(im.width,slots)
            out = Image.new('RGBA',(im.width,im.height+band.height))
            out.alpha_composite(im);out.alpha_composite(band,(0,im.height));out.convert('RGB').save(path)
            report['captures'].append(name)
    elif (ART/'verificacion_escala.json').exists():
        report['captures'] = json.loads((ART/'verificacion_escala.json').read_text(encoding='utf-8'))['captures']
    baseline = json.loads((BACKUP/'data_hashes.json').read_text())
    current = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Data').rglob('*') if p.is_file()}
    if not args.permitir_data_modificada:
        assert current == baseline, 'Data ha cambiado'
    report['data_unchanged'] = current == baseline
    report['backup'] = str(BACKUP.relative_to(ROOT))
    report['reproducible_from_saved_sources'] = True
    report['components'] = {'microscopio': {'before_with_table':64,'after_instrument':24,'after_table':24,'after_total':48}, 'tetera': {'before_with_stool':47,'after_kettle':12,'after_stool':24,'after_total':36}}
    target = ROOT/'diseno/verificaciones/verificacion_escala_revision.json' if args.permitir_data_modificada else ART/'verificacion_escala.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'hojas_auditadas':len(report['sheets']),'capturas':report['captures'],'data_sin_cambios':report['data_unchanged']},ensure_ascii=False))


if __name__ == '__main__':
    main()
