# Kokoro 82M – instalación local

Pasos probados en macOS (Apple Silicon):

1. **Python 3.12**  
   ```bash
   brew install python@3.12
   ```

2. **Entorno virtual**  
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -e . soundfile
   ```

3. **Prueba rápida de inferencia**  
   ```bash
   PYTORCH_ENABLE_MPS_FALLBACK=1 python - <<'PY'
   from kokoro import KPipeline
   import numpy as np, soundfile as sf
   text = "Hola, esta es una prueba rápida de Kokoro."
   pipe = KPipeline(lang_code='a')
   chunks = [audio for _, _, audio in pipe(text, voice='af_bella')]
   audio = np.concatenate(chunks)
   sf.write("output/kokoro-demo.wav", audio, 24000)
   PY
   ```

El primer arranque descarga automáticamente:

- Los pesos del modelo `hexgrad/Kokoro-82M` desde Hugging Face.
- El modelo lingüístico `en_core_web_sm` de spaCy.

El archivo generado `output/kokoro-demo.wav` sirve para comprobar que todo quedó funcionando.

### Generación en español

1. Abre `input/es_text.txt` y reemplaza el texto de ejemplo por el que quieras locutar (puedes pegar varios párrafos y separarlos con líneas en blanco).
2. Ejecuta:
   ```bash
   source .venv/bin/activate
   python scripts/spanish_tts.py
   ```
   El script ahora te preguntará si quieres activar la aceleración MPS:
   - En macOS basta con pulsar **Enter** (respuesta por defecto = Sí).
   - En Windows/Linux pulsa **Enter** para continuar en CPU o escribe `y` solo si sabes que tienes soporte MPS.
3. El audio queda en `output/kokoro-es.wav` (o en la ruta que definas).

El script usa `lang_code='e'`, voz `ef_dora`, velocidad 0.92, bloques de hasta 320 caracteres y silencios suaves de 320 ms entre párrafos. Puedes ajustar estos valores editando las constantes al inicio de `scripts/spanish_tts.py`. Más consejos en `PODCAST_TIPS.md`.
