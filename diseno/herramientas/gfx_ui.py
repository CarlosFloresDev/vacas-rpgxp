from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import random, os
P = "D:/descargas/Proyectos personales/Vacas/Graphics/"
RTP = "D:/SteamLibrary/steamapps/common/RPGXP/rtp/Graphics/"
for d in ("Titles", "Gameovers", "Windowskins", "Pictures"):
    os.makedirs(P + d, exist_ok=True)
FONT = "C:/Windows/Fonts/"
def font(name, size):
    for n in name:
        try:
            return ImageFont.truetype(FONT + n, size)
        except Exception:
            pass
    return ImageFont.load_default()

rnd = random.Random(7)

# ---- windowskin: oscuro, marron nicotina
ws = Image.open(RTP + "Windowskins/001-Blue01.png").convert("RGBA")
rgb = ws.convert("RGB")
rgb = ImageEnhance.Color(rgb).enhance(0.0)
r, g, b = rgb.split()
r = r.point(lambda v: int(v * 0.62)); g = g.point(lambda v: int(v * 0.52)); b = b.point(lambda v: int(v * 0.40))
out = Image.merge("RGB", (r, g, b)).convert("RGBA"); out.putalpha(ws.getchannel("A"))
# fondo de ventana (128x128 de la izquierda): marron muy oscuro con grano
bg = Image.new("RGBA", (128, 128), (26, 20, 16, 255))
dd = ImageDraw.Draw(bg)
for i in range(1400):
    x, y = rnd.randrange(128), rnd.randrange(128)
    v = rnd.randint(18, 44)
    dd.point((x, y), fill=(v + 6, v, v - 6, 255))
out.paste(bg, (0, 0))
out.save(P + "Windowskins/vacas_ventana.png")

# ---- titulo 640x480
W, H = 640, 480
t = Image.new("RGB", (W, H), (10, 8, 7))
d = ImageDraw.Draw(t)
# resplandor de tele
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([180, 150, 460, 400], fill=(90, 100, 90))
glow = glow.filter(ImageFilter.GaussianBlur(70))
t = Image.blend(t, glow, 0.6)
d = ImageDraw.Draw(t)
# tele pequena en el centro abajo
tx, ty = 270, 250
d.rectangle([tx, ty, tx + 100, ty + 80], fill=(60, 40, 26), outline=(20, 14, 10), width=3)
d.rounded_rectangle([tx + 10, ty + 10, tx + 72, ty + 62], radius=10, fill=(40, 44, 40))
for y in range(ty + 12, ty + 61):
    for x in range(tx + 12, tx + 71):
        v = rnd.randint(40, 200)
        d.point((x, y), fill=(v, v, v))
for yy in range(ty + 14, ty + 60, 4):
    d.line([(tx + 80, yy), (tx + 92, yy)], fill=(30, 20, 14))
d.line([(tx + 40, ty), (tx + 20, ty - 40)], fill=(110, 110, 110), width=2)
d.line([(tx + 60, ty), (tx + 84, ty - 44)], fill=(110, 110, 110), width=2)
d.line([(tx + 10, ty + 80), (tx + 6, ty + 96)], fill=(20, 14, 10), width=3)
d.line([(tx + 90, ty + 80), (tx + 94, ty + 96)], fill=(20, 14, 10), width=3)
# titulo
f = font(["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"], 110)
txt = "VACAS"
bb = d.textbbox((0, 0), txt, font=f)
x = (W - (bb[2] - bb[0])) // 2
d.text((x + 4, 64), txt, font=f, fill=(40, 0, 0))
d.text((x, 60), txt, font=f, fill=(150, 26, 22))
f2 = font(["georgiai.ttf", "timesi.ttf", "arial.ttf"], 22)
sub = "Acto I: El piso"
bb = d.textbbox((0, 0), sub, font=f2)
d.text(((W - (bb[2] - bb[0])) // 2, 186), sub, font=f2, fill=(170, 150, 120))
# grano y lineas de barrido
px = t.load()
for y in range(H):
    dark = 0.86 if y % 2 else 1.0
    for x in range(0, W):
        r_, g_, b_ = px[x, y]
        n = rnd.randint(-10, 10)
        px[x, y] = (max(0, min(255, int(r_ * dark) + n)), max(0, min(255, int(g_ * dark) + n)), max(0, min(255, int(b_ * dark) + n)))
# vineta
vig = Image.new("L", (W, H), 0)
ImageDraw.Draw(vig).ellipse([-120, -100, W + 120, H + 100], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(80))
t = Image.composite(t, Image.new("RGB", (W, H), (0, 0, 0)), vig)
t.save(P + "Titles/vacas_titulo.png")

# ---- game over
g = Image.new("RGB", (W, H), (6, 0, 0))
d = ImageDraw.Draw(g)
f = font(["georgiab.ttf", "timesbd.ttf"], 54)
txt = "La Bestia te ha encontrado."
bb = d.textbbox((0, 0), txt, font=f)
d.text(((W - (bb[2] - bb[0])) // 2, 190), txt, font=f, fill=(140, 20, 18))
f2 = font(["georgiai.ttf", "timesi.ttf"], 22)
s = "El veneno ya no cabe dentro de ti."
bb = d.textbbox((0, 0), s, font=f2)
d.text(((W - (bb[2] - bb[0])) // 2, 270), s, font=f2, fill=(150, 120, 110))
g.save(P + "Gameovers/vacas_gameover.png")
print("ok")
