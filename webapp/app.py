#!/usr/bin/env python3
"""
Kokoro TTS - Interfaz Web Simple
Interfaz web para generar audio con Kokoro TTS
"""
from flask import Flask, render_template, request, send_file, jsonify
from kokoro import KPipeline
import soundfile as sf
import torch
import os
from pathlib import Path
import tempfile
import uuid
from datetime import datetime

app = Flask(__name__)

# Configuración
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR = Path(tempfile.gettempdir()) / "kokoro_temp"
TEMP_DIR.mkdir(exist_ok=True)

# Inicializar pipelines y modelo
print("Inicializando Kokoro TTS...")

# Detectar si estamos en macOS para MPS
if os.sys.platform == "darwin" and torch.backends.mps.is_available():
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
    print("✓ Aceleración MPS activada (Apple Silicon)")

# Inicializar pipelines para los lenguajes más comunes
pipelines = {
    'a': KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M'),  # American English
    'b': KPipeline(lang_code='b', repo_id='hexgrad/Kokoro-82M'),  # British English
    'e': KPipeline(lang_code='e', repo_id='hexgrad/Kokoro-82M'),  # Spanish
}

# Voces disponibles organizadas por idioma
VOICES = {
    'Español': {
        'ef_dora': '🇪🇸 🚺 Dora',
        'em_alex': '🇪🇸 🚹 Alex',
        'em_santa': '🇪🇸 🚹 Santa',
    },
    'English (US)': {
        'af_heart': '🇺🇸 🚺 Heart ❤️',
        'af_bella': '🇺🇸 🚺 Bella 🔥',
        'af_nicole': '🇺🇸 🚺 Nicole 🎧',
        'af_sarah': '🇺🇸 🚺 Sarah',
        'af_sky': '🇺🇸 🚺 Sky',
        'am_michael': '🇺🇸 🚹 Michael',
        'am_adam': '🇺🇸 🚹 Adam',
    },
    'English (UK)': {
        'bf_emma': '🇬🇧 🚺 Emma',
        'bf_isabella': '🇬🇧 🚺 Isabella',
        'bm_george': '🇬🇧 🚹 George',
        'bm_lewis': '🇬🇧 🚹 Lewis',
    }
}

# Pre-cargar voces más comunes
print("Cargando voces...")
for voice_id in ['ef_dora', 'af_heart', 'bf_emma']:
    lang_code = voice_id[0]
    if lang_code in pipelines:
        pipelines[lang_code].load_voice(voice_id)
        print(f"✓ Voz cargada: {voice_id}")

print("✓ Kokoro TTS listo!")

@app.route('/')
def index():
    return render_template('index.html', voices=VOICES)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        text = data.get('text', '').strip()
        voice = data.get('voice', 'ef_dora')
        speed = float(data.get('speed', 0.92))
        split_pattern = data.get('split_pattern', r'\n+')

        if not text:
            return jsonify({'error': 'El texto no puede estar vacío'}), 400

        # Determinar el pipeline según la voz
        lang_code = voice[0]
        if lang_code not in pipelines:
            return jsonify({'error': 'Voz no soportada'}), 400

        pipeline = pipelines[lang_code]

        # Generar audio
        print(f"Generando audio: voz={voice}, velocidad={speed}")
        audio_chunks = []
        total_chunks = 0

        for _, _, audio in pipeline(text, voice=voice, speed=speed, split_pattern=split_pattern):
            if audio is not None:
                audio_chunks.append(audio)
                total_chunks += 1

        if not audio_chunks:
            return jsonify({'error': 'No se pudo generar el audio'}), 500

        # Combinar chunks
        import numpy as np
        full_audio = np.concatenate(audio_chunks)

        # Guardar en archivo temporal
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"kokoro_{timestamp}_{uuid.uuid4().hex[:8]}.wav"
        filepath = TEMP_DIR / filename

        sf.write(filepath, full_audio, 24000)

        duration = len(full_audio) / 24000  # duración en segundos

        return jsonify({
            'success': True,
            'audio_url': f'/audio/{filename}',
            'filename': filename,
            'duration': round(duration, 2),
            'chunks': total_chunks
        })

    except Exception as e:
        print(f"Error generando audio: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    filepath = TEMP_DIR / filename
    if filepath.exists():
        return send_file(filepath, mimetype='audio/wav')
    return "Archivo no encontrado", 404

@app.route('/download/<filename>')
def download_audio(filename):
    filepath = TEMP_DIR / filename
    if filepath.exists():
        return send_file(filepath, mimetype='audio/wav', as_attachment=True, download_name=filename)
    return "Archivo no encontrado", 404

def find_free_port(start_port=5000, max_port=5010):
    """Encuentra un puerto libre empezando desde start_port"""
    import socket
    for port in range(start_port, max_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    return None

if __name__ == '__main__':
    port = find_free_port()

    if port is None:
        print("\n❌ Error: No se pudo encontrar un puerto disponible entre 5000-5010")
        print("\nIntenta cerrar otras aplicaciones o ejecutar:")
        print("  lsof -ti:5000 | xargs kill -9  # Para liberar el puerto 5000")
        exit(1)

    print("\n" + "="*60)
    print("🎙️  KOKORO TTS - Interfaz Web")
    print("="*60)
    print(f"Abre tu navegador en: http://localhost:{port}")
    if port != 5000:
        print(f"\n⚠️  Puerto 5000 ocupado, usando puerto {port}")
    print("Presiona Ctrl+C para detener el servidor")
    print("="*60 + "\n")

    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n\n✓ Servidor detenido")
    except Exception as e:
        print(f"\n❌ Error al iniciar servidor: {e}")
        exit(1)
