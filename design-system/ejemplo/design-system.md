# Design system de Plata Clara

> Ejemplo con una marca inventada. Sirve para ver el formato completo y para probar los skills de guion y edición.

```yaml
formato: design-system-v1
actualizado: 2026-11-25

marca:
  nombre: "Plata Clara"
  handle: "@plataclara"
  que_hace: "Enseño finanzas personales a gente que acaba de conseguir su primer trabajo"
  promesa: "Saber a dónde va tu sueldo sin hojas de cálculo eternas"
  idioma: es
  variante: neutro

publico:
  quien: "Profesionales de 22 a 30 años con su primer sueldo fijo"
  problema: "Llegan a fin de mes sin saber en qué se fue la plata"
  nivel: principiante

voz:
  personalidad: [cercana, directa, divertida]
  trato: tu
  humor: medio
  frases_si: ["hagamos cuentas", "sin culpa"]
  frases_no: ["libertad financiera", "hazte millonario", "invierte ya"]
  emojis: pocos

color:
  modo: claro
  primario: "#1F7A5C"
  sobre_primario: "#FFFFFF"
  fondo: "#FAFAF5"
  superficie: "#EEF3EC"
  texto: "#18201C"
  texto_secundario: "#4A5550"
  acento: "#E07A2F"
  oscuro:
    fondo: "#101513"       # propuesto
    superficie: "#1B2320"  # propuesto
    texto: "#E6ECE8"       # propuesto
    texto_secundario: "#A9B5AF"  # propuesto
    primario: "#6FD3AE"    # propuesto
    sobre_primario: "#00382A"    # propuesto
  prohibidos: ["rojo intenso (se lee como alarma o deuda)"]

tipografia:
  titulos: { familia: "Nunito", peso: 900, fuente_url: "https://fonts.google.com/specimen/Nunito" }
  texto:   { familia: "Nunito Sans", peso: 400, fuente_url: "https://fonts.google.com/specimen/Nunito+Sans" }
  mono:    { familia: "", peso: 500, fuente_url: "" }
  mayusculas_en_titulos: false

formas:
  esquinas: redondeadas
  radio_px: 32
  elementos: ["moneda dibujada a mano", "subrayado a mano"]
  textura: grano
  sombras: suaves

logo:
  tiene: false
  archivo: ""
  descripcion: "Pendiente. Dirección: una moneda con una C abierta, en primario"
  marca_de_agua: "@plataclara"
  marca_de_agua_opacidad: 0.35

movimiento:
  energia: media
  entradas: con-rebote
  transicion_ms: 250

video:
  formato: "1080x1920"
  modo: claro
  zona_segura: { x: [120, 960], y: [270, 1250] }
  plataformas: [tiktok, instagram]
  duracion_s: [30, 50]
  ritmo: rapido
  musica: suave
  efectos_sonido: pocos
  broll: [capturas, texto animado, memes propios]

subtitulos:
  activar: true
  fuente: ""
  peso: 900
  tamano_px: 68
  color: "#FFFFFF"
  resaltado: "acento"
  contorno: { color: "#18201C", grosor_px: 6 }
  caja: false
  posicion: centro
  palabras_por_linea: 3
  lineas: 1
  mayusculas: true
  emojis: false

guiones:
  estructura: gancho-desarrollo-cierre
  gancho: "Una cifra de su propio sueldo que sorprende"
  cierre: "Un paso que puedes hacer hoy, y la invitación a la newsletter"
  temas: [presupuesto, ahorro, deudas de tarjeta, primer sueldo]
  temas_no: [criptomonedas, recomendaciones de acciones, política]
  fuentes: verificar
```

## Quién es y para quién
Plata Clara le habla a quien recién cobra su primer sueldo y siente que el dinero se le escapa. No vende inversiones: enseña a mirar los números sin miedo.

## Voz
Como una amiga que sabe de plata y te explica en un café. Frases cortas, cuentas con números redondos y cero culpa.
- Sí: "Hagamos cuentas: si gastas 10 al día en delivery, son 300 al mes."
- No: "Descubre el secreto para alcanzar la libertad financiera."

## Color
El verde primario marca lo que importa: botones, cifras clave y el subrayado. El naranja de acento solo resalta una palabra o un dato por pantalla. Nunca rojo intenso, ni siquiera para pérdidas: se usa el texto secundario con un ícono.

## Tipografía
Nunito 900 para ganchos y cifras grandes; Nunito Sans 400 para el resto. Las cifras van siempre en titulares, nunca escondidas en un párrafo.

## Formas y logo
Tarjetas con esquinas de 32 px y grano suave. La moneda dibujada a mano aparece como sticker en una esquina, una por pieza. Marca de agua: @plataclara abajo a la derecha, dentro de la zona segura.

## Video
Ritmo rápido: cortes cada 2 o 3 segundos y zoom leve en las cifras. Capturas de apps de banco con los datos borrosos. Memes propios, nunca con material de terceros.

## Subtítulos
Blancos en mayúsculas con contorno oscuro, 3 palabras por línea, al centro. La palabra que se está diciendo cambia a naranja. Muestra: `TU SUELDO SE **VA**`.

## Guiones
Abre con una cifra que duele ("El 40% de tu sueldo se va en cosas que no recuerdas") y cierra con un paso concreto para hoy. Duración de 30 a 50 segundos.

## Límites
Nunca promete rendimientos, no recomienda acciones ni criptomonedas y no muestra datos bancarios reales.
