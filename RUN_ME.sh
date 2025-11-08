#!/bin/bash

# ═══════════════════════════════════════════════════════════════
#  🎙️ KOKORO TTS - PRUEBA RÁPIDA
# ═══════════════════════════════════════════════════════════════
#
#  Este script inicia la interfaz web para probar voces TTS
#
#  Uso: ./RUN_ME.sh
#
# ═══════════════════════════════════════════════════════════════

# Función para limpiar al salir
cleanup() {
    echo ""
    echo ""
    echo "✓ Servidor detenido"
    exit 0
}

trap cleanup INT TERM

clear

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║          🎙️  KOKORO TTS - Easy Voice Testing            ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Iniciando interfaz web..."
echo ""

# Verificar si existe el entorno virtual
if [ -d ".venv" ]; then
    echo "✓ Activando entorno virtual..."
    source .venv/bin/activate
else
    echo "⚠️  No se encontró .venv - usando Python del sistema"
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo ""
    echo "Instala Python 3 desde: https://www.python.org/"
    exit 1
fi

# Verificar dependencias básicas
echo "✓ Verificando dependencias..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "📦 Instalando Flask..."
    pip3 install -q flask soundfile
fi

python3 -c "import kokoro" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Instalando Kokoro TTS..."
    pip3 install -q kokoro
fi

# Verificar si el puerto 5000 está ocupado
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo ""
    echo "⚠️  Puerto 5000 ocupado - buscando puerto alternativo..."
    echo ""
    echo "💡 Tip: En macOS, desactiva 'AirPlay Receiver' en:"
    echo "   Configuración > General > AirDrop y Handoff"
fi

# Configurar GPU en macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    export PYTORCH_ENABLE_MPS_FALLBACK=1
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✨ Interfaz iniciando..."
echo ""
echo "  • El puerto se mostrará al cargar"
echo "  • Si puerto 5000 está ocupado, usará otro"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Cambiar al directorio webapp
cd webapp || {
    echo "❌ Error: No se encontró el directorio webapp/"
    exit 1
}

# Iniciar la aplicación
python3 app.py
