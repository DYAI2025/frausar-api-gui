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
- Batch-Import-Funktionen für Massenverarbeitung
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import yaml
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import threading
import time

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


class BatchImportManager:
    """Verwaltet Batch-Import-Operationen für mehrere Dateien."""
    
    def __init__(self, marker_dir, json_dir, history_logger=None):
        """Initialisiert den Batch-Import-Manager."""
        self.marker_dir = Path(marker_dir)
        self.json_dir = Path(json_dir)
        self.history_logger = history_logger
        self.import_results = []
        self.duplicate_checker = set()
        
        # Import Bridge Komponenten
        if IMPORT_BRIDGE_AVAILABLE:
            self.yaml_splitter = YAMLBlockSplitter()
            self.marker_validator = MarkerValidator()
            self.marker_writer = MarkerWriter(self.marker_dir, self.json_dir)
        else:
            self.yaml_splitter = None
            self.marker_validator = None
            self.marker_writer = None
    
    def process_batch_files(self, file_paths: List[Path], progress_callback=None) -> Dict[str, Any]:
        """Verarbeitet mehrere Dateien im Batch-Modus."""
        results = {
            'total_files': len(file_paths),
            'successful_imports': 0,
            'failed_imports': 0,
            'duplicates_found': 0,
            'total_markers': 0,
            'errors': [],
            'imported_files': [],
            'failed_files': []
        }
        
        for i, file_path in enumerate(file_paths):
            try:
                # Progress-Callback
                if progress_callback:
                    progress_callback(i + 1, len(file_paths), f"Verarbeite: {file_path.name}")
                
                # Datei verarbeiten
                file_result = self.process_single_file(file_path)
                
                # Ergebnisse sammeln
                results['total_markers'] += file_result.get('markers_processed', 0)
                results['duplicates_found'] += file_result.get('duplicates', 0)
                
                if file_result['success']:
                    results['successful_imports'] += 1
                    results['imported_files'].append(str(file_path))
                else:
                    results['failed_imports'] += 1
                    results['failed_files'].append(str(file_path))
                    results['errors'].extend(file_result.get('errors', []))
                
                # Kurze Pause für UI-Update
                time.sleep(0.01)
                
            except Exception as e:
                results['failed_imports'] += 1
                results['failed_files'].append(str(file_path))
                results['errors'].append(f"Fehler bei {file_path.name}: {str(e)}")
        
        return results
    
    def process_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Verarbeitet eine einzelne Datei."""
        result = {
            'file_path': str(file_path),
            'success': False,
            'markers_processed': 0,
            'duplicates': 0,
            'errors': []
        }
        
        try:
            # Datei lesen
            content = file_path.read_text(encoding='utf-8')
            
            if not IMPORT_BRIDGE_AVAILABLE:
                result['errors'].append("Import Bridge nicht verfügbar")
                return result
            
            # YAML-Blöcke aufteilen
            blocks = self.yaml_splitter.split_blocks(content)
            
            for block in blocks:
                try:
                    # Marker validieren
                    data, errors = self.marker_validator.validate(block)
                    
                    if errors:
                        result['errors'].extend([f"Validierungsfehler: {e}" for e in errors])
                        continue
                    
                    # Duplikat-Check
                    marker_id = data.get('id', '')
                    if marker_id in self.duplicate_checker:
                        result['duplicates'] += 1
                        continue
                    
                    # Marker schreiben
                    success = self.marker_writer.write_marker(data)
                    if success:
                        self.duplicate_checker.add(marker_id)
                        result['markers_processed'] += 1
                        
                        # History loggen
                        if self.history_logger:
                            self.history_logger.log_import(
                                marker_id, str(file_path), "batch_import", "success"
                            )
                    else:
                        result['errors'].append(f"Fehler beim Schreiben von Marker {marker_id}")
                
                except Exception as e:
                    result['errors'].append(f"Fehler bei Marker-Verarbeitung: {str(e)}")
            
            result['success'] = result['markers_processed'] > 0
            
        except Exception as e:
            result['errors'].append(f"Datei-Fehler: {str(e)}")
        
        return result
    
    def get_supported_extensions(self) -> List[str]:
        """Gibt unterstützte Datei-Erweiterungen zurück."""
        return ['.txt', '.py', '.json', '.yaml', '.yml', '.md']
    
    def validate_file_selection(self, file_paths: List[Path]) -> Dict[str, Any]:
        """Validiert die ausgewählten Dateien."""
        validation = {
            'valid_files': [],
            'invalid_files': [],
            'errors': []
        }
        
        for file_path in file_paths:
            if not file_path.exists():
                validation['invalid_files'].append(str(file_path))
                validation['errors'].append(f"Datei nicht gefunden: {file_path}")
                continue
            
            if file_path.suffix.lower() not in self.get_supported_extensions():
                validation['invalid_files'].append(str(file_path))
                validation['errors'].append(f"Nicht unterstütztes Format: {file_path.suffix}")
                continue
            
            validation['valid_files'].append(file_path)
        
        return validation


class BatchImportDialog:
    """Dialog für Batch-Import-Operationen."""
    
    def __init__(self, parent, batch_manager):
        """Initialisiert den Batch-Import-Dialog."""
        self.parent = parent
        self.batch_manager = batch_manager
        self.selected_files = []
        self.import_results = None
        
        # Dialog-Fenster
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("📦 Batch-Import Manager")
        self.dialog.geometry("900x700")
        self.dialog.resizable(True, True)
        
        # Zentriere das Fenster
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # GUI-Setup
        self.setup_ui()
        
        # Event-Bindings
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_ui(self):
        """Erstellt die Dialog-Benutzeroberfläche."""
        # Haupt-Container
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title = ttk.Label(main_frame, text="📦 Batch-Import Manager", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))
        
        # Datei-Auswahl-Bereich
        file_frame = ttk.LabelFrame(main_frame, text="📁 Dateien auswählen", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons für Datei-Auswahl
        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="📂 Dateien auswählen", 
                  command=self.select_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="🗑️ Alle löschen", 
                  command=self.clear_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="🔄 Aktualisieren", 
                  command=self.refresh_file_list).pack(side=tk.LEFT)
        
        # Datei-Liste
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar für Datei-Liste
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Datei-Listbox
        self.file_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Progress-Bereich
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Fortschritt", padding="10")
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Progress-Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Status-Label
        self.status_label = ttk.Label(progress_frame, text="Bereit für Import...")
        self.status_label.pack()
        
        # Import-Button
        self.import_button = ttk.Button(main_frame, text="🚀 Batch-Import starten", 
                                       command=self.start_batch_import)
        self.import_button.pack(pady=(0, 10))
        
        # Ergebnisse-Bereich
        results_frame = ttk.LabelFrame(main_frame, text="📋 Import-Ergebnisse", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ergebnisse-Text
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def select_files(self):
        """Öffnet Datei-Auswahl-Dialog."""
        filetypes = [
            ("Alle unterstützten Formate", "*.txt *.py *.json *.yaml *.yml *.md"),
            ("Text-Dateien", "*.txt"),
            ("Python-Dateien", "*.py"),
            ("JSON-Dateien", "*.json"),
            ("YAML-Dateien", "*.yaml *.yml"),
            ("Markdown-Dateien", "*.md"),
            ("Alle Dateien", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Dateien für Batch-Import auswählen",
            filetypes=filetypes
        )
        
        if files:
            self.selected_files.extend([Path(f) for f in files])
            self.refresh_file_list()
    
    def clear_files(self):
        """Löscht alle ausgewählten Dateien."""
        self.selected_files.clear()
        self.refresh_file_list()
    
    def refresh_file_list(self):
        """Aktualisiert die Datei-Liste."""
        self.file_listbox.delete(0, tk.END)
        
        for file_path in self.selected_files:
            self.file_listbox.insert(tk.END, f"📄 {file_path.name} ({file_path.parent})")
        
        # Status aktualisieren
        count = len(self.selected_files)
        self.status_label.config(text=f"{count} Datei(en) ausgewählt")
    
    def start_batch_import(self):
        """Startet den Batch-Import-Prozess."""
        if not self.selected_files:
            messagebox.showwarning("Warnung", "Keine Dateien ausgewählt!")
            return
        
        # Validierung
        validation = self.batch_manager.validate_file_selection(self.selected_files)
        
        if validation['invalid_files']:
            error_msg = "Folgende Dateien sind ungültig:\n\n"
            error_msg += "\n".join(validation['errors'])
            messagebox.showerror("Validierungsfehler", error_msg)
            return
        
        # Import starten
        self.import_button.config(state="disabled")
        self.progress_var.set(0)
        self.status_label.config(text="Import läuft...")
        
        # Thread für Import
        import_thread = threading.Thread(target=self.run_batch_import)
        import_thread.daemon = True
        import_thread.start()
    
    def run_batch_import(self):
        """Führt den Batch-Import in einem separaten Thread aus."""
        try:
            def progress_callback(current, total, message):
                progress = (current / total) * 100
                self.dialog.after(0, lambda: self.progress_var.set(progress))
                self.dialog.after(0, lambda: self.status_label.config(text=message))
            
            # Batch-Import ausführen
            results = self.batch_manager.process_batch_files(
                self.selected_files, progress_callback
            )
            
            # Ergebnisse anzeigen
            self.dialog.after(0, lambda: self.show_import_results(results))
            
        except Exception as e:
            self.dialog.after(0, lambda: messagebox.showerror("Import-Fehler", str(e)))
        finally:
            self.dialog.after(0, lambda: self.import_button.config(state="normal"))
    
    def show_import_results(self, results):
        """Zeigt die Import-Ergebnisse an."""
        self.import_results = results
        
        # Ergebnisse formatieren
        report = f"""📊 BATCH-IMPORT ERGEBNISSE
{'='*50}

