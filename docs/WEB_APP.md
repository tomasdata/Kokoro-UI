# 🎙️ Kokoro TTS - Web Interface

Una interfaz web moderna y completa para [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), un modelo TTS de código abierto con 82 millones de parámetros.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Kokoro](https://img.shields.io/badge/Kokoro-0.9.4-purple.svg)](https://github.com/hexgrad/kokoro)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Inicio Rápido](#-inicio-rápido)
- [Arquitectura](#-arquitectura)
- [Uso](#-uso)
- [Voces Disponibles](#-voces-disponibles)
- [Configuración](#-configuración)
- [API](#-api)
- [Licencia](#-licencia)

## ✨ Características

- **🎨 Interfaz Web Moderna**: UI responsive con diseño glassmorphism
- **🎤 12+ Voces**: Español, Inglés US/UK con voces masculinas y femeninas
- **⚡ Rápido**: Optimizado con aceleración GPU (CUDA/MPS)
- **🔧 Configurable**: Control de velocidad, split patterns
- **📦 Fácil de Usar**: Un solo comando para iniciar
- **💾 Descarga Directa**: Exporta archivos WAV de alta calidad
- **🌐 Multi-idioma**: Soporte para 9 idiomas
- **📱 Responsive**: Funciona en desktop y móvil

## 🚀 Inicio Rápido

### Requisitos

- Python 3.10 o superior
- pip o uv
- espeak-ng (para fallback en inglés)

### Instalación

```bash
# Clonar el repositorio
git clone <tu-repo>
cd Kokoro

# Instalar dependencias
pip install flask soundfile kokoro

# En macOS, instalar espeak-ng
brew install espeak-ng

# En Ubuntu/Debian
sudo apt-get install espeak-ng
```

### Iniciar la Aplicación

#### Opción 1: Script automático (recomendado)

**Mac/Linux:**
```bash
./start_web.sh
```

**Windows:**
```bash
start_web.bat
```

#### Opción 2: Manual

```bash
# Activar aceleración GPU en Mac (opcional)
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Iniciar servidor
python3 web_app.py
```

Abre tu navegador en: **http://localhost:5000**

## 🏗️ Arquitectura

### Estructura del Proyecto

```
Kokoro/
├── web_app.py              # Backend Flask (API REST)
├── templates/
│   └── index.html          # Frontend (UI moderna)
├── kokoro/                 # Biblioteca principal de Kokoro TTS
│   ├── pipeline.py         # Pipeline de generación
│   ├── model.py            # Modelo neural
│   └── __init__.py
├── scripts/
│   └── spanish_tts.py      # Script CLI para español
├── demo/
│   └── app.py              # Demo alternativo con Gradio
├── start_web.sh            # Script de inicio Unix
└── start_web.bat           # Script de inicio Windows
```

### Flujo de Datos

```
┌─────────────┐
│  Frontend   │  Usuario ingresa texto y selecciona voz
│ (HTML/JS)   │
└──────┬──────┘
       │ HTTP POST /generate
       ▼
┌─────────────┐
│   Flask     │  Recibe parámetros (text, voice, speed)
│   Backend   │
└──────┬──────┘
       │ Llama a KPipeline
       ▼
┌─────────────┐
│  KPipeline  │  1. G2P (texto → fonemas)
│             │  2. Chunking (divide texto largo)
└──────┬──────┘
       │ Para cada chunk
       ▼
┌─────────────┐
│   KModel    │  3. Modelo neural (fonemas → audio)
│  (82M)      │  4. Vocoder (genera waveform)
└──────┬──────┘
       │ numpy array
       ▼
┌─────────────┐
│  soundfile  │  5. Guarda WAV (24kHz)
│             │
└──────┬──────┘
       │ Retorna URL
       ▼
┌─────────────┐
│  Frontend   │  6. Reproduce/descarga audio
│             │
└─────────────┘
```

### Componentes Clave

#### 1. Backend (Flask)

**web_app.py** - Servidor API REST

- **Endpoints**:
  - `GET /` - Sirve la interfaz HTML
  - `POST /generate` - Genera audio desde texto
  - `GET /audio/<filename>` - Sirve archivos de audio
  - `GET /download/<filename>` - Descarga de audio

- **Pipelines**:
  ```python
  pipelines = {
      'a': KPipeline(lang_code='a'),  # American English
      'b': KPipeline(lang_code='b'),  # British English
      'e': KPipeline(lang_code='e'),  # Spanish
  }
  ```

- **Caché de Voces**: Pre-carga voces comunes al inicio

#### 2. Frontend (HTML/CSS/JS)

**templates/index.html** - Single Page Application

- **Tecnologías**:
  - HTML5 + CSS3 (gradientes, animaciones)
  - JavaScript vanilla (fetch API)
  - Web Audio API (reproducción)

- **Características UI**:
  - Glassmorphism design
  - Animaciones suaves (cubic-bezier)
  - Loading states
  - Error handling
  - LocalStorage para persistencia

#### 3. Kokoro TTS Core

**kokoro/pipeline.py** - Pipeline principal

```python
# Flujo de generación
pipeline = KPipeline(lang_code='e')
for graphemes, phonemes, audio in pipeline(text, voice='ef_dora', speed=0.92):
    # graphemes: texto original
    # phonemes: representación fonética
    # audio: numpy array (24kHz)
```

**Proceso**:
1. **G2P (Grapheme-to-Phoneme)**: Convierte texto a fonemas
2. **Chunking**: Divide en segmentos de ≤510 tokens
3. **Voice Loading**: Carga embeddings de voz desde HuggingFace
4. **Inference**: Modelo genera audio por chunk
5. **Concatenación**: Une todos los chunks

## 📖 Uso

### Interfaz Web

1. **Selecciona una voz** del dropdown (agrupadas por idioma)
2. **Escribe o pega tu texto** (soporta múltiples párrafos)
3. **Ajusta la velocidad** (0.5x - 2.0x, default: 0.92x)
4. **Click en "Generar Audio"**
5. **Reproduce** automáticamente o **descarga** el archivo

### Consejos para Mejores Resultados

#### Para Podcasts (Español)
```
- Usa frases largas con pausas naturales
- Velocidad: 0.92x (óptima para español)
- Separa párrafos con doble salto de línea
- Usa signos de exclamación para énfasis
```

#### Para Texto en Inglés
```
- Velocidad: 1.0x (más natural)
- Usa puntuación para controlar pausas
- Markdown links para pronunciación: [word](/pronunciation/)
```

## 🎤 Voces Disponibles

### 🇪🇸 Español (3 voces)

| Código | Género | Nombre | Características |
|--------|--------|--------|-----------------|
| `ef_dora` | 🚺 | Dora | Cálida, clara, ideal para podcasts |
| `em_alex` | 🚹 | Alex | Profesional, neutra |
| `em_santa` | 🚹 | Santa | Grave, autoritativa |

### 🇺🇸 English US (7 voces)

| Código | Género | Nombre | Características |
|--------|--------|--------|-----------------|
| `af_heart` | 🚺 | Heart | Amigable, versátil |
| `af_bella` | 🚺 | Bella | Enérgica, joven |
| `af_nicole` | 🚺 | Nicole | Clara, profesional |
| `af_sarah` | 🚺 | Sarah | Suave, natural |
| `af_sky` | 🚺 | Sky | Brillante, moderna |
| `am_michael` | 🚹 | Michael | Autoritativa, confiable |
| `am_adam` | 🚹 | Adam | Relajada, amigable |

### 🇬🇧 English UK (4 voces)

| Código | Género | Nombre | Características |
|--------|--------|--------|-----------------|
| `bf_emma` | 🚺 | Emma | Elegante, británica |
| `bf_isabella` | 🚺 | Isabella | Sofisticada |
| `bm_george` | 🚹 | George | Formal, británica |
| `bm_lewis` | 🚹 | Lewis | Natural, amigable |

### Otros Idiomas Soportados

- 🇫🇷 Francés (fr-fr)
- 🇮🇹 Italiano (it)
- 🇧🇷 Portugués Brasil (pt-br)
- 🇮🇳 Hindi (hi)
- 🇯🇵 Japonés (ja) - requiere `pip install misaki[ja]`
- 🇨🇳 Chino Mandarín (zh) - requiere `pip install misaki[zh]`

## ⚙️ Configuración

### Variables de Entorno

```bash
# Aceleración GPU en Mac
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Puerto personalizado
export FLASK_PORT=8000
```

### Configuración Avanzada

Edita `web_app.py`:

```python
# Cambiar voz por defecto
DEFAULT_VOICE = 'ef_dora'

# Cambiar velocidad por defecto
DEFAULT_SPEED = 0.92

# Cambiar puerto
PORT = 5000

# Directorio de salida
TEMP_DIR = Path("/custom/path")
```

### Aceleración GPU

#### CUDA (NVIDIA)
```bash
# Automático si torch detecta CUDA
python3 web_app.py
```

#### MPS (Apple Silicon)
```bash
export PYTORCH_ENABLE_MPS_FALLBACK=1
python3 web_app.py
```

#### CPU (Fallback)
```bash
# Sin configuración adicional
python3 web_app.py
```

## 🔌 API

### POST /generate

Genera audio desde texto.

**Request:**
```json
{
  "text": "Hola, ¿cómo estás?",
  "voice": "ef_dora",
  "speed": 0.92,
  "split_pattern": "\\n+"
}
```

**Response:**
```json
{
  "success": true,
  "audio_url": "/audio/kokoro_20250108_143025_a1b2c3d4.wav",
  "filename": "kokoro_20250108_143025_a1b2c3d4.wav",
  "duration": 2.5,
  "chunks": 1
}
```

**Ejemplo con cURL:**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola mundo","voice":"ef_dora","speed":1.0}'
```

### GET /audio/<filename>

Sirve archivo de audio para streaming.

**Response:** `audio/wav` (24kHz, mono)

### GET /download/<filename>

Descarga archivo de audio.

**Response:** `audio/wav` con header `attachment`

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"

```bash
pip install flask soundfile
```

### Error: "No module named 'kokoro'"

```bash
pip install kokoro
```

### Error: "CUDA out of memory"

Reduce el tamaño del texto o usa CPU:

```python
# Deshabilitar GPU temporalmente
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

### Audio se corta o tiene artefactos

- Reduce la velocidad (0.8x - 0.9x)
- Divide el texto en párrafos más cortos
- Usa mejor puntuación

### Aceleración MPS no funciona (Mac)

```bash
# Verificar disponibilidad
python3 -c "import torch; print(torch.backends.mps.is_available())"

# Si es False, usar CPU
unset PYTORCH_ENABLE_MPS_FALLBACK
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto usa **Kokoro-82M**, que está licenciado bajo [Apache License 2.0](LICENSE).

**Puedes:**
- ✅ Usar comercialmente
- ✅ Modificar el código
- ✅ Distribuir
- ✅ Uso privado

**Debes:**
- 📋 Incluir la licencia original
- 📋 Declarar cambios significativos

## 🙏 Agradecimientos

- [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) por el modelo TTS
- [StyleTTS 2](https://github.com/yl4579/StyleTTS2) por la arquitectura base
- [Misaki](https://github.com/hexgrad/misaki) por el sistema G2P
- Comunidad de código abierto

## 📚 Recursos Adicionales

- [Documentación de Kokoro](https://github.com/hexgrad/kokoro)
- [HuggingFace Model Card](https://huggingface.co/hexgrad/Kokoro-82M)
- [Samples de Audio](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/SAMPLES.md)
- [Discord de Kokoro](https://discord.gg/QuGxSWBfQy)

---

**Hecho con ❤️ usando Kokoro TTS**
