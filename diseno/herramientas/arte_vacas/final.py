import sys; sys.path.insert(0,"D:/descargas/Proyectos personales/Vacas/diseno/herramientas")
import arte_gen as A, os, json
from PIL import Image, ImageChops, ImageEnhance
P="D:/descargas/Proyectos personales/Vacas/"
PICK=json.load(open("picks.json"))
def crop_aspect(im,ar):
    w,h=im.size
    if w/h>ar:
        tw=int(h*ar); return im.crop(((w-tw)//2,0,(w-tw)//2+tw,h))
    th=int(w/ar); return im.crop((0,0,w,th))
def portrait(f): return A.pixelizar(crop_aspect(Image.open(f),240/340),(120,170),(240,340),alpha=True)
def enemy(f): return A.pixelizar(Image.open(f),(160,150),(320,300),alpha=True)
def screamer(f): return A.pixelizar(Image.open(f),(320,240),(640,480),contrast=1.1)
def battleback(f):
    im=Image.open(f).convert("RGB")
    w,h=im.size
    # oscurecer: viñeta con luz mínima central + tinte verde/negro
    import math
    vig=Image.new("L",(w,h)); p=vig.load()
    for y in range(h):
        for x in range(w):
            d=math.hypot((x-w/2)/(w/2),(y-h*0.45)/(h/2)); p[x,y]=int(255*max(0.35,1-d*0.8)**1.1)
    dark=ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.7)).enhance(0.8)
    tint=Image.new("RGB",(w,h),(14,24,14))
    base=Image.composite(dark,tint,vig)
    base=ImageEnhance.Contrast(base).enhance(1.15)
    return A.pixelizar(base,(320,240),(640,480),sharpen=False)
out={}
for k,f in PICK["portraits"].items(): out[f"Graphics/Pictures/retrato_{k}.png"]=portrait(f)
for k,f in PICK["enemies"].items(): out[f"Graphics/Battlers/{k}.png"]=enemy(f)
out["Graphics/Battlers/enemigo_moscas.png"]=Image.open("moscas_final.png").convert("RGBA")
def pad_aspect(im,ar):
    w,h=im.size; tw=int(h*ar)
    bg=im.getpixel((2,2)); c=Image.new("RGB",(tw,h),bg); c.paste(im.convert("RGB"),((tw-w)//2,0)); return c
out["Graphics/Battlers/steven_mente.png"]=A.pixelizar(pad_aspect(Image.open(PICK["stevenm"]),240/340),(120,170),(240,340),alpha=True)
for k,f in PICK["screamers"].items(): out[f"Graphics/Pictures/screamer_{k}.png"]=screamer(f)
for k,f in PICK["bb"].items(): out[f"Graphics/Battlebacks/mente_{k}.png"]=battleback(f)
os.makedirs("out",exist_ok=True)
for rel,im in out.items():
    ph=Image.open(P+"diseno/arte_provisional/"+rel)
    assert im.size==ph.size,(rel,im.size,ph.size)
    im=im.convert(ph.mode)
    d="out/"+rel; os.makedirs(os.path.dirname(d),exist_ok=True); im.save(d)
print(len(out))