📁 Dateien verarbeitet: {results['total_files']}
✅ Erfolgreiche Imports: {results['successful_imports']}
❌ Fehlgeschlagene Imports: {results['failed_imports']}
🔄 Marker verarbeitet: {results['total_markers']}
🔄 Duplikate gefunden: {results['duplicates_found']}

📋 IMPORTIERTE DATEIEN:
{'-'*30}
"""
        
        for file_path in results['imported_files']:
            report += f"✅ {Path(file_path).name}\n"
        
        if results['failed_files']:
            report += f"\n❌ FEHLGESCHLAGENE DATEIEN:\n{'-'*30}\n"
            for file_path in results['failed_files']:
                report += f"❌ {Path(file_path).name}\n"
        
        if results['errors']:
            report += f"\n⚠️ FEHLER:\n{'-'*30}\n"
            for error in results['errors'][:10]:  # Maximal 10 Fehler anzeigen
                report += f"• {error}\n"
            
            if len(results['errors']) > 10:
                report += f"... und {len(results['errors']) - 10} weitere Fehler\n"
        
        # Ergebnisse anzeigen
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, report)
        
        # Status aktualisieren
        success_rate = (results['successful_imports'] / results['total_files']) * 100
        self.status_label.config(
            text=f"Import abgeschlossen: {success_rate:.1f}% Erfolgsrate"
        )
        
        # Erfolgsmeldung
        if results['successful_imports'] > 0:
            messagebox.showinfo(
                "Import erfolgreich", 
                f"{results['successful_imports']} von {results['total_files']} Dateien erfolgreich importiert!\n"
                f"{results['total_markers']} Marker verarbeitet."
            )
    
    def on_close(self):
        """Behandelt das Schließen des Dialogs."""
        self.dialog.destroy()


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


class StatisticsManager:
    """Verwaltet erweiterte Statistiken und Analytics für das Marker-System."""
    
    def __init__(self, marker_dir, json_dir):
        """Initialisiert den Statistics-Manager."""
        self.marker_dir = Path(marker_dir)
        self.json_dir = Path(json_dir)
        self.stats_cache = {}
        self.last_update = None
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Gibt umfassende Statistiken zurück."""
        stats = {
            'total_markers': 0,
            'categories': {},
            'formats': {},
            'levels': {},
            'status': {},
            'authors': {},
            'growth_data': [],
            'recent_activity': [],
            'validation_stats': {
                'valid': 0,
                'invalid': 0,
                'errors': []
            },
            'import_stats': {
                'total_imports': 0,
                'successful_imports': 0,
                'failed_imports': 0,
                'duplicates_found': 0
            },
            'performance': {
                'cache_size': 0,
                'search_speed': 0,
                'import_speed': 0
            }
        }
        
        try:
            # Marker-Dateien analysieren
            marker_files = list(self.marker_dir.glob("*.yaml")) + list(self.marker_dir.glob("*.yml"))
            stats['total_markers'] = len(marker_files)
            
            for file_path in marker_files:
                try:
                    # Datei-Statistiken
                    file_stats = self.analyze_marker_file(file_path)
                    
                    # Kategorien zählen
                    category = file_stats.get('category', 'unknown')
                    stats['categories'][category] = stats['categories'].get(category, 0) + 1
                    
                    # Level zählen
                    level = file_stats.get('level', 0)
                    stats['levels'][level] = stats['levels'].get(level, 0) + 1
                    
                    # Status zählen
                    status = file_stats.get('status', 'unknown')
                    stats['status'][status] = stats['status'].get(status, 0) + 1
                    
                    # Autoren zählen
                    author = file_stats.get('author', 'unknown')
                    stats['authors'][author] = stats['authors'].get(author, 0) + 1
                    
                    # Wachstumsdaten
                    if 'created_date' in file_stats:
                        stats['growth_data'].append({
                            'date': file_stats['created_date'],
                            'marker_id': file_stats.get('id', 'unknown'),
                            'category': category
                        })
                    
                    # Validierungsstatistiken
                    if file_stats.get('is_valid', True):
                        stats['validation_stats']['valid'] += 1
                    else:
                        stats['validation_stats']['invalid'] += 1
                        stats['validation_stats']['errors'].append({
                            'file': file_path.name,
                            'errors': file_stats.get('validation_errors', [])
                        })
                
                except Exception as e:
                    stats['validation_stats']['invalid'] += 1
                    stats['validation_stats']['errors'].append({
                        'file': file_path.name,
                        'errors': [str(e)]
                    })
            
            # Wachstumsdaten sortieren
            stats['growth_data'].sort(key=lambda x: x['date'])
            
            # Format-Statistiken
            stats['formats'] = {
                'yaml': len(list(self.marker_dir.glob("*.yaml"))),
                'yml': len(list(self.marker_dir.glob("*.yml")))
            }
            
            # JSON-Statistiken
            json_files = list(self.json_dir.glob("*.json"))
            stats['import_stats']['total_imports'] = len(json_files)
            
            # Performance-Statistiken (Beispielwerte)
            stats['performance'] = {
                'cache_size': len(stats['categories']),
                'search_speed': 0.1,  # Sekunden
                'import_speed': 0.5   # Sekunden pro Marker
            }
            
        except Exception as e:
            stats['validation_stats']['errors'].append({
                'file': 'statistics_manager',
                'errors': [str(e)]
            })
        
        return stats
    
    def analyze_marker_file(self, file_path: Path) -> Dict[str, Any]:
        """Analysiert eine einzelne Marker-Datei."""
        stats = {
            'id': 'unknown',
            'category': 'unknown',
            'level': 0,
            'status': 'unknown',
            'author': 'unknown',
            'created_date': None,
            'is_valid': True,
            'validation_errors': []
        }
        
        try:
            # Datei lesen
            content = file_path.read_text(encoding='utf-8')
            
            # YAML parsen
            import yaml
            data = yaml.safe_load(content)
            
            if data:
                stats['id'] = data.get('id', 'unknown')
                stats['category'] = data.get('category', 'unknown')
                stats['level'] = data.get('level', 0)
                stats['status'] = data.get('status', 'unknown')
                stats['author'] = data.get('author', 'unknown')
                
                # Erstellungsdatum aus Datei-Metadaten
                stats['created_date'] = datetime.fromtimestamp(file_path.stat().st_ctime)
            
        except Exception as e:
            stats['is_valid'] = False
            stats['validation_errors'].append(str(e))
        
        return stats
    
    def get_growth_chart_data(self) -> Dict[str, Any]:
        """Gibt Daten für Wachstums-Charts zurück."""
        stats = self.get_comprehensive_stats()
        
        # Gruppiere nach Monaten
        monthly_data = {}
        for item in stats['growth_data']:
            month_key = item['date'].strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    'total': 0,
                    'categories': {}
                }
            
            monthly_data[month_key]['total'] += 1
            category = item['category']
            monthly_data[month_key]['categories'][category] = monthly_data[month_key]['categories'].get(category, 0) + 1
        
        return {
            'labels': list(monthly_data.keys()),
            'datasets': [
                {
                    'label': 'Gesamt',
                    'data': [monthly_data[month]['total'] for month in monthly_data.keys()],
                    'borderColor': '#007bff',
                    'backgroundColor': 'rgba(0, 123, 255, 0.1)'
                }
            ],
            'category_data': monthly_data
        }
    
    def get_category_distribution(self) -> Dict[str, Any]:
        """Gibt Daten für Kategorie-Verteilung zurück."""
        stats = self.get_comprehensive_stats()
        
        categories = stats['categories']
        total = sum(categories.values())
        
        return {
            'labels': list(categories.keys()),
            'data': list(categories.values()),
            'percentages': [round((count / total) * 100, 1) for count in categories.values()],
            'colors': self.generate_colors(len(categories))
        }
    
    def get_level_distribution(self) -> Dict[str, Any]:
        """Gibt Daten für Level-Verteilung zurück."""
        stats = self.get_comprehensive_stats()
        
        levels = stats['levels']
        total = sum(levels.values())
        
        return {
            'labels': [f"Level {level}" for level in sorted(levels.keys())],
            'data': [levels[level] for level in sorted(levels.keys())],
            'percentages': [round((count / total) * 100, 1) for count in levels.values()],
            'colors': self.generate_colors(len(levels))
        }
    
    def generate_colors(self, count: int) -> List[str]:
        """Generiert Farben für Charts."""
        colors = [
            '#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1',
            '#fd7e14', '#20c997', '#e83e8c', '#6c757d', '#17a2b8'
        ]
        
        # Wiederhole Farben falls nötig
        while len(colors) < count:
            colors.extend(colors[:count - len(colors)])
        
        return colors[:count]
    
    def get_recent_activity(self, days: int = 7) -> List[Dict[str, Any]]:
        """Gibt die letzten Aktivitäten zurück."""
        stats = self.get_comprehensive_stats()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_activity = []
        
        for item in stats['growth_data']:
            if item['date'] >= cutoff_date:
                recent_activity.append({
                    'date': item['date'].strftime('%Y-%m-%d %H:%M'),
                    'marker_id': item['marker_id'],
                    'category': item['category'],
                    'action': 'created'
                })
        
        return sorted(recent_activity, key=lambda x: x['date'], reverse=True)
    
    def export_statistics_report(self, output_path: Path) -> bool:
        """Exportiert einen detaillierten Statistiken-Bericht."""
        try:
            stats = self.get_comprehensive_stats()
            
            report = f"""# Enhanced Smart Marker System - Statistiken
Erstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Übersicht
- **Gesamt-Marker**: {stats['total_markers']}
- **Gültige Marker**: {stats['validation_stats']['valid']}
- **Ungültige Marker**: {stats['validation_stats']['invalid']}
- **Erfolgsrate**: {round((stats['validation_stats']['valid'] / max(stats['total_markers'], 1)) * 100, 1)}%

## 📂 Kategorien
"""
            
            for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
                percentage = round((count / max(stats['total_markers'], 1)) * 100, 1)
                report += f"- **{category}**: {count} ({percentage}%)\n"
            
            report += f"""
## 📈 Level-Verteilung
"""
            
            for level in sorted(stats['levels'].keys()):
                count = stats['levels'][level]
                percentage = round((count / max(stats['total_markers'], 1)) * 100, 1)
                report += f"- **Level {level}**: {count} ({percentage}%)\n"
            
            report += f"""
## 👥 Autoren
"""
            
            for author, count in sorted(stats['authors'].items(), key=lambda x: x[1], reverse=True):
                percentage = round((count / max(stats['total_markers'], 1)) * 100, 1)
                report += f"- **{author}**: {count} ({percentage}%)\n"
            
            if stats['validation_stats']['errors']:
                report += f"""
## ⚠️ Validierungsfehler
"""
                
                for error in stats['validation_stats']['errors'][:10]:  # Maximal 10 Fehler
                    report += f"- **{error['file']}**: {', '.join(error['errors'])}\n"
            
            # Bericht speichern
            output_path.write_text(report, encoding='utf-8')
            return True
            
        except Exception as e:
            print(f"Fehler beim Exportieren des Berichts: {e}")
            return False


