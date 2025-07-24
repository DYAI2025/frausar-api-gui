#!/usr/bin/env python3
"""
ENHANCED SMART MARKER GUI
=========================

Erweiterte GUI mit Multi-Format-Support, Live-Suche und Marker-Übersicht
- Multi-Format-Support (.txt, .py, .json, .yaml, .yml)
- Live-Suche mit Fuzzy-Matching
- Marker-Übersicht parallel zur Eingabe
- Icon-basierte Kategorisierung
- Inline-Editor für Marker-Bearbeitung
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import yaml
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

# Eigene Module importieren
from marker_manager import MarkerManager
from search_engine import SearchEngine

# Import Bridge Integration
import sys
import subprocess
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
try:
    from marker_import_bridge import YAMLBlockSplitter, MarkerValidator, MarkerWriter, HistoryLogger
    IMPORT_BRIDGE_AVAILABLE = True
except ImportError:
    IMPORT_BRIDGE_AVAILABLE = False


class InlineEditor:
    """Inline-Editor für Marker-Bearbeitung."""
    
    def __init__(self, parent, marker_data, original_file=None):
        """Initialisiert den Inline-Editor."""
        self.parent = parent
        self.marker_data = marker_data.copy()
        self.original_file = original_file
        self.backup_data = marker_data.copy()
        
        # Editor-Fenster
        self.editor_window = tk.Toplevel(parent)
        self.editor_window.title(f"✏️ Marker bearbeiten: {marker_data.get('id', 'Unbekannt')}")
        self.editor_window.geometry("800x600")
        self.editor_window.resizable(True, True)
        
        # Zentriere das Fenster
        self.editor_window.transient(parent)
        self.editor_window.grab_set()
        
        # Variablen
        self.validation_errors = []
        self.is_modified = False
        
        # GUI-Setup
        self.setup_ui()
        self.load_marker_data()
        
        # Event-Bindings
        self.editor_window.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def setup_ui(self):
        """Erstellt die Editor-Benutzeroberfläche."""
        # Haupt-Container
        main_frame = ttk.Frame(self.editor_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title = ttk.Label(main_frame, text="✏️ Marker Inline-Editor", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))
        
        # Editor-Bereich
        editor_frame = ttk.LabelFrame(main_frame, text="📝 YAML-Editor", padding="10")
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # YAML-Textfeld
        self.yaml_text = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.NONE,
            font=("Consolas", 12),
            background="#f8f9fa",
            foreground="#212529",
            insertbackground="#212529"
        )
        self.yaml_text.pack(fill=tk.BOTH, expand=True)
        
        # Syntax-Highlighting
        self.setup_syntax_highlighting()
        
        # Validierung und Status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Validierungs-Status
        self.validation_label = ttk.Label(status_frame, text="✅ Validierung OK", 
                                         foreground="green")
        self.validation_label.pack(side=tk.LEFT)
        
        # Änderungs-Status
        self.modified_label = ttk.Label(status_frame, text="", 
                                      foreground="blue")
        self.modified_label.pack(side=tk.RIGHT)
        
        # Fehler-Anzeige
        self.error_frame = ttk.LabelFrame(main_frame, text="⚠️ Validierungsfehler", padding="5")
        self.error_text = scrolledtext.ScrolledText(self.error_frame, height=4, 
                                                  font=("Consolas", 10),
                                                  background="#fff3cd",
                                                  foreground="#856404")
        self.error_text.pack(fill=tk.BOTH, expand=True)
        
        # Button-Bereich
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Speichern-Button
        self.save_button = ttk.Button(button_frame, text="💾 Speichern", 
                                     command=self.save_marker, style="Accent.TButton")
        self.save_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Abbrechen-Button
        ttk.Button(button_frame, text="❌ Abbrechen", 
                  command=self.cancel_edit).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Zurücksetzen-Button
        ttk.Button(button_frame, text="🔄 Zurücksetzen", 
                  command=self.reset_changes).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Vorschau-Button
        ttk.Button(button_frame, text="👁️ Vorschau", 
                  command=self.show_preview).pack(side=tk.LEFT)
        
        # Event-Bindings für Live-Validierung
        self.yaml_text.bind('<KeyRelease>', self.on_text_change)
        self.yaml_text.bind('<Control-s>', lambda e: self.save_marker())
        self.yaml_text.bind('<Control-z>', lambda e: self.reset_changes())
        
    def setup_syntax_highlighting(self):
        """Richtet Syntax-Highlighting für YAML ein."""
        # YAML-Schlüsselwörter
        yaml_keywords = [
            'id', 'level', 'description', 'version', 'status', 'author',
            'created', 'updated', 'tags', 'category', 'priority', 'examples'
        ]
        
        # Tag-Konfiguration
        for keyword in yaml_keywords:
            self.yaml_text.tag_configure(f"keyword_{keyword}", 
                                       foreground="#007bff", 
                                       font=("Consolas", 12, "bold"))
        
        # Allgemeine Tags
        self.yaml_text.tag_configure("comment", foreground="#6c757d", 
                                   font=("Consolas", 12, "italic"))
        self.yaml_text.tag_configure("string", foreground="#28a745")
        self.yaml_text.tag_configure("number", foreground="#fd7e14")
        
    def load_marker_data(self):
        """Lädt die Marker-Daten in den Editor."""
        try:
            # Konvertiere zu YAML
            yaml_str = yaml.dump(self.marker_data, default_flow_style=False, 
                               allow_unicode=True, sort_keys=False)
            
            # Füge Kommentar hinzu
            header = f"# Marker: {self.marker_data.get('id', 'Unbekannt')}\n"
            header += f"# Bearbeitet: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            header += "# Änderungen werden automatisch validiert\n\n"
            
            self.yaml_text.delete("1.0", tk.END)
            self.yaml_text.insert("1.0", header + yaml_str)
            
            # Validiere initial
            self.validate_yaml()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Marker-Daten: {str(e)}")
    
    def on_text_change(self, event=None):
        """Wird bei Text-Änderungen aufgerufen."""
        self.is_modified = True
        self.modified_label.config(text="📝 Geändert")
        self.validate_yaml()
        
        # Verzögerte Validierung (debouncing)
        if hasattr(self, '_validation_timer'):
            self.editor_window.after_cancel(self._validation_timer)
        self._validation_timer = self.editor_window.after(500, self.validate_yaml)
    
    def validate_yaml(self):
        """Validiert das YAML und zeigt Fehler an."""
        try:
            yaml_content = self.yaml_text.get("1.0", tk.END)
            
            # Entferne Kommentare für Validierung
            lines = yaml_content.split('\n')
            clean_lines = []
            for line in lines:
                if not line.strip().startswith('#'):
                    clean_lines.append(line)
            
            clean_yaml = '\n'.join(clean_lines)
            
            # Parse YAML
            parsed_data = yaml.safe_load(clean_yaml)
            
            if parsed_data is None:
                self.validation_errors = ["Leeres YAML-Dokument"]
            else:
                # Validiere mit Import Bridge falls verfügbar
                if IMPORT_BRIDGE_AVAILABLE:
                    from marker_import_bridge import MarkerValidator
                    validator = MarkerValidator()
                    _, errors = validator.validate(clean_yaml)
                    self.validation_errors = errors if errors else []
                else:
                    # Einfache Validierung
                    self.validation_errors = []
                    if not parsed_data.get('id'):
                        self.validation_errors.append("ID ist erforderlich")
                    if not parsed_data.get('description'):
                        self.validation_errors.append("Beschreibung ist erforderlich")
            
            # Update UI
            self.update_validation_display()
            
        except yaml.YAMLError as e:
            self.validation_errors = [f"YAML-Syntax-Fehler: {str(e)}"]
            self.update_validation_display()
        except Exception as e:
            self.validation_errors = [f"Validierungsfehler: {str(e)}"]
            self.update_validation_display()
    
    def update_validation_display(self):
        """Aktualisiert die Validierungs-Anzeige."""
        if not self.validation_errors:
            self.validation_label.config(text="✅ Validierung OK", foreground="green")
            self.error_frame.pack_forget()
            self.save_button.config(state="normal")
        else:
            self.validation_label.config(text=f"❌ {len(self.validation_errors)} Fehler", 
                                       foreground="red")
            self.error_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Zeige Fehler an
            self.error_text.delete("1.0", tk.END)
            for i, error in enumerate(self.validation_errors, 1):
                self.error_text.insert(tk.END, f"{i}. {error}\n")
            
            self.save_button.config(state="disabled")
    
    def save_marker(self):
        """Speichert den bearbeiteten Marker."""
        if self.validation_errors:
            messagebox.showerror("Validierungsfehler", 
                               "Bitte beheben Sie alle Validierungsfehler vor dem Speichern!")
            return
        
        try:
            # Parse YAML
            yaml_content = self.yaml_text.get("1.0", tk.END)
            lines = yaml_content.split('\n')
            clean_lines = []
            for line in lines:
                if not line.strip().startswith('#'):
                    clean_lines.append(line)
            
            clean_yaml = '\n'.join(clean_lines)
            new_data = yaml.safe_load(clean_yaml)
            
            if not new_data:
                messagebox.showerror("Fehler", "Leere Marker-Daten!")
                return
            
            # Erstelle Backup
            self.create_backup()
            
            # Speichere neue Daten
            if self.original_file:
                # Überschreibe Original-Datei
                with open(self.original_file, 'w', encoding='utf-8') as f:
                    yaml.dump(new_data, f, default_flow_style=False, 
                             allow_unicode=True, sort_keys=False)
                
                self.update_status(f"✅ Marker gespeichert: {new_data.get('id', 'Unbekannt')}")
            else:
                # Erstelle neue Datei
                marker_id = new_data.get('id', 'UNKNOWN')
                filename = f"{marker_id}.yaml"
                filepath = Path.cwd() / "markers" / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    yaml.dump(new_data, f, default_flow_style=False, 
                             allow_unicode=True, sort_keys=False)
                
                self.update_status(f"✅ Neuer Marker erstellt: {filename}")
            
            # Update Parent
            if hasattr(self.parent, 'load_existing_markers'):
                self.parent.load_existing_markers()
            
            self.is_modified = False
            self.modified_label.config(text="✅ Gespeichert")
            
            messagebox.showinfo("Erfolg", "Marker erfolgreich gespeichert!")
            self.editor_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")
    
    def create_backup(self):
        """Erstellt ein Backup der ursprünglichen Daten."""
        try:
            backup_dir = Path.cwd() / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            marker_id = self.marker_data.get('id', 'unknown')
            backup_file = backup_dir / f"{marker_id}_{timestamp}.yaml"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.backup_data, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
            
        except Exception as e:
            print(f"Backup-Fehler: {e}")
    
    def reset_changes(self):
        """Setzt alle Änderungen zurück."""
        if self.is_modified:
            result = messagebox.askyesno("Bestätigung", 
                                       "Möchten Sie alle Änderungen verwerfen?")
            if result:
                self.load_marker_data()
                self.is_modified = False
                self.modified_label.config(text="")
    
    def show_preview(self):
        """Zeigt eine Vorschau des Markers an."""
        try:
            yaml_content = self.yaml_text.get("1.0", tk.END)
            lines = yaml_content.split('\n')
            clean_lines = []
            for line in lines:
                if not line.strip().startswith('#'):
                    clean_lines.append(line)
            
            clean_yaml = '\n'.join(clean_lines)
            preview_data = yaml.safe_load(clean_yaml)
            
            if preview_data:
                preview_window = tk.Toplevel(self.editor_window)
                preview_window.title("👁️ Marker-Vorschau")
                preview_window.geometry("600x400")
                
                preview_text = scrolledtext.ScrolledText(preview_window, 
                                                       font=("Consolas", 12))
                preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Formatiere Vorschau
                preview_str = f"ID: {preview_data.get('id', 'N/A')}\n"
                preview_str += f"Level: {preview_data.get('level', 'N/A')}\n"
                preview_str += f"Beschreibung: {preview_data.get('description', 'N/A')}\n"
                preview_str += f"Version: {preview_data.get('version', 'N/A')}\n"
                preview_str += f"Status: {preview_data.get('status', 'N/A')}\n"
                preview_str += f"Autor: {preview_data.get('author', 'N/A')}\n\n"
                
                if 'examples' in preview_data:
                    preview_str += "Beispiele:\n"
                    for i, example in enumerate(preview_data['examples'], 1):
                        preview_str += f"{i}. {example}\n"
                
                preview_text.insert("1.0", preview_str)
                preview_text.config(state="disabled")
            else:
                messagebox.showwarning("Warnung", "Keine gültigen Daten für Vorschau!")
                
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei Vorschau: {str(e)}")
    
    def cancel_edit(self):
        """Bricht die Bearbeitung ab."""
        if self.is_modified:
            result = messagebox.askyesno("Bestätigung", 
                                       "Möchten Sie die Bearbeitung wirklich abbrechen?\n"
                                       "Alle Änderungen gehen verloren!")
            if not result:
                return
        
        self.editor_window.destroy()
    
    def on_close(self):
        """Wird beim Schließen des Fensters aufgerufen."""
        self.cancel_edit()
    
    def update_status(self, message):
        """Aktualisiert die Status-Anzeige im Parent-Fenster."""
        if hasattr(self.parent, 'update_status'):
            self.parent.update_status(message)


class EnhancedSmartMarkerGUI:
    """Erweiterte Smart Marker GUI mit allen Features."""
    
    def __init__(self):
        """Initialisiert die erweiterte GUI."""
        self.root = tk.Tk()
        self.root.title("🎯 Enhanced Smart Marker-Erstellung - Multi-Format & Live-Suche")
        self.root.geometry("1400x900")
        
        # Marker-Verzeichnis
        self.marker_dir = Path.cwd() / "markers"
        self.marker_dir.mkdir(exist_ok=True)
        
        # Import Bridge Verzeichnisse
        self.json_dir = Path.cwd() / "markers_json"
        self.json_dir.mkdir(exist_ok=True)
        
        # Manager und Engine
        self.marker_manager = MarkerManager()
        self.search_engine = SearchEngine()
        
        # Import Bridge Komponenten
        if IMPORT_BRIDGE_AVAILABLE:
            self.yaml_splitter = YAMLBlockSplitter()
            self.marker_validator = MarkerValidator()
            self.marker_writer = MarkerWriter(self.marker_dir, self.json_dir)
            self.history_logger = HistoryLogger(Path("import_history.json"))
        else:
            self.yaml_splitter = None
            self.marker_validator = None
            self.marker_writer = None
            self.history_logger = None
        
        # Marker-Daten
        self.all_markers = []
        self.filtered_markers = []
        self.selected_marker = None
        
        # GUI-Setup
        self.setup_ui()
        self.load_existing_markers()
        
    def setup_ui(self):
        """Erstellt die Benutzeroberfläche."""
        # Haupt-Container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title = ttk.Label(main_frame, text="🎯 Enhanced Smart Marker-Erstellung", 
                         font=("Arial", 20, "bold"))
        title.pack(pady=(0, 10))
        
        # Hauptbereich mit 3 Spalten
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Linke Spalte - Marker-Übersicht
        self.setup_marker_overview(content_frame)
        
        # Mittlere Spalte - Eingabe
        self.setup_input_section(content_frame)
        
        # Rechte Spalte - Details und Tools
        self.setup_details_section(content_frame)
        
        # Status-Bar
        self.setup_status_bar(main_frame)
    
    def setup_marker_overview(self, parent):
        """Erstellt die Marker-Übersicht (linke Spalte)."""
        left_frame = ttk.LabelFrame(parent, text="📋 Marker-Übersicht", padding="5")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        
        # Suchbereich
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(search_frame, text="🔍").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Clear-Button
        ttk.Button(search_frame, text="✖", width=3,
                  command=self.clear_search).pack(side=tk.RIGHT, padx=(2, 0))
        
        # Filter-Bereich
        filter_frame = ttk.LabelFrame(left_frame, text="🔧 Filter", padding="5")
        filter_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Kategorie-Filter
        ttk.Label(filter_frame, text="Kategorie:").pack(anchor=tk.W)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var)
        self.category_combo.pack(fill=tk.X, pady=(0, 5))
        self.category_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Format-Filter
        ttk.Label(filter_frame, text="Format:").pack(anchor=tk.W)
        self.format_var = tk.StringVar()
        self.format_combo = ttk.Combobox(filter_frame, textvariable=self.format_var)
        self.format_combo.pack(fill=tk.X, pady=(0, 5))
        self.format_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Fehler-Filter
        self.error_only_var = tk.BooleanVar()
        ttk.Checkbutton(filter_frame, text="Nur Fehler-Marker", 
                       variable=self.error_only_var,
                       command=self.on_filter_change).pack(anchor=tk.W)
        
        # Clear-Filter-Button
        ttk.Button(filter_frame, text="🗑️ Filter löschen", 
                  command=self.clear_filters).pack(fill=tk.X, pady=(5, 0))
        
        # Marker-Liste
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar für Liste
        list_scrollbar = ttk.Scrollbar(list_frame)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Marker-Listbox
        self.marker_listbox = tk.Listbox(list_frame, yscrollcommand=list_scrollbar.set)
        self.marker_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.marker_listbox.bind('<<ListboxSelect>>', self.on_marker_select)
        list_scrollbar.config(command=self.marker_listbox.yview)
        
        # Aktions-Buttons
        actions_frame = ttk.Frame(left_frame)
        actions_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(actions_frame, text="🔄 Aktualisieren", 
                  command=self.refresh_markers).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        ttk.Button(actions_frame, text="📁 Verzeichnis", 
                  command=self.change_directory).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
    
    def setup_input_section(self, parent):
        """Erstellt den Eingabe-Bereich (mittlere Spalte)."""
        middle_frame = ttk.LabelFrame(parent, text="✏️ Marker-Erstellung", padding="10")
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Eingabe-Methoden
        method_frame = ttk.LabelFrame(middle_frame, text="📝 Eingabe-Methode", padding="5")
        method_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_method = tk.StringVar(value="text")
        ttk.Radiobutton(method_frame, text="Freier Text (Multi-Marker)", 
                       variable=self.input_method, value="text").pack(anchor=tk.W)
        ttk.Radiobutton(method_frame, text="YAML/Python-Code", 
                       variable=self.input_method, value="code").pack(anchor=tk.W)
        
        # Eingabe-Bereich
        input_frame = ttk.LabelFrame(middle_frame, text="✏️ Marker-Text eingeben", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Hilfetext
        help_text = ttk.Label(input_frame,
                            text="💡 Tipp: Mehrere Marker mit '---' trennen. Automatische ID-Erkennung!",
                            font=("Arial", 10, "italic"))
        help_text.pack(pady=(0, 10))
        
        # Textfeld
        self.text_widget = scrolledtext.ScrolledText(input_frame, height=20,
                                                   wrap=tk.WORD, font=("Consolas", 12))
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Beispiel-Text einfügen
        example_text = """Beispiel für mehrere Marker:

