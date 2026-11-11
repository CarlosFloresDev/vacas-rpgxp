"""Adaptación CPU reproducible desde originales respaldados y fuentes image_gen.
Solo escribe Graphics y diseno; conserva tamaño y rejilla de cada reemplazo.
"""
from pathlib import Path
import json, shutil
import numpy as np
from PIL import Image, ImageEnhance
from auditar_coherencia import ROOT, BACK, OUT, sha, dump

SOURCES=ROOT/'diseno/fuentes/coherencia_arte'
GEN=Path('D:/DevTools/codex/generated_images/01a1c8b4-2bd6-77f0-a0d7-d831d888987f')
SOURCE_FILES={
 'furgoneta':'exec-0719e986-8e1c-4f59-a8ba-8dcff3501ee9.png',
 'muebles':'exec-6efe056f-2b2b-4f5f-9f72-0691f117b241.png',
 'suelo':'exec-6b9052a3-ed69-42b0-9a0c-82e419474978.png',
 'vaca':'exec-ab0ea000-5c99-466c-af2c-655dc412396d.png',
 'vaca_canela':'exec-e6e09b76-d498-4c81-8b23-fa28c45ce713.png',
 'titulo':'exec-4077a883-ed80-421b-a8d4-bc90d3412fca.png',
}
changes=[]

def original(rel):
    dest=ROOT/rel; b=BACK/rel
    if not b.exists():
        b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,b)
    return Image.open(b).convert('RGBA')

def save(rel,im,why):
    dest=ROOT/rel
    before=original(rel) if dest.exists() else None
    if before is not None: assert before.size==im.size,(rel,before.size,im.size)
    dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
    changes.append(dict(archivo=rel,motivo=why,tamano=list(im.size),original_sha256=sha(BACK/rel) if before else None,sha256=sha(dest)))

def finish(im,saturation=1,colors=64):
    alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0)
    rgb=ImageEnhance.Color(im.convert('RGB')).enhance(saturation)
    rgb=rgb.quantize(colors=colors,dither=Image.Dither.NONE).convert('RGBA');rgb.putalpha(alpha)
    # RGB cero en transparentes: evita halos en importaciones posteriores.
    a=np.array(rgb);a[a[:,:,3]==0]=0
    return Image.fromarray(a)

