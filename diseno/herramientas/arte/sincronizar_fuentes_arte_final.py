"""Sincroniza fuentes de instalación y marca los constructores gráficos históricos."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import re,json
from instalar_arte_final import R,A,B,backup
def edit(rel,fn):
 p=R/rel;backup(p);s=p.read_text(encoding='utf-8-sig');p.write_text(fn(s),encoding='utf8')
pairs={18:'turno_noche',19:'res_cuenta',20:'gancho_respira',21:'cripps_matarife',33:'censo_bocas',34:'mesa_exige',35:'rey_sin_rostro',36:'numero_cadena',37:'puerta_muerde'}
for rel in ['diseno/herramientas/actos/acto5/contenido5.py','diseno/herramientas/actos/acto6/contenido6.py']:
 def change(s):
  for n,key in pairs.items():s=re.sub(r'\('+str(n)+r",\s*'[^']+',\s*\d+,\s*'",f"({n},'{key}',0,'",s)
  if rel.endswith(str(_ROOT / 'diseno/herramientas/actos/acto6/contenido6.py')):s=s.replace("'Madre':'madre'","'Madre':'madre_envejecida'")
  return s
 edit(rel,change)
def build(s):
 start=s.index('# --- sustos provisionales:')
 end=s.index("((_ROOT / 'diseno/archivo/lotes/b_acto5.json'))",start)
 return s[:start]+"# Arte final integrado: nunca regenerar los sustos con reencuadres PIL.\nfor n in (12,13):\n    if not (ROOT/'Graphics/Pictures'/('screamer_%d.png'%n)).exists():raise FileNotFoundError('Instalar arte_final antes del Acto V')\n"+s[end:]
edit('diseno/herramientas/actos/acto5/build_acto5.py',build)
edit('diseno/herramientas/actos/acto5/maps5.py',lambda s:s.replace("if __name__ == '__main__':\n    build()","if __name__ == '__main__':\n    if (ROOT/'diseno/fuentes/arte_hd2d/arte_final/manifest.json').exists():\n        raise SystemExit('Constructor PIL historico desactivado. Usar componer_arte_final.py y aplicar_arte_final.mjs.')\n    build()"))
edit('diseno/herramientas/actos/acto6/maps6.py',lambda s:s.replace("if __name__=='__main__':m.build()","if __name__=='__main__':\n    if (m.ROOT/'diseno/fuentes/arte_hd2d/arte_final/manifest.json').exists():\n        raise SystemExit('Constructor PIL historico desactivado. Usar componer_arte_final.py y aplicar_arte_final.mjs.')\n    m.build()"))
notes={
'ACTO_V.md':'> **Arte actualizado (10-11-2026):** enemigos 18–21 con PNG propios y hue=0; sustos 12/13 generados desde sus escenas; utilería image_gen integrada en el tileset 69. Las notas provisionales de la implementación original, conservadas abajo, quedan sustituidas por [AUDITORIA_ARTE.md](AUDITORIA_ARTE.md). No ejecutar el constructor PIL histórico.',
'ACTO_VI.md':'> **Arte actualizado (10-11-2026):** enemigos 33–37 con PNG exclusivos/hue=0; retrato madre_envejecida_neutral asignado solo al VI; Guernsey con rombo propio; trono generado y utilería image_gen en tileset70. Cinemáticas con cuatro placas originales. Perro conserva sus apariciones estáticas: el seguidor entre mapas continúa pendiente. Las notas provisionales originales se conservan como historia, no como estado actual. Ver [auditoría](AUDITORIA_ARTE.md).',
'CINEMATICAS.md':'> **Arte actualizado (10-11-2026):** cine_piso, cine_matadero, cine_ciudad y cine_altar son ahora cuatro placas originales image_gen, adaptadas a640×480. Los renders de mapas de la implementación original se conservaron en el respaldo. No ejecutar b_cine_render.json para reemplazarlas: destruiría el acabado nuevo. Escenas, música, saltos y tiempos no cambian. Fuentes/prompts/manifiesto: arte_hd2d/arte_final/.'
}
for file,note in notes.items():
 edit('diseno/'+file,lambda s,note=note:s.split('\n',1)[0]+'\n\n'+note+'\n'+s.split('\n',1)[1])
edit('diseno/docs/arte/BIBLIA_PERSONAJES.md',lambda s:s+"""
## Producción final de los actos V y VI — 10-11-2026

Fuentes y prompts íntegros: arte_hd2d/arte_final/generaciones.json; manifiesto y parámetros de adaptación en la misma carpeta. image_gen integrado; sin GPU local, sin nuevas ilustraciones PIL. Las rampas adicionales de ropa/piel conservan identidad dentro de las paletas de zona.

- Cripps matarife: misma identidad, rapado/camisa gris/delantal marfil/correas marrones; figura humana física con herramienta de perno, separada de su Sombra.
- Turno de noche: tres uniformes vacíos y seis manos en guantes encadenadas a un reloj de fichar.
- Res que cuenta: cabeza bovina crema/marrón con balanza y anillas de etiquetas, nueva silueta.
- Gancho que respira: gancho articulado y fuelle orgánico, sin canal colgada.
- Censo de las bocas: siete hocicos con etiquetas alrededor de un contador mecánico.
- Mesa que exige: mesa doméstica/mantel mostaza, máscara de madre en silla y manos de yeso; no sustituye a la madre cotidiana.
- Rey sin rostro: Steven, camisa marrón con bolsillo, corona de ganchos, cara en facetas de espejo y cadenas; no reemplaza al Rey del cajón anterior.
- Tu Número en la cadena: etiqueta con ojos sobre camisa de trabajo vacía, jaula y cadena.
- Puerta que muerde: marco industrial, puerta doméstica y dientes de porcelana/pernos; sin figura de Cripps.
- Madre envejecida: conserva cara ancha, moño bajo, bata mostaza y ausencia de joyas; más canas/arrugas y cansancio, retrato exclusivo del VI.
- Guernsey de mapa: canela, rombo crema, ojo castaño y cuernos curvos, ya no vaca canela del fondo. Excepción animal:192×192/celda48×48.
- Madre, Cripps, Muesca y Junco: fuentes originales readaptadas a128×192/celdas32×48; objetos y animales conservan sus excepciones.
- Sustos10/11: nuevos planos de Coro/Pulmón;12: Cripps entre ganchos acercando la mano;13: interior de escondite con reflejo asustado de Steven.
""")
print('Fuentes de eventos sincronizadas; constructores PIL protegidos y documentación actualizada.')

