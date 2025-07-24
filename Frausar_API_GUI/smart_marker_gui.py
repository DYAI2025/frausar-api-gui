#!/usr/bin/env python3
"""
SMART MARKER-ERSTELLUNG
========================

Benutzerfreundliche GUI mit automatischer Fehlerbehebung
- Automatische YAML-Korrektur
- Klare, verständliche Fehlermeldungen
- Sofortige Marker-Erstellung
- Mehrere Marker auf einmal
- Marker-Übersicht
- Beispiele hinzufügen
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import yaml
import os
import re
from pathlib import Path
from datetime import datetime

class SmartMarkerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Smart Marker-Erstellung - Einfach & Benutzerfreundlich")
        self.root.geometry("1200x800")
        
        # Marker-Verzeichnis
        self.marker_dir = Path.cwd() / "markers"
        self.marker_dir.mkdir(exist_ok=True)
        
        # Ausgewählter Marker für Beispiele
        self.selected_marker = None
        
        self.setup_ui()
        self.refresh_marker_list()
    
    def setup_ui(self):
        # Haupt-Container mit PanedWindow für Aufteilung
        paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Linke Seite - Eingabe
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=2)
        
        # Rechte Seite - Übersicht
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)
        
        self.setup_input_section(left_frame)
        self.setup_overview_section(right_frame)
    
    def setup_input_section(self, parent):
        # Titel
        title = ttk.Label(parent, text="🎯 Smart Marker-Erstellung", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))
        
        # Untertitel
        subtitle = ttk.Label(parent, 
                           text="Einfach Text eingeben - wir machen den Rest!",
                           font=("Arial", 11))
        subtitle.pack(pady=(0, 15))
        
        # Verzeichnis-Anzeige
        dir_frame = ttk.LabelFrame(parent, text="📁 Speicherort", padding="8")
        dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.dir_label = ttk.Label(dir_frame, text=f"{self.marker_dir}")
        self.dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        dir_button = ttk.Button(dir_frame, text="📂 Ändern", command=self.change_directory)
        dir_button.pack(side=tk.RIGHT)
        
        # Eingabe-Bereich
        input_frame = ttk.LabelFrame(parent, text="✏️ Marker-Text eingeben (beliebiges Format)", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Hilfetext
        help_text = ttk.Label(input_frame, 
                            text="💡 Tipp: Mehrere Marker mit '---' oder '###' trennen",
                            font=("Arial", 10, "italic"))
        help_text.pack(pady=(0, 10))
        
        # Textfeld
        self.text_widget = scrolledtext.ScrolledText(input_frame, height=20, 
                                                   wrap=tk.WORD, font=("Consolas", 12))
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Beispiel-Text einfügen
        example_text = """Beispiel für mehrere Marker:

ABBRUCHMARKER
Level: 1
Beschreibung: Marker für Abbruch-Erkennung
Kategorie: system

---

FEHLER_MARKER
Level: 2
Beschreibung: Marker für Fehler-Erkennung
Kategorie: error

---

