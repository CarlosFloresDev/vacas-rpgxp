# Graficos del Acto II (matadero): tileset propio, autotile del canal de
# desague, personajes derivados del RTP y hoja de objetos dibujada a mano.
# Ejecutar: python gfx_acto2.py
from PIL import Image, ImageDraw, ImageEnhance
import random

PROJ = "D:/descargas/Proyectos personales/Vacas/Graphics/"
RTP = "D:/SteamLibrary/steamapps/common/RPGXP/rtp/Graphics/"

# ------------------------------------------------------------------ paleta
TILE = (196, 198, 190); TILE_L = (214, 216, 208); GROUT = (150, 152, 146)
TILE_D = (170, 170, 160)
BLOOD = (112, 20, 18); BLOOD_D = (70, 10, 10); BLOOD_L = (150, 36, 30)
CONC = (118, 116, 110); CONC_D = (92, 90, 86); CONC_L = (136, 134, 128)
STEEL = (150, 156, 162); STEEL_L = (190, 196, 200); STEEL_D = (78, 84, 92)
COLD = (172, 188, 198); COLD_L = (205, 218, 226); COLD_D = (120, 138, 150)
BRICK = (108, 70, 60); BRICK_D = (74, 48, 42); MORTAR = (130, 118, 108)
ASPH = (58, 58, 62); ASPH_L = (74, 74, 78)
STRAW = (150, 128, 78); STRAW_D = (112, 94, 56); MUD = (84, 70, 52)
WOOD = (92, 68, 46); WOOD_D = (62, 44, 30); WOOD_L = (120, 92, 64)
LINO = (110, 112, 92); LINO_D = (92, 94, 76)
OUTL = (24, 22, 22)
BLACK = (14, 14, 16)

def rgba(c, a=255):
    return tuple(c[:3]) + (a,)

COLS = 8
TILES = []          # (nombre, funcion, pasable, prioridad, bush)
def tile(name, passable=True, prio=0, bush=False):
    def deco(fn):
        TILES.append((name, fn, passable, prio, bush))
        return fn
    return deco

def new():
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)

def noise(d, color, n, r, spread=10, box=(0, 0, 31, 31)):
    for _ in range(n):
        x = r.randint(box[0], box[2]); y = r.randint(box[1], box[3])
        k = r.randint(-spread, spread)
        d.point((x, y), fill=rgba(tuple(max(0, min(255, c + k)) for c in color)))

def tiled_floor(d, base, grout, r, size=16, dirt=0):
    d.rectangle([0, 0, 31, 31], fill=rgba(base))
    for i in range(0, 32, size):
        d.line([(i, 0), (i, 31)], fill=rgba(grout))
        d.line([(0, i), (31, i)], fill=rgba(grout))
    noise(d, base, 40 + dirt, r, 8)

def splat(d, r, cx, cy, rad, col=BLOOD, drops=6):
    d.ellipse([cx - rad, cy - rad * 0.7, cx + rad, cy + rad * 0.7], fill=rgba(col))
    for _ in range(drops):
        a = r.uniform(0, 6.28); dist = rad + r.randint(1, 6)
        import math
        x = cx + math.cos(a) * dist; y = cy + math.sin(a) * dist * 0.8
        s = r.randint(1, 2)
        d.ellipse([x - s, y - s, x + s, y + s], fill=rgba(col))

# ===================================================== fila 0: suelos
@tile("azulejo")
def _(d, r): tiled_floor(d, TILE, GROUT, r)
@tile("azulejo_sucio")
def _(d, r):
    tiled_floor(d, TILE_D, GROUT, r, dirt=30)
    for _ in range(5):
        x, y = r.randint(2, 29), r.randint(2, 29)
        d.point((x, y), fill=rgba(BLOOD_D))
@tile("azulejo_sangre")
def _(d, r):
    tiled_floor(d, TILE_D, GROUT, r)
    splat(d, r, 16, 17, 6)
    d.ellipse([12, 14, 16, 17], fill=rgba(BLOOD_L))
@tile("azulejo_arrastre")
def _(d, r):
    tiled_floor(d, TILE_D, GROUT, r)
    for i in range(4):
        y = 10 + i * 4 + r.randint(-1, 1)
        d.line([(0, y), (31, y + r.randint(-2, 2))], fill=rgba(BLOOD if i % 2 else BLOOD_D), width=2)
@tile("hormigon")
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(CONC)); noise(d, CONC, 120, r, 12)
@tile("hormigon_mojado")
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(CONC)); noise(d, CONC, 100, r, 12)
    d.ellipse([4, 8, 26, 24], fill=rgba(CONC_D)); d.ellipse([9, 12, 18, 18], fill=rgba((80, 60, 58)))
    d.line([(10, 13), (15, 13)], fill=rgba(CONC_L))
@tile("rejilla_suelo")
def _(d, r):
    tiled_floor(d, TILE_D, GROUT, r)
    d.ellipse([7, 7, 24, 24], fill=rgba(STEEL_D), outline=rgba(OUTL))
    for x in range(10, 23, 3):
        d.line([(x, 9), (x, 22)], fill=rgba(BLACK))
    d.arc([5, 5, 26, 26], 200, 340, fill=rgba(BLOOD_D), width=2)
