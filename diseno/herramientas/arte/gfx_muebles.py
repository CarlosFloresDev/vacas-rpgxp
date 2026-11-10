
# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
from PIL import Image, ImageDraw
import random
OUT = "D:/descargas/Proyectos personales/Vacas/Graphics/Characters/"
FW, FH = 32, 64
sheet = Image.new("RGBA", (FW * 4, FH * 4), (0, 0, 0, 0))


def frame():
    im = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def put(im, col, row):
    sheet.alpha_composite(im, (col * FW, row * FH))


OUTL = (28, 20, 14, 255)
WOOD = (92, 62, 38, 255); WOODL = (122, 86, 54, 255); WOODD = (64, 42, 26, 255)


def tv(screen_fn, seed=0):
    im, d = frame()
    d.line([(6, 56), (5, 62)], fill=OUTL, width=2)
    d.line([(25, 56), (26, 62)], fill=OUTL, width=2)
    d.rectangle([2, 24, 29, 57], fill=WOOD, outline=OUTL)
    d.line([(3, 25), (28, 25)], fill=WOODL); d.line([(3, 56), (28, 56)], fill=WOODD)
    d.rounded_rectangle([5, 28, 22, 46], radius=4, fill=(40, 44, 40, 255), outline=OUTL)
    screen_fn(im, d, random.Random(seed))
    for y in range(29, 46, 2):
        d.line([(24, y), (27, y)], fill=WOODD)
    d.ellipse([23, 48, 27, 52], fill=(170, 150, 110, 255), outline=OUTL)
    d.ellipse([16, 48, 20, 52], fill=(170, 150, 110, 255), outline=OUTL)
    d.rectangle([6, 49, 13, 51], fill=WOODD)
    d.line([(14, 24), (9, 12)], fill=(120, 120, 120, 255)); d.line([(17, 24), (23, 11)], fill=(120, 120, 120, 255))
    d.point([(9, 12), (23, 11)], fill=(200, 200, 200, 255))
    return im


def static(im, d, r):
    for y in range(30, 45):
        for x in range(7, 21):
            v = r.randint(60, 230)
            d.point((x, y), fill=(v, v, int(v * 0.95), 255))
    yy = 30 + r.randint(0, 14)
    d.line([(7, yy), (20, yy)], fill=(240, 240, 230, 255))


def off(im, d, r):
    d.rounded_rectangle([6, 29, 21, 45], radius=3, fill=(30, 34, 32, 255))
    d.line([(8, 31), (11, 31)], fill=(70, 80, 76, 255)); d.point((8, 32), fill=(70, 80, 76, 255))


def carta(im, d, r):
    cols = [(200, 200, 200), (200, 200, 60), (60, 200, 200), (60, 200, 60), (200, 60, 200), (200, 60, 60), (60, 60, 200)]
    for i, c in enumerate(cols):
        d.rectangle([7 + i * 2, 30, 8 + i * 2, 40], fill=c + (255,))
    d.rectangle([7, 41, 20, 44], fill=(20, 20, 20, 255))
    d.ellipse([11, 33, 16, 38], outline=(240, 240, 240, 255))


def vaca(im, d, r):
    d.rounded_rectangle([6, 29, 21, 45], radius=3, fill=(150, 160, 150, 255))
    d.ellipse([10, 33, 17, 43], fill=(30, 30, 30, 255))
    d.polygon([(10, 34), (6, 31), (9, 35)], fill=(30, 30, 30, 255))
    d.polygon([(17, 34), (21, 31), (18, 35)], fill=(30, 30, 30, 255))
    d.point([(12, 37), (15, 37)], fill=(220, 30, 30, 255))


def rojo(im, d, r):
    d.rounded_rectangle([6, 29, 21, 45], radius=3, fill=(120, 20, 18, 255))
    for y in range(30, 45, 2):
        d.line([(7, y), (20, y)], fill=(90, 10, 10, 255))


for i in range(4):
    put(tv(static, i + 1), i, 0)
put(tv(off), 0, 1); put(tv(carta), 1, 1); put(tv(vaca), 2, 1); put(tv(rojo), 3, 1)


def armario(open_=False):
    im, d = frame()
    d.rectangle([1, 8, 30, 62], fill=WOOD, outline=OUTL)
    d.rectangle([1, 8, 30, 11], fill=WOODL, outline=OUTL)
    if not open_:
        d.line([(15, 12), (15, 61)], fill=OUTL); d.line([(16, 12), (16, 61)], fill=WOODD)
        for x0 in (4, 19):
            d.rectangle([x0, 15, x0 + 8, 56], outline=WOODD)
        d.point([(13, 36), (18, 36)], fill=(200, 180, 120, 255))
    else:
        d.rectangle([3, 12, 15, 61], fill=(14, 10, 8, 255))
        d.line([(5, 14), (5, 30)], fill=(60, 60, 60, 255)); d.rectangle([4, 30, 10, 46], fill=(52, 58, 46, 255))
        d.line([(16, 12), (16, 61)], fill=OUTL); d.rectangle([19, 15, 27, 56], outline=WOODD)
    d.line([(2, 62), (29, 62)], fill=WOODD)
    return im


