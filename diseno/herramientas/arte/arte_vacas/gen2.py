
# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import sys; sys.path.insert(0, str(_tools / 'arte'))
import arte_gen as A, os
os.makedirs("raw2",exist_ok=True)
NEG=A.NEG+", photograph, text, logo, cute"
EN=", pixel art horror game monster battler, front view, centered, full creature, strong dark outlines, flat cel shading, grotesque gore, muted sickly olive brown palette with deep red blood, solid flat olive-gray background"
ENEM={
"vaca":"floating severed cow head, long red tongue hanging down like a ribbon, bulging bloodshot eyes, blood dripping",
"madre":"empty mustard yellow housecoat floating, cracked plaster face with fissures, huge oversized pale hands",
"tunel":"long faceless elongated worm-like creature made of pipe and slime, tiny glowing eyes at the bottom of a dark conduit",
"sombra_cripps":"tall dark hulking silhouette of a man deformed by meat hooks piercing his body, chains, dripping blood",
"moscas":"swarm of hundreds of black flies forming the shape of a human face",
"guernsey":"ghostly tan cow made of smoke, horns made of rusty pipes, hollow glowing eyes",
"canal":"hanging split carcass on a meat hook, ribs like prison bars, exposed viscera, dripping blood",
"televisor":"1950s television set with faces of static and screaming mouths on the screen, tangled cables, blood",
"rey":"pale gaunt thin man crowned with meat hooks, torn butcher apron, bloody, hollow dark eyes, executioner king",
}
SC=", pixel art horror jump scare, extreme close up, centered, high contrast, dark black background, deep red blood, sickly yellow light, strong dark outlines, flat cel shading, grotesque"
SCR={
1:"huge bloodshot eye of a stern furious old woman seen through a cracked mirror, deep wrinkles, nicotine yellow light",
2:"1950s television family of four faces made of static with wide black screaming mouths, red glow",
3:"huge wet cow snout and bloodshot eye pressed against dirty glass, foam, dark truck cabin",
4:"human face with no features, replaced by a gaping dark drain hole with rusty grate, blood seeping",
5:"single huge brown cow eye behind metal grille bars, blood vessels, dark",
6:"huge shadow of a bald giant man between hanging meat hooks and carcasses, only glowing eyes, harsh backlight, blood",
7:"pale gaunt young man reflection wearing a crown of meat hooks, blood running down his face, screaming",
}
BB=", pixel art game battle background, no characters, one-point perspective, oppressive, dark green and black shadows, one faint light at the center, muted palette, flat shading"
BBS={
"piso":"dark apartment corridor with peeling wallpaper, flickering tv glow at the end, stained floor",
"matadero":"slaughterhouse hall with rail of hanging carcasses, tiled walls, blood on the floor",
"tunel":"damp concrete sewer tunnel, rusty pipes, drain, mold, dripping slime",
}
def go(path,p,w,h,s,lora):
    if not os.path.exists(path): A.txt2img(p,w=w,h=h,seed=s,lora=lora,neg=NEG).save(path)
if __name__=="__main__":
    for k,v in ENEM.items():
        for s in (31,32,33): go(f"raw2/en_{k}_{s}.png",v+EN,512,480,s,0.6)
    for k,v in SCR.items():
        for s in (41,42,43): go(f"raw2/sc_{k}_{s}.png",v+SC,640,480,s,0.5)
    for k,v in BBS.items():
        for s in (51,52): go(f"raw2/bb_{k}_{s}.png",v+BB,640,480,s,0.5)
    go("raw2/stevenm_61.png","full body young thin man standing, messy black hair, gray work shirt, trousers, holding a rusty pipe, scared"+EN,512,704,61,0.6)
    go("raw2/stevenm_62.png","full body young thin man standing, messy black hair, gray work shirt, trousers, holding a rusty pipe, scared"+EN,512,704,62,0.6)
