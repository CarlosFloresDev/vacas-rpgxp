# Construye los mapas del Acto I (tiles) y genera lotes para el MCP.
import json, random, sys

def blank(w, h):
    return [[0] * w for _ in range(h)]

def stamp(layer, x, y, block):
    for j, row in enumerate(block):
        for i, t in enumerate(row):
            if t:
                layer[y + j][x + i] = t

def ops_for(mid, z0, z1, z2, wall_cells, wall_slot=0, extra=None):
    b = []
    b.append(["set_map_tiles", {"mapId": mid, "layer": 0, "x": 0, "y": 0, "grid": z0}])
    b.append(["set_map_tiles", {"mapId": mid, "layer": 1, "x": 0, "y": 0, "grid": z1}])
    b.append(["set_map_tiles", {"mapId": mid, "layer": 2, "x": 0, "y": 0, "grid": z2}])
    if wall_cells:
        b.append(["apply_autotile", {"mapId": mid, "layer": 0, "autotileSlot": wall_slot, "cells": wall_cells}])
    for e in (extra or []):
        b.append(e)
    return b

# ---------------------------------------------------------------- PISO (map 2)
PISO = [
    "##############################",
    "#WWWWWWWW#WWWWW#WWWWWWWWWWWWW#",
    "#wwwwwwww#wwwww#wwwwwwwwwwwww#",
    "#........#,,,,,#.............#",
    "#........#,,,,,#.............#",
    "#........#,,,,,#.............#",
    "#........#,,,,,#.............#",
    "#........#,,,,,#.............#",
    "#........#,,,,,#.............#",
    "#####.######,#########.#######",
    "#WWWW.WWWWWW,WWWWWWWWW.WWWWWW#",
    "#wwww.wwwwww,wwwwwwwww.wwwwww#",
    "#............................#",
    "#............................#",
    "######.#######..######.#######",
    "#WWWWW.WWWWWW#..#WWWWW.WWWWWW#",
    "#wwwww.wwwwww#..#wwwww.wwwwww#",
    "#............#..#,,,,,,,,,,,,#",
    "#............#..#,,,,,,,,,,,,#",
    "#............#..#,,,,,,,,,,,,#",
    "#............#..#,,,,,,,,,,,,#",
    "##############..##############",
]

def build_piso():
    H, W = len(PISO), len(PISO[0])
    assert all(len(r) == W for r in PISO), [len(r) for r in PISO]
    z0, z1, z2 = blank(W, H), blank(W, H), blank(W, H)
    rnd = random.Random(3)
    walls = []
    def brick_zone(x, y):
        return (10 <= x <= 14 and y <= 8) or (17 <= x <= 28 and y >= 15)
    for y, row in enumerate(PISO):
        for x, c in enumerate(row):
            if c == '#':
                walls.append([x, y])
            elif c in 'Ww':
                up = c == 'W'
                k = x % 3
                if brick_zone(x, y):
                    z0[y][x] = (416 if up else 424) + k
                else:
                    z0[y][x] = (400 if up else 408) + k
            elif c == '.':
                z0[y][x] = (388 if rnd.random() < 0.9 else 387)
            elif c == ',':
                z0[y][x] = (385 if rnd.random() < 0.85 else 384)
    # puertas abiertas en filas de pared superior que el ASCII deja como '.'/','
    # ventanas
    for (x, y) in [(3, 1), (19, 1), (26, 1), (3, 15), (26, 15)]:
        z1[y][x] = 406; z1[y + 1][x] = 414
    # ---- cuarto de Steven
    stamp(z1, 1, 3, [[447], [455]])          # cama
    stamp(z1, 3, 2, [[458, 459], [466, 467]])  # cajonera
    stamp(z1, 5, 3, [[422]])                 # taburete
    stamp(z2, 3, 2, [[0, 431]])              # libro sobre la cajonera
    # ---- bano: tuberia
    stamp(z1, 14, 1, [[505], [513]])
    # ---- cuarto de la madre
    stamp(z1, 17, 3, [[447, 463], [455, 471]])   # cama doble
    stamp(z1, 21, 2, [[458, 459], [466, 467]])   # comoda
    stamp(z1, 23, 1, [[469]])                    # reloj de cuco
    stamp(z1, 25, 1, [[478]])                    # cuadro
    stamp(z1, 27, 3, [[474, 475], [482, 483]])   # cajas
    stamp(z1, 19, 7, [[462]])                    # cesta
    stamp(z1, 28, 7, [[446], [454]])             # lena
    # ---- pasillo
    stamp(z1, 2, 10, [[579], [587]])             # perchero con abrigo
    stamp(z1, 17, 10, [[469]])                   # reloj
    stamp(z1, 9, 10, [[478]])                    # cuadro
    stamp(z1, 27, 12, [[422]])
    stamp(z2, 27, 12, [[423]])
    # ---- salon
    stamp(z1, 5, 19, [[553, 554, 555], [561, 562, 563]])  # banco-sofa
    stamp(z1, 11, 15, [[476], [0]])               # estante en pared
    # ---- cocina
    stamp(z1, 19, 15, [[0, 436, 0], [443, 444, 445], [451, 452, 453]])  # fogon
    stamp(z1, 17, 15, [[456, 457], [464, 465], [472, 473], [480, 481]])  # aparador
    stamp(z1, 24, 18, [[432, 433, 434], [440, 441, 442], [448, 449, 450]])  # mesa
    stamp(z2, 25, 18, [[438]])                    # tetera
    stamp(z1, 27, 20, [[484]])                    # barreno con agua
    stamp(z1, 23, 15, [[477]])                    # botellas en estante
    # alfombras (autotile 1, alfombra) en z1
    extra = [
        ["apply_autotile", {"mapId": 2, "layer": 1, "autotileSlot": 1, "region": {"x": 3, "y": 17, "w": 8, "h": 2}}],
    ]
    return W, H, ops_for(2, z0, z1, z2, walls, 0, extra)