@tile("paja", bush=True)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(MUD)); noise(d, MUD, 60, r, 10)
    for _ in range(46):
        x, y = r.randint(0, 31), r.randint(0, 31)
        d.line([(x, y), (x + r.randint(-4, 4), y + r.randint(-2, 2))], fill=rgba(STRAW if r.random() < .6 else STRAW_D))

# ===================================================== fila 1: paredes
def wall_tiles(d, r, base, grout, upper, stain=False):
    d.rectangle([0, 0, 31, 31], fill=rgba(base))
    for y in range(0, 32, 8):
        d.line([(0, y), (31, y)], fill=rgba(grout))
    for x in range(0, 32, 8):
        d.line([(x, 0), (x, 31)], fill=rgba(grout))
    noise(d, base, 30, r, 6)
    if upper:
        d.line([(0, 0), (31, 0)], fill=rgba(OUTL))
    else:
        d.rectangle([0, 28, 31, 31], fill=rgba(tuple(int(c * 0.6) for c in base)))
        if stain:
            for _ in range(3):
                x = r.randint(2, 28); h = r.randint(6, 18)
                d.line([(x, 28 - h), (x, 28)], fill=rgba(BLOOD_D))
                d.point((x, 28 - h - 1), fill=rgba(BLOOD))
@tile("pared_azulejo_alta", False)
def _(d, r): wall_tiles(d, r, TILE_L, GROUT, True)
@tile("pared_azulejo_baja", False)
def _(d, r): wall_tiles(d, r, TILE, GROUT, False, True)
@tile("pared_hormigon_alta", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(CONC_L)); noise(d, CONC_L, 90, r, 10)
    d.line([(0, 15), (31, 15)], fill=rgba(CONC_D)); d.line([(0, 0), (31, 0)], fill=rgba(OUTL))
@tile("pared_hormigon_baja", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(CONC)); noise(d, CONC, 90, r, 10)
    d.rectangle([0, 26, 31, 31], fill=rgba(CONC_D))
    x = r.randint(4, 26); d.line([(x, 4), (x + 3, 26)], fill=rgba((70, 80, 60)))
@tile("pared_fria_alta", False)
def _(d, r):
    wall_tiles(d, r, COLD_L, COLD_D, True)
    for _ in range(14):
        x, y = r.randint(0, 31), r.randint(0, 6)
        d.point((x, y), fill=rgba((240, 248, 255)))
@tile("pared_fria_baja", False)
def _(d, r):
    wall_tiles(d, r, COLD, COLD_D, False)
    for x in range(1, 31, 4):
        h = r.randint(2, 6); d.line([(x, 0), (x, h)], fill=rgba((235, 245, 250)))
@tile("pared_madera_alta", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(WOOD))
    for x in range(0, 32, 8):
        d.line([(x, 0), (x, 31)], fill=rgba(WOOD_D))
    noise(d, WOOD, 40, r, 8); d.line([(0, 0), (31, 0)], fill=rgba(OUTL))
@tile("pared_madera_baja", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(WOOD))
    for x in range(0, 32, 8):
        d.line([(x, 0), (x, 31)], fill=rgba(WOOD_D))
    d.rectangle([0, 24, 31, 31], fill=rgba(WOOD_D)); d.line([(0, 23), (31, 23)], fill=rgba(WOOD_L))
    noise(d, WOOD, 40, r, 8)

# ===================================================== fila 2: exterior y suelos 2
@tile("ladrillo_alto", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(MORTAR))
    for row in range(4):
        off = 0 if row % 2 == 0 else 8
        for x in range(-16, 32, 16):
            d.rectangle([x + off + 1, row * 8 + 1, x + off + 14, row * 8 + 6], fill=rgba(BRICK if r.random() < .8 else BRICK_D))
    d.line([(0, 0), (31, 0)], fill=rgba(OUTL))
@tile("ladrillo_bajo", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(MORTAR))
    for row in range(4):
        off = 0 if row % 2 == 0 else 8
        for x in range(-16, 32, 16):
            d.rectangle([x + off + 1, row * 8 + 1, x + off + 14, row * 8 + 6], fill=rgba(BRICK_D if r.random() < .6 else BRICK))
    d.rectangle([0, 27, 31, 31], fill=rgba((50, 40, 36)))
@tile("asfalto")
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(ASPH)); noise(d, ASPH, 140, r, 14)
@tile("asfalto_charco")
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(ASPH)); noise(d, ASPH, 100, r, 14)
    d.ellipse([3, 9, 28, 24], fill=rgba((44, 48, 56))); d.ellipse([6, 12, 22, 20], fill=rgba((60, 30, 32)))
    d.line([(9, 14), (16, 14)], fill=rgba((110, 110, 120)))
@tile("acera")
def _(d, r):
    tiled_floor(d, (128, 126, 120), (96, 94, 90), r, 16)
