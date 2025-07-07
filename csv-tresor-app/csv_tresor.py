#!/usr/bin/env python3
"""
CSV-Tresor - Einfache Verschlüsselung für CSV-Dateien
Einfach per Doppelklick starten
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CSVTresor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔒 CSV-Tresor - Sichere Verschlüsselung")
        self.root.geometry("600x500")
        
        self.current_file = None
        self.is_encrypted_file = False
        
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        """Erstelle die Benutzeroberfläche"""
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title_label = ttk.Label(main_frame, text="🔒 CSV-Tresor", 
                               font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Sichere Verschlüsselung für CSV-Dateien", 
                                  font=("Arial", 12))
        subtitle_label.pack(pady=(0, 30))
        
        # Datei-Auswahl Bereich
        file_frame = ttk.LabelFrame(main_frame, text="Datei auswählen", padding="20")
        file_frame.pack(fill=tk.X, pady=20)
        
        self.file_label = ttk.Label(file_frame, 
                                   text="📁 Keine Datei ausgewählt", 
                                   font=("Arial", 12))
        self.file_label.pack(pady=10)
        
        ttk.Button(file_frame, text="📂 CSV-Datei auswählen", 
                  command=self.browse_csv_file, 
                  style="Accent.TButton").pack(pady=5)
        
        ttk.Button(file_frame, text="🔒 Verschlüsselte Datei auswählen", 
                  command=self.browse_encrypted_file).pack(pady=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Bereit - Datei auswählen", 
                                     font=("Arial", 11), foreground="blue")
        self.status_label.pack(pady=15)
        
        # Aktions-Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        self.encrypt_btn = ttk.Button(button_frame, text="🔒 Verschlüsseln", 
                                     command=self.encrypt_file, state="disabled",
                                     style="Accent.TButton")
        self.encrypt_btn.pack(side=tk.LEFT, padx=10)
        
        self.decrypt_btn = ttk.Button(button_frame, text="🔓 Entschlüsseln", 
                                     command=self.decrypt_file, state="disabled",
                                     style="Accent.TButton")
        self.decrypt_btn.pack(side=tk.LEFT, padx=10)
        
        # Info-Bereich
        info_frame = ttk.LabelFrame(main_frame, text="So funktioniert's", padding="15")
        info_frame.pack(fill=tk.X, pady=20)
        
        info_text = """💡 Verschlüsseln:
1. CSV-Datei auswählen
2. "Verschlüsseln" klicken
3. Passwort eingeben + bestätigen
4. Sichere .encrypted Datei wird erstellt

