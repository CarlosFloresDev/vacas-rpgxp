"""Cliente ComfyUI para el arte de Vacas (txt2img / img2img) + postproceso pixel art.
Todo en D:. Requiere el servidor en http://127.0.0.1:8188.
Uso desde Python: import arte_gen as A; A.txt2img(...), A.img2img(...), A.pixelizar(...)
"""
import io, json, time, uuid, urllib.request
from PIL import Image, ImageFilter, ImageDraw

SERVER = "http://127.0.0.1:8188"
CKPT = "v1-5-pruned-emaonly-fp16.safetensors"
LORA = "pixel-art-lora-sd15.safetensors"

# Paleta única de Vacas: amarillos/marrones/verdes enfermizos, rojos sangre, grises sucios.
PALETTE = [
    "0A0806", "17110D", "241A14", "35271D", "4A3626", "654B33", "86663F", "A98A52",  # marrones
    "C9B073", "E3D49A", "F3EBC8",                                                    # amarillos/hueso
    "11160F", "1E2A1B", "2E3F27", "465A33", "6A7A43", "8E9A5C",                      # verdes enfermizos
    "1C0507", "3A0A0E", "5C1015", "7F171B", "A3262A", "C9453A",                      # sangre
    "2A2B2A", "4A4B47", "74746C", "A3A298", "C9C5B4",                                # grises sucios
    "6E5A66", "8E7A6E",                                                              # carne pálida/malva
]

NEG = ("blurry, smooth gradient, soft, photo, 3d render, realistic, text, watermark, signature, frame, border, "
       "deformed, extra fingers, extra limbs, extra eyes, cropped, lowres, jpeg artifacts, cartoon, cute, anime, "
       "bright colors, neon, oversaturated, multiple people")


def _post(path, data, headers):
    req = urllib.request.Request(SERVER + path, data=data, headers=headers)
    return json.loads(urllib.request.urlopen(req).read())


def upload(img):
    buf = io.BytesIO(); img.convert("RGB").save(buf, "PNG")
    b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"v_{b[:8]}.png\"\r\n"
            f"Content-Type: image/png\r\n\r\n").encode() + buf.getvalue() + f"\r\n--{b}--\r\n".encode()
    return _post("/upload/image", body, {"Content-Type": f"multipart/form-data; boundary={b}"})["name"]


