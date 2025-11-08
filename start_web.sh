#!/bin/bash

# Script para iniciar la interfaz web de Kokoro TTS

# Función para limpiar al salir
cleanup() {
    echo ""
    echo "✓ Servidor detenido"
    exit 0
}

trap cleanup INT TERM

echo "================================================"
echo "🎙️  KOKORO TTS - Interfaz Web"
echo "================================================"
echo ""

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    echo "✓ Activando entorno virtual..."
    source .venv/bin/activate
fi

# Verificar dependencias
echo "✓ Verificando dependencias..."
python3 -c "import flask" 2>/dev/null || {
    echo "⚠️  Flask no está instalado. Instalando..."
    pip3 install -q flask soundfile
}

python3 -c "import kokoro" 2>/dev/null || {
    echo "⚠️  Kokoro no está instalado. Instalando..."
    pip3 install -q kokoro
}

# Verificar si el puerto 5000 está ocupado
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo ""
    echo "⚠️  Puerto 5000 ocupado - se usará puerto alternativo"
    echo ""
    echo "💡 Tip macOS: Desactiva 'AirPlay Receiver' en:"
    echo "   Configuración > General > AirDrop y Handoff"
fi

# Configurar MPS en macOS si está disponible
if [[ "$OSTYPE" == "darwin"* ]]; then
    export PYTORCH_ENABLE_MPS_FALLBACK=1
    echo "✓ Aceleración MPS activada (Apple Silicon)"
fi

echo ""
echo "================================================"
echo "🚀 Iniciando servidor web..."
echo "================================================"
echo "   El puerto se mostrará al cargar"
echo "   Presiona Ctrl+C para detener"
echo "================================================"
echo ""

# Cambiar al directorio webapp
cd webapp || {
    echo "❌ Error: No se encontró el directorio webapp/"
    exit 1
}

# Iniciar la aplicación
python3 app.py
