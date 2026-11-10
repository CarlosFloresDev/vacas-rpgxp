"""Acto V: seis mapas apretados de 20x15. Base con baldosas del matadero y una capa
de utileria dibujada con PIL (sin IA ni GPU) troceada en baldosas nuevas del tileset 69.
   python maps5.py  -> b_tiles5.json, Graphics/Tilesets/acto5_matanza.png,
                       Graphics/Pictures/acto5_luzNN.png, maps5_info.json"""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json, random, math
from pathlib import Path
from PIL import Image, ImageDraw
from gfx_acto2 import ID
BASE = Path(__file__).resolve().parent
ROOT=_ROOT
RTP = Path('D:/SteamLibrary/steamapps/common/RPGXP/rtp/Graphics')
_src = ((_ROOT / 'diseno/herramientas/arte/revision_mapas.py')).read_text(encoding='utf-8')
_ns = dict(ROOT=ROOT, RTP=RTP, Image=Image, ImageDraw=ImageDraw, random=random)
exec(_src[_src.index('def asset'):_src.index('# Anchor positions')], _ns)
rev_prop = _ns['prop']
TS = Image.open(ROOT / 'Graphics/Tilesets/vacas_matadero.png').convert('RGBA')
OBJ = Image.open(ROOT / 'Graphics/Characters/vacas_matadero.png').convert('RGBA')
COSAS = Image.open(ROOT / 'Graphics/Characters/vacas_cosas.png').convert('RGBA')
BLOCKED = {n for n in ID if n.startswith('pared_') or n.startswith('ladrillo_')} | {
    'valla_h', 'valla_v', 'valla_poste', 'puerta_corral', 'taquilla_alta', 'taquilla_baja', 'banco', 'reloj_pared',
    'cinta', 'cinta_ini', 'cinta_fin', 'mesa_acero', 'escritorio_izq', 'escritorio_der', 'archivador_alto',
    'archivador_bajo', 'puerta_metal', 'rejilla_pared', 'tuberia', 'cajas', 'cubo_despojos', 'manguera',
    'ventana_nave', 'cajon_aturdir', 'cuchillos', 'fregadero', 'silla', 'ventana_oficina', 'persiana_alta',
    'persiana_baja', 'alambrada', 'cartel', 'farola', 'vacio'}
INV = {v: k for k, v in ID.items()}

