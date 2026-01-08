# Istruzioni per Impacchettare su Windows

## Prerequisiti

1. **Installa Python 3.8+**
   - Scarica da https://www.python.org/downloads/
   - Durante l'installazione, seleziona "Add Python to PATH"

2. **Installa le dipendenze**
   ```cmd
   pip install -r requirements.txt
   ```

## Metodi di Build

### Metodo 1: Script Batch (Più Semplice)

1. Apri il Prompt dei Comandi o PowerShell
2. Naviga nella cartella del progetto
3. Esegui:
   ```cmd
   build_windows.bat
   ```

Lo script installerà automaticamente PyInstaller e reportlab se necessario, poi creerà l'eseguibile.

### Metodo 2: PyInstaller Manuale

```cmd
REM Installa PyInstaller (se non già installato)
pip install pyinstaller

REM Crea l'eseguibile (GUI senza console)
pyinstaller --name fattura_generator --onefile --windowed fattura_generator.py

REM Oppure con console visibile (per debug)
pyinstaller --name fattura_generator --onefile --console fattura_generator.py
```

### Metodo 3: Usa il File .spec

```cmd
pyinstaller fattura_generator_windows.spec
```

## Risultato

Dopo il build, troverai:
- **dist\fattura_generator.exe** - L'eseguibile Windows
- **build\** - File temporanei (puoi eliminarli)

## Aggiungere un'Icona

1. Crea o scarica un file `.ico` (icona Windows)
2. Modifica il comando:
   ```cmd
   pyinstaller --name fattura_generator --onefile --windowed --icon=icona.ico fattura_generator.py
   ```

Oppure modifica `fattura_generator_windows.spec` e cambia:
```python
icon='icona.ico',  # invece di icon=None
```

## Risoluzione Problemi

### "Python non trovato"
- Assicurati che Python sia nel PATH
- Riavvia il terminale dopo l'installazione

### "PyInstaller non trovato"
```cmd
pip install pyinstaller
```

### "reportlab non trovato"
```cmd
pip install reportlab
```

### L'eseguibile è troppo grande
- Usa `--onefile` solo se necessario
- Considera `--onedir` invece di `--onefile` per file più piccoli

### Antivirus segnala l'eseguibile
- PyInstaller crea eseguibili che alcuni antivirus segnalano come falsi positivi
- Aggiungi un'eccezione o firma digitalmente l'eseguibile

## Distribuzione

L'eseguibile `fattura_generator.exe` è standalone e include:
- Python runtime
- Tutte le librerie necessarie (tkinter, reportlab, ecc.)
- Il codice dell'applicazione

Puoi distribuirlo senza richiedere l'installazione di Python o altre dipendenze.