🔓 Entschlüsseln:
1. .encrypted Datei auswählen  
2. "Entschlüsseln" klicken
3. Passwort eingeben
4. CSV-Datei wird wiederhergestellt"""
        
        ttk.Label(info_frame, text=info_text, 
                 font=("Arial", 10), justify="left").pack()
        
        # Warnung
        warning_frame = ttk.Frame(main_frame)
        warning_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(warning_frame, text="⚠️ Wichtig: Passwort gut merken - keine Wiederherstellung möglich!", 
                 font=("Arial", 10, "bold"), foreground="red").pack()
        
    def center_window(self):
        """Zentriere das Fenster"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
            
    def browse_csv_file(self):
        """CSV-Datei auswählen"""
        file_path = filedialog.askopenfilename(
            title="CSV-Datei zum Verschlüsseln auswählen",
            filetypes=[
                ("CSV Dateien", "*.csv"),
                ("Text Dateien", "*.txt"),
                ("Alle Dateien", "*.*")
            ]
        )
        if file_path:
            self.load_file(file_path, is_encrypted=False)
            
    def browse_encrypted_file(self):
        """Verschlüsselte Datei auswählen"""
        file_path = filedialog.askopenfilename(
            title="Verschlüsselte Datei zum Entschlüsseln auswählen",
            filetypes=[
                ("Verschlüsselte Dateien", "*.encrypted"),
                ("Alle Dateien", "*.*")
            ]
        )
        if file_path:
            self.load_file(file_path, is_encrypted=True)
            
    def load_file(self, file_path: str, is_encrypted: bool):
        """Datei laden und UI aktualisieren"""
        self.current_file = file_path
        self.is_encrypted_file = is_encrypted
        filename = Path(file_path).name
        
        if is_encrypted:
            self.file_label.config(text=f"🔒 {filename}")
            self.encrypt_btn.config(state="disabled")
            self.decrypt_btn.config(state="normal")
            self.status_label.config(text="Verschlüsselte Datei geladen - Entschlüsseln möglich", 
                                   foreground="green")
        else:
            self.file_label.config(text=f"📄 {filename}")
            self.encrypt_btn.config(state="normal")
            self.decrypt_btn.config(state="disabled")
            self.status_label.config(text="CSV-Datei geladen - Verschlüsselung möglich", 
                                   foreground="green")
            
    def get_password(self, title: str, confirm: bool = False) -> str:
        """Passwort-Dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Zentriere Dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 125
        dialog.geometry(f'+{x}+{y}')
        
        # Hauptframe
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        ttk.Label(main_frame, text=title, font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Passwort eingeben
        ttk.Label(main_frame, text="Passwort eingeben:", font=("Arial", 12)).pack(anchor="w")
        password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, textvariable=password_var, show="*", width=35, font=("Arial", 11))
        password_entry.pack(pady=(5, 15), fill=tk.X)
        password_entry.focus()
        
        # Passwort bestätigen (falls nötig)
        confirm_var = None
        if confirm:
            ttk.Label(main_frame, text="Passwort wiederholen:", font=("Arial", 12)).pack(anchor="w")
            confirm_var = tk.StringVar()
            confirm_entry = ttk.Entry(main_frame, textvariable=confirm_var, show="*", width=35, font=("Arial", 11))
            confirm_entry.pack(pady=(5, 15), fill=tk.X)
        
        result = {'password': None}
        
        def on_ok():
            password = password_var.get()
            if not password:
                messagebox.showerror("Fehler", "Bitte Passwort eingeben!")
                return
                
            if confirm:
                if password != confirm_var.get():
                    messagebox.showerror("Fehler", "Passwörter stimmen nicht überein!")
                    return
                    
            result['password'] = password
            dialog.destroy()
            
        def on_cancel():
            dialog.destroy()
            
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="OK", command=on_ok, style="Accent.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Abbrechen", command=on_cancel).pack(side=tk.LEFT, padx=10)
        
        # Enter für OK
        password_entry.bind('<Return>', lambda e: on_ok())
        if confirm:
            confirm_entry.bind('<Return>', lambda e: on_ok())
            
        dialog.wait_window()
        return result['password']
        
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """Schlüssel aus Passwort ableiten"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
        
    def encrypt_file(self):
        """CSV-Datei verschlüsseln"""
        if not self.current_file:
            return
            
        self.status_label.config(text="Verschlüsselung läuft...", foreground="orange")
        self.root.update()
            
        # Passwort abfragen
        password = self.get_password("Passwort für Verschlüsselung", confirm=True)
        if not password:
            self.status_label.config(text="Verschlüsselung abgebrochen", foreground="red")
            return
            
        try:
            # Datei lesen
            with open(self.current_file, 'rb') as f:
                data = f.read()
                
            # Salt generieren
            salt = os.urandom(16)
            
            # Schlüssel ableiten
            key = self.derive_key(password, salt)
            fernet = Fernet(key)
            
            # Verschlüsseln
            encrypted_data = fernet.encrypt(data)
            
            # Speicherort wählen
            output_path = filedialog.asksaveasfilename(
                title="Verschlüsselte Datei speichern",
                defaultextension=".encrypted",
                filetypes=[("Verschlüsselte Dateien", "*.encrypted")],
                initialname=Path(self.current_file).stem + ".encrypted"
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(salt + encrypted_data)
                    
                self.status_label.config(text=f"✅ Erfolgreich verschlüsselt!", foreground="green")
                messagebox.showinfo("Erfolg", 
                    f"Datei wurde verschlüsselt gespeichert!\n\n"
                    f"📁 Datei: {Path(output_path).name}\n"
                    f"🔒 Zum Öffnen wird das gleiche Passwort benötigt.\n\n"
                    f"⚠️ Passwort gut merken - keine Wiederherstellung möglich!")
            else:
                self.status_label.config(text="Verschlüsselung abgebrochen", foreground="red")
                    
        except Exception as e:
            self.status_label.config(text="❌ Fehler bei der Verschlüsselung", foreground="red")
            messagebox.showerror("Fehler", f"Verschlüsselung fehlgeschlagen:\n{str(e)}")
            
    def decrypt_file(self):
        """Verschlüsselte Datei entschlüsseln"""
        if not self.current_file:
            return
            
        self.status_label.config(text="Entschlüsselung läuft...", foreground="orange")
        self.root.update()
            
        # Passwort abfragen
        password = self.get_password("Passwort zum Entschlüsseln")
        if not password:
            self.status_label.config(text="Entschlüsselung abgebrochen", foreground="red")
            return
            
        try:
            # Verschlüsselte Datei lesen
            with open(self.current_file, 'rb') as f:
                data = f.read()
                
            # Salt und verschlüsselte Daten trennen
            salt = data[:16]
            encrypted_data = data[16:]
            
            # Schlüssel ableiten
            key = self.derive_key(password, salt)
            fernet = Fernet(key)
            
            # Entschlüsseln
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Speicherort wählen
            output_path = filedialog.asksaveasfilename(
                title="Entschlüsselte CSV speichern",
                defaultextension=".csv",
                filetypes=[("CSV Dateien", "*.csv")],
                initialname=Path(self.current_file).stem + ".csv"
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(decrypted_data)
                    
                self.status_label.config(text=f"✅ Erfolgreich entschlüsselt!", foreground="green")
                messagebox.showinfo("Erfolg", 
                    f"Datei wurde entschlüsselt gespeichert!\n\n"
                    f"📁 Datei: {Path(output_path).name}")
            else:
                self.status_label.config(text="Entschlüsselung abgebrochen", foreground="red")
                    
        except Exception as e:
            self.status_label.config(text="❌ Fehler beim Entschlüsseln", foreground="red")
            if "InvalidToken" in str(e):
                messagebox.showerror("Falsches Passwort", 
                    "Das eingegebene Passwort ist falsch!\n\n"
                    "Bitte versuchen Sie es erneut.")
            else:
                messagebox.showerror("Fehler", f"Entschlüsselung fehlgeschlagen:\n{str(e)}")
                
    def run(self):
        """GUI starten"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CSVTresor()
    app.run() 