
# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
from PIL import Image,ImageDraw
import glob,os,sys
root=sys.argv[1]; outp=sys.argv[2]
def L(pat): return sorted(glob.glob(root+pat))
def tile(f,sz):
    im=Image.open(f).convert("RGBA"); bg=Image.new("RGBA",im.size,(70,60,70,255)); bg.alpha_composite(im)
    return bg.convert("RGB").resize(sz,Image.NEAREST)
P=L("/Graphics/Pictures/retrato_*.png")+L("/Graphics/Battlers/steven_mente.png")
S=Image.new("RGB",(1920,2420),(20,16,18)); d=ImageDraw.Draw(S)
x=y=0
for f in P:
    S.paste(tile(f,(240,340)),(x,y)); x+=240
    if x>=1920: x=0;y+=340
y+=340 if x else 0; x=0
for f in L("/Graphics/Battlers/enemigo_*.png"):
    S.paste(tile(f,(320,300)),(x,y)); x+=320
    if x>=1920: x=0;y+=300
S=S.crop((0,0,1920,y+300+0)) if False else S
y2=y+300; x=0
for f in L("/Graphics/Pictures/screamer_*.png"):
    S.paste(tile(f,(320,240)),(x,y2)); x+=320
    if x>=1920: x=0;y2+=240
if x: y2+=240
x=0
for f in L("/Graphics/Battlebacks/mente_*.png"):
    S.paste(tile(f,(320,240)),(x,y2)); x+=320
S.crop((0,0,1920,y2+240)).save(outp)
print(y2+240)
