
# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
# Deriva sprites RTP desaturados/sucios para Vacas
from PIL import Image, ImageEnhance
import colorsys
RTP="D:/SteamLibrary/steamapps/common/RPGXP/rtp/Graphics/Characters/"
OUT="D:/descargas/Proyectos personales/Vacas/Graphics/Characters/"
def grim(im, sat=0.45, bright=0.85, tint=(1.0,0.97,0.85)):
    im=im.convert("RGBA")
    a=im.getchannel("A")
    rgb=im.convert("RGB")
    rgb=ImageEnhance.Color(rgb).enhance(sat)
    rgb=ImageEnhance.Brightness(rgb).enhance(bright)
    r,g,b=rgb.split()
    r=r.point(lambda v:min(255,int(v*tint[0]))); g=g.point(lambda v:min(255,int(v*tint[1]))); b=b.point(lambda v:min(255,int(v*tint[2])))
    out=Image.merge("RGB",(r,g,b)).convert("RGBA"); out.putalpha(a); return out
def scale_sheet(im, sx, sy):
    fw,fh=im.width//4, im.height//4
    nw,nh=int(round(fw*sx)), int(round(fh*sy))
    out=Image.new("RGBA",(nw*4,nh*4),(0,0,0,0))
    for r in range(4):
        for c in range(4):
            f=im.crop((c*fw,r*fh,(c+1)*fw,(r+1)*fh)).resize((nw,nh),Image.NEAREST)
            out.alpha_composite(f,(c*nw,r*nh))
    return out
def src(n): return Image.open(RTP+n+".png")
grim(src("107-Civilian07"),0.4,0.85).save(OUT+"vacas_steven.png")
m=grim(src("122-Civilian22"),0.35,0.78,(1.0,0.95,0.78))
scale_sheet(m,1.5,1.4).save(OUT+"vacas_madre.png")
grim(src("151-Animal01"),0.35,0.7,(1.0,0.9,0.75)).save(OUT+"vacas_perro.png")
grim(src("110-Civilian10"),0.4,0.85).save(OUT+"vacas_anselmo.png")
grim(src("119-Civilian19"),0.4,0.85).save(OUT+"vacas_remedios.png")
grim(src("147-Storekeeper01"),0.45,0.85,(1.05,0.95,0.9)).save(OUT+"vacas_carnicero.png")
grim(src("134-Butler01"),0.3,0.8).save(OUT+"vacas_reclutador.png")
grim(src("190-Down02"),0.35,0.8).save(OUT+"vacas_borracho.png")
grim(src("102-Civilian02"),0.35,0.8).save(OUT+"vacas_transeunte.png")
grim(src("186-Bulletin01"),0.4,0.8).save(OUT+"vacas_tablon.png")
grim(src("187-Lorry01"),0.3,0.75).save(OUT+"vacas_furgoneta.png")
grim(src("170-Door01"),0.5,0.75).save(OUT+"vacas_puerta.png")
print("ok")
