#!/usr/bin/env python3
"""
CSV Vault - Anonymous English Version
Simple CSV file encryption tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CSVVault:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CSV Vault")
        self.root.geometry("500x400")
        self.root.configure(bg='#ffffff')
        
        # Clean styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        """Create clean user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="CSV Vault", font=('Arial', 16, 'bold'))
        title.pack(pady=(0, 20))
        
        # CSV file selection
        csv_frame = ttk.LabelFrame(main_frame, text="CSV File", padding="15")
        csv_frame.pack(fill=tk.X, pady=10)
        
        self.csv_path = tk.StringVar()
        csv_entry_frame = ttk.Frame(csv_frame)
        csv_entry_frame.pack(fill=tk.X)
        
        self.csv_entry = ttk.Entry(csv_entry_frame, textvariable=self.csv_path, width=40)
        self.csv_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(csv_entry_frame, text="Select CSV File", 
                  command=self.browse_csv_file).pack(side=tk.RIGHT)
        
        # Encrypted file selection
        encrypted_frame = ttk.LabelFrame(main_frame, text="Encrypted File", padding="15")
        encrypted_frame.pack(fill=tk.X, pady=10)
        
        self.encrypted_path = tk.StringVar()
        encrypted_entry_frame = ttk.Frame(encrypted_frame)
        encrypted_entry_frame.pack(fill=tk.X)
        
        self.encrypted_entry = ttk.Entry(encrypted_entry_frame, textvariable=self.encrypted_path, width=40)
        self.encrypted_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(encrypted_entry_frame, text="Select Encrypted File", 
                  command=self.browse_encrypted_file).pack(side=tk.RIGHT)
        
        # Password section
        password_frame = ttk.LabelFrame(main_frame, text="Password", padding="15")
        password_frame.pack(fill=tk.X, pady=10)
        
        self.password = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password, 
                                       show="*", width=30)
        self.password_entry.pack()
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.encrypt_btn = ttk.Button(button_frame, text="Encrypt CSV", 
                                     command=self.encrypt_csv, width=15)
        self.encrypt_btn.pack(side=tk.LEFT, padx=5)
        
        self.decrypt_btn = ttk.Button(button_frame, text="Decrypt File", 
                                     command=self.decrypt_file, width=15)
        self.decrypt_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_all, width=15).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
        self.status_label.pack(pady=10)
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def update_status(self, message: str, color: str = "black"):
        """Update status message"""
        self.status_label.config(text=message, foreground=color)
        self.root.update()
        
    def browse_csv_file(self):
        """Browse for CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_path.set(file_path)
            self.encrypted_path.set("")  # Clear encrypted path
            
    def browse_encrypted_file(self):
        """Browse for encrypted file"""
        file_path = filedialog.askopenfilename(
            title="Select encrypted file",
            filetypes=[("Encrypted files", "*.encrypted"), ("All files", "*.*")]
        )
        if file_path:
            self.encrypted_path.set(file_path)
            self.csv_path.set("")  # Clear CSV path
            
    def encrypt_csv(self):
        """Encrypt CSV file"""
        if not self.csv_path.get():
            messagebox.showerror("Error", "Please select a CSV file")
            return
            
        if not self.password.get():
            messagebox.showerror("Error", "Please enter a password")
            return
            
        if not os.path.exists(self.csv_path.get()):
            messagebox.showerror("Error", "Selected CSV file does not exist")
            return
            
        try:
            self.update_status("Encrypting...", "blue")
            
            # Read CSV file
            with open(self.csv_path.get(), 'rb') as f:
                csv_data = f.read()
                
            # Generate salt and derive key
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.password.get().encode()))
            
            # Encrypt
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(csv_data)
            
            # Save encrypted file
            output_path = filedialog.asksaveasfilename(
                title="Save encrypted file",
                defaultextension=".encrypted",
                filetypes=[("Encrypted files", "*.encrypted"), ("All files", "*.*")]
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(salt + encrypted_data)
                    
                self.update_status("Encryption completed successfully", "green")
                messagebox.showinfo("Success", "CSV file encrypted successfully!")
            else:
                self.update_status("Ready", "green")
                
        except Exception as e:
            self.update_status("Encryption failed", "red")
            messagebox.showerror("Error", f"Encryption failed:\n{str(e)}")
            
    def decrypt_file(self):
        """Decrypt encrypted file"""
        if not self.encrypted_path.get():
            messagebox.showerror("Error", "Please select an encrypted file")
            return
            
        if not self.password.get():
            messagebox.showerror("Error", "Please enter a password")
            return
            
        if not os.path.exists(self.encrypted_path.get()):
            messagebox.showerror("Error", "Selected encrypted file does not exist")
            return
            
        try:
            self.update_status("Decrypting...", "blue")
            
            # Read encrypted file
            with open(self.encrypted_path.get(), 'rb') as f:
                data = f.read()
                
            # Extract salt and encrypted data
            salt = data[:16]
            encrypted_data = data[16:]
            
            # Derive key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.password.get().encode()))
            
            # Decrypt
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Save decrypted file
            output_path = filedialog.asksaveasfilename(
                title="Save decrypted file",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(decrypted_data)
                    
                self.update_status("Decryption completed successfully", "green")
                messagebox.showinfo("Success", "File decrypted successfully!")
            else:
                self.update_status("Ready", "green")
                
        except Exception as e:
            self.update_status("Decryption failed", "red")
            if "InvalidToken" in str(e):
                messagebox.showerror("Error", "Decryption failed. Please check your password.")
            else:
                messagebox.showerror("Error", f"Decryption failed:\n{str(e)}")
                
    def clear_all(self):
        """Clear all inputs"""
        self.csv_path.set("")
        self.encrypted_path.set("")
        self.password.set("")
        self.update_status("Ready", "green")
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CSVVault()
    app.run() 