def tile(name):
    i = ID[name] - 384
    return TS.crop((i % 8 * 32, i // 8 * 32, i % 8 * 32 + 32, i // 8 * 32 + 32))
def ofr(col, row):
    im = OBJ.crop((col * 32, row * 64, col * 32 + 32, row * 64 + 64)); return im.crop(im.getbbox())
def cfr(col, row):
    im = COSAS.crop((col * 32, row * 32, col * 32 + 32, row * 32 + 32)); return im.crop(im.getbbox())
OUT = '#151a18'

def draw(kind, r):
    def new(w, h):
        im = Image.new('RGBA', (w, h)); return im, ImageDraw.Draw(im)
    if kind in ('crate', 'shelf', 'rack', 'archive', 'bench', 'trash'):
        return rev_prop(kind, r.randint(0, 9999))
    if kind == 'crates2':
        im, d = new(32, 52); a = rev_prop('crate', 1); im.alpha_composite(a, (0, 20)); im.alpha_composite(a.resize((26, 26)), (r.choice([1, 4]), 0)); return im
    if kind == 'barrel':
        im, d = new(22, 30); c = r.choice(['#4a5f66', '#6b4a36', '#55604a'])
        d.rounded_rectangle((1, 3, 20, 29), radius=3, fill=c, outline=OUT); d.ellipse((1, 0, 20, 8), fill='#2a3230', outline=OUT)
        for y in (12, 21): d.line((2, y, 19, y), fill='#22292a')
        d.line((4, 9, 4, 27), fill='#8a9a94'); d.rectangle((9, 14, 14, 19), fill='#b9a14f'); return im
    if kind == 'pallet':
        im, d = new(32, 14)
        for y in (1, 9): d.rectangle((0, y, 31, y + 3), fill='#7b6243', outline='#2a2a22')
        for x in (1, 14, 27): d.rectangle((x, 4, x + 3, 9), fill='#4f3f2c')
        return im
    if kind == 'sacks':
        im, d = new(32, 30)
        for i, (x, y) in enumerate([(0, 16), (15, 17), (7, 6)]):
            d.rounded_rectangle((x, y, x + 16, y + 12), radius=4, fill=['#8f8667', '#7c7458', '#9a9070'][i], outline='#2c2a20'); d.line((x + 3, y + 3, x + 12, y + 3), fill='#5d573f')
        return im
    if kind == 'truck':
        im, d = new(128, 64)
        d.rectangle((30, 6, 126, 50), fill='#3d4640', outline=OUT)
        for x in range(34, 124, 9): d.rectangle((x, 10, x + 5, 46), fill='#232a27')
        for y in (16, 28, 40): d.line((31, y, 125, y), fill='#6f7a6d', width=2)
        d.rectangle((2, 18, 30, 50), fill='#7a2f26', outline=OUT); d.rectangle((5, 22, 18, 34), fill='#141c20'); d.line((6, 24, 12, 24), fill='#52646a')
        d.rectangle((0, 46, 127, 52), fill='#1d2220')
        for x in (8, 52, 104): d.ellipse((x, 44, x + 18, 62), fill='#0f1211', outline='#2e3432'); d.ellipse((x + 6, 50, x + 12, 56), fill='#4a504c')
        for _ in range(7): x = r.randint(36, 118); d.line((x, 46, x + r.randint(-2, 2), 50), fill='#5a2019')
        d.rectangle((118, 30, 126, 50), fill='#2b312e'); return im
    if kind == 'farol':
        im, d = new(18, 64); d.rectangle((8, 8, 10, 62), fill='#2c3431'); d.rectangle((5, 58, 13, 63), fill='#222826')
        d.polygon([(2, 8), (16, 8), (13, 2), (5, 2)], fill='#39423d', outline=OUT); d.rectangle((5, 8, 13, 10), fill='#e6d58a'); return im
    if kind == 'dumpster':
        im, d = new(60, 38); d.polygon([(2, 10), (57, 10), (53, 36), (6, 36)], fill='#35503f', outline=OUT); d.rectangle((0, 6, 59, 11), fill='#27382e', outline=OUT)
        for x in (16, 30, 44): d.line((x, 12, x, 35), fill='#27382e')
        d.ellipse((20, 0, 34, 9), fill='#7d6f5b'); d.line((38, 5, 47, 1), fill='#c9c1a6', width=2); d.ellipse((6, 26, 16, 33), fill='#5a2019'); return im
    if kind == 'cone':
        im, d = new(10, 14); d.polygon([(4, 0), (6, 0), (9, 12), (0, 12)], fill='#a8562b', outline='#2c1c12'); d.line((2, 7, 7, 7), fill='#d9d0b8'); d.rectangle((0, 12, 9, 13), fill='#3b2a20'); return im
    if kind in ('carcass0', 'carcass1', 'carcass2'): return ofr(int(kind[-1]), 1)
    if kind == 'hook': return ofr(3, 1)
    if kind == 'panelreloj': return ofr(0, 2)
    if kind == 'bucket': return ofr(2, 2)
    if kind == 'meatbox': return ofr(3, 2)
    if kind == 'dung': return cfr(3, 0)
    if kind == 'note': return cfr(0, 1)
    if kind == 'bottles': return cfr(1, 1)
    if kind == 'meat': return cfr(r.randint(0, 2), 0)
    if kind == 'radiotable':
        im, d = new(28, 28); d.rectangle((1, 12, 26, 18), fill='#6a5a44', outline=OUT); d.rectangle((3, 19, 5, 27), fill='#3a3128'); d.rectangle((22, 19, 24, 27), fill='#3a3128')
        d.rounded_rectangle((6, 3, 20, 12), radius=2, fill='#8a7350', outline=OUT); d.ellipse((8, 5, 13, 10), fill='#2b2620'); d.rectangle((15, 5, 18, 7), fill='#d7b95e'); d.line((19, 3, 24, 0), fill='#9aa39a'); return im
    if kind == 'heater':
        im, d = new(20, 26); d.rounded_rectangle((1, 4, 18, 25), radius=2, fill='#4a4f4b', outline=OUT)
        for y in range(8, 22, 3): d.line((4, y, 15, y), fill='#c7682c' if y < 17 else '#272b29')
        d.rectangle((7, 0, 12, 4), fill='#2f3431'); return im
    if kind == 'stool':
        im, d = new(14, 14); d.ellipse((1, 1, 12, 7), fill='#6d5a40', outline=OUT); d.line((3, 7, 2, 13), fill='#2f2a22', width=2); d.line((10, 7, 11, 13), fill='#2f2a22', width=2); return im
    if kind == 'keyboard':
        im, d = new(24, 18); d.rectangle((0, 0, 23, 17), fill='#5d4a35', outline=OUT)
        for x in range(3, 21, 5):
            for y in (3, 10): d.point((x, y), fill='#d0c9aa'); d.line((x, y + 1, x, y + 4), fill=r.choice(['#b9a14f', '#9aa39a']))
        return im
    if kind == 'calendar':
        im, d = new(12, 16); d.rectangle((0, 0, 11, 15), fill='#cfc6a6', outline=OUT); d.rectangle((1, 1, 10, 5), fill='#7a2f26')
        for y in (8, 11, 13): d.line((2, y, 9, y), fill='#6f6a56')
        return im
    if kind == 'board':
        im, d = new(44, 24); d.rectangle((0, 0, 43, 23), fill='#6f5a3c', outline=OUT)
        for _ in range(6):
            x, y = r.randint(2, 32), r.randint(2, 13); d.rectangle((x, y, x + 8, y + 8), fill=r.choice(['#d2caa9', '#b9b294', '#c9b98a'])); d.line((x + 1, y + 3, x + 6, y + 3), fill='#57523f'); d.point((x + 4, y), fill='#a33a2c')
        return im
    if kind == 'skull':
        im, d = new(24, 22); d.polygon([(6, 4), (17, 4), (16, 14), (13, 21), (10, 21), (7, 14)], fill='#cfc7ab', outline='#2c2a20')
        d.line((6, 5, 0, 1), fill='#a59b7c', width=2); d.line((17, 5, 23, 1), fill='#a59b7c', width=2); d.rectangle((8, 8, 10, 11), fill='#2a2620'); d.rectangle((13, 8, 15, 11), fill='#2a2620'); return im
    if kind == 'plaque':
        im, d = new(46, 14); d.rectangle((0, 0, 45, 13), fill='#b9b294', outline=OUT); d.rectangle((2, 2, 12, 11), fill='#7a2f26')
        for x in range(16, 42, 6): d.rectangle((x, 4, x + 3, 9), fill='#3c3a30')
        return im
    if kind == 'fusebox':
        im, d = new(20, 24); d.rectangle((0, 0, 19, 23), fill='#5a625c', outline=OUT); d.rectangle((3, 3, 16, 12), fill='#2b302d')
        for x in (5, 9, 13): d.rectangle((x, 5, x + 1, 10), fill='#c9c1a6')
        d.polygon([(8, 15), (12, 15), (10, 21)], fill='#d7b95e'); return im
    if kind == 'siren':
        im, d = new(22, 24); d.rectangle((2, 8, 19, 23), fill='#5a625c', outline=OUT); d.pieslice((3, 0, 18, 16), 180, 360, fill='#9a2a22', outline=OUT); d.line((7, 4, 9, 2), fill='#e0a79a'); d.line((10, 23, 10, 23), fill='#111'); d.rectangle((8, 13, 13, 18), fill='#2b302d'); return im
    if kind == 'armero':
        im, d = new(28, 28); d.rectangle((0, 0, 27, 27), fill='#4f5a54', outline=OUT); d.rectangle((3, 3, 24, 24), fill='#1f2522')
        d.rectangle((6, 9, 20, 13), fill='#9aa39a'); d.rectangle((16, 13, 20, 21), fill='#5d4a35'); d.rectangle((4, 10, 7, 12), fill='#d0d6cc'); d.point((25, 14), fill='#d7b95e'); return im
    if kind == 'cuadro':
        im, d = new(30, 30); d.rectangle((0, 0, 29, 29), fill='#59605b', outline=OUT); d.rectangle((3, 3, 26, 12), fill='#1c2421')
        for i, x in enumerate((6, 13, 20)): d.ellipse((x, 5, x + 4, 9), fill=['#a33a2c', '#b9a14f', '#5c8a55'][i])
        d.rectangle((6, 16, 10, 26), fill='#2b302d'); d.rectangle((7, 15, 9, 20), fill='#c9c1a6'); d.rectangle((17, 16, 21, 26), fill='#2b302d'); d.rectangle((18, 21, 20, 26), fill='#a33a2c'); return im
    if kind == 'prods':
        im, d = new(30, 22); d.rectangle((0, 2, 29, 5), fill='#5d4a35', outline=OUT)
        for x in (4, 12, 20): d.line((x, 5, x, 20), fill='#b9a14f', width=2); d.rectangle((x - 1, 16, x + 1, 21), fill='#2a2620')
        return im
    if kind == 'hooks':
        im, d = new(40, 22); d.rectangle((0, 2, 39, 5), fill='#7c8580', outline=OUT)
        for x in range(4, 38, 7): d.line((x, 5, x, 14), fill='#c3cbc4'); d.arc((x - 4, 10, x, 18), 0, 180, fill='#c3cbc4'); d.point((x - 3, 16), fill='#7a1f18')
        return im
    if kind == 'thermo':
        im, d = new(8, 20); d.rectangle((0, 0, 7, 19), fill='#cfd6d0', outline=OUT); d.line((4, 3, 4, 15), fill='#3f6f8a', width=2); return im
    if kind == 'trough':
        im, d = new(60, 16); d.polygon([(0, 2), (59, 2), (55, 15), (4, 15)], fill='#4c5450', outline=OUT); d.rectangle((3, 3, 56, 6), fill='#6f6a40'); return im
    if kind == 'bale':
        im, d = new(30, 24); d.rounded_rectangle((0, 3, 29, 23), radius=2, fill='#a08a4a', outline='#3a321c')
        for y in range(6, 23, 4): d.line((1, y, 28, y + r.randint(-1, 1)), fill='#7a6a36')
        for x in (9, 20): d.line((x, 3, x, 23), fill='#4a3f2a')
        return im
    if kind == 'noria':
        im, d = new(40, 64); d.rectangle((3, 0, 6, 63), fill='#59605b', outline=OUT); d.rectangle((33, 0, 36, 63), fill='#59605b', outline=OUT); d.rectangle((0, 2, 39, 8), fill='#6e7670', outline=OUT)
        d.ellipse((13, 10, 27, 24), fill='#2b302d', outline='#8a938c'); d.line((20, 24, 20, 46), fill='#aab2ab'); d.arc((15, 42, 25, 54), 0, 200, fill='#c9d0c9', width=2)
        d.rectangle((0, 58, 39, 63), fill='#3d4440'); d.ellipse((14, 56, 28, 62), fill='#5a1b16'); return im
    if kind == 'cart':
        im, d = new(36, 30); d.polygon([(2, 4), (33, 4), (30, 22), (5, 22)], fill='#7d8782', outline=OUT); d.rectangle((0, 2, 35, 5), fill='#59605b')
        d.ellipse((6, 0, 18, 7), fill='#7a2a22'); d.ellipse((16, 1, 28, 7), fill='#93403a'); d.ellipse((6, 22, 12, 29), fill='#1b1f1d'); d.ellipse((24, 22, 30, 29), fill='#1b1f1d'); d.line((9, 9, 10, 20), fill='#5a1b16'); return im
    if kind == 'safe':
        im, d = new(28, 30); d.rectangle((0, 0, 27, 29), fill='#3f4a45', outline=OUT); d.rectangle((3, 3, 24, 26), fill='#4f5b55', outline='#232a27'); d.ellipse((10, 10, 17, 17), fill='#b9a14f', outline='#2a2a22'); d.line((20, 9, 20, 19), fill='#9aa39a', width=2); return im
    if kind == 'sofa':
        im, d = new(60, 32); d.rounded_rectangle((0, 2, 59, 22), radius=4, fill='#5a3a2a', outline=OUT); d.rounded_rectangle((4, 12, 55, 27), radius=3, fill='#70493a', outline='#2a1c14')
        d.line((30, 13, 30, 26), fill='#2a1c14'); d.line((12, 16, 17, 20), fill='#c9c1a6'); d.rectangle((3, 27, 7, 31), fill='#221a14'); d.rectangle((52, 27, 56, 31), fill='#221a14'); return im
    if kind == 'coatrack':
        im, d = new(18, 54); d.line((9, 2, 9, 52), fill='#3a3128', width=2); d.line((3, 53, 15, 53), fill='#3a3128', width=2); d.line((4, 4, 14, 4), fill='#3a3128', width=2)
        d.polygon([(3, 6), (9, 6), (11, 30), (2, 30)], fill='#70664a', outline='#2a261c'); d.line((6, 8, 6, 28), fill='#4f4834'); return im
    if kind == 'plant':
        im, d = new(16, 26); d.polygon([(3, 16), (12, 16), (11, 25), (4, 25)], fill='#70493a', outline=OUT)
        for a in (-5, -1, 3): d.line((8, 16, 8 + a, 3 + abs(a)), fill='#5a5a3a')
        return im
    if kind == 'deskset':
        im, d = new(60, 22); d.rectangle((4, 12, 15, 19), fill='#cfc6a6'); d.line((6, 15, 13, 15), fill='#5d584a'); d.rectangle((2, 10, 13, 17), fill='#bfb692', outline='#5d584a')
        d.rectangle((22, 13, 31, 19), fill='#1d2220'); d.line((23, 12, 30, 12), fill='#3a403d', width=2)
        d.rectangle((40, 6, 43, 18), fill='#4f6a3a', outline='#1f2a18'); d.rectangle((41, 3, 42, 6), fill='#1f2a18'); d.rectangle((46, 13, 49, 18), fill='#a9b2aa')
        d.line((54, 18, 54, 6), fill='#2a2a22', width=2); d.polygon([(49, 6), (59, 6), (56, 0), (52, 0)], fill='#4f6a3a', outline=OUT); d.line((51, 7, 57, 7), fill='#f0e2a0'); return im
    if kind == 'rug':
        im, d = new(96, 60); d.rectangle((0, 0, 95, 59), fill=(92, 46, 38, 215), outline=(40, 22, 18, 255)); d.rectangle((6, 6, 89, 53), outline=(150, 120, 80, 200))
        for _ in range(30): x, y = r.randint(2, 90), r.randint(2, 55); d.line((x, y, x + r.randint(2, 6), y), fill=(60, 30, 26, 200))
        return im
    if kind == 'railing':
        im, d = new(32, 22); d.line((0, 2, 31, 2), fill='#8a938c', width=2); d.line((0, 12, 31, 12), fill='#5d6660')
        for x in (1, 16, 30): d.line((x, 2, x, 21), fill='#6e7670', width=2)
        return im
    if kind == 'blood':
        s = r.randint(18, 30); im, d = new(s + 8, s)
        for _ in range(5):
            x, y = r.randint(0, s // 2), r.randint(0, s // 2); d.ellipse((x, y, x + r.randint(7, s // 2 + 4), y + r.randint(4, s // 3 + 3)), fill=(96, 22, 18, r.randint(150, 215)))
        return im
    if kind == 'bloodtrail':
        im, d = new(20, 64)
        for y in range(0, 62, r.randint(5, 8)): x = 8 + r.randint(-5, 5); d.ellipse((x, y, x + r.randint(2, 5), y + r.randint(2, 4)), fill=(104, 24, 18, 220))
        return im
    if kind == 'drag':
        im, d = new(64, 18)
        for y in (3, 8, 13): d.line((r.randint(0, 6), y, 63 - r.randint(0, 9), y + r.randint(-2, 2)), fill=(86, 24, 20, 150), width=2)
        return im
    if kind == 'puddle':
        im, d = new(40, 18); d.ellipse((0, 2, 38, 16), fill=(18, 26, 30, 150)); d.arc((6, 5, 26, 12), 190, 300, fill=(120, 130, 120, 160)); return im
    if kind == 'oil':
        im, d = new(26, 14); d.ellipse((0, 1, 25, 12), fill=(10, 12, 12, 170)); d.ellipse((6, 3, 14, 8), fill=(60, 50, 80, 90)); return im
    if kind == 'tracks':
        im, d = new(96, 20)
        for y in (2, 14):
            for x in range(0, 94, 5): d.line((x, y, x + 2, y + 3), fill=(12, 14, 14, 120), width=2)
        return im
    if kind == 'cable':
        im, d = new(60, 22); pts = [(0, r.randint(4, 16))]
        for x in range(10, 61, 10): pts.append((x, r.randint(2, 19)))
        d.line(pts, fill=(20, 26, 24, 230), width=2); return im
    if kind == 'papers':
        im, d = new(28, 20)
        for _ in range(3):
            p = Image.new('RGBA', (12, 9)); pd = ImageDraw.Draw(p); pd.rectangle((0, 0, 11, 8), fill=(172, 164, 132, 220)); pd.line((2, 3, 9, 3), fill='#5d584a'); pd.line((2, 6, 7, 6), fill='#5d584a')
            p = p.rotate(r.randint(-40, 40), expand=True); im.alpha_composite(p, (r.randint(0, 12), r.randint(0, 6)))
        return im
    if kind == 'straw':
        im, d = new(32, 20)
        for _ in range(16): x, y = r.randint(1, 26), r.randint(1, 16); d.line((x, y, x + r.randint(-4, 5), y + r.randint(-2, 3)), fill=(150, 128, 70, 200))
        return im
    if kind == 'chain':
        im, d = new(12, 22)
        for y in range(0, 20, 4): d.ellipse((3 + (y // 4) % 2, y, 8 + (y // 4) % 2, y + 5), outline='#b7bdb5')
        d.rectangle((2, 17, 9, 21), fill='#b9a14f', outline=OUT); return im
    if kind == 'hoofs':
        im, d = new(40, 30)
        for i in range(5): x, y = 4 + i * 7 + r.randint(-2, 2), 22 - i * 4 + r.randint(-3, 3); d.ellipse((x, y, x + 3, y + 5), fill=(70, 26, 20, 190)); d.ellipse((x + 4, y, x + 7, y + 5), fill=(70, 26, 20, 190))
        return im
    if kind == 'cap':
        im, d = new(14, 9); d.pieslice((0, 0, 11, 14), 180, 360, fill='#3a4a3a', outline=OUT); d.line((9, 7, 13, 7), fill='#222a22', width=2); return im
    if kind == 'ramp':
        im, d = new(30, 40); d.polygon([(4, 0), (26, 0), (29, 39), (0, 39)], fill='#4c5450', outline=OUT)
        for y in range(5, 38, 6): d.line((3, y, 27, y), fill='#2b302d')
        return im
    if kind == 'tile:rail': return tile('rail')
    if kind == 'tile:rail_gancho': return tile('rail_gancho')
    if kind == 'tile:lampara': return tile('lampara')
    raise ValueError(kind)

# ---------------------------------------------------------------- definicion de mapas
FLOOR = {'.': ('azulejo', 'azulejo_sucio', .38), ',': ('hormigon', 'hormigon_mojado', .1), ':': ('suelo_frio', 'suelo_frio', 0),
         'o': ('linoleo', 'linoleo', 0), 'a': ('asfalto', 'asfalto_charco', .04), 'c': ('acera', 'acera', 0), 'p': ('paja', 'paja', 0),
         'b': ('barro', 'barro', 0), 'g': ('rejilla_suelo',) * 2 + (0,), 's': ('azulejo_sangre',) * 2 + (0,), 'r': ('azulejo_arrastre',) * 2 + (0,),
         'W': 'pared_azulejo_alta', 'w': 'pared_azulejo_baja', 'H': 'pared_hormigon_alta', 'h': 'pared_hormigon_baja', 'F': 'pared_fria_alta',
         'f': 'pared_fria_baja', 'M': 'pared_madera_alta', 'm': 'pared_madera_baja', 'L': 'ladrillo_alto', 'l': 'ladrillo_bajo'}
M = {}
def mapa(mid, rows, furn, props, lights, tint, dark, blood=0.0):
    assert len(rows) == 15 and all(len(x) == 20 for x in rows), (mid, [len(x) for x in rows])
    M[mid] = dict(rows=rows, furn=furn, props=props, lights=lights, tint=tint, dark=dark, blood=blood)
def P(kind, x, y, dx=0, dy=0, block=True, flip=False): return ('P', kind, x, y, dx, dy, block, flip)
def D(kind, x, y, dx=0, dy=0, flip=False): return ('D', kind, x, y, dx, dy, False, flip)       # calco de suelo/pared
def O(kind, x, y, dx=0, dy=0): return ('O', kind, x, y, dx, dy, False, False)                    # sobre la cabeza
def F(name, *cells): return [(x, y, name) for x, y in cells]
def span(y, x1, x2): return [(x, y) for x in range(x1, x2 + 1)]
def col(x, y1, y2): return [(x, y) for y in range(y1, y2 + 1)]

# 22 Muelle de carga ---------------------------------------------------------------
mapa(22, [
    '####################', 'LLLLLLLLLLLLLLLLLLLL', 'llllllllllllllllllll', 'ccccccccccccccc#MMM#', 'ccccccccccccccc#mmm#',
    'aaaaaaaaaaaaaaa#ooo#', 'aaaaaaaaaaaaaaa#ooo#', 'aaaaaaaaaaaaaaa##o##', 'aaaaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaa',
    'aaaaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaa', 'aaagaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaa'],
    F('puerta_metal', (4, 2)) + F('cartel', (6, 2)) + F('ventana_nave', (10, 2), (12, 2)) + F('tuberia', (14, 2), (1, 2)) + F('rejilla_pared', (2, 2))
    + F('reloj_pared', (17, 4)) + F('alambrada', *span(13, 0, 19)) + F('huellas', (4, 5), (5, 8), (4, 4)) + F('mancha', (9, 10), (13, 8)),
    [P('truck', 6, 9, dx=2), P('truck', 11, 11, dx=4, flip=True), P('ramp', 5, 9, dx=6, dy=4, block=False), P('crates2', 8, 3), P('crate', 9, 3, dx=3), P('bench', 0, 3, dx=2),
     P('sacks', 11, 3), P('pallet', 11, 4, dy=-2, block=False), P('barrel', 13, 3, dx=3), P('barrel', 14, 3, dx=1, dy=-3), P('barrel', 0, 5, dx=4), P('pallet', 9, 5, dy=-6, block=False),
     P('barrel', 0, 12, dx=2), P('barrel', 1, 12, dx=-3, dy=-4), P('crate', 2, 12, dx=-4), P('dumpster', 17, 12, dx=2), P('sacks', 19, 10), P('pallet', 19, 10, dy=1, block=False),
     P('crates2', 19, 8), P('farol', 0, 8, dx=7), P('farol', 15, 10, dx=7), P('cone', 3, 5, dx=12, dy=-8, block=False), P('cone', 10, 7, dx=8, dy=-6, block=False),
     P('crate', 13, 5), P('crate', 16, 12, dx=-2), P('barrel', 15, 12, dx=2), P('pallet', 6, 12, dy=-5, block=False), P('sacks', 7, 12, dx=-6), P('cone', 15, 8, dx=10, dy=-10, block=False),
     P('radiotable', 16, 5, dx=2), P('heater', 18, 6, dx=6), D('stool', 16, 6, dx=8, dy=-6), D('keyboard', 18, 4, dx=4, dy=-6), D('calendar', 16, 4, dx=10, dy=-8),
     D('plaque', 7, 2, dx=6, dy=-10), D('tracks', 2, 8, dy=-4), D('tracks', 8, 12, dx=10, dy=-2), D('tracks', 15, 10, dx=40, dy=6), D('puddle', 2, 10, dx=6), D('puddle', 16, 9, dx=4, dy=-8),
     D('oil', 10, 10, dx=8), D('oil', 4, 7), D('bloodtrail', 4, 5, dx=6, dy=20), D('bloodtrail', 5, 8, dx=-2, dy=6), D('blood', 5, 9, dx=-8), D('blood', 4, 3, dx=6, dy=-2),
     D('papers', 12, 7, dx=4), D('papers', 17, 9), D('cable', 15, 8, dx=-30, dy=-6), D('straw', 5, 10, dx=10), D('straw', 9, 11), D('straw', 14, 12, dx=8), D('papers', 2, 4),
     D('hoofs', 6, 5, dy=-4), D('note', 17, 6, dx=18, dy=-14)],
    [(4, 3, 1.0), (17, 5, .9), (15, 9, 1.2), (0, 7, 1.1), (9, 11, .6)], (26, 20, 8), 150)

# 23 Corrales de espera -------------------------------------------------------------
PEN_U = [(1, 5), (7, 11), (13, 17)]; PEN_L = [(1, 5), (7, 11)]
f23 = F('rejilla_pared', (6, 2)) + F('tuberia', (3, 2), (15, 2)) + F('cartel', (9, 2))
for a, b in PEN_U:
    f23 += F('valla_v', *col(a, 3, 5), *col(b, 3, 5)) + F('valla_poste', (a, 6), (b, 6)) + F('valla_h', (a + 1, 6), (a + 3, 6)) + F('puerta_corral', (a + 2, 6))
for a, b in PEN_L:
    f23 += F('valla_v', *col(a, 10, 12), *col(b, 10, 12)) + F('valla_poste', (a, 9), (b, 9), (a, 13), (b, 13)) + F('valla_h', (a + 1, 9), (a + 3, 9), *span(13, a + 1, a + 3)) + F('puerta_corral', (a + 2, 9))
f23 += F('paja_suelta', (6, 5), (12, 4), (4, 7), (10, 8), (15, 7), (6, 10), (12, 11), (17, 8)) + F('huellas', (8, 7), (13, 7), (18, 7), (12, 9)) + F('mancha', (3, 8), (16, 6))
mapa(23, [
    '####################', 'HHHHHHHHHHHHHHHHHHHH', 'hhhhhhhhhhhhhhhhhhhh', '#,ppp,,,ppp,,,ppp,,#', '#,ppp,,,ppp,,,ppp,,#',
    '#,ppp,,,ppp,,,ppp,,#', '#,,,,,,,,,,,,,,,,,,#', '#,,,,,,,,,,,,,,,,,,,', '#,,,,,,,,,,,,,,,,,,#', '#,,,,,,,,,,,,,######',
    '#,ppp,,,ppp,,,#hhhh#', '#,ppp,,,ppp,,,,,,,,#', '#,ppp,,,ppp,,,#,,,,#', '#,,,,,,,,,,,,,######', '############,#######'],
    f23,
    [P('sacks', 18, 3), P('bale', 18, 4, dx=1), P('bale', 6, 13, dx=1), P('barrel', 13, 13, dx=6), P('crate', 13, 10), P('bucket', 13, 12, dx=8, dy=-4, block=False),
     P('barrel', 18, 12, dx=6), P('crate', 16, 12, dx=2), P('heater', 15, 12, dx=4), D('stool', 17, 12, dx=8, dy=-6), D('siren', 16, 10, dx=5, dy=-5), D('board', 17, 10, dx=12, dy=-4),
     D('calendar', 15, 10, dx=8, dy=-8), D('prods', 18, 2, dy=-6), D('board', 12, 2, dx=-6, dy=-4), D('plaque', 9, 2, dx=-40, dy=-8), D('hooks', 16, 2, dx=-10, dy=-6),
     P('trough', 2, 3, dx=6, dy=-14, block=False), P('trough', 8, 5, dx=20, dy=2, block=False), P('trough', 14, 3, dx=6, dy=-14, block=False), P('trough', 2, 12, dx=10, dy=2, block=False), P('trough', 8, 10, dx=8, dy=-14, block=False),
     D('dung', 3, 4, dx=6), D('dung', 9, 4, dx=-6, dy=4), D('dung', 15, 5, dx=10), D('dung', 3, 11, dx=8), D('dung', 9, 12, dx=-8), D('dung', 16, 3, dx=4), D('straw', 2, 5), D('straw', 9, 3),
     D('straw', 14, 5), D('straw', 3, 11), D('straw', 8, 11), D('chain', 3, 6, dx=10, dy=-2), D('chain', 9, 6, dx=10, dy=-2), D('chain', 15, 6, dx=10, dy=-2), D('chain', 3, 9, dx=10, dy=-2), D('chain', 9, 9, dx=10, dy=-2),
     D('puddle', 5, 7, dx=10), D('puddle', 14, 8, dx=-6), D('drag', 16, 7, dx=10, dy=-4), D('hoofs', 10, 7), D('hoofs', 2, 8, dx=-4), D('blood', 18, 7, dx=-6), D('cable', 15, 11, dx=4, dy=-4),
     D('papers', 17, 11, dx=6), D('straw', 12, 6), D('straw', 6, 8, dx=8), D('straw', 12, 13), D('puddle', 6, 11, dx=-4, dy=-6), D('straw', 18, 6), D('bucket', 6, 3, dx=18, dy=-14), D('papers', 12, 3, dx=6),
     O('tile:lampara', 3, 7), O('tile:lampara', 9, 7), O('tile:lampara', 15, 7), O('tile:lampara', 12, 11)],
    [(3, 7, 1.0), (9, 7, 1.0), (15, 7, 1.0), (16, 11, .8), (12, 11, .8)], (8, 22, 14), 150)

# 24 Sala de matanza ----------------------------------------------------------------
f24 = (F('valla_h', *span(6, 1, 5), *span(8, 1, 3)) + F('cajon_aturdir', (7, 7)) + F('cinta_ini', (9, 6)) + F('cinta', *span(6, 10, 14)) + F('cinta_fin', (15, 6))
       + F('mesa_acero', (3, 3), (4, 3), (2, 13), (3, 13)) + F('fregadero', (1, 3)) + F('cuchillos', (3, 2), (5, 2)) + F('manguera', (18, 3)) + F('cajas', (18, 5), (10, 10))
       + F('cubo_despojos', (4, 10), (5, 13), (11, 5)) + F('puerta_metal', (17, 2)) + F('ventana_nave', (8, 2), (12, 2)) + F('tuberia', (15, 2), (6, 2)) + F('reloj_pared', (10, 2))
       + F('azulejo_sangre', (8, 8), (9, 4), (14, 5)) + F('azulejo_arrastre', (9, 8), (10, 8)) + F('huellas', (5, 7), (3, 7), (12, 4)) + F('mancha', (6, 9), (16, 4), (2, 12)))
mapa(24, [
    '####################', 'WWWWWWWWWWWWWWWWWWWW', 'wwwwwwwwwwwwwwwwwwww', '#..................#', '#..................#',
    '#..................#', '#..................#', '............########', '#...........#wwwwww#', '#..................#',
    '#...........#......#', '#~~~~~~~~~~~########', '#...........wwwwwww#', '#..................#', '####################'],
    f24,
    [P('noria', 8, 7, dx=-4), P('carcass0', 10, 4), P('carcass2', 13, 4), P('carcass1', 15, 4, dx=2), P('cart', 2, 10, dx=-2), P('barrel', 1, 9, dx=4), P('cart', 7, 13), P('barrel', 9, 13, dx=4),
     P('barrel', 10, 13, dx=-2, dy=-3), P('crates2', 18, 13), P('crate', 17, 13, dx=-2), P('crate', 16, 13, dx=2), P('heater', 18, 10, dx=6), P('crate', 18, 9), D('stool', 16, 10, dx=10, dy=-4),
     P('meatbox', 12, 6, dy=-12, block=False), P('meatbox', 14, 6, dx=-4, dy=-12, block=False), P('meat', 10, 6, dx=8, dy=-14, block=False), P('bucket', 16, 5, dx=8, dy=-2), P('bucket', 1, 5, dx=4), P('crate', 1, 4),
     P('barrel', 18, 6, dx=4), D('meat', 3, 3, dx=6, dy=-14), D('meat', 2, 13, dx=10, dy=-14), D('bottles', 4, 3, dx=6, dy=-12), D('cuadro', 15, 8), D('fusebox', 17, 8, dx=6, dy=-4), D('calendar', 13, 8, dx=10, dy=-8),
     D('armero', 15, 12, dx=2, dy=-2), D('hooks', 13, 12, dx=-8, dy=-6), D('plaque', 17, 12, dx=-10, dy=-10), D('plaque', 1, 2, dx=6, dy=-8), D('hooks', 13, 2, dy=-4),
     D('blood', 7, 8, dx=6), D('blood', 9, 7, dx=4, dy=-4), D('blood', 10, 5), D('blood', 13, 5, dx=6, dy=-2), D('blood', 15, 5, dx=-4), D('blood', 3, 12, dx=6), D('blood', 8, 12, dx=-6), D('drag', 5, 9, dy=-6),
     D('drag', 9, 9, dx=6, dy=2), D('bloodtrail', 8, 9, dx=10), D('bloodtrail', 6, 10, dx=4, dy=14), D('puddle', 3, 9, dx=10), D('puddle', 14, 13, dx=6, dy=-4), D('cable', 13, 10, dy=-4), D('papers', 14, 9, dx=8),
     D('hoofs', 1, 7, dx=8, dy=-2), D('hoofs', 4, 7, dy=-2), D('straw', 2, 7), D('straw', 5, 8, dx=8), D('blood', 17, 4, dx=-2), D('bloodtrail', 17, 3, dx=6, dy=-8), D('papers', 7, 4), D('chain', 16, 3, dx=14, dy=-12),
     D('blood', 11, 12, dx=-2, dy=-4), D('puddle', 6, 12, dx=-10), D('blood', 4, 5, dx=4), D('drag', 12, 3, dx=-6, dy=10),
     O('tile:rail', 8, 3), O('tile:rail_gancho', 9, 3), O('tile:rail', 11, 3), O('tile:rail_gancho', 12, 3), O('tile:rail', 14, 3), O('tile:rail_gancho', 16, 3), O('tile:rail', 17, 3),
     O('tile:lampara', 4, 5), O('tile:lampara', 12, 8), O('tile:lampara', 5, 12)],
    [(7, 6, 1.1), (13, 4, 1.0), (15, 9, .8), (4, 12, .8), (17, 3, .7), (3, 4, .8)], (10, 22, 18), 135, .05)

# 25 Camara de sangrado -------------------------------------------------------------
GAPS = {5: (4, 11, 16), 8: (2, 8, 14), 11: (5, 10, 17)}
p25 = []; rr = random.Random(25)
for y, gaps in GAPS.items():
    for x in range(2, 18):
        if x in gaps: continue
        p25.append(P('carcass%d' % rr.randint(0, 2), x, y, dx=rr.choice([-1, 0, 1]), dy=-rr.choice([2, 4, 6])))
        p25.append(O('tile:rail' if rr.random() < .6 else 'tile:rail_gancho', x, y - 2, dy=20))
    for x in gaps: p25.append(O('tile:rail_gancho', x, y - 2, dy=20))
    p25 += [O('tile:rail', 1, y - 2, dy=20), O('tile:rail', 18, y - 2, dy=20)]
p25 += [D('blood', x, y, dx=rr.randint(-6, 8), dy=rr.randint(-6, 4)) for x, y in [(3, 4), (7, 3), (12, 4), (16, 3), (2, 7), (6, 6), (10, 7), (15, 6), (17, 7), (4, 9), (9, 10), (13, 9), (16, 10), (3, 12), (8, 13), (12, 12), (15, 13)]]
p25 += [D('bloodtrail', 4, 5, dy=10), D('bloodtrail', 11, 5, dy=8), D('bloodtrail', 8, 8, dy=8), D('bloodtrail', 14, 8, dy=10), D('bloodtrail', 10, 11, dy=8), D('drag', 12, 13, dy=-4), D('drag', 5, 10, dx=8),
        D('drag', 14, 4, dy=-2), D('puddle', 1, 6, dx=4), D('puddle', 17, 9, dx=-8), P('barrel', 1, 3, dx=4), P('barrel', 18, 13, dx=4), P('cart', 18, 6, dx=-6), P('bucket', 1, 9, dx=6), P('bucket', 18, 10, dx=4),
        P('cart', 1, 12, dx=-2), P('crate', 18, 4), D('hooks', 9, 2, dy=-6), D('thermo', 14, 2, dx=12, dy=-8), D('plaque', 6, 2, dx=6, dy=-10), D('hooks', 16, 2, dx=-4, dy=-6), D('chain', 3, 2, dx=14, dy=-4),
        D('meat', 6, 13, dx=4, dy=-2), D('meat', 13, 7, dx=6), D('meat', 2, 10, dx=10, dy=-4), D('hoofs', 16, 12, dx=-6)]
mapa(25, [
    '####################', 'FFFFFFFFFFFFFFFFFFFF', 'ffffffffffffffffffff', '#::::::::::::::::::#', '#::::::::::::::::::#',
    '#g~~~~~~~~~~~~~~~~:#', '#::::::::::::::::::#', '#::::::::::::::::::#', '#:~~~~~~~~~~~~~~~~g#', '#::::::::::::::::::#',
    '#::::::::::::::::::#', '#g~~~~~~~~~~~~~~~~:#', '#::::::::::::::::::#', '#::::::::::::::::::#', '#################:##'],
    F('puerta_metal', (2, 2)) + F('tuberia', (5, 2), (15, 2)) + F('rejilla_pared', (12, 2)) + F('manguera', (18, 3)) + F('mancha', (5, 6), (11, 9), (14, 12), (8, 4), (16, 7)),
    p25, [(3, 4, .8), (15, 4, .8), (9, 7, .8), (4, 10, .8), (15, 12, .9), (2, 3, .6)], (6, 16, 26), 160)

# 26 Oficina alta -------------------------------------------------------------------
mapa(26, [
    '####################', 'MMMMMMMMMMMMMMMMMMMM', 'mmmmmmmmmmmmmmmmmmmm', '#oooooo#ooooooooooo#', '#oooooo#ooooooooooo#',
    '#oooooo#ooooooooooo#', '#oooooooooooooooooo#', '#oooooo#ooooooooooo#', '#oooooo#ooooooooooo#', '###o####ooooooooooo#',
    '#,,,,,,#############', '#,,,,,,hhhhhhhhhhhh#', '#,,,,,,,,,,,,,,,,,,,', '###,################', '###,################'],
    F('escritorio_izq', (12, 5)) + F('escritorio_der', (13, 5)) + F('ventana_oficina', (10, 2), (15, 2)) + F('reloj_pared', (3, 2)) + F('archivador_bajo', (18, 4), (18, 5))
    + F('persiana_baja', (5, 2)) + F('tuberia', (9, 11), (14, 11)) + F('rejilla_pared', (17, 11)) + F('silla', (10, 6)) + F('mancha', (9, 5), (15, 7), (4, 11)) + F('huellas', (11, 8), (8, 6), (5, 12), (10, 12)),
    [P('archive', 1, 3, dx=-1), P('archive', 5, 3, dx=-6, dy=0), P('bench', 5, 5, dx=-4), P('crate', 1, 5), P('crates2', 1, 6, dx=2), P('radiotable', 1, 8, dx=2), P('coatrack', 4, 3, dx=-10),
     P('crate', 6, 8, dx=-2), D('papers', 3, 5), D('papers', 4, 7, dx=6), D('papers', 2, 4, dx=10, dy=4), D('note', 5, 5, dx=6, dy=-16),
     P('archive', 16, 3), P('safe', 18, 9, dx=2), P('sofa', 9, 9, dx=-2), P('coatrack', 8, 3, dx=4), P('plant', 8, 9, dx=8), P('crate', 18, 7, dx=-2), P('crates2', 17, 9, dx=-6), P('rack', 14, 9), P('crate', 11, 3, dx=2), D('stool', 13, 8, dx=8), D('papers', 12, 9), D('bottles', 16, 9, dx=-12, dy=-2),
     D('rug', 11, 7, dx=-8, dy=6), D('deskset', 12, 5, dx=2, dy=-12), D('skull', 12, 2, dx=4, dy=-8), D('skull', 13, 2, dx=6, dy=-6), D('skull', 8, 2, dx=6, dy=-8), D('prods', 17, 2, dx=-6, dy=-6),
     D('board', 13, 2, dx=38, dy=-6), D('calendar', 9, 2, dx=10, dy=-8), D('bottles', 14, 5, dx=6, dy=-6), D('papers', 14, 6, dx=4), D('papers', 10, 4), D('papers', 16, 6, dx=-6), D('blood', 9, 6, dx=-10),
     D('bloodtrail', 8, 6, dx=-20, dy=-6), D('cap', 11, 8, dx=8, dy=-8), D('bottles', 9, 9, dx=40, dy=-2), D('cable', 15, 8, dy=-2), D('keyboard', 17, 2, dx=34, dy=-6),
     P('crates2', 1, 10, dx=2), P('barrel', 1, 12, dx=4), P('sacks', 5, 10, dx=2), P('bucket', 6, 10, dx=10, dy=-2, block=False), D('railing', 4, 13, dy=-12), D('railing', 5, 13, dy=-12), D('railing', 2, 13, dx=-2, dy=-12),
     D('fusebox', 11, 11, dx=6, dy=-4), D('plaque', 12, 11, dx=20, dy=-10), D('puddle', 8, 12, dx=6, dy=-4), D('blood', 6, 12, dx=-2, dy=-4), D('bloodtrail', 3, 11, dx=6, dy=4), D('hoofs', 13, 12, dy=-4),
     D('papers', 16, 12, dx=4), D('straw', 2, 11), D('cable', 3, 10, dx=10, dy=-10),
     O('tile:lampara', 3, 5), O('tile:lampara', 13, 6)],
    [(3, 5, .9), (12, 5, 1.1), (16, 8, .7), (3, 11, .8), (13, 12, .7), (1, 8, .5)], (30, 20, 6), 140)

# 27 Patio del alba -----------------------------------------------------------------
mapa(27, [
    '####################', 'LLLLLLLLLLLLLLLLLLLL', 'llllllllllllllllllll', 'cccccccccccccccccccc', 'aaaaaaaaaaaaaaaaaaaa',
    'aaaaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaa',
    'aaabbbaaaaaaabbbbaaa', 'bbbbbbbaaaabbbbbbbbb', 'bbbbbbbbaabbbbbbbbbb', 'aaaaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaa'],
    F('puerta_metal', (3, 2)) + F('ventana_nave', (7, 2), (11, 2), (15, 2)) + F('tuberia', (9, 2), (18, 2)) + F('cartel', (5, 2)) + F('alambrada', *span(13, 0, 8), *span(13, 11, 19))
    + F('huellas', (9, 9), (10, 11), (8, 7), (11, 6), (9, 12), (4, 5), (6, 8)) + F('mancha', (12, 9), (5, 6), (14, 7)),
    [P('truck', 14, 6, dx=2), P('ramp', 13, 6, dx=6, dy=4, block=False), P('truck', 0, 7, flip=True), P('crates2', 0, 3), P('crate', 1, 3, dx=3), P('barrel', 17, 3, dx=3), P('barrel', 18, 3, dx=2, dy=-4),
     P('dumpster', 12, 3, dx=2), P('pallet', 9, 3, dy=-4, block=False), P('sacks', 9, 3, dx=2, dy=-10), P('farol', 6, 4, dx=7), P('farol', 19, 9, dx=4), P('barrel', 0, 12, dx=4), P('crate', 1, 12),
     P('crate', 18, 12), P('sacks', 19, 12, dx=-2), P('cone', 8, 12, dx=20, dy=-4, block=False), P('cone', 11, 12, dx=-6, dy=-6, block=False), P('bench', 15, 3, dx=2), P('pallet', 5, 10, dy=-6, block=False),
     D('tracks', 3, 9, dy=-2), D('tracks', 10, 5, dx=6), D('tracks', 6, 12, dx=-10, dy=-8), D('puddle', 4, 11, dx=4), D('puddle', 15, 11), D('puddle', 8, 5, dx=-6), D('oil', 16, 8, dx=6), D('oil', 2, 9, dy=6),
     D('blood', 14, 10, dx=4), D('blood', 15, 10, dx=-6, dy=4), D('blood', 9, 6, dx=4), D('bloodtrail', 4, 4, dx=6), D('bloodtrail', 5, 6, dx=10, dy=6), D('hoofs', 6, 6), D('hoofs', 9, 10, dx=8),
     D('hoofs', 12, 8, dx=-4), D('hoofs', 3, 6, dx=10, dy=8), D('drag', 13, 10, dx=-10, dy=-8), D('cap', 14, 10, dx=18, dy=-6), D('straw', 12, 7), D('straw', 16, 9), D('straw', 3, 10), D('straw', 7, 9, dx=10),
     D('papers', 10, 4, dx=6), D('papers', 2, 5), D('plaque', 13, 2, dx=6, dy=-10), D('chain', 8, 13, dx=20, dy=-4), D('chain', 11, 13, dx=-6, dy=-4), D('cable', 16, 4, dx=6), D('dung', 8, 8, dx=6), D('dung', 12, 11, dx=4)],
    [(3, 3, 1.0), (6, 4, 1.1), (10, 9, 1.4), (17, 9, 1.0)], (26, 16, 10), 95)

# ---------------------------------------------------------------- composicion
def build():
    ops = []; added = []; index = {}; info = {}
    ntiles_base = 64
    def new_tile(im, passage, prio):
        key = (im.tobytes(), passage, prio)
        if key not in index:
            index[key] = 384 + ntiles_base + len(added); added.append((im, passage, prio))
        return index[key]
    for mid, m in M.items():
        r = random.Random(500 + mid); W, H = 20, 15
        z = [[[0] * W for _ in range(H)] for _ in range(3)]; walls = []; canal = []; blocked = set()
        for y, row in enumerate(m['rows']):
            for x, c in enumerate(row):
                if c == '#': walls.append([x, y]); blocked.add((x, y))
                elif c == '~': canal.append([x, y])
                else:
                    t = FLOOR[c]
                    if isinstance(t, tuple):
                        name = t[1] if r.random() < t[2] else t[0]
                        if c == '.' and r.random() < m['blood']: name = r.choice(['azulejo_sangre', 'azulejo_arrastre'])
                    else: name = t
                    z[0][y][x] = ID[name]
                    if name in BLOCKED: blocked.add((x, y))
        for x, y, name in m['furn']:
            z[1][y][x] = ID[name]
            if name in BLOCKED: blocked.add((x, y))
        floor = Image.new('RGBA', (W * 32, H * 32)); obj = Image.new('RGBA', (W * 32, H * 32)); over = Image.new('RGBA', (W * 32, H * 32))
        pblock = set(); ptop = set()
        for n, (typ, kind, x, y, dx, dy, block, flip) in enumerate(m['props']):
            im = draw(kind, random.Random(mid * 1000 + n))
            if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
            px = x * 32 + dx + (max(0, (32 - im.width) // 2) if im.width < 32 else 0); py = y * 32 + 32 - im.height + dy
            if typ == 'O': px, py = x * 32 + dx, y * 32 + dy
            px = max(0, min(W * 32 - im.width, px)); py = max(0, min(H * 32 - im.height, py))
            (floor if typ == 'D' else over if typ == 'O' else obj).alpha_composite(im, (px, py))
            if typ == 'P':
                cx1, cx2 = px // 32, (px + im.width - 1) // 32
                for cy in range(py // 32, (py + im.height - 1) // 32 + 1):
                    for cx in range(cx1, cx2 + 1):
                        if cy == y and block:
                            # solo cuenta como huella si la pieza ocupa de verdad la celda
                            cell = im.crop((max(0, cx * 32 - px), 0, min(im.width, cx * 32 + 32 - px), im.height))
                            if cell.getbbox() and (cell.getbbox()[2] - cell.getbbox()[0]) >= 9: pblock.add((cx, cy))
                        elif cy < y: ptop.add((cx, cy))
        for y in range(H):
            for x in range(W):
                box = (x * 32, y * 32, x * 32 + 32, y * 32 + 32)
                a, b, c = floor.crop(box), obj.crop(box), over.crop(box)
                if not (a.getbbox() or b.getbbox() or c.getbbox()): continue
                im = Image.new('RGBA', (32, 32)); im.alpha_composite(a); im.alpha_composite(b); im.alpha_composite(c)
                blk = (x, y) in pblock or (x, y) in blocked
                prio = 0 if (x, y) in pblock else 2 if c.getbbox() else 1 if ((x, y) in ptop and b.getbbox()) else 0
                if blk: blocked.add((x, y))
                z[2][y][x] = new_tile(im, 15 if blk else 0, prio)
        for l in range(3): ops.append(['set_map_tiles', dict(mapId=mid, layer=l, x=0, y=0, grid=z[l])])
        if walls: ops.append(['apply_autotile', dict(mapId=mid, layer=0, autotileSlot=0, cells=walls)])
        if canal: ops.append(['apply_autotile', dict(mapId=mid, layer=0, autotileSlot=1, cells=canal)])
        info[mid] = dict(blocked=sorted(blocked))
        # mascara de luz nocturna anclada al mapa
        mask = Image.new('RGBA', (W * 32, H * 32)); pix = mask.load(); tr, tg, tb = m['tint']
        for py in range(H * 32):
            for px in range(W * 32):
                glow = max(math.exp(-(((px - (lx * 32 + 16)) / (64 * s)) ** 2 + ((py - (ly * 32 + 18)) / (58 * s)) ** 2) / 2) for lx, ly, s in m['lights'])
                edge = min(px, py, W * 32 - 1 - px, H * 32 - 1 - py)
                a = int(m['dark'] + max(0, 28 - edge) * 1.1 - (m['dark'] - 8) * min(1, glow * 1.15))
                pix[px, py] = (tr // 3, tg // 3, tb // 3, max(0, min(190, a)))
        mask.save(ROOT / 'Graphics/Pictures' / ('acto5_luz%02d.png' % mid))
    rows = math.ceil(len(added) / 8)
    sheet = Image.new('RGBA', (256, 256 + rows * 32)); sheet.alpha_composite(TS)
    for n, (im, p, pr) in enumerate(added): sheet.alpha_composite(im, (n % 8 * 32, 256 + n // 8 * 32))
    sheet.save(ROOT / 'Graphics/Tilesets/acto5_matanza.png')
    snap = json.loads(((_ROOT / 'diseno/verificaciones/inventario/snapshot.json')).read_text(encoding='utf-8'))
    t = snap['Tilesets'][51]; up = {}
    for key in ['passages', 'priorities', 'terrain_tags']:
        vals = t[key]['data'][:448] + [p if key == 'passages' else pr if key == 'priorities' else 0 for _, p, pr in added]
        up[key] = {'_class': 'Table', 'dim': 1, 'xsize': len(vals), 'ysize': 1, 'zsize': 1, 'data': vals}
    ops.insert(0, ['update_database_entry', dict(kind='tilesets', id=69, updates=up)])
    ((_ROOT / 'diseno/archivo/lotes/b_tiles5.json')).write_text(json.dumps(ops), encoding='utf-8')
    ((_ROOT / 'diseno/herramientas/actos/acto5/maps5_info.json')).write_text(json.dumps(info), encoding='utf-8')
    print(len(added), 'baldosas nuevas;', len(ops), 'operaciones')

if __name__ == '__main__':
    if (ROOT/'diseno/fuentes/arte_hd2d/arte_final/manifest.json').exists():
        raise SystemExit('Constructor PIL historico desactivado. Usar componer_arte_final.py y aplicar_arte_final.mjs.')
    build()
