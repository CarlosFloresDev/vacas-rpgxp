"""Retoque CPU de la hoja generada: identidad fija y proporciones de mapa."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
from pathlib import Path
from PIL import Image
BASE=_ROOT/'diseno/fuentes/arte_hd2d'
im=Image.open(BASE/'steven_sheet_grid.png').convert('RGBA')
im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0))
sw,sh=im.width//4,im.height//4
out=Image.new('RGBA',(128,192))
for row in range(4):
    poses=[]
    for col in range(4):
        p=im.crop((col*sw,row*sh,(col+1)*sw,(row+1)*sh))
        poses.append(p.crop(p.getchannel('A').getbbox()))
    base=poses[1]
    width=22 if row in (0,3) else 24
    # Cabeza 16 px y resto 24 px: 2.5 cabezas; conservar silueta original.
    split=round(base.height*.32); waist=round(base.height*.70)
    head=base.crop((0,0,base.width,split)).resize((width,16),Image.Resampling.BOX)
    torso=base.crop((0,split,base.width,waist)).resize((width,14),Image.Resampling.BOX)
    for col,p in enumerate(poses):
        tile=Image.new('RGBA',(32,48)); x=(32-width)//2
        tile.alpha_composite(head,(x,7)); tile.alpha_composite(torso,(x,23))
        legs=p.crop((0,round(p.height*.70),p.width,p.height)).resize((width,10),Image.Resampling.BOX)
        tile.alpha_composite(legs,(x,37))
        out.alpha_composite(tile,(col*32,row*48))
out.save(BASE/'steven_coherente.png')
