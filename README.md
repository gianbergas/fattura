# Python Test Projects

Raccolta di progetti Python utili e divertenti, inclusi giochi, utilità e applicazioni.

## 📦 Progetti Inclusi

### 🎨 Visual Art Generator
Generatore di arte visiva con 5 modalità animate e colorate.
- Spirali colorate rotanti
- Onde animate multicolori
- Particelle con attrazione
- Mandala rotanti
- Effetto tunnel/starfield

**Esegui:** `python visual_art.py`

### 🎮 Breakout Game
Classico gioco Breakout/Arkanoid con paddle, pallina e mattoncini.
- Sistema di punteggio
- 3 vite
- Fisica di rimbalzo realistica

**Esegui:** `python breakout_game.py`

### 📋 Todo Manager
Gestore di todo list da terminale con persistenza su file JSON.
- Aggiungi, completa, elimina task
- Statistiche
- Salvataggio automatico

**Esegui:** `python todo_manager.py`

### 🧾 Generatore di Fatture
Applicazione GUI completa per creare fatture professionali in PDF.
- Interfaccia grafica intuitiva
- Gestione prodotti/servizi
- Calcolo automatico IVA e totali
- Generazione PDF professionale
- Salvataggio/caricamento dati

**Esegui:** `python fattura_generator.py`

### 🧾 Fattura Pro (Nuovo!)
Generatore professionale di fatture italiane con design moderno e funzionalità avanzate.
- ✨ Interfaccia moderna e fluida
- 🇮🇹 Conforme alle normative italiane
- 📊 Riepilogo dettagliato per aliquota IVA
- 🔄 Auto-numerazione fatture
- ✅ Validazione P.IVA italiana
- 💳 Supporto dati bancari (IBAN)
- 📄 PDF professionale con layout ottimizzato
- 💾 Salvataggio/caricamento template

**Esegui:** `python fattura_pro.py`

## 🚀 Installazione

### Prerequisiti
- Python 3.8 o superiore
- pip (gestore pacchetti Python)

### Dipendenze

```bash
pip install -r requirements.txt
```

**Dipendenze principali:**
- `pygame` - Per i giochi e visualizzazioni
- `reportlab` - Per la generazione PDF (fatture)
- `pyinstaller` - Per impacchettare le app

### Dipendenze Sistema (Linux)

```bash
# Per tkinter (fattura_generator)
sudo apt-get install python3-tk
```

## 📦 Impacchettamento

Tutte le app possono essere impacchettate in eseguibili standalone usando PyInstaller.

### Linux/macOS
```bash
python build_app.py visual_art.py
```

### Windows
```cmd
build_windows.bat
```

Vedi [README_BUILD.md](README_BUILD.md) e [ISTRUZIONI_WINDOWS.md](ISTRUZIONI_WINDOWS.md) per dettagli completi.

## 📁 Struttura Progetto

```
python-test/
├── visual_art.py              # Generatore arte visiva
├── breakout_game.py           # Gioco Breakout
├── todo_manager.py            # Gestore todo
├── fattura_generator.py       # Generatore fatture
├── build_app.py               # Script build
├── requirements.txt           # Dipendenze
├── README.md                  # Questo file
├── README_BUILD.md            # Guida build
└── ISTRUZIONI_WINDOWS.md      # Istruzioni Windows
```

## 🎮 Controlli

### Visual Art Generator
- **1-5** - Cambia modalità visiva
- **ESC** - Esci

### Breakout Game
- **Frecce/A/D** - Muovi paddle
- **R** - Ricomincia
- **ESC** - Esci

### Todo Manager
- **add <task>** - Aggiungi todo
- **list** - Mostra tutti
- **complete <id>** - Completa
- **delete <id>** - Elimina
- **stats** - Statistiche
- **quit** - Esci

## 📝 Note

- I file `todos.json` e `fattura_settings.json` sono esclusi da git (vedi .gitignore)
- Gli eseguibili generati si trovano in `dist/`
- I file temporanei di build si trovano in `build/`

## 🤝 Contribuire

Sentiti libero di:
- Aggiungere nuove funzionalità
- Migliorare il codice esistente
- Segnalare bug
- Suggerire nuove app

## 📄 Licenza

Questo progetto è rilasciato nel pubblico dominio. Usa liberamente per qualsiasi scopo.

## 👨‍💻 Autore

Creato come raccolta di progetti Python utili e divertenti.
