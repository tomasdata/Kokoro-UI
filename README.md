# 🎙️ Kokoro TTS - Easy Voice Testing

**Una manera cómoda de probar Text-to-Speech con el modelo Kokoro-82M**

Este proyecto te permite **probar y experimentar con voces de alta calidad** de forma rápida y sencilla a través de una interfaz web moderna. Perfecto para podcasters, desarrolladores, creadores de contenido o cualquiera que quiera experimentar con síntesis de voz.

> **Kokoro-82M** es un modelo TTS open-source con 82 millones de parámetros. A pesar de ser ligero, ofrece calidad comparable a modelos más grandes. Licencia Apache 2.0.

## ✨ ¿Qué hace este proyecto?

**Te permite probar voces TTS de manera cómoda:**
- 🎤 **12+ voces** en Español e Inglés (US/UK)
- 🚀 **Interfaz web simple** - Solo texto → voz → descarga
- ⚡ **Rápido** - Con aceleración GPU cuando está disponible
- 💯 **Gratis y open-source** - Sin límites ni restricciones
- 🎨 **Fácil de usar** - Un solo comando para iniciar

**Ideal para:**
- Probar diferentes voces para tu proyecto
- Crear demos de audio rápidamente
- Experimentar con síntesis de voz
- Podcasts y contenido multimedia
- Prototipos de aplicaciones de voz

## 🚀 Inicio Rápido

### 1. Ejecuta el script:

**Mac/Linux:**
```bash
./start_web.sh
```

**Windows:**
```bash
start_web.bat
```

### 2. Abre tu navegador:

```
http://localhost:5000
```

### 3. ¡Listo!

Selecciona una voz, escribe tu texto y genera audio. Así de simple.

---

## 📖 Documentación

- **[Guía de la Web App](docs/WEB_APP.md)** - Documentación completa + arquitectura
- **[Deployment](docs/DEPLOYMENT.md)** - Cómo deployar en producción
- **[Local Setup](docs/LOCAL_SETUP.md)** - Setup personalizado
- **[Podcast Tips](docs/PODCAST_TIPS.md)** - Tips para podcasts

---

## 🎤 Voces Disponibles

### 🇪🇸 Español (3 voces)
- **Dora** (Femenina) - Cálida y clara
- **Alex** (Masculina) - Profesional
- **Santa** (Masculina) - Grave y autoritativa

### 🇺🇸 English US (7 voces)
- Heart, Bella, Nicole, Sarah, Sky (Femeninas)
- Michael, Adam (Masculinas)

### 🇬🇧 English UK (4 voces)
- Emma, Isabella (Femeninas)
- George, Lewis (Masculinas)

---

## 📁 Estructura del Proyecto

```
Kokoro/
├── webapp/              # 🌐 Interfaz web
│   ├── app.py          # Backend Flask
│   ├── templates/      # HTML templates
│   └── requirements.txt
│
├── kokoro/             # 📦 Biblioteca TTS core
├── demo/               # 🎭 Demo alternativo (Gradio)
├── scripts/            # 📝 Scripts CLI
├── docs/               # 📚 Documentación
│
├── start_web.sh        # 🚀 Launcher Unix
└── start_web.bat       # 🚀 Launcher Windows
```

---

## 🛠️ Uso Avanzado (Python)

### Instalación

```bash
pip install kokoro soundfile
```

### Ejemplo Básico

```python
from kokoro import KPipeline
import soundfile as sf

# Inicializar pipeline
pipeline = KPipeline(lang_code='e')  # 'e' = español

# Generar audio
text = "Hola, esto es una prueba de Kokoro TTS"
for _, _, audio in pipeline(text, voice='ef_dora', speed=0.92):
    sf.write('output.wav', audio, 24000)
```

### Ejemplo con Múltiples Voces

```python
# Inglés americano
pipeline_us = KPipeline(lang_code='a')
for _, _, audio in pipeline_us("Hello world", voice='af_heart'):
    sf.write('hello_en.wav', audio, 24000)

# Español
pipeline_es = KPipeline(lang_code='e')
for _, _, audio in pipeline_es("Hola mundo", voice='ef_dora'):
    sf.write('hola_es.wav', audio, 24000)
```

Ver más ejemplos en [`examples/`](examples/)

---

## ⚙️ Configuración

### Aceleración GPU

**Mac (Apple Silicon):**
```bash
export PYTORCH_ENABLE_MPS_FALLBACK=1
./start_web.sh
```

**NVIDIA (CUDA):**
```bash
# Detectado automáticamente
./start_web.sh
```

### Cambiar Puerto

Edita `webapp/app.py`:
```python
app.run(host='0.0.0.0', port=8000)  # Cambia 5000 a 8000
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Este proyecto busca hacer TTS accesible y fácil de probar.

---

## 📄 Licencia

Este proyecto usa Kokoro-82M bajo licencia **Apache 2.0**.

Puedes:
- ✅ Usar comercialmente
- ✅ Modificar
- ✅ Distribuir
- ✅ Uso privado

---

## 🙏 Créditos

- [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) - Modelo TTS
- [StyleTTS 2](https://github.com/yl4579/StyleTTS2) - Arquitectura base
- [Misaki](https://github.com/hexgrad/misaki) - Sistema G2P

---

## 🔗 Enlaces

- [HuggingFace Model Card](https://huggingface.co/hexgrad/Kokoro-82M)
- [Samples de Audio](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/SAMPLES.md)
- [Kokoro en PyPI](https://pypi.org/project/kokoro/)
- [Discord](https://discord.gg/QuGxSWBfQy)

---

**Hecho para facilitar pruebas de TTS 🎙️**
