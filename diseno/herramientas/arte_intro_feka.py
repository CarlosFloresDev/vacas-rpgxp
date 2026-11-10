# -*- coding: utf-8 -*-
"""Genera los graficos de la intro de Feka Studios (Graphics/Pictures/feka_*.png).

Fuente: diseno/marca/feka-logo-transparente.png (2688x1263, hueso sobre alfa).
Reproducible, solo CPU:  python diseno/herramientas/arte_intro_feka.py
"""
import os
from collections import deque
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'diseno', 'marca', 'feka-logo-transparente.png')
OUT = os.path.join(ROOT, 'Graphics', 'Pictures')
HUESO = (0xef, 0xe9, 0xf2)
NEON = (0xff, 0x3d, 0x57)
ANCHO = 360          # ancho del logo en pantalla
MARGEN = 4           # borde transparente para que el remuestreo no corte


def solido(alpha, color):
    """Imagen RGBA de color plano con el alfa dado (bordes limpios)."""
    im = Image.new('RGBA', alpha.size, color + (0,))
    im.putalpha(alpha)
    return im


def componente(alpha, semilla, umbral=8):
    """Mascara L de la componente conexa (la gota suelta) que contiene semilla."""
    w, h = alpha.size
    px = alpha.load()
    mask = Image.new('L', alpha.size, 0)
    mp = mask.load()
    cola = deque([semilla])
    mp[semilla] = 255
    while cola:
        x, y = cola.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and mp[nx, ny] == 0 and px[nx, ny] > umbral:
                mp[nx, ny] = 255
                cola.append((nx, ny))
    return mask


def main():
    src = Image.open(SRC).convert('RGBA')
    alpha = src.split()[3]
    caja = alpha.point(lambda v: 255 if v > 40 else 0).getbbox()
    escala = ANCHO / float(caja[2] - caja[0])

    # --- gota suelta del goteo de la F: se separa para animarla ---
    mask = componente(alpha, (819, 722))
    gcaja = mask.getbbox()
    mask_d = mask.filter(ImageFilter.MaxFilter(5))
    a_gota = Image.composite(alpha, Image.new('L', alpha.size, 0), mask_d)
    a_logo = Image.composite(Image.new('L', alpha.size, 0), alpha, mask_d)

    # --- logo sin gota, 360 px, LANCZOS sobre el alfa (color plano exacto) ---
    alto = int(round((caja[3] - caja[1]) * escala))
    a = a_logo.crop(caja).resize((ANCHO, alto), Image.LANCZOS)
    lienzo = Image.new('L', (ANCHO + 2 * MARGEN, alto + 2 * MARGEN), 0)
    lienzo.paste(a, (MARGEN, MARGEN))
    solido(lienzo, HUESO).save(os.path.join(OUT, 'feka_logo.png'))

    # --- gota: 16x16 centrada ---
    lado = max(gcaja[2] - gcaja[0], gcaja[3] - gcaja[1])
    cx = (gcaja[0] + gcaja[2]) / 2.0
    cy = (gcaja[1] + gcaja[3]) / 2.0
    medio = 16 / escala / 2.0
    rec = tuple(int(round(v)) for v in (cx - medio, cy - medio, cx + medio, cy + medio))
    g = a_gota.crop(rec).resize((16, 16), Image.LANCZOS)
    solido(g, HUESO).save(os.path.join(OUT, 'feka_gota.png'))
    gx = (cx - caja[0]) * escala + MARGEN
    gy = (cy - caja[1]) * escala + MARGEN

    # --- halo de neon rojo (se dibuja en modo aditivo) ---
    w, h = 512, 256
    halo = Image.new('L', (w, h), 0)
    hp = halo.load()
    for y in range(h):
        for x in range(w):
            dx = (x - w / 2.0) / (w / 2.0)
            dy = (y - h / 2.0) / (h / 2.0)
            d = min(1.0, (dx * dx + dy * dy) ** 0.5)
            hp[x, y] = int(150 * (1.0 - d) ** 2.2)
    solido(halo, NEON).save(os.path.join(OUT, 'feka_halo.png'))

    # --- linea de neon bajo el logo (nace en la salpicadura) ---
    S = 4
    lw, lh = 368, 13
    core = Image.new('L', (lw * S, lh * S), 0)
    d = ImageDraw.Draw(core)
    d.rounded_rectangle((4 * S, 6 * S - 3, (lw - 4) * S, 6 * S + 3 + S), radius=S, fill=255)
    core = core.resize((lw, lh), Image.LANCZOS)
    glow = core.filter(ImageFilter.GaussianBlur(2.6)).point(lambda v: min(255, int(v * 1.5)))
    linea = solido(glow, NEON)
    linea.alpha_composite(solido(core, (255, 150, 165)))
    # extremos desvanecidos
    lp = linea.load()
    for x in range(lw):
        k = min(1.0, min(x, lw - 1 - x) / 46.0)
        for y in range(lh):
            r, gg, b, al = lp[x, y]
            lp[x, y] = (r, gg, b, int(al * k))
    linea.save(os.path.join(OUT, 'feka_linea.png'))

    # --- "PRESENTA" con el espaciado ancho de STUDIOS ---
    fuente = None
    for nombre in ('bahnschrift.ttf', 'arialbd.ttf', 'arial.ttf'):
        ruta = os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts', nombre)
        if os.path.exists(ruta):
            fuente = ImageFont.truetype(ruta, 17 * S)
            if nombre == 'bahnschrift.ttf':
                try:
                    fuente.set_variation_by_name('SemiBold Condensed')
                except Exception:
                    pass
            break
    texto, paso = 'PRESENTA', 11 * S
    anchos = [fuente.getlength(c) for c in texto]
    total = int(sum(anchos) + paso * (len(texto) - 1))
    t = Image.new('L', (total + 8 * S, 28 * S), 0)
    d = ImageDraw.Draw(t)
    x = 4 * S
    for c, wc in zip(texto, anchos):
        d.text((x, 4 * S), c, font=fuente, fill=255)
        x += wc + paso
    t = t.resize((t.size[0] // S, t.size[1] // S), Image.LANCZOS)
    solido(t, HUESO).save(os.path.join(OUT, 'feka_presenta.png'))

    print('logo %dx%d  gota en (%.1f, %.1f) del logo  presenta %dx%d'
          % (lienzo.size[0], lienzo.size[1], gx, gy, t.size[0], t.size[1]))


if __name__ == '__main__':
    main()