put(armario(False), 0, 2); put(armario(True), 1, 2)

# nevera
im, d = frame()
WH = (196, 190, 170, 255)
d.rounded_rectangle([3, 14, 28, 62], radius=4, fill=WH, outline=OUTL)
d.line([(4, 32), (27, 32)], fill=OUTL); d.line([(5, 15), (26, 15)], fill=(230, 226, 210, 255))
d.rectangle([24, 20, 25, 28], fill=(120, 120, 120, 255)); d.rectangle([24, 36, 25, 48], fill=(120, 120, 120, 255))
for p in [(8, 50), (9, 51), (18, 40), (12, 58), (20, 55)]:
    d.point(p, fill=(120, 90, 50, 255))
d.rectangle([6, 18, 12, 23], fill=(210, 200, 120, 255))
d.line([(7, 20), (11, 20)], fill=(90, 70, 40, 255))
put(im, 2, 2)

# banera vertical
im, d = frame()
d.rounded_rectangle([2, 2, 29, 62], radius=9, fill=(205, 200, 185, 255), outline=OUTL)
d.rounded_rectangle([6, 6, 25, 58], radius=7, fill=(150, 140, 110, 255), outline=(120, 110, 85, 255))
d.rounded_rectangle([8, 30, 23, 56], radius=6, fill=(110, 96, 64, 255))
d.line([(9, 28), (22, 28)], fill=(96, 70, 40, 255)); d.line([(8, 29), (23, 29)], fill=(80, 58, 34, 255))
d.rectangle([14, 2, 17, 6], fill=(140, 140, 140, 255), outline=OUTL)
d.ellipse([14, 50, 17, 53], fill=(40, 40, 40, 255))
put(im, 3, 2)

# vater
im, d = frame()
d.rectangle([9, 26, 22, 40], fill=(200, 196, 180, 255), outline=OUTL)
d.line([(10, 27), (21, 27)], fill=(230, 228, 214, 255)); d.rectangle([20, 29, 21, 31], fill=(140, 140, 140, 255))
d.ellipse([7, 38, 24, 58], fill=(205, 200, 185, 255), outline=OUTL)
d.ellipse([10, 42, 21, 55], fill=(110, 100, 70, 255), outline=(150, 140, 110, 255))
d.rectangle([12, 56, 19, 62], fill=(180, 174, 156, 255), outline=OUTL)
put(im, 0, 3)

# lavabo con espejo
im, d = frame()
d.rectangle([7, 4, 24, 24], fill=(90, 90, 80, 255), outline=OUTL)
d.rectangle([9, 6, 22, 22], fill=(150, 165, 165, 255))
d.line([(10, 20), (20, 8)], fill=(200, 210, 210, 255)); d.line([(9, 15), (13, 22)], fill=(60, 60, 60, 255))
d.rectangle([4, 36, 27, 46], fill=(205, 200, 185, 255), outline=OUTL)
d.ellipse([8, 37, 23, 45], fill=(140, 130, 100, 255), outline=(120, 110, 90, 255))
d.rectangle([14, 32, 17, 37], fill=(140, 140, 140, 255), outline=OUTL)
d.rectangle([13, 46, 18, 62], fill=(190, 186, 170, 255), outline=OUTL)
put(im, 1, 3)

# sillon gastado
im, d = frame()
C = (110, 74, 60, 255); CL = (140, 98, 78, 255); CD = (78, 50, 40, 255)
d.rounded_rectangle([3, 26, 28, 60], radius=5, fill=C, outline=OUTL)
d.rounded_rectangle([6, 28, 25, 42], radius=4, fill=CL, outline=CD)
d.rectangle([3, 42, 8, 58], fill=CD, outline=OUTL); d.rectangle([23, 42, 28, 58], fill=CD, outline=OUTL)
d.rectangle([8, 44, 23, 56], fill=CL, outline=CD)
d.ellipse([12, 47, 18, 52], fill=(150, 130, 70, 255))
d.line([(15, 30), (17, 38)], fill=(200, 190, 160, 255))
put(im, 2, 3)

# piano tapado
im, d = frame()
d.polygon([(1, 62), (2, 24), (8, 18), (24, 18), (30, 24), (31, 62)], fill=(186, 180, 164, 255), outline=OUTL)
d.line([(8, 20), (5, 60)], fill=(150, 144, 128, 255)); d.line([(22, 20), (26, 60)], fill=(150, 144, 128, 255))
d.line([(15, 22), (15, 60)], fill=(160, 154, 138, 255))
d.rectangle([4, 58, 9, 62], fill=(40, 28, 20, 255)); d.rectangle([23, 58, 28, 62], fill=(40, 28, 20, 255))
put(im, 3, 3)
sheet.save(OUT + "vacas_muebles.png")

