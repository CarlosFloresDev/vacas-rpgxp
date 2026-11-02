import json, subprocess, sys
import ev
from ev import flatten
import contenido as C
import contenido2 as C2

def existing(map_id):
    out = subprocess.run(["node", "rx.mjs", "get_map_events", json.dumps({"mapId": map_id})],
                         capture_output=True, text=True, encoding="utf-8").stdout
    try:
        return {e["id"] for e in json.loads(out)}
    except Exception:
        print("no pude leer eventos", map_id, out[:200]); sys.exit(1)

ops = []
summary = []
def piso():
    m = C.piso(); C2.extender_piso(m); return m
def escalera():
    m = C.escalera(); C2.extender_escalera(m); return m
for fn in (C.prologo, piso, escalera, C.calle, C2.entrada, C2.vestuario, C2.corrales,
           C2.cadena, C2.camaras, C2.oficina, C2.pasillo):
    m = fn()
    ex = existing(m.map_id)
    if len(ex) > len(m.events):
        print(f"AVISO: mapa {m.map_id} tiene {len(ex)} eventos y el contenido define {len(m.events)}")
    ops += m.ops(ex)
    summary.append((m.map_id, len(m.events), {k: v for k, v in m.ids.items()}))
ce = C.evento_comun_notas()
extra = flatten(C2.notas_acto2())
lst = ce[1]['updates']['list']
lst[-1:-1] = [{'_class': 'RPG::EventCommand', **c} for c in extra]
ops.append(ce)
ops.append(["update_starting_position", {"mapId": 1, "x": 9, "y": 7}])
json.dump(ops, open("b_events.json", "w", encoding="utf-8"), ensure_ascii=False)
for w in ev.WARN:
    print("WARN", w)
for s in summary:
    print("mapa", s[0], "eventos", s[1])
print("ops", len(ops))
json.dump(summary, open("event_ids.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