TEST_MARKER
Level 1
Test-Marker"""
        
        self.text_widget.insert("1.0", example_text)
        
        # Button-Bereich
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        create_button = ttk.Button(button_frame, text="🚀 Alle Marker erstellen", 
                                 command=self.create_markers, style="Accent.TButton")
        create_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(button_frame, text="🗑️ Leeren", command=self.clear_text)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        demo_button = ttk.Button(button_frame, text="📋 Demo laden", command=self.load_demo)
        demo_button.pack(side=tk.LEFT)
        
        # Status-Bereich
        status_frame = ttk.LabelFrame(parent, text="📊 Status", padding="8")
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.status_label = ttk.Label(status_frame, text="✅ Bereit - Geben Sie Text ein")
        self.status_label.pack(anchor=tk.W)
        
        # Fehler-Bereich (versteckt)
        self.error_frame = ttk.LabelFrame(parent, text="⚠️ Hinweise", padding="8")
        self.error_text = scrolledtext.ScrolledText(self.error_frame, height=4, 
                                                  wrap=tk.WORD, font=("Arial", 10))
        self.error_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_overview_section(self, parent):
        # Titel
        title = ttk.Label(parent, text="📋 Marker-Übersicht", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=(0, 10))
        
        # Button-Bereich
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        refresh_button = ttk.Button(button_frame, text="🔄 Aktualisieren", command=self.refresh_marker_list)
        refresh_button.pack(side=tk.LEFT, padx=(0, 5))
        
        examples_button = ttk.Button(button_frame, text="📝 Beispiele hinzufügen", command=self.add_examples)
        examples_button.pack(side=tk.LEFT)
        
        # Marker-Liste
        list_frame = ttk.LabelFrame(parent, text="📁 Verfügbare Marker", padding="8")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview für Marker
        columns = ("ID", "Level", "Kategorie", "Beschreibung")
        self.marker_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Spalten konfigurieren
        for col in columns:
            self.marker_tree.heading(col, text=col)
            self.marker_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.marker_tree.yview)
        self.marker_tree.configure(yscrollcommand=scrollbar.set)
        
        self.marker_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Doppelklick-Event
        self.marker_tree.bind("<Double-1>", self.on_marker_select)
        
        # Marker-Details
        details_frame = ttk.LabelFrame(parent, text="📄 Marker-Details", padding="8")
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.details_text = scrolledtext.ScrolledText(details_frame, height=8, 
                                                    wrap=tk.WORD, font=("Consolas", 10))
        self.details_text.pack(fill=tk.BOTH, expand=True)
    
    def change_directory(self):
        directory = filedialog.askdirectory(title="Marker-Verzeichnis wählen")
        if directory:
            self.marker_dir = Path(directory)
            self.dir_label.config(text=f"{self.marker_dir}")
            self.update_status("Verzeichnis geändert")
            self.refresh_marker_list()
    
    def clear_text(self):
        self.text_widget.delete("1.0", tk.END)
        self.hide_errors()
        self.update_status("Textfeld geleert")
    
    def load_demo(self):
        demo_text = """ABBRUCHMARKER
Level: 1
Beschreibung: Marker für Abbruch-Erkennung
Kategorie: system

---

