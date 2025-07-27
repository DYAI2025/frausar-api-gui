#!/usr/bin/env python3
"""
GPT-YAML GENERATOR
==================

Exportiert Marker für GPT-Kompatibilität
- Marker-Format-Konvertierung
- Batch-Export-Funktionalität
- Benutzerdefinierte Formatierung
- Validierung vor Export
"""

import yaml
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

class GPTYAMLGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 GPT-YAML Generator - Marker Export für GPTs")
        self.root.geometry("1000x700")
        
        # Marker-Verzeichnis
        self.marker_dir = Path.cwd() / "markers"
        self.export_dir = Path.cwd() / "exports"
        self.export_dir.mkdir(exist_ok=True)
        
        self.setup_ui()
        self.load_markers()
    
    def setup_ui(self):
        # Haupt-Container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title = ttk.Label(main_frame, text="🤖 GPT-YAML Generator", 
                         font=("Arial", 20, "bold"))
        title.pack(pady=(0, 10))
        
        subtitle = ttk.Label(main_frame, text="Exportiert Marker für GPT-Kompatibilität",
                           font=("Arial", 12))
        subtitle.pack(pady=(0, 20))
        
        # Konfigurations-Bereich
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Export-Konfiguration", padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Format-Auswahl
        format_frame = ttk.Frame(config_frame)
        format_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(format_frame, text="Export-Format:", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        
        self.format_var = tk.StringVar(value="yaml")
        format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                   values=["yaml", "json", "txt"], state="readonly", width=10)
        format_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # GPT-Typ-Auswahl
        gpt_frame = ttk.Frame(config_frame)
        gpt_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(gpt_frame, text="GPT-Typ:", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        
        self.gpt_var = tk.StringVar(value="claude")
        gpt_combo = ttk.Combobox(gpt_frame, textvariable=self.gpt_var,
                                values=["claude", "gpt4", "custom"], state="readonly", width=15)
        gpt_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Optionen
        options_frame = ttk.Frame(config_frame)
        options_frame.pack(fill=tk.X)
        
        self.include_metadata = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Metadaten einschließen", 
                       variable=self.include_metadata).pack(side=tk.LEFT)
        
        self.pretty_print = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Pretty Print", 
                       variable=self.pretty_print).pack(side=tk.LEFT, padx=(20, 0))
        
        self.validate_before_export = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Vor Export validieren", 
                       variable=self.validate_before_export).pack(side=tk.LEFT, padx=(20, 0))
        
        # Marker-Auswahl
        selection_frame = ttk.LabelFrame(main_frame, text="📋 Marker-Auswahl", padding="15")
        selection_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Buttons für Marker-Auswahl
        button_frame = ttk.Frame(selection_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="📁 Alle auswählen", 
                  command=self.select_all_markers).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="❌ Alle abwählen", 
                  command=self.deselect_all_markers).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="🔄 Liste aktualisieren", 
                  command=self.load_markers).pack(side=tk.LEFT)
        
        # Marker-Liste
        list_frame = ttk.Frame(selection_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview für Marker
        columns = ("Select", "ID", "Level", "Category", "Description")
        self.marker_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # Spalten konfigurieren
        self.marker_tree.heading("Select", text="✓")
        self.marker_tree.heading("ID", text="Marker ID")
        self.marker_tree.heading("Level", text="Level")
        self.marker_tree.heading("Category", text="Kategorie")
        self.marker_tree.heading("Description", text="Beschreibung")
        
        self.marker_tree.column("Select", width=50, anchor=tk.CENTER)
        self.marker_tree.column("ID", width=150)
        self.marker_tree.column("Level", width=80, anchor=tk.CENTER)
        self.marker_tree.column("Category", width=120)
        self.marker_tree.column("Description", width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.marker_tree.yview)
        self.marker_tree.configure(yscrollcommand=scrollbar.set)
        
        self.marker_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export-Button
        export_frame = ttk.Frame(main_frame)
        export_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(export_frame, text="🚀 Export starten", 
                  command=self.export_markers, style="Accent.TButton").pack(side=tk.RIGHT)
        
        # Status
        self.status_var = tk.StringVar(value="✅ Bereit für Export")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                               font=("Arial", 10, "italic"))
        status_label.pack(anchor=tk.W)
    
    def load_markers(self):
        """Lädt verfügbare Marker"""
        # Liste leeren
        for item in self.marker_tree.get_children():
            self.marker_tree.delete(item)
        
        if not self.marker_dir.exists():
            self.status_var.set("❌ Marker-Verzeichnis nicht gefunden")
            return
        
        marker_count = 0
        for yaml_file in self.marker_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    marker_data = yaml.safe_load(f)
                
                if marker_data:
                    self.marker_tree.insert("", "end", values=(
                        "☐",  # Checkbox
                        marker_data.get('id', 'Unbekannt'),
                        marker_data.get('level', '?'),
                        marker_data.get('category', 'general'),
                        marker_data.get('description', 'Keine Beschreibung')[:50] + "..."
                    ))
                    marker_count += 1
                    
            except Exception as e:
                print(f"Fehler beim Laden von {yaml_file}: {e}")
        
        self.status_var.set(f"✅ {marker_count} Marker geladen")
    
    def select_all_markers(self):
        """Wählt alle Marker aus"""
        for item in self.marker_tree.get_children():
            values = list(self.marker_tree.item(item)['values'])
            values[0] = "☑"
            self.marker_tree.item(item, values=values)
    
    def deselect_all_markers(self):
        """Wählt alle Marker ab"""
        for item in self.marker_tree.get_children():
            values = list(self.marker_tree.item(item)['values'])
            values[0] = "☐"
            self.marker_tree.item(item, values=values)
    
    def get_selected_markers(self) -> List[str]:
        """Gibt IDs der ausgewählten Marker zurück"""
        selected = []
        for item in self.marker_tree.get_children():
            values = self.marker_tree.item(item)['values']
            if values[0] == "☑":
                selected.append(values[1])  # ID ist in Spalte 1
        return selected
    
    def convert_for_gpt(self, marker_data: Dict[str, Any], gpt_type: str) -> Dict[str, Any]:
        """Konvertiert Marker für GPT-Kompatibilität"""
        converted = marker_data.copy()
        
        if gpt_type == "claude":
            # Claude-spezifische Anpassungen
            if 'examples' in converted:
                converted['examples'] = [str(ex) for ex in converted['examples']]
            if 'pattern' in converted:
                converted['pattern'] = [str(p) for p in converted['pattern']]
        
        elif gpt_type == "gpt4":
            # GPT-4-spezifische Anpassungen
            if 'description' in converted:
                converted['description'] = converted['description'][:500]  # Limit length
        
        elif gpt_type == "custom":
            # Custom-Format
            converted['exported_at'] = datetime.now().isoformat()
            converted['export_format'] = 'gpt_custom'
        
        return converted
    
    def export_markers(self):
        """Exportiert ausgewählte Marker"""
        selected_markers = self.get_selected_markers()
        
        if not selected_markers:
            messagebox.showwarning("Warnung", "Bitte wählen Sie mindestens einen Marker aus!")
            return
        
        try:
            export_format = self.format_var.get()
            gpt_type = self.gpt_var.get()
            
            # Export-Verzeichnis erstellen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = self.export_dir / f"gpt_export_{timestamp}"
            export_path.mkdir(exist_ok=True)
            
            exported_count = 0
            failed_count = 0
            
            for marker_id in selected_markers:
                try:
                    # Marker laden
                    marker_file = self.marker_dir / f"{marker_id}.yaml"
                    if not marker_file.exists():
                        failed_count += 1
                        continue
                    
                    with open(marker_file, 'r', encoding='utf-8') as f:
                        marker_data = yaml.safe_load(f)
                    
                    # Validierung
                    if self.validate_before_export.get():
                        if not self.validate_marker(marker_data):
                            failed_count += 1
                            continue
                    
                    # GPT-Konvertierung
                    converted_data = self.convert_for_gpt(marker_data, gpt_type)
                    
                    # Export
                    if export_format == "yaml":
                        output_file = export_path / f"{marker_id}.yaml"
                        with open(output_file, 'w', encoding='utf-8') as f:
                            yaml.dump(converted_data, f, default_flow_style=False, 
                                    allow_unicode=True, sort_keys=False)
                    
                    elif export_format == "json":
                        output_file = export_path / f"{marker_id}.json"
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(converted_data, f, indent=2, ensure_ascii=False)
                    
                    elif export_format == "txt":
                        output_file = export_path / f"{marker_id}.txt"
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(f"Marker: {marker_id}\n")
                            f.write(f"Level: {converted_data.get('level', 'N/A')}\n")
                            f.write(f"Description: {converted_data.get('description', 'N/A')}\n")
                            if 'examples' in converted_data:
                                f.write("Examples:\n")
                                for ex in converted_data['examples']:
                                    f.write(f"  - {ex}\n")
                    
                    exported_count += 1
                    
                except Exception as e:
                    print(f"Fehler beim Export von {marker_id}: {e}")
                    failed_count += 1
            
            # Erfolgsmeldung
            success_message = f"""✅ Export abgeschlossen!

📁 Export-Verzeichnis: {export_path}
📊 Exportiert: {exported_count} Marker
❌ Fehlgeschlagen: {failed_count} Marker
🎯 Format: {export_format.upper()}
🤖 GPT-Typ: {gpt_type}"""
            
            messagebox.showinfo("Export erfolgreich!", success_message)
            self.status_var.set(f"✅ {exported_count} Marker exportiert")
            
        except Exception as e:
            error_message = f"❌ Export fehlgeschlagen: {str(e)}"
            messagebox.showerror("Export-Fehler", error_message)
            self.status_var.set("❌ Export fehlgeschlagen")
    
    def validate_marker(self, marker_data: Dict[str, Any]) -> bool:
        """Validiert Marker vor Export"""
        required_fields = ['id', 'level', 'description']
        
        for field in required_fields:
            if field not in marker_data or not marker_data[field]:
                return False
        
        return True
    
    def run(self):
        self.root.mainloop()

def main():
    app = GPTYAMLGenerator()
    app.run()

if __name__ == "__main__":
    main() 