# cosas pequenas 32x32
S2 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))


def small(col, row, fn):
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); fn(ImageDraw.Draw(im)); S2.alpha_composite(im, (col * 32, row * 32))


def bowl(full):
    def f(d):
        d.ellipse([7, 18, 25, 30], fill=(150, 40, 30, 255), outline=OUTL)
        d.ellipse([10, 20, 22, 27], fill=(120, 90, 60, 255) if full else (60, 30, 24, 255))
        if full:
            for p in [(12, 22), (15, 23), (18, 22), (14, 25), (19, 25)]:
                d.point(p, fill=(170, 120, 90, 255))
    return f


small(0, 0, bowl(False)); small(1, 0, bowl(True))


def meat(d):
    d.ellipse([5, 16, 27, 30], fill=(220, 216, 200, 255), outline=OUTL)
    d.ellipse([9, 18, 23, 27], fill=(150, 30, 36, 255), outline=(100, 16, 20, 255))
    d.line([(11, 21), (20, 24)], fill=(225, 200, 190, 255)); d.point((14, 25), fill=(90, 10, 10, 255))


small(2, 0, meat)


def puddle(d):
    d.ellipse([4, 14, 28, 28], fill=(90, 70, 40, 150)); d.ellipse([16, 10, 26, 18], fill=(90, 70, 40, 120))


small(3, 0, puddle)


def papel(d):
    d.polygon([(8, 4), (24, 6), (23, 28), (7, 27)], fill=(220, 214, 180, 255), outline=OUTL)
    for y in range(9, 24, 3):
        d.line([(10, y), (21, y + 1)], fill=(80, 70, 60, 255))
    d.rectangle([11, 6, 20, 8], fill=(150, 30, 30, 255))


small(0, 1, papel)


def botellas(d):
    for i, x in enumerate((7, 14, 21)):
        c = (60, 80, 50, 255) if i != 1 else (90, 60, 30, 255)
        d.rectangle([x, 12, x + 5, 29], fill=c, outline=OUTL)
        d.rectangle([x + 1, 6, x + 4, 12], fill=c, outline=OUTL)


small(1, 1, botellas)


def cenicero(d):
    d.ellipse([7, 18, 25, 28], fill=(140, 140, 140, 255), outline=OUTL); d.ellipse([11, 20, 21, 26], fill=(60, 60, 60, 255))
    d.line([(14, 22), (22, 18)], fill=(230, 220, 200, 255), width=2); d.point((22, 18), fill=(220, 80, 20, 255))


small(2, 1, cenicero)


def cesta(d):
    d.ellipse([3, 12, 29, 30], fill=(120, 90, 50, 255), outline=OUTL); d.ellipse([6, 15, 26, 27], fill=(80, 64, 48, 255))
    d.line([(8, 20), (22, 22)], fill=(110, 100, 90, 255), width=3)


small(3, 1, cesta)
S2.save(OUT + "vacas_cosas.png")

# furgoneta del matadero 96x64
im = Image.new("RGBA", (96, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
BODY = (196, 192, 180, 255)
d.rectangle([4, 10, 70, 52], fill=BODY, outline=OUTL)
d.polygon([(70, 22), (84, 24), (92, 36), (92, 52), (70, 52)], fill=BODY, outline=OUTL)
d.polygon([(73, 25), (84, 27), (89, 36), (73, 36)], fill=(70, 90, 96, 255), outline=OUTL)
d.rectangle([4, 40, 92, 44], fill=(140, 30, 30, 255))
d.text((10, 16), "MATADERO", fill=(120, 24, 24, 255)); d.text((12, 27), "MUNICIPAL", fill=(90, 80, 70, 255))
for x in (18, 76):
    d.ellipse([x - 8, 44, x + 8, 60], fill=(30, 30, 30, 255), outline=OUTL)
    d.ellipse([x - 3, 49, x + 3, 55], fill=(120, 120, 120, 255))
d.line([(6, 50), (30, 48)], fill=(120, 40, 30, 255))
V = Image.new("RGBA", (96 * 4, 64 * 4), (0, 0, 0, 0))
for r in range(4):
    for c in range(4):
        V.alpha_composite(im, (c * 96, r * 64))
V.save(OUT + "vacas_furgoneta.png")

prev = Image.new("RGBA", (128 + 8 + 128 + 8 + 96, 256), (70, 66, 60, 255))
prev.alpha_composite(sheet, (0, 0)); prev.alpha_composite(S2, (136, 0)); prev.alpha_composite(im, (272, 0))
prev.resize((prev.width * 3, prev.height * 3), Image.NEAREST).save("atlas/muebles.png")
print("ok")
