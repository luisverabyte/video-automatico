---
name: editar-video
description: Edita videos verticales hablando a cámara: corta silencios y tomas repetidas, agrega zoom entre cortes, subtítulos palabra por palabra con el estilo de tu design-system.md, música y marca de agua. Todo gratis con Whisper y ffmpeg. Úsalo cuando tengas un video grabado para editar.
---

# Editar video con subtítulos

Tú grabas; este skill corta, pone subtítulos con tu estilo, agrega música y te entrega el video listo para revisar. Corre en tu computadora con herramientas gratuitas: **Whisper** (transcribe) y **ffmpeg** (edita).

## Dónde funciona

- **Claude Code o Claude Cowork con acceso a una carpeta:** hace todo solo. Es la forma recomendada.
- **Un chat sin acceso a tu computadora** (Claude.ai, ChatGPT, Gemini): no puede editar archivos grandes. Pasa al **modo guía**: te da los comandos para que los pegues en tu terminal, o los pasos para hacerlo en CapCut (sección "Sin terminal").

## Antes de empezar

1. **Tu design-system.md** (formato `design-system-v1`). Lee `subtitulos`, `color`, `tipografia`, `video`, `logo` y la sección **Video**. Si no existe, usa los valores por defecto, dilo en una línea y sugiere el skill `design-system`. Si falta una clave, valor por defecto y aviso; nunca bloquees.
2. **El guion** (opcional, ayuda mucho): sirve para escribir bien los nombres propios y para detectar frases repetidas.
3. **Herramientas**, una sola vez. Comprueba con `ffmpeg -version` y `python3 --version`; si falta algo, instálalo o explícale a la persona cómo:
   - ffmpeg: Mac `brew install ffmpeg`; Windows `winget install ffmpeg`; Linux `sudo apt install ffmpeg`.
   - Python 3.9 o más nuevo, y después `pip install faster-whisper pyyaml numpy`.
   - La primera transcripción baja el modelo de Whisper (unos 500 MB el `small`); después funciona sin internet.
   - En Windows, si `python` abre la Microsoft Store, usa `py` o la ruta completa de Python. Si la PC tiene tarjeta NVIDIA sin CUDA instalado, el script pasa solo a CPU.

Los scripts están en `scripts/` dentro de este skill. Trabaja en una carpeta por video (`videos/<tema>/`) y nunca sobrescribas el crudo.

## Pasos

### 1. Revisar el crudo

`ffprobe` del video: resolución, duración, fps y si es HDR (`color_transfer` `arib-std-b67` o `smpte2084`). Si es HDR, avisa: los colores pueden verse lavados en redes; el paso de corte lo convierte a un video normal, pero conviene grabar en SDR la próxima vez. Si es horizontal, el corte lo recorta a vertical por el centro: avísalo.

### 2. Encontrar qué se queda

```
python3 scripts/subtitulos.py transcribir crudo.mp4 -o crudo.json --guion guion.md
python3 scripts/cortar.py crudo.mp4 --ver > tramos.txt
```

Con la transcripción y los tramos:
- Si una frase se repite, queda **la última toma** (casi siempre es la buena). Quita las anteriores de `tramos.txt`.
- Corta por energía del audio (los tramos de `cortar.py`), no por los tiempos de Whisper: Whisper marca el fin de palabra antes del audio real y en el ruido inventa palabras.
- Quita lo que la persona dijo fuera del guion si suena a error ("espera, de nuevo").
- Respeta los cortes que la persona ya hizo al grabar.
- Nunca cortes pegado a una palabra: deja al menos 0,15 s de aire.
- Si algo dicho cambia el sentido del guion o falta una frase clave, no lo tapes: avisa qué regrabar.

### 3. Cortar

```
python3 scripts/cortar.py crudo.mp4 -o cortado.mp4 --tramos tramos.txt
```

Quita pausas largas, deja el video en 1080x1920 y alterna el encuadre entre 100 % y 110 % en cada corte (el salto se siente como cambio de cámara). Ajusta según `video.ritmo`: `pausado` → `--pausa 0.9 --zoom 1.06`; `rapido` → `--pausa 0.4 --zoom 1.12`. Con `--zoom 1` no hay zoom.

### 4. Transcribir el video cortado y corregir

```
python3 scripts/subtitulos.py transcribir cortado.mp4 -o transcripcion.json --guion guion.md
```

Abre `transcripcion.json` y compara cada palabra con el guion. Corrige la ortografía de nombres, marcas, cifras y términos (cambia solo el texto `"w"`, nunca los tiempos `"i"` y `"f"`). En pantalla va lo que se dijo de verdad: si dijo algo distinto al guion, se respeta lo dicho. Haz esto siempre, Whisper se equivoca con nombres propios.

### 5. Subtítulos

```
python3 scripts/subtitulos.py quemar cortado.mp4 transcripcion.json -o subtitulado.mp4 --ds design-system.md
```

Lee la sección `subtitulos`: fuente (o `tipografia.titulos`), peso, tamaño, color, color de la palabra que se está diciendo (`resaltado`), contorno, caja, posición, palabras por línea, líneas y mayúsculas. Intenta bajar la fuente de Google Fonts; si no está ahí, pide el `.ttf` y pásalo con `--fuentes carpeta/`. Siempre quedan dentro de `video.zona_segura`, lejos de los botones de TikTok, Reels y Shorts.

