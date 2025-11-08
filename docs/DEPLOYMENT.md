# 🚀 Deployment Guide

Guía para desplegar la interfaz web de Kokoro TTS en diferentes plataformas.

## 📦 Local Development

```bash
./start_web.sh  # Mac/Linux
# o
start_web.bat   # Windows
```

## ☁️ Cloud Deployment

### 1. Heroku

```bash
# Crear Procfile
echo "web: gunicorn web_app:app" > Procfile

# Actualizar requirements
echo "gunicorn==21.2.0" >> requirements_web.txt

# Deploy
heroku create kokoro-tts
git push heroku main
```

### 2. Railway

```bash
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python3 web_app.py"
healthcheckPath = "/"
healthcheckTimeout = 100
```

### 3. Render

```yaml
# render.yaml
services:
  - type: web
    name: kokoro-tts
    env: python
    buildCommand: "pip install -r requirements_web.txt && pip install kokoro"
    startCommand: "python3 web_app.py"
```

### 4. DigitalOcean App Platform

```yaml
name: kokoro-tts
services:
- name: web
  github:
    repo: tu-usuario/kokoro-web
    branch: main
  run_command: python3 web_app.py
  environment_slug: python
```

### 5. Fly.io

```toml
# fly.toml
app = "kokoro-tts"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"
  PYTORCH_ENABLE_MPS_FALLBACK = "0"

[[services]]
  http_checks = []
  internal_port = 5000
  protocol = "tcp"
```

## 🐳 Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar espeak-ng
RUN apt-get update && apt-get install -y espeak-ng && rm -rf /var/lib/apt/lists/*

# Copiar archivos
COPY requirements_web.txt .
COPY web_app.py .
COPY templates/ templates/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements_web.txt && \
    pip install --no-cache-dir kokoro

EXPOSE 5000

CMD ["python3", "web_app.py"]
```

**Build & Run:**
```bash
docker build -t kokoro-tts .
docker run -p 5000:5000 kokoro-tts
```

## 🔒 Producción

### Variables de Entorno

```bash
# .env
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-here
PORT=5000
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Para archivos de audio grandes
        client_max_body_size 100M;
        proxy_read_timeout 300s;
    }
}
```

### Systemd Service

```ini
# /etc/systemd/system/kokoro-tts.service
[Unit]
Description=Kokoro TTS Web Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/kokoro-tts
Environment="PYTORCH_ENABLE_MPS_FALLBACK=0"
ExecStart=/usr/bin/python3 web_app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Activar:**
```bash
sudo systemctl enable kokoro-tts
sudo systemctl start kokoro-tts
```

## ⚡ Optimizaciones

### 1. Gunicorn (Workers)

```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 --timeout 120 web_app:app
```

### 2. Redis Cache (Voice Embeddings)

```python
import redis
cache = redis.Redis(host='localhost', port=6379)
```

### 3. CDN para Audio

Usar S3 + CloudFront para servir archivos:

```python
import boto3
s3 = boto3.client('s3')
s3.upload_file(filepath, 'bucket-name', filename)
```

## 📊 Monitoreo

### Health Check Endpoint

Agregar a `web_app.py`:

```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200
```

### Logs

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🔐 Seguridad

### Rate Limiting

```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    default_limits=["100 per hour"]
)

@limiter.limit("10 per minute")
@app.route('/generate', methods=['POST'])
def generate():
    ...
```

### CORS (si necesario)

```bash
pip install flask-cors
```

```python
from flask_cors import CORS
CORS(app, origins=['https://tu-dominio.com'])
```

## 💰 Estimación de Costos

### Heroku
- Dyno Básico: $7/mes
- Con GPU: No disponible

### Railway
- Starter: $5/mes
- GPU: $10-50/mes

### AWS EC2
- t3.medium: ~$30/mes
- g4dn.xlarge (GPU): ~$380/mes

### DigitalOcean
- Basic Droplet: $12/mes
- GPU Droplet: $100+/mes

## 📈 Escalabilidad

### Horizontal Scaling

```bash
# Múltiples workers
gunicorn --workers 8 web_app:app
```

### Load Balancer

```nginx
upstream kokoro_backend {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}
```

### Queue System (Celery)

Para procesamiento asíncrono de audio:

```python
from celery import Celery

celery = Celery('kokoro', broker='redis://localhost:6379')

@celery.task
def generate_audio_task(text, voice, speed):
    # Procesar en background
    pass
```

---

**Para más información, consulta [README_WEB_APP.md](README_WEB_APP.md)**
