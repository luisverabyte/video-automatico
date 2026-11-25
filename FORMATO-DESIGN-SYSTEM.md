# Formato compartido: `design-system.md` (v1)

Este es el contrato entre los skills del kit. El skill **design-system** lo produce; **guion**, **edición de video** (con subtítulos) y el bonus **teleprompter** lo leen. Si un skill necesita un dato de marca, lo busca aquí y en ningún otro lado.

## Reglas del contrato

1. **Un solo archivo**, `design-system.md`, en Markdown. Funciona en cualquier AI: se sube como archivo, se guarda en un Proyecto o se pega al inicio del chat.
2. **Dos capas.** Un bloque YAML con los valores (lo que leen las máquinas) y secciones en prosa con las reglas (lo que leen las personas y los modelos). Los valores viven solo en el YAML; la prosa no repite hex ni tamaños.
3. **Claves fijas.** Los nombres de las claves y de los encabezados `##` no se traducen ni se cambian. Un skill que lee el archivo puede confiar en ellos.
4. **Nada vacío.** Si la persona no supo responder, el skill propone un valor y lo marca con `# propuesto` al final de la línea. Así los otros skills saben que pueden sugerir cambios.
5. **Versión.** `formato: design-system-v1` en el YAML. Si el contrato cambia, sube a `v2` y los skills avisan cuando leen una versión que no conocen.
6. **Derivados opcionales.** Donde se pueden escribir archivos (Claude Code, Cowork), el skill puede generar `tokens.css` desde el YAML. El `.md` sigue siendo la fuente de verdad: si cambia un valor, se cambia ahí y se regenera.

## Cómo lo lee cada skill

| Skill | Lee | Para qué |
| --- | --- | --- |
| Guion | `marca`, `publico`, `voz`, `guiones` y las secciones "Voz" y "Guiones" | Tono, palabras sí y no, duración, estructura, gancho, cierre y temas prohibidos |
| Edición de video | `color`, `tipografia`, `formas`, `movimiento`, `video`, `subtitulos`, `logo` y la sección "Video" | Overlays, colores, fuentes, zona segura, marca de agua, música, efectos y el estilo de los subtítulos |
| Teleprompter (bonus) | `color`, `tipografia`, `video.modo` | Colores y fuente de la página para grabar |

Si una clave falta (por ejemplo, un archivo hecho a mano), el skill usa el valor por defecto de la tabla de abajo y lo dice en una línea.

## Plantilla

Copia exacta de lo que entrega el skill. Los comentarios `#` explican cada clave y valores válidos.

````markdown
# Design system de <marca>

