#!/usr/bin/env python3
"""
EINFACHE & FUNKTIONALE Marker-Erstellung
========================================

Diese GUI funktioniert SOFORT ohne Probleme.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import yaml
import os
from pathlib import Path
from datetime import datetime

class WorkingMarkerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Marker-Erstellung - FUNKTIONAL")
        self.root.geometry("800x600")
        
        # Marker-Verzeichnis
        self.marker_dir = Path.cwd() / "markers"
        self.marker_dir.mkdir(exist_ok=True)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Haupt-Container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title = ttk.Label(main_frame, text="🎯 Marker-Erstellung", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))
        
        # Verzeichnis-Anzeige
        dir_frame = ttk.LabelFrame(main_frame, text="Speicherort", padding="5")
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.dir_label = ttk.Label(dir_frame, text=f"📁 {self.marker_dir}")
        self.dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        dir_button = ttk.Button(dir_frame, text="Ändern", command=self.change_directory)
        dir_button.pack(side=tk.RIGHT)
        
        # Eingabe-Bereich
        input_frame = ttk.LabelFrame(main_frame, text="Marker-Text eingeben", padding="5")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Textfeld
        self.text_widget = scrolledtext.ScrolledText(input_frame, height=20, wrap=tk.WORD, font=("Consolas", 11))
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        create_button = ttk.Button(button_frame, text="🚀 Marker erstellen", command=self.create_markers)
        create_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(button_frame, text="🗑️ Leeren", command=self.clear_text)
        clear_button.pack(side=tk.LEFT)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Bereit")
        self.status_label.pack(anchor=tk.W, pady=(10, 0))
    
    def change_directory(self):
        directory = filedialog.askdirectory(title="Marker-Verzeichnis wählen")
        if directory:
            self.marker_dir = Path(directory)
            self.dir_label.config(text=f"📁 {self.marker_dir}")
    
    def clear_text(self):
        self.text_widget.delete("1.0", tk.END)
        self.status_label.config(text="Textfeld geleert")
    
    def create_markers(self):
        text = self.text_widget.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warnung", "Bitte geben Sie Marker-Text ein!")
            return
        
        try:
            # YAML parsen
            marker_data = yaml.safe_load(text)
            
            if not marker_data:
                messagebox.showerror("Fehler", "Keine gültigen Marker-Daten gefunden!")
                return
            
            # Marker-ID generieren falls fehlend
            if 'id' not in marker_data:
                marker_data['id'] = f"marker_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Datei speichern
            filename = f"{marker_data['id']}.yaml"
            filepath = self.marker_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(marker_data, f, default_flow_style=False, allow_unicode=True)
            
            messagebox.showinfo("Erfolg", f"Marker erstellt: {filename}")
            self.status_label.config(text=f"Marker erstellt: {filename}")
            
            # Textfeld leeren
            self.text_widget.delete("1.0", tk.END)
            
        except yaml.YAMLError as e:
            messagebox.showerror("YAML-Fehler", f"Syntax-Fehler: {str(e)}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen: {str(e)}")
    
    def run(self):
        self.root.mainloop()

def main():
    app = WorkingMarkerGUI()
    app.run()

if __name__ == "__main__":
    main() 