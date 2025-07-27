#!/usr/bin/env python3
"""
Einfache Marker-Erstellungs-GUI
===============================

Eine funktionierende GUI zum Erstellen von Markern mit:
- Copy-Paste-Funktionalität
- Sofortige Verarbeitung
- Fehlerbehandlung ohne störende Meldungen
- "Alle Marker erstellen" Button
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import sys
import os
from pathlib import Path
import yaml
import re
from datetime import datetime

class SimpleMarkerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Marker-Erstellung - Einfach & Funktional")
        self.root.geometry("1000x700")
        
        # Marker-Verzeichnis
        self.marker_dir = None
        self.setup_ui()
        self.select_marker_directory()
    
    def setup_ui(self):
        """Erstellt die Benutzeroberfläche."""
        # Haupt-Container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title_label = ttk.Label(main_frame, text="🎯 Marker-Erstellung", 
                               font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Verzeichnis-Anzeige
        self.dir_frame = ttk.LabelFrame(main_frame, text="Marker-Verzeichnis", padding="5")
        self.dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.dir_label = ttk.Label(self.dir_frame, text="Kein Verzeichnis ausgewählt")
        self.dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        dir_button = ttk.Button(self.dir_frame, text="Verzeichnis ändern", 
                               command=self.select_marker_directory)
        dir_button.pack(side=tk.RIGHT)
        
        # Eingabe-Bereich
        input_frame = ttk.LabelFrame(main_frame, text="Marker-Text eingeben", padding="5")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Anleitung
        instruction_text = """📝 Anleitung:
• Fügen Sie hier einen oder mehrere YAML-Marker ein
• Trennen Sie mehrere Marker durch '---' 
• Sie können Text kopieren und einfügen (Ctrl+V)
• Fehler werden automatisch behoben"""
        
        instruction_label = ttk.Label(input_frame, text=instruction_text, 
                                     font=("Helvetica", 10), foreground="blue")
        instruction_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Textfeld für Marker-Eingabe
        self.marker_text = scrolledtext.ScrolledText(input_frame, height=20, 
                                                    wrap=tk.WORD, font=("Consolas", 11),
                                                    state=tk.NORMAL)  # Explizit normal setzen
        self.marker_text.pack(fill=tk.BOTH, expand=True)
        
        # Fokus auf Textfeld setzen
        self.marker_text.focus_set()
        
        # Test-Text einfügen um zu zeigen dass es funktioniert
        self.marker_text.insert("1.0", "# Hier können Sie Marker-Text eingeben\n# Beispiel:\nid: A_test_marker\nlevel: 1\ndescription: Test-Marker\n\n")
        
        # Button-Bereich
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Alle Marker erstellen Button
        self.create_button = ttk.Button(button_frame, text="🚀 Alle Marker erstellen", 
                                       command=self.create_all_markers, 
                                       style="Accent.TButton")
        self.create_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Textfeld leeren
        clear_button = ttk.Button(button_frame, text="🗑️ Textfeld leeren", 
                                 command=self.clear_text)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Demo-Marker laden
        demo_button = ttk.Button(button_frame, text="📋 Demo-Marker laden", 
                                command=self.load_demo_markers)
        demo_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Test-Eingabe
        test_button = ttk.Button(button_frame, text="🧪 Test Eingabe", 
                                command=self.test_input)
        test_button.pack(side=tk.LEFT)
        
        # Status-Bereich
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Bereit für Marker-Erstellung")
        self.status_label.pack(anchor=tk.W)
        
        # Fehler-Bereich (ausgeblendet)
        self.error_frame = ttk.LabelFrame(main_frame, text="⚠️ Fehler", padding="5")
        self.error_text = scrolledtext.ScrolledText(self.error_frame, height=6, 
                                                   wrap=tk.WORD, font=("Consolas", 10))
        self.error_text.pack(fill=tk.BOTH, expand=True)
        
        # Keyboard-Shortcuts
        self.root.bind('<Control-v>', self.paste_text)
        self.root.bind('<Control-a>', self.select_all)
    
    def select_marker_directory(self):
        """Wählt das Marker-Verzeichnis aus."""
        directory = filedialog.askdirectory(
            title="Wählen Sie Ihr Marker-Verzeichnis",
            initialdir=str(Path.cwd())
        )
        
        if directory:
            self.marker_dir = Path(directory)
            self.dir_label.config(text=f"📁 {self.marker_dir}")
            self.update_status("Verzeichnis ausgewählt - Bereit für Marker-Erstellung")
        else:
            # Standard-Verzeichnis verwenden
            self.marker_dir = Path.cwd() / "markers"
            self.marker_dir.mkdir(exist_ok=True)
            self.dir_label.config(text=f"📁 {self.marker_dir} (Standard)")
            self.update_status("Standard-Verzeichnis verwendet")
    
    def paste_text(self, event=None):
        """Behandelt Paste-Operationen."""
        try:
            # Text aus Clipboard holen
            clipboard_text = self.root.clipboard_get()
            self.marker_text.insert(tk.INSERT, clipboard_text)
            self.update_status("Text eingefügt")
        except:
            pass
        return "break"
    
    def select_all(self, event=None):
        """Wählt den gesamten Text aus."""
        self.marker_text.tag_add(tk.SEL, "1.0", tk.END)
        return "break"
    
    def clear_text(self):
        """Leert das Textfeld."""
        self.marker_text.delete("1.0", tk.END)
        self.hide_errors()
        self.update_status("Textfeld geleert")
    
    def test_input(self):
        """Testet ob das Eingabefeld funktioniert."""
        current_text = self.marker_text.get("1.0", tk.END).strip()
        if current_text:
            messagebox.showinfo("Test", f"✅ Textfeld funktioniert!\n\nEingabe:\n{current_text[:200]}...")
            self.update_status("Textfeld-Test erfolgreich")
        else:
            messagebox.showwarning("Test", "❌ Kein Text im Textfeld gefunden")
            self.update_status("Textfeld-Test fehlgeschlagen")
    
    def load_demo_markers(self):
        """Lädt Demo-Marker."""
        demo_text = """id: A_demo_marker
