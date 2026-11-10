
# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
# Mapas del Acto II (matadero). Genera lotes de tiles para el MCP.
#   python maps2.py crear        -> b_crear_mapas2.json (create_map x7)
#   python maps2.py tiles        -> b_tiles2.json (todas las capas)
import json, random, sys
from gfx_acto2 import ID

TS = 51
# id, nombre, ancho, alto
MAPAS = [
    (5, "Matadero: entrada", 30, 22),
    (6, "Matadero: vestuario", 20, 15),
    (7, "Matadero: corrales", 30, 20),
    (8, "Matadero: la cadena", 40, 24),
    (9, "Matadero: cámaras frías", 30, 20),
    (10, "Matadero: oficina de Cripps", 20, 15),
    (11, "Matadero: pasillo de mantenimiento", 30, 15),
]

def blank(w, h):
    return [[0] * w for _ in range(h)]

class Mapa:
    def __init__(self, mid, rows, legend, seed):
        self.mid = mid
        self.rows = rows
        self.H, self.W = len(rows), len(rows[0])
        assert all(len(r) == self.W for r in rows), (mid, [len(r) for r in rows])
        self.z = [blank(self.W, self.H) for _ in range(3)]
        self.walls, self.canal = [], []
        self.r = random.Random(seed)
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == '#':
                    self.walls.append([x, y])
                elif c == '~':
                    self.canal.append([x, y])
                else:
                    t = legend[c]
                    if isinstance(t, (list, tuple)):     # (comun, raro, prob_raro)
                        t = t[1] if self.r.random() < t[2] else t[0]
                    self.z[0][y][x] = ID[t]
    def put(self, layer, x, y, name):
        self.z[layer][y][x] = ID[name]
    def ops(self):
        b = []
        for l in range(3):
            b.append(["set_map_tiles", {"mapId": self.mid, "layer": l, "x": 0, "y": 0, "grid": self.z[l]}])
        if self.walls:
            b.append(["apply_autotile", {"mapId": self.mid, "layer": 0, "autotileSlot": 0, "cells": self.walls}])
        if self.canal:
            b.append(["apply_autotile", {"mapId": self.mid, "layer": 0, "autotileSlot": 1, "cells": self.canal}])
        return b

TILE_FLOOR = ("azulejo", "azulejo_sucio", 0.35)

# ------------------------------------------------------------ 5 entrada
ENTRADA = [
    "##############################",
    "#WWWWWWWWWWWWWWWWWWWWWWWWWWWW#",
    "#wwwwwwwwwwwwwwwwwwwwwwwwwwww#",
    "#............................#",
    "#............................#",
    "#............................#",
    "#............................#",
    "#............................#",
    "#............................#",
    "##############..##############",
    "BBBBBBBBBBBBBB..BBBBBBBBBBBBBB",
    "bbbbbbbbbbbbbb..bbbbbbbbbbbbbb",
    "pppppppppppppp..pppppppppppppp",
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "mmmmmmmaaaaaaaaaaaaaaaaaaaaaaa",
    "mmmmmmmaaaaaaaaaaaaaaaaaaaaaaa",
    "mmmmmmmaaaaaaaaaaaaaaaaaaaaaaa",
    "mmmmmmaaaaaaaaaaaaaaaaaaaaaaaa",
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "ffffffffffffffaaffffffffffffff",
]
def build_entrada():
    m = Mapa(5, ENTRADA, {
        "W": "pared_azulejo_alta", "w": "pared_azulejo_baja", ".": TILE_FLOOR,
        "B": "ladrillo_alto", "b": "ladrillo_bajo", "p": "acera",
        "a": ("asfalto", "asfalto_charco", 0.04), "m": ("barro", "barro", 0), "f": "alambrada"}, 5)
    for x in (4, 10, 19, 25):
        m.put(0, x, 1, "ventana_nave")
    m.put(0, 5, 2, "puerta_metal"); m.put(0, 24, 2, "puerta_metal")
    m.put(0, 17, 2, "reloj_pared")
    for x in (9, 10, 11):
        m.put(1, x, 7, "banco")
    m.put(1, 2, 3, "cajas"); m.put(1, 27, 3, "cubo_despojos")
    m.put(1, 20, 5, "mancha"); m.put(1, 14, 8, "huellas"); m.put(1, 15, 7, "huellas")
    for x in (7, 22):
        m.put(2, x, 4, "lampara")
    m.put(0, 11, 10, "cartel"); m.put(0, 18, 10, "cartel")
    for x in (3, 26):
        m.put(1, x, 13, "farola")
    m.put(1, 3, 17, "paja_suelta"); m.put(1, 5, 15, "paja_suelta"); m.put(1, 6, 18, "mancha")
    m.put(1, 8, 16, "huellas")
    return m