@tile("barro", bush=True)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(MUD)); noise(d, MUD, 140, r, 14)
    for _ in range(3):
        x, y = r.randint(4, 26), r.randint(4, 26)
        d.ellipse([x - 3, y - 2, x + 3, y + 2], outline=rgba((60, 50, 38)))
@tile("linoleo")
def _(d, r):
    tiled_floor(d, LINO, LINO_D, r, 8); d.line([(3, 27), (12, 24)], fill=rgba((80, 60, 50)))
@tile("suelo_frio")
def _(d, r):
    tiled_floor(d, COLD, COLD_D, r, 16)
    for _ in range(12):
        x, y = r.randint(0, 31), r.randint(0, 31); d.point((x, y), fill=rgba((235, 245, 250)))

# ===================================================== fila 3: corrales y vestuario
def rails_h(d, y0=8):
    for y in (y0, y0 + 10):
        d.rectangle([0, y, 31, y + 2], fill=rgba(STEEL)); d.line([(0, y), (31, y)], fill=rgba(STEEL_L))
        d.line([(0, y + 3), (31, y + 3)], fill=rgba(OUTL))
@tile("valla_h", False)
def _(d, r):
    rails_h(d)
    d.rectangle([14, 4, 17, 30], fill=rgba(STEEL_D), outline=rgba(OUTL))
@tile("valla_v", False)
def _(d, r):
    for x in (9, 20):
        d.rectangle([x, 0, x + 2, 31], fill=rgba(STEEL)); d.line([(x, 0), (x, 31)], fill=rgba(STEEL_L))
        d.line([(x + 3, 0), (x + 3, 31)], fill=rgba(OUTL))
@tile("valla_poste", False)
def _(d, r):
    rails_h(d)
    d.rectangle([11, 2, 20, 30], fill=rgba(STEEL_D), outline=rgba(OUTL)); d.line([(12, 3), (12, 28)], fill=rgba(STEEL))
@tile("puerta_corral", False)
def _(d, r):
    rails_h(d, 6); rails_h(d, 12)
    d.line([(2, 6), (29, 26)], fill=rgba(STEEL_D), width=2)
    d.rectangle([28, 4, 31, 30], fill=rgba(STEEL_D))
    d.rectangle([2, 15, 6, 19], fill=rgba(BLOOD_D))
@tile("taquilla_alta", False, 1)
def _(d, r):
    d.rectangle([2, 4, 29, 31], fill=rgba((96, 108, 104)), outline=rgba(OUTL))
    d.line([(15, 4), (15, 31)], fill=rgba(OUTL))
    for x in (5, 18):
        for y in (8, 11, 14):
            d.line([(x, y), (x + 8, y)], fill=rgba((60, 70, 68)))
    d.line([(3, 5), (28, 5)], fill=rgba((130, 140, 136)))
@tile("taquilla_baja", False)
def _(d, r):
    d.rectangle([2, 0, 29, 29], fill=rgba((96, 108, 104)), outline=rgba(OUTL))
    d.line([(15, 0), (15, 29)], fill=rgba(OUTL))
    d.rectangle([11, 4, 13, 9], fill=rgba(STEEL_L)); d.rectangle([17, 4, 19, 9], fill=rgba(STEEL_L))
    d.rectangle([2, 29, 29, 31], fill=rgba((40, 40, 40)))
    d.point((24, 22), fill=rgba(BLOOD))
@tile("banco", False)
def _(d, r):
    d.rectangle([0, 12, 31, 18], fill=rgba(WOOD_L), outline=rgba(OUTL))
    d.line([(1, 13), (30, 13)], fill=rgba((150, 118, 84)))
    d.rectangle([3, 19, 5, 27], fill=rgba(STEEL_D)); d.rectangle([26, 19, 28, 27], fill=rgba(STEEL_D))
@tile("reloj_pared", False)
def _(d, r):
    wall_tiles(d, r, TILE, GROUT, False, False)
    d.ellipse([7, 3, 25, 21], fill=rgba((230, 228, 216)), outline=rgba(OUTL))
    d.line([(16, 12), (16, 6)], fill=rgba(OUTL)); d.line([(16, 12), (21, 14)], fill=rgba(OUTL))

