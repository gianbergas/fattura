@echo off
REM Script per impacchettare l'app per Windows
REM Esegui questo script su Windows dopo aver installato Python e le dipendenze

echo === Build App per Windows ===
echo.

REM Verifica che Python sia installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo Installa Python da https://www.python.org/
    pause
    exit /b 1
)

REM Verifica che PyInstaller sia installato
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller non trovato. Installazione...
    pip install pyinstaller
)

REM Verifica che reportlab sia installato
python -c "import reportlab" >nul 2>&1
if errorlevel 1 (
    echo reportlab non trovato. Installazione...
    pip install reportlab
)

echo.
echo Costruzione dell'eseguibile per Windows...
echo.

REM Build con PyInstaller
pyinstaller --name fattura_generator --onefile --windowed --icon=NONE fattura_generator.py

if errorlevel 1 (
    echo.
    echo ERRORE durante la build!
    pause
    exit /b 1
)

echo.
echo === Build completato! ===
echo L'eseguibile si trova in: dist\fattura_generator.exe
echo.
pause
