#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frausar API GUI
===============
Eine moderne, schnelle und stabile GUI, die auf der neuen, modularen
MarkerEngine aufbaut.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import sys
from pathlib import Path

# Passe den sys.path an, um die MarkerEngine zu finden
# Dies geht davon aus, dass die GUI im Hauptverzeichnis des Projekts liegt
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from MarkerEngine.core.engine import MarkerEngine

class FrausarAPIGUI:
    """Die Hauptklasse für die neue, Engine-basierte GUI."""

    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Frausar API GUI - Powered by MarkerEngine")
        self.root.geometry("1200x800")

        # Initialisiere die MarkerEngine
        # Wir fragen den Benutzer nach dem Verzeichnis
        self.engine = None
        
        self.setup_ui()
        # Schedule the directory selection to run after the main window is ready
        self.root.after(100, self.select_marker_directory)

    def setup_ui(self):
        """Erstellt die Haupt-UI-Komponenten."""
        self.setup_menubar()

        # Haupt-Container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Zweigeteilte Ansicht
        paned_window = ttk.PanedWindow(main_container, orient=HORIZONTAL)
        paned_window.pack(fill=BOTH, expand=True)

        # Linke Seite: Marker-Liste
        marker_list_frame = ttk.Labelframe(paned_window, text="Marker-Verzeichnis", padding=10)
        paned_window.add(marker_list_frame, weight=1)

        # Rechte Seite: Tabs
        self.notebook = ttk.Notebook(paned_window)
        paned_window.add(self.notebook, weight=3)
        
        # --- Linke Seite füllen ---
        self.marker_listbox = tk.Listbox(marker_list_frame)
        self.marker_listbox.pack(fill=BOTH, expand=True)
        self.marker_listbox.bind("<<ListboxSelect>>", self.on_marker_select)

        refresh_button = ttk.Button(marker_list_frame, text="Aktualisieren", command=self.refresh_marker_list)
        refresh_button.pack(fill=X, pady=(5,0))

        # --- Rechte Seite füllen (Tabs) ---
        self.create_marker_tab = ttk.Frame(self.notebook, padding=10)
        self.ai_tools_tab = ttk.Frame(self.notebook, padding=10)
        self.repo_tools_tab = ttk.Frame(self.notebook, padding=10)
        self.preview_tab = ttk.Frame(self.notebook, padding=10) # Neuer Tab

        self.notebook.add(self.create_marker_tab, text="📝 Marker Erstellung")
        self.notebook.add(self.preview_tab, text="👁️ Marker-Vorschau") # Neuer Tab
        self.notebook.add(self.ai_tools_tab, text="🤖 KI-Werkzeuge")
        self.notebook.add(self.repo_tools_tab, text="🔧 Repository-Werkzeuge")

        # Log-Fenster
        log_frame = ttk.Labelframe(main_container, text="Log-Ausgabe", padding=10)
        log_frame.pack(fill=X, pady=(10, 0), side=BOTTOM)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, state="disabled", wrap=WORD)
        self.log_text.pack(fill=X, expand=True)
        # Redirect stdout to the log widget
        sys.stdout = self.TextRedirector(self.log_text)

    def setup_menubar(self):
        """Erstellt die Menüleiste."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)
        
        file_menu.add_command(label="Marker-Verzeichnis wechseln...", command=self.select_marker_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.root.quit)

    def select_marker_directory(self):
        """Fragt den Benutzer nach dem Marker-Verzeichnis und lädt die Marker."""
        directory = filedialog.askdirectory(
            title="Wählen Sie Ihr Marker-Verzeichnis",
            initialdir=str(Path.cwd())
        )
        if directory:
            self.engine = MarkerEngine(directory)
            self.root.title(f"🚀 Frausar API GUI - {directory}")
            self.log_message(f"MarkerEngine initialisiert für: {directory}")
            
            # Fülle die Tabs und die Marker-Liste mit Inhalt
            self.refresh_marker_list()
            self.populate_create_marker_tab()
            self.populate_repo_tools_tab()
            self.populate_ai_tools_tab()
            self.populate_preview_tab() # Preview-Tab initial füllen
        elif not self.engine:
             # Wenn beim ersten Mal abgebrochen wird
            messagebox.showwarning("Abbruch", "Ohne Marker-Verzeichnis kann die Anwendung nicht starten.")
            self.root.destroy()
            
    def refresh_marker_list(self):
        """Lädt die Marker aus dem Verzeichnis und zeigt sie in der Liste an."""
        if not self.engine:
            return
        
        self.log_message("Marker-Liste wird aktualisiert...")
        self.marker_listbox.delete(0, END)
        try:
            markers = self.engine.list_markers()
            for marker in sorted(markers):
                self.marker_listbox.insert(END, marker)
            self.log_message(f"{len(markers)} Marker geladen.")
        except Exception as e:
            self.log_message(f"Fehler beim Laden der Marker: {e}")

    def on_marker_select(self, event=None):
        """Wird aufgerufen, wenn ein Marker in der Liste ausgewählt wird."""
        selection = self.marker_listbox.curselection()
        if not selection:
            return
        
        marker_name = self.marker_listbox.get(selection[0])
        self.show_marker_preview(marker_name)

    def show_marker_preview(self, marker_name):
        """Zeigt den Inhalt des ausgewählten Markers im Vorschau-Tab an."""
        if not self.engine:
            return
            
        try:
            marker = self.engine.get_marker(marker_name)
            
            # Formatiere den Inhalt für die Anzeige
            content = f"Name: {marker.marker_name}\n"
            content += f"Kategorie: {marker.kategorie or 'N/A'}\n"
            content += f"Grabber ID: {marker.semantische_grabber.id}\n"
            content += "="*50 + "\n"
            content += "Beschreibung:\n" + "-"*20 + f"\n{marker.beschreibung}\n\n"
            content += "Beispiele:\n" + "-"*20 + "\n"
            for ex in marker.beispiele:
                content += f"- {ex.text}\n"
            
            self.preview_text.config(state="normal")
            self.preview_text.delete("1.0", END)
            self.preview_text.insert("1.0", content)
            self.preview_text.config(state="disabled")
            
            # Wechsle zum Vorschau-Tab
            self.notebook.select(self.preview_tab)

        except Exception as e:
            self.log_message(f"Fehler beim Anzeigen der Vorschau für {marker_name}: {e}")

    def populate_preview_tab(self):
        """Füllt den Vorschau-Tab mit Widgets."""
        tab_frame = self.preview_tab
        for widget in tab_frame.winfo_children():
            widget.destroy()
            
        self.preview_text = scrolledtext.ScrolledText(tab_frame, wrap=WORD, state="disabled")
        self.preview_text.pack(fill=BOTH, expand=True)

    def populate_create_marker_tab(self):
        """Füllt den 'Marker Erstellung'-Tab mit Widgets."""
        # Frame für den Tab-Inhalt
        tab_frame = self.create_marker_tab
        for widget in tab_frame.winfo_children():
            widget.destroy() # Alte Widgets entfernen

        # Anleitung
        info_text = "Fügen Sie hier einen oder mehrere YAML-Marker ein. Trennen Sie mehrere Marker durch eine Zeile mit '---'."
        info_label = ttk.Label(tab_frame, text=info_text, wraplength=800, justify=LEFT)
        info_label.pack(fill=X, pady=(0, 10))

        # Textfeld für die Eingabe
        self.multi_marker_text = scrolledtext.ScrolledText(tab_frame, height=20, wrap=WORD)
        self.multi_marker_text.pack(fill=BOTH, expand=True)
        self.multi_marker_text.insert(END, "# Fügen Sie hier Ihre Marker ein...\n---\n")

        # Button zum Erstellen
        self.create_button = ttk.Button(tab_frame, text="Alle Marker erstellen", command=self.handle_create_multiple_markers, style="success.TButton")
        self.create_button.pack(pady=(10, 0))
        
        # Initially disable widgets until a directory is selected
        self.multi_marker_text.config(state="disabled")
        self.create_button.config(state="disabled")

    def populate_repo_tools_tab(self):
        """Füllt den 'Repository-Werkzeuge'-Tab mit Widgets."""
        tab_frame = self.repo_tools_tab
        for widget in tab_frame.winfo_children():
            widget.destroy()

        validate_button = ttk.Button(tab_frame, text="Repository validieren", command=self.handle_validate_repo)
        validate_button.pack(pady=10)
        
        repair_button = ttk.Button(tab_frame, text="Repository automatisch reparieren", command=self.handle_repair_repo, style="warning.TButton")
        repair_button.pack(pady=10)

    def populate_ai_tools_tab(self):
        """Füllt den 'KI-Werkzeuge'-Tab mit Widgets."""
        tab_frame = self.ai_tools_tab
        for widget in tab_frame.winfo_children():
            widget.destroy()
            
        label = ttk.Label(tab_frame, text="KI-Funktionen sind in Entwicklung.", font=("Helvetica", 14))
        label.pack(pady=20)

    def handle_create_multiple_markers(self):
        """Nimmt den Text aus dem Eingabefeld und erstellt die Marker."""
        if not self.engine:
            self.log_message("Fehler: Kein Marker-Verzeichnis ausgewählt.")
            return

        content = self.multi_marker_text.get("1.0", END).strip()
        if not content:
            self.log_message("Warnung: Kein Text zur Erstellung von Markern eingegeben.")
            return
        
        self.log_message("\nStarte Multi-Marker-Erstellung...")
        
        # Direkter Aufruf unserer robusten Engine-Funktion
        created_markers = self.engine.create_multiple_markers(content)
        
        if created_markers:
            self.log_message(f"Erfolg: {len(created_markers)} Marker wurden erfolgreich erstellt/aktualisiert.")
            messagebox.showinfo("Erfolg", f"{len(created_markers)} Marker erfolgreich erstellt!")
        else:
            self.log_message("Fehler: Keine Marker konnten erstellt werden. Überprüfen Sie die Log-Ausgabe auf Fehler.")
            messagebox.showerror("Fehler", "Keine Marker konnten erstellt werden. Details im Log.")
            
        # Textfeld leeren nach Erfolg
        self.multi_marker_text.delete("1.0", END)

    def handle_validate_repo(self):
        if not self.engine: return
        self.log_message("\nStarte Repository-Validierung...")
        self.engine.validate_repository(auto_repair=False)
        self.log_message("Validierung abgeschlossen.")

    def handle_repair_repo(self):
        if not self.engine: return
        self.log_message("\nStarte Repository-Reparatur...")
        self.engine.validate_repository(auto_repair=True)
        self.log_message("Reparatur abgeschlossen.")

    def log_message(self, message):
        """Schreibt eine Nachricht in das Log-Fenster."""
        self.log_text.config(state="normal")
        self.log_text.insert(END, f"{message}\n")
        self.log_text.config(state="disabled")
        self.log_text.see(END)

    # Klasse zur Umleitung von print-Ausgaben ins Log-Fenster
    class TextRedirector:
        def __init__(self, widget):
            self.widget = widget

        def write(self, s):
            self.widget.config(state="normal")
            self.widget.insert(END, s)
            self.widget.config(state="disabled")
            self.widget.see(END)

        def flush(self):
            pass # Nötig für die file-like interface


def main():
    # Style mit ttkbootstrap
    root = ttkb.Window(themename="superhero")
    app = FrausarAPIGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 