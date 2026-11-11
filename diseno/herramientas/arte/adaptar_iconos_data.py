"""Adapta las dos fuentes image_gen: recorte alfa, NEAREST, paleta y celda24."""
from PIL import Image
from aplicar_coherencia import ROOT, finish
from auditar_coherencia import sha, dump
import json

def main():
    manifest_path=ROOT/'diseno/fuentes/coherencia_arte/manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf8'))
    for name in ('tubo_oxidado','ropa_trabajo'):
        source=ROOT/f'diseno/fuentes/coherencia_arte/data_{name}.png'
        im=Image.open(source).convert('RGBA')
        mask=im.getchannel('A').point(lambda a:255 if a>=128 else 0)
        im.putalpha(mask)
        im=im.crop(mask.getbbox())
        ratio=min(22/im.width,22/im.height)
        im=im.resize((max(1,round(im.width*ratio)),max(1,round(im.height*ratio))),Image.Resampling.NEAREST)
        out=Image.new('RGBA',(24,24))
        out.alpha_composite(im,((24-im.width)//2,(24-im.height)//2))
        out=finish(out,.7,16)
        rel=f'Graphics/Icons/vacas_{name}.png'
        out.save(ROOT/rel)
        manifest['cambios']=[c for c in manifest['cambios'] if c['archivo']!=rel]
        manifest['cambios'].append(dict(archivo=rel,sha256=sha(ROOT/rel),tamano=[24,24],original_sha256=None,motivo='Icono propio image_gen para equipo de Steven; NEAREST, 16 colores, alpha binario'))
        manifest['fuentes']['data_'+name]=dict(archivo=source.relative_to(ROOT).as_posix(),sha256=sha(source))
    dump(manifest_path,manifest)

if __name__=='__main__':main()
