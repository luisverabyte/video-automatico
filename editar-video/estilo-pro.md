# Edición pro: overlays, B-roll, sonido y control de calidad

Referencia del skill `editar-video` para el nivel 2. Léela cuando el video necesita más que cortes, zoom, subtítulos y música. Todo lo visual sale del design-system.md: `color`, `tipografia`, `formas`, `movimiento`, `video` y `logo`. Donde dice "tu sistema visual", es eso.

Este método nació de editar videos reales con ffmpeg. Las piezas de cada paso (render de HTML con alfa, seguimiento de cara, composición) las arma el asistente con lo que tengas instalado; no hay scripts listos para todo, así que empieza siempre por una muestra de 3 segundos antes de renderizar el video entero.

## Estilo visual

**Continuidad (manda sobre todo).** El creador y los gráficos son narradores; quien mira pasa de uno a otro sin saltos. Toda entrada y salida de B-roll y todo cambio de escena nace de algo en pantalla y vuelve a algo que ya estaba (contenedor que se vuelve el siguiente, toma que se encoge a una forma y vuelve, respuesta que cambia en la misma burbuja), con motion blur real. Principio, no plantilla. Toma a cámara o marco grande que cambia de forma → formas regulares (rectángulo redondeado, píldora).

**Transiciones**
- A-roll → A-roll: salto limpio con margen de silencio, sin `xfade` ni efecto. El dinamismo lo dan los zooms.
- A-roll ↔ B-roll: desde algo en pantalla. Forma probada: un elemento crece hasta ser el B-roll y se encoge de vuelta (render HTML a .mov con alfa), sin desenfoque ni escala de entrada. Semilla según lo que dice: pregunta → burbuja, comparación → 1.ª tarjeta, cifra → tarjeta del dato, post → su tarjeta, concepto → etiqueta o ícono. Transiciones de catálogo solo si no hay elemento del cual nacer. Un salto de A-roll bajo un B-roll no se ve: aprovecharlo.
- Fotos y videos de eventos: Ken Burns por foto, Push, Zoom-through, Mosaic, Card, Iris; `xfade` 0,4 s entre tomas parecidas, 0,15-0,2 s si cambia la escena. La vuelta a cámara arranca en el primer cuadro usado, nunca con un empalme propio del crudo dentro.
- Light Leak: solo encima de capas de vidrio/translúcidas, nunca como corte.

**Movimiento**: nada entra, sale ni queda quieto en seco (entradas suaves, respiración leve, salidas animadas). Un cambio de contenido es un cambio de estado en el mismo render. Un protagonista moviéndose a la vez, amplitudes chicas. Fundidos: overlay 0,2 s, B-roll 0,3 s.

**Zoom**
- Entre tomas: salto 100/110 %.
- Dentro de la toma: zoom continuo a velocidad constante hacia la cara sin sacarla de cuadro (detección de cara con OpenCV/MediaPipe; tope ~1,45). Con trípode, cortes por secciones con zoom alternado de 35-45 % en secciones > 5 s.
- En tomas de énfasis, un zoom de catálogo (Push In lento, Punch-In escalonado, Pull Back Reveal, Camera Shake suave) **reemplaza** al continuo; nunca se suman.
- Con overlay o capa en el fondo: zoom bajo (~1,12) y sin zooms de catálogo.
- Fotos de eventos 12 %, videos 8 %, alternando acercar/alejar.
- Overlays y portada sin zoom, con tiempos sobre el corte ya con zoom.

**Tipos de apoyo** (elegir por secuencia y mezclar). El zoom es el piso, no el plan. El creador sigue siendo el centro: completo o en recuadro ≥ ~70 % del video, nunca dos B-roll seguidos sin volver a él. En videos ≥ 30 s, ≥ 3 tipos de apoyo además del zoom y ninguno que cubra todo el video.

| La secuencia… | Opciones de apoyo |
|---|---|
| Opinión, take, gancho, cierre, chiste a cámara | Su toma + zoom (de catálogo si es énfasis) |
| Nombra empresa, persona, cifra, post o estudio | Overlay con lo real (logo, captura, fuente), capa detrás de él, texto animado |
| Señala con la mano o habla de algo «aquí» | Tarjeta junto a lo que señala o capa en el fondo |
| Muestra una pantalla, chat o documento | Tarjeta baja (cara arriba), B-roll con él en recuadro, chat que se escribe solo |
| Idea con pasos: proceso, comparación, antes/después | Tramo continuo: él se encoge a tarjeta y vuelve |
| Algo que hay que VER (producto, lugar, escena, diagrama) | B-roll a pantalla completa |
| A vs B | Dos tarjetas que cambian de estado o pantalla dividida |
| La palabra que es EL concepto del video | Texto en el fondo detrás de su silueta |

- Overlay arriba: HTML renderizado con alfa y compuesto con ffmpeg, en la franja de overlays.
- Capa en el fondo: tarjetas en la pared **detrás de su silueta** (máscara de segmentación) con paralaje. Máx. 3, nunca sobre la cara, salen ≥ 0,3 s antes de un corte; si cubren más de ~40 % de los cuadros, acortar.
- Tramo continuo: 8-20 s como una composición con su toma como capa, para una idea con pasos. Fronteras en saltos de toma. Nunca el video entero.
- Texto animado por letras: una palabra clave o cifra con movimiento dentro de un overlay o B-roll; un solo punto focal por pantalla.
- B-roll a pantalla completa cuando la secuencia lo pide, o con su cara en recuadro de narrador: su toma se encoge a un recuadro dentro de la zona segura, sin tapar texto ni subtítulos, y vuelve a crecer al salir. Es la forma preferida de pasar a un B-roll largo (> ~4 s). Ninguna imagen < 1 s (salvo la portada).
- Plantillas o librerías de terceros: re-pintarlas con tu sistema visual y hacer una muestra de 3 s antes del primer uso.

