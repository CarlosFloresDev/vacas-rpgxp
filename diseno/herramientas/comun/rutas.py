"""Raíz del proyecto e importaciones compartidas para herramientas históricas."""
from pathlib import Path
import sys

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Game.rxproj').is_file())
HERRAMIENTAS = ROOT / 'diseno/herramientas'

def preparar_imports():
    """Expone módulos comunes y de actos sin ejecutarlos ni cambiar el cwd."""
    folders = [HERRAMIENTAS/'comun', HERRAMIENTAS/'arte', HERRAMIENTAS/'audio']
    folders += sorted((HERRAMIENTAS/'actos').glob('acto*'))
    for folder in folders:
        value = str(folder)
        if value not in sys.path:
            sys.path.append(value)

def herramienta(nombre):
    matches = list(HERRAMIENTAS.rglob(nombre))
    if len(matches) != 1:
        raise ValueError('Nombre de herramienta ambiguo o ausente: '+nombre)
    return matches[0]
