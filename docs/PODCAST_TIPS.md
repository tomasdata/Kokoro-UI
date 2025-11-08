# Kokoro 82M – Guía rápida para podcasts en español

## 1. Preparar el texto
- Escribe en `input/es_text.txt`.
- Separa párrafos con una línea en blanco; el script usa esos cortes para generar bloques manejables.
- Acentúa bien las palabras y evita abreviaturas sin contexto.
- Añade puntuación generosa: comas, puntos y signos de exclamación/pregunta ayudan al ritmo.
- Para guiar pronunciaciones difíciles puedes usar fonética: `[Kokoro](/kˈokoro/)`.

## 2. Ejecutar el script con parámetros útiles
```
source .venv/bin/activate
python scripts/spanish_tts.py
```
- El script preguntará si deseas activar MPS. En macOS pulsa Enter (sí por defecto); en Windows/Linux pulsa Enter para seguir en CPU.
- Los parámetros predeterminados están optimizados para podcast (`ef_dora`, velocidad 0.92, 320 caracteres por bloque, 320 ms de silencio). Si necesitas variantes, edita las constantes al inicio del script.

## 3. Trucos para mejorar la naturalidad
- Une frases cortas en bloques de 2–3 oraciones para que el modelo tenga contexto.
- Usa mayúsculas para enfatizar palabras clave o añade “–” y “…” antes de pausas dramáticas.
- Si mezclas idiomas, escribe la pronunciación aproximada (ej. “Nueva York (Niu Êrk)”).
- Después de generar el WAV, aplica post-proceso ligero (EQ, compresión suave, limitador) en tu DAW preferido.
- Para episodios largos, genera varias partes (`--output output/episodio_parte1.wav`, etc.) y ensámblalas.

## 4. Workflow recomendado
1. Edita `es_text.txt` con el guion final.
2. Ejecuta el script con los parámetros deseados y escucha el WAV.
3. Ajusta signos de puntuación/énfasis según lo que escuches y vuelve a generar.
4. Exporta a tu sesión de podcast para mezclar con música o invitados.

Con estos ajustes Kokoro produce resultados más fluidos y constantes para narraciones largas. Experimenta con cada parámetro hasta encontrar el tono que mejor se adapte a tu estilo. *** End Patch