# ------------------------------------------------------------ 6 vestuario
VEST = [
    "####################",
    "#WWWWWWWWWWWWWWWWWW#",
    "#wwwwwwwwwwwwwwwwww#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#...................",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#########..#########",
    "####################",
]
def build_vestuario():
    m = Mapa(6, VEST, {"W": "pared_azulejo_alta", "w": "pared_azulejo_baja", ".": TILE_FLOOR}, 6)
    for x in range(2, 11):
        m.put(1, x, 2, "taquilla_alta"); m.put(1, x, 3, "taquilla_baja")
    for x in range(3, 9):
        m.put(1, x, 7, "banco")
    for x in (14, 15, 16):
        m.put(1, x, 3, "fregadero")
    m.put(0, 17, 2, "manguera"); m.put(0, 12, 2, "reloj_pared")
    m.put(0, 15, 9, "rejilla_suelo")
    m.put(1, 13, 10, "huellas"); m.put(1, 16, 6, "mancha")
    m.put(2, 7, 5, "lampara"); m.put(2, 15, 6, "lampara")
    m.put(1, 2, 11, "cajas"); m.put(1, 18, 12, "cubo_despojos")
    return m

# ------------------------------------------------------------ 7 corrales
CORR = [
    "##############################",
    "#WWWWWWWWWWWWWWWWWWWWWWWWWWWW#",
    "#wwwwwwwwwwwwwwwwwwwwwwwwwwww#",
    "#.............................",
    "#.............................",
    "#............................#",
    "#............................#",
    "#ssssssss.ssssssss.sssssssss.#",
    "#ssssssss.ssssssss.sssssssss.#",
    "#ssssssss.ssssssss.sssssssss.#",
    "#ssssssss.ssssssss.sssssssss.#",
    "#ssssssss.ssssssss.sssssssss.#",
    "#ssssssss.ssssssss.sssssssss.#",
    "#ssssssss.ssssssss.sssssssss.#",
    "#ssssssss.ssssssss.sssssssss.#",
    "#ssssssss.ssssssss.sssssssss.#",
    "#............................#",
    "#............................#",
    "#............................#",
    "##############################",
]
def build_corrales():
    m = Mapa(7, CORR, {"W": "pared_hormigon_alta", "w": "pared_hormigon_baja",
                       ".": ("hormigon", "hormigon_mojado", 0.04), "s": "paja"}, 7)
    # manga (pasillo de las reses) hacia la cadena: filas 3-4 desde x=12
    for x in range(12, 29):
        m.put(1, x, 5, "valla_h")
    m.put(1, 12, 5, "valla_poste")
    # corrales: vallas superior (fila 7) e inferior (fila 16) y laterales; fila 6 = pasillo
    for x in range(1, 28):
        if x in (9, 18):
            continue
        m.put(1, x, 7, "valla_h"); m.put(1, x, 16, "valla_h")
    for x in (4, 13, 23):
        m.put(1, x, 7, "puerta_corral")
    for y in range(8, 16):
        m.put(1, 9, y, "valla_v"); m.put(1, 18, y, "valla_v"); m.put(1, 28, y, "valla_v")
    for x in (9, 18, 28):
        m.put(1, x, 7, "valla_poste"); m.put(1, x, 16, "valla_poste")
    m.put(0, 6, 2, "tuberia"); m.put(0, 20, 2, "tuberia"); m.put(0, 26, 2, "manguera")
    m.put(1, 2, 17, "cubo_despojos"); m.put(1, 25, 18, "cajas")
    m.put(1, 20, 3, "huellas"); m.put(1, 26, 4, "mancha"); m.put(1, 15, 17, "mancha")
    for x in (6, 15, 24):
        m.put(2, x, 9, "lampara")
    return m

