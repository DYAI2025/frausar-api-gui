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

class SmartMarkerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Smart Marker-Erstellung - Einfach & Benutzerfreundlich")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
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

A_ISOLATION_MARKER
Level: 1
Beschreibung: Marker für Isolation-Erkennung
Kategorie: system

---

A_LOVE_SCANMARKER
Level: 2
Beschreibung: Marker für Liebes-Scanning
Kategorie: emotion"""

        self.text_widget.insert(tk.END, example_text)
        
        # Button-Bereich
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="🚀 Marker erstellen", 
                  command=self.create_markers).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="🗑️ Löschen", 
                  command=self.clear_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 Demo laden", 
                  command=self.load_demo).pack(side=tk.LEFT, padx=5)
        
        # Test-Ergebnisse
        test_frame = ttk.LabelFrame(parent, text="🧪 Test-Ergebnisse", padding="10")
        test_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.test_text = scrolledtext.ScrolledText(test_frame, height=8, wrap=tk.WORD)
        self.test_text.pack(fill=tk.BOTH, expand=True)
        
        test_button_frame = ttk.Frame(test_frame)
        test_button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(test_button_frame, text="🧪 Tests ausführen", 
                  command=self.run_tests).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(test_button_frame, text="🗑️ Tests löschen", 
                  command=lambda: self.test_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        ttk.Button(test_button_frame, text="📁 GPT YAML erstellen", 
                  command=self.create_gpt_yaml).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = ttk.Label(parent, text="Bereit", font=("Arial", 10))
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
        columns = ("Name", "ID", "Level", "Kategorie")
        self.marker_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Spalten konfigurieren
        self.marker_tree.heading("Name", text="Name")
        self.marker_tree.heading("ID", text="ID")
        self.marker_tree.heading("Level", text="Level")
        self.marker_tree.heading("Kategorie", text="Kategorie")
        
        self.marker_tree.column("Name", width=150)
        self.marker_tree.column("ID", width=100)
        self.marker_tree.column("Level", width=50)
        self.marker_tree.column("Kategorie", width=80)
        
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
    
    def clear_text(self):
        self.text_widget.delete(1.0, tk.END)
        self.update_status("Text gelöscht")
    
    def load_demo(self):
        demo_text = """A_ISOLATION_MARKER
Level: 1
Beschreibung: Marker für Isolation-Erkennung
Kategorie: system

---

A_LOVE_SCANMARKER
Level: 2
Beschreibung: Marker für Liebes-Scanning
Kategorie: emotion

---

