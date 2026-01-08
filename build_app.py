#!/usr/bin/env python3
"""
Script per impacchettare l'applicazione in un eseguibile
"""

import subprocess
import sys
import os
from pathlib import Path


def build_app(app_name: str = "visual_art.py", onefile: bool = True, windowed: bool = False):
    """
    Costruisce un eseguibile usando PyInstaller
    
    Args:
        app_name: Nome del file Python da impacchettare
        onefile: Se True, crea un singolo file eseguibile
        windowed: Se True, nasconde la console (solo Windows/macOS)
    """
    if not os.path.exists(app_name):
        print(f"Errore: File {app_name} non trovato!")
        return False
    
    print(f"Costruzione dell'eseguibile per {app_name}...")
    
    # Nome dell'app senza estensione
    app_base = Path(app_name).stem
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--name", app_base,
        "--clean",
    ]
    
    if onefile:
        cmd.append("--onefile")
    
    if windowed:
        cmd.append("--windowed")
    else:
        cmd.append("--console")
    
    # Aggiungi icona se esiste
    icon_path = f"{app_base}.ico"
    if os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
    
    # Aggiungi il file principale
    cmd.append(app_name)
    
    print(f"Eseguendo: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✓ Eseguibile creato con successo!")
        print(f"  Posizione: dist/{app_base}")
        if sys.platform == "win32":
            print(f"  File: dist/{app_base}.exe")
        else:
            print(f"  File: dist/{app_base}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Errore durante la build: {e}")
        return False
    except FileNotFoundError:
        print("\n✗ PyInstaller non trovato!")
        print("  Installa con: pip install pyinstaller")
        return False


def main():
    """Funzione principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Impacchetta un'applicazione Python")
    parser.add_argument("app", nargs="?", default="visual_art.py",
                       help="File Python da impacchettare (default: visual_art.py)")
    parser.add_argument("--no-onefile", action="store_true",
                       help="Crea una cartella invece di un singolo file")
    parser.add_argument("--windowed", action="store_true",
                       help="Nasconde la console (solo Windows/macOS)")
    
    args = parser.parse_args()
    
    onefile = not args.no_onefile
    success = build_app(args.app, onefile=onefile, windowed=args.windowed)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
