#!/usr/bin/env python3
"""Pone música de fondo que baja sola cuando hablas (ducking) y se apaga al final.

  python3 musica.py video.mp4 cancion.mp3 -o con-musica.mp4 [--volumen -20]

--volumen es cuántos dB queda la música bajo tu voz cuando no hablas (por defecto -20; más negativo = más baja).
Usa música con licencia libre para redes (por ejemplo, la biblioteca de audio de YouTube, Mixkit o Pixabay Music).
Requisitos: ffmpeg y ffprobe en el PATH.
"""
import argparse
import shutil
import subprocess
import sys


def main():
    if not shutil.which("ffmpeg"):
        sys.exit("Falta ffmpeg. Instálalo: https://ffmpeg.org/download.html")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("musica")
    ap.add_argument("-o", "--salida", default="con-musica.mp4")
    ap.add_argument("--volumen", type=float, default=-20)
    a = ap.parse_args()
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                a.video], check=True, capture_output=True, text=True).stdout.strip())
    grafo = (f"[1:a]volume={a.volumen}dB,afade=t=in:d=0.5,afade=t=out:st={max(0, dur - 1.5):.2f}:d=1.5[m];"
             "[0:a]asplit=2[voz][clave];"
             "[m][clave]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[mb];"
             "[voz][mb]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", a.video, "-stream_loop", "-1", "-i", a.musica,
                    "-filter_complex", grafo, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "192k", "-t", f"{dur:.3f}", "-movflags", "+faststart", a.salida], check=True)
    print(f"listo: {a.salida}")


if __name__ == "__main__":
    main()
