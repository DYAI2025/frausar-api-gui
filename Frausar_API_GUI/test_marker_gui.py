#!/usr/bin/env python3
"""
Test-Skript für die Marker-GUI
=============================

Testet ob das Eingabefeld funktioniert und Text eingegeben werden kann.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import os

def test_text_input():
    """Testet das Textfeld."""
    root = tk.Tk()
    root.title("🧪 Test: Textfeld-Funktionalität")
    root.geometry("600x400")
    
    # Haupt-Container
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Titel
    title_label = ttk.Label(main_frame, text="🧪 Test: Textfeld-Funktionalität", 
                           font=("Helvetica", 14, "bold"))
    title_label.pack(pady=(0, 10))
    
    # Anleitung
    instruction_text = """Test-Anleitung:
1. Klicken Sie in das Textfeld unten
2. Tippen Sie etwas ein (z.B. "Test")
3. Drücken Sie Enter
4. Prüfen Sie ob der Text erscheint"""
    
    instruction_label = ttk.Label(main_frame, text=instruction_text, 
                                 font=("Helvetica", 10), foreground="blue")
    instruction_label.pack(anchor=tk.W, pady=(0, 10))
    
    # Textfeld
    text_frame = ttk.LabelFrame(main_frame, text="Textfeld-Test", padding="5")
    text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    text_widget = scrolledtext.ScrolledText(text_frame, height=15, 
                                           wrap=tk.WORD, font=("Consolas", 11))
    text_widget.pack(fill=tk.BOTH, expand=True)
    
    # Test-Button
    def test_input():
        """Testet die Eingabe."""
        current_text = text_widget.get("1.0", tk.END).strip()
        if current_text:
            result_label.config(text=f"✅ Textfeld funktioniert! Eingabe: '{current_text}'")
        else:
            result_label.config(text="❌ Kein Text im Textfeld gefunden")
    
    test_button = ttk.Button(main_frame, text="🧪 Test Eingabe", command=test_input)
    test_button.pack(pady=(0, 10))
    
    # Ergebnis
    result_label = ttk.Label(main_frame, text="Klicken Sie 'Test Eingabe' nach der Eingabe", 
                            font=("Helvetica", 10))
    result_label.pack()
    
    # Fokus auf Textfeld setzen
    text_widget.focus_set()
    
    # Test-Text einfügen
    text_widget.insert("1.0", "Test-Text: Tippen Sie hier etwas ein...\n")
    
    root.mainloop()

if __name__ == "__main__":
    test_text_input() 