A_SEXUAL_TENSION
Level: 3
Beschreibung: Marker für sexuelle Spannung
Kategorie: relationship"""
        
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, demo_text)
        self.update_status("Demo geladen")
    
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
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    
                    if data:
                        # Name aus name-Feld oder intelligent aus ID generieren
                        name = data.get('name', '')
                        if not name and 'id' in data:
                            name = data['id'].replace('_', ' ').title()
                        
                        # ID aus id-Feld oder Dateiname
                        marker_id = data.get('id', file_path.stem)
                        
                        # Level und Kategorie
                        level = data.get('level', '')
                        kategorie = data.get('kategorie', data.get('category', ''))
                        
                        self.marker_tree.insert("", tk.END, values=(name, marker_id, level, kategorie))
                        
                except Exception as e:
                    # Fehlerhafte Datei anzeigen
                    self.marker_tree.insert("", tk.END, values=(f"Fehler: {file_path.stem}", file_path.stem, "", ""))
        
        self.update_status(f"{len(self.marker_tree.get_children())} Marker geladen")
    
    def on_marker_select(self, event):
        selection = self.marker_tree.selection()
        if selection:
            item = self.marker_tree.item(selection[0])
            marker_id = item['values'][1]  # ID ist in der zweiten Spalte
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
        
        item = self.marker_tree.item(selection[0])
        marker_id = item['values'][1]
        
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
        
        item = self.marker_tree.item(selection[0])
        marker_id = item['values'][1]
        
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
        marker_id = item['values'][1]
        
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
    
    def run_tests(self):
        self.test_text.delete(1.0, tk.END)
        self.test_text.insert(tk.END, "🧪 Führe Tests aus...\n\n")
        
        results = []
        
        # Test 1: Verzeichnis-Zugriff
        try:
            if self.marker_dir.exists():
                results.append("✅ Verzeichnis-Zugriff: OK")
            else:
                results.append("❌ Verzeichnis-Zugriff: Fehlgeschlagen")
        except Exception as e:
            results.append(f"❌ Verzeichnis-Zugriff: {e}")
        
        # Test 2: YAML-Validierung
        try:
            text = self.text_widget.get(1.0, tk.END).strip()
            if text:
                yaml.safe_load(text)
                results.append("✅ YAML-Validierung: OK")
            else:
                results.append("⚠️ YAML-Validierung: Kein Text zum Testen")
        except Exception as e:
            results.append(f"❌ YAML-Validierung: {e}")
        
        # Test 3: Marker-Struktur
        try:
            text = self.text_widget.get(1.0, tk.END).strip()
            if text:
                data = yaml.safe_load(text)
                if data and isinstance(data, dict):
                    if 'id' in data or 'name' in data:
                        results.append("✅ Marker-Struktur: OK")
                    else:
                        results.append("⚠️ Marker-Struktur: Keine ID/Name gefunden")
                else:
                    results.append("❌ Marker-Struktur: Ungültige Struktur")
            else:
                results.append("⚠️ Marker-Struktur: Kein Text zum Testen")
        except Exception as e:
            results.append(f"❌ Marker-Struktur: {e}")
        
        # Test 4: Performance
        try:
            marker_count = len(self.marker_tree.get_children())
            if marker_count < 100:
                results.append("✅ Performance: OK")
            elif marker_count < 1000:
                results.append("⚠️ Performance: Viele Marker ({marker_count})")
            else:
                results.append("❌ Performance: Zu viele Marker ({marker_count})")
        except Exception as e:
            results.append(f"❌ Performance: {e}")
        
        # Ergebnisse anzeigen
        for result in results:
            self.test_text.insert(tk.END, f"{result}\n")
        
        self.test_text.insert(tk.END, "\n🎯 Tests abgeschlossen!")
        self.update_status("Tests ausgeführt")
    
    def create_gpt_yaml(self):
        output_dir = filedialog.askdirectory(title="Ausgabe-Verzeichnis für GPT-YAML wählen")
        if not output_dir:
            return
        
        try:
            # Alle Marker sammeln
            markers = []
            for item in self.marker_tree.get_children():
                values = self.marker_tree.item(item)['values']
                marker_id = values[1]
                marker_name = values[0]
                
                marker_file = self.marker_dir / f"{marker_id}.yaml"
                if marker_file.exists():
                    with open(marker_file, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data:
                            data['name'] = marker_name
                            markers.append(data)
            
            if not markers:
                messagebox.showwarning("Warnung", "Keine Marker zum Exportieren gefunden.")
                return
            
            # GPT-YAML erstellen
            gpt_data = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'total_markers': len(markers),
                    'source_directory': str(self.marker_dir)
                },
                'markers': markers
            }
            
            # Datei speichern
            output_file = Path(output_dir) / f"gpt_markers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml.dump(gpt_data, f, default_flow_style=False, allow_unicode=True)
            
            messagebox.showinfo("Erfolg", f"GPT-YAML erfolgreich erstellt:\n{output_file}")
            self.update_status(f"GPT-YAML erstellt: {len(markers)} Marker")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen der GPT-YAML: {e}")
    
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
        text = self.text_widget.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warnung", "Bitte gib Text ein!")
            return
        
        # Marker mit '---' oder '###' trennen
        marker_blocks = re.split(r'\n\s*---\s*\n|\n\s*###\s*\n', text)
        marker_blocks = [block.strip() for block in marker_blocks if block.strip()]
        
        created_markers = []
        errors = []
        
        for i, block in enumerate(marker_blocks):
            try:
                data = self.smart_parse_text(block)
                if data:
                    # Datei speichern
                    filename = f"{data['id']}.yaml"
                    filepath = self.marker_dir / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
                    
                    created_markers.append({
                        'name': data.get('name', data['id']),
                        'id': data['id'],
                        'filename': filename
                    })
                    
            except Exception as e:
                errors.append(f"Block {i+1}: {e}")
        
        # Ergebnisse anzeigen
        if created_markers:
            success_msg = f"Marker erfolgreich erstellt!\n\n📁 Erstellte Marker:\n"
            for marker in created_markers:
                success_msg += f"• {marker['name']} ({marker['filename']})\n"
            
            if errors:
                success_msg += f"\n⚠️ Fehler:\n"
                for error in errors:
                    success_msg += f"• {error}\n"
            
            messagebox.showinfo("Erfolg", success_msg)
            self.update_status(f"{len(created_markers)} Marker erstellt")
            self.refresh_marker_list()
        else:
            error_msg = "Keine Marker erstellt!\n\nFehler:\n"
            for error in errors:
                error_msg += f"• {error}\n"
            messagebox.showerror("Fehler", error_msg)
    
    def run(self):
        self.root.mainloop()

def main():
    app = SmartMarkerGUI()
    app.run()

if __name__ == "__main__":
    main() 