**Recap** (experiencia con material propio): intro y cierre a cámara; en el cuerpo, fotos y videos a pantalla completa justo cuando nombra cada parte; overlays arriba con día, nombre y datos que dice. Fotos horizontales o 3:4 enteras sobre un fondo desenfocado de sí mismas.

## Audio

- Nunca cortar pegado a una palabra: hasta 1 s de silencio a cada lado; si el hueco es menor, no cortar ahí. Puntos de corte por energía del audio, no por los tiempos de Whisper (el fin de palabra llega antes del audio real, tras pausa larga el inicio sale 0,3-0,5 s antes, y en ruido inventa palabras).
- Quitar una frase: A = fin real de la última palabra que queda + ~0,2 s; B = inicio de la siguiente − ~0,45 s, ambos < -35 dB.
- Solo se quita: frases que no quiere, silencio inicial (≤ 0,3 s) y final (+ ~0,6 s), y el centro de pausas largas. Micro-pausas se quedan.
- Si tu herramienta de subtítulos recorta pausas sola: entrégale el compuesto con **toda pausa ≤ 0,45 s a -35 dB**, ≥ 0,2 s de silencio a cada lado, y sin fundidos sobre pausas largas.
- Algunos celulares graban con audio que deriva respecto del video: verifica la sincronía; corta con `-ss` sobre el contenedor, nunca con `aresample=async`.

## Efectos de sonido

- **Dónde suenan** (un efecto por evento; nunca dos whooshes a la vez; un click a menos de 0,3 s de otro sonido sobra): whoosh cuando una tarjeta, overlay grande o B-roll entra y sale; click suave al iluminar una opción; pop en una etiqueta; swipe al cambiar de estado; campana al cerrar una idea. Los saltos de A-roll no llevan sonido.
- **Tiempos**: los cues salen del mismo script que genera los overlays, en tiempo del compuesto, para que sonido e imagen se muevan juntos si algo cambia.
- **Fuentes libres, sin IA generativa**: síntesis propia o biblioteca con licencia comercial.
- **Nivel** contra la voz de esa ventana (RMS ~350 ms): whoosh ≈ 8-10 dB bajo la voz, clicks y pops ≈ 10-14 dB bajo el pico local. La mezcla no cambia el pico ni el LUFS integrado de la voz. Un solo mando de volumen general.
- **Mezcla**: voz del corte + efectos → wav → mux sobre el compuesto con `-c:v copy`. Mide el pico por canal.

## Color y calidad

- `ffprobe` de cada crudo: si es 1080p, avisar (techo de calidad); si es HDR (`arib-std-b67`/HLG), convertir a SDR con tonemap.
- Todo en **SDR bt709** (`-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`); la portada también (portada SDR + video HLG = sobresaturado).
- Trabajar al 120 % y bajar a 1080x1920 con lanczos. Compuesto codificado **una vez**: `libx264 -crf 12 -preset slow -tune film -profile:v high -pix_fmt yuv420p` con `-t` = duración exacta.

## Control de calidad completo

Todo pasa antes de mostrar o subir:

- volumen y true peak ≤ -1 dBTP; cuadros congelados o negros; caja de cada overlay contra la zona segura;
- cuadrícula de cuadros en cada transición a B-roll, cada salto de A-roll y los últimos cuadros (sin cuadros de otra toma ni nada sobre la franja de subtítulos);
- una guía de zona segura encima de un cuadro por cada overlay, tarjeta y B-roll (al final de su zoom);
- pausas ≤ 0,45 s a -35 dB y ningún empalme muerde una palabra;
- sincronía del corte con el crudo;
- sonido: voz de la mezcla alineada con la del corte (desfase 0), pico < -1 dBFS por canal, LUFS igual al de la voz sola, cada efecto ≥ 8 dB bajo la voz de su ventana;
- piel y fondo como en el crudo.
Para revisión: MP4 1080x1920, `-crf 21 -preset medium`, aac 128k, `+faststart`; el crf 12 es el master. Para revisar en el celular: 720x1280, crf 26-28, ≤ 15 MB.

## Registro de experimentos

Cada video suma al menos un recurso poco usado o nuevo y no se siente igual al anterior. Lleva `videos/EXPERIMENTOS.md` (recurso, video, resultado), léelo al planear y agrega la fila al entregar.

## Si usas una herramienta externa de subtítulos (OpusClip, Submagic, CapCut)

Opcional: el skill ya quema los subtítulos gratis. Si prefieres una herramienta que cobra por proyecto:

1. **Proyectos que cuestan**: si tu herramienta de subtítulos cobra por proyecto, sube solo la versión final. Un error puntual del crudo se parcha (subtítulo corregido con asterisco: "palabra*"). Con **varios** (palabra que cambia el sentido, frases faltantes, cierre distinto, dato sin salvedad): no subir; avisar con la lista, el parche y qué regrabar.
2. Un proyecto nuevo pierde los ajustes manuales del anterior: avisar antes y juntar todos los cambios en una versión.

3. Sube solo cuando el creador apruebe el compuesto, sin recortes automáticos y con una plantilla de subtítulos hecha con su design system. Si la herramienta recorta pausas sola, entrégale el compuesto con toda pausa ≤ 0,45 s a -35 dB.
4. Corrige el transcript en la herramienta (mismo número de palabras por reemplazo) y revisa: duración igual al compuesto, últimas palabras completas, subtítulos sin tapar overlays y primer cuadro igual a la portada.
