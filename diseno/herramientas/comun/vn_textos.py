"""Selección editorial de retratos para los mensajes de ambos actos."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import re
SPEAKERS={
 'Steven':'steven', 'Madre':'madre','Voz de madre':'madre',
 'Lucy':'lucy','Cripps':'cripps','Cripps (desde lejos)':'cripps',
 'La Guernsey':'guernsey','Voz en la rejilla':'guernsey',
 'Benito':'benito','Encarna':'encarna','El Rubio':'rubio','El Chato':'chato',
 'Obrero de la sierra':'sierra','Doña Remedios':'remedios','Señor Anselmo':'anselmo',
 'Molina':'molina','Borracho':'borracho','Hombre del matadero':'reclutador'}
def vn_metadata(text):
 m=re.match(r'^\\c\[\d\]([^\\]+):\\c\[0\] ?',text)
 name=m[1] if m else ('Steven' if text.startswith('\\c[7]') else '')
 key=SPEAKERS.get(name)
 if not key and ('Perro' in text or 'perro' in text):key='dog'; name='Perro'
 if not key:return '',text
 body=text[m.end():] if m else text
 exp='neutral'
 if key=='madre' and ('!' in body or 'dinero' in body or 'MI ' in body):exp='ira'
 if key=='cripps' and ('!' in body or 'cajón' in body or 'rata' in body):exp='ira'
 if key=='steven' and any(x in body.lower() for x in ['miedo','tiembla','sangre','sueñ','hoy.']):exp='miedo'
 if key in ['lucy','guernsey']:exp='susurro'
 if key=='dog' and ('aparta' in body or 'gime' in body):exp='miedo'
 side='L' if key in ['steven','dog','lucy'] else 'R'
 dim=1 if key in ['madre','cripps','guernsey','lucy'] else 0
 return f'\\P[{key}_{exp}]\\{side}\\D[{dim}]\\NOMBRE[{name}]',body