```yaml
formato: design-system-v1
actualizado: 2026-11-25           # AAAA-MM-DD

marca:
  nombre: ""                      # cómo se llama la marca o la persona
  handle: ""                      # @usuario en redes, si tiene
  que_hace: ""                    # una frase: qué hace y para quién
  promesa: ""                     # qué se lleva quien la sigue
  idioma: es                      # código ISO; los textos salen en este idioma
  variante: neutro                # neutro | mx | ar | co | pe | es | ... (modismos permitidos)

publico:
  quien: ""                       # rol o situación, no edad
  problema: ""                    # lo que le duele o quiere lograr
  nivel: intermedio               # principiante | intermedio | avanzado

voz:
  personalidad: []                # 2 a 4 adjetivos
  trato: tu                       # tu | usted | vos
  humor: medio                    # nada | poco | medio | mucho
  frases_si: []                   # expresiones propias que suenan a la marca
  frases_no: []                   # palabras o muletillas prohibidas
  emojis: pocos                   # nunca | pocos | libres

color:
  modo: claro                     # claro | oscuro | ambos (el primero es el principal)
  primario: "#000000"             # color de la marca: botones, resaltados, logo
  sobre_primario: "#FFFFFF"       # texto encima del primario (contraste >= 4.5:1)
  fondo: "#FFFFFF"
  superficie: "#F2F2F2"           # tarjetas y bloques sobre el fondo
  texto: "#111111"
  texto_secundario: "#555555"
  acento: "#000000"               # uso puntual, nunca protagonista
  oscuro:                         # solo si modo es oscuro o ambos
    fondo: "#111111"
    superficie: "#1C1C1C"
    texto: "#EEEEEE"
    texto_secundario: "#AAAAAA"
    primario: "#000000"
    sobre_primario: "#FFFFFF"
  prohibidos: []                  # colores que nunca se usan

tipografia:
  titulos: { familia: "", peso: 800, fuente_url: "" }   # fuente_url: Google Fonts o archivo propio
  texto:   { familia: "", peso: 400, fuente_url: "" }
  mono:    { familia: "", peso: 500, fuente_url: "" }   # opcional; vacío si no se usa
  mayusculas_en_titulos: false

formas:
  esquinas: redondeadas           # rectas | suaves | redondeadas | pildora
  radio_px: 24                    # radio de tarjetas a 1080 px de ancho
  elementos: []                   # formas o recursos propios (ej. "círculo", "subrayado a mano")
  textura: ninguna                # ninguna | grano | papel | vidrio | ...
  sombras: suaves                 # ninguna | suaves | marcadas

logo:
  tiene: false
  archivo: ""                     # ruta o nombre del archivo, si existe
  descripcion: ""                 # cómo es, si no hay archivo
  marca_de_agua: ""               # texto o logo; vacío si no lleva
  marca_de_agua_opacidad: 0.35

movimiento:
  energia: media                  # calmada | media | alta
  entradas: suaves                # secas | suaves | con-rebote
  transicion_ms: 250

video:
  formato: "1080x1920"            # vertical 9:16 por defecto
  modo: claro                     # claro | oscuro: fondo de overlays y tarjetas
  zona_segura: { x: [120, 960], y: [270, 1250] }       # lo que se lee va dentro
  plataformas: []                 # tiktok | instagram | youtube | linkedin | ...
  duracion_s: [30, 60]
  ritmo: medio                    # pausado | medio | rapido (cortes y zooms)
  musica: suave                   # ninguna | suave | protagonista
  efectos_sonido: pocos           # ninguno | pocos | muchos
  broll: []                       # qué tipo de apoyo visual le gusta: capturas, memes, fotos, texto...

subtitulos:
  activar: true
  fuente: ""                      # vacío = tipografia.titulos
  peso: 800
  tamano_px: 64                   # a 1080x1920
  color: "#FFFFFF"
  resaltado: "primario"           # palabra que se está diciendo: primario | acento | hex | ninguno
  contorno: { color: "#000000", grosor_px: 6 }
  caja: false                     # true = fondo detrás del texto
  posicion: centro                # arriba | centro | abajo (siempre dentro de la zona segura)
  palabras_por_linea: 3
  lineas: 1
  mayusculas: false
  emojis: false

guiones:
  estructura: gancho-desarrollo-cierre   # o el nombre de su fórmula propia
  gancho: ""                      # cómo le gusta abrir (pregunta, dato, contradicción...)
  cierre: ""                      # cómo cierra; el CTA, si tiene
  temas: []                       # de qué habla
  temas_no: []                    # de qué nunca habla
  fuentes: verificar              # verificar | libre (verificar = cada dato con fuente)
```

## Quién es y para quién
Dos o tres frases en prosa con lo que no cabe en el YAML.

## Voz
Reglas de escritura, con un ejemplo de frase que sí y uno que no.

## Color
Cuándo va cada color. Combinaciones prohibidas.

## Tipografía
Jerarquía y usos especiales.

## Formas y logo
Cómo se usan las formas, el logo y la marca de agua. Lo que nunca se hace.

## Video
Estilo de edición: qué le gusta y qué no. Cómo se ven los overlays.

## Subtítulos
Estilo en una frase y una muestra en texto: `ESTO ES **CLAVE**`.

## Guiones
Fórmula, gancho y cierre preferidos, con un ejemplo de cada uno.

## Límites
Lo que la marca nunca hace o dice.
````

## Valores por defecto

Los usa un skill lector cuando falta una clave. El skill design-system nunca los deja sin preguntar o proponer.

| Clave | Por defecto |
| --- | --- |
| `video.formato` | `1080x1920` |
| `video.zona_segura` | x 120 a 960, y 270 a 1250 (deja libres los botones y textos de TikTok, Reels y Shorts) |
| `subtitulos.tamano_px` | 64 |
| `subtitulos.palabras_por_linea` | 3 |
| `subtitulos.posicion` | `centro` |
| `subtitulos.resaltado` | `primario` |
| `movimiento.transicion_ms` | 250 |
| `voz.trato` | `tu` |

Ejemplo completo con una marca inventada: [`design-system/ejemplo/design-system.md`](design-system/ejemplo/design-system.md).