FEHLER_MARKER
Level: 2
Beschreibung: Marker für Fehler-Erkennung
Kategorie: error"""
        
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", demo_text)
        self.update_status("Demo-Marker geladen")
    
    def hide_errors(self):
        self.error_frame.pack_forget()
    
    def show_errors(self, message):
        self.error_text.delete("1.0", tk.END)
        self.error_text.insert("1.0", message)
        self.error_frame.pack(fill=tk.X, pady=(10, 0))
    
    def update_status(self, message):
        self.status_label.config(text=f"✅ {message}")
    
    def refresh_marker_list(self):
        """Aktualisiert die Marker-Liste"""
        # Liste leeren
        for item in self.marker_tree.get_children():
            self.marker_tree.delete(item)
        
        # Marker-Dateien laden
        if self.marker_dir.exists():
            for yaml_file in self.marker_dir.glob("*.yaml"):
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        marker_data = yaml.safe_load(f)
                    
                    if marker_data:
                        self.marker_tree.insert("", "end", values=(
                            marker_data.get('id', 'Unbekannt'),
                            marker_data.get('level', '?'),
                            marker_data.get('category', 'general'),
                            marker_data.get('description', 'Keine Beschreibung')[:50] + "..."
                        ))
                except Exception as e:
                    print(f"Fehler beim Laden von {yaml_file}: {e}")
        
        self.update_status(f"{len(self.marker_tree.get_children())} Marker geladen")
    
    def on_marker_select(self, event):
        """Wird aufgerufen wenn ein Marker ausgewählt wird"""
        selection = self.marker_tree.selection()
        if selection:
            item = self.marker_tree.item(selection[0])
            marker_id = item['values'][0]
            self.show_marker_details(marker_id)
            self.selected_marker = marker_id
    
    def show_marker_details(self, marker_id):
        """Zeigt Details eines Markers an"""
        marker_file = self.marker_dir / f"{marker_id}.yaml"
        
        if marker_file.exists():
            try:
                with open(marker_file, 'r', encoding='utf-8') as f:
                    marker_data = yaml.safe_load(f)
                
                # YAML formatieren
                yaml_content = yaml.dump(marker_data, default_flow_style=False, 
                                       allow_unicode=True, sort_keys=False)
                
                self.details_text.delete("1.0", tk.END)
                self.details_text.insert("1.0", yaml_content)
                
            except Exception as e:
                self.details_text.delete("1.0", tk.END)
                self.details_text.insert("1.0", f"Fehler beim Laden: {str(e)}")
        else:
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert("1.0", f"Marker {marker_id} nicht gefunden")
    
    def add_examples(self):
        """Öffnet Dialog zum Hinzufügen von Beispielen"""
        if not self.selected_marker:
            messagebox.showinfo("Info", "Bitte wählen Sie zuerst einen Marker aus!")
            return
        
        # Beispiel-Dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"📝 Beispiele hinzufügen - {self.selected_marker}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Dialog-Inhalt
        ttk.Label(dialog, text="Beispiele eingeben (ein Beispiel pro Zeile):", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        examples_text = scrolledtext.ScrolledText(dialog, height=15, wrap=tk.WORD)
        examples_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aktuelle Beispiele laden
        marker_file = self.marker_dir / f"{self.selected_marker}.yaml"
        if marker_file.exists():
            try:
                with open(marker_file, 'r', encoding='utf-8') as f:
                    marker_data = yaml.safe_load(f)
                
                current_examples = marker_data.get('examples', [])
                if current_examples:
                    examples_text.insert("1.0", "\n".join(current_examples))
            except:
                pass
        
        def save_examples():
            new_examples = examples_text.get("1.0", tk.END).strip().split('\n')
            new_examples = [ex.strip() for ex in new_examples if ex.strip()]
            
            try:
                # Marker-Datei laden
                with open(marker_file, 'r', encoding='utf-8') as f:
                    marker_data = yaml.safe_load(f)
                
                # Beispiele aktualisieren
                marker_data['examples'] = new_examples
                
                # Datei speichern
                with open(marker_file, 'w', encoding='utf-8') as f:
                    yaml.dump(marker_data, f, default_flow_style=False, allow_unicode=True)
                
                messagebox.showinfo("Erfolg", f"{len(new_examples)} Beispiele gespeichert!")
                dialog.destroy()
                self.refresh_marker_list()
                self.show_marker_details(self.selected_marker)
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="💾 Speichern", command=save_examples).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="❌ Abbrechen", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def smart_parse_text(self, text):
        """Intelligente Text-Parsing mit automatischer Korrektur"""
        lines = text.strip().split('\n')
        marker_data = {}
        
        # ID wird später gesetzt, wenn gefunden
        marker_id_found = False
        
        current_key = None
        examples = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Zuerst nach Marker-ID suchen (erste Zeile in Großbuchstaben)
            if not marker_id_found and line.upper() == line and len(line) > 3 and not ':' in line:
                marker_data['id'] = line
                marker_id_found = True
                continue
            
            # Verschiedene Formate erkennen und korrigieren
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip().strip('"\'')
                
                # Schlüssel-Mapping
                key_mapping = {
                    'level': 'level',
                    'beschreibung': 'description',
                    'description': 'description',
                    'kategorie': 'category',
                    'category': 'category',
                    'beispiele': 'examples',
                    'examples': 'examples'
                }
                
                if key in key_mapping:
                    current_key = key_mapping[key]
                    if current_key == 'examples':
                        examples.append(value)
                    else:
                        marker_data[current_key] = value
                elif key.upper() == key and not marker_id_found:  # ID in Großbuchstaben
                    marker_data['id'] = value
                    marker_id_found = True
                else:
                    marker_data[key] = value
            
            elif current_key == 'examples' and line.startswith('-'):
                examples.append(line[1:].strip())
            
            elif 'level' in line.lower():
                # Level aus verschiedenen Formaten extrahieren
                level_match = re.search(r'level\s*:?\s*(\d+)', line.lower())
                if level_match:
                    marker_data['level'] = int(level_match.group(1))
            
            elif 'beschreibung' in line.lower() or 'description' in line.lower():
                # Beschreibung extrahieren
                desc_match = re.search(r'(?:beschreibung|description)\s*:?\s*(.+)', line.lower())
                if desc_match:
                    marker_data['description'] = desc_match.group(1).strip()
        
        # Automatische ID-Generierung falls keine gefunden
        if 'id' not in marker_data:
            marker_data['id'] = f"marker_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Standardwerte setzen
        if 'level' not in marker_data:
            marker_data['level'] = 1
        
        if 'description' not in marker_data:
            marker_data['description'] = f"Marker {marker_data['id']}"
        
        if 'category' not in marker_data:
            marker_data['category'] = 'general'
        
        if examples:
            marker_data['examples'] = examples
        
        return marker_data
    
    def create_markers(self):
        text = self.text_widget.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showinfo("Info", "Bitte geben Sie Text ein!")
            return
        
        try:
            # Text in Marker-Blöcke aufteilen
            separators = ['---', '###', '***']
            blocks = [text]
            
            for sep in separators:
                new_blocks = []
                for block in blocks:
                    new_blocks.extend(block.split(sep))
                blocks = new_blocks
            
            # Leere Blöcke entfernen
            blocks = [block.strip() for block in blocks if block.strip()]
            
            created_markers = []
            used_ids = set()
            
            for i, block in enumerate(blocks):
                try:
                    # Intelligente Text-Verarbeitung
                    marker_data = self.smart_parse_text(block)
                    
                    # Eindeutige ID sicherstellen
                    original_id = marker_data['id']
                    counter = 1
                    while marker_data['id'] in used_ids:
                        marker_data['id'] = f"{original_id}_{counter}"
                        counter += 1
                    
                    used_ids.add(marker_data['id'])
                    
                    # Datei speichern
                    filename = f"{marker_data['id']}.yaml"
                    filepath = self.marker_dir / filename
                    
                    # YAML formatieren
                    yaml_content = yaml.dump(marker_data, default_flow_style=False, 
                                           allow_unicode=True, sort_keys=False)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(yaml_content)
                    
                    created_markers.append(marker_data['id'])
                    
                except Exception as e:
                    print(f"Fehler beim Erstellen von Marker {i+1}: {e}")
            
            # Erfolgsmeldung
            if created_markers:
                success_message = f"""✅ {len(created_markers)} Marker erfolgreich erstellt!