# ===================================================== fila 4: cadena
@tile("cinta", False)
def _(d, r):
    d.rectangle([0, 6, 31, 25], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.rectangle([0, 9, 31, 22], fill=rgba((52, 52, 54)))
    for x in range(2, 32, 6):
        d.line([(x, 9), (x, 22)], fill=rgba((76, 76, 78)))
    d.line([(0, 26), (31, 26)], fill=rgba(BLACK)); d.point((9, 15), fill=rgba(BLOOD))
@tile("cinta_ini", False)
def _(d, r):
    d.rectangle([4, 6, 31, 25], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.ellipse([0, 6, 10, 25], fill=rgba(STEEL), outline=rgba(OUTL))
    d.rectangle([8, 9, 31, 22], fill=rgba((52, 52, 54)))
@tile("cinta_fin", False)
def _(d, r):
    d.rectangle([0, 6, 27, 25], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.ellipse([21, 6, 31, 25], fill=rgba(STEEL), outline=rgba(OUTL))
    d.rectangle([0, 9, 23, 22], fill=rgba((52, 52, 54)))
    d.ellipse([12, 12, 20, 19], fill=rgba(BLOOD_D))
@tile("mesa_acero", False)
def _(d, r):
    d.rectangle([1, 5, 30, 22], fill=rgba(STEEL), outline=rgba(OUTL))
    d.line([(2, 6), (29, 6)], fill=rgba(STEEL_L))
    d.rectangle([3, 23, 5, 30], fill=rgba(STEEL_D)); d.rectangle([26, 23, 28, 30], fill=rgba(STEEL_D))
    splat(d, r, 12, 14, 3, BLOOD, 3)
@tile("rail", True, 2)
def _(d, r):
    d.rectangle([0, 2, 31, 6], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.line([(0, 3), (31, 3)], fill=rgba(STEEL))
@tile("rail_gancho", True, 2)
def _(d, r):
    d.rectangle([0, 2, 31, 6], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.line([(0, 3), (31, 3)], fill=rgba(STEEL))
    d.line([(16, 7), (16, 17)], fill=rgba(STEEL_L))
    d.arc([10, 14, 22, 26], 300, 210, fill=rgba(STEEL_L), width=2)
    d.point((11, 18), fill=rgba(STEEL_L))
@tile("escritorio_izq", False)
def _(d, r):
    d.rectangle([2, 6, 31, 22], fill=rgba(WOOD), outline=rgba(OUTL)); d.line([(3, 7), (31, 7)], fill=rgba(WOOD_L))
    d.rectangle([4, 23, 14, 30], fill=rgba(WOOD_D), outline=rgba(OUTL))
    d.rectangle([7, 9, 18, 16], fill=rgba((206, 200, 180)))
    for y in (11, 13): d.line([(8, y), (17, y)], fill=rgba((90, 90, 90)))
@tile("escritorio_der", False)
def _(d, r):
    d.rectangle([0, 6, 29, 22], fill=rgba(WOOD), outline=rgba(OUTL)); d.line([(0, 7), (28, 7)], fill=rgba(WOOD_L))
    d.rectangle([17, 23, 27, 30], fill=rgba(WOOD_D), outline=rgba(OUTL))
    d.rectangle([14, 8, 22, 15], fill=rgba((40, 40, 40)), outline=rgba(OUTL))  # telefono
    d.ellipse([4, 10, 10, 15], fill=rgba((200, 196, 186)))  # taza
    d.ellipse([5, 11, 9, 13], fill=rgba((80, 50, 30)))

# ===================================================== fila 5: oficina y mantenimiento
@tile("archivador_alto", False, 1)
def _(d, r):
    d.rectangle([4, 6, 27, 31], fill=rgba((112, 116, 108)), outline=rgba(OUTL))
    d.line([(5, 7), (26, 7)], fill=rgba((150, 154, 146)))
    d.rectangle([8, 12, 23, 24], outline=rgba(OUTL)); d.rectangle([13, 16, 18, 18], fill=rgba(STEEL_L))
@tile("archivador_bajo", False)
def _(d, r):
    d.rectangle([4, 0, 27, 29], fill=rgba((112, 116, 108)), outline=rgba(OUTL))
    d.rectangle([8, 4, 23, 14], outline=rgba(OUTL)); d.rectangle([13, 8, 18, 10], fill=rgba(STEEL_L))
    d.rectangle([8, 17, 23, 26], outline=rgba(OUTL)); d.rectangle([13, 20, 18, 22], fill=rgba(STEEL_L))
    d.rectangle([4, 29, 27, 31], fill=rgba((40, 40, 40)))
@tile("puerta_metal", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(TILE))
    d.rectangle([3, 0, 28, 31], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.rectangle([7, 4, 24, 12], fill=rgba((40, 50, 54)), outline=rgba(OUTL))
    d.rectangle([22, 16, 25, 19], fill=rgba(STEEL_L))
    d.line([(4, 30), (27, 30)], fill=rgba(BLOOD_D))
@tile("rejilla_pared", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(CONC)); noise(d, CONC, 70, r, 10)
    d.rectangle([5, 6, 26, 24], fill=rgba(STEEL_D), outline=rgba(OUTL))
    for y in range(9, 23, 3):
        d.line([(7, y), (24, y)], fill=rgba(BLACK))
@tile("tuberia", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(CONC)); noise(d, CONC, 70, r, 10)
    d.rectangle([11, 0, 20, 31], fill=rgba((88, 94, 84)), outline=rgba(OUTL))
    d.line([(13, 0), (13, 31)], fill=rgba((120, 126, 112)))
    d.rectangle([9, 12, 22, 16], fill=rgba((70, 74, 66)), outline=rgba(OUTL))
    d.line([(16, 17), (16, 24)], fill=rgba((60, 80, 70)))
@tile("cajas", False)
def _(d, r):
    d.rectangle([2, 10, 29, 30], fill=rgba((130, 110, 80)), outline=rgba(OUTL))
    d.line([(2, 20), (29, 20)], fill=rgba(OUTL)); d.line([(15, 10), (15, 30)], fill=rgba(OUTL))
    d.rectangle([6, 2, 25, 10], fill=rgba((150, 128, 92)), outline=rgba(OUTL))
    d.rectangle([5, 23, 12, 27], fill=rgba(BLOOD_D))
@tile("cubo_despojos", False)
def _(d, r):
    d.polygon([(6, 8), (26, 8), (24, 29), (8, 29)], fill=rgba((100, 104, 108)), outline=rgba(OUTL))
    d.ellipse([6, 5, 26, 12], fill=rgba(BLOOD_D), outline=rgba(OUTL))
    d.ellipse([10, 6, 16, 10], fill=rgba(BLOOD_L)); d.ellipse([17, 7, 22, 10], fill=rgba((150, 110, 110)))
    d.line([(9, 12), (9, 20)], fill=rgba(BLOOD))
@tile("manguera", False)
def _(d, r):
    wall_tiles(d, r, TILE, GROUT, False, False)
    d.ellipse([6, 4, 26, 24], fill=rgba((40, 80, 54)), outline=rgba(OUTL))
    d.ellipse([11, 9, 21, 19], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.line([(8, 20), (6, 30)], fill=rgba((40, 80, 54)), width=3)

# ===================================================== fila 6: varios
@tile("ventana_nave", False)
def _(d, r):
    wall_tiles(d, r, TILE_L, GROUT, True)
    d.rectangle([4, 6, 27, 27], fill=rgba((70, 80, 84)), outline=rgba(OUTL))
    d.line([(16, 6), (16, 27)], fill=rgba(OUTL)); d.line([(4, 16), (27, 16)], fill=rgba(OUTL))
    d.line([(6, 8), (12, 8)], fill=rgba((150, 160, 160)))
@tile("cajon_aturdir", False, 1)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(STEEL_D))
    d.rectangle([2, 2, 29, 29], fill=rgba((60, 64, 68)), outline=rgba(OUTL))
    for x in range(4, 30, 5): d.line([(x, 2), (x, 29)], fill=rgba(STEEL))
    d.rectangle([2, 24, 29, 29], fill=rgba(BLOOD_D))
@tile("cuchillos", False)
def _(d, r):
    wall_tiles(d, r, TILE, GROUT, False, True)
    d.rectangle([3, 6, 28, 9], fill=rgba(WOOD), outline=rgba(OUTL))
    for i, x in enumerate(range(6, 28, 5)):
        L = 10 + (i % 3) * 3
        d.rectangle([x, 10, x + 1, 10 + L], fill=rgba(STEEL_L)); d.rectangle([x, 4, x + 1, 9], fill=rgba(OUTL))
@tile("fregadero", False)
def _(d, r):
    d.rectangle([2, 6, 29, 24], fill=rgba(STEEL), outline=rgba(OUTL))
    d.rectangle([6, 10, 25, 21], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.ellipse([14, 14, 17, 17], fill=rgba(BLACK)); d.line([(16, 2), (16, 9)], fill=rgba(STEEL_L), width=2)
    d.line([(9, 18), (14, 16)], fill=rgba(BLOOD))
@tile("silla", False)
def _(d, r):
    d.rectangle([9, 4, 22, 12], fill=rgba(WOOD_D), outline=rgba(OUTL))
    d.rectangle([8, 13, 23, 20], fill=rgba(WOOD), outline=rgba(OUTL))
    d.line([(9, 21), (9, 28)], fill=rgba(OUTL)); d.line([(22, 21), (22, 28)], fill=rgba(OUTL))
@tile("ventana_oficina", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(WOOD)); d.line([(0, 0), (31, 0)], fill=rgba(OUTL))
    d.rectangle([3, 5, 28, 28], fill=rgba((50, 46, 44)), outline=rgba(OUTL))
    for y in range(7, 28, 3): d.line([(4, y), (27, y)], fill=rgba((130, 120, 100)))  # persiana
@tile("persiana_alta", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba((100, 98, 92))); d.line([(0, 0), (31, 0)], fill=rgba(OUTL))
    for y in range(3, 32, 4): d.line([(0, y), (31, y)], fill=rgba((76, 74, 70)))
@tile("persiana_baja", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba((100, 98, 92)))
    for y in range(3, 28, 4): d.line([(0, y), (31, y)], fill=rgba((76, 74, 70)))
    d.rectangle([0, 28, 31, 31], fill=rgba((50, 48, 46))); d.rectangle([4, 20, 27, 27], fill=rgba(BLOOD_D))

# ===================================================== fila 7: exterior y capas
@tile("alambrada", False)
def _(d, r):
    d.rectangle([0, 14, 31, 31], fill=rgba((0, 0, 0, 0)))
    for i in range(-32, 32, 6):
        d.line([(i, 2), (i + 28, 30)], fill=rgba((120, 124, 126)))
        d.line([(i + 28, 2), (i, 30)], fill=rgba((120, 124, 126)))
    d.rectangle([0, 0, 31, 2], fill=rgba(STEEL_D)); d.rectangle([14, 0, 17, 31], fill=rgba(STEEL_D), outline=rgba(OUTL))
@tile("cartel", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(BRICK_D))
    d.rectangle([1, 6, 30, 24], fill=rgba((196, 190, 176)), outline=rgba(OUTL))
    d.rectangle([3, 9, 28, 14], fill=rgba(BLOOD)); d.rectangle([3, 17, 28, 20], fill=rgba((60, 60, 60)))
@tile("farola", False, 1)
def _(d, r):
    d.rectangle([14, 2, 17, 31], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.rectangle([9, 0, 22, 5], fill=rgba((200, 190, 140)), outline=rgba(OUTL))
@tile("vacio", False)
def _(d, r):
    d.rectangle([0, 0, 31, 31], fill=rgba(BLACK))
@tile("lampara", True, 3)
def _(d, r):
    d.line([(16, 0), (16, 8)], fill=rgba(OUTL))
    d.polygon([(8, 16), (24, 16), (20, 8), (12, 8)], fill=rgba((70, 74, 70)), outline=rgba(OUTL))
    d.ellipse([12, 14, 20, 19], fill=rgba((230, 224, 180)))
@tile("mancha", True)
def _(d, r):
    splat(d, r, 15, 16, 5, BLOOD_D, 7); d.ellipse([12, 13, 17, 16], fill=rgba(BLOOD))
@tile("huellas", True)
def _(d, r):
    for i in range(4):
        x = 6 + i * 6; y = 22 - i * 5 + (i % 2) * 3
        d.ellipse([x, y, x + 3, y + 5], fill=rgba(BLOOD_D, 200))
@tile("paja_suelta", True, 0, True)
def _(d, r):
    for _ in range(18):
        x, y = r.randint(0, 31), r.randint(0, 31)
        d.line([(x, y), (x + r.randint(-4, 4), y + r.randint(-2, 2))], fill=rgba(STRAW))

assert len(TILES) == 64, len(TILES)
ID = {name: 384 + i for i, (name, *_ ) in enumerate(TILES)}

def build_tileset():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for i, (name, fn, *_ ) in enumerate(TILES):
        im, d = new()
        fn(d, random.Random(i * 7 + 1))
        sheet.alpha_composite(im, ((i % COLS) * 32, (i // COLS) * 32))
    sheet.save(PROJ + "Tilesets/vacas_matadero.png")

def tables(ts18_passages, ts18_prios):
    """Tablas de pasabilidad y prioridad para el tileset nuevo (448 ids)."""
    n = 384 + 64
    pas = [0] * n; pri = [0] * n
    pri[0] = ts18_prios[0]   # 5, como en RMXP: los eventos sin tile no abren paso
    # autotile 0 (pared, 48..95): igual que en el tileset 18
    for i in range(48, 96):
        pas[i] = ts18_passages[i]; pri[i] = ts18_prios[i]
    # autotile 1 (canal de desague, 96..143): pasable, con efecto «bush»
    for i in range(96, 144):
        pas[i] = 64
    for i, (name, fn, passable, prio, bush) in enumerate(TILES):
        tid = 384 + i
        pas[tid] = (0 if passable else 15) + (64 if bush else 0)
        pri[tid] = prio
    return pas, pri

# ------------------------------------------------------------------ autotile canal
def build_canal():
    src = Image.open(RTP + "Autotiles/048-Water01.png").convert("RGBA")
    px = src.load()
    out = Image.new("RGBA", src.size)
    po = out.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = px[x, y]
            lum = (r * 3 + g * 6 + b) / 10
            sat = max(r, g, b) - min(r, g, b)
            if lum < 125 or (b > r + 6 and sat > 12):   # agua -> sangre oscura, lisa
                v = int(lum * 0.35)
                po[x, y] = (58 + v, 8 + v // 6, 8 + v // 6, a)
            else:                                # piedra -> azulejo blanco sucio
                v = int(min(235, lum * 1.1 + 25))
                po[x, y] = (v, v, int(v * 0.96), a)
    out.save(PROJ + "Autotiles/vacas_canal.png")

# ------------------------------------------------------------------ personajes
def grim(im, sat=0.45, bright=0.85, tint=(1.0, 0.97, 0.85)):
    im = im.convert("RGBA"); a = im.getchannel("A")
    rgb = im.convert("RGB")
    rgb = ImageEnhance.Color(rgb).enhance(sat); rgb = ImageEnhance.Brightness(rgb).enhance(bright)
    r, g, b = rgb.split()
    r = r.point(lambda v: min(255, int(v * tint[0]))); g = g.point(lambda v: min(255, int(v * tint[1])))
    b = b.point(lambda v: min(255, int(v * tint[2])))
    out = Image.merge("RGB", (r, g, b)).convert("RGBA"); out.putalpha(a); return out

def scale_sheet(im, sx, sy):
    fw, fh = im.width // 4, im.height // 4
    nw, nh = int(round(fw * sx)), int(round(fh * sy))
    out = Image.new("RGBA", (nw * 4, nh * 4), (0, 0, 0, 0))
    for r in range(4):
        for c in range(4):
            f = im.crop((c * fw, r * fh, (c + 1) * fw, (r + 1) * fh)).resize((nw, nh), Image.NEAREST)
            out.alpha_composite(f, (c * nw, r * nh))
    return out

def stains(im, seed, n=10, color=BLOOD, region=(0.3, 0.55, 0.95)):
    """Salpica manchas de sangre sobre los pixeles opacos del cuerpo."""
    r = random.Random(seed)
    px = im.load()
    fw, fh = im.width // 4, im.height // 4
    for row in range(4):
        for col in range(4):
            for _ in range(n):
                for _try in range(20):
                    x = col * fw + r.randint(int(fw * .2), int(fw * .8))
                    y = row * fh + r.randint(int(fh * region[1]), int(fh * region[2]) - 1)
                    if px[x, y][3] > 200:
                        px[x, y] = rgba(color)
                        if x + 1 < im.width and px[x + 1, y][3] > 200:
                            px[x + 1, y] = rgba(BLOOD_D)
                        break
    return im

def whites(im, strength=0.75):
    """Blanquea la ropa: aclara los pixeles de color saturado (mono de trabajo)."""
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 10: continue
            mx, mn = max(r, g, b), min(r, g, b)
            # no tocar piel (r>g>b calidos) ni pelo oscuro
            skin = r > 150 and g > 100 and r > b + 30 and r - g < 70
            if not skin and mx > 60 and mx - mn > 25:
                v = int(mx * strength + 255 * (1 - strength) * 0.8)
                px[x, y] = (v, v, int(v * 0.96), a)
    return im

def src(n):
    return Image.open(RTP + "Characters/" + n + ".png").convert("RGBA")

def build_chars():
    C = PROJ + "Characters/"
    # Cripps: grande, pesado, delantal manchado
    cr = grim(src("046-Grappler01"), 0.25, 0.72, (1.0, 0.95, 0.88))
    cr = stains(whites(cr, 0.8), 11, 14)
    scale_sheet(cr, 1.3, 1.25).save(C + "vacas_cripps.png")
    # companeros de la cadena: monos blancos, sangre
    for i, n in enumerate(["138-Cook01", "143-Farmer01", "144-Farmer02", "145-Prisoner01"]):
        o = grim(src(n), 0.3, 0.82)
        o = stains(whites(o, 0.85), 20 + i, 8)
        o.save(C + "vacas_obrero%d.png" % (i + 1))
    # Steven con el mono de trabajo
    st = grim(src("107-Civilian07"), 0.4, 0.85)
    whites(st, 0.9).save(C + "vacas_steven_mono.png")
    # vacas del corral
    grim(src("156-Animal06"), 0.35, 0.8, (1.0, 0.95, 0.88)).save(C + "vacas_vaca.png")
    # la vaca del fondo: clara, color leche con canela
    grim(src("156-Animal06"), 0.55, 1.45, (1.12, 0.98, 0.78)).save(C + "vacas_vaca_canela.png")
    # Lucy
    grim(src("123-Civilian23"), 0.4, 0.82, (1.0, 0.96, 0.9)).save(C + "vacas_lucy.png")

# ------------------------------------------------------------------ objetos
FW, FH = 32, 64
def build_objetos():
    sheet = Image.new("RGBA", (FW * 4, FH * 4), (0, 0, 0, 0))
    def frame():
        im = Image.new("RGBA", (FW, FH), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
    def put(im, col, row): sheet.alpha_composite(im, (col * FW, row * FH))
    # fila 0 (dir 2): cinta en movimiento (4 fotogramas) con una pieza
    for k in range(4):
        im, d = frame()
        d.rectangle([0, 38, 31, 57], fill=rgba(STEEL_D), outline=rgba(OUTL))
        d.rectangle([0, 41, 31, 54], fill=rgba((52, 52, 54)))
        for x in range(-6 + k * 2, 32, 6):
            d.line([(x, 41), (x, 54)], fill=rgba((80, 80, 82)))
        d.line([(0, 58), (31, 58)], fill=rgba(BLACK))
        put(im, k, 0)
    # fila 1 (dir 4): canales colgadas
    def canal(d, full=True, sway=0):
        d.line([(16, 0), (16, 8)], fill=rgba(STEEL_L), width=2)
        d.arc([11, 6, 21, 14], 0, 180, fill=rgba(STEEL_L), width=2)
        pts = [(10 + sway, 12), (22 + sway, 12), (25 + sway, 30), (23 + sway, 50), (17 + sway, 60), (13 + sway, 60), (8 + sway, 46), (7 + sway, 28)]
        if not full:
            pts = [(12 + sway, 12), (20 + sway, 12), (22 + sway, 30), (20 + sway, 50), (16 + sway, 60), (12 + sway, 46), (10 + sway, 28)]
        d.polygon(pts, fill=rgba((146, 52, 48)), outline=rgba(OUTL))
        d.polygon([(p[0] + (2 if p[0] < 16 + sway else -2), p[1] + 2) for p in pts[2:6]], fill=rgba((176, 84, 72)))
        for y in range(20, 52, 5):
            d.line([(11 + sway, y), (21 + sway, y + 1)], fill=rgba((214, 196, 170)))   # costillas / grasa
        d.line([(16 + sway, 14), (16 + sway, 58)], fill=rgba((96, 26, 24)))
    for k, (full, sway) in enumerate([(True, 0), (False, 0), (True, 1), (None, 0)]):
        im, d = frame()
        if full is None:
            d.line([(16, 0), (16, 10)], fill=rgba(STEEL_L), width=2)
            d.arc([10, 8, 22, 22], 300, 210, fill=rgba(STEEL_L), width=2)
            d.point((11, 13), fill=rgba(STEEL_L))
        else:
            canal(d, full, sway)
        put(im, k, 1)
    # fila 2 (dir 6): fichadora, pistola de perno, cubo, caja de piezas
    im, d = frame()
    d.rectangle([5, 22, 26, 58], fill=rgba((150, 140, 116)), outline=rgba(OUTL))
    d.ellipse([9, 26, 22, 39], fill=rgba((226, 222, 206)), outline=rgba(OUTL))
    d.line([(15, 32), (15, 28)], fill=rgba(OUTL)); d.line([(15, 32), (19, 33)], fill=rgba(OUTL))
    d.rectangle([10, 43, 21, 46], fill=rgba(BLACK))
    for i in range(5): d.rectangle([27, 24 + i * 7, 31, 29 + i * 7], fill=rgba((200, 196, 170)), outline=rgba(OUTL))
    d.text((9, 48), "TURNO", fill=rgba(BLOOD)) if False else d.rectangle([9, 50, 22, 53], fill=rgba(BLOOD))
    put(im, 0, 2)
    im, d = frame()
    d.line([(16, 10), (16, 28)], fill=rgba((40, 40, 40)))
    d.rectangle([9, 28, 23, 36], fill=rgba(STEEL), outline=rgba(OUTL))
    d.rectangle([13, 36, 19, 50], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.rectangle([20, 31, 28, 34], fill=rgba(STEEL_L), outline=rgba(OUTL))
    d.line([(16, 50), (16, 54)], fill=rgba(BLOOD))
    put(im, 1, 2)
    im, d = frame()
    d.polygon([(6, 38), (26, 38), (24, 60), (8, 60)], fill=rgba((100, 104, 108)), outline=rgba(OUTL))
    d.ellipse([6, 34, 26, 42], fill=rgba(BLOOD_D), outline=rgba(OUTL))
    d.ellipse([10, 35, 16, 39], fill=rgba(BLOOD_L))
    put(im, 2, 2)
    im, d = frame()
    d.rectangle([4, 42, 27, 60], fill=rgba((180, 184, 186)), outline=rgba(OUTL))
    d.rectangle([7, 38, 24, 46], fill=rgba((150, 52, 46)), outline=rgba(OUTL))
    d.line([(9, 41), (21, 41)], fill=rgba((214, 196, 170)))
    put(im, 3, 2)
    # fila 3 (dir 8): la rejilla de ventilacion (normal, ojo, hocico, doblada)
    def rejilla(d, inner):
        d.rectangle([3, 34, 28, 58], fill=rgba(STEEL_D), outline=rgba(OUTL))
        d.rectangle([5, 36, 26, 56], fill=rgba(BLACK))
        inner(d)
        for y in range(38, 56, 3):
            d.line([(5, y), (26, y)], fill=rgba((96, 100, 106)))
        for x in (3, 26):
            d.rectangle([x, 35, x + 2, 37], fill=rgba(STEEL_L))
    def nada(d): pass
    def ojo(d):
        d.ellipse([9, 41, 22, 50], fill=rgba((150, 120, 90)))
        d.ellipse([12, 42, 19, 49], fill=rgba((40, 26, 20)))
        d.ellipse([14, 44, 16, 46], fill=rgba((230, 230, 220)))
    def hocico(d):
        d.ellipse([6, 42, 25, 56], fill=rgba((176, 128, 110)))
        d.ellipse([9, 47, 13, 51], fill=rgba((40, 20, 20))); d.ellipse([18, 47, 22, 51], fill=rgba((40, 20, 20)))
        d.point([(11, 44), (20, 53)], fill=rgba((230, 230, 240)))
    for k, fn in enumerate([nada, ojo, hocico]):
        im, d = frame(); rejilla(d, fn); put(im, k, 3)
    im, d = frame()
    d.rectangle([3, 34, 28, 58], fill=rgba(BLACK), outline=rgba(OUTL))
    d.polygon([(5, 36), (26, 36), (22, 44), (8, 42)], fill=rgba(STEEL_D), outline=rgba(OUTL))
    d.line([(10, 56), (12, 50)], fill=rgba((150, 120, 90)))
    put(im, 3, 3)
    sheet.save(PROJ + "Characters/vacas_matadero.png")

if __name__ == "__main__":
    build_tileset(); build_canal(); build_chars(); build_objetos()
    print("tiles", len(TILES))
