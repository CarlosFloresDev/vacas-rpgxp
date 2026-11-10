
# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
import json
SE_BOOK = {"_class": "RPG::AudioFile", "name": "046-Book01", "volume": 80, "pitch": 100}
items = [
    (1, "Lata para perro", "032-Item01", "Una lata abollada. El perro de la etiqueta sonríe; Perro nunca sonríe.", False),
    (2, "Abrelatas", "001-Weapon01", "Oxidado. Madre lo guarda como si fuera una llave.", False),
    (3, "Jarabe de madre", "021-Potion01", "Un frasco marrón pegajoso. Huele a regaliz y a algo podrido.", False),
    (4, "Lista de madre", "035-Item04", "Su letra aprieta tanto que rompe el papel. (Úsala para leerla.)", True),
    (5, "Carne picada", "033-Item02", "Medio kilo envuelto en papel de periódico. Ya ha empezado a sangrar.", False),
    (6, "Anuncio del matadero", "035-Item04", "Arrancado del tablón del portal. (Úsalo para leerlo.)", True),
    (7, "Llave del piso", "029-Key01", "La llave de casa. Te la presta. Nunca es tuya.", False),
    (8, "Foto rascada", "036-Item05", "Una foto antigua de un hombre. Alguien le ha borrado la cara. (Úsala.)", True),
]
b = []
for iid, name, icon, desc, readable in items:
    b.append(["update_item", {"itemId": iid, "updates": {
        "name": name, "icon_name": icon, "description": desc,
        "scope": 0, "occasion": 2 if readable else 3, "consumable": False,
        "common_event_id": 1 if readable else 0, "price": 0,
        "recover_hp": 0, "recover_hp_rate": 0, "recover_sp": 0, "recover_sp_rate": 0,
        "animation1_id": 0, "animation2_id": 0, "menu_se": SE_BOOK}}])
b.append(["update_actor", {"actorId": 1, "updates": {"name": "Steven", "character_name": "vacas_steven", "character_hue": 0, "battler_name": ""}}])
switches = {
    1: "Intro vista", 2: "Madre dio las ordenes", 3: "Perro alimentado", 4: "Jarabe entregado",
    5: "Carne comprada", 6: "Carne entregada", 7: "Anuncio leido", 8: "Cena hecha",
    9: "Es de noche", 10: "BUSQUEDA: la Bestia busca", 11: "BUSQUEDA: Steven escondido",
    12: "BUSQUEDA: terminada", 13: "Manana del dia 2", 14: "Contratado en el matadero",
    15: "HUD veneno oculto", 16: "Sin efectos de veneno", 17: "BUSQUEDA: Steven pillado",
    18: "Puerta del piso abierta", 19: "Abrelatas conseguido", 20: "Lata encontrada",
}
variables = {1: "Veneno (0-100)", 2: "Etapa de la historia", 3: "Canal de la tele",
             4: "Veces viendo la tele", 5: "Auxiliar", 6: "Insulto de madre (aleatorio)"}
for k, v in switches.items():
    b.append(["set_switch_name", {"switchId": k, "name": v}])
for k, v in variables.items():
    b.append(["set_variable_name", {"variableId": k, "name": v}])
b.append(["update_game_title", {"title": "Vacas"}])
json.dump(b, open("b_db.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(b))
