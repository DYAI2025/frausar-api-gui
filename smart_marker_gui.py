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
- Marker bearbeiten
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import yaml
import os
import re
import uuid
from pathlib import Path
from datetime import datetime
from marker_v3_1_manager import MarkerV31Manager

class SmartMarkerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Smart Marker-Erstellung v3.1 - Lean-Deep Enhanced")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # Initialize v3.1 manager
        self.v31_manager = MarkerV31Manager()
        
        # Marker-Verzeichnis
        self.marker_dir = Path.cwd() / "markers"
        self.marker_dir.mkdir(exist_ok=True)
        
        # Ausgewählter Marker für Beispiele
        self.selected_marker = None
        
        self.setup_ui()
        self.refresh_marker_list()
    
    def setup_ui(self):
        # Haupt-Container mit Canvas für Scrollbarkeit
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # PanedWindow für Aufteilung
        paned_window = ttk.PanedWindow(scrollable_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Linke Seite - Eingabe
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=2)
        
        # Rechte Seite - Übersicht
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)
        
        self.setup_input_section(left_frame)
        self.setup_overview_section(right_frame)
        
        # Canvas und Scrollbar packen
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_input_section(self, parent):
        # Titel
        title = ttk.Label(parent, text="🎯 Smart Marker-Erstellung v3.1", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))
        
        # Untertitel
        subtitle = ttk.Label(parent, 
                           text="Lean-Deep v3.1 / MEWT Enhanced Schema - Alle Marker folgen dem neuen Standard!",
                           font=("Arial", 11))
        subtitle.pack(pady=(0, 15))
        
        # v3.1 Schema Info
        schema_frame = ttk.LabelFrame(parent, text="📋 v3.1 Schema Anforderungen", padding="8")
        schema_frame.pack(fill=tk.X, pady=(0, 15))
        
        schema_info = ttk.Label(schema_frame, 
                              text="✓ Vier-Seiten-Frame (signal, concept, pragmatics, narrative)\n"
                                   "✓ Ein Strukturblock (pattern | composed_of | detect_class)\n"
                                   "✓ Logistic Scoring (base/weight/decay)\n"
                                   "✓ Klare Aktivierung (ANY 1, SUM(weight)>=0.7 WITHIN 48h)\n"
                                   "✓ Mindestens 5 variantenreiche Beispiele",
                              font=("Arial", 10))
        schema_info.pack(anchor=tk.W)
        
        # Template-Erstellung
        template_frame = ttk.LabelFrame(parent, text="🛠️ Template-Generator", padding="10")
        template_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Level-Auswahl
        level_frame = ttk.Frame(template_frame)
        level_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(level_frame, text="Level:").pack(side=tk.LEFT, padx=(0, 5))
        self.level_var = tk.StringVar(value="1")
        level_combo = ttk.Combobox(level_frame, textvariable=self.level_var, 
                                 values=["1 - Atomic", "2 - Semantic", "3 - Cluster", "4 - Meta"],
                                 state="readonly", width=20)
        level_combo.pack(side=tk.LEFT, padx=(0, 10))
        level_combo.bind("<<ComboboxSelected>>", self.on_level_change)
        
        # Marker Name
        name_frame = ttk.Frame(template_frame)
        name_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(name_frame, text="Name (UPPER_SNAKE_CASE):").pack(side=tk.LEFT, padx=(0, 5))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, width=30)
        name_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Author
        author_frame = ttk.Frame(template_frame)
        author_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(author_frame, text="Author:").pack(side=tk.LEFT, padx=(0, 5))
        self.author_var = tk.StringVar(value="Your Name")
        author_entry = ttk.Entry(author_frame, textvariable=self.author_var, width=30)
        author_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Auto-Fill Info
        self.category_label = ttk.Label(template_frame, text="Category: ATOMIC (auto)", 
                                      font=("Arial", 10, "italic"))
        self.category_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Template-Buttons
        template_button_frame = ttk.Frame(template_frame)
        template_button_frame.pack(fill=tk.X)
        
        ttk.Button(template_button_frame, text="🚀 Template erstellen", 
                  command=self.create_template).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(template_button_frame, text="🔄 v3.1 konvertieren", 
                  command=self.convert_to_v31).pack(side=tk.LEFT, padx=5)
        
        # Verzeichnis-Anzeige
        dir_frame = ttk.LabelFrame(parent, text="📁 Speicherort", padding="8")
        dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.dir_label = ttk.Label(dir_frame, text=f"{self.marker_dir}")
        self.dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        dir_button = ttk.Button(dir_frame, text="📂 Ändern", command=self.change_directory)
        dir_button.pack(side=tk.RIGHT)
        
        # Eingabe-Bereich
        input_frame = ttk.LabelFrame(parent, text="✏️ Marker-YAML (v3.1 Format)", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Hilfetext
        help_text = ttk.Label(input_frame, 
                            text="💡 Verwende Template-Generator oder bearbeite YAML direkt. Mehrere Marker mit '---' trennen.",
                            font=("Arial", 10, "italic"))
        help_text.pack(pady=(0, 10))
        
        # Textfeld
        self.text_widget = scrolledtext.ScrolledText(input_frame, height=20, 
                                                   wrap=tk.WORD, font=("Consolas", 12))
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Button-Bereich
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="🚀 Marker erstellen", 
                  command=self.create_markers).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="✅ Validieren", 
                  command=self.validate_current_yaml).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Löschen", 
                  command=self.clear_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 Demo laden", 
                  command=self.load_demo).pack(side=tk.LEFT, padx=5)
        
        # Test-Ergebnisse
        test_frame = ttk.LabelFrame(parent, text="🧪 Validierungs-Ergebnisse", padding="10")
        test_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.test_text = scrolledtext.ScrolledText(test_frame, height=8, wrap=tk.WORD)
        self.test_text.pack(fill=tk.BOTH, expand=True)
        
        test_button_frame = ttk.Frame(test_frame)
        test_button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(test_button_frame, text="🗑️ Löschen",
                  command=lambda: self.test_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=(0, 5))
        
        # Status
        self.status_label = ttk.Label(parent, text="Bereit für v3.1", font=("Arial", 10))
        self.status_label.pack(pady=(5, 0))
    
    def setup_overview_section(self, parent):
        # Titel
        title = ttk.Label(parent, text="📋 Marker-Übersicht", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=(0, 10))
        
        # Marker-Liste
        list_frame = ttk.LabelFrame(parent, text="📁 Verfügbare Marker", padding="8")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview für Marker-Liste
        columns = ("Name", "Kategorie")
        self.marker_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=15
        )

        # Spalten konfigurieren
        self.marker_tree.heading("Name", text="Name")
        self.marker_tree.heading("Kategorie", text="Kategorie")

        self.marker_tree.column("Name", width=200)
        self.marker_tree.column("Kategorie", width=100)
        
        # Scrollbar für Treeview
        tree_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.marker_tree.yview)
        self.marker_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.marker_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Marker auswählen
        self.marker_tree.bind("<<TreeviewSelect>>", self.on_marker_select)
        
        # Button-Bereich
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="🔄 Aktualisieren", 
                  command=self.refresh_marker_list).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="✏️ Bearbeiten", 
                  command=self.edit_marker).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Speichern", 
                  command=self.save_edited_marker).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Löschen", 
                  command=self.delete_marker).pack(side=tk.LEFT, padx=5)
        
        # Details-Bereich
        details_frame = ttk.LabelFrame(parent, text="📄 Marker-Details", padding="8")
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.details_text = scrolledtext.ScrolledText(details_frame, height=10, wrap=tk.WORD)
        self.details_text.pack(fill=tk.BOTH, expand=True)
    
    def change_directory(self):
        new_dir = filedialog.askdirectory(title="Marker-Verzeichnis auswählen")
        if new_dir:
            self.marker_dir = Path(new_dir)
            self.marker_dir.mkdir(exist_ok=True)
            self.dir_label.config(text=f"{self.marker_dir}")
            self.refresh_marker_list()
    
    def on_level_change(self, event=None):
        """Handle level selection change to update category."""
        level_text = self.level_var.get()
        level = int(level_text.split(' - ')[0]) if level_text else 1
        category = self.v31_manager.level_categories.get(level, "ATOMIC")
        self.category_label.config(text=f"Category: {category} (auto)")
    
    def create_template(self):
        """Create a v3.1 template based on user input."""
        # Get level
        level_text = self.level_var.get()
        level = int(level_text.split(' - ')[0]) if level_text else 1
        
        # Get marker name
        marker_name = self.name_var.get().strip()
        if not marker_name:
            messagebox.showwarning("Warnung", "Bitte gib einen Marker-Namen ein!")
            return
        
        # Get author
        author = self.author_var.get().strip() or "Your Name"
        
        try:
            # Create template
            template = self.v31_manager.create_marker_template(level, marker_name, author)
            
            # Convert to YAML and insert into text widget
            yaml_content = yaml.dump(template, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, yaml_content)
            
            self.update_status(f"v3.1 Template für Level {level} erstellt")
            messagebox.showinfo("Erfolg", f"Template für '{template['id']}' erstellt!\n\n"
                                         f"Vergiss nicht, mindestens 5 Beispiele hinzuzufügen.")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen des Templates: {str(e)}")
    
    def convert_to_v31(self):
        """Convert current YAML content to v3.1 format."""
        text = self.text_widget.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warnung", "Bitte gib YAML-Inhalt ein zum Konvertieren!")
            return
        
        try:
            # Parse existing YAML
            old_data = yaml.safe_load(text)
            if not old_data:
                raise ValueError("Ungültiges YAML-Format")
            
            # Convert to v3.1
            new_data = self.v31_manager.convert_old_marker_to_v31(old_data)
            
            # Convert back to YAML
            yaml_content = yaml.dump(new_data, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, yaml_content)
            
            self.update_status("Zu v3.1 konvertiert")
            messagebox.showinfo("Erfolg", f"Marker zu v3.1 konvertiert!\n\n"
                                         f"ID: {new_data['id']}\n"
                                         f"Level: {new_data['level']}\n"
                                         f"Category: {new_data['category']}")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Konvertierung: {str(e)}")
    
    def validate_current_yaml(self):
        """Validate current YAML content against v3.1 schema."""
        text = self.text_widget.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warnung", "Bitte gib YAML-Inhalt ein zum Validieren!")
            return
        
        self.test_text.delete(1.0, tk.END)
        self.test_text.insert(tk.END, "🧪 Validiere gegen v3.1 Schema...\n\n")
        
        try:
            # Split multiple markers
            marker_blocks = re.split(r'\n\s*---\s*\n', text)
            marker_blocks = [block.strip() for block in marker_blocks if block.strip()]
            
            all_valid = True
            
            for i, block in enumerate(marker_blocks):
                self.test_text.insert(tk.END, f"--- Marker {i+1} ---\n")
                
                try:
                    data = yaml.safe_load(block)
                    if not data:
                        self.test_text.insert(tk.END, "❌ Leeres YAML\n\n")
                        all_valid = False
                        continue
                    
                    # Validate with v3.1 schema
                    is_valid, errors = self.v31_manager.validate_marker_schema(data)
                    
                    if is_valid:
                        self.test_text.insert(tk.END, f"✅ {data.get('id', 'Unknown')} - VALID\n")
                        
                        # Additional info
                        level = data.get('level', 'Unknown')
                        category = data.get('category', 'Unknown') 
                        examples_count = len(data.get('examples', []))
                        self.test_text.insert(tk.END, f"   Level: {level}, Category: {category}, Examples: {examples_count}\n")
                    else:
                        self.test_text.insert(tk.END, f"❌ {data.get('id', 'Unknown')} - INVALID\n")
                        for error in errors[:5]:  # Show first 5 errors
                            self.test_text.insert(tk.END, f"   • {error}\n")
                        all_valid = False
                    
                except yaml.YAMLError as e:
                    self.test_text.insert(tk.END, f"❌ YAML Parse Error: {str(e)}\n")
                    all_valid = False
                
                self.test_text.insert(tk.END, "\n")
            
            # Summary
            status = "✅ ALLE MARKER VALID" if all_valid else "❌ EINIGE MARKER INVALID"
            self.test_text.insert(tk.END, f"🎯 Ergebnis: {status}\n")
            
            self.update_status(f"Validierung: {len(marker_blocks)} Marker geprüft")
            
        except Exception as e:
            self.test_text.insert(tk.END, f"❌ Unerwarteter Fehler: {str(e)}\n")
            self.update_status("Validierungsfehler")
    
    def clear_text(self):
        self.text_widget.delete(1.0, tk.END)
        self.update_status("Text gelöscht")
    
    def load_demo(self):
        """Load a v3.1 demo template."""
        demo_template = self.v31_manager.create_marker_template(1, "DEMO_MARKER", "Demo Author")
        demo_template["description"] = "Demo marker for testing v3.1 schema"
        demo_template["examples"] = [
            "Demo example 1 - basic usage pattern",
            "Demo example 2 - alternative expression", 
            "Demo example 3 - edge case handling",
            "Demo example 4 - complex scenario test",
            "Demo example 5 - boundary condition check"
        ]
        
        yaml_content = yaml.dump(demo_template, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, yaml_content)
        self.update_status("v3.1 Demo geladen")
    
    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        self.root.update_idletasks()
    
    def refresh_marker_list(self):
        # Treeview leeren
        for item in self.marker_tree.get_children():
            self.marker_tree.delete(item)
        
        # Marker-Dateien laden
        if self.marker_dir.exists():
            for file_path in self.marker_dir.glob("*.yaml"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)

                    if data is None:
                        data = {}

                    marker_id = data.get("id", file_path.stem)
                    kategorie = data.get("kategorie", data.get("category", ""))

                    # Datei anzeigen
                    self.marker_tree.insert(
                        "",
                        tk.END,
                        iid=marker_id,
                        values=(file_path.name, kategorie),
                    )

                except Exception:
                    # Fehlerhafte Datei anzeigen
                    self.marker_tree.insert(
                        "",
                        tk.END,
                        iid=file_path.stem,
                        values=(f"Fehler: {file_path.name}", ""),
                    )
        
        self.update_status(f"{len(self.marker_tree.get_children())} Marker geladen")
    
    def on_marker_select(self, event):
        selection = self.marker_tree.selection()
        if selection:
            marker_id = selection[0]
            self.show_marker_details(marker_id)
    
    def show_marker_details(self, marker_id):
        # Marker-Datei finden und laden
        marker_file = self.marker_dir / f"{marker_id}.yaml"
        
        if marker_file.exists():
            try:
                with open(marker_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, content)
                
            except Exception as e:
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, f"Fehler beim Laden: {e}")
        else:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Datei nicht gefunden: {marker_file}")
    
    def edit_marker(self):
        selection = self.marker_tree.selection()
        if not selection:
            messagebox.showwarning("Warnung", "Bitte wähle einen Marker zum Bearbeiten aus.")
            return
        
        marker_id = selection[0]
        
        # Marker-Datei laden und in Textfeld einfügen
        marker_file = self.marker_dir / f"{marker_id}.yaml"
        
        if marker_file.exists():
            try:
                with open(marker_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)
                
                self.update_status(f"Marker '{marker_id}' zum Bearbeiten geladen")
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden des Markers: {e}")
        else:
            messagebox.showerror("Fehler", f"Datei nicht gefunden: {marker_file}")
    
    def save_edited_marker(self):
        selection = self.marker_tree.selection()
        if not selection:
            messagebox.showwarning("Warnung", "Bitte wähle einen Marker zum Speichern aus.")
            return
        
        marker_id = selection[0]
        
        # Text aus Textfeld parsen
        text = self.text_widget.get(1.0, tk.END).strip()
        
        try:
            # YAML parsen
            data = yaml.safe_load(text)
            if not data:
                raise ValueError("Ungültiges YAML-Format")
            
            # Originale ID beibehalten
            data['id'] = marker_id
            
            # Datei speichern
            marker_file = self.marker_dir / f"{marker_id}.yaml"
            with open(marker_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            self.refresh_marker_list()
            self.update_status(f"Marker '{marker_id}' gespeichert")
            messagebox.showinfo("Erfolg", f"Marker '{marker_id}' erfolgreich gespeichert!")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")
    
    def delete_marker(self):
        selection = self.marker_tree.selection()
        if not selection:
            messagebox.showwarning("Warnung", "Bitte wähle einen Marker zum Löschen aus.")
            return
        
        item = self.marker_tree.item(selection[0])
        marker_name = item['values'][0]
        marker_id = selection[0]
        
        if messagebox.askyesno("Bestätigung", f"Möchtest du den Marker '{marker_name}' wirklich löschen?"):
            marker_file = self.marker_dir / f"{marker_id}.yaml"
            
            try:
                marker_file.unlink()
                self.refresh_marker_list()
                self.details_text.delete(1.0, tk.END)
                self.update_status(f"Marker '{marker_name}' gelöscht")
                messagebox.showinfo("Erfolg", f"Marker '{marker_name}' erfolgreich gelöscht!")
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Löschen: {e}")
    
    
    def smart_parse_text(self, text):
        """Intelligente Text-Parsing mit verbesserter ID-Generierung"""
        lines = text.strip().split('\n')
        if not lines:
            return None
        
        # Erste Zeile analysieren
        first_line = lines[0].strip()
        
        # Versuche ID aus erster Zeile zu extrahieren
        marker_id = None
        marker_name = None
        
        # Wenn erste Zeile ein Großbuchstaben-String ist (kein Key-Value)
        if first_line and first_line.isupper() and ':' not in first_line:
            marker_id = first_line
            # Intelligente Name-Generierung aus ID
            marker_name = first_line.replace('_', ' ').title()
        else:
            # UUID-basierte ID als Fallback
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            marker_id = f"MARKER_{timestamp}_{str(uuid.uuid4())[:8].upper()}"
            marker_name = "Unbekannter Marker"
        
        # YAML-Daten parsen
        try:
            data = yaml.safe_load(text)
            if not data:
                data = {}
        except yaml.YAMLError:
            # Fallback: Einfache Struktur erstellen
            data = {'content': text}
        
        # Name aus Daten extrahieren oder generieren
        if 'name' in data:
            marker_name = data['name']
        elif 'title' in data:
            marker_name = data['title']
        elif not marker_name or marker_name == "Unbekannter Marker":
            # Intelligente Name-Generierung aus ID
            if marker_id and marker_id != "Unbekannter Marker":
                marker_name = marker_id.replace('_', ' ').title()
        
        # Daten mit ID und Name aktualisieren
        data['id'] = marker_id
        data['name'] = marker_name
        
        # Standard-Felder hinzufügen falls fehlend
        if 'level' not in data:
            data['level'] = 1
        if 'beschreibung' not in data and 'description' not in data:
            data['description'] = f"Marker {marker_name}"
        if 'kategorie' not in data and 'category' not in data:
            data['category'] = 'general'
        
        return data
    
    def create_markers(self):
        """Create markers using v3.1 schema validation."""
        text = self.text_widget.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warnung", "Bitte gib YAML-Inhalt ein!")
            return
        
        # Marker mit '---' trennen
        marker_blocks = re.split(r'\n\s*---\s*\n', text)
        marker_blocks = [block.strip() for block in marker_blocks if block.strip()]
        
        created_markers = []
        errors = []
        
        for i, block in enumerate(marker_blocks):
            try:
                # Parse YAML
                data = yaml.safe_load(block)
                if not data:
                    errors.append(f"Block {i+1}: Leeres YAML")
                    continue
                
                # Validate with v3.1 schema
                is_valid, validation_errors = self.v31_manager.validate_marker_schema(data)
                
                if not is_valid:
                    error_msg = f"Block {i+1} ({data.get('id', 'Unknown')}): " + ", ".join(validation_errors[:3])
                    errors.append(error_msg)
                    continue
                
                # Generate correct filename
                filename = self.v31_manager.generate_filename(data['id'])
                filepath = self.marker_dir / filename
                
                # Save with sorted keys for consistency
                with open(filepath, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                
                created_markers.append({
                    'name': data.get('name', data['id']),
                    'id': data['id'],
                    'filename': filename,
                    'level': data.get('level', 'Unknown'),
                    'category': data.get('category', 'Unknown')
                })
                
            except yaml.YAMLError as e:
                errors.append(f"Block {i+1}: YAML-Fehler - {str(e)}")
            except Exception as e:
                errors.append(f"Block {i+1}: {str(e)}")
        
        # Ergebnisse anzeigen
        if created_markers:
            success_msg = f"✅ {len(created_markers)} v3.1 Marker erfolgreich erstellt!\n\n📁 Erstellte Marker:\n"
            for marker in created_markers:
                success_msg += f"• {marker['name']} (Level {marker['level']}, {marker['category']})\n"
                success_msg += f"  📄 {marker['filename']}\n"
            
            if errors:
                success_msg += f"\n⚠️ Fehler ({len(errors)}):\n"
                for error in errors[:5]:  # Show max 5 errors
                    success_msg += f"• {error}\n"
                if len(errors) > 5:
                    success_msg += f"... und {len(errors)-5} weitere\n"
            
            messagebox.showinfo("Erfolg", success_msg)
            self.update_status(f"{len(created_markers)} v3.1 Marker erstellt")
            self.refresh_marker_list()
        else:
            error_msg = "❌ Keine Marker erstellt!\n\nFehler:\n"
            for error in errors:
                error_msg += f"• {error}\n"
            error_msg += "\n💡 Tipp: Verwende Template-Generator oder validiere YAML zuerst."
            messagebox.showerror("Fehler", error_msg)
    
    def run(self):
        self.root.mainloop()

def main():
    app = SmartMarkerGUI()
    app.run()

if __name__ == "__main__":
    main() 