class StatisticsDialog:
    """Dialog für erweiterte Statistiken und Analytics."""
    
    def __init__(self, parent, statistics_manager):
        """Initialisiert den Statistics-Dialog."""
        self.parent = parent
        self.statistics_manager = statistics_manager
        
        # Dialog-Fenster
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("📊 Erweiterte Statistiken & Analytics")
        self.dialog.geometry("1000x800")
        self.dialog.resizable(True, True)
        
        # Zentriere das Fenster
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # GUI-Setup
        self.setup_ui()
        self.load_statistics()
        
        # Event-Bindings
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_ui(self):
        """Erstellt die Dialog-Benutzeroberfläche."""
        # Haupt-Container
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title = ttk.Label(main_frame, text="📊 Erweiterte Statistiken & Analytics", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))
        
        # Notebook für Tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Übersicht
        self.overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_frame, text="📋 Übersicht")
        self.setup_overview_tab()
        
        # Tab 2: Kategorien
        self.categories_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.categories_frame, text="📂 Kategorien")
        self.setup_categories_tab()
        
        # Tab 3: Wachstum
        self.growth_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.growth_frame, text="📈 Wachstum")
        self.setup_growth_tab()
        
        # Tab 4: Aktivität
        self.activity_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.activity_frame, text="🕒 Aktivität")
        self.setup_activity_tab()
        
        # Button-Bereich
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="🔄 Aktualisieren", 
                  command=self.refresh_statistics).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="📄 Bericht exportieren", 
                  command=self.export_report).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="❌ Schließen", 
                  command=self.on_close).pack(side=tk.RIGHT)
    
    def setup_overview_tab(self):
        """Erstellt den Übersicht-Tab."""
        # Haupt-Statistiken
        stats_frame = ttk.LabelFrame(self.overview_frame, text="📊 Haupt-Statistiken", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Statistik-Labels
        self.total_label = ttk.Label(stats_frame, text="Gesamt-Marker: 0", font=("Arial", 12))
        self.total_label.pack(anchor=tk.W)
        
        self.valid_label = ttk.Label(stats_frame, text="Gültige Marker: 0", font=("Arial", 12))
        self.valid_label.pack(anchor=tk.W)
        
        self.success_rate_label = ttk.Label(stats_frame, text="Erfolgsrate: 0%", font=("Arial", 12))
        self.success_rate_label.pack(anchor=tk.W)
        
        # Level-Verteilung
        level_frame = ttk.LabelFrame(self.overview_frame, text="📈 Level-Verteilung", padding="10")
        level_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.level_text = scrolledtext.ScrolledText(level_frame, height=8)
        self.level_text.pack(fill=tk.BOTH, expand=True)
        
        # Autoren-Statistiken
        authors_frame = ttk.LabelFrame(self.overview_frame, text="👥 Top-Autoren", padding="10")
        authors_frame.pack(fill=tk.BOTH, expand=True)
        
        self.authors_text = scrolledtext.ScrolledText(authors_frame, height=6)
        self.authors_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_categories_tab(self):
        """Erstellt den Kategorien-Tab."""
        # Kategorie-Verteilung
        cat_frame = ttk.LabelFrame(self.categories_frame, text="📂 Kategorie-Verteilung", padding="10")
        cat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.categories_text = scrolledtext.ScrolledText(cat_frame, height=15)
        self.categories_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_growth_tab(self):
        """Erstellt den Wachstum-Tab."""
        # Wachstums-Daten
        growth_frame = ttk.LabelFrame(self.growth_frame, text="📈 Marker-Wachstum", padding="10")
        growth_frame.pack(fill=tk.BOTH, expand=True)
        
        self.growth_text = scrolledtext.ScrolledText(growth_frame, height=15)
        self.growth_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_activity_tab(self):
        """Erstellt den Aktivität-Tab."""
        # Letzte Aktivitäten
        activity_frame = ttk.LabelFrame(self.activity_frame, text="🕒 Letzte Aktivitäten", padding="10")
        activity_frame.pack(fill=tk.BOTH, expand=True)
        
        self.activity_text = scrolledtext.ScrolledText(activity_frame, height=15)
        self.activity_text.pack(fill=tk.BOTH, expand=True)
    
    def load_statistics(self):
        """Lädt die Statistiken."""
        try:
            # Haupt-Statistiken laden
            stats = self.statistics_manager.get_comprehensive_stats()
            
            # Übersicht aktualisieren
            self.total_label.config(text=f"Gesamt-Marker: {stats['total_markers']}")
            self.valid_label.config(text=f"Gültige Marker: {stats['validation_stats']['valid']}")
            
            success_rate = round((stats['validation_stats']['valid'] / max(stats['total_markers'], 1)) * 100, 1)
            self.success_rate_label.config(text=f"Erfolgsrate: {success_rate}%")
            
            # Level-Verteilung
            level_dist = self.statistics_manager.get_level_distribution()
            level_text = "📊 Level-Verteilung:\n\n"
            for i, (label, count, percentage) in enumerate(zip(level_dist['labels'], level_dist['data'], level_dist['percentages'])):
                level_text += f"{label}: {count} Marker ({percentage}%)\n"
            
            self.level_text.delete(1.0, tk.END)
            self.level_text.insert(1.0, level_text)
            
            # Autoren-Statistiken
            authors_text = "👥 Top-Autoren:\n\n"
            for author, count in sorted(stats['authors'].items(), key=lambda x: x[1], reverse=True)[:10]:
                percentage = round((count / max(stats['total_markers'], 1)) * 100, 1)
                authors_text += f"• {author}: {count} Marker ({percentage}%)\n"
            
            self.authors_text.delete(1.0, tk.END)
            self.authors_text.insert(1.0, authors_text)
            
            # Kategorien
            cat_dist = self.statistics_manager.get_category_distribution()
            cat_text = "📂 Kategorie-Verteilung:\n\n"
            for i, (label, count, percentage) in enumerate(zip(cat_dist['labels'], cat_dist['data'], cat_dist['percentages'])):
                cat_text += f"• {label}: {count} Marker ({percentage}%)\n"
            
            self.categories_text.delete(1.0, tk.END)
            self.categories_text.insert(1.0, cat_text)
            
            # Wachstum
            growth_data = self.statistics_manager.get_growth_chart_data()
            growth_text = "📈 Marker-Wachstum:\n\n"
            for i, (month, data) in enumerate(growth_data['category_data'].items()):
                growth_text += f"📅 {month}: {data['total']} neue Marker\n"
                for category, count in data['categories'].items():
                    growth_text += f"   • {category}: {count}\n"
                growth_text += "\n"
            
            self.growth_text.delete(1.0, tk.END)
            self.growth_text.insert(1.0, growth_text)
            
            # Aktivität
            recent_activity = self.statistics_manager.get_recent_activity()
            activity_text = "🕒 Letzte Aktivitäten (7 Tage):\n\n"
            for activity in recent_activity[:20]:  # Maximal 20 Einträge
                activity_text += f"📅 {activity['date']} - {activity['action']}: {activity['marker_id']} ({activity['category']})\n"
            
            self.activity_text.delete(1.0, tk.END)
            self.activity_text.insert(1.0, activity_text)
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Statistiken: {str(e)}")
    
    def refresh_statistics(self):
        """Aktualisiert die Statistiken."""
        self.load_statistics()
    
    def export_report(self):
        """Exportiert einen Statistiken-Bericht."""
        file_path = filedialog.asksaveasfilename(
            title="Statistiken-Bericht speichern",
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("Text", "*.txt"), ("Alle Dateien", "*.*")]
        )
        
        if file_path:
            success = self.statistics_manager.export_statistics_report(Path(file_path))
            if success:
                messagebox.showinfo("Erfolg", f"Bericht erfolgreich exportiert:\n{file_path}")
            else:
                messagebox.showerror("Fehler", "Fehler beim Exportieren des Berichts")
    
    def on_close(self):
        """Behandelt das Schließen des Dialogs."""
        self.dialog.destroy()


