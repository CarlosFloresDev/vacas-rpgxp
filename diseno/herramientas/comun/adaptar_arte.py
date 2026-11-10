"""Adaptación CPU/Pillow a RGSS1. Rutas relativas a la raíz del proyecto.

python diseno/herramientas/comun/adaptar_arte.py --help
No genera imágenes ni ejecuta los generadores antiguos.
"""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
import hashlib
import math

from PIL import Image, ImageChops, ImageColor, ImageFilter, ImageOps, ImageDraw

ROOT = _ROOT
BACKUP = ROOT / 'diseno/fuentes/arte_provisional/sd_v1'
PALETTES = {
    'piso': ['#141318', '#29252A', '#494039', '#71634B', '#A18A59', '#D1BA7B', '#E8D9AA', '#444B50', '#77848A', '#A6B8BE', '#533E38', '#946A55', '#C69878', '#E4C4A0', '#350F19', '#701D2C'],
    'matadero': ['#10171D', '#263239', '#465557', '#738585', '#ADC0BD', '#DFE7DC', '#F3F0D9', '#251018', '#4B1020', '#78192A', '#A42A39', '#CE5259', '#E8908A', '#694139', '#AA7656', '#D4B48A'],
    'alcantarillas': ['#090F12', '#142422', '#243C34', '#3D5744', '#62745A', '#8B9870', '#BBC19A', '#394C54', '#6C8B91', '#ACCDCA', '#30121B', '#641B2C', '#9B3442', '#C76768', '#927461', '#D2B996'],
}


def path(value):
    p = Path(value)
    return p.resolve() if p.is_absolute() else (ROOT / p).resolve()


def dimensions(value):
    if isinstance(value, (list, tuple)):
        result = tuple(map(int, value))
    else:
        result = tuple(map(int, value.lower().split('x')))
    if len(result) != 2 or min(result) < 1:
        raise ValueError('El tamaño debe ser ANCHOxALTO, con valores positivos')
    return result


def alpha_cleanup(im, threshold):
    if threshold is not None:
        if not 1 <= threshold <= 255:
            raise ValueError('alpha_threshold debe estar entre 1 y 255')
        im.putalpha(im.getchannel('A').point(lambda a: 255 if a >= threshold else 0))
    return im


def remove_key(im, key, tolerance):
    if not 0 <= tolerance <= 255:
        raise ValueError('key_tolerance debe estar entre 0 y 255')
    rgb = ImageColor.getrgb(key)
    im.putdata([(r, g, b, 0 if max(abs(r-rgb[0]), abs(g-rgb[1]), abs(b-rgb[2])) <= tolerance else a)
                for r, g, b, a in im.getdata()])
    return im


def crop(im):
    box = im.getchannel('A').getbbox()
    if box is None:
        raise ValueError('Imagen/celda vacía; revise transparencia o color clave')
    return im.crop(box)


def quantize(im, zone):
    if not zone:
        return im
    colors = [ImageColor.getrgb(c) for c in PALETTES[zone]]
    palette = Image.new('P', (1, 1))
    # Rellenar con el último color, sin introducir negro fuera de paleta.
    palette.putpalette([v for c in colors + [colors[-1]] * (256-len(colors)) for v in c])
    result = im.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
    result.putalpha(im.getchannel('A'))
    return result


def outline(im, color):
    alpha = im.getchannel('A')
    edge = ImageChops.subtract(alpha.filter(ImageFilter.MaxFilter(3)), alpha)
    base = Image.new('RGBA', im.size, ImageColor.getrgb(color) + (0,))
    base.putalpha(edge)
    base.alpha_composite(im)
    return base