TEST_MARKER_1
Level: 1
Beschreibung: Erster Test-Marker
Kategorie: test
Beispiele:
- Beispiel 1
- Beispiel 2

---

PRODUCTION_MARKER
Level: 2
Beschreibung: Produktions-Marker
Kategorie: production
Beispiele:
- Produktions-Beispiel

---

PYTHON_MARKER
Level: 3
Beschreibung: Python-Code Marker
Kategorie: python
Beispiele:
- def test_function():
- class TestClass:"""

        self.text_widget.insert("1.0", example_text)
        
        # Buttons
        buttons_frame = ttk.Frame(middle_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(buttons_frame, text="🚀 Alle Marker erstellen", 
                  command=self.create_markers, style="Accent.TButton").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(buttons_frame, text="🗑️ Text löschen", 
                  command=self.clear_text).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        # Import Bridge Buttons
        if IMPORT_BRIDGE_AVAILABLE:
            ttk.Button(buttons_frame, text="🔗 Import Bridge", 
                      command=self.use_import_bridge).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            ttk.Button(buttons_frame, text="📁 Datei importieren", 
                      command=self.import_from_file).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 0))
        else:
            ttk.Button(buttons_frame, text="⚠️ Import Bridge nicht verfügbar", 
                      state="disabled").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Demo-Button
        ttk.Button(middle_frame, text="🎯 Demo-Marker laden", 
                  command=self.load_demo).pack(fill=tk.X)
    
    def setup_details_section(self, parent):
        """Erstellt den Details-Bereich (rechte Spalte)."""
        right_frame = ttk.LabelFrame(parent, text="📊 Details & Tools", padding="5")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(5, 0))
        
        # Marker-Details
        details_frame = ttk.LabelFrame(right_frame, text="📋 Marker-Details", padding="5")
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.details_text = scrolledtext.ScrolledText(details_frame, height=15,
                                                    wrap=tk.WORD, font=("Consolas", 10))
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        # Aktions-Buttons
        actions_frame = ttk.Frame(right_frame)
        actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(actions_frame, text="✏️ Bearbeiten", 
                  command=self.edit_marker).pack(fill=tk.X, pady=(0, 2))
        ttk.Button(actions_frame, text="🗑️ Löschen", 
                  command=self.delete_marker).pack(fill=tk.X, pady=(0, 2))
        ttk.Button(actions_frame, text="📝 Beispiele hinzufügen", 
                  command=self.add_examples).pack(fill=tk.X, pady=(0, 2))
        
        # Statistiken
        stats_frame = ttk.LabelFrame(right_frame, text="📈 Statistiken", padding="5")
        stats_frame.pack(fill=tk.X)
        
        self.stats_label = ttk.Label(stats_frame, text="Lade Statistiken...")
        self.stats_label.pack(anchor=tk.W)
        
        # Such-Statistiken
        self.search_stats_label = ttk.Label(stats_frame, text="")
        self.search_stats_label.pack(anchor=tk.W)
    
    def setup_status_bar(self, parent):
        """Erstellt die Status-Bar."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="✅ System bereit")
        self.status_label.pack(side=tk.LEFT)
        
        # Performance-Info
        self.performance_label = ttk.Label(status_frame, text="")
        self.performance_label.pack(side=tk.RIGHT)
    
    def load_existing_markers(self):
        """Lädt bestehende Marker aus dem Verzeichnis."""
        try:
            self.all_markers = self.marker_manager.collect_markers_from_directory(str(self.marker_dir))
            self.filtered_markers = self.all_markers.copy()
            self.update_marker_list()
            self.update_statistics()
            self.update_filter_options()
            self.update_status(f"✅ {len(self.all_markers)} Marker geladen")
        except Exception as e:
            self.update_status(f"❌ Fehler beim Laden: {str(e)}")
    
    def update_marker_list(self):
        """Aktualisiert die Marker-Liste."""
        self.marker_listbox.delete(0, tk.END)
        
        for marker in self.filtered_markers:
            summary = self.marker_manager.get_marker_summary(marker)
            self.marker_listbox.insert(tk.END, summary)
    
    def update_statistics(self):
        """Aktualisiert die Statistiken."""
        if not self.all_markers:
            self.stats_label.config(text="Keine Marker vorhanden")
            return
        
        stats = self.search_engine.get_search_statistics(self.all_markers)
        
        stats_text = f"""📊 Marker-Statistiken:
• Gesamt: {stats['total_markers']}
• Gültig: {stats['valid_markers']}
• Fehler: {stats['error_markers']}

📂 Kategorien:"""
        
        for category, count in sorted(stats['categories'].items()):
            stats_text += f"\n  • {category}: {count}"
        
        stats_text += "\n\n📄 Formate:"
        for format_type, count in sorted(stats['formats'].items()):
            stats_text += f"\n  • {format_type}: {count}"
        
        self.stats_label.config(text=stats_text)
    
    def update_filter_options(self):
        """Aktualisiert die Filter-Optionen."""
        if not self.all_markers:
            return
        
        stats = self.search_engine.get_search_statistics(self.all_markers)
        
        # Kategorien
        categories = sorted(stats['categories'].keys())
        self.category_combo['values'] = [''] + categories
        
        # Formate
        formats = sorted(stats['formats'].keys())
        self.format_combo['values'] = [''] + formats
    
    def on_search_change(self, *args):
        """Wird aufgerufen wenn sich die Suche ändert."""
        query = self.search_var.get()
        self.filtered_markers = self.search_engine.live_search(query, self.all_markers)
        self.apply_active_filters()
        self.update_marker_list()
        self.update_search_statistics()
    
    def on_filter_change(self, *args):
        """Wird aufgerufen wenn sich Filter ändern."""
        self.apply_active_filters()
        self.update_marker_list()
        self.update_search_statistics()
    
    def apply_active_filters(self):
        """Wendet aktive Filter an."""
        filters = {}
        
        if self.category_var.get():
            filters['category'] = self.category_var.get()
        
        if self.format_var.get():
            filters['format'] = self.format_var.get()
        
        if self.error_only_var.get():
            filters['error_only'] = True
        
        if filters:
            self.filtered_markers = self.search_engine.apply_filters(self.filtered_markers, filters)
    
    def update_search_statistics(self):
        """Aktualisiert die Such-Statistiken."""
        if not self.filtered_markers:
            self.search_stats_label.config(text="Keine Ergebnisse")
            return
        
        query = self.search_var.get()
        if query:
            self.search_stats_label.config(
                text=f"🔍 Suche: '{query}' - {len(self.filtered_markers)} Ergebnisse"
            )
        else:
            self.search_stats_label.config(
                text=f"📋 Alle Marker: {len(self.filtered_markers)}"
            )
    
    def clear_search(self):
        """Löscht die Suche."""
        self.search_var.set("")
    
    def clear_filters(self):
        """Löscht alle Filter."""
        self.category_var.set("")
        self.format_var.set("")
        self.error_only_var.set(False)
        self.filtered_markers = self.all_markers.copy()
        self.update_marker_list()
        self.update_search_statistics()
    
    def on_marker_select(self, event):
        """Wird aufgerufen wenn ein Marker ausgewählt wird."""
        selection = self.marker_listbox.curselection()
        if not selection:
            self.selected_marker = None
            self.details_text.delete("1.0", tk.END)
            return
        
        index = selection[0]
        if index < len(self.filtered_markers):
            self.selected_marker = self.filtered_markers[index]
            self.show_marker_details(self.selected_marker)
    
    def show_marker_details(self, marker):
        """Zeigt Marker-Details an."""
        self.details_text.delete("1.0", tk.END)
        
        details = f"""📋 Marker-Details:

🆔 ID: {marker.get('id', 'Unbekannt')}
📊 Level: {marker.get('level', 1)}
📝 Beschreibung: {marker.get('description', 'Keine')}
🏷️ Kategorie: {marker.get('category', 'general')}
📄 Format: {marker.get('format', 'unknown')}
📁 Datei: {marker.get('source_file', 'Unbekannt')}

"""
        
        # Beispiele
        examples = marker.get('examples', [])
        if examples:
            details += "📚 Beispiele:\n"
            for i, example in enumerate(examples, 1):
                details += f"  {i}. {example}\n"
            details += "\n"
        
        # Fehler-Informationen
        if 'error' in marker:
            details += f"❌ Fehler: {marker['error']}\n\n"
        
        # Validierung
        is_valid, errors = self.marker_manager.validate_marker(marker)
        if not is_valid:
            details += "⚠️ Validierungsfehler:\n"
            for error in errors:
                details += f"  • {error}\n"
        
        self.details_text.insert("1.0", details)
    
    def create_markers(self):
        """Erstellt Marker aus dem eingegebenen Text."""
        text = self.text_widget.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showinfo("Info", "Bitte geben Sie Text ein!")
            return
        
        try:
            # Text in Marker-Blöcke aufteilen
            blocks = self.split_marker_blocks(text)
            
            created_markers = []
            used_ids = set()
            
            for i, block in enumerate(blocks):
                if not block.strip():
                    continue
                
                # Marker parsen
                marker_data = self.marker_manager.smart_parse_text(block)
                
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
                
                created_markers.append(marker_data)
            
            # Erfolgsmeldung
            success_message = f"""✅ {len(created_markers)} Marker erfolgreich erstellt!

"""
            for marker in created_markers:
                success_message += f"📁 {marker['id']}.yaml\n"
            
            success_message += "\nDie Marker wurden automatisch korrekt formatiert und gespeichert."
            
            messagebox.showinfo("Erfolg!", success_message)
            self.update_status(f"Marker erstellt: {len(created_markers)} Dateien")
            
            # GUI aktualisieren
            self.text_widget.delete("1.0", tk.END)
            self.load_existing_markers()
            
        except Exception as e:
            error_message = f"""❌ Fehler beim Erstellen der Marker:

🔧 Was wir versucht haben:
- Ihren Text zu verstehen
- Automatisch zu korrigieren
- Als Marker zu speichern

💡 Versuchen Sie es nochmal mit einem einfacheren Text.

Technischer Fehler: {str(e)}"""
            
            messagebox.showerror("Fehler", error_message)
            self.update_status("Fehler beim Erstellen")
    
    def split_marker_blocks(self, text):
        """Teilt Text in Marker-Blöcke auf."""
        separators = ['---', '###', '***']
        blocks = [text]
        
        for sep in separators:
            new_blocks = []
            for block in blocks:
                new_blocks.extend(block.split(sep))
            blocks = new_blocks
        
        return [block.strip() for block in blocks if block.strip()]
    
    def edit_marker(self):
        """Öffnet den Inline-Editor für den ausgewählten Marker."""
        if not self.selected_marker:
            messagebox.showinfo("Info", "Bitte wählen Sie einen Marker aus!")
            return
        
        # Erstelle InlineEditor-Instanz
        InlineEditor(self.root, self.selected_marker, self.selected_marker.get('source_file'))
    
    def delete_marker(self):
        """Löscht den ausgewählten Marker."""
        if not self.selected_marker:
            messagebox.showinfo("Info", "Bitte wählen Sie einen Marker aus!")
            return
        
        marker_id = self.selected_marker.get('id', 'Unbekannt')
        result = messagebox.askyesno("Bestätigung", 
                                   f"Möchten Sie den Marker '{marker_id}' wirklich löschen?")
        
        if result:
            try:
                source_file = self.selected_marker.get('source_file')
                if source_file and os.path.exists(source_file):
                    os.remove(source_file)
                    self.update_status(f"Marker gelöscht: {marker_id}")
                    self.load_existing_markers()
                else:
                    messagebox.showerror("Fehler", "Datei nicht gefunden!")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Löschen: {str(e)}")
    
    def add_examples(self):
        """Fügt Beispiele zum ausgewählten Marker hinzu."""
        if not self.selected_marker:
            messagebox.showinfo("Info", "Bitte wählen Sie einen Marker aus!")
            return
        
        # TODO: Beispiel-Hinzufügung implementieren
        messagebox.showinfo("Info", "Beispiel-Hinzufügung wird in Phase 1.2 implementiert!")
    
    def clear_text(self):
        """Löscht den Eingabe-Text."""
        self.text_widget.delete("1.0", tk.END)
    
    def use_import_bridge(self):
        """Verwendet die Import Bridge für die Marker-Erstellung."""
        if not IMPORT_BRIDGE_AVAILABLE:
            messagebox.showerror("Fehler", "Import Bridge ist nicht verfügbar!")
            return
        
        text = self.text_widget.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warnung", "Kein Text zum Importieren vorhanden!")
            return
        
        try:
            # Verwende Import Bridge
            blocks = self.yaml_splitter.split(text)
            imported_count = 0
            failed_count = 0
            
            for block in blocks:
                if not block.strip():
                    continue
                
                # Validiere Marker
                data, errors = self.marker_validator.validate(block)
                
                if errors:
                    # Versuche Reparatur
                    from marker_repair_engine import MarkerRepairEngine
                    repairer = MarkerRepairEngine({})
                    data, _ = repairer.repair(data)
                    
                    # Validiere erneut
                    from io import StringIO
                    yaml = YAML()
                    stream = StringIO()
                    yaml.dump(data, stream)
                    yaml_str = stream.getvalue()
                    data, errors = self.marker_validator.validate(yaml_str)
                    
                    if errors:
                        failed_count += 1
                        self.history_logger.append({
                            "status": "failed", 
                            "errors": errors, 
                            "snippet": block
                        })
                        continue
                    else:
                        status = "fixed"
                else:
                    status = "imported"
                
                # Schreibe Marker
                yaml_path, json_path = self.marker_writer.write(data)
                self.history_logger.append({
                    "status": status, 
                    "id": data["id"],
                    "paths": {
                        "yaml": str(yaml_path),
                        "json": str(json_path)
                    }
                })
                imported_count += 1
            
            # Aktualisiere GUI
            self.load_existing_markers()
            
            # Zeige Ergebnis
            if failed_count == 0:
                messagebox.showinfo("Erfolg", f"✅ {imported_count} Marker erfolgreich importiert!")
            else:
                messagebox.showwarning("Teilweise erfolgreich", 
                                     f"✅ {imported_count} Marker importiert\n❌ {failed_count} Marker fehlgeschlagen")
            
            self.update_status(f"Import Bridge: {imported_count} importiert, {failed_count} fehlgeschlagen")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Import Bridge Fehler: {str(e)}")
            self.update_status(f"❌ Import Bridge Fehler: {str(e)}")
    
    def import_from_file(self):
        """Importiert Marker aus einer Datei."""
        if not IMPORT_BRIDGE_AVAILABLE:
            messagebox.showerror("Fehler", "Import Bridge ist nicht verfügbar!")
            return
        
        file_path = filedialog.askopenfilename(
            title="Marker-Datei auswählen",
            filetypes=[
                ("Alle Dateien", "*.*"),
                ("Text-Dateien", "*.txt"),
                ("YAML-Dateien", "*.yaml;*.yml"),
                ("JSON-Dateien", "*.json")
            ]
        )
        
        if not file_path:
            return
        
        try:
            # Lade Datei
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Zeige Inhalt im Text-Widget
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", content)
            
            # Verwende Import Bridge
            self.use_import_bridge()
            
            self.update_status(f"📁 Datei importiert: {Path(file_path).name}")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Datei: {str(e)}")
            self.update_status(f"❌ Datei-Lade-Fehler: {str(e)}")
    
    def load_demo(self):
        """Lädt Demo-Marker."""
        demo_text = """DEMO_MARKER_1
Level: 1
Beschreibung: Demo-Marker für Tests
Kategorie: demo
Beispiele:
- Demo-Beispiel 1
- Demo-Beispiel 2

---

DEMO_MARKER_2
Level: 2
Beschreibung: Zweiter Demo-Marker
Kategorie: demo
Beispiele:
- Weitere Demo-Beispiele"""
        
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", demo_text)
    
    def refresh_markers(self):
        """Aktualisiert die Marker-Liste."""
        self.load_existing_markers()
    
    def change_directory(self):
        """Ändert das Marker-Verzeichnis."""
        new_dir = filedialog.askdirectory(title="Marker-Verzeichnis wählen")
        if new_dir:
            self.marker_dir = Path(new_dir)
            self.load_existing_markers()
    
    def update_status(self, message):
        """Aktualisiert die Status-Anzeige."""
        self.status_label.config(text=message)
        
        # Performance-Info aktualisieren
        perf_info = self.search_engine.get_performance_info()
        self.performance_label.config(
            text=f"Cache: {perf_info['cache_size']} | "
                 f"Fuzzy: {perf_info['fuzzy_threshold']:.1f}"
        )
    
    def run(self):
        """Startet die GUI."""
        self.root.mainloop()


def main():
    """Hauptfunktion."""
    app = EnhancedSmartMarkerGUI()
    app.run()


if __name__ == "__main__":
    main() 