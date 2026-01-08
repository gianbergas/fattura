#!/usr/bin/env python3
"""
Generatore di Fatture - Crea fatture professionali in PDF
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os
from pathlib import Path


try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class FatturaGenerator:
    """Classe principale per generare fatture"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Generatore di Fatture")
        self.root.geometry("900x700")
        
        # Dati fattura
        self.dati_azienda = {
            "ragione_sociale": "",
            "indirizzo": "",
            "citta": "",
            "cap": "",
            "p_iva": "",
            "codice_fiscale": "",
            "telefono": "",
            "email": ""
        }
        
        self.dati_cliente = {
            "ragione_sociale": "",
            "indirizzo": "",
            "citta": "",
            "cap": "",
            "p_iva": "",
            "codice_fiscale": ""
        }
        
        self.prodotti = []
        self.numero_fattura = ""
        self.data_fattura = datetime.now().strftime("%d/%m/%Y")
        self.scadenza = ""
        self.condizioni_pagamento = ""
        self.note = ""
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Crea l'interfaccia utente"""
        # Notebook per le tab
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab Dati Azienda
        tab_azienda = ttk.Frame(notebook)
        notebook.add(tab_azienda, text="Dati Azienda")
        self.create_azienda_tab(tab_azienda)
        
        # Tab Dati Cliente
        tab_cliente = ttk.Frame(notebook)
        notebook.add(tab_cliente, text="Dati Cliente")
        self.create_cliente_tab(tab_cliente)
        
        # Tab Prodotti
        tab_prodotti = ttk.Frame(notebook)
        notebook.add(tab_prodotti, text="Prodotti/Servizi")
        self.create_prodotti_tab(tab_prodotti)
        
        # Tab Fattura
        tab_fattura = ttk.Frame(notebook)
        notebook.add(tab_fattura, text="Dettagli Fattura")
        self.create_fattura_tab(tab_fattura)
        
        # Barra pulsanti
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Genera PDF", command=self.genera_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salva Dati", command=self.salva_dati).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Carica Dati", command=self.carica_dati).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Anteprima", command=self.anteprima).pack(side=tk.LEFT, padx=5)
        
        if not REPORTLAB_AVAILABLE:
            ttk.Label(button_frame, text="⚠ reportlab non installato - installa con: pip install reportlab",
                     foreground="orange").pack(side=tk.LEFT, padx=10)
    
    def create_form_frame(self, parent, fields):
        """Crea un frame con campi form"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        entries = {}
        row = 0
        for label, key in fields:
            ttk.Label(frame, text=label + ":").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(frame, width=50)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky=tk.EW)
            entries[key] = entry
            row += 1
        
        frame.columnconfigure(1, weight=1)
        return entries
    
    def create_azienda_tab(self, parent):
        """Crea la tab dei dati azienda"""
        fields = [
            ("Ragione Sociale", "ragione_sociale"),
            ("Indirizzo", "indirizzo"),
            ("Città", "citta"),
            ("CAP", "cap"),
            ("P. IVA", "p_iva"),
            ("Codice Fiscale", "codice_fiscale"),
            ("Telefono", "telefono"),
            ("Email", "email")
        ]
        self.entries_azienda = self.create_form_frame(parent, fields)
    
    def create_cliente_tab(self, parent):
        """Crea la tab dei dati cliente"""
        fields = [
            ("Ragione Sociale", "ragione_sociale"),
            ("Indirizzo", "indirizzo"),
            ("Città", "citta"),
            ("CAP", "cap"),
            ("P. IVA", "p_iva"),
            ("Codice Fiscale", "codice_fiscale")
        ]
        self.entries_cliente = self.create_form_frame(parent, fields)
    
    def create_prodotti_tab(self, parent):
        """Crea la tab dei prodotti"""
        # Frame per la lista prodotti
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview per i prodotti
        columns = ("Descrizione", "Quantità", "Prezzo Unit.", "IVA %", "Totale")
        self.tree_prodotti = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree_prodotti.heading(col, text=col)
            self.tree_prodotti.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree_prodotti.yview)
        self.tree_prodotti.configure(yscrollcommand=scrollbar.set)
        
        self.tree_prodotti.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame per aggiungere prodotti
        add_frame = ttk.LabelFrame(parent, text="Aggiungi Prodotto/Servizio")
        add_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(add_frame, text="Descrizione:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_desc = ttk.Entry(add_frame, width=30)
        self.entry_desc.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Quantità:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_qty = ttk.Entry(add_frame, width=10)
        self.entry_qty.grid(row=0, column=3, padx=5, pady=5)
        self.entry_qty.insert(0, "1")
        
        ttk.Label(add_frame, text="Prezzo Unit.:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_prezzo = ttk.Entry(add_frame, width=10)
        self.entry_prezzo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="IVA %:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_iva = ttk.Entry(add_frame, width=10)
        self.entry_iva.grid(row=1, column=3, padx=5, pady=5)
        self.entry_iva.insert(0, "22")
        
        ttk.Button(add_frame, text="Aggiungi", command=self.aggiungi_prodotto).grid(row=2, column=0, columnspan=4, pady=5)
        ttk.Button(add_frame, text="Rimuovi Selezionato", command=self.rimuovi_prodotto).grid(row=3, column=0, columnspan=4, pady=5)
        
        # Totale
        self.label_totale = ttk.Label(parent, text="Totale: € 0.00", font=("Arial", 12, "bold"))
        self.label_totale.pack(pady=10)
    
    def create_fattura_tab(self, parent):
        """Crea la tab dei dettagli fattura"""
        fields = [
            ("Numero Fattura", "numero_fattura"),
            ("Data Fattura", "data_fattura"),
            ("Scadenza", "scadenza"),
            ("Condizioni di Pagamento", "condizioni_pagamento")
        ]
        self.entries_fattura = self.create_form_frame(parent, fields)
        
        # Note
        note_frame = ttk.LabelFrame(parent, text="Note")
        note_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.text_note = tk.Text(note_frame, height=10, width=50)
        self.text_note.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Imposta data di default
        if "data_fattura" in self.entries_fattura:
            self.entries_fattura["data_fattura"].insert(0, self.data_fattura)
    
    def aggiungi_prodotto(self):
        """Aggiunge un prodotto alla lista"""
        try:
            descrizione = self.entry_desc.get()
            quantita = float(self.entry_qty.get())
            prezzo = float(self.entry_prezzo.get())
            iva = float(self.entry_iva.get())
            
            if not descrizione:
                messagebox.showwarning("Attenzione", "Inserisci una descrizione")
                return
            
            totale = quantita * prezzo
            totale_iva = totale * (1 + iva / 100)
            
            self.tree_prodotti.insert("", tk.END, values=(
                descrizione,
                f"{quantita:.2f}",
                f"€ {prezzo:.2f}",
                f"{iva:.0f}%",
                f"€ {totale_iva:.2f}"
            ))
            
            prodotto = {
                "descrizione": descrizione,
                "quantita": quantita,
                "prezzo": prezzo,
                "iva": iva,
                "totale": totale_iva
            }
            self.prodotti.append(prodotto)
            
            # Pulisci campi
            self.entry_desc.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
            self.entry_qty.insert(0, "1")
            self.entry_prezzo.delete(0, tk.END)
            self.entry_iva.delete(0, tk.END)
            self.entry_iva.insert(0, "22")
            
            self.aggiorna_totale()
            
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi")
    
    def rimuovi_prodotto(self):
        """Rimuove il prodotto selezionato"""
        selected = self.tree_prodotti.selection()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona un prodotto da rimuovere")
            return
        
        for item in selected:
            index = self.tree_prodotti.index(item)
            self.tree_prodotti.delete(item)
            del self.prodotti[index]
        
        self.aggiorna_totale()
    
    def aggiorna_totale(self):
        """Aggiorna il totale della fattura"""
        totale = sum(p["totale"] for p in self.prodotti)
        self.label_totale.config(text=f"Totale: € {totale:.2f}")
    
    def get_dati_azienda(self):
        """Recupera i dati azienda dai campi"""
        for key in self.dati_azienda:
            if key in self.entries_azienda:
                self.dati_azienda[key] = self.entries_azienda[key].get()
    
    def get_dati_cliente(self):
        """Recupera i dati cliente dai campi"""
        for key in self.dati_cliente:
            if key in self.entries_cliente:
                self.dati_cliente[key] = self.entries_cliente[key].get()
    
    def get_dati_fattura(self):
        """Recupera i dati fattura dai campi"""
        self.numero_fattura = self.entries_fattura["numero_fattura"].get()
        self.data_fattura = self.entries_fattura["data_fattura"].get()
        self.scadenza = self.entries_fattura["scadenza"].get()
        self.condizioni_pagamento = self.entries_fattura["condizioni_pagamento"].get()
        self.note = self.text_note.get("1.0", tk.END).strip()
    
    def genera_pdf(self):
        """Genera il PDF della fattura"""
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Errore", "reportlab non installato!\nInstalla con: pip install reportlab")
            return
        
        self.get_dati_azienda()
        self.get_dati_cliente()
        self.get_dati_fattura()
        
        # Validazione
        if not self.dati_azienda["ragione_sociale"]:
            messagebox.showerror("Errore", "Inserisci i dati dell'azienda")
            return
        
        if not self.dati_cliente["ragione_sociale"]:
            messagebox.showerror("Errore", "Inserisci i dati del cliente")
            return
        
        if not self.prodotti:
            messagebox.showerror("Errore", "Aggiungi almeno un prodotto/servizio")
            return
        
        # Chiedi dove salvare
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Fattura_{self.numero_fattura or 'N'}.pdf"
        )
        
        if not filename:
            return
        
        try:
            self.create_pdf(filename)
            messagebox.showinfo("Successo", f"Fattura generata: {filename}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella generazione PDF:\n{str(e)}")
    
    def create_pdf(self, filename):
        """Crea il file PDF"""
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Stile titolo
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Titolo
        story.append(Paragraph("FATTURA", title_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Dati azienda
        azienda_text = f"""
        <b>{self.dati_azienda['ragione_sociale']}</b><br/>
        {self.dati_azienda['indirizzo']}<br/>
        {self.dati_azienda['cap']} {self.dati_azienda['citta']}<br/>
        P. IVA: {self.dati_azienda['p_iva']}<br/>
        CF: {self.dati_azienda['codice_fiscale']}<br/>
        Tel: {self.dati_azienda['telefono']}<br/>
        Email: {self.dati_azienda['email']}
        """
        story.append(Paragraph(azienda_text, styles['Normal']))
        story.append(Spacer(1, 1*cm))
        
        # Dati cliente
        cliente_text = f"""
        <b>Cliente:</b><br/>
        {self.dati_cliente['ragione_sociale']}<br/>
        {self.dati_cliente['indirizzo']}<br/>
        {self.dati_cliente['cap']} {self.dati_cliente['citta']}<br/>
        P. IVA: {self.dati_cliente['p_iva']}<br/>
        CF: {self.dati_cliente['codice_fiscale']}
        """
        story.append(Paragraph(cliente_text, styles['Normal']))
        story.append(Spacer(1, 1*cm))
        
        # Dettagli fattura
        dettagli_data = [
            ["Numero Fattura:", self.numero_fattura or "N/A"],
            ["Data:", self.data_fattura],
            ["Scadenza:", self.scadenza or "N/A"],
            ["Pagamento:", self.condizioni_pagamento or "N/A"]
        ]
        
        dettagli_table = Table(dettagli_data, colWidths=[4*cm, 6*cm])
        dettagli_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(dettagli_table)
        story.append(Spacer(1, 1*cm))
        
        # Tabella prodotti
        prodotti_data = [["Descrizione", "Q.tà", "Prezzo Unit.", "IVA %", "Totale"]]
        
        totale_imponibile = 0
        totale_iva = 0
        
        for p in self.prodotti:
            imponibile = p['quantita'] * p['prezzo']
            iva_importo = imponibile * (p['iva'] / 100)
            totale_imponibile += imponibile
            totale_iva += iva_importo
            
            prodotti_data.append([
                p['descrizione'],
                f"{p['quantita']:.2f}",
                f"€ {p['prezzo']:.2f}",
                f"{p['iva']:.0f}%",
                f"€ {p['totale']:.2f}"
            ])
        
        # Totali
        totale_generale = totale_imponibile + totale_iva
        prodotti_data.append(["", "", "", "Imponibile:", f"€ {totale_imponibile:.2f}"])
        prodotti_data.append(["", "", "", "IVA:", f"€ {totale_iva:.2f}"])
        prodotti_data.append(["", "", "", "<b>TOTALE:</b>", f"<b>€ {totale_generale:.2f}</b>"])
        
        prodotti_table = Table(prodotti_data, colWidths=[6*cm, 2*cm, 2.5*cm, 2*cm, 2.5*cm])
        prodotti_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (3, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (4, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -4), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -4), [colors.white, colors.lightgrey]),
            ('FONTNAME', (3, -3), (4, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (3, -3), (4, -1), 11),
        ]))
        story.append(prodotti_table)
        story.append(Spacer(1, 1*cm))
        
        # Note
        if self.note:
            story.append(Paragraph(f"<b>Note:</b><br/>{self.note}", styles['Normal']))
        
        # Genera PDF
        doc.build(story)
    
    def salva_dati(self):
        """Salva i dati in un file JSON"""
        self.get_dati_azienda()
        self.get_dati_cliente()
        self.get_dati_fattura()
        
        data = {
            "azienda": self.dati_azienda,
            "cliente": self.dati_cliente,
            "fattura": {
                "numero": self.numero_fattura,
                "data": self.data_fattura,
                "scadenza": self.scadenza,
                "condizioni": self.condizioni_pagamento,
                "note": self.note
            },
            "prodotti": self.prodotti
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Successo", "Dati salvati!")
    
    def carica_dati(self):
        """Carica i dati da un file JSON"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Carica dati azienda
            if "azienda" in data:
                for key, value in data["azienda"].items():
                    if key in self.entries_azienda:
                        self.entries_azienda[key].delete(0, tk.END)
                        self.entries_azienda[key].insert(0, value)
            
            # Carica dati cliente
            if "cliente" in data:
                for key, value in data["cliente"].items():
                    if key in self.entries_cliente:
                        self.entries_cliente[key].delete(0, tk.END)
                        self.entries_cliente[key].insert(0, value)
            
            # Carica dati fattura
            if "fattura" in data:
                f = data["fattura"]
                if "numero" in f:
                    self.entries_fattura["numero_fattura"].delete(0, tk.END)
                    self.entries_fattura["numero_fattura"].insert(0, f.get("numero", ""))
                if "data" in f:
                    self.entries_fattura["data_fattura"].delete(0, tk.END)
                    self.entries_fattura["data_fattura"].insert(0, f.get("data", ""))
                if "scadenza" in f:
                    self.entries_fattura["scadenza"].delete(0, tk.END)
                    self.entries_fattura["scadenza"].insert(0, f.get("scadenza", ""))
                if "condizioni" in f:
                    self.entries_fattura["condizioni_pagamento"].delete(0, tk.END)
                    self.entries_fattura["condizioni_pagamento"].insert(0, f.get("condizioni", ""))
                if "note" in f:
                    self.text_note.delete("1.0", tk.END)
                    self.text_note.insert("1.0", f.get("note", ""))
            
            # Carica prodotti
            if "prodotti" in data:
                self.prodotti = data["prodotti"]
                # Aggiorna treeview
                for item in self.tree_prodotti.get_children():
                    self.tree_prodotti.delete(item)
                
                for p in self.prodotti:
                    self.tree_prodotti.insert("", tk.END, values=(
                        p["descrizione"],
                        f"{p['quantita']:.2f}",
                        f"€ {p['prezzo']:.2f}",
                        f"{p['iva']:.0f}%",
                        f"€ {p['totale']:.2f}"
                    ))
                
                self.aggiorna_totale()
            
            messagebox.showinfo("Successo", "Dati caricati!")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel caricamento:\n{str(e)}")
    
    def load_settings(self):
        """Carica le impostazioni salvate"""
        settings_file = "fattura_settings.json"
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "azienda" in data:
                    for key, value in data["azienda"].items():
                        if key in self.entries_azienda:
                            self.entries_azienda[key].insert(0, value)
            except:
                pass
    
    def anteprima(self):
        """Mostra un'anteprima dei dati"""
        self.get_dati_azienda()
        self.get_dati_cliente()
        self.get_dati_fattura()
        
        totale = sum(p["totale"] for p in self.prodotti)
        
        preview = f"""
ANTEPRIMA FATTURA
================

AZIENDA:
{self.dati_azienda['ragione_sociale']}
{self.dati_azienda['indirizzo']}
{self.dati_azienda['cap']} {self.dati_azienda['citta']}

CLIENTE:
{self.dati_cliente['ragione_sociale']}
{self.dati_cliente['indirizzo']}

FATTURA N. {self.numero_fattura or 'N/A'}
Data: {self.data_fattura}

PRODOTTI: {len(self.prodotti)}
TOTALE: € {totale:.2f}
"""
        
        messagebox.showinfo("Anteprima", preview)


def main():
    """Funzione principale"""
    root = tk.Tk()
    app = FatturaGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
