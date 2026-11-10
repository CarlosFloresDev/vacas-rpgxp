"""Instala solo arte image_gen y readapta fuentes aprobadas; respaldo inmutable por ruta."""
import json,shutil,hashlib
from pathlib import Path
from PIL import Image
from adaptar_arte import adapt, PALETTES
# Rampas adicionales autorizadas por ESTILO_ARTE: piel, ropa e iluminaci?n.
MATERIALES=["#211C1E","#393132","#594B42","#71634B","#8B674A","#AA7656","#927461","#D2B996","#C69878","#946A55","#E4C4A0","#C19A75","#444B50","#77848A","#A6B8BE","#D0D2C2","#A18A59","#D1BA7B","#E8D9AA","#D4C6AA","#694139","#B7AF91","#9B9B8D","#B4AB90","#2B241F","#4B3D31","#6B5440","#8B7050"]
for zone in PALETTES: PALETTES[zone]=list(dict.fromkeys(PALETTES[zone]+MATERIALES))
R=Path(__file__).resolve().parents[2]
A=R/'diseno/arte_hd2d/arte_final'
B=R/'diseno/respaldos/antes_arte_final'
def backup(p):
 p=Path(p);dst=B/p.relative_to(R)
 if p.exists() and not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
def write_image(p,im):
 backup(p);p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
def run():
 specs=[]
 for key,zone in [('turno_noche','matadero'),('res_cuenta','matadero'),('gancho_respira','matadero'),('cripps_matarife','matadero'),('censo_bocas','alcantarillas'),('mesa_exige','piso'),('rey_sin_rostro','alcantarillas'),('numero_cadena','alcantarillas'),('puerta_muerde','alcantarillas')]:
  specs.append(dict(source=f'diseno/arte_hd2d/arte_final/{key}_fuente.png',destination=f'Graphics/Battlers/enemigo_{key}.png',type='battler',size='320x300',max_height=300,padding=4,resample='box',alpha_threshold=128,zone=zone))
 for n in (10,11,12,13):
  specs.append(dict(source=f'diseno/arte_hd2d/arte_final/screamer_{n}_fuente.png',destination=f'Graphics/Pictures/screamer_{n}.png',type='picture',size='640x480',resample='box',zone_direction='alcantarillas' if n<12 else 'matadero'))
 specs.append(dict(source='diseno/arte_hd2d/arte_final/madre_envejecida_edit_fuente.png',expression_base='Graphics/Pictures/retrato_madre_neutral.png',expression_polygon=[[0.29,0.25],[0.70,0.25],[0.80,0.43],[0.76,0.56],[0.63,0.65],[0.35,0.65],[0.18,0.49]],expression_feather=1.5,preserve_canvas=True,destination='Graphics/Pictures/retrato_madre_envejecida_neutral.png',type='retrato',size='240x340',padding=4,resample='box',alpha_threshold=128))
 for key,zone in [('cine_piso','piso'),('cine_matadero','matadero'),('cine_ciudad','alcantarillas'),('cine_altar','alcantarillas')]:
  specs.append(dict(source=f'diseno/arte_hd2d/arte_final/{key}_fuente.png',destination=f'Graphics/Pictures/{key}.png',type='picture',size='640x480',resample='box',zone_direction=zone))
 if (A/'guernsey_fuente.png').exists():
  specs.append(dict(source='diseno/arte_hd2d/arte_final/guernsey_fuente.png',destination='Graphics/Characters/vacas_guernsey4.png',type='character',cell='48x48',padding=2,resample='box',alpha_threshold=128,pad_grid=True))
 # Hojas humanas conservan fuentes/poses aprobadas; nuevo lienzo estándar 32x48.
 for key in ('madre','cripps'):
  old=json.loads((R/f'diseno/arte_hd2d/lote_{key}.json').read_text(encoding='utf8'))['assets']
  a=next(x.copy() for x in old if x['type']=='character');a.update(cell='32x48',padding=2);specs.append(a)
 specs.append(dict(source='diseno/arte_hd2d/arte_final/niebla_fuente.png',destination='Graphics/Fogs/002-Clouds01.png',type='picture',size='256x256',preserve_alpha=True,resample='box',zone='alcantarillas'))
 results=[(s,*adapt(s)) for s in specs]
 for spec,p,im in results:write_image(p,im)
 manifest=dict(generator='image_gen integrado, fuentes/prompts en generaciones.json. Adaptación CPU mediante adaptar_arte.py, sin dithering ni dibujos PIL nuevos.',assets=specs,additional_material_ramps=MATERIALES,notes=['Retrato conserva rampas ilustradas de identidad; la paleta piso se dirige en prompt sin cuantización estricta que borre rasgos.','Los battlers nuevos tienen nombres propios; las visiones I/II se preservan.','Hojas humanas normalizadas a128x192; Guernsey conserva excepción animal192x192.'])
 (A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
 print('Instalados',len(results),'PNG')
if __name__=='__main__':run()

