#!/usr/bin/env python3
"""
FRAUSAR API GUI - HAUPTMENÜ
============================

Zentrale Anlaufstelle für alle Frausar-Funktionen
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from pathlib import Path

class FrausarMainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Frausar API GUI - Hauptmenü")
        self.root.geometry("800x600")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Haupt-Container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title = ttk.Label(main_frame, text="🚀 Frausar API GUI", 
                         font=("Arial", 24, "bold"))
        title.pack(pady=(0, 10))
        
        subtitle = ttk.Label(main_frame, text="Zentrale Anlaufstelle für alle Funktionen",
                           font=("Arial", 14))
        subtitle.pack(pady=(0, 30))
        
        # Funktionen-Bereich
        functions_frame = ttk.LabelFrame(main_frame, text="📋 Verfügbare Funktionen", padding="20")
        functions_frame.pack(fill=tk.BOTH, expand=True)
        
        # Smart Marker-Erstellung
        marker_frame = ttk.Frame(functions_frame)
        marker_frame.pack(fill=tk.X, pady=(0, 15))
        
        marker_title = ttk.Label(marker_frame, text="🎯 Smart Marker-Erstellung", 
                               font=("Arial", 16, "bold"))
        marker_title.pack(anchor=tk.W)
        
        marker_desc = ttk.Label(marker_frame, 
                              text="Benutzerfreundliche Marker-Erstellung mit automatischer Fehlerbehebung\n"
                                   "• Mehrere Marker auf einmal\n"
                                   "• Marker-Übersicht\n"
                                   "• Beispiele hinzufügen\n"
                                   "• Automatische YAML-Korrektur",
                              font=("Arial", 11))
        marker_desc.pack(anchor=tk.W, pady=(5, 10))
        
        marker_button = ttk.Button(marker_frame, text="🚀 Smart Marker-Erstellung starten", 
                                 command=self.start_smart_marker_gui, style="Accent.TButton")
        marker_button.pack(anchor=tk.W)
        
        # Trenner
        separator = ttk.Separator(functions_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=15)
        
        # API-Server
        api_frame = ttk.Frame(functions_frame)
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        api_title = ttk.Label(api_frame, text="🌐 Frausar AI-API", 
                            font=("Arial", 16, "bold"))
        api_title.pack(anchor=tk.W)
        
        api_desc = ttk.Label(api_frame, 
                           text="AI-gestützte Datenanalyse und -bereinigung\n"
                                "• FastAPI-Server auf http://localhost:8000\n"
                                "• DataCleaningAgent mit Pandas-Integration\n"
                                "• API-Dokumentation verfügbar",
                           font=("Arial", 11))
        api_desc.pack(anchor=tk.W, pady=(5, 10))
        
        api_button = ttk.Button(api_frame, text="🌐 API-Server starten", 
                              command=self.start_api_server)
        api_button.pack(anchor=tk.W)
        
        # Trenner
        separator2 = ttk.Separator(functions_frame, orient='horizontal')
        separator2.pack(fill=tk.X, pady=15)
        
        # Tests
        test_frame = ttk.Frame(functions_frame)
        test_frame.pack(fill=tk.X)
        
        test_title = ttk.Label(test_frame, text="🧪 Tests & Diagnose", 
                             font=("Arial", 16, "bold"))
        test_title.pack(anchor=tk.W)
        
        test_desc = ttk.Label(test_frame, 
                            text="Automatisierte Tests für alle Komponenten\n"
                                 "• API-Verfügbarkeit\n"
                                 "• Datei-Upload und -Verarbeitung\n"
                                 "• Datenbereinigung",
                            font=("Arial", 11))
        test_desc.pack(anchor=tk.W, pady=(5, 10))
        
        test_button = ttk.Button(test_frame, text="🧪 Tests ausführen", 
                               command=self.run_tests)
        test_button.pack(anchor=tk.W)
        
        # Status-Bereich
        status_frame = ttk.LabelFrame(main_frame, text="📊 System-Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.status_label = ttk.Label(status_frame, text="✅ System bereit")
        self.status_label.pack(anchor=tk.W)
    
    def start_smart_marker_gui(self):
        """Startet die Smart Marker-Erstellung"""
        try:
            # Smart Marker GUI starten
            script_path = Path(__file__).parent / "smart_marker_gui.py"
            
            if script_path.exists():
                subprocess.Popen([sys.executable, str(script_path)])
                self.update_status("Smart Marker-Erstellung gestartet")
                messagebox.showinfo("Info", "Smart Marker-Erstellung wird gestartet...")
            else:
                messagebox.showerror("Fehler", "Smart Marker GUI nicht gefunden!")
                
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Starten: {str(e)}")
    
    def start_api_server(self):
        """Startet den API-Server"""
        try:
            # API-Server starten
            api_path = Path(__file__).parent / "api" / "main.py"
            
            if api_path.exists():
                subprocess.Popen([sys.executable, "-m", "uvicorn", "api.main:app", 
                                "--host", "0.0.0.0", "--port", "8000"])
                self.update_status("API-Server gestartet")
                messagebox.showinfo("Info", "API-Server wird gestartet...\n\n"
                                          "Verfügbar unter: http://localhost:8000\n"
                                          "API-Docs: http://localhost:8000/docs")
            else:
                messagebox.showerror("Fehler", "API-Server nicht gefunden!")
                
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Starten: {str(e)}")
    
    def run_tests(self):
        """Führt Tests aus"""
        try:
            # Tests ausführen
            test_path = Path(__file__).parent / "test_ai_integration.py"
            
            if test_path.exists():
                result = subprocess.run([sys.executable, str(test_path)], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    messagebox.showinfo("Tests erfolgreich", "Alle Tests bestanden!")
                else:
                    messagebox.showwarning("Tests fehlgeschlagen", 
                                         f"Einige Tests sind fehlgeschlagen:\n\n{result.stdout}")
                
                self.update_status("Tests ausgeführt")
            else:
                messagebox.showerror("Fehler", "Test-Datei nicht gefunden!")
                
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Ausführen der Tests: {str(e)}")
    
    def update_status(self, message):
        """Aktualisiert den Status"""
        self.status_label.config(text=f"✅ {message}")
    
    def run(self):
        self.root.mainloop()

def main():
    app = FrausarMainGUI()
    app.run()

if __name__ == "__main__":
    main() 