# ---------------------------------------------------------------- ESCALERA (map 3)
ESC = [
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
    "####################",
    "####################",
]

def build_escalera():
    H, W = len(ESC), len(ESC[0])
    z0, z1, z2 = blank(W, H), blank(W, H), blank(W, H)
    rnd = random.Random(5)
    walls = []
    for y, row in enumerate(ESC):
        for x, c in enumerate(row):
            if c == '#':
                walls.append([x, y])
            elif c in 'Ww':
                z0[y][x] = (416 if c == 'W' else 424) + (x % 3) + (3 if x % 7 == 0 else 0)
            elif c == '.':
                z0[y][x] = (385 if rnd.random() < 0.9 else 384)
    z1[1][12] = 406; z1[2][12] = 414            # ventana sucia
    # escalera que sube (al cuarto piso) contra la pared derecha
    stamp(z1, 16, 1, [[528, 529, 530], [536, 537, 538], [544, 545, 546]])
    # escalera que baja (a la calle), abajo a la izquierda
    stamp(z1, 1, 10, [[528, 529, 530], [536, 537, 538], [544, 545, 546]])
    # barandilla alrededor del hueco de bajada
    stamp(z1, 4, 10, [[0], [0], [0]])
    # trastos
    stamp(z1, 7, 7, [[474, 475], [482, 483]])    # cajas apiladas
    stamp(z1, 14, 9, [[422]])                    # taburete roto
    stamp(z1, 18, 9, [[446], [454]])             # lena / bolsas
    return W, H, ops_for(3, z0, z1, z2, walls, 0)

# ---------------------------------------------------------------- CALLE (map 4)
def build_calle():
    W, H = 40, 20
    z0, z1, z2 = blank(W, H), blank(W, H), blank(W, H)
    rnd = random.Random(9)
    # fachadas y = 0..5
    for x in range(W):
        for y in range(0, 6):
            if x <= 13:      # bloque de Steven: ladrillo marron
                z0[y][x] = (620 + x % 4) if y == 5 else (604 + x % 4 if y > 0 else 596 + x % 4)
            elif x <= 23:    # carniceria: estuco blanco
                z0[y][x] = (616 + x % 4) if y == 5 else (600 + x % 4 if y > 0 else 592 + x % 4)
            else:            # nave vieja: piedra con musgo
                z0[y][x] = (424 if y % 2 else 416) + x % 8
    # ventanas
    for x in (1, 4, 10):
        stamp(z1, x, 1, [[552, 553], [560, 561]])
        stamp(z1, x, 3, [[552, 553], [560, 561]])
    stamp(z1, 15, 2, [[537], [545]])           # escaparate
    stamp(z1, 21, 2, [[554], [562]])
    stamp(z1, 30, 2, [[538], [546]])           # ventanuco de la nave
    stamp(z1, 35, 2, [[538], [546]])
    # acera, calzada, acera, muro
    for x in range(W):
        for y in range(6, H):
            if y <= 8 or 15 <= y <= 16:
                z0[y][x] = 465
            elif 9 <= y <= 14:
                z0[y][x] = 385 if rnd.random() < 0.95 else 393
            else:
                z0[y][x] = (420 if y == 17 else 428) + x % 4
    # cierres laterales (calle cortada)
    for y in range(6, 17):
        z0[y][0] = 416 + (y % 4); z0[y][39] = 416 + (y % 4)
    # toldo de la carniceria
    stamp(z2, 17, 5, [[475, 476, 477], [483, 484, 485], [491, 492, 493]])
    # farolas (3 de alto)
    for x in (5, 26, 34):
        stamp(z2, x, 6, [[480], [488]])
        stamp(z1, x, 8, [[496]])
    for x in (12, 30):
        stamp(z2, x, 13, [[480], [488]])
        stamp(z1, x, 15, [[496]])
    # barriles y bancos
    for (x, y) in [(2, 7), (24, 6), (25, 6), (38, 7), (22, 16)]:
        z1[y][x] = 396
    stamp(z1, 15, 15, [[504, 505], [512, 513]])
    return W, H, ops_for(4, z0, z1, z2, [], 0)

if __name__ == "__main__":
    which = sys.argv[1]
    fn = {"piso": build_piso, "escalera": build_escalera, "calle": build_calle}[which]
    W, H, ops = fn()
    json.dump(ops, open(f"b_map_{which}.json", "w"), ensure_ascii=False)
    print(which, W, H, len(ops))
