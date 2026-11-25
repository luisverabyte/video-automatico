#!/usr/bin/env python3
"""Corta silencios y tomas malas, alterna un zoom leve entre cortes y deja el video en vertical 1080x1920.

  python3 cortar.py crudo.mp4 -o cortado.mp4                 # detecta los silencios solo
  python3 cortar.py crudo.mp4 -o cortado.mp4 --ver           # solo muestra los tramos, no corta
  python3 cortar.py crudo.mp4 -o cortado.mp4 --tramos t.txt  # usa tus tramos: una línea "inicio fin" en segundos

Por defecto quita pausas de 0,6 s o más, deja 0,15 s de aire a cada lado de la voz y alterna
el encuadre entre 100 % y 110 % en cada corte (el salto se siente como cambio de cámara, no como error).

Requisitos: ffmpeg y ffprobe en el PATH. Sin dependencias de Python.
"""
import argparse
import re
import shutil
import subprocess
import sys


def duracion(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def silencios(video, umbral_db, pausa):
    err = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", video, "-vn", "-af",
                          f"silencedetect=noise={umbral_db}dB:d={pausa}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(ini, fin + [None] * (len(ini) - len(fin))))


def tramos_de_voz(video, umbral_db, pausa, margen, minimo):
    total = duracion(video)
    tramos, cursor = [], 0.0
    for s_ini, s_fin in silencios(video, umbral_db, pausa):
        if s_ini - cursor > 0:
            tramos.append([cursor, s_ini])
        cursor = s_fin if s_fin is not None else total
    if total - cursor > 0:
        tramos.append([cursor, total])
    con_aire = []
    for a, b in tramos:
        a, b = max(0.0, a - margen), min(total, b + margen)
        if con_aire and a <= con_aire[-1][1]:
            con_aire[-1][1] = b
        else:
            con_aire.append([a, b])
    return [t for t in con_aire if t[1] - t[0] >= minimo]


def leer_tramos(ruta):
    tramos = []
    for linea in open(ruta, encoding="utf-8"):
        linea = linea.split("#")[0].strip()
        if linea:
            a, b = linea.split()[:2]
            tramos.append([float(a), float(b)])
    return tramos


def main():
    for b in ("ffmpeg", "ffprobe"):
        if not shutil.which(b):
            sys.exit("Falta ffmpeg. Instálalo: https://ffmpeg.org/download.html")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-o", "--salida", default="cortado.mp4")
    ap.add_argument("--tramos", help="archivo con 'inicio fin' por línea; si no, se detectan los silencios")
    ap.add_argument("--pausa", type=float, default=0.6, help="silencio mínimo que se quita (s)")
    ap.add_argument("--umbral", type=float, default=-35, help="dB bajo los que se considera silencio")
    ap.add_argument("--margen", type=float, default=0.15, help="aire que queda a cada lado de la voz (s)")
    ap.add_argument("--minimo", type=float, default=0.3, help="tramos más cortos se descartan (s)")
    ap.add_argument("--zoom", type=float, default=1.10, help="zoom de los cortes alternos; 1 = sin zoom")
    ap.add_argument("--ancho", type=int, default=1080)
    ap.add_argument("--alto", type=int, default=1920)
    ap.add_argument("--ver", action="store_true", help="solo lista los tramos")
    a = ap.parse_args()

    tramos = leer_tramos(a.tramos) if a.tramos else tramos_de_voz(a.video, a.umbral, a.pausa, a.margen, a.minimo)
    if not tramos:
        sys.exit("No encontré voz. Prueba con --umbral -45.")
    total = sum(b - a_ for a_, b in tramos)
    print(f"{len(tramos)} tramos, {total:.1f} s de {duracion(a.video):.1f} s")
    for i, (x, y) in enumerate(tramos):
        print(f"{x:8.2f} {y:8.2f}   # tramo {i + 1}")
    if a.ver:
        return

    W, H = a.ancho, a.alto
    # Llena el cuadro vertical sin deformar (recorta lo que sobra) y aplica el zoom alterno.
    base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
    partes, concat = [], ""
    for i, (x, y) in enumerate(tramos):
        z = a.zoom if i % 2 else 1.0
        zoom = "" if z == 1.0 else f",scale=iw*{z}:ih*{z},crop={W}:{H}"
        partes.append(f"[0:v]trim={x}:{y},setpts=PTS-STARTPTS,{base}{zoom}[v{i}];"
                      f"[0:a]atrim={x}:{y},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                      f"afade=t=out:st={max(0, y - x - 0.01):.3f}:d=0.01[a{i}];")
        concat += f"[v{i}][a{i}]"
    grafo = "".join(partes) + f"{concat}concat=n={len(tramos)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", a.video, "-filter_complex", grafo,
                    "-map", "[v]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.salida],
                   check=True)
    print(f"listo: {a.salida}")


if __name__ == "__main__":
    main()