class TemplateManager:
    """Verwaltet Marker-Templates für schnellere Marker-Erstellung."""
    
    def __init__(self, template_dir=None):
        """Initialisiert den Template-Manager."""
        if template_dir is None:
            template_dir = Path.cwd() / "templates"
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(exist_ok=True)
        
        # Standard-Templates erstellen
        self.create_default_templates()
    
    def create_default_templates(self):
        """Erstellt Standard-Templates."""
        default_templates = {
            "basic_marker.yaml": """id: TEMPLATE_ID
level: 1
description: Template-Beschreibung
category: template
status: draft
author: template_user
version: 1.0.0
examples:
  - Beispiel 1
  - Beispiel 2
tags:
  - template
  - basic""",
            
            "production_marker.yaml": """id: PROD_TEMPLATE_ID
level: 2
description: Produktions-Marker Template
category: production
status: active
author: production_user
version: 1.0.0
priority: high
examples:
  - Produktions-Beispiel 1
  - Produktions-Beispiel 2
tags:
  - production
  - high-priority
validation_rules:
  - required_fields: [id, level, description]
  - id_format: "[A-Z]{1,3}_.+"
  - level_range: [1, 5]""",
            
            "python_code_marker.yaml": """id: PYTHON_TEMPLATE_ID
level: 3
description: Python-Code Marker Template
category: python
status: draft
author: python_user
version: 1.0.0
language: python
examples:
  - def function_name():
  - class ClassName:
  - import module_name
code_patterns:
  - pattern: "def\\s+\\w+\\s*\\("
    description: "Funktionsdefinition"
  - pattern: "class\\s+\\w+"
    description: "Klassendefinition"
tags:
  - python
  - code
  - programming""",
            
            "api_marker.yaml": """id: API_TEMPLATE_ID
level: 2
description: API-Marker Template
category: api
status: active
author: api_user
version: 1.0.0
endpoint: /api/endpoint
method: GET
examples:
  - curl -X GET http://api.example.com/endpoint
  - requests.get("http://api.example.com/endpoint")
tags:
  - api
  - rest
  - http
parameters:
  - name: param1
    type: string
    required: true
  - name: param2
    type: integer
    required: false""",
            
            "database_marker.yaml": """id: DB_TEMPLATE_ID
level: 2
description: Datenbank-Marker Template
category: database
status: active
author: db_user
version: 1.0.0
database_type: sql
examples:
  - SELECT * FROM table_name
  - INSERT INTO table_name VALUES (...)
  - UPDATE table_name SET column = value
tags:
  - database
  - sql
  - query
table_info:
  - table_name: example_table
    columns:
      - id (INTEGER, PRIMARY KEY)
      - name (VARCHAR(255))
      - created_at (TIMESTAMP)"""
        }
        
        for filename, content in default_templates.items():
            template_path = self.template_dir / filename
            if not template_path.exists():
                template_path.write_text(content, encoding='utf-8')
    
    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Gibt alle verfügbaren Templates zurück."""
        templates = []
        
        for template_file in self.template_dir.glob("*.yaml"):
            try:
                # Template-Metadaten extrahieren
                content = template_file.read_text(encoding='utf-8')
                template_info = self.extract_template_info(content, template_file.name)
                templates.append(template_info)
            except Exception as e:
                print(f"Fehler beim Lesen von Template {template_file.name}: {e}")
        
        return sorted(templates, key=lambda x: x['name'])
    
    def extract_template_info(self, content: str, filename: str) -> Dict[str, Any]:
        """Extrahiert Informationen aus einem Template."""
        import yaml
        
        try:
            data = yaml.safe_load(content)
            
            return {
                'name': filename.replace('.yaml', ''),
                'filename': filename,
                'id': data.get('id', 'TEMPLATE_ID'),
                'level': data.get('level', 1),
                'description': data.get('description', 'Keine Beschreibung'),
                'category': data.get('category', 'template'),
                'status': data.get('status', 'draft'),
                'author': data.get('author', 'unknown'),
                'version': data.get('version', '1.0.0'),
                'examples_count': len(data.get('examples', [])),
                'tags': data.get('tags', []),
                'content': content
            }
        except Exception as e:
            return {
                'name': filename.replace('.yaml', ''),
                'filename': filename,
                'id': 'TEMPLATE_ID',
                'level': 1,
                'description': f'Fehler beim Parsen: {str(e)}',
                'category': 'error',
                'status': 'error',
                'author': 'unknown',
                'version': '1.0.0',
                'examples_count': 0,
                'tags': ['error'],
                'content': content
            }
    
    def create_template(self, name: str, content: str) -> bool:
        """Erstellt ein neues Template."""
        try:
            template_path = self.template_dir / f"{name}.yaml"
            template_path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Fehler beim Erstellen des Templates: {e}")
            return False
    
    def delete_template(self, filename: str) -> bool:
        """Löscht ein Template."""
        try:
            template_path = self.template_dir / filename
            if template_path.exists():
                template_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Fehler beim Löschen des Templates: {e}")
            return False
    
    def get_template_content(self, filename: str) -> str:
        """Gibt den Inhalt eines Templates zurück."""
        try:
            template_path = self.template_dir / filename
            return template_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Fehler beim Lesen des Templates: {e}")
            return ""
    
    def apply_template(self, template_content: str, custom_values: Dict[str, str] = None) -> str:
        """Wendet ein Template mit benutzerdefinierten Werten an."""
        if custom_values is None:
            custom_values = {}
        
        # Template-Inhalt kopieren
        result = template_content
        
        # Standard-Ersetzungen
        default_replacements = {
            'TEMPLATE_ID': f"MARKER_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'PROD_TEMPLATE_ID': f"PROD_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'PYTHON_TEMPLATE_ID': f"PYTHON_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'API_TEMPLATE_ID': f"API_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'DB_TEMPLATE_ID': f"DB_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'template_user': custom_values.get('author', 'current_user'),
            'production_user': custom_values.get('author', 'current_user'),
            'python_user': custom_values.get('author', 'current_user'),
            'api_user': custom_values.get('author', 'current_user'),
            'db_user': custom_values.get('author', 'current_user'),
            'Template-Beschreibung': custom_values.get('description', 'Neue Marker-Beschreibung'),
            'template': custom_values.get('category', 'general')
        }
        
        # Benutzerdefinierte Werte hinzufügen
        for key, value in custom_values.items():
            default_replacements[key] = value
        
        # Ersetzungen durchführen
        for placeholder, value in default_replacements.items():
            result = result.replace(placeholder, str(value))
        
        return result
    
    def validate_template(self, content: str) -> Dict[str, Any]:
        """Validiert ein Template."""
        import yaml
        
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            data = yaml.safe_load(content)
            
            if not data:
                result['valid'] = False
                result['errors'].append("Template ist leer")
                return result
            
            # Pflichtfelder prüfen
            required_fields = ['id', 'level', 'description']
            for field in required_fields:
                if field not in data:
                    result['warnings'].append(f"Pflichtfeld '{field}' fehlt")
            
            # ID-Format prüfen
            if 'id' in data:
                import re
                if not re.match(r'[A-Z]{1,3}_.+', data['id']):
                    result['warnings'].append("ID-Format sollte '[A-Z]{1,3}_.+' sein")
            
            # Level-Bereich prüfen
            if 'level' in data:
                level = data['level']
                if not isinstance(level, int) or level < 1 or level > 5:
                    result['warnings'].append("Level sollte zwischen 1 und 5 sein")
            
        except yaml.YAMLError as e:
            result['valid'] = False
            result['errors'].append(f"YAML-Fehler: {str(e)}")
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Allgemeiner Fehler: {str(e)}")
        
        return result


class TemplateDialog:
    """Dialog für Template-Verwaltung und -Anwendung."""
    
    def __init__(self, parent, template_manager):
        """Initialisiert den Template-Dialog."""
        self.parent = parent
        self.template_manager = template_manager
        self.selected_template = None
        
        # Dialog-Fenster
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("📋 Marker-Templates")
        self.dialog.geometry("900x700")
        self.dialog.resizable(True, True)
        
        # Zentriere das Fenster
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # GUI-Setup
        self.setup_ui()
        self.load_templates()
        
        # Event-Bindings
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_ui(self):
        """Erstellt die Dialog-Benutzeroberfläche."""
        # Haupt-Container
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title = ttk.Label(main_frame, text="📋 Marker-Templates", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))
        
        # Template-Liste und Vorschau
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Linke Seite - Template-Liste
        left_frame = ttk.LabelFrame(content_frame, text="📋 Verfügbare Templates", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Template-Listbox
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar für Template-Liste
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Template-Listbox
        self.template_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.template_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.template_listbox.yview)
        
        # Template-Buttons
        template_buttons_frame = ttk.Frame(left_frame)
        template_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(template_buttons_frame, text="🔄 Aktualisieren", 
                  command=self.load_templates).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(template_buttons_frame, text="➕ Neues Template", 
                  command=self.create_new_template).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(template_buttons_frame, text="🗑️ Löschen", 
                  command=self.delete_selected_template).pack(side=tk.LEFT)
        
        # Rechte Seite - Vorschau und Anwendung
        right_frame = ttk.LabelFrame(content_frame, text="👁️ Vorschau & Anwendung", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Template-Info
        info_frame = ttk.LabelFrame(right_frame, text="ℹ️ Template-Informationen", padding="5")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_label = ttk.Label(info_frame, text="Wählen Sie ein Template aus...")
        self.info_label.pack(anchor=tk.W)
        
        # Benutzerdefinierte Werte
        values_frame = ttk.LabelFrame(right_frame, text="✏️ Benutzerdefinierte Werte", padding="5")
        values_frame.pack(fill=tk.X, pady=(0, 10))
        
        # ID
        ttk.Label(values_frame, text="ID:").pack(anchor=tk.W)
        self.id_var = tk.StringVar()
        self.id_entry = ttk.Entry(values_frame, textvariable=self.id_var)
        self.id_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Beschreibung
        ttk.Label(values_frame, text="Beschreibung:").pack(anchor=tk.W)
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(values_frame, textvariable=self.description_var)
        self.description_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Kategorie
        ttk.Label(values_frame, text="Kategorie:").pack(anchor=tk.W)
        self.category_var = tk.StringVar()
        self.category_entry = ttk.Entry(values_frame, textvariable=self.category_var)
        self.category_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Autor
        ttk.Label(values_frame, text="Autor:").pack(anchor=tk.W)
        self.author_var = tk.StringVar()
        self.author_entry = ttk.Entry(values_frame, textvariable=self.author_var)
        self.author_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Vorschau
        preview_frame = ttk.LabelFrame(right_frame, text="👁️ Vorschau", padding="5")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=10)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Anwendungs-Buttons
        apply_frame = ttk.Frame(right_frame)
        apply_frame.pack(fill=tk.X)
        
        ttk.Button(apply_frame, text="🔄 Vorschau aktualisieren", 
                  command=self.update_preview).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(apply_frame, text="✅ Template anwenden", 
                  command=self.apply_template).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(apply_frame, text="❌ Schließen", 
                  command=self.on_close).pack(side=tk.RIGHT)
        
        # Event-Bindings
        self.template_listbox.bind('<<ListboxSelect>>', self.on_template_select)
    
    def load_templates(self):
        """Lädt die verfügbaren Templates."""
        try:
            templates = self.template_manager.get_available_templates()
            
            self.template_listbox.delete(0, tk.END)
            self.templates_data = templates
            
            for template in templates:
                display_text = f"📋 {template['name']} ({template['category']}) - {template['description'][:50]}..."
                self.template_listbox.insert(tk.END, display_text)
            
            if templates:
                self.template_listbox.selection_set(0)
                self.on_template_select(None)
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Templates: {str(e)}")
    
    def on_template_select(self, event):
        """Behandelt die Template-Auswahl."""
        try:
            selection = self.template_listbox.curselection()
            if not selection:
                return
            
            index = selection[0]
            self.selected_template = self.templates_data[index]
            
            # Template-Informationen anzeigen
            template = self.selected_template
            info_text = f"""📋 {template['name']}
