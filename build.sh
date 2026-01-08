#!/bin/bash
# Script per impacchettare l'applicazione

APP_NAME="${1:-visual_art.py}"

echo "=== Build App ==="
echo "App: $APP_NAME"
echo ""

# Verifica che PyInstaller sia installato
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller non trovato. Installazione..."
    pip install pyinstaller
fi

# Esegui il build
python build_app.py "$APP_NAME"

echo ""
echo "=== Build completato ==="
echo "L'eseguibile si trova nella cartella 'dist/'"
