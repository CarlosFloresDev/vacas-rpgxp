"""Extrae fuentes vigentes del inventario sin instalar ni alterar Scripts.rxdata."""
from pathlib import Path
import json, re
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Game.rxproj').exists())
SCRIPTS=ROOT/'diseno/scripts'
DESCRIPCIONES=[
 'Constantes, estado y comandos de eventos del juego.',
 'Efectos y presentación del veneno y la cordura.',
 'Menú, estado y objetos del jugador.',
 'Título, derrota, pantallas y entradas de prueba.',
 'Turnos, tareas y progreso del matadero.',
 'Diálogos, retratos y presentación de novela visual.',
 'Eventos y pruebas del mundo mental.',
 'Accesos y correcciones de tránsito entre mapas.',
 'Progreso, diálogos y pruebas del Acto III (Lucy).',
 'Máscaras de luz de los mapas 1 a 16.',
 'Progreso, combate y pruebas del Acto IV (BajoCiudad).',
 'Interfaz, configuración, audio, HUD, combate y guardado.',
 'Presentación inicial de la marca Feka.',
 'Progreso y pruebas del Acto V (La matanza).',
 'Progreso, finales y pruebas del Acto VI (Reydios).',
 'Cinemáticas, transiciones y omisión de escenas.'
]

def actualizar():
    snapshot=json.loads((ROOT/'diseno/verificaciones/inventario/snapshot.json').read_text(encoding='utf8'))
    rows=[s for s in snapshot['Scripts'] if s['name'].startswith('Vacas_')]
    files=sorted(SCRIPTS.glob('*.rb'))
    assert len(rows)==len(files)==16
    manifest=[];archived=[]
    # Conserva las copias antiguas si estaban desincronizadas; son antecedentes útiles.
    for p,s,description in zip(files,rows,DESCRIPCIONES):
        code=s['code'];old=p.read_text(encoding='utf-8-sig')
        if old!=code and not old.startswith('# === VACAS: FUENTE VIGENTE ==='):
            dst=ROOT/'diseno/archivo/scripts_anteriores'/p.name
            dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(old,encoding='utf8');archived.append(p.name)
        switches=sorted(set(re.findall(r'\bSW_[A-Z0-9_]+\b',code)))
        variables=sorted(set(re.findall(r'\bVAR_[A-Z0-9_]+\b',code)))
        switch_ids=sorted(set(re.findall(r'\$game_switches\[(\d+)\]',code)),key=int)
        variable_ids=sorted(set(re.findall(r'\$game_variables\[(\d+)\]',code)),key=int)
        header=['# === VACAS: FUENTE VIGENTE ===',
                '# Script: '+s['name']+' | posición en Scripts.rxdata: '+str(s['index'])+' (base 0)',
                '# Función: '+description,
                '# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.',
                '# Switches simbólicos: '+(', '.join(switches) or 'ninguno'),
                '# Switches con ID literal: '+(', '.join(switch_ids) or 'ninguno'),
                '# Variables simbólicas: '+(', '.join(variables) or 'ninguna'),
                '# Variables con ID literal: '+(', '.join(variable_ids) or 'ninguna'),
                '# Los índices calculados y rangos se describen en el código y en docs/sistemas/.',
                '# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).',
                '# === FIN CABECERA ===','']
        p.write_text('\n'.join(header)+code,encoding='utf8',newline='')
        manifest.append({'file':p.relative_to(ROOT).as_posix(),'name':s['name'],'index':s['index']})
    (SCRIPTS/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    print('Fuentes sincronizadas:',len(manifest),'; antecedentes archivados:',archived)

if __name__=='__main__':actualizar()