def place(im, size, padding, resample, bottom=True):
    w, h = size
    if min(w, h) <= padding*2:
        raise ValueError('El margen ocupa toda la imagen')
    ratio = min((w-padding*2)/im.width, (h-padding*2)/im.height)
    im = im.resize((max(1, round(im.width*ratio)), max(1, round(im.height*ratio))), resample)
    out = Image.new('RGBA', size)
    out.alpha_composite(im, ((w-im.width)//2, h-padding-im.height if bottom else (h-im.height)//2))
    return out


def adapt(spec):
    source, dest = path(spec['source']), path(spec['destination'])
    # Solo arte del proyecto, nunca Data ni scripts ni respaldos como destino.
    dest.relative_to(ROOT / 'Graphics')
    categories = {'Animations', 'Autotiles', 'Battlebacks', 'Battlers', 'Characters',
                  'Fogs', 'Gameovers', 'Icons', 'Panoramas', 'Pictures', 'Tilesets',
                  'Titles', 'Transitions', 'Windowskins'}
    if dest.parent.parent != ROOT / 'Graphics' or dest.parent.name not in categories:
        raise ValueError('Destino fuera de las carpetas gráficas de RGSS1')
    if dest.suffix.lower() != '.png' or source == dest:
        raise ValueError('Destino PNG distinto del origen, dentro de Graphics/')
    kind = spec['type']
    if kind not in ('character', 'indexed', 'battler', 'face', 'retrato', 'picture', 'battleback'):
        raise ValueError('Tipo de asset desconocido: ' + kind)
    im = Image.open(source).convert('RGBA')
    if spec.get('source_box'):
        box=tuple(map(int,spec['source_box']))
        if len(box)!=4 or not (0<=box[0]<box[2]<=im.width and 0<=box[1]<box[3]<=im.height):
            raise ValueError('Recorte de fuente fuera del lienzo')
        im=im.crop(box)
    # Las expresiones reutilizan literalmente ropa, pelo, luz y encuadre base.
    # El polígono normalizado limita la sustitución a ojos/cejas/boca generados.
    if spec.get('expression_base'):
        base = Image.open(path(spec['expression_base'])).convert('RGBA')
        im = im.resize(base.size, Image.Resampling.LANCZOS)
        points = spec['expression_polygon']
        if len(points) < 3 or any(not 0 <= v <= 1 for p in points for v in p):
            raise ValueError('Polígono facial normalizado inválido')
        mask = Image.new('L', base.size)
        ImageDraw.Draw(mask).polygon([(round(x*base.width), round(y*base.height)) for x,y in points], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(float(spec.get('expression_feather', 2))))
        im = Image.composite(im, base, mask)
        im.putalpha(base.getchannel('A'))
    if spec.get('key'):
        im = remove_key(im, spec['key'], int(spec.get('key_tolerance', 0)))
    threshold = spec.get('alpha_threshold')
    im = alpha_cleanup(im, threshold)
    resample = {'nearest': Image.Resampling.NEAREST, 'box': Image.Resampling.BOX,
                'lanczos': Image.Resampling.LANCZOS}[spec.get('resample', 'nearest')]
    padding = int(spec.get('padding', 1))
    if padding < 0:
        raise ValueError('Margen negativo')
    if spec.get('outline'):
        padding = max(1, padding)

    def finish(img):
        img = quantize(alpha_cleanup(img, threshold), spec.get('zone'))
        return outline(img, spec['outline']) if spec.get('outline') else img

    if kind == 'indexed':
        # Objetos/tiles/UI: los huecos y anclas vienen del respaldo, no de
        # una supuesta animación humana. Cada fuente conserva su propio índice.
        layout = Image.open(path(spec['layout_source'])).convert('RGBA')
        size = dimensions(spec['size'])
        cw, ch = dimensions(spec['cell'])
        if layout.size != size or size[0] % cw or size[1] % ch:
            raise ValueError('Layout indexado incompatible con tamaño/celda')
        cols, rows = size[0]//cw, size[1]//ch
        sc,sr=spec.get('source_grid',[cols,rows])
        if sc*sr!=cols*rows:
            raise ValueError('La fuente y destino deben contener el mismo numero de indices')
        xs = spec.get('source_columns', [round(x*im.width/sc) for x in range(sc+1)])
        ys = spec.get('source_rows', [round(y*im.height/sr) for y in range(sr+1)])
        for bounds, count, limit in ((xs, sc, im.width), (ys, sr, im.height)):
            if (len(bounds) != count+1 or bounds[0] != 0 or bounds[-1] != limit
                    or any(not isinstance(v, int) for v in bounds)
                    or any(a >= b for a, b in zip(bounds, bounds[1:]))):
                raise ValueError('Límites de fuente indexada incompatibles con su cuadrícula')
        result = Image.new('RGBA', size)
        mode = spec.get('indexed_mode', 'fit')
        if mode not in ('fit', 'resize'):
            raise ValueError('indexed_mode debe ser fit o resize')
        for y in range(rows):
            for x in range(cols):
                box = (x*cw, y*ch, (x+1)*cw, (y+1)*ch)
                old = layout.crop(box)
                bounds = old.getchannel('A').getbbox()
                if bounds is None:
                    continue
                if spec.get('repeat_source'):
                    tile = im.copy()
                else:
                    si=y*cols+x;sx,sy=si%sc,si//sc
                    tile = im.crop((xs[sx], ys[sy], xs[sx+1], ys[sy+1]))
                if mode == 'resize':
                    tile = tile.resize((cw, ch), resample)
                else:
                    target = (bounds[2]-bounds[0], bounds[3]-bounds[1])
                    fitted = place(crop(tile), target, 0, resample)
                    tile = Image.new('RGBA', (cw, ch))
                    tile.alpha_composite(fitted, bounds[:2])
                mix = float(spec.get('layout_mix', 0))
                if not 0 <= mix <= 1:
                    raise ValueError('layout_mix debe estar entre cero y uno')
                if mix:
                    alpha = tile.getchannel('A')
                    tile = Image.blend(tile, old, mix)
                    tile.putalpha(alpha)
                if spec.get('preserve_alpha'):
                    tile.putalpha(old.getchannel('A'))
                # Escala física por índice, independiente del tamaño de la celda.
                # Los recortes de componentes usan coordenadas de la celda adaptada;
                # permiten conservar una mesa y reducir sólo el objeto que soporta.
                rule = spec.get('cell_scale', {}).get(str(y*cols+x))
                if rule:
                    scaled = Image.new('RGBA', (cw, ch))
                    for part in rule.get('parts', [rule]):
                        obj = crop(tile.crop(tuple(part.get('crop', (0, 0, cw, ch)))))
                        height = int(part['height'])
                        width = max(1, round(obj.width*height/obj.height))
                        bottom = ch-int(part.get('bottom', 0))
                        if height < 1 or width > cw or bottom > ch or bottom-height < 0:
                            raise ValueError('Escala fuera de celda: ' + str(y*cols+x))
                        obj = alpha_cleanup(obj.resize((width, height), resample), threshold)
                        scaled.alpha_composite(obj, ((cw-width)//2, bottom-height))
                    tile = scaled
                tile = finish(tile)
                if y*cols+x in spec.get('opaque_indices', []):
                    ground = Image.new('RGBA', (cw, ch), spec.get('opaque_background', '#090f12'))
                    ground.alpha_composite(tile)
                    tile = ground
                result.alpha_composite(tile, (x*cw, y*ch))
    elif kind == 'character':
        cw, ch = dimensions(spec.get('cell', '32x48'))
        if spec.get('pad_grid') and (im.width % 4 or im.height % 4):
            padded = Image.new('RGBA', (im.width + (-im.width % 4), im.height + (-im.height % 4)))
            padded.alpha_composite(im)
            im = padded
        if im.width % 4 or im.height % 4:
            raise ValueError('Hoja de origen: ancho y alto deben ser divisibles entre 4')
        sw, sh = im.width//4, im.height//4
        # Algunas fuentes generadas espacian las filas de forma desigual.
        # Límites explícitos separan las poses completas sin perder cabeza/pies.
        xs = spec.get('source_columns', [x*sw for x in range(5)])
        ys = spec.get('source_rows', [y*sh for y in range(5)])
        for bounds, limit in ((xs, im.width), (ys, im.height)):
            if (len(bounds) != 5 or bounds[0] != 0 or bounds[-1] != limit
                    or any(not isinstance(v, int) for v in bounds)
                    or any(a >= b for a, b in zip(bounds, bounds[1:]))):
                raise ValueError('Límites de fuente: cinco enteros crecientes de cero al tamaño')
        cells = [crop(im.crop((xs[x], ys[y], xs[x+1], ys[y+1]))) for y in range(4) for x in range(4)]
        if min(cw, ch) <= 2*padding:
            raise ValueError('Margen incompatible con celda')
        # Una escala común evita que cada paso cambie el tamaño del cuerpo.
        ratio = min((cw-2*padding)/max(c.width for c in cells), (ch-2*padding)/max(c.height for c in cells))
        result = Image.new('RGBA', (cw*4, ch*4))
        for n, c in enumerate(cells):
            c = c.resize((max(1, round(c.width*ratio)), max(1, round(c.height*ratio))), resample)
            tile = Image.new('RGBA', (cw, ch))
            tile.alpha_composite(c, ((cw-c.width)//2, ch-padding-c.height))
            result.alpha_composite(finish(tile), ((n % 4)*cw, (n//4)*ch))
    elif kind in ('face', 'retrato'):
        size = dimensions(spec.get('size', '240x340'))
        if spec.get('preserve_canvas'):
            if im.size != size:
                raise ValueError('preserve_canvas requiere lienzo del tamaño de destino')
            result = finish(im)
        else:
            result = finish(place(crop(im), size, padding, resample))
    elif kind == 'battler':
        im = crop(im)
        height = int(spec.get('max_height', 300))
        if height <= padding*2:
            raise ValueError('Altura máxima insuficiente')
        if spec.get('size'):
            size = dimensions(spec['size'])
            if size[1] > height:
                raise ValueError('El lienzo supera max_height')
        else:
            scale = min(1, (height-padding*2)/im.height)
            size = (max(1, round(im.width*scale))+padding*2, round(im.height*scale)+padding*2)
        result = finish(place(im, size, padding, resample))
    else:
        size = dimensions(spec.get('size', '640x480'))
        # Cubrir sin deformar; recorte central. Preparar composición 4:3 en origen.
        result = ImageOps.fit(im, size, method=resample)
        if spec.get('preserve_alpha', False):
            result = finish(result)
        else:
            bg = Image.new('RGBA', size, spec.get('background', '#101217'))
            bg.alpha_composite(result)
            result = finish(bg).convert('RGB')
    return dest, result


def save(dest, im):
    backup = BACKUP / dest.relative_to(ROOT)
    if dest.exists() and not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest, backup)  # Primer original: nunca sobrescribirlo al iterar.
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(suffix='.png', dir=dest.parent)
    os.close(fd)
    try:
        im.save(temporary, format='PNG')
        os.replace(temporary, dest)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print(f'{dest.relative_to(ROOT)}: {im.width}x{im.height}, {im.mode}')


def review_inventory(value):
    """Auditoría de PNG y láminas 1x/2x; nunca escribe en Graphics ni Data."""
    inventory = json.loads(path(value).read_text(encoding='utf-8-sig'))
    installed = set()
    specs_by_dest = {}
    for manifest in (ROOT / 'diseno/fuentes/arte_hd2d').glob('lote_*.json'):
        for spec in json.loads(manifest.read_text(encoding='utf-8-sig'))['assets']:
            installed.add(spec['destination'])
            specs_by_dest[spec['destination']] = spec
    errors, checked = [], []
    for rel in installed - {r['path'] for r in inventory}:
        errors.append('Destino de manifiesto fuera del inventario: ' + rel)
    for row in inventory:
        rel = row['path']
        current, backup = ROOT / rel, BACKUP / rel
        if not current.exists() or not backup.exists():
            errors.append(f'Falta actual o respaldo: {rel}')
            continue
        with Image.open(current) as im, Image.open(backup) as original:
            im.load()
            if im.size != original.size or list(im.size) != row['size']:
                errors.append(f'Tamaño distinto: {rel}: {im.size} / {original.size}')
            if im.mode != row['mode']:
                errors.append(f'Modo distinto: {rel}: {im.mode} / {row["mode"]}')
            if rel.startswith('Graphics/Characters/') and (im.width % 4 or im.height % 4):
                errors.append('Cuadrícula no divisible entre cuatro: ' + rel)
            if rel.endswith('vacas_vacio.png') and im.convert('RGBA').getchannel('A').getbbox():
                errors.append('vacas_vacio dejó de ser transparente')
            if rel in installed and (rel.startswith(('Graphics/Characters/', 'Graphics/Battlers/')) or '/retrato_' in rel):
                if im.mode != 'RGBA' or im.getchannel('A').getextrema()[0] != 0:
                    errors.append('Falta transparencia: ' + rel)
            spec = specs_by_dest.get(rel, {})
            cell = [im.width//4, im.height//4] if '/Characters/' in rel else None
            slot_checks = None
            if spec.get('type') == 'indexed':
                cw, ch = dimensions(spec['cell'])
                cell = [cw, ch]
                blank, occupied = 0, 0
                for y in range(0, im.height, ch):
                    for x in range(0, im.width, cw):
                        box = (x, y, x+cw, y+ch)
                        before = original.convert('RGBA').crop(box).getchannel('A').getbbox()
                        after = im.convert('RGBA').crop(box).getchannel('A').getbbox()
                        if bool(before) != bool(after):
                            errors.append(f'Ocupación de celda cambiada: {rel} ({x//cw},{y//ch})')
                        if before:
                            occupied += 1
                            scale_rule = spec.get('cell_scale', {}).get(str(y//ch*(im.width//cw)+x//cw))
                            if scale_rule and after and after[3] != ch:
                                errors.append(f'Objeto escalado sin apoyo inferior: {rel} ({x//cw},{y//ch})')
                            if (not scale_rule and spec.get('indexed_mode', 'fit') == 'fit' and after and
                                    (after[0] < before[0] or after[1] < before[1] or
                                     after[2] > before[2] or after[3] > before[3])):
                                errors.append(f'Objeto fuera de su ancla: {rel} ({x//cw},{y//ch})')
                        else:
                            blank += 1
                slot_checks = {'occupied': occupied, 'empty_preserved': blank}
                if spec.get('preserve_alpha'):
                    expected_alpha = alpha_cleanup(original.convert('RGBA'), spec.get('alpha_threshold')).getchannel('A')
                    if ImageChops.difference(im.getchannel('A'), expected_alpha).getbbox():
                        errors.append('Máscara técnica distinta: ' + rel)
            if spec.get('repeat_source'):
                cw, ch = dimensions(spec['cell'])
                first = im.crop((0, 0, cw, ch)).tobytes()
                if any(im.crop((x, y, x+cw, y+ch)).tobytes() != first
                       for y in range(0, im.height, ch) for x in range(0, im.width, cw)):
                    errors.append('Celdas repetidas diferentes: ' + rel)
            status = 'FASE 2' if rel in installed else 'APROBADO FASE 1' if row['status'] == 'approved_phase1' else 'TECNICO' if row['status'] == 'technical_preserve' else 'PENDIENTE'
            checked.append({'path': rel, 'size': list(im.size), 'backup_size': list(original.size),
                            'status': status, 'mode': im.mode, 'cell': cell,
                            'backup_cell': cell, 'indexed_slots': slot_checks,
                            'sha256': hashlib.sha256(current.read_bytes()).hexdigest(),
                            'backup_sha256': hashlib.sha256(backup.read_bytes()).hexdigest()})
    protected_file = ROOT / 'diseno/fuentes/arte_hd2d/protegidos_fase2.json'
    protected = json.loads(protected_file.read_text(encoding='utf-8'))
    for rel, expected in protected.items():
        if not (ROOT/rel).exists() or hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() != expected:
            errors.append('Archivo protegido cambiado: ' + rel)
    report = {'checked': checked, 'errors': errors, 'protected_unchanged': not any('protegido' in e for e in errors),
              'scope': 'Inventario completo frente a respaldo y tamaño inicial; no prueba animación dentro del motor.'}
    (ROOT / 'diseno/verificaciones/fuentes/verificacion_fase2.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    objects = {'vacas_cosas', 'vacas_furgoneta', 'vacas_matadero', 'vacas_muebles', 'vacas_puerta', 'vacas_tablon', 'vacas_vacio'}
    groups = {
        'personajes': [r for r in checked if '/retrato_' in r['path'] or ('/Characters/' in r['path'] and Path(r['path']).stem not in objects)],
        'enemigos': [r for r in checked if '/Battlers/' in r['path']],
        'sustos': [r for r in checked if '/screamer_' in r['path']],
    }
    captures = ROOT / 'diseno/capturas/arte'
    captures.mkdir(parents=True, exist_ok=True)
    for name, rows in groups.items():
        columns = 1 if name == 'sustos' else 3
        width = max(r['size'][0] for r in rows)*3 + 48
        height = max(r['size'][1] for r in rows)*2 + 60
        sheet = Image.new('RGB', (columns*width, math.ceil(len(rows)/columns)*height+40), '#30343A')
        draw = ImageDraw.Draw(sheet)
        draw.text((12, 10), 'VACAS FASE 2 - ' + name + ' - izquierda 1x / derecha 2x - estados por archivo', fill='white')
        for n, row in enumerate(rows):
            x, y = (n % columns)*width, (n//columns)*height+40
            color = '#99D5A5' if row['status'] == 'FASE 2' else '#E2C580'
            draw.text((x+10,y+4), Path(row['path']).name, fill='white')
            draw.text((x+10,y+20), row['status'], fill=color)
            im = Image.open(ROOT / row['path']).convert('RGBA')
            sheet.paste(im, (x+10,y+44), im)
            enlarged = im.resize((im.width*2,im.height*2), Image.Resampling.NEAREST)
            sheet.paste(enlarged, (x+im.width+28,y+44), enlarged)
        sheet.save(captures / ('fase2_' + name + '.png'))
    print(json.dumps({'png_checked': len(checked), 'phase2_installed': len(installed), 'errors': errors}, ensure_ascii=False))
    if errors:
        raise ValueError('Errores de inventario; consultar verificacion_fase2.json')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--review-inventory', help='JSON de inventario: audita y crea láminas 1x/2x')
    p.add_argument('--review-source', help='Fuente para vista de inspección sobre fondo opaco')
    p.add_argument('--review-output', help='PNG de inspección dentro de diseno/capturas')
    p.add_argument('--batch', help='JSON: lista de assets o {"assets": [...]}')
    p.add_argument('--source')
    p.add_argument('--destination')
    p.add_argument('--type', choices=['character', 'indexed', 'battler', 'face', 'retrato', 'picture', 'battleback'])
    p.add_argument('--cell', default='32x48')
    p.add_argument('--size')
    p.add_argument('--max-height', type=int, default=300)
    p.add_argument('--padding', type=int, default=1)
    p.add_argument('--zone', choices=PALETTES)
    p.add_argument('--alpha-threshold', type=int)
    p.add_argument('--key', help='Color clave, por ejemplo #FF00FF')
    p.add_argument('--key-tolerance', type=int, default=0)
    p.add_argument('--outline', help='Color del contorno de 1 px')
    p.add_argument('--resample', choices=['nearest', 'box', 'lanczos'], default='nearest')
    args = vars(p.parse_args())
    review = args.pop('review_inventory')
    if review:
        review_inventory(review)
        return
    review_source, review_output = args.pop('review_source'), args.pop('review_output')
    if review_source:
        if not review_output:
            p.error('review-source requiere review-output')
        dest = path(review_output)
        dest.relative_to(ROOT / 'diseno/capturas')
        if dest.suffix.lower() != '.png':
            p.error('La vista debe ser PNG')
        im = alpha_cleanup(Image.open(path(review_source)).convert('RGBA'), 128)
        im.thumbnail((960, 960), Image.Resampling.BOX)
        bg = Image.new('RGBA', im.size, '#30343A')
        bg.alpha_composite(im)
        dest.parent.mkdir(parents=True, exist_ok=True)
        bg.convert('RGB').save(dest)
        return
    batch = args.pop('batch')
    try:
        if batch:
            specs = json.loads(path(batch).read_text(encoding='utf-8-sig'))
            if isinstance(specs, dict):
                specs = specs['assets']
            if not isinstance(specs, list) or not specs:
                raise ValueError('El lote debe contener una lista no vacía')
        else:
            specs = [{k: v for k, v in args.items() if v is not None}]
        # Validar todos antes de reemplazar el primer archivo.
        results = [adapt(s) for s in specs]
        if len({p for p, _ in results}) != len(results):
            raise ValueError('Destinos duplicados en el lote')
        for dest, im in results:
            save(dest, im)
    except (ValueError, KeyError, OSError, TypeError) as exc:
        p.exit(2, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
