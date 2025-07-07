#!/usr/bin/env python3
"""
Tax Calculator Storage - Anonymous English Version
Multi-format file encryption tool with professional interface
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class TaxCalculatorStorage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tax Calculator Storage")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Professional styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        """Create professional user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="Tax Calculator Storage", style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="15")
        file_frame.pack(fill=tk.X, pady=10)
        
        # Input file
        ttk.Label(file_frame, text="Select file to process:").pack(anchor=tk.W)
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        self.input_path = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path, width=50)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(input_frame, text="Browse", command=self.browse_input_file).pack(side=tk.RIGHT)
        
        # Encrypted file (for decryption)
        ttk.Label(file_frame, text="Or select encrypted file:").pack(anchor=tk.W, pady=(10, 0))
        encrypted_frame = ttk.Frame(file_frame)
        encrypted_frame.pack(fill=tk.X, pady=5)
        
        self.encrypted_path = tk.StringVar()
        self.encrypted_entry = ttk.Entry(encrypted_frame, textvariable=self.encrypted_path, width=50)
        self.encrypted_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(encrypted_frame, text="Browse", command=self.browse_encrypted_file).pack(side=tk.RIGHT)
        
        # Password section
        password_frame = ttk.LabelFrame(main_frame, text="Security", padding="15")
        password_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(password_frame, text="Password:").pack(anchor=tk.W)
        self.password = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password, show="*", width=30)
        self.password_entry.pack(anchor=tk.W, pady=5)
        
        # Confirm password (only for encryption)
        ttk.Label(password_frame, text="Confirm password (for encryption):").pack(anchor=tk.W, pady=(10, 0))
        self.confirm_password = tk.StringVar()
        self.confirm_entry = ttk.Entry(password_frame, textvariable=self.confirm_password, show="*", width=30)
        self.confirm_entry.pack(anchor=tk.W, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.process_btn = ttk.Button(button_frame, text="Process Data", 
                                     command=self.process_data, width=15)
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        self.decrypt_btn = ttk.Button(button_frame, text="Decrypt File", 
                                     command=self.decrypt_file, width=15)
        self.decrypt_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_all, width=15).pack(side=tk.LEFT, padx=5)
        
        # Status area
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.status_text = tk.Text(status_frame, height=8, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Footer
        footer = ttk.Label(main_frame, text="Professional Data Processing Tool", 
                          font=('Arial', 8), foreground='gray')
        footer.pack(pady=(10, 0))
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def log_status(self, message: str):
        """Add status message"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()
        
    def browse_input_file(self):
        """Browse for input file"""
        file_path = filedialog.askopenfilename(
            title="Select file to process",
            filetypes=[
                ("CSV files", "*.csv"),
                ("SIP files", "*.sip"),
                ("Text files", "*.txt"),
                ("XML files", "*.xml"),
                ("JSON files", "*.json"),
                ("Data files", "*.dat"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.input_path.set(file_path)
            self.encrypted_path.set("")  # Clear encrypted path
            
    def browse_encrypted_file(self):
        """Browse for encrypted file"""
        file_path = filedialog.askopenfilename(
            title="Select encrypted file",
            filetypes=[("Encrypted files", "*.encrypted"), ("All files", "*.*")]
        )
        if file_path:
            self.encrypted_path.set(file_path)
            self.input_path.set("")  # Clear input path
            
    def validate_inputs(self, for_encryption=True):
        """Validate user inputs"""
        if for_encryption:
            if not self.input_path.get():
                messagebox.showerror("Error", "Please select a file to process")
                return False
            if not os.path.exists(self.input_path.get()):
                messagebox.showerror("Error", "Selected file does not exist")
                return False
        else:
            if not self.encrypted_path.get():
                messagebox.showerror("Error", "Please select an encrypted file")
                return False
            if not os.path.exists(self.encrypted_path.get()):
                messagebox.showerror("Error", "Selected encrypted file does not exist")
                return False
                
        if not self.password.get():
            messagebox.showerror("Error", "Please enter a password")
            return False
            
        if for_encryption:
            if not self.confirm_password.get():
                messagebox.showerror("Error", "Please confirm your password")
                return False
            if self.password.get() != self.confirm_password.get():
                messagebox.showerror("Error", "Passwords do not match")
                return False
            if len(self.password.get()) < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters long")
                return False
                
        return True
        
    def process_data(self):
        """Process (encrypt) the selected file"""
        if not self.validate_inputs(for_encryption=True):
            return
            
        try:
            input_file = self.input_path.get()
            password = self.password.get()
            
            self.log_status("Starting data processing...")
            
            # Read file
            with open(input_file, 'rb') as f:
                file_data = f.read()
                
            self.log_status(f"File loaded: {len(file_data)} bytes")
            
            # Generate salt and derive key
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            
            # Encrypt
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(file_data)
            
            # Save encrypted file
            output_path = filedialog.asksaveasfilename(
                title="Save processed file",
                defaultextension=".encrypted",
                filetypes=[("Encrypted files", "*.encrypted"), ("All files", "*.*")]
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(salt + encrypted_data)
                    
                self.log_status(f"Data processing completed successfully")
                self.log_status(f"Output saved: {Path(output_path).name}")
                messagebox.showinfo("Success", "File processed and secured successfully!")
            
        except Exception as e:
            self.log_status(f"Error during processing: {str(e)}")
            messagebox.showerror("Error", f"Processing failed:\n{str(e)}")
            
    def decrypt_file(self):
        """Decrypt the selected encrypted file"""
        if not self.validate_inputs(for_encryption=False):
            return
            
        try:
            encrypted_file = self.encrypted_path.get()
            password = self.password.get()
            
            self.log_status("Starting file decryption...")
            
            # Read encrypted file
            with open(encrypted_file, 'rb') as f:
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
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            
            # Decrypt
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Save decrypted file
            output_path = filedialog.asksaveasfilename(
                title="Save decrypted file",
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(decrypted_data)
                    
                self.log_status("Decryption completed successfully")
                self.log_status(f"Output saved: {Path(output_path).name}")
                messagebox.showinfo("Success", "File decrypted successfully!")
                
        except Exception as e:
            self.log_status(f"Decryption failed: {str(e)}")
            if "InvalidToken" in str(e):
                messagebox.showerror("Error", "Decryption failed. Please check your password.")
            else:
                messagebox.showerror("Error", f"Decryption failed:\n{str(e)}")
                
    def clear_all(self):
        """Clear all inputs and status"""
        self.input_path.set("")
        self.encrypted_path.set("")
        self.password.set("")
        self.confirm_password.set("")
        
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
        
        self.log_status("Interface cleared")
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TaxCalculatorStorage()
    app.run() 