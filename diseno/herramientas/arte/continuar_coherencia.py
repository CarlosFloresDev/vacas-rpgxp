"""Cierre incremental: conserva el arte del árbol y corrige sus anclas.

No restaura hojas ni ejecuta la producción histórica completa. Idempotente.
"""
import json,shutil
from PIL import Image
from auditar_coherencia import ROOT, BACK, sha, dump
from aplicar_coherencia import assemble, changes

MANIFEST=ROOT/'diseno/fuentes/coherencia_arte/manifest.json'

def actualizar(rel, im, motivo):
    manifest=json.loads(MANIFEST.read_text(encoding='utf8'))
    p=ROOT/rel
    assert Image.open(p).size==im.size
    if not (BACK/rel).exists():
        (BACK/rel).parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,BACK/rel)
    im.save(p)
    entry=next(x for x in manifest['cambios'] if x['archivo']==rel)
    entry.update(sha256=sha(p),motivo=motivo)
    dump(MANIFEST,manifest)

def preparar_variantes():
    # Las variantes pendientes ya tenían lienzo80, pero dos seguían comprimidas
    # lateralmente por la celda48 de origen. Ajustar solo esas vistas a58x38.
    for name in ('guernsey4','junco','muesca'):
        rel=f'Graphics/Characters/vacas_{name}_80.png'
        im=Image.open(ROOT/rel).convert('RGBA');out=Image.new('RGBA',im.size)
        for i in range(16):
            row,col=divmod(i,4);cell=im.crop((col*80,row*80,(col+1)*80,(row+1)*80))
            b=cell.getchannel('A').getbbox();sprite=cell.crop(b)
            if row in (1,2):sprite=sprite.resize((58,38),Image.Resampling.NEAREST)
            out.alpha_composite(sprite,(col*80+(80-sprite.width)//2,row*80+b[3]-sprite.height))
        actualizar(rel,out,'Variante adulta pendiente de Data: vistas laterales58x38, frontal conservado, NEAREST, mismo lienzo320 y apoyo por celda')

def main():
    for name in ('vaca','vaca_canela','furgoneta','muebles'):
        rel=f'Graphics/Characters/vacas_{name}.png'
        current=Image.open(ROOT/rel).convert('RGBA')
        original=Image.open(BACK/rel).convert('RGBA')
        cw,ch=current.width//4,current.height//4
        out=Image.new('RGBA',current.size)
        for i in range(16):
            row,col=divmod(i,4);box=(col*cw,row*ch,(col+1)*cw,(row+1)*ch)
            cell=current.crop(box)
            b=cell.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
            old=original.crop(box).getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
            assert bool(b)==bool(old),(name,i)
            if b:
                assert b[3]-b[1]<=old[3],(name,i)
                sprite=cell.crop(b)
                out.alpha_composite(sprite,(col*cw+b[0],row*ch+old[3]-sprite.height))
        actualizar(rel,out,'Arte image_gen conservado; ancla inferior exacta del original en cada una de las 16 celdas; sin cambios de escala, paleta ni rejilla')
    # Nueva fuente localizada; no vuelve a ejecutar los demás generadores.
    assemble('laboratorio','Graphics/Characters/vacas_laboratorio.png',[
        (26,58),(30,58),(26,42),(14,14),
        (14,12),(14,12),(24,58),(10,14),
        (30,28),(26,38),(26,44),(12,16),
        (26,52),(24,26),(30,56),(24,36)],64,.9,source_boxes=[
        (0,0,222,445),(228,0,447,445),(467,90,667,445),(685,300,887,445),
        (15,745,215,890),(245,745,445,890),(470,470,730,890),(765,745,887,890),
        (0,1040,222,1310),(240,1010,444,1310),(450,960,668,1310),(730,1140,886,1310),
        (0,1350,222,1774),(240,1480,445,1774),(450,1320,668,1774),(690,1490,887,1774)])
    manifest=json.loads(MANIFEST.read_text(encoding='utf8'))
    for entry in changes:
        manifest['cambios']=[x for x in manifest['cambios'] if x['archivo']!=entry['archivo']]+[entry]
    source=ROOT/'diseno/fuentes/coherencia_arte/laboratorio.png'
    manifest['fuentes']['laboratorio']={'archivo':source.relative_to(ROOT).as_posix(),'sha256':sha(source)}
    dump(MANIFEST,manifest)
    preparar_variantes()
    print('Anclas, laboratorio y variantes adultas corregidas; manifiesto actualizado.')

if __name__=='__main__':main()
