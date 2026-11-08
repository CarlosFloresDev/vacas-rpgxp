import sys; sys.path.insert(0,"D:/descargas/Proyectos personales/Vacas/diseno/herramientas")
import arte_gen as A, os, json
from PIL import Image
STYLE=", pixel art portrait, dark horror game character illustration, half body bust, front view, strong dark outlines, flat cel shading, muted sickly brown and olive palette, top-left light, solid flat olive-gray background"
NEG=A.NEG+", photograph, realistic skin, text, logo"
C={
"steven":"young thin man, messy black hair, sunken tired eyes with dark circles, gray work shirt, pale skin, neutral expression",
"madre":"large dominant middle-aged woman, stern hard face, hair in a tight bun, mustard yellow housecoat, cigarette stained yellow light, cruel neutral expression",
"lucy":"young woman, pale blond hair tied up, pale hospital gown, anxious wide eyes, thin, holding an empty glass jar",
"cripps":"burly bald slaughterhouse foreman, thick neck, scarred face, stained leather apron with blood, cold neutral expression",
"dog":"scruffy mongrel dog head and chest, drooping ears, warm brown eyes, lying down, no human",
"guernsey":"tan Guernsey cow face, curved horns, one large brown eye looking through a metal grille, no human",
"benito":"veteran elderly factory worker, gray hair, wrinkled face, worn gray coveralls",
"encarna":"middle-aged woman worker, hair pulled back, white coveralls, tired face",
"rubio":"young man worker, blond hair, dark gloves, white coveralls, sly face",
"chato":"short stocky man worker, wide face, flat nose, dirty coveralls",
"sierra":"worker wearing a protective face mask and hard hat, goggles, coveralls",
"remedios":"elderly woman neighbor, white hair, dark shawl, kind wrinkled face",
"anselmo":"elderly man neighbor, gray mustache, old jacket, tired kind face",
"molina":"butcher with mustache, reddish blood-stained apron, thick arms, bloody cleaver on shoulder",
"borracho":"disheveled drunk man, long coat, red nose, stubble, bleary eyes",
"reclutador":"driver recruiter man, peaked cap, jacket, holding a clipboard folder, shifty smile",
}
os.makedirs("raw",exist_ok=True)
def gen(name,seeds,lora=0.6):
    out=[]
    for s in seeds:
        f=f"raw/{name}_{s}.png"
        if not os.path.exists(f): A.txt2img(C[name]+STYLE,seed=s,lora=lora,neg=NEG).save(f)
        out.append(f)
    return out
def pix(f): 
    q=A.pixelizar(Image.open(f),(120,170),(240,340),alpha=True)
    bg=Image.new("RGBA",q.size,(70,60,70,255)); bg.alpha_composite(q); return bg.convert("RGB")
def sheet(names,seeds,out):
    W=Image.new("RGB",(240*8,340*((len(names)+1)//2)))
    for i,n in enumerate(names):
        for j,f in enumerate(gen(n,seeds)):
            W.paste(pix(f),((i%2)*960+j*240,(i//2)*340))
    W.save(out)
if __name__=="__main__":
    names=list(C); seeds=[21,22,23,24]
    for k in range(0,len(names),8): sheet(names[k:k+8],seeds,f"sheet_{k//8}.png")
