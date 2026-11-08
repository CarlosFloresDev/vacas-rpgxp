import random, math
from PIL import Image, ImageDraw
random.seed(7)
W,H=160,150
m=Image.new("L",(W,H),0); d=ImageDraw.Draw(m)
d.ellipse((36,10,124,138),fill=255)          # cabeza
d.rectangle((60,120,100,148),fill=255)       # cuello
d.ellipse((50,48,76,72),fill=0); d.ellipse((84,48,110,72),fill=0)   # ojos huecos
d.polygon([(78,76),(82,76),(86,96),(74,96)],fill=0)                 # nariz
d.ellipse((58,100,102,124),fill=0)           # boca abierta
mp=m.load()
img=Image.new("RGBA",(W,H),(0,0,0,0)); px=img.load()
DARK=[(10,8,6),(23,17,13),(36,39,31),(53,39,29)]
def fly(x,y):
    c=random.choice(DARK)
    for dx,dy in ((0,0),(1,0),(0,1),(1,1)):
        if 0<=x+dx<W and 0<=y+dy<H: px[x+dx,y+dy]=c+(255,)
    wx=x+random.choice((-1,2)); wy=y+random.choice((-1,0))
    if 0<=wx<W and 0<=wy<H and px[wx,wy][3]==0: px[wx,wy]=(116,116,108,255)
for _ in range(2600):
    x,y=random.randrange(W),random.randrange(H)
    if mp[x,y]: fly(x,y)
# glow en las cavidades: ojos rojos
for (cx,cy) in ((63,60),(97,60)):
    for dx in range(-2,3):
        for dy in range(-1,2):
            px[cx+dx,cy+dy]=(201,69,58,255) if abs(dx)+abs(dy)<3 else (127,23,27,255)
# moscas sueltas alrededor
for _ in range(70):
    a=random.random()*6.28; r=random.uniform(48,70)
    x=int(80+math.cos(a)*r*1.0); y=int(75+math.sin(a)*r*1.05)
    if 0<=x<W-2 and 0<=y<H-2 and not mp[x,y]: fly(x,y)
import sys; sys.path.insert(0,"D:/descargas/Proyectos personales/Vacas/diseno/herramientas")
import arte_gen as A
img=A.contorno(img)
img.resize((320,300),Image.NEAREST).save("moscas_final.png")
