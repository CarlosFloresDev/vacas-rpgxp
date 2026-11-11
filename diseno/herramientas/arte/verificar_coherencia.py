"""Verifica los contratos reales de sustitución; no altera Data ni scripts."""
import json
import numpy as np
from PIL import Image
from auditar_coherencia import ROOT,BACK,OUT,sha,dump

def main():
    baseline=json.loads((OUT/'auditoria_coherencia_arte_antes.json').read_text(encoding='utf8'))
    initial={a['archivo']:a for a in baseline['archivos']}
    manifest=json.loads((ROOT/'diseno/fuentes/coherencia_arte/manifest.json').read_text(encoding='utf8'))
    checks=[]
    def check(name,ok,details=None):checks.append(dict(prueba=name,ok=bool(ok),detalle=details))
    for entry in manifest['cambios']:
        rel=entry['archivo'];p=ROOT/rel;im=Image.open(p).convert('RGBA')
        check(rel+': hash reproducido',sha(p)==entry['sha256'])
        if rel not in initial:continue
        b=BACK/rel
        check(rel+': respaldo original',b.exists() and sha(b)==initial[rel]['sha256'])
        check(rel+': dimensiones',list(im.size)==initial[rel]['tamano'])
        if '/Characters/' in rel:
            old=Image.open(b).convert('RGBA');w,h=im.width//4,im.height//4
            for i in range(16):
                x,y=i%4*w,i//4*h;box=(x,y,x+w,y+h)
                a=old.crop(box).getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
                z=im.crop(box).getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
                check(f'{rel}: ocupación celda {i}',bool(a)==bool(z))
                # No se fuerza que una lámpara colgante tenga el mismo ancla que una persona.
                if a and z:check(f'{rel}: ancla celda {i}',a[3]==z[3],[a[3],z[3]])
    im=np.array(Image.open(ROOT/'Graphics/Tilesets/acto4_alcantarillas.png').convert('RGBA'))
    before=np.array(Image.open(BACK/'Graphics/Tilesets/acto4_alcantarillas.png').convert('RGBA'))
    mask=np.zeros(im.shape[:2],bool);mask[:32,:64]=True;mask[32:64,224:256]=True
    check('alcantarilla: otros 13 tiles idénticos',np.array_equal(im[~mask],before[~mask]))
    tile=im[:32,:32,:3].astype(float)
    check('suelo: unión horizontal exacta',np.array_equal(tile[:,0],tile[:,-1]))
    check('suelo: unión vertical exacta',np.array_equal(tile[0],tile[-1]))
    # Cada PNG inicial sigue existiendo y conserva tamaño aunque no se haya intervenido.
    for rel,f in initial.items():
        check(rel+': contrato global', (ROOT/rel).exists() and list(Image.open(ROOT/rel).size)==f['tamano'])
    result=dict(comprobaciones=len(checks),fallos=sum(not x['ok'] for x in checks),pruebas=checks,limites='No ejecuta Game.exe ni certifica perspectiva automáticamente. Data se modifica por otra tarea: no se usan hashes globales para atribuir cambios.')
    dump(OUT/'verificacion_coherencia_arte.json',result)
    print(json.dumps({'comprobaciones':len(checks),'fallos':result['fallos']}))
    if result['fallos']:
        for c in checks:
            if not c['ok']:print(c)
        raise SystemExit(1)

if __name__=='__main__':main()