📁 Erstellte Marker:
{chr(10).join([f"  • {marker_id}" for marker_id in created_markers])}

Die Marker wurden automatisch korrekt formatiert und gespeichert."""
                
                messagebox.showinfo("Erfolg!", success_message)
                self.update_status(f"{len(created_markers)} Marker erstellt")
                
                # Textfeld leeren und Liste aktualisieren
                self.text_widget.delete("1.0", tk.END)
                self.hide_errors()
                self.refresh_marker_list()
            else:
                messagebox.showwarning("Warnung", "Keine Marker konnten erstellt werden.")
            
        except Exception as e:
            # Benutzerfreundliche Fehlermeldung
            error_message = f"""❌ Ups! Da ist etwas schiefgegangen.

🔧 Was wir versucht haben:
- Ihren Text zu verstehen
- Automatisch zu korrigieren
- Als Marker zu speichern

💡 Versuchen Sie es nochmal mit einem einfacheren Text.

Technischer Fehler: {str(e)}"""
            
            messagebox.showerror("Fehler", error_message)
            self.update_status("Fehler beim Erstellen")
            self.show_errors(f"Fehler: {str(e)}\n\nVersuchen Sie es mit einem einfacheren Text.")
    
    def run(self):
        self.root.mainloop()

def main():
    app = SmartMarkerGUI()
    app.run()

if __name__ == "__main__":
    main() 