📝 Beschreibung: {template['description']}
🏷️ Kategorie: {template['category']}
👤 Autor: {template['author']}
📊 Level: {template['level']}
📈 Status: {template['status']}
🔄 Version: {template['version']}
📚 Beispiele: {template['examples_count']}
🏷️ Tags: {', '.join(template['tags'])}"""
            
            self.info_label.config(text=info_text)
            
            # Standardwerte setzen
            self.id_var.set(template['id'])
            self.description_var.set(template['description'])
            self.category_var.set(template['category'])
            self.author_var.set(template['author'])
            
            # Vorschau aktualisieren
            self.update_preview()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei Template-Auswahl: {str(e)}")
    
    def update_preview(self):
        """Aktualisiert die Vorschau."""
        if not self.selected_template:
            return
        
        try:
            # Benutzerdefinierte Werte sammeln
            custom_values = {
                'id': self.id_var.get(),
                'description': self.description_var.get(),
                'category': self.category_var.get(),
                'author': self.author_var.get()
            }
            
            # Template anwenden
            result = self.template_manager.apply_template(
                self.selected_template['content'], custom_values
            )
            
            # Vorschau anzeigen
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, result)
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei Vorschau-Aktualisierung: {str(e)}")
    
    def apply_template(self):
        """Wendet das Template an und schließt den Dialog."""
        if not self.selected_template:
            messagebox.showwarning("Warnung", "Kein Template ausgewählt!")
            return
        
        try:
            # Benutzerdefinierte Werte sammeln
            custom_values = {
                'id': self.id_var.get(),
                'description': self.description_var.get(),
                'category': self.category_var.get(),
                'author': self.author_var.get()
            }
            
            # Template anwenden
            result = self.template_manager.apply_template(
                self.selected_template['content'], custom_values
            )
            
            # Ergebnis an Haupt-GUI senden
            if hasattr(self.parent, 'text_widget'):
                self.parent.text_widget.delete(1.0, tk.END)
                self.parent.text_widget.insert(1.0, result)
                self.parent.update_status("✅ Template erfolgreich angewendet")
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Anwenden des Templates: {str(e)}")
    
    def create_new_template(self):
        """Erstellt ein neues Template."""
        # Einfacher Dialog für neues Template
        template_name = tk.simpledialog.askstring(
            "Neues Template", 
            "Name des neuen Templates:"
        )
        
        if template_name:
            # Standard-Template-Inhalt
            default_content = f"""id: {template_name.upper()}_ID
