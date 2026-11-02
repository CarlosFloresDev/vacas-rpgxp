# Mini DSL para generar eventos de RPG Maker XP como JSON para el MCP.
import re

MAXLEN = 46
WARN = []

# ------------------------------------------------------------ comandos base
def cmd(code, *params):
    return ("C", code, list(params))

from PIL import ImageFont
_FONT = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
MAXW = 428
CODE = re.compile(r"\\[cCvVnN]\[\d+\]")
def _w(s):
    return _FONT.getlength(CODE.sub("", s))
def _wrap(text):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w) if cur else w
        if _w(t) <= MAXW:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def T(text):
    """Show Text. Si empieza por un nombre coloreado (codigo c[n] Nombre: c[0]),
    el nombre va en su propia linea en cada caja. Las lineas que no caben se
    reajustan por anchura real."""
    speaker = None
    m = re.match(r"^(\\c\[\d\][^\\]+:\\c\[0\]) ?", text)
    if m:
        speaker = m.group(1)
        text = text[m.end():]
    lines = text.split("\n")
    if any(_w(l) > MAXW for l in lines):
        # conservar el color abierto al principio si lo hay
        lines = _wrap(" ".join(l.strip() for l in lines))
    for l in lines:
        if _w(l) > MAXW:
            WARN.append(f"no cabe: {l}")
    per = 3 if speaker else 4
    out = []
    for i in range(0, len(lines), per):
        box = ([speaker] if speaker else []) + lines[i:i + per]
        out.append(cmd(101, box[0]))
        for l in box[1:]:
            out.append(cmd(401, l))
    return ("L", out)

def audio(name, vol=80, pitch=100):
    return {"_class": "RPG::AudioFile", "name": name, "volume": vol, "pitch": pitch}

def tone(r, g, b, gray=0):
    return {"_class": "Tone", "red": float(r), "green": float(g), "blue": float(b), "alpha": float(gray)}

def color(r, g, b, a=255):
    return {"_class": "Color", "red": float(r), "green": float(g), "blue": float(b), "alpha": float(a)}

SW = lambda i, on=True: cmd(121, i, i, 0 if on else 1)
VAR = lambda i, val, op=0: cmd(122, i, i, op, 0, val)          # op 0 set,1 add,2 sub
VARRAND = lambda i, lo, hi: cmd(122, i, i, 0, 2, lo, hi)
SS = lambda ch="A", on=True: cmd(123, ch, 0 if on else 1)
GOLD = lambda n: cmd(125, 0 if n >= 0 else 1, 0, abs(n))
ITEM = lambda i, n=1: cmd(126, i, 0 if n >= 0 else 1, 0, abs(n))
WAIT = lambda f: cmd(106, f)
SE = lambda n, v=80, p=100: cmd(250, audio(n, v, p))
BGS = lambda n, v=80, p=100: cmd(245, audio(n, v, p))
BGM = lambda n, v=80, p=100: cmd(241, audio(n, v, p))
STOPBGS = lambda s=2: cmd(246, s)
STOPBGM = lambda s=2: cmd(242, s)
ME = lambda n, v=80, p=100: cmd(249, audio(n, v, p))
TONE = lambda r, g, b, gray=0, f=20: cmd(223, tone(r, g, b, gray), f)
FLASH = lambda r, g, b, a=255, f=10: cmd(224, color(r, g, b, a), f)
SHAKE = lambda p=5, s=5, f=20: cmd(225, p, s, f)
WEATHER = lambda t, p=5, f=0: cmd(236, t, p, f)
FOG = lambda name, op=64, blend=0, zoom=200, sx=0, sy=0, hue=0: cmd(204, 1, name, hue, op, blend, zoom, sx, sy)
TRANSFER = lambda m, x, y, d=0, fade=True: cmd(201, 0, m, x, y, d, 0 if fade else 1)
EVLOC = lambda ev, x, y, d=0: cmd(202, ev, 0, x, y, d)
WAITMOVE = cmd(210)
TRANSP = lambda on=True: cmd(208, 0 if on else 1)
SAVE = cmd(352)
GAMEOVER = cmd(353)
ERASE = cmd(214)
EXIT = cmd(115)
TIMER = lambda sec: cmd(124, 0, sec)
TIMERSTOP = cmd(124, 1)
PARTY_OUT = lambda a: cmd(129, a, 1, 0)
SAVEACCESS = lambda on: cmd(134, 1 if on else 0)
MENUACCESS = lambda on: cmd(135, 1 if on else 0)
COMMON = lambda i: cmd(117, i)

def SCRIPT(code):
    lines = (code + "\ntrue").split("\n")
    out = [cmd(355, lines[0])] + [cmd(655, l) for l in lines[1:]]
    return ("L", out)

def VEN(n):
    return SCRIPT(f"subir_veneno({n})" if n > 0 else f"bajar_veneno({-n})")

# ------------------------------------------------------------ rutas de movimiento
def mv(code, *p):
    return {"_class": "RPG::MoveCommand", "code": code, "parameters": list(p)}
DOWN, LEFT, RIGHT, UP = 1, 2, 3, 4
def route(cmds, repeat=False, skip=True):
    lst = []
    for c in cmds:
        if isinstance(c, int):
            lst.append(mv(c))
        else:
            lst.append(c)
    lst.append(mv(0))
    return {"_class": "RPG::MoveRoute", "repeat": repeat, "skippable": skip, "list": lst}
def steps(direction, n):
    return [direction] * n
