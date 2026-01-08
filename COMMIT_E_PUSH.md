# Istruzioni per Commit e Push su GitHub

## ✅ Eseguibile Creato

L'eseguibile di **Fattura Pro** è stato creato con successo:
- **File:** `dist/fattura_pro`
- **Dimensione:** ~25-30 MB
- **Pronto per la distribuzione**

## 📝 Passi per Caricare su GitHub

### 1. Configura Git (se non già fatto)

```bash
git config --global user.name "Il Tuo Nome"
git config --global user.email "tua-email@esempio.com"
```

Oppure solo per questo repository:
```bash
git config user.name "Il Tuo Nome"
git config user.email "tua-email@esempio.com"
```

### 2. Fai il Commit

```bash
cd /home/cobra/Progetti/python-test

# Verifica i file da committare
git status

# Fai il commit
git commit -m "Aggiunto Fattura Pro - Generatore professionale di fatture italiane

- Interfaccia moderna e fluida
- Conforme alle normative italiane
- Auto-numerazione fatture
- Validazione P.IVA italiana
- PDF professionale con layout ottimizzato
- Riepilogo dettagliato per aliquota IVA
- Supporto dati bancari (IBAN)
- Eseguibile impacchettato incluso"
```

### 3. Crea Repository su GitHub (se non esiste)

1. Vai su https://github.com
2. Clicca su "New repository" (o il pulsante "+" in alto a destra)
3. Scegli un nome (es: "python-projects" o "fattura-pro")
4. **NON** inizializzare con README, .gitignore o licenza (già presenti)
5. Clicca "Create repository"

### 4. Collega e Carica

```bash
# Aggiungi il remote (sostituisci USERNAME e REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Oppure se usi SSH:
# git remote add origin git@github.com:USERNAME/REPO_NAME.git

# Rinomina il branch in main (opzionale ma consigliato)
git branch -M main

# Carica su GitHub
git push -u origin main
```

### 5. Verifica

Vai sul tuo repository su GitHub e verifica che tutti i file siano stati caricati.

## 📦 File Inclusi nel Repository

- ✅ `fattura_pro.py` - Programma principale
- ✅ `fattura_generator.py` - Versione base
- ✅ `README.md` - Documentazione aggiornata
- ✅ `requirements.txt` - Dipendenze
- ✅ `build_app.py` - Script per impacchettare
- ✅ `build_windows.bat` - Script Windows
- ✅ Altri progetti Python

## ⚠️ File Esclusi (grazie a .gitignore)

- `dist/` - Eseguibili (troppo grandi per git)
- `build/` - File temporanei
- `.venv/` - Virtual environment
- `*.spec` - File PyInstaller
- `fattura_*.json` - Dati fatture salvate
- `fattura_pro_settings.json` - Impostazioni

## 💡 Note

- Gli eseguibili sono troppo grandi per GitHub (limite 100MB)
- Se vuoi distribuire gli eseguibili, usa GitHub Releases
- Il codice sorgente è completo e funzionante

## 🚀 GitHub Releases (Opzionale)

Per distribuire gli eseguibili:

1. Vai su "Releases" nel tuo repository GitHub
2. Clicca "Create a new release"
3. Tag: `v1.0.0`
4. Titolo: `Fattura Pro v1.0.0`
5. Carica `dist/fattura_pro` come asset
