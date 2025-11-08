@echo off
echo ================================================
echo     KOKORO TTS - Interfaz Web
echo ================================================
echo.

REM Activar entorno virtual si existe
if exist ".venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
)

REM Verificar dependencias
echo Verificando dependencias...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask no esta instalado. Instalando...
    pip install flask soundfile
)

echo.
echo ================================================
echo Iniciando servidor web...
echo ================================================
echo    Abre tu navegador en: http://localhost:5000
echo    Presiona Ctrl+C para detener
echo ================================================
echo.

REM Iniciar la aplicación
cd webapp
python app.py

pause