TURN = {2: 16, 4: 17, 6: 18, 8: 19}
def turn(d): return mv(TURN[d])
def mwait(f): return mv(15, f)
def mgraphic(name, d=2, pat=0, hue=0): return mv(41, name, hue, d, pat)
STEP_ANIME_ON = mv(33)
STEP_ANIME_OFF = mv(34)
def MOVE(target, cmds, repeat=False, skip=True):
    r = route(cmds, repeat, skip)
    out = [cmd(209, target, r)] + [cmd(509, m) for m in r["list"][:-1]]
    return ("L", out)

# ------------------------------------------------------------ estructuras
def IF(cond, then, els=None):
    return ("IF", cond, then, els)
def CHOICE(opts, branches, cancel=None):
    # cancel: indice (1-based) de la opcion que toma Cancelar; por defecto la ultima
    return ("CH", opts, branches, len(opts) if cancel is None else cancel)
def LOOP(body):
    return ("LOOP", body)
BREAK = cmd(113)

c_sw = lambda i, on=True: [0, i, 0 if on else 1]
c_var = lambda i, val, op=0: [1, i, 0, val, op]   # 0 ==,1 >=,2 <=,3 >,4 <,5 !=
c_ss = lambda ch="A", on=True: [2, ch, 0 if on else 1]
c_timer_le = lambda sec: [3, sec, 1]
c_gold = lambda n: [7, n, 0]
c_item = lambda i: [8, i]
c_script = lambda s: [12, s]

def flatten(items, indent=0):
    out = []
    for it in items:
        if it is None:
            continue
        if isinstance(it, list):
            out += flatten(it, indent)
            continue
        kind = it[0]
        if kind == "C":
            out.append({"code": it[1], "indent": indent, "parameters": it[2]})
        elif kind == "L":
            for c in it[1]:
                out.append({"code": c[1], "indent": indent, "parameters": c[2]})
        elif kind == "IF":
            _, cond, then, els = it
            out.append({"code": 111, "indent": indent, "parameters": cond})
            out += flatten(then, indent + 1)
            out.append({"code": 0, "indent": indent + 1, "parameters": []})
            if els is not None:
                out.append({"code": 411, "indent": indent, "parameters": []})
                out += flatten(els, indent + 1)
                out.append({"code": 0, "indent": indent + 1, "parameters": []})
            out.append({"code": 412, "indent": indent, "parameters": []})
        elif kind == "CH":
            _, opts, branches, cancel = it
            out.append({"code": 102, "indent": indent, "parameters": [opts, cancel]})
            for i, (o, b) in enumerate(zip(opts, branches)):
                out.append({"code": 402, "indent": indent, "parameters": [i, o]})
                out += flatten(b, indent + 1)
                out.append({"code": 0, "indent": indent + 1, "parameters": []})
            out.append({"code": 404, "indent": indent, "parameters": []})
        elif kind == "LOOP":
            out.append({"code": 112, "indent": indent, "parameters": []})
            out += flatten(it[1], indent + 1)
            out.append({"code": 0, "indent": indent + 1, "parameters": []})
            out.append({"code": 413, "indent": indent, "parameters": []})
        else:
            raise ValueError(it)
    return out

# ------------------------------------------------------------ paginas y eventos
def page(lst=None, sw1=None, sw2=None, var=None, ss=None, char="", d=2, pat=0, hue=0,
         tile=0, opacity=255, blend=0, trigger=0, move_type=0, speed=3, freq=3,
         mroute=None, walk=True, step=False, dirfix=False, through=False, top=False):
    cond = {"_class": "RPG::Event::Page::Condition",
            "switch1_valid": sw1 is not None, "switch2_valid": sw2 is not None,
            "variable_valid": var is not None, "self_switch_valid": ss is not None,
            "switch1_id": sw1 or 1, "switch2_id": sw2 or 1,
            "variable_id": var[0] if var else 1, "variable_value": var[1] if var else 0,
            "self_switch_ch": ss or "A"}
    g = {"_class": "RPG::Event::Page::Graphic", "tile_id": tile, "character_name": char,
         "character_hue": hue, "direction": d, "pattern": pat, "opacity": opacity, "blend_type": blend}
    return {"_class": "RPG::Event::Page", "condition": cond, "graphic": g,
            "move_type": move_type, "move_speed": speed, "move_frequency": freq,
            "move_route": mroute or route([], True, False),
            "walk_anime": walk, "step_anime": step, "direction_fix": dirfix,
            "through": through, "always_on_top": top, "trigger": trigger,
            "list": flatten(lst or [])}

class MapEvents:
    def __init__(self, map_id):
        self.map_id = map_id
        self.events = []
        self.ids = {}
    def add(self, name, x, y, pages):
        self.events.append({"name": name, "x": x, "y": y, "pages": pages})
        self.ids[name] = len(self.events)
        return len(self.events)
    def reserve(self, name):
        """Reserva un id (para referencias cruzadas) - se rellena luego con set()"""
        self.events.append(None)
        self.ids[name] = len(self.events)
        return len(self.events)
    def set(self, name, x, y, pages):
        self.events[self.ids[name] - 1] = {"name": name, "x": x, "y": y, "pages": pages}
    def ops(self, existing_ids):
        b = []
        for i, e in enumerate(self.events):
            assert e is not None, f"evento reservado sin rellenar: {i+1}"
            eid = i + 1
            if eid in existing_ids:
                b.append(["update_map_event", {"mapId": self.map_id, "eventId": eid, "updates": e}])
            else:
                b.append(["create_map_event", {"mapId": self.map_id, **e}])
        return b
