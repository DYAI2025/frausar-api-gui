"""
GUI-Passwort-Dialog für sichere Passwort-Eingabe
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

class PasswordDialog:
    """
    Tkinter-Dialog für Passwort-Eingabe
    """
    
    def __init__(self):
        self.password = None
        self.root = None
        
    def get_password(self) -> Optional[str]:
        """
        Zeigt Passwort-Dialog und gibt eingegebenes Passwort zurück
        
        Returns:
            Optional[str]: Eingegebenes Passwort oder None bei Abbruch
        """
        # Hauptfenster erstellen
        self.root = tk.Tk()
        self.root.title("InPricer - Passwort für CSV-Verschlüsselung")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        
        # Zentriere Fenster
        self._center_window()
        
        # Icon setzen (falls verfügbar)
        try:
            # Fallback für fehlendes Icon
            pass
        except:
            pass
        
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header
        header_label = ttk.Label(
            main_frame, 
            text="CSV-Datei Verschlüsselung",
            font=("Arial", 16, "bold")
        )
        header_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Beschreibung
        desc_text = (
            "Ihre CSV-Datei wird mit einem Passwort verschlüsselt.\n"
            "Bitte wählen Sie ein sicheres Passwort:"
        )
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.CENTER)
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Passwort-Eingabe
        password_label = ttk.Label(main_frame, text="Passwort:")
        password_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            main_frame, 
            textvariable=self.password_var, 
            show="*", 
            width=30,
            font=("Arial", 11)
        )
        self.password_entry.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Passwort bestätigen
        confirm_label = ttk.Label(main_frame, text="Passwort bestätigen:")
        confirm_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        self.confirm_var = tk.StringVar()
        self.confirm_entry = ttk.Entry(
            main_frame, 
            textvariable=self.confirm_var, 
            show="*", 
            width=30,
            font=("Arial", 11)
        )
        self.confirm_entry.grid(row=5, column=0, columnspan=2, pady=(0, 15), sticky=(tk.W, tk.E))
        
        # Passwort-Stärke Anzeige
        self.strength_label = ttk.Label(main_frame, text="Passwort-Stärke: ")
        self.strength_label.grid(row=6, column=0, columnspan=2, pady=(0, 15))
        
        # Event-Binding für Live-Validation
        self.password_var.trace('w', self._update_password_strength)
        self.confirm_var.trace('w', self._validate_passwords)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(10, 0))
        
        self.ok_button = ttk.Button(
            button_frame, 
            text="Verschlüsseln", 
            command=self._on_ok,
            style="Accent.TButton"
        )
        self.ok_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = ttk.Button(
            button_frame, 
            text="Abbrechen", 
            command=self._on_cancel
        )
        cancel_button.pack(side=tk.LEFT)
        
        # Enter-Taste bindet an OK
        self.root.bind('<Return>', lambda e: self._on_ok())
        self.root.bind('<Escape>', lambda e: self._on_cancel())
        
        # Fokus auf Passwort-Feld
        self.password_entry.focus()
        
        # Grid-Konfiguration für Responsive Design
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Dialog starten
        self.root.mainloop()
        
        return self.password
    
    def _center_window(self):
        """
        Zentriert das Fenster auf dem Bildschirm
        """
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _update_password_strength(self, *args):
        """
        Aktualisiert Passwort-Stärke-Anzeige
        """
        password = self.password_var.get()
        strength, color = self._calculate_password_strength(password)
        
        self.strength_label.config(
            text=f"Passwort-Stärke: {strength}",
            foreground=color
        )
        
        self._validate_passwords()
    
    def _calculate_password_strength(self, password: str) -> tuple:
        """
        Berechnet Passwort-Stärke
        
        Args:
            password: Zu bewertendas Passwort
            
        Returns:
            tuple: (Stärke-Text, Farbe)
        """
        if len(password) == 0:
            return ("", "black")
        
        score = 0
        
        # Länge
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        
        # Zeichen-Typen
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        
        if score <= 2:
            return ("Schwach", "red")
        elif score <= 4:
            return ("Mittel", "orange")
        else:
            return ("Stark", "green")
    
    def _validate_passwords(self, *args):
        """
        Validiert Passwort-Übereinstimmung
        """
        password = self.password_var.get()
        confirm = self.confirm_var.get()
        
        # OK-Button aktivieren/deaktivieren
        if len(password) >= 6 and password == confirm:
            self.ok_button.config(state="normal")
        else:
            self.ok_button.config(state="disabled")
    
    def _on_ok(self):
        """
        OK-Button Callback
        """
        password = self.password_var.get()
        confirm = self.confirm_var.get()
        
        # Validierung
        if len(password) < 6:
            messagebox.showerror(
                "Fehler", 
                "Das Passwort muss mindestens 6 Zeichen lang sein."
            )
            return
        
        if password != confirm:
            messagebox.showerror(
                "Fehler", 
                "Die Passwörter stimmen nicht überein."
            )
            return
        
        # Sicherheitswarnung bei schwachem Passwort
        strength, _ = self._calculate_password_strength(password)
        if strength == "Schwach":
            result = messagebox.askyesno(
                "Schwaches Passwort",
                "Das gewählte Passwort ist schwach. Möchten Sie trotzdem fortfahren?"
            )
            if not result:
                return
        
        self.password = password
        self.root.destroy()
    
    def _on_cancel(self):
        """
        Abbrechen-Button Callback
        """
        self.password = None
        self.root.destroy()

# Convenience-Funktion für einfachen Zugriff
def get_password_from_user() -> Optional[str]:
    """
    Convenience-Funktion für Passwort-Dialog
    
    Returns:
        Optional[str]: Eingegebenes Passwort oder None
    """
    dialog = PasswordDialog()
    return dialog.get_password() 