level: 1
description: Beschreibung für {template_name}
category: {template_name.lower()}
status: draft
author: current_user
version: 1.0.0
examples:
  - Beispiel 1
  - Beispiel 2
tags:
  - {template_name.lower()}
  - template"""
            
            success = self.template_manager.create_template(template_name, default_content)
            
            if success:
                messagebox.showinfo("Erfolg", f"Template '{template_name}' erstellt!")
                self.load_templates()
            else:
                messagebox.showerror("Fehler", "Fehler beim Erstellen des Templates")
    
    def delete_selected_template(self):
        """Löscht das ausgewählte Template."""
        if not self.selected_template:
            messagebox.showwarning("Warnung", "Kein Template ausgewählt!")
            return
        
        template_name = self.selected_template['filename']
        
        if messagebox.askyesno("Bestätigung", f"Template '{template_name}' wirklich löschen?"):
            success = self.template_manager.delete_template(template_name)
            
            if success:
                messagebox.showinfo("Erfolg", f"Template '{template_name}' gelöscht!")
                self.load_templates()
            else:
                messagebox.showerror("Fehler", "Fehler beim Löschen des Templates")
    
    def on_close(self):
        """Behandelt das Schließen des Dialogs."""
        self.dialog.destroy()


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
        
        # Batch-Import-Manager
        self.batch_import_manager = BatchImportManager(
            self.marker_dir, self.json_dir, self.history_logger
        )
        
        # Statistics-Manager
        self.statistics_manager = StatisticsManager(self.marker_dir, self.json_dir)
        
        # Template-Manager
        self.template_manager = TemplateManager()
        
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
                      command=self.import_from_file).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            ttk.Button(buttons_frame, text="📦 Batch-Import", 
                      command=self.open_batch_import).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 0))
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
        
        # Erweiterte Statistiken Button
        ttk.Button(stats_frame, text="📊 Erweiterte Statistiken", 
                  command=self.open_statistics_dialog).pack(fill=tk.X, pady=(5, 0))
        
        # Template-Button
        ttk.Button(stats_frame, text="📋 Marker-Templates", 
                  command=self.open_template_dialog).pack(fill=tk.X, pady=(5, 0))
    
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
    
    def open_batch_import(self):
        """Öffnet den Batch-Import-Dialog."""
        if not IMPORT_BRIDGE_AVAILABLE:
            messagebox.showerror("Fehler", "Import Bridge ist nicht verfügbar!")
            return
        
        try:
            # Batch-Import-Dialog öffnen
            batch_dialog = BatchImportDialog(self.root, self.batch_import_manager)
            self.update_status("📦 Batch-Import-Dialog geöffnet")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen des Batch-Import-Dialogs: {str(e)}")
            self.update_status(f"❌ Batch-Import-Fehler: {str(e)}")
    
    def open_statistics_dialog(self):
        """Öffnet den erweiterten Statistiken-Dialog."""
        try:
            # Statistics-Dialog öffnen
            stats_dialog = StatisticsDialog(self.root, self.statistics_manager)
            self.update_status("📊 Erweiterte Statistiken geöffnet")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen der Statistiken: {str(e)}")
            self.update_status(f"❌ Statistiken-Fehler: {str(e)}")
    
    def open_template_dialog(self):
        """Öffnet den Template-Dialog."""
        try:
            # Template-Dialog öffnen
            template_dialog = TemplateDialog(self.root, self.template_manager)
            self.update_status("📋 Marker-Templates geöffnet")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen der Templates: {str(e)}")
            self.update_status(f"❌ Template-Fehler: {str(e)}")
    
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