def assemble(source,rel,targets,colors=64,sat=.9,source_boxes=None):
    src=Image.open(SOURCES/(source+'.png')).convert('RGBA')
    old=original(rel);out=Image.new('RGBA',old.size)
    cw,ch=old.width//4,old.height//4
    for i,(tw,th) in enumerate(targets):
        col,row=i%4,i//4
        box=source_boxes[i] if source_boxes else (round(col*src.width/4),round(row*src.height/4),round((col+1)*src.width/4),round((row+1)*src.height/4))
        cell=src.crop(box)
        alpha=cell.getchannel('A').point(lambda a:255 if a>=128 else 0);cell.putalpha(alpha)
        bbox=alpha.getbbox();assert bbox,(source,i)
        sprite=cell.crop(bbox)
        # Encajar por celda con NEAREST; ninguna contaminación entre frames.
        ratio=min(tw/sprite.width,th/sprite.height)
        sprite=sprite.resize((max(1,round(sprite.width*ratio)),max(1,round(sprite.height*ratio))),Image.Resampling.NEAREST)
        # XP centra la celda, no su figura. Conservar el suelo de cada índice
        # original evita desplazar pies/ruedas incluso al reducir la silueta.
        oldbox=old.crop((col*cw,row*ch,(col+1)*cw,(row+1)*ch)).getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
        bottom=oldbox[3] if oldbox else ch
        assert sprite.height<=bottom,(rel,i,sprite.height,bottom)
        out.alpha_composite(sprite,(col*cw+(cw-sprite.width)//2,row*ch+bottom-sprite.height))
    save(rel,finish(out,sat,colors),'Regeneración image_gen; recorte por celda, NEAREST, ancla inferior, alpha binario y paleta sin dithering')

def main():
    SOURCES.mkdir(parents=True,exist_ok=True)
    for name,filename in SOURCE_FILES.items():
        dest=SOURCES/(name+'.png')
        if not dest.exists():shutil.copy2(GEN/filename,dest)
    assemble('furgoneta','Graphics/Characters/vacas_furgoneta.png',[(42,58)]*4+[(90,54)]*8+[(42,58)]*4)
    save('Graphics/Titles/vacas_titulo.png',Image.open(SOURCES/'titulo.png').convert('RGB').resize((640,480),Image.Resampling.NEAREST),'Título regenerado: texto dentro de área segura y60..420, lienzo 640x480 conservado')
    assemble('muebles','Graphics/Characters/vacas_muebles.png',[(26,26)]*8+[(30,54),(30,54),(28,52),(28,56),(22,26),(28,48),(28,30),(28,36)])
    for name in ('vaca','vaca_canela'):
        assemble(name,f'Graphics/Characters/vacas_{name}.png',[(29,48)]*4+[(62,38)]*8+[(29,48)]*4,48,.85)
    for name in ('guernsey4','junco','muesca'):
        rel=f'Graphics/Characters/vacas_{name}.png'
        save(rel,finish(original(rel),.78 if name=='guernsey4' else .9,48),'Paleta bovina apagada; misma anatomía, marcas, rejilla y direcciones')
        source=Image.open(ROOT/rel).convert('RGBA');canvas=Image.new('RGBA',(320,320))
        for i in range(16):
            row,col=divmod(i,4);sprite=source.crop((col*48,row*48,(col+1)*48,(row+1)*48));sprite=sprite.crop(sprite.getchannel('A').getbbox())
            tw,th=(29,48) if row in (0,3) else (62,38)
            ratio=min(tw/sprite.width,th/sprite.height);sprite=sprite.resize((round(sprite.width*ratio),round(sprite.height*ratio)),Image.Resampling.NEAREST)
            canvas.alpha_composite(sprite,(col*80+(80-sprite.width)//2,(row+1)*80-sprite.height))
        save(f'Graphics/Characters/vacas_{name}_80.png',canvas,'Variante de escala adulta preparada; NO asignada porque exige cambiar referencias de eventos y tamaño de celda')
    # Las hojas indexadas NO son ciclos de marcha; cada índice es un objeto.
    for name in ('cosas','laboratorio','matadero','alcantarilla'):
        rel=f'Graphics/Characters/vacas_{name}.png'
        save(rel,finish(original(rel),.75 if name=='alcantarilla' else .9,64),'Unificación de rampas y alpha; objetos y anclas conservados por índice')
    # Bordes de tiles y pequeños iconos: eliminar antialias ajeno al plano jugable.
    baseline=json.loads((OUT/'auditoria_coherencia_arte_antes.json').read_text(encoding='utf8'))
    for f in baseline['archivos']:
        rel=f['archivo'];cat=Path(rel).parent.name
        if f['rtp']['hash_identico'] or cat not in ('Tilesets','Autotiles','Icons'):continue
        if not any(w in f['avisos'] for w in ('alpha_parcial_en_pixel_art','saturacion_media_mayor_055')):continue
        save(rel,finish(original(rel),.72 if f['metricas']['saturacion_media']>.55 else 1,128 if cat=='Tilesets' else 64),'Alpha binario en plano jugable; saturación corregida solo donde supera guía')
    # Suelo de alcantarilla: conserva todos los índices y bordes, sin alterar muros/agua.
    rel='Graphics/Tilesets/acto4_alcantarillas.png';im=original(rel)
    tile=Image.open(SOURCES/'suelo.png').convert('RGB').resize((32,32),Image.Resampling.NEAREST)
    a=np.array(tile).astype(float)
    # Emparejar los cuatro bordes de forma simétrica (sin desenfoque).
    for k in range(3):
        weight=(3-k)/6
        left=a[:,k].copy();right=a[:,-1-k].copy()
        a[:,k]=left*(1-weight)+right*weight;a[:,-1-k]=right*(1-weight)+left*weight
        top=a[k].copy();bottom=a[-1-k].copy()
        a[k]=top*(1-weight)+bottom*weight;a[-1-k]=bottom*(1-weight)+top*weight
    tile=Image.fromarray(a.clip(0,255).astype('uint8')).quantize(colors=16,dither=Image.Dither.NONE).convert('RGBA')
    im.paste(tile,(0,0));im.paste(tile,(32,0))
    # El índice 399 es el vacío exterior: su motivo diagonal repetido distraía.
    exterior=ImageEnhance.Brightness(tile.convert('RGB')).enhance(.38).convert('RGBA')
    im.paste(exterior,(224,32))
    save(rel,im,'Tiles 384/385 y 399: suelo y vacío de bajo contraste con bordes enlazados; otros 13 índices intactos')
    # Sustitutos preparados, no asignados. Registros de reserva sin contexto de mapa.
    aliases=[('02','obrero1','benito'),('03','obrero4','chato'),('04','obrero3','encarna'),('05','transeunte','transeunte'),('06','reclutador','reclutador'),('07','lucy','lucy'),('08','remedios','remedios')]
    for aid,char,portrait in aliases:
        for cat,source in [('Characters',f'Graphics/Characters/vacas_{char}.png'),('Battlers',f'diseno/fuentes/arte_hd2d/referencias/{portrait}.png')]:
            dest=f'Graphics/{cat}/vacas_reserva_actor{aid}.png'
            im=Image.open(ROOT/source).convert('RGBA')
            if cat=='Battlers':
                im=im.crop((0,0,im.width//2,im.height))
                im=im.crop(im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox())
                im.thumbnail((220,320),Image.Resampling.NEAREST)
                canvas=Image.new('RGBA',(240,340));canvas.alpha_composite(im,((240-im.width)//2,340-im.height));im=finish(canvas,1,128)
            save(dest,im,'Sustituto civil de reserva preparado desde arte propio; requiere asignación en Actors, sin uso en mapa detectado')
    save('Graphics/Characters/vacas_luz_escalera.png',Image.open(ROOT/'Graphics/Characters/185-Light02.png').convert('RGBA'),'Alias de lámpara existente del proyecto; comprobar procedencia y cambiar referencia del mapa3 evento11')
    for source in ('016-Ice01','024-Support01'):
        im=Image.open(ROOT/f'Graphics/Animations/{source}.png').convert('RGBA')
        canvas=Image.new('RGBA',(960,im.height));canvas.paste(im,(0,0))
        save(f'Graphics/Animations/vacas_rejilla_{source}.png',canvas,'Corrección de geometría preparada con otro nombre: relleno transparente a 960 sin mover celdas 192; conserva arte RTP pendiente')
    dump(SOURCES/'manifest.json',dict(fuentes={k:{'archivo':f'diseno/fuentes/coherencia_arte/{k}.png','sha256':sha(SOURCES/(k+'.png'))} for k in SOURCE_FILES},cambios=changes))
    print(f'{len(changes)} recursos escritos; dimensiones de reemplazo comprobadas')

if __name__=='__main__': main()
