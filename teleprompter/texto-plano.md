<!--
Cómo usarlo en cualquier AI (ChatGPT, Gemini, Copilot, Claude sin skills…):
- Lo ideal, una sola vez: guarda tu design-system.md donde tu AI lo recuerde (en Claude o ChatGPT, súbelo a un Proyecto y abre ahí tus chats; en Gemini, conviértelo en un skill). Sube también este texto al Proyecto, o en Gemini guárdalo como otro skill. Así no repites nada en cada video.
- Rápido, para probar: copia todo lo que está debajo de la línea, pégalo como primer mensaje del chat y adjunta tu design-system.md.
-->

----------------------------------------------------------------

A partir de ahora, cuando apruebe un guion, generas su teleprompter siguiendo estas instrucciones. Si no puedes crear archivos, entrégame el HTML completo en un bloque de código para que lo guarde como .html y lo abra en el navegador.

# Teleprompter para grabar un guion

Es un bonus: grabar con teleprompter es opcional. Sirve si te cuesta memorizar o quieres decir el guion palabra por palabra.

Úsalo cuando el creador aprueba un guión de `guion-video` ("apruebo", "vamos a grabar", "dame el teleprompter"); si no está claro que lo aprobó, pregunta. Es solo para grabar: las tomas A-roll/B-roll no aparecen.

## Texto

- Fuente: `guiones/<tema>.md` (o el guion que esté en el chat), solo la columna "Lo que dices", palabra por palabra. Si algo debe corregirse, díselo al creador; no lo cambies en silencio.
- Una sola toma, en el orden del guión, con etiquetas pequeñas de su parte (Gancho, Planteamiento, Detonante, Nudo, Clímax, Desenlace).
- **Loop:** la frase de cierre va al final completa, con las palabras que en edición abren el video resaltadas. Al inicio no se repiten: arranca en lo que sigue a ellas en el gancho.

## Construcción

1. Una sola página HTML autocontenida (CSS y JS en línea), fondo oscuro, texto grande y centrado, con estos controles:
   - avance automático con velocidad ajustable;
   - tamaño de letra;
   - modo espejo (para teleprompter físico con vidrio);
   - botón de volver al inicio y barra espaciadora para pausar;
   - pantalla siempre encendida (Wake Lock API);
   - recordar velocidad y tamaño en `localStorage`, con un prefijo del video en las claves.
   Parte de `plantilla.html` (en la carpeta de este skill): ya trae todo eso. Cambia solo lo marcado `CAMBIA`: `<title>` ("Teleprompter <tema corto>"), encabezado, líneas, el prefijo de `localStorage` y, desde tu design-system.md, los colores del modo oscuro (`color.oscuro.*`, `color.acento`) y la fuente de `tipografia.texto`. Sin design system, deja los valores de la plantilla.
   Si no puedes leer archivos, escribe la página completa con esos mismos controles.
2. Guárdala como `guiones/teleprompter-<tema>.html` y entrégala en el formato nativo de tu AI para leerla al grabar: en Claude, como artefacto; en ChatGPT o Gemini, en Canvas con vista previa; si no hay nada de eso, el HTML completo para guardarlo y abrirlo en el navegador del celular o la tablet. Si ya existe una de ese video, o hay cambios (primero en el guión), actualiza la misma.

## Entrega

Mensaje corto con el enlace o la ruta y, si hay loop, qué palabras del final se cortan para el inicio. No toques el guión (el cierre sigue al final para aprobar la estructura) ni el skill `guion-video`.

---

Kit original "Mis videos automatizados en 3 pasos" de Luis Vera (@luisverabyte) · https://luisverabyte.com · Licencia MIT: puedes usarlo y adaptarlo manteniendo este crédito.
