# Istruzioni per Caricare su GitHub

## 1. Configura Git (se non già fatto)

```bash
git config --global user.name "Il Tuo Nome"
git config --global user.email "tua-email@esempio.com"
```

Oppure solo per questo repository:
```bash
git config user.name "Il Tuo Nome"
git config user.email "tua-email@esempio.com"
```

## 2. Crea il Repository su GitHub

1. Vai su https://github.com
2. Clicca su "New repository" (o il pulsante "+" in alto a destra)
3. Scegli un nome per il repository (es: "python-projects")
4. **NON** inizializzare con README, .gitignore o licenza (già li abbiamo)
5. Clicca "Create repository"

## 3. Collega il Repository Locale a GitHub

GitHub ti mostrerà le istruzioni. Esegui questi comandi (sostituisci USERNAME e REPO_NAME):

```bash
cd /home/cobra/Progetti/python-test

# Aggiungi il remote (sostituisci con il tuo URL)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Oppure se usi SSH:
# git remote add origin git@github.com:USERNAME/REPO_NAME.git

# Rinomina il branch in main (opzionale, ma consigliato)
git branch -M main

# Fai il commit iniziale (se non già fatto)
git commit -m "Initial commit: Python projects collection"

# Carica su GitHub
git push -u origin main
```

## 4. Verifica

Vai sul tuo repository su GitHub e verifica che tutti i file siano stati caricati.

## Comandi Utili

```bash
# Verifica lo stato
git status

# Aggiungi modifiche
git add .
git commit -m "Descrizione delle modifiche"

# Carica modifiche
git push

# Vedi i remote configurati
git remote -v
```

## Note

- I file in `.gitignore` (build/, dist/, .venv/, etc.) non verranno caricati
- Il file `todos.json` e `fattura_settings.json` sono esclusi per privacy
- Gli eseguibili in `dist/` non vengono caricati (sono troppo grandi)
