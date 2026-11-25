#!/usr/bin/env python3
"""Subtítulos palabra por palabra, gratis y en tu computadora.

Dos pasos, para que puedas corregir la transcripción antes de quemarla:

  1) python3 subtitulos.py transcribir video.mp4 -o transcripcion.json [--modelo small] [--idioma es] [--guion guion.md]
  2) python3 subtitulos.py quemar video.mp4 transcripcion.json -o final.mp4 [--ds design-system.md] [--fuentes carpeta]

Paso 1 usa faster-whisper (Whisper de OpenAI, corre local y sin costo).
Paso 2 arma un .ass con el estilo de tu design-system.md (sección subtitulos), lo quema con ffmpeg
y deja también un .srt al lado, por si la plataforma pide subir los subtítulos aparte.

Requisitos: ffmpeg en el PATH, Python 3.9+, `pip install faster-whisper pyyaml numpy`.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

# Valores por defecto del formato design-system-v1 (FORMATO-DESIGN-SYSTEM.md).
DEFAULTS = {
    "fuente": "",
    "peso": 800,
    "tamano_px": 64,
    "color": "#FFFFFF",
    "resaltado": "primario",
    "contorno": {"color": "#000000", "grosor_px": 6},
    "caja": False,
    "posicion": "centro",
    "palabras_por_linea": 3,
    "lineas": 1,
    "mayusculas": False,
}
ZONA_DEFAULT = {"x": [120, 960], "y": [270, 1250]}
BASE_W, BASE_H = 1080, 1920
PAUSA_CORTE = 0.5  # segundos de silencio que abren un nuevo bloque de subtítulo


def aviso(msg):
    print(f"[subtitulos] {msg}", file=sys.stderr)


# ---------- design-system.md ----------

def leer_ds(ruta):
    if not ruta:
        return {}
    texto = open(ruta, encoding="utf-8").read()
    m = re.search(r"```ya?ml\s*\n(.*?)```", texto, re.S)
    if not m:
        aviso(f"{ruta} no tiene bloque ```yaml```; uso valores por defecto.")
        return {}
    try:
        import yaml
    except ImportError:
        aviso("Falta pyyaml (pip install pyyaml); uso valores por defecto.")
        return {}
    datos = yaml.safe_load(m.group(1)) or {}
    fmt = datos.get("formato", "")
    if fmt and fmt != "design-system-v1":
        aviso(f"formato {fmt} no es design-system-v1; leo lo que reconozco.")
    return datos


def estilo_desde_ds(ds):
    sub = dict(DEFAULTS)
    sub.update({k: v for k, v in (ds.get("subtitulos") or {}).items() if v not in (None, "")})
    faltan = [k for k in DEFAULTS if k not in (ds.get("subtitulos") or {})]
    if ds and faltan:
        aviso("subtitulos sin " + ", ".join(faltan) + ": uso valores por defecto.")
    color = ds.get("color") or {}
    tipo = ds.get("tipografia") or {}
    video = ds.get("video") or {}
    if not sub.get("fuente"):
        sub["fuente"] = (tipo.get("titulos") or {}).get("familia") or "Arial"
    res = str(sub.get("resaltado", "primario")).strip()
    if res in ("primario", "acento"):
        res = color.get(res) or ("#FFD400" if res == "acento" else "#FFD400")
    sub["resaltado"] = None if res == "ninguno" else res
    sub["zona"] = video.get("zona_segura") or ZONA_DEFAULT
    sub["fondo_caja"] = color.get("superficie") or "#000000"
    return sub


# ---------- fuentes ----------

def bajar_fuente(familia, peso, carpeta):
    """Intenta bajar la fuente de Google Fonts como .ttf. Si no se puede, libass usa una parecida."""
    if not familia or familia.lower() in ("arial", "sans", "sans-serif"):
        return False
    os.makedirs(carpeta, exist_ok=True)
    url = "https://fonts.googleapis.com/css2?family=" + familia.replace(" ", "+") + f":wght@{int(peso)}"
    try:
        # Sin user-agent de navegador, Google Fonts entrega .ttf, que es lo que lee libass.
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
        css = urllib.request.urlopen(req, timeout=20).read().decode()
        ttf = re.search(r"url\((https://[^)]+\.ttf)\)", css)
        if not ttf:
            return False
        destino = os.path.join(carpeta, familia.replace(" ", "") + f"-{int(peso)}.ttf")
        urllib.request.urlretrieve(ttf.group(1), destino)
        aviso(f"fuente {familia} {peso} lista en {destino}")
        return True
    except Exception as e:  # sin red o familia que no está en Google Fonts
        aviso(f"no pude bajar {familia} ({e.__class__.__name__}); pon el .ttf en --fuentes o instálala.")
        return False


# ---------- transcribir ----------

def audio_16k(video):
    import numpy as np
    out = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(out, np.int16).astype(np.float32) / 32768.0


def transcribir(a):
    from faster_whisper import WhisperModel
    prompt = None
    if a.guion:
        texto = open(a.guion, encoding="utf-8").read()
        dichos = re.findall(r'"([^"]{3,})"', texto) or [texto]
        prompt = " ".join(dichos)[:800]  # nombres y palabras raras del guion ayudan a escribirlas bien
    audio = audio_16k(a.video)

    def correr(dispositivo):
        modelo = WhisperModel(a.modelo, device=dispositivo, compute_type="int8")
        segs, info = modelo.transcribe(audio, language=a.idioma, word_timestamps=True,
                                       vad_filter=True, initial_prompt=prompt)
        palabras = []
        for s in segs:  # la transcripción ocurre aquí; un error de GPU sale en este bucle
            for w in s.words or []:
                t = w.word.strip()
                if t:
                    palabras.append({"w": t, "i": round(w.start, 3), "f": round(w.end, 3)})
        return palabras, info

    try:
        palabras, info = correr(a.dispositivo)
    except (RuntimeError, OSError) as e:
        # Tarjeta NVIDIA sin las librerías CUDA (cuBLAS, cuDNN): pasa a CPU, que siempre funciona.
        if a.dispositivo == "cpu":
            raise
        aviso(f"la GPU no está lista ({str(e)[:80]}); sigo con CPU.")
        palabras, info = correr("cpu")
    json.dump({"idioma": info.language, "palabras": palabras,
               "texto": " ".join(p["w"] for p in palabras)},
              open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    aviso(f"{len(palabras)} palabras en {a.salida}. Revísalas contra el guion antes de quemar.")


# ---------- quemar ----------

def ass_color(hexa, alfa=0):
    h = hexa.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alfa:02X}{b}{g}{r}".upper()


def ass_tiempo(t):
    t = max(0, t)
    h, rest = divmod(t, 3600)
    m, s = divmod(rest, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def srt_tiempo(t):
    ms = int(round(max(0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def agrupar(palabras, por_linea, lineas):
    tope = max(1, por_linea * lineas)
    grupos, actual = [], []
    for i, p in enumerate(palabras):
        actual.append(p)
        sig = palabras[i + 1] if i + 1 < len(palabras) else None
        fin_frase = p["w"][-1:] in ".?!…"
        pausa = sig is not None and sig["i"] - p["f"] >= PAUSA_CORTE
        if len(actual) >= tope or fin_frase or pausa or sig is None:
            grupos.append(actual)
            actual = []
    return grupos


def medida_video(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "csv=p=0", video],
                         check=True, capture_output=True, text=True).stdout.strip()
    w, h = out.split(",")[:2]
    return int(w), int(h)


def quemar(a):
    ds = leer_ds(a.ds)
    if not ds:
        aviso("sin design-system.md: estilo por defecto (blanco, contorno negro, 3 palabras, centro).")
    st = estilo_desde_ds(ds)
    w, h = medida_video(a.video)
    esc = w / BASE_W  # todo el estilo está pensado a 1080 de ancho
    tam = round(st["tamano_px"] * esc)
    zy0, zy1 = [v * h / BASE_H for v in st["zona"]["y"]]
    alto_bloque = tam * 1.25 * st["lineas"]
    y = {"arriba": zy0 + alto_bloque / 2,
         "centro": zy0 + 0.65 * (zy1 - zy0),
         "abajo": zy1 - alto_bloque / 2}.get(st["posicion"], zy0 + 0.65 * (zy1 - zy0))
    zx0, zx1 = [v * w / BASE_W for v in st["zona"]["x"]]
    x = (zx0 + zx1) / 2

    fuentes = a.fuentes or os.path.join(os.path.dirname(os.path.abspath(a.salida)), "fuentes")
    bajar_fuente(st["fuente"], st["peso"], fuentes)

    contorno = st.get("contorno") or {}
    borde = round(float(contorno.get("grosor_px", 6)) * esc, 1)
    estilo_borde = 3 if st.get("caja") else 1
    fondo = ass_color(st["fondo_caja"] if st.get("caja") else contorno.get("color", "#000000"),
                      0x30 if st.get("caja") else 0)
    negrita = -1 if int(st["peso"]) >= 600 else 0
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{st['fuente']},{tam},{ass_color(st['color'])},{ass_color(st['color'])},{ass_color(contorno.get('color', '#000000'))},{fondo},{negrita},0,0,0,100,100,0,0,{estilo_borde},{borde},0,5,{int(zx0)},{int(w - zx1)},0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    datos = json.load(open(a.transcripcion, encoding="utf-8"))
    palabras = datos["palabras"]
    if st.get("mayusculas"):
        palabras = [dict(p, w=p["w"].upper()) for p in palabras]
    grupos = agrupar(palabras, int(st["palabras_por_linea"]), int(st["lineas"]))
    por_linea = int(st["palabras_por_linea"])
    resaltado = ass_color(st["resaltado"]) if st["resaltado"] else None
    eventos, srt = [], []
    for gi, g in enumerate(grupos):
        fin_grupo = g[-1]["f"] + 0.25
        if gi + 1 < len(grupos):
            fin_grupo = min(fin_grupo, grupos[gi + 1][0]["i"])
        for k, p in enumerate(g):
            ini = p["i"] if k else g[0]["i"]
            fin = g[k + 1]["i"] if k + 1 < len(g) else fin_grupo
            partes = []
            for j, q in enumerate(g):
                t = q["w"].replace("{", "(").replace("}", ")")
                if j == k and resaltado:
                    t = r"{\c" + resaltado + "}" + t + r"{\c" + ass_color(st["color"]) + "}"
                partes.append(t)
                if j + 1 < len(g):
                    partes.append(r"\N" if (j + 1) % por_linea == 0 else " ")
            texto = "".join(partes).replace(r" \N ", r"\N")
            eventos.append(f"Dialogue: 0,{ass_tiempo(ini)},{ass_tiempo(fin)},Sub,,0,0,0,,"
                           + r"{\an5\pos(" + f"{x:.0f},{y:.0f}" + ")}" + texto)
        srt.append(f"{gi + 1}\n{srt_tiempo(g[0]['i'])} --> {srt_tiempo(fin_grupo)}\n"
                   + " ".join(q["w"] for q in g) + "\n")

    base = os.path.splitext(a.salida)[0]
    ruta_ass, ruta_srt = base + ".ass", base + ".srt"
    open(ruta_ass, "w", encoding="utf-8").write(cab + "\n".join(eventos) + "\n")
    open(ruta_srt, "w", encoding="utf-8").write("\n".join(srt))
    aviso(f"{len(grupos)} bloques -> {ruta_ass} y {ruta_srt}")

    def esc_filtro(r):
        return r.replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
    filtro = f"ass='{esc_filtro(ruta_ass)}'"
    if os.path.isdir(fuentes):
        filtro += f":fontsdir='{esc_filtro(fuentes)}'"
    cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", a.video, "-vf", filtro,
           "-c:v", "libx264", "-crf", str(a.crf), "-preset", "medium", "-pix_fmt", "yuv420p",
           "-c:a", "copy", "-movflags", "+faststart", a.salida]
    subprocess.run(cmd, check=True)
    aviso(f"listo: {a.salida}")


def main():
    if not shutil.which("ffmpeg"):
        sys.exit("Falta ffmpeg. Instálalo: https://ffmpeg.org/download.html")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="paso", required=True)
    t = sp.add_parser("transcribir", help="video -> transcripcion.json con tiempos por palabra")
    t.add_argument("video")
    t.add_argument("-o", "--salida", default="transcripcion.json")
    t.add_argument("--modelo", default="small", help="tiny | base | small | medium | large-v3 | turbo")
    t.add_argument("--idioma", default="es")
    t.add_argument("--guion", help="guion .md: sus palabras ayudan a escribir bien nombres propios")
    t.add_argument("--dispositivo", default="auto", help="auto | cpu | cuda (auto usa GPU si está lista y si no, CPU)")
    q = sp.add_parser("quemar", help="video + transcripcion.json -> video con subtítulos")
    q.add_argument("video")
    q.add_argument("transcripcion")
    q.add_argument("-o", "--salida", default="final.mp4")
    q.add_argument("--ds", help="ruta a design-system.md")
    q.add_argument("--fuentes", help="carpeta con los .ttf de la fuente de subtítulos")
    q.add_argument("--crf", type=int, default=18)
    a = ap.parse_args()
    transcribir(a) if a.paso == "transcribir" else quemar(a)


if __name__ == "__main__":
    main()