# ------------------------------------------------------------ 8 la cadena
CAD = [
    "########################################",
    "#WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW#",
    "#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww#",
    "#......................................#",
    "#......................................#",
    "#......................................#",
    "#......................................#",
    ".......................................#",
    "#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#",
    "#.......................................",
    "#......................................#",
    "#......................................#",
    "#......................................#",
    "#......................................#",
    "#......................................#",
    "#......................................#",
    "#......................................#",
    "#......................................#",
    "#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#",
    "#......................................#",
    "#......................................#",
    "#......................................#",
    "#####.##########################.#######",
    "########################################",
]
def build_cadena():
    m = Mapa(8, CAD, {"W": "pared_azulejo_alta", "w": "pared_azulejo_baja",
                      ".": ("azulejo_sucio", "azulejo_sangre", 0.06)}, 8)
    for x in (8, 16, 24, 30):
        m.put(0, x, 1, "ventana_nave")
    m.put(0, 35, 2, "puerta_metal")          # escalera a la oficina
    m.put(0, 11, 2, "cuchillos"); m.put(0, 12, 2, "cuchillos"); m.put(0, 27, 2, "cuchillos")
    m.put(0, 20, 2, "reloj_pared"); m.put(0, 31, 2, "manguera")
    # cajon de aturdimiento (oeste), junto a la entrada de la manga
    for (x, y) in [(2, 4), (3, 4), (2, 5), (3, 5)]:
        m.put(1, x, y, "cajon_aturdir")
    m.put(1, 1, 7, "huellas"); m.put(1, 3, 6, "mancha"); m.put(1, 5, 5, "azulejo_arrastre")
    m.put(0, 5, 5, "azulejo_arrastre"); m.put(0, 6, 6, "azulejo_arrastre")
    # railes de carga (capa superior) y ganchos
    for y in (5, 11):
        for x in range(5, 38):
            m.put(2, x, y, "rail_gancho" if x % 3 == 0 else "rail")
    # la cinta
    m.put(1, 8, 15, "cinta_ini")
    for x in range(9, 30):
        m.put(1, x, 15, "cinta")
    m.put(1, 30, 15, "cinta_fin")
    # mesas y cubos
    for x in (12, 13, 26, 27):
        m.put(1, x, 20, "mesa_acero")
    for (x, y) in [(7, 17), (32, 16), (36, 13), (2, 10)]:
        m.put(1, x, y, "cubo_despojos")
    m.put(1, 37, 19, "cajas"); m.put(1, 38, 19, "cajas")
    for (x, y) in [(1, 9), (38, 9), (1, 19), (38, 17)]:
        m.put(0, x, y, "rejilla_suelo")
    for (x, y) in [(10, 13), (21, 7), (29, 12), (17, 19), (33, 6), (6, 10)]:
        m.put(1, x, y, "mancha")
    for (x, y) in [(24, 17), (25, 16), (4, 20), (33, 20)]:
        m.put(1, x, y, "huellas")
    for (x, y) in [(10, 3), (20, 3), (30, 3), (10, 13), (20, 13), (30, 13), (20, 20)]:
        m.put(2, x, y, "lampara")
    return m

# ------------------------------------------------------------ 9 camaras frias
CAM = [
    "##############################",
    "#WWWWWWWW#WWWWWWWW#WWWWWWWWWW#",
    "#wwwwwwww#wwwwwwww#wwwwwwwwww#",
    "#........#........#..........#",
    "#........#........#..........#",
    "#........#........#..........#",
    "#........#........#..........#",
    "#........#........#..........#",
    "#........#........#..........#",
    "#........#........#..........#",
    "#........#........#..........#",
    "#........#........#..........#",
    "#........#........#..........#",
    "####..########..########..####",
    "#WWW..WWWWWWWW..WWWWWWWW..WWW#",
    "#www..wwwwwwww..wwwwwwww..www#",
    "#............................#",
    ".............................#",
    "#............................#",
    "##############################",
]
def build_camaras():
    m = Mapa(9, CAM, {"W": "pared_fria_alta", "w": "pared_fria_baja", ".": "suelo_frio"}, 9)
    for (x0, x1) in [(2, 7), (11, 16), (20, 27)]:
        for x in range(x0, x1 + 1):
            if x % 2 == 0:
                for y in (4, 8):
                    m.put(2, x, y, "rail_gancho")
    m.put(1, 3, 3, "cajas"); m.put(1, 7, 3, "cajas")
    m.put(1, 12, 3, "cubo_despojos"); m.put(1, 16, 3, "cubo_despojos")
    m.put(1, 21, 3, "cajas"); m.put(1, 27, 3, "cajas")
    for (x, y) in [(5, 12), (14, 10), (23, 11), (10, 17), (19, 16)]:
        m.put(1, x, y, "mancha")
    for x in (5, 14, 24):
        m.put(2, x, 16, "lampara")
    return m

