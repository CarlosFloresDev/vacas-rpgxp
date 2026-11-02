# Base de datos del Acto II: objetos, interruptores y variables con nombre.
import json
SE_BOOK = {"_class": "RPG::AudioFile", "name": "046-Book01", "volume": 80, "pitch": 100}
items = [
    (9, "Tarjeta de fichar", "035-Item04", "Tu tarjeta del matadero. Pone STEPHEN, con PH. (Úsala para leerla.)", True),
    (10, "Registro de reses", "036-Item05", "El libro verde de Cripps. Lo apunta todo. (Úsalo para leerlo.)", True),
    (11, "Plano del desagüe", "035-Item04", "Un plano azul de lo que hay debajo del matadero. (Úsalo para leerlo.)", True),
    (12, "Manguera", "033-Item02", "La manguera grande del pasillo de mantenimiento. Pesa como una serpiente dormida.", False),
    (13, "Nota de Lucy", "035-Item04", "Un papel doblado en cuatro, con letra redonda. (Úsala para leerla.)", True),
]
b = []
for iid, name, icon, desc, readable in items:
    b.append(["update_item", {"itemId": iid, "updates": {
        "name": name, "icon_name": icon, "description": desc,
        "scope": 0, "occasion": 2 if readable else 3, "consumable": False,
        "common_event_id": 1 if readable else 0, "price": 0,
        "recover_hp": 0, "recover_hp_rate": 0, "recover_sp": 0, "recover_sp_rate": 0,
        "animation1_id": 0, "animation2_id": 0, "menu_se": SE_BOOK}}])
switches = {
    21: "BUSQUEDA: tiempo agotado",
    22: "A2: Acto II empezado", 23: "A2: En el matadero (turno)", 24: "A2: Fichado",
    25: "A2: Mono puesto", 26: "A2: Cripps patrulla camaras", 27: "A2: Noche en casa",
    28: "A2: Sueldo entregado", 29: "A2: Cripps patrulla oficina", 30: "A2: Steven escondido",
    31: "A2: Pillado por Cripps", 32: "A2: Registro cogido", 33: "A2: Plano cogido",
    34: "A2: PRIMERA MUERTE hecha", 35: "A2: Obedecio en el cajon", 36: "A2: Se resistio en el cajon",
    37: "A2: Se guardo dinero", 38: "A2: Pacto con la Guernsey", 39: "A2: Lucy conocida",
    40: "A2: Lleva una pieza", 41: "A2: Vaca del fondo en la manga", 42: "A2: Madre le pillo la moneda",
    43: "A2: Tercer turno", 44: "A2: Manguera cogida",
}
variables = {
    7: "A2: Turno (1-3)", 8: "A2: Fase del turno (0-9)", 9: "A2: Sueldo de hoy",
    10: "A2: Sueldo total", 11: "A2: Charlas con la Guernsey", 12: "A2: Resultado minijuego",
    13: "A2: Piezas clasificadas", 14: "A2: Pieza que lleva (1-3)", 15: "Huella (veneno minimo)",
    16: "A2: Veces pillado por Cripps", 17: "A2: Ultima noche con Perro",
}
for k, v in switches.items():
    b.append(["set_switch_name", {"switchId": k, "name": v}])
for k, v in variables.items():
    b.append(["set_variable_name", {"variableId": k, "name": v}])
json.dump(b, open("b_db2.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(b))