También deja `subtitulado.srt`: súbelo como subtítulos en YouTube o LinkedIn si la persona prefiere subtítulos que se pueden apagar.

Si `subtitulos.activar` es `false`, salta este paso.

### 6. Nivel 2 (opcional): overlays, B-roll y efectos de sonido

Si la persona quiere más que cortes y subtítulos, o `video.broll` y `video.efectos_sonido` lo piden, lee `estilo-pro.md` antes de planear: continuidad entre la persona y los gráficos, tipos de apoyo por secuencia, zooms, efectos de sonido y control de calidad completo. Haz el plan de recursos, una muestra de 3 s y luego el render. Se compone sobre `cortado.mp4` y **antes** del paso 5 (vuelve a quemar los subtítulos sobre el resultado), para que los subtítulos queden encima y nada los tape. Los overlays no cambian los tiempos, así que `transcripcion.json` sirve igual.

### 7. Música (si `video.musica` no es `ninguna`)

Propón 3 canciones libres para redes que encajen con el tono (biblioteca de audio de YouTube, Mixkit, Pixabay Music) y espera a que elija. Nunca música con derechos de autor ni generada con AI sin que la persona lo pida.

```
python3 scripts/musica.py subtitulado.mp4 cancion.mp3 -o final.mp4 --volumen -20
```

La música baja sola cuando hay voz. `suave` → `--volumen -22`; `protagonista` → `--volumen -14`.

### 8. Marca de agua (si `logo.marca_de_agua` tiene algo)

Texto, con la fuente de títulos y abajo a la derecha dentro de la zona segura:

```
ffmpeg -i final.mp4 -vf "drawtext=text='@usuario':fontfile=fuentes/Fuente.ttf:fontsize=34:fontcolor=white@0.35:x=960-tw:y=1250-th" -c:a copy final-marca.mp4
```

Si es un logo en PNG: `-i logo.png -filter_complex "[1]format=rgba,colorchannelmixer=aa=0.35,scale=140:-1[l];[0][l]overlay=960-w:1250-h"`. Usa `logo.marca_de_agua_opacidad`.

### 9. Revisar antes de entregar

- Saca un cuadro en cada corte y en 3 momentos con subtítulos (`ffmpeg -ss <t> -i final.mp4 -frames:v 1 c.png`) y míralos: nada de texto fuera de la zona segura ni tapando la cara.
- Escucha los cortes: ninguna palabra mordida.
- Volumen: `ffmpeg -i final.mp4 -af loudnorm=print_format=summary -f null -`. Para redes, entre -16 y -14 LUFS integrado; si está muy bajo, normaliza con `loudnorm=I=-14:TP=-1.5:LRA=11`.
- Los subtítulos dicen lo mismo que el audio, palabra por palabra.

### 10. Entregar

El video va como archivo en la carpeta del proyecto (o descargable si la AI lo permite); si estás en Claude con artefactos, puedes sumar una página con el video para verlo en el celular. Mensaje corto con el video final, qué se cortó (tomas repetidas, pausas), qué palabras corregiste en los subtítulos y qué canción entró. Nunca publiques ni programes nada sin que la persona lo pida explícitamente.

## Sin terminal: CapCut (gratis)

Si la persona no puede correr los scripts:

1. Importa el video y usa **Texto > Subtítulos automáticos** en español.
2. Corrige palabra por palabra contra el guion.
3. Aplica el estilo del design system: fuente, tamaño, color, contorno, posición y color de resaltado de palabra (si su versión lo permite).
4. Usa **Eliminar pausas** o corta a mano con margen de aire.
5. Exporta en 1080x1920, 30 fps.

Otra opción de pago: OpusClip, que hace subtítulos y recortes automáticos; carga ahí la fuente y los colores del design system como plantilla de marca.

## Reglas firmes

1. **Revisión antes de publicar:** entrega el MP4 y espera el visto bueno. Nunca publiques ni programes sin un "publícalo".
2. **Errores del crudo:** uno puntual se parcha en el subtítulo con asterisco ("palabra*"). Si hay varios (una palabra que cambia el sentido, frases que faltan, un cierre distinto), no los tapes: avisa con la lista, el parche y qué regrabar.
3. **Edita en copias;** el crudo no se toca y no borres archivos de la persona.
4. **Zona segura:** todo lo que se lee va dentro de `video.zona_segura` (por defecto x 120 a 960, y 270 a 1250 en 1080x1920). Fuera, solo imagen. Verifica estas medidas contra la interfaz actual de cada plataforma.
5. **En pantalla, lo que se dijo de verdad.** Respeta los cortes que la persona hizo al grabar.
6. **Nada generado con AI** (imágenes, voces, música, video) sin aprobación, y nada con derechos de autor.
7. **Calidad:** todo en SDR bt709; si el crudo es 1080p, avisa que es el techo de calidad. Detalle en `estilo-pro.md`.
8. Respeta la sección **Límites** del design system.

---

Kit original "Mis videos automatizados en 3 pasos" de Luis Vera (@luisverabyte) · https://luisverabyte.com · Licencia MIT: puedes usarlo y adaptarlo manteniendo este crédito.