# ------------------------------------------------------------ 10 oficina
OFI = [
    "####################",
    "#WWWWWWWWWWWWWWWWWW#",
    "#wwwwwwwwwwwwwwwwww#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#########..#########",
    "####################",
]
def build_oficina():
    m = Mapa(10, OFI, {"W": "pared_madera_alta", "w": "pared_madera_baja", ".": ("linoleo", "linoleo", 0)}, 10)
    for x in range(3, 8):
        m.put(0, x, 1, "persiana_alta"); m.put(0, x, 2, "persiana_baja")
    m.put(0, 12, 1, "ventana_oficina")
    m.put(1, 4, 6, "escritorio_izq"); m.put(1, 5, 6, "escritorio_der")
    m.put(1, 5, 7, "silla")
    for x in (14, 15, 16):
        m.put(1, x, 2, "archivador_alto"); m.put(1, x, 3, "archivador_bajo")
    m.put(1, 18, 9, "cajas"); m.put(1, 18, 10, "cajas"); m.put(1, 2, 11, "cubo_despojos")
    m.put(1, 9, 11, "huellas"); m.put(1, 10, 9, "huellas"); m.put(1, 7, 8, "mancha")
    m.put(2, 9, 5, "lampara")
    return m

# ------------------------------------------------------------ 11 pasillo
PAS = [
    "##############################",
    "#WWWWWWWWWWWWWWWWWWWWWWWWWWWW#",
    "#wwwwwwwwwwwwwwwwwwwwwwwwwwww#",
    "#............................#",
    "#............................#",
    "#............................#",
    "#............................#",
    ".............................#",
    "#............................#",
    "#............................#",
    "#............................#",
    "#............................#",
    "##############################",
    "##############################",
    "##############################",
]
def build_pasillo():
    m = Mapa(11, PAS, {"W": "pared_hormigon_alta", "w": "pared_hormigon_baja",
                       ".": ("hormigon", "hormigon_mojado", 0.05)}, 11)
    for x in (3, 7, 11, 15, 26):
        m.put(0, x, 2, "tuberia")
    m.put(0, 22, 2, "rejilla_pared")         # LA rejilla (el evento va encima)
    m.put(0, 9, 2, "manguera")
    m.put(1, 2, 3, "cajas"); m.put(1, 3, 3, "cajas"); m.put(1, 2, 4, "cajas")
    m.put(1, 28, 10, "cubo_despojos"); m.put(1, 13, 11, "cajas")
    m.put(0, 26, 9, "rejilla_suelo")        # trampilla al desague (Acto IV)
    m.put(1, 21, 4, "huellas"); m.put(1, 23, 5, "mancha")
    for x in (6, 18):
        m.put(2, x, 5, "lampara")
    return m

BUILDERS = [build_entrada, build_vestuario, build_corrales, build_cadena, build_camaras, build_oficina, build_pasillo]

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "crear":
        b = [["create_map", {"name": n, "width": w, "height": h, "tilesetId": TS}] for (_, n, w, h) in MAPAS]
        json.dump(b, open(str(_ROOT / 'diseno/archivo/lotes/b_crear_mapas2.json'), "w", encoding="utf-8"), ensure_ascii=False)
    else:
        b = []
        for fn in BUILDERS:
            b += fn().ops()
        json.dump(b, open(str(_ROOT / 'diseno/archivo/lotes/b_tiles2.json'), "w", encoding="utf-8"), ensure_ascii=False)
    print(what, len(b))
