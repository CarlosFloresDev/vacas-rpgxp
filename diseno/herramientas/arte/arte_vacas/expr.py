
# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
from chars import *
PICK={"steven":24,"madre":23,"lucy":24,"cripps":22,"dog":23,"guernsey":23}
EX={
"steven_miedo":("steven","young thin man, messy black hair, terrified expression, wide eyes, mouth open in fear, sweating, gray work shirt, pale skin"),
"madre_ira":("madre","large dominant middle-aged woman, hair in a tight bun, mustard yellow housecoat, furious screaming expression, bared teeth, glaring eyes"),
"lucy_susurro":("lucy","young woman, pale blond hair tied up, pale hospital gown, whispering, finger to lips, eyes darting sideways, anxious"),
"cripps_ira":("cripps","burly bald slaughterhouse foreman, furious snarling expression, bared teeth, veins, stained leather apron with blood"),
"dog_miedo":("dog","scruffy mongrel dog head and chest, ears flattened back, scared whining eyes, no human"),
"guernsey_susurro":("guernsey","tan Guernsey cow face, curved horns, one large brown eye looking through a metal grille, mouth slightly open as if whispering, no human"),
}
for k,(c,p) in EX.items():
    init=Image.open(f"raw/{c}_{PICK[c]}.png")
    for s in (71,72,73):
        f=f"raw/ex_{k}_{s}.png"
        if not os.path.exists(f): A.img2img(init,p+STYLE,seed=s,denoise=0.5,lora=0.6,neg=NEG).save(f)
