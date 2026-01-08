#!/usr/bin/env python3
"""
Fattura Pro - Generatore Professionale di Fatture Italiane
Versione migliorata con design moderno e conforme alle normative italiane
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional


try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm, mm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
        PageBreak, KeepTogether
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# Colori moderni per l'interfaccia
COLOR_PRIMARY = "#2563eb"  # Blu moderno
COLOR_SECONDARY = "#10b981"  # Verde
COLOR_DANGER = "#ef4444"  # Rosso
COLOR_BG = "#f8fafc"  # Grigio chiaro
COLOR_CARD = "#ffffff"  # Bianco


class ModernEntry(ttk.Frame):
    """Entry widget moderno con label integrata"""
    
    def __init__(self, parent, label, width=30, **kwargs):
        super().__init__(parent)
        self.label = ttk.Label(self, text=label, font=("Segoe UI", 9))
        self.label.pack(anchor=tk.W, pady=(0, 2))
        self.entry = ttk.Entry(self, width=width, font=("Segoe UI", 10), **kwargs)
        self.entry.pack(fill=tk.X, ipady=4)
    
    def get(self):
        return self.entry.get()
    
    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def delete(self, first, last=None):
        self.entry.delete(first, last)
    
    def insert(self, index, string):
        self.entry.insert(index, string)


class FatturaPro:
    """Generatore professionale di fatture italiane"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Fattura Pro - Generatore Fatture Italiane")
        self.root.geometry("1100x750")
        self.root.configure(bg=COLOR_BG)
        
        # Stile moderno
        self.setup_styles()
        
        # Dati
        self.dati_azienda = self.init_dati_azienda()
        self.dati_cliente = self.init_dati_cliente()
        self.prodotti: List[Dict] = []
        self.numero_fattura = ""
        self.data_fattura = datetime.now().strftime("%d/%m/%Y")
        self.data_scadenza = ""
        self.tipo_fattura = "Fattura"  # Fattura, Nota di Credito, etc.
        self.condizioni_pagamento = ""
        self.causale = ""
        self.note = ""
        self.banca_iban = ""
        self.banca_nome = ""
        
        self.setup_ui()
        self.load_settings()
        self.auto_numero_fattura()
    
    def setup_styles(self):
        """Configura gli stili moderni"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Stile per i pulsanti principali
        style.configure('Primary.TButton',
                      font=('Segoe UI', 10, 'bold'),
                      padding=10)
        
        style.configure('Success.TButton',
                      font=('Segoe UI', 10),
                      padding=8)
    
    def init_dati_azienda(self) -> Dict:
        """Inizializza i dati azienda"""
        return {
            "ragione_sociale": "",
            "indirizzo": "",
            "citta": "",
            "cap": "",
            "provincia": "",
            "p_iva": "",
            "codice_fiscale": "",
            "pec": "",
            "telefono": "",
            "email": "",
            "sito_web": "",
            "rea": "",  # Numero REA
            "capitale_sociale": ""
        }
    
    def init_dati_cliente(self) -> Dict:
        """Inizializza i dati cliente"""
        return {
            "ragione_sociale": "",
            "indirizzo": "",
            "citta": "",
            "cap": "",
            "provincia": "",
            "p_iva": "",
            "codice_fiscale": "",
            "pec": "",
            "codice_destinatario": "",  # SDI
            "telefono": "",
            "email": ""
        }
    
    def setup_ui(self):
        """Crea l'interfaccia utente moderna"""
        # Header
        header = tk.Frame(self.root, bg=COLOR_PRIMARY, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="FATTURA PRO", 
                        font=("Segoe UI", 18, "bold"),
                        bg=COLOR_PRIMARY, fg="white")
        title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Status bar
        self.status_label = tk.Label(header, text="Pronto", 
                                    font=("Segoe UI", 9),
                                    bg=COLOR_PRIMARY, fg="white")
        self.status_label.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Container principale
        main_container = tk.Frame(self.root, bg=COLOR_BG)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook con stile moderno
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab
        self.create_azienda_tab()
        self.create_cliente_tab()
        self.create_prodotti_tab()
        self.create_fattura_tab()
        self.create_riepilogo_tab()
        
        # Barra azioni
        self.create_action_bar()
    
    def create_azienda_tab(self):
        """Tab dati azienda"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="🏢 Azienda")
        
        # Scrollable frame
        canvas_frame = tk.Canvas(tab, bg=COLOR_BG)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas_frame.yview)
        scrollable = tk.Frame(canvas_frame, bg=COLOR_BG)
        
        scrollable.bind("<Configure>", lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")))
        canvas_frame.create_window((0, 0), window=scrollable, anchor="nw")
        canvas_frame.configure(yscrollcommand=scrollbar.set)
        
        # Form azienda
        fields = [
            ("Ragione Sociale *", "ragione_sociale", 40),
            ("Indirizzo *", "indirizzo", 40),
            ("Città *", "citta", 20),
            ("CAP *", "cap", 10),
            ("Provincia", "provincia", 10),
            ("Partita IVA *", "p_iva", 20),
            ("Codice Fiscale", "codice_fiscale", 20),
            ("PEC", "pec", 30),
            ("Telefono", "telefono", 20),
            ("Email", "email", 30),
            ("Sito Web", "sito_web", 30),
            ("Numero REA", "rea", 20),
            ("Capitale Sociale", "capitale_sociale", 20),
        ]
        
        self.entries_azienda = {}
        row = 0
        for label, key, width in fields:
            entry = ModernEntry(scrollable, label, width=width)
            entry.grid(row=row, column=0, sticky=tk.EW, padx=10, pady=8)
            self.entries_azienda[key] = entry
            row += 1
        
        scrollable.columnconfigure(0, weight=1)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_cliente_tab(self):
        """Tab dati cliente"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="👤 Cliente")
        
        canvas_frame = tk.Canvas(tab, bg=COLOR_BG)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas_frame.yview)
        scrollable = tk.Frame(canvas_frame, bg=COLOR_BG)
        
        scrollable.bind("<Configure>", lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")))
        canvas_frame.create_window((0, 0), window=scrollable, anchor="nw")
        canvas_frame.configure(yscrollcommand=scrollbar.set)
        
        fields = [
            ("Ragione Sociale *", "ragione_sociale", 40),
            ("Indirizzo *", "indirizzo", 40),
            ("Città *", "citta", 20),
            ("CAP *", "cap", 10),
            ("Provincia", "provincia", 10),
            ("Partita IVA", "p_iva", 20),
            ("Codice Fiscale", "codice_fiscale", 20),
            ("PEC", "pec", 30),
            ("Codice Destinatario (SDI)", "codice_destinatario", 20),
            ("Telefono", "telefono", 20),
            ("Email", "email", 30),
        ]
        
        self.entries_cliente = {}
        row = 0
        for label, key, width in fields:
            entry = ModernEntry(scrollable, label, width=width)
            entry.grid(row=row, column=0, sticky=tk.EW, padx=10, pady=8)
            self.entries_cliente[key] = entry
            row += 1
        
        scrollable.columnconfigure(0, weight=1)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_prodotti_tab(self):
        """Tab prodotti con design migliorato"""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="📦 Prodotti/Servizi")
        
        # Frame principale
        main_frame = tk.Frame(tab, bg=COLOR_BG)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista prodotti
        list_frame = tk.LabelFrame(main_frame, text="Lista Prodotti", 
                                   font=("Segoe UI", 10, "bold"),
                                   bg=COLOR_BG, fg=COLOR_PRIMARY)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview migliorato
        columns = ("#", "Descrizione", "Q.tà", "Prezzo Unit.", "IVA %", "Totale")
        self.tree_prodotti = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        widths = [40, 300, 80, 100, 80, 120]
        for col, width in zip(columns, widths):
            self.tree_prodotti.heading(col, text=col)
            self.tree_prodotti.column(col, width=width, anchor=tk.CENTER if col != "Descrizione" else tk.W)
        
        scrollbar_tree = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree_prodotti.yview)
        self.tree_prodotti.configure(yscrollcommand=scrollbar_tree.set)
        
        self.tree_prodotti.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Form aggiunta prodotto
        form_frame = tk.LabelFrame(main_frame, text="Aggiungi Prodotto/Servizio",
                                  font=("Segoe UI", 10, "bold"),
                                  bg=COLOR_BG, fg=COLOR_PRIMARY)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Grid per i campi
        fields_frame = tk.Frame(form_frame, bg=COLOR_BG)
        fields_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(fields_frame, text="Descrizione *:", font=("Segoe UI", 9)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_desc = ttk.Entry(fields_frame, width=40, font=("Segoe UI", 10))
        self.entry_desc.grid(row=0, column=1, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(fields_frame, text="Quantità:", font=("Segoe UI", 9)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_qty = ttk.Entry(fields_frame, width=10, font=("Segoe UI", 10))
        self.entry_qty.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.entry_qty.insert(0, "1.00")
        
        ttk.Label(fields_frame, text="Prezzo Unit. (€):", font=("Segoe UI", 9)).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_prezzo = ttk.Entry(fields_frame, width=12, font=("Segoe UI", 10))
        self.entry_prezzo.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(fields_frame, text="IVA %:", font=("Segoe UI", 9)).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_iva = ttk.Combobox(fields_frame, width=10, font=("Segoe UI", 10),
                                      values=["0", "4", "5", "10", "22"], state="readonly")
        self.entry_iva.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.entry_iva.set("22")
        
        fields_frame.columnconfigure(1, weight=1)
        
        # Pulsanti
        btn_frame = tk.Frame(form_frame, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="➕ Aggiungi", command=self.aggiungi_prodotto,
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✏️ Modifica", command=self.modifica_prodotto).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Rimuovi", command=self.rimuovi_prodotto).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Svuota", command=self.svuota_prodotti).pack(side=tk.LEFT, padx=5)
        
        # Totale
        total_frame = tk.Frame(main_frame, bg=COLOR_BG)
        total_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.label_totale = tk.Label(total_frame, text="Totale: € 0.00", 
                                    font=("Segoe UI", 14, "bold"),
                                    bg=COLOR_BG, fg=COLOR_PRIMARY)
        self.label_totale.pack(side=tk.RIGHT, padx=10)
    
    def create_fattura_tab(self):
        """Tab dettagli fattura"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="📄 Fattura")
        
        canvas_frame = tk.Canvas(tab, bg=COLOR_BG)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas_frame.yview)
        scrollable = tk.Frame(canvas_frame, bg=COLOR_BG)
        
        scrollable.bind("<Configure>", lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")))
        canvas_frame.create_window((0, 0), window=scrollable, anchor="nw")
        canvas_frame.configure(yscrollcommand=scrollbar.set)
        
        # Dati fattura
        fields = [
            ("Tipo Documento", "tipo_fattura"),
            ("Numero Fattura *", "numero_fattura"),
            ("Data Fattura *", "data_fattura"),
            ("Data Scadenza", "data_scadenza"),
            ("Condizioni di Pagamento", "condizioni_pagamento"),
            ("Causale", "causale"),
        ]
        
        self.entries_fattura = {}
        row = 0
        for label, key in fields:
            if key == "tipo_fattura":
                frame = tk.Frame(scrollable, bg=COLOR_BG)
                frame.grid(row=row, column=0, sticky=tk.EW, padx=10, pady=8)
                ttk.Label(frame, text=label + ":", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 10))
                combo = ttk.Combobox(frame, values=["Fattura", "Nota di Credito", "Nota di Debito"],
                                    state="readonly", width=20, font=("Segoe UI", 10))
                combo.set("Fattura")
                combo.pack(side=tk.LEFT)
                self.entries_fattura[key] = combo
            else:
                entry = ModernEntry(scrollable, label, width=30)
                entry.grid(row=row, column=0, sticky=tk.EW, padx=10, pady=8)
                self.entries_fattura[key] = entry
            row += 1
        
        # Data default
        if "data_fattura" in self.entries_fattura:
            self.entries_fattura["data_fattura"].set(self.data_fattura)
        
        # Note
        note_frame = tk.LabelFrame(scrollable, text="Note", font=("Segoe UI", 10, "bold"),
                                  bg=COLOR_BG, fg=COLOR_PRIMARY)
        note_frame.grid(row=row, column=0, sticky=tk.EW, padx=10, pady=10)
        note_frame.columnconfigure(0, weight=1)
        
        self.text_note = tk.Text(note_frame, height=8, width=50, font=("Segoe UI", 10),
                                 wrap=tk.WORD, relief=tk.FLAT, borderwidth=1)
        self.text_note.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Dati bancari
        row += 1
        bank_frame = tk.LabelFrame(scrollable, text="Dati Bancari", font=("Segoe UI", 10, "bold"),
                                  bg=COLOR_BG, fg=COLOR_PRIMARY)
        bank_frame.grid(row=row, column=0, sticky=tk.EW, padx=10, pady=10)
        
        ttk.Label(bank_frame, text="IBAN:", font=("Segoe UI", 9)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_iban = ttk.Entry(bank_frame, width=35, font=("Segoe UI", 10))
        self.entry_iban.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(bank_frame, text="Banca:", font=("Segoe UI", 9)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_banca = ttk.Entry(bank_frame, width=35, font=("Segoe UI", 10))
        self.entry_banca.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        bank_frame.columnconfigure(1, weight=1)
        scrollable.columnconfigure(0, weight=1)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_riepilogo_tab(self):
        """Tab riepilogo con calcoli"""
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="📊 Riepilogo")
        
        frame = tk.Frame(tab, bg=COLOR_BG)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Calcoli
        calc_frame = tk.LabelFrame(frame, text="Calcoli Fattura", 
                                  font=("Segoe UI", 12, "bold"),
                                  bg=COLOR_BG, fg=COLOR_PRIMARY)
        calc_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.label_imponibile = tk.Label(calc_frame, text="Imponibile: € 0.00",
                                         font=("Segoe UI", 11), bg=COLOR_BG)
        self.label_imponibile.pack(anchor=tk.W, padx=20, pady=5)
        
        self.label_iva = tk.Label(calc_frame, text="IVA: € 0.00",
                                  font=("Segoe UI", 11), bg=COLOR_BG)
        self.label_iva.pack(anchor=tk.W, padx=20, pady=5)
        
        self.label_totale_riepilogo = tk.Label(calc_frame, text="TOTALE: € 0.00",
                                                font=("Segoe UI", 16, "bold"),
                                                bg=COLOR_BG, fg=COLOR_PRIMARY)
        self.label_totale_riepilogo.pack(anchor=tk.W, padx=20, pady=15)
        
        # Anteprima
        preview_frame = tk.LabelFrame(frame, text="Anteprima Dati",
                                      font=("Segoe UI", 12, "bold"),
                                      bg=COLOR_BG, fg=COLOR_PRIMARY)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.text_preview = tk.Text(preview_frame, height=15, font=("Courier", 9),
                                   wrap=tk.WORD, bg="white", relief=tk.SUNKEN)
        self.text_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(preview_frame, text="🔄 Aggiorna Anteprima", 
                  command=self.aggiorna_anteprima).pack(pady=5)
    
    def create_action_bar(self):
        """Barra azioni principale"""
        action_frame = tk.Frame(self.root, bg=COLOR_BG, height=70)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        action_frame.pack_propagate(False)
        
        # Pulsanti principali
        btn_frame = tk.Frame(action_frame, bg=COLOR_BG)
        btn_frame.pack(expand=True)
        
        ttk.Button(btn_frame, text="💾 Salva Dati", command=self.salva_dati,
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📂 Carica Dati", command=self.carica_dati,
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Nuova Fattura", command=self.nuova_fattura,
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📄 Genera PDF", command=self.genera_pdf,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=10)
    
    def auto_numero_fattura(self):
        """Genera automaticamente il numero fattura"""
        if not self.numero_fattura:
            # Cerca l'ultimo numero usato
            last_num = self.get_last_fattura_num()
            new_num = last_num + 1
            self.numero_fattura = f"FAT-{datetime.now().year}-{new_num:04d}"
            if "numero_fattura" in self.entries_fattura:
                self.entries_fattura["numero_fattura"].set(self.numero_fattura)
    
    def get_last_fattura_num(self) -> int:
        """Recupera l'ultimo numero fattura usato"""
        # Cerca file JSON salvati
        max_num = 0
        for file in Path(".").glob("fattura_*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "fattura" in data and "numero" in data["fattura"]:
                        num_str = data["fattura"]["numero"]
                        # Estrai numero
                        match = re.search(r'(\d{4})$', num_str)
                        if match:
                            max_num = max(max_num, int(match.group(1)))
            except:
                pass
        return max_num
    
    def aggiungi_prodotto(self):
        """Aggiunge un prodotto"""
        try:
            descrizione = self.entry_desc.get().strip()
            if not descrizione:
                messagebox.showwarning("Attenzione", "Inserisci una descrizione")
                return
            
            quantita = float(self.entry_qty.get() or "1")
            prezzo = float(self.entry_prezzo.get() or "0")
            iva = float(self.entry_iva.get() or "22")
            
            imponibile = quantita * prezzo
            iva_importo = imponibile * (iva / 100)
            totale = imponibile + iva_importo
            
            prodotto = {
                "descrizione": descrizione,
                "quantita": quantita,
                "prezzo": prezzo,
                "iva": iva,
                "imponibile": imponibile,
                "iva_importo": iva_importo,
                "totale": totale
            }
            
            self.prodotti.append(prodotto)
            self.aggiorna_lista_prodotti()
            
            # Pulisci campi
            self.entry_desc.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
            self.entry_qty.insert(0, "1.00")
            self.entry_prezzo.delete(0, tk.END)
            self.entry_iva.set("22")
            
            self.aggiorna_totali()
            self.status_label.config(text=f"Prodotto aggiunto: {descrizione[:30]}...")
            
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi")
    
    def modifica_prodotto(self):
        """Modifica il prodotto selezionato"""
        selected = self.tree_prodotti.selection()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona un prodotto da modificare")
            return
        
        item = selected[0]
        index = int(self.tree_prodotti.item(item, "values")[0]) - 1
        
        if 0 <= index < len(self.prodotti):
            p = self.prodotti[index]
            self.entry_desc.insert(0, p["descrizione"])
            self.entry_qty.insert(0, str(p["quantita"]))
            self.entry_prezzo.insert(0, str(p["prezzo"]))
            self.entry_iva.set(str(int(p["iva"])))
            
            # Rimuovi e riaggiungi
            self.rimuovi_prodotto()
    
    def rimuovi_prodotto(self):
        """Rimuove il prodotto selezionato"""
        selected = self.tree_prodotti.selection()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona un prodotto da rimuovere")
            return
        
        for item in selected:
            index = int(self.tree_prodotti.item(item, "values")[0]) - 1
            if 0 <= index < len(self.prodotti):
                self.tree_prodotti.delete(item)
                del self.prodotti[index]
        
        self.aggiorna_lista_prodotti()
        self.aggiorna_totali()
    
    def svuota_prodotti(self):
        """Svuota tutti i prodotti"""
        if messagebox.askyesno("Conferma", "Vuoi rimuovere tutti i prodotti?"):
            self.prodotti.clear()
            for item in self.tree_prodotti.get_children():
                self.tree_prodotti.delete(item)
            self.aggiorna_totali()
    
    def aggiorna_lista_prodotti(self):
        """Aggiorna la lista prodotti nel treeview"""
        # Svuota
        for item in self.tree_prodotti.get_children():
            self.tree_prodotti.delete(item)
        
        # Riempie
        for i, p in enumerate(self.prodotti, 1):
            self.tree_prodotti.insert("", tk.END, values=(
                i,
                p["descrizione"],
                f"{p['quantita']:.2f}",
                f"€ {p['prezzo']:.2f}",
                f"{p['iva']:.0f}%",
                f"€ {p['totale']:.2f}"
            ))
    
    def aggiorna_totali(self):
        """Aggiorna i totali"""
        totale_imponibile = sum(p["imponibile"] for p in self.prodotti)
        totale_iva = sum(p["iva_importo"] for p in self.prodotti)
        totale_generale = totale_imponibile + totale_iva
        
        self.label_totale.config(text=f"Totale: € {totale_generale:.2f}")
        self.label_imponibile.config(text=f"Imponibile: € {totale_imponibile:.2f}")
        self.label_iva.config(text=f"IVA: € {totale_iva:.2f}")
        self.label_totale_riepilogo.config(text=f"TOTALE: € {totale_generale:.2f}")
    
    def aggiorna_anteprima(self):
        """Aggiorna l'anteprima"""
        self.get_all_data()
        
        preview = f"""
FATTURA {self.tipo_fattura.upper()}
{'='*50}

AZIENDA:
{self.dati_azienda['ragione_sociale']}
{self.dati_azienda['indirizzo']}
{self.dati_azienda['cap']} {self.dati_azienda['citta']}
P.IVA: {self.dati_azienda['p_iva']}

CLIENTE:
{self.dati_cliente['ragione_sociale']}
{self.dati_cliente['indirizzo']}
{self.dati_cliente['cap']} {self.dati_cliente['citta']}

FATTURA N. {self.numero_fattura}
Data: {self.data_fattura}
Scadenza: {self.data_scadenza or 'N/A'}

PRODOTTI:
{chr(10).join([f"{i+1}. {p['descrizione']} - Q.tà: {p['quantita']:.2f} - € {p['totale']:.2f}" for i, p in enumerate(self.prodotti)])}

TOTALE: € {sum(p['totale'] for p in self.prodotti):.2f}
"""
        self.text_preview.delete("1.0", tk.END)
        self.text_preview.insert("1.0", preview)
    
    def get_all_data(self):
        """Recupera tutti i dati dai form"""
        # Azienda
        for key in self.dati_azienda:
            if key in self.entries_azienda:
                self.dati_azienda[key] = self.entries_azienda[key].get()
        
        # Cliente
        for key in self.dati_cliente:
            if key in self.entries_cliente:
                self.dati_cliente[key] = self.entries_cliente[key].get()
        
        # Fattura
        self.tipo_fattura = self.entries_fattura["tipo_fattura"].get()
        self.numero_fattura = self.entries_fattura["numero_fattura"].get()
        self.data_fattura = self.entries_fattura["data_fattura"].get()
        self.data_scadenza = self.entries_fattura["data_scadenza"].get()
        self.condizioni_pagamento = self.entries_fattura["condizioni_pagamento"].get()
        self.causale = self.entries_fattura["causale"].get()
        self.note = self.text_note.get("1.0", tk.END).strip()
        self.banca_iban = self.entry_iban.get()
        self.banca_nome = self.entry_banca.get()
    
    def valida_dati(self) -> tuple[bool, str]:
        """Valida i dati inseriti"""
        # Azienda obbligatoria
        if not self.dati_azienda.get("ragione_sociale"):
            return False, "Inserisci la ragione sociale dell'azienda"
        if not self.dati_azienda.get("p_iva"):
            return False, "Inserisci la Partita IVA dell'azienda"
        
        # Cliente obbligatorio
        if not self.dati_cliente.get("ragione_sociale"):
            return False, "Inserisci la ragione sociale del cliente"
        
        # Fattura
        if not self.numero_fattura:
            return False, "Inserisci il numero fattura"
        if not self.data_fattura:
            return False, "Inserisci la data fattura"
        
        # Prodotti
        if not self.prodotti:
            return False, "Aggiungi almeno un prodotto/servizio"
        
        # Valida P.IVA italiana (11 cifre)
        piva_azienda = self.dati_azienda.get("p_iva", "").replace(" ", "")
        if piva_azienda and (len(piva_azienda) != 11 or not piva_azienda.isdigit()):
            return False, "Partita IVA azienda non valida (deve essere di 11 cifre)"
        
        piva_cliente = self.dati_cliente.get("p_iva", "").replace(" ", "")
        if piva_cliente and (len(piva_cliente) != 11 or not piva_cliente.isdigit()):
            return False, "Partita IVA cliente non valida (deve essere di 11 cifre)"
        
        return True, ""
    
    def genera_pdf(self):
        """Genera il PDF della fattura"""
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Errore", 
                               "reportlab non installato!\nInstalla con: pip install reportlab")
            return
        
        self.get_all_data()
        valid, error = self.valida_dati()
        if not valid:
            messagebox.showerror("Errore Validazione", error)
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Fattura_{self.numero_fattura.replace('/', '_')}.pdf"
        )
        
        if not filename:
            return
        
        try:
            self.create_pdf_professionale(filename)
            messagebox.showinfo("Successo", f"Fattura generata:\n{filename}")
            self.status_label.config(text="PDF generato con successo")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella generazione PDF:\n{str(e)}")
            self.status_label.config(text="Errore nella generazione PDF")
    
    def create_pdf_professionale(self, filename):
        """Crea un PDF professionale con design italiano"""
        doc = SimpleDocTemplate(filename, pagesize=A4,
                               rightMargin=2*cm, leftMargin=2*cm,
                               topMargin=2*cm, bottomMargin=2*cm)
        story = []
        styles = getSampleStyleSheet()
        
        # Stili personalizzati
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        header_style = ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            spaceAfter=5,
            fontName='Helvetica'
        )
        
        # Titolo
        story.append(Paragraph(f"<b>{self.tipo_fattura.upper()}</b>", title_style))
        story.append(Spacer(1, 0.3*cm))
        
        # Linea decorativa
        story.append(Spacer(1, 0.2*cm))
        
        # Dati azienda e cliente in due colonne
        azienda_text = f"""
        <b>{self.dati_azienda['ragione_sociale']}</b><br/>
        {self.dati_azienda['indirizzo']}<br/>
        {self.dati_azienda['cap']} {self.dati_azienda['citta']}
        {f"({self.dati_azienda['provincia']})" if self.dati_azienda.get('provincia') else ""}<br/>
        P.IVA: {self.dati_azienda['p_iva']}<br/>
        {f"CF: {self.dati_azienda['codice_fiscale']}<br/>" if self.dati_azienda.get('codice_fiscale') else ""}
        {f"PEC: {self.dati_azienda['pec']}<br/>" if self.dati_azienda.get('pec') else ""}
        {f"Tel: {self.dati_azienda['telefono']}<br/>" if self.dati_azienda.get('telefono') else ""}
        {f"Email: {self.dati_azienda['email']}" if self.dati_azienda.get('email') else ""}
        """
        
        cliente_text = f"""
        <b>Cliente:</b><br/>
        {self.dati_cliente['ragione_sociale']}<br/>
        {self.dati_cliente['indirizzo']}<br/>
        {self.dati_cliente['cap']} {self.dati_cliente['citta']}
        {f"({self.dati_cliente['provincia']})" if self.dati_cliente.get('provincia') else ""}<br/>
        {f"P.IVA: {self.dati_cliente['p_iva']}<br/>" if self.dati_cliente.get('p_iva') else ""}
        {f"CF: {self.dati_cliente['codice_fiscale']}<br/>" if self.dati_cliente.get('codice_fiscale') else ""}
        {f"Cod. Dest.: {self.dati_cliente['codice_destinatario']}" if self.dati_cliente.get('codice_destinatario') else ""}
        """
        
        # Tabella a due colonne
        dati_table_data = [
            [Paragraph(azienda_text, header_style), Paragraph(cliente_text, header_style)]
        ]
        dati_table = Table(dati_table_data, colWidths=[9*cm, 9*cm])
        dati_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(dati_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Dettagli fattura
        dettagli_data = [
            ["<b>Numero Fattura:</b>", self.numero_fattura],
            ["<b>Data Fattura:</b>", self.data_fattura],
            ["<b>Data Scadenza:</b>", self.data_scadenza or "N/A"],
            ["<b>Pagamento:</b>", self.condizioni_pagamento or "N/A"],
        ]
        
        dettagli_table = Table(dettagli_data, colWidths=[5*cm, 13*cm])
        dettagli_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
        ]))
        story.append(dettagli_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Tabella prodotti
        prodotti_data = [["#", "Descrizione", "Q.tà", "Prezzo Unit.", "IVA %", "Totale"]]
        
        totale_imponibile = 0
        totale_iva = 0
        iva_breakdown = {}  # Raggruppa per aliquota IVA
        
        for i, p in enumerate(self.prodotti, 1):
            prodotti_data.append([
                str(i),
                p['descrizione'],
                f"{p['quantita']:.2f}",
                f"€ {p['prezzo']:.2f}",
                f"{p['iva']:.0f}%",
                f"€ {p['totale']:.2f}"
            ])
            totale_imponibile += p['imponibile']
            totale_iva += p['iva_importo']
            
            # Raggruppa per IVA
            iva_key = f"{p['iva']:.0f}%"
            if iva_key not in iva_breakdown:
                iva_breakdown[iva_key] = {'imponibile': 0, 'iva': 0}
            iva_breakdown[iva_key]['imponibile'] += p['imponibile']
            iva_breakdown[iva_key]['iva'] += p['iva_importo']
        
        # Totali per aliquota IVA
        for iva_key in sorted(iva_breakdown.keys(), key=lambda x: float(x.replace('%', ''))):
            imp = iva_breakdown[iva_key]['imponibile']
            iva_imp = iva_breakdown[iva_key]['iva']
            prodotti_data.append([
                "", "", "", "",
                f"<b>Imponibile {iva_key}:</b>",
                f"<b>€ {imp:.2f}</b>"
            ])
            prodotti_data.append([
                "", "", "", "",
                f"<b>IVA {iva_key}:</b>",
                f"<b>€ {iva_imp:.2f}</b>"
            ])
        
        # Totali generali
        totale_generale = totale_imponibile + totale_iva
        prodotti_data.append(["", "", "", "", "", ""])
        prodotti_data.append([
            "", "", "", "",
            "<b>Totale Imponibile:</b>",
            f"<b>€ {totale_imponibile:.2f}</b>"
        ])
        prodotti_data.append([
            "", "", "", "",
            "<b>Totale IVA:</b>",
            f"<b>€ {totale_iva:.2f}</b>"
        ])
        prodotti_data.append([
            "", "", "", "",
            "<b>TOTALE FATTURA:</b>",
            f"<b>€ {totale_generale:.2f}</b>"
        ])
        
        prodotti_table = Table(prodotti_data, colWidths=[1*cm, 7*cm, 1.5*cm, 2*cm, 1.5*cm, 2.5*cm])
        prodotti_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('ALIGN', (4, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -len(prodotti_data)+len([x for x in prodotti_data if len(x) > 0 and x[0] == ""])), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -len([x for x in prodotti_data if len(x) > 0 and x[0] == ""])-1), [colors.white, colors.HexColor('#f9fafb')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('FONTNAME', (4, -4), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (4, -4), (-1, -1), 11),
            ('BACKGROUND', (4, -3), (-1, -1), colors.HexColor('#fef3c7')),
            ('TEXTCOLOR', (4, -1), (-1, -1), colors.HexColor('#1e40af')),
            ('FONTSIZE', (4, -1), (-1, -1), 14),
        ]))
        story.append(prodotti_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Dati bancari
        if self.banca_iban or self.banca_nome:
            banca_text = f"<b>Dati Bancari:</b><br/>"
            if self.banca_nome:
                banca_text += f"Banca: {self.banca_nome}<br/>"
            if self.banca_iban:
                banca_text += f"IBAN: {self.banca_iban}"
            story.append(Paragraph(banca_text, header_style))
            story.append(Spacer(1, 0.3*cm))
        
        # Note
        if self.note:
            story.append(Paragraph(f"<b>Note:</b><br/>{self.note}", header_style))
            story.append(Spacer(1, 0.3*cm))
        
        # Causale
        if self.causale:
            story.append(Paragraph(f"<b>Causale:</b> {self.causale}", header_style))
        
        # Footer
        story.append(Spacer(1, 1*cm))
        footer_text = f"<i>Documento generato il {datetime.now().strftime('%d/%m/%Y alle %H:%M')} con Fattura Pro</i>"
        story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'], 
                                                          fontSize=8, textColor=colors.grey,
                                                          alignment=TA_CENTER)))
        
        doc.build(story)
    
    def salva_dati(self):
        """Salva i dati"""
        self.get_all_data()
        
        data = {
            "azienda": self.dati_azienda,
            "cliente": self.dati_cliente,
            "fattura": {
                "tipo": self.tipo_fattura,
                "numero": self.numero_fattura,
                "data": self.data_fattura,
                "scadenza": self.data_scadenza,
                "condizioni": self.condizioni_pagamento,
                "causale": self.causale,
                "note": self.note
            },
            "banca": {
                "iban": self.banca_iban,
                "nome": self.banca_nome
            },
            "prodotti": self.prodotti
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"fattura_{self.numero_fattura.replace('/', '_')}.json"
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Successo", "Dati salvati!")
            self.status_label.config(text="Dati salvati")
    
    def carica_dati(self):
        """Carica i dati"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Carica azienda
            if "azienda" in data:
                for key, value in data["azienda"].items():
                    if key in self.entries_azienda:
                        self.entries_azienda[key].set(value)
            
            # Carica cliente
            if "cliente" in data:
                for key, value in data["cliente"].items():
                    if key in self.entries_cliente:
                        self.entries_cliente[key].set(value)
            
            # Carica fattura
            if "fattura" in data:
                f = data["fattura"]
                if "tipo" in f:
                    self.entries_fattura["tipo_fattura"].set(f["tipo"])
                if "numero" in f:
                    self.entries_fattura["numero_fattura"].set(f["numero"])
                if "data" in f:
                    self.entries_fattura["data_fattura"].set(f["data"])
                if "scadenza" in f:
                    self.entries_fattura["data_scadenza"].set(f["scadenza"])
                if "condizioni" in f:
                    self.entries_fattura["condizioni_pagamento"].set(f["condizioni"])
                if "causale" in f:
                    self.entries_fattura["causale"].set(f["causale"])
                if "note" in f:
                    self.text_note.delete("1.0", tk.END)
                    self.text_note.insert("1.0", f.get("note", ""))
            
            # Carica banca
            if "banca" in data:
                self.entry_iban.delete(0, tk.END)
                self.entry_iban.insert(0, data["banca"].get("iban", ""))
                self.entry_banca.delete(0, tk.END)
                self.entry_banca.insert(0, data["banca"].get("nome", ""))
            
            # Carica prodotti
            if "prodotti" in data:
                self.prodotti = data["prodotti"]
                self.aggiorna_lista_prodotti()
                self.aggiorna_totali()
            
            messagebox.showinfo("Successo", "Dati caricati!")
            self.status_label.config(text="Dati caricati")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel caricamento:\n{str(e)}")
    
    def nuova_fattura(self):
        """Crea una nuova fattura"""
        if messagebox.askyesno("Conferma", "Vuoi creare una nuova fattura?\nI dati non salvati andranno persi."):
            # Mantieni solo i dati azienda
            azienda_backup = {}
            for key in self.dati_azienda:
                if key in self.entries_azienda:
                    azienda_backup[key] = self.entries_azienda[key].get()
            
            # Reset
            self.dati_cliente = self.init_dati_cliente()
            self.prodotti = []
            self.numero_fattura = ""
            self.data_fattura = datetime.now().strftime("%d/%m/%Y")
            self.data_scadenza = ""
            self.condizioni_pagamento = ""
            self.causale = ""
            self.note = ""
            self.banca_iban = ""
            self.banca_nome = ""
            
            # Pulisci form
            for key in self.entries_cliente:
                self.entries_cliente[key].set("")
            
            for item in self.tree_prodotti.get_children():
                self.tree_prodotti.delete(item)
            
            self.entries_fattura["numero_fattura"].set("")
            self.entries_fattura["data_fattura"].set(self.data_fattura)
            self.entries_fattura["data_scadenza"].set("")
            self.entries_fattura["condizioni_pagamento"].set("")
            self.entries_fattura["causale"].set("")
            self.text_note.delete("1.0", tk.END)
            self.entry_iban.delete(0, tk.END)
            self.entry_banca.delete(0, tk.END)
            
            # Ripristina azienda
            for key, value in azienda_backup.items():
                if key in self.entries_azienda:
                    self.entries_azienda[key].set(value)
            
            self.auto_numero_fattura()
            self.aggiorna_totali()
            self.status_label.config(text="Nuova fattura creata")
    
    def load_settings(self):
        """Carica le impostazioni"""
        settings_file = "fattura_pro_settings.json"
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "azienda" in data:
                    for key, value in data["azienda"].items():
                        if key in self.entries_azienda:
                            self.entries_azienda[key].set(value)
            except:
                pass


def main():
    """Funzione principale"""
    root = tk.Tk()
    app = FatturaPro(root)
    root.mainloop()


if __name__ == "__main__":
    main()
