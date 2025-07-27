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
- Marker bearbeiten und speichern
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import yaml
import os
import re
from pathlib import Path
from datetime import datetime
import uuid

class SmartMarkerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Smart Marker-Erstellung - Einfach & Benutzerfreundlich")
        self.root.geometry("1400x900")
        
        # Responsive Design: Minimum-Größe setzen
        self.root.minsize(1000, 700)
        
        # Marker-Verzeichnis
        self.marker_dir = Path.cwd() / "markers"
        self.marker_dir.mkdir(exist_ok=True)
        
        # Ausgewählter Marker für Beispiele
        self.selected_marker = None
        self.editing_marker = None
        
        # Status-Tracking
        self.status_var = tk.StringVar(value="✅ System bereit")
        
        # Setup UI mit verbesserter Fehlerbehandlung
        try:
            self.setup_ui()
            self.refresh_marker_list()
            self.update_status("✅ GUI erfolgreich geladen")
        except Exception as e:
            messagebox.showerror("Initialisierungsfehler", f"Fehler beim Laden der GUI: {str(e)}")
            self.root.destroy()
            raise
    
    def setup_ui(self):
        """Setup der UI mit verbesserter Fehlerbehandlung und Responsive Design"""
        try:
            # Haupt-Container mit PanedWindow für Aufteilung
            paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
            paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Linke Seite - Eingabe
            left_frame = ttk.Frame(paned_window)
            paned_window.add(left_frame, weight=2)
            
            # Rechte Seite - Übersicht
            right_frame = ttk.Frame(paned_window)
            paned_window.add(right_frame, weight=1)
            
            # Responsive Design: Bind resize events
            self.root.bind('<Configure>', self.on_resize)
            
            self.setup_input_section(left_frame)
            self.setup_overview_section(right_frame)
            
        except Exception as e:
            print(f"❌ Fehler beim Setup der UI: {str(e)}")
            raise
    
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
        
        # Text-Widget mit Scrollbar
        text_frame = ttk.Frame(input_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = scrolledtext.ScrolledText(text_frame, height=15, wrap=tk.WORD,
                                                   font=("Consolas", 10))
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Button-Frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Buttons
        ttk.Button(button_frame, text="🗑️ Löschen", command=self.clear_text).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="📋 Demo laden", command=self.load_demo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="🎯 Marker erstellen", command=self.create_markers,
                  style="Accent.TButton").pack(side=tk.RIGHT)
        
        # Status-Bar
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                     font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT)
    
    def setup_overview_section(self, parent):
        # Titel
        title = ttk.Label(parent, text="📋 Marker-Übersicht", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=(0, 10))
        
        # Button-Frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="🔄 Aktualisieren", command=self.refresh_marker_list).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="📝 Beispiele", command=self.add_examples).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="✏️ Bearbeiten", command=self.edit_marker).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="💾 Speichern", command=self.save_edited_marker).pack(side=tk.LEFT)
        
        # Marker-Liste
        list_frame = ttk.LabelFrame(parent, text="📁 Verfügbare Marker", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview für Marker
        columns = ("ID", "Level", "Kategorie", "Beschreibung")
        self.marker_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        
        # Spalten konfigurieren
        for col in columns:
            self.marker_tree.heading(col, text=col)
            self.marker_tree.column(col, width=100)
        
        # Scrollbar für Treeview
        tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.marker_tree.yview)
        self.marker_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.marker_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Marker-Auswahl Event
        self.marker_tree.bind("<<TreeviewSelect>>", self.on_marker_select)
        
        # Details-Bereich
        details_frame = ttk.LabelFrame(parent, text="📄 Marker-Details", padding="5")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        self.details_text = scrolledtext.ScrolledText(details_frame, height=10, wrap=tk.WORD,
                                                    font=("Consolas", 9))
        self.details_text.pack(fill=tk.BOTH, expand=True)
    
    def change_directory(self):
        """Ändert das Marker-Verzeichnis"""
        new_dir = filedialog.askdirectory(title="Marker-Verzeichnis wählen",
                                        initialdir=str(self.marker_dir))
        if new_dir:
            self.marker_dir = Path(new_dir)
            self.marker_dir.mkdir(exist_ok=True)
            self.dir_label.config(text=str(self.marker_dir))
            self.refresh_marker_list()
            self.update_status(f"Verzeichnis geändert: {self.marker_dir}")
    
    def clear_text(self):
        """Löscht den Eingabe-Text"""
        self.text_widget.delete("1.0", tk.END)
        self.update_status("Text gelöscht")
    
    def load_demo(self):
        """Lädt Demo-Marker"""
        demo_text = """SEXUAL_TENSION
Level: 3
Kategorie: romance
Beschreibung: Marker für sexuelle Spannung zwischen Charakteren
Beispiele:
- "Ihre Augen trafen sich über den Tisch hinweg"
- "Die Spannung war greifbar zwischen ihnen"
- "Ein elektrischer Moment der Anziehung"

FLIRTING
Level: 2
Kategorie: romance
Beschreibung: Spielerisches Flirten und Annäherung
Beispiele:
- "Er warf ihr einen verführerischen Blick zu"
- "Sie neckte ihn mit einem süßen Lächeln"
- "Die Chemie zwischen ihnen war unübersehbar"

CONFLICT
Level: 4
Kategorie: drama
Beschreibung: Konflikte und Spannungen zwischen Charakteren
Beispiele:
- "Ihre Stimmen wurden lauter"
- "Die Atmosphäre war angespannt"
- "Ein Streit bahnte sich an"
"""
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", demo_text)
        self.update_status("Demo-Marker geladen")
    
    def hide_errors(self):
        """Versteckt Fehlermeldungen"""
        self.error_label.pack_forget()
    
    def show_errors(self, message):
        """Zeigt Fehlermeldungen an"""
        self.error_label.config(text=message)
        self.error_label.pack()
    
    def update_status(self, message):
        """Aktualisiert den Status mit verbesserter Fehlerbehandlung"""
        try:
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"✅ {message}")
            if hasattr(self, 'status_var'):
                self.status_var.set(f"✅ {message}")
            print(f"📊 Status: {message}")
        except Exception as e:
            print(f"❌ Fehler beim Status-Update: {str(e)}")
    
    def on_resize(self, event):
        """Behandelt Resize-Events für Responsive Design"""
        try:
            if hasattr(self, '_last_size'):
                if abs(event.width - self._last_size[0]) < 10 and abs(event.height - self._last_size[1]) < 10:
                    return
            self._last_size = (event.width, event.height)
            print(f"🔄 Resize: {event.width}x{event.height}")
        except Exception as e:
            print(f"❌ Fehler beim Resize: {str(e)}")
    
    def refresh_marker_list(self):
        """Aktualisiert die Marker-Liste mit verbesserter ID-Anzeige"""
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
                        # ID korrekt anzeigen
                        marker_id = marker_data.get('id', 'Unbekannt')
                        if marker_id == 'Unbekannt':
                            # Versuche ID aus Dateinamen zu extrahieren
                            marker_id = yaml_file.stem
                        
                        self.marker_tree.insert("", "end", values=(
                            marker_id,
                            marker_data.get('level', '?'),
                            marker_data.get('category', 'general'),
                            marker_data.get('description', 'Keine Beschreibung')[:50] + "..."
                        ))
                except Exception as e:
                    print(f"Fehler beim Laden von {yaml_file}: {e}")
                    # Zeige Datei auch bei Fehler an
                    self.marker_tree.insert("", "end", values=(
                        yaml_file.stem,
                        '?',
                        'error',
                        f'Fehler beim Laden: {str(e)[:30]}...'
                    ))
        
        self.update_status(f"{len(self.marker_tree.get_children())} Marker geladen")
    
    def on_marker_select(self, event):
        """Wird aufgerufen wenn ein Marker ausgewählt wird"""
        selection = self.marker_tree.selection()
        if selection:
            item = self.marker_tree.item(selection[0])
            marker_id = item['values'][0]
            self.show_marker_details(marker_id)
            self.selected_marker = marker_id
            self.editing_marker = None  # Bearbeitung zurücksetzen
    
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
    
    def edit_marker(self):
        """Aktiviert Bearbeitung des ausgewählten Markers"""
        if not self.selected_marker:
            messagebox.showinfo("Info", "Bitte wählen Sie zuerst einen Marker aus!")
            return
        
        marker_file = self.marker_dir / f"{self.selected_marker}.yaml"
        if marker_file.exists():
            try:
                with open(marker_file, 'r', encoding='utf-8') as f:
                    self.editing_marker = yaml.safe_load(f)
                
                # YAML in Text-Widget laden
                yaml_content = yaml.dump(self.editing_marker, default_flow_style=False, 
                                       allow_unicode=True, sort_keys=False)
                
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert("1.0", yaml_content)
                
                self.update_status(f"Marker '{self.selected_marker}' zum Bearbeiten geladen")
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden des Markers: {str(e)}")
        else:
            messagebox.showerror("Fehler", f"Marker-Datei nicht gefunden: {marker_file}")
    
    def save_edited_marker(self):
        """Speichert den bearbeiteten Marker"""
        if not self.editing_marker or not self.selected_marker:
            messagebox.showinfo("Info", "Kein Marker zum Speichern ausgewählt!")
            return
        
        try:
            # YAML aus Text-Widget parsen
            yaml_text = self.text_widget.get("1.0", tk.END).strip()
            updated_marker = yaml.safe_load(yaml_text)
            
            if not updated_marker:
                messagebox.showerror("Fehler", "Ungültiges YAML-Format!")
                return
            
            # ID beibehalten
            updated_marker['id'] = self.selected_marker
            
            # Datei speichern
            marker_file = self.marker_dir / f"{self.selected_marker}.yaml"
            with open(marker_file, 'w', encoding='utf-8') as f:
                yaml.dump(updated_marker, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
            
            # UI aktualisieren
            self.refresh_marker_list()
            self.show_marker_details(self.selected_marker)
            self.editing_marker = None
            
            self.update_status(f"Marker '{self.selected_marker}' erfolgreich gespeichert")
            messagebox.showinfo("Erfolg", f"Marker '{self.selected_marker}' wurde gespeichert!")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")
    
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
                    yaml.dump(marker_data, f, default_flow_style=False, 
                             allow_unicode=True, sort_keys=False)
                
                # UI aktualisieren
                self.refresh_marker_list()
                self.show_marker_details(self.selected_marker)
                
                dialog.destroy()
                self.update_status(f"{len(new_examples)} Beispiele für '{self.selected_marker}' gespeichert")
                messagebox.showinfo("Erfolg", f"{len(new_examples)} Beispiele gespeichert!")
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="❌ Abbrechen", command=dialog.destroy).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="💾 Speichern", command=save_examples).pack(side=tk.RIGHT)
    
    def smart_parse_text(self, text):
        """Intelligente Text-Parsing mit verbesserter ID-Generierung"""
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
        
        # Verbesserte ID-Generierung falls keine gefunden
        if 'id' not in marker_data:
            # Versuche ID aus erstem Wort zu extrahieren
            first_line = lines[0].strip().upper()
            if first_line and len(first_line) > 3 and not ':' in first_line:
                marker_data['id'] = first_line
            else:
                # Generiere eindeutige ID
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_id = str(uuid.uuid4())[:8]
                marker_data['id'] = f"MARKER_{timestamp}_{unique_id}"
        
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
        """Erstellt Marker mit verbesserter Fehlerbehandlung und Validierung"""
        text = self.text_widget.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showinfo("Info", "Bitte geben Sie Text ein!")
            return
        
        try:
            # Verzeichnis-Validierung
            if not self.marker_dir.exists():
                try:
                    self.marker_dir.mkdir(parents=True, exist_ok=True)
                    print(f"✅ Verzeichnis erstellt: {self.marker_dir}")
                except PermissionError:
                    error_msg = f"Keine Berechtigung zum Erstellen des Verzeichnisses: {self.marker_dir}"
                    messagebox.showerror("Berechtigungsfehler", error_msg)
                    return
                except Exception as e:
                    error_msg = f"Fehler beim Erstellen des Verzeichnisses: {str(e)}"
                    messagebox.showerror("Verzeichnisfehler", error_msg)
                    return
            
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
            
            if not blocks:
                messagebox.showwarning("Warnung", "Keine gültigen Marker-Blöcke gefunden!")
                return
            
            created_markers = []
            failed_markers = []
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
                    
                    # Datei speichern mit verbesserter Fehlerbehandlung
                    filename = f"{marker_data['id']}.yaml"
                    filepath = self.marker_dir / filename
                    
                    # YAML formatieren
                    yaml_content = yaml.dump(marker_data, default_flow_style=False, 
                                           allow_unicode=True, sort_keys=False)
                    
                    # Datei schreiben mit Fehlerbehandlung
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(yaml_content)
                        created_markers.append(marker_data['id'])
                        print(f"✅ Marker gespeichert: {filename}")
                    except PermissionError:
                        error_msg = f"Keine Berechtigung zum Speichern: {filename}"
                        failed_markers.append(f"Block {i+1}: {error_msg}")
                        print(f"❌ Berechtigungsfehler: {filename}")
                    except Exception as e:
                        error_msg = f"Fehler beim Speichern: {str(e)}"
                        failed_markers.append(f"Block {i+1}: {error_msg}")
                        print(f"❌ Speicherfehler: {filename} - {str(e)}")
                    
                except Exception as e:
                    error_msg = f"Fehler beim Verarbeiten von Block {i+1}: {str(e)}"
                    failed_markers.append(error_msg)
                    print(f"❌ Verarbeitungsfehler Block {i+1}: {str(e)}")
            
            # Detaillierte Erfolgsmeldung
            if created_markers:
                success_message = f"""✅ {len(created_markers)} Marker erfolgreich erstellt!

📁 Erstellte Marker:
{chr(10).join([f"  • {marker_id}" for marker_id in created_markers])}

💾 Speicherort: {self.marker_dir}"""
                
                if failed_markers:
                    success_message += f"""

⚠️ Fehlgeschlagene Marker ({len(failed_markers)}):
{chr(10).join([f"  • {error}" for error in failed_markers])}"""
                
                messagebox.showinfo("Erfolg", success_message)
                self.update_status(f"{len(created_markers)} Marker erstellt")
                
                # UI aktualisieren
                self.refresh_marker_list()
                self.clear_text()
                
            else:
                error_message = f"""❌ Keine Marker erstellt!

Fehler:
{chr(10).join([f"  • {error}" for error in failed_markers])}"""
                
                messagebox.showerror("Fehler", error_message)
                self.update_status("Marker-Erstellung fehlgeschlagen")
                
        except Exception as e:
            error_msg = f"Unerwarteter Fehler: {str(e)}"
            messagebox.showerror("Systemfehler", error_msg)
            print(f"❌ Systemfehler: {str(e)}")
            self.update_status("Systemfehler aufgetreten")
    
    def run(self):
        """Startet die GUI"""
        self.root.mainloop()

def main():
    app = SmartMarkerGUI()
    app.run()

if __name__ == "__main__":
    main() 