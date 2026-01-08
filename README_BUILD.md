# Guida all'Impacchettamento dell'App

Questo progetto include script per creare eseguibili standalone delle applicazioni Python.

## Installazione Dipendenze

```bash
pip install -r requirements.txt
```

## Metodi di Build

### Metodo 1: Script Python (Consigliato)

```bash
# Build dell'app predefinita (visual_art.py)
python build_app.py

# Build di un'app specifica
python build_app.py breakout_game.py
python build_app.py todo_manager.py

# Build senza singolo file (cartella con più file)
python build_app.py visual_art.py --no-onefile

# Build senza console (solo Windows/macOS)
python build_app.py visual_art.py --windowed
```

### Metodo 2: Script Bash

```bash
chmod +x build.sh
./build.sh visual_art.py
```

### Metodo 3: PyInstaller Diretto

```bash
# Singolo file eseguibile
pyinstaller --onefile --name visual_art visual_art.py

# Cartella con più file (più veloce da avviare)
pyinstaller --name visual_art visual_art.py
```

## Output

Dopo il build, troverai:
- **dist/** - Contiene l'eseguibile finale
- **build/** - File temporanei (può essere eliminato)
- ***.spec** - File di configurazione PyInstaller

## Eseguire l'App Impacchettata

```bash
# Linux/macOS
./dist/visual_art

# Windows
dist\visual_art.exe
```

## Note

- Il primo avvio dell'eseguibile può essere lento (estrazione temporanea)
- Per app con GUI, usa `--windowed` per nascondere la console
- Per distribuzione, il singolo file (`--onefile`) è più comodo
- Per sviluppo/test, la cartella (`--no-onefile`) è più veloce

## Build per Windows

### Prerequisiti su Windows:
1. Installa Python da https://www.python.org/
2. Installa le dipendenze: `pip install -r requirements.txt`
3. Installa PyInstaller: `pip install pyinstaller`

### Metodo 1: Script Batch (Windows)
```cmd
build_windows.bat
```

### Metodo 2: PyInstaller Diretto (Windows)
```cmd
REM Per app GUI (senza console)
pyinstaller --name fattura_generator --onefile --windowed fattura_generator.py

REM Per app con console
pyinstaller --name fattura_generator --onefile --console fattura_generator.py
```

### Metodo 3: Usa il file .spec
```cmd
pyinstaller fattura_generator_windows.spec
```

**Nota:** Il build per Windows deve essere eseguito su un sistema Windows. PyInstaller crea eseguibili specifici per la piattaforma su cui viene eseguito.

## App Disponibili

- `visual_art.py` - Generatore di arte visiva
- `breakout_game.py` - Gioco Breakout
- `todo_manager.py` - Gestore todo list
- `fattura_generator.py` - Generatore di fatture (GUI)
- `main.py` - App di esempio