level: 1
description: Ein Demo-Marker für Tests
version: 1.0.0
status: draft
author: demo_user
---
id: S_another_marker
level: 2
description: Ein weiterer Demo-Marker
version: 1.0.0
status: draft
author: demo_user"""
        
        self.marker_text.delete("1.0", tk.END)
        self.marker_text.insert("1.0", demo_text)
        self.update_status("Demo-Marker geladen")
    
    def parse_markers(self, text):
        """Parst den Text in einzelne Marker."""
        # Marker durch '---' trennen
        blocks = re.split(r'^\s*---\s*$', text, flags=re.MULTILINE)
        markers = []
        errors = []
        
        for i, block in enumerate(blocks):
            block = block.strip()
            if not block:
                continue
            
            try:
                # YAML parsen
                marker_data = yaml.safe_load(block)
                if marker_data:
                    markers.append({
                        'data': marker_data,
                        'original_text': block,
                        'block_number': i + 1
                    })
            except yaml.YAMLError as e:
                errors.append({
                    'block_number': i + 1,
                    'error': str(e),
                    'text': block[:100] + "..." if len(block) > 100 else block
                })
        
        return markers, errors
    
    def repair_marker(self, marker_data):
        """Repariert häufige Marker-Fehler."""
        repaired = marker_data.copy()
        
        # Häufige Feld-Fehler korrigieren
        field_fixes = {
            'beschreibg': 'description',
            'descr': 'description',
            'kategorie': 'category',
            'level': 'level',
            'id': 'id'
        }
        
        for wrong, correct in field_fixes.items():
            if wrong in repaired and correct not in repaired:
                repaired[correct] = repaired.pop(wrong)
        
        # Standardwerte hinzufügen
        defaults = {
            'version': '1.0.0',
            'status': 'draft',
            'author': 'auto_created'
        }
        
        for key, value in defaults.items():
            if key not in repaired:
                repaired[key] = value
        
        return repaired
    
    def create_all_markers(self):
        """Erstellt alle Marker."""
        if not self.marker_dir:
            messagebox.showerror("Fehler", "Bitte wählen Sie zuerst ein Marker-Verzeichnis aus!")
            return
        
        text = self.marker_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warnung", "Bitte geben Sie Marker-Text ein!")
            return
        
        self.update_status("Verarbeite Marker...")
        self.root.update()
        
        # Marker parsen
        markers, errors = self.parse_markers(text)
        
        if not markers and not errors:
            messagebox.showinfo("Info", "Keine Marker gefunden!")
            return
        
        # Fehler anzeigen (falls vorhanden)
        if errors:
            self.show_errors(errors)
        
        # Marker erstellen
        created_count = 0
        failed_count = 0
        
        for marker_info in markers:
            try:
                # Marker reparieren
                marker_data = self.repair_marker(marker_info['data'])
                
                # Marker-ID generieren falls fehlend
                if 'id' not in marker_data:
                    # Intelligente ID aus Beschreibung generieren
                    if 'description' in marker_data:
                        desc = marker_data['description']
                        words = desc.split()[:3]
                        if words:
                            id_base = ''.join(c for c in ' '.join(words) if c.isalnum() or c.isspace()).strip()
                            id_base = id_base.replace(' ', '_').upper()
                            if len(id_base) > 15:
                                id_base = id_base[:15]
                            marker_data['id'] = id_base
                        else:
                            marker_data['id'] = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{created_count}"
                    else:
                        marker_data['id'] = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{created_count}"
                
                # Datei speichern
                filename = f"{marker_data['id']}.yaml"
                filepath = self.marker_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    yaml.dump(marker_data, f, default_flow_style=False, 
                             allow_unicode=True, sort_keys=False)
                
                created_count += 1
                
            except Exception as e:
                failed_count += 1
                print(f"Fehler beim Erstellen von Marker {marker_info['block_number']}: {e}")
        
        # Ergebnis anzeigen
        if created_count > 0:
            message = f"✅ {created_count} Marker erfolgreich erstellt!"
            if failed_count > 0:
                message += f"\n❌ {failed_count} Marker fehlgeschlagen"
            if errors:
                message += f"\n⚠️ {len(errors)} Blöcke mit Syntax-Fehlern"
            
            messagebox.showinfo("Erfolg", message)
            self.update_status(f"{created_count} Marker erstellt")
            
            # Textfeld leeren nach erfolgreicher Erstellung
            self.marker_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Fehler", "Keine Marker konnten erstellt werden!")
            self.update_status("Marker-Erstellung fehlgeschlagen")
    
    def show_errors(self, errors):
        """Zeigt Fehler an."""
        error_text = "Syntax-Fehler gefunden:\n\n"
        for error in errors:
            error_text += f"Block {error['block_number']}:\n"
            error_text += f"Fehler: {error['error']}\n"
            error_text += f"Text: {error['text']}\n"
            error_text += "-" * 50 + "\n"
        
        self.error_text.delete("1.0", tk.END)
        self.error_text.insert("1.0", error_text)
        self.error_frame.pack(fill=tk.X, pady=(10, 0))
    
    def hide_errors(self):
        """Versteckt den Fehler-Bereich."""
        self.error_frame.pack_forget()
    
    def update_status(self, message):
        """Aktualisiert die Status-Anzeige."""
        self.status_label.config(text=f"📊 {message}")
        self.root.update()

def main():
    """Hauptfunktion."""
    root = tk.Tk()
    
    # Style konfigurieren
    style = ttk.Style()
    style.theme_use('clam')
    
    # Accent-Button-Style
    style.configure("Accent.TButton", 
                   background="#0078d4", 
                   foreground="white",
                   font=("Helvetica", 11, "bold"))
    
    app = SimpleMarkerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 