def _wf(prompt, neg, seed, steps, cfg, lora, w=None, h=None, image=None, denoise=1.0):
    wf = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "2": {"class_type": "LoraLoader", "inputs": {"model": ["1", 0], "clip": ["1", 1], "lora_name": LORA,
              "strength_model": lora, "strength_clip": lora}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 1], "text": prompt}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 1], "text": neg}},
    }
    if image is None:
        wf["5"] = {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}}
    else:
        wf["10"] = {"class_type": "LoadImage", "inputs": {"image": image}}
        wf["5"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["10", 0], "vae": ["1", 2]}}
    wf["7"] = {"class_type": "KSampler", "inputs": {"model": ["2", 0], "positive": ["3", 0], "negative": ["4", 0],
               "latent_image": ["5", 0], "seed": seed, "steps": steps, "cfg": cfg, "sampler_name": "dpmpp_2m",
               "scheduler": "karras", "denoise": denoise}}
    wf["8"] = {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["1", 2]}}
    wf["9"] = {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": "vacas"}}
    return wf


def _run(wf):
    pid = _post("/prompt", json.dumps({"prompt": wf}).encode(), {"Content-Type": "application/json"})["prompt_id"]
    while True:
        hist = json.loads(urllib.request.urlopen(f"{SERVER}/history/{pid}").read())
        if pid in hist:
            out = hist[pid]["outputs"]["9"]["images"][0]
            url = f"{SERVER}/view?filename={out['filename']}&subfolder={out['subfolder']}&type={out['type']}"
            return Image.open(io.BytesIO(urllib.request.urlopen(url).read())).convert("RGB")
        time.sleep(0.7)


def txt2img(prompt, w=512, h=704, seed=1, steps=28, cfg=7.5, lora=0.8, neg=NEG):
    return _run(_wf(prompt, neg, seed, steps, cfg, lora, w=w, h=h))


def img2img(init, prompt, seed=1, denoise=0.45, steps=28, cfg=7.5, lora=0.8, neg=NEG):
    return _run(_wf(prompt, neg, seed, steps, cfg, lora, image=upload(init), denoise=denoise))


# ---------- postproceso ----------
def _pal_img():
    p = Image.new("P", (1, 1)); flat = []
    for h in PALETTE: flat += [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    p.putpalette(flat + [0] * (768 - len(flat))); return p


def quantizar(rgb, dither=False):
    return rgb.convert("RGB").quantize(palette=_pal_img(),
        dither=Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE).convert("RGB")


def quitar_fondo(img, tol=55, grow=1):
    """Flood-fill desde los bordes sobre el color de fondo dominante; devuelve RGBA."""
    rgb = img.convert("RGB"); w, h = rgb.size
    px = rgb.load()
    border = [px[x, 0] for x in range(w)] + [px[x, h - 1] for x in range(w)] + \
             [px[0, y] for y in range(h)] + [px[w - 1, y] for y in range(h)]
    bg = tuple(sorted(c[i] for c in border)[len(border) // 2] for i in range(3))
    mask = Image.new("L", (w, h), 0); mp = mask.load()
    stack = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    def near(c): return sum(abs(c[i] - bg[i]) for i in range(3)) <= tol * 3
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h or mp[x, y]: continue
        if not near(px[x, y]): continue
        mp[x, y] = 255
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    for _ in range(grow): mask = mask.filter(ImageFilter.MaxFilter(3))
    out = rgb.convert("RGBA"); out.putalpha(Image.eval(mask, lambda v: 255 - v))
    return out


def contorno(rgba, color=(10, 8, 6)):
    """Contorno oscuro de 1 px (en la rejilla pixelada) alrededor de la silueta."""
    a = rgba.split()[3].point(lambda v: 255 if v > 127 else 0)
    ring = a.filter(ImageFilter.MaxFilter(3))
    out = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", rgba.size, color + (255,)), mask=ring)
    base = rgba.copy(); base.putalpha(a)
    out.alpha_composite(base)
    return out


def limpiar_alpha(a, minfrac=0.04):
    """Deja solo los componentes conexos grandes de la máscara (quita motas del fondo)."""
    w, h = a.size; px = a.load(); seen = [[0] * w for _ in range(h)]; comps = []
    for y in range(h):
        for x in range(w):
            if px[x, y] and not seen[y][x]:
                st = [(x, y)]; seen[y][x] = 1; c = []
                while st:
                    cx, cy = st.pop(); c.append((cx, cy))
                    for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1), (cx+1, cy+1), (cx-1, cy-1), (cx+1, cy-1), (cx-1, cy+1)):
                        if 0 <= nx < w and 0 <= ny < h and px[nx, ny] and not seen[ny][nx]:
                            seen[ny][nx] = 1; st.append((nx, ny))
                comps.append(c)
    if not comps: return a
    big = max(len(c) for c in comps); out = Image.new("L", a.size, 0); op = out.load()
    for c in comps:
        if len(c) >= big * minfrac:
            for x, y in c: op[x, y] = 255
    return out


def pixelizar(img, grid, final, alpha=False, out_line=True, sharpen=True, contrast=1.0):
    """img (PIL) -> rejilla `grid` (w,h) -> paleta Vacas -> nearest hasta `final` (w,h).
    alpha=True: quita fondo antes de reducir y devuelve RGBA."""
    from PIL import ImageEnhance
    im = img.convert("RGB")
    if contrast != 1.0: im = ImageEnhance.Contrast(im).enhance(contrast)
    if sharpen: im = im.filter(ImageFilter.UnsharpMask(2, 90, 3))
    a = None
    if alpha:
        rgba = quitar_fondo(im)
        a = rgba.split()[3].resize(grid, Image.BOX).point(lambda v: 255 if v > 140 else 0)
        a = limpiar_alpha(a).filter(ImageFilter.MinFilter(3))
    small = im.resize(grid, Image.BOX)
    small = quantizar(small)
    if alpha:
        small = small.convert("RGBA"); small.putalpha(a)
        if out_line: small = contorno(small)
        return small.resize(final, Image.NEAREST)
    return small.resize(final, Image.NEAREST)
