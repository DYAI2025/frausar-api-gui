#!/usr/bin/env python3
"""
Tax Calculator Storage - Data Processing Tool
Simple CSV data management utility
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class TaxCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tax Calculator Storage v2.1")
        self.root.geometry("480x380")
        self.root.configure(bg='#f0f0f0')
        
        self.current_file = None
        self.is_encrypted_file = False
        
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        """Create user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Tax Calculator Storage", 
                              font=("Arial", 12, "normal"), bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=(0, 8))
        
        subtitle_label = tk.Label(main_frame, text="Data processing utility for tax calculations", 
                                 font=("Arial", 9), bg='#f0f0f0', fg='#666666')
        subtitle_label.pack(pady=(0, 20))
        
        # File selection area
        file_frame = tk.LabelFrame(main_frame, text="Select File", 
                                  font=("Arial", 9), bg='#f0f0f0', fg='#333333', 
                                  relief='groove', bd=1, padx=10, pady=8)
        file_frame.pack(fill=tk.X, pady=8)
        
        self.file_label = tk.Label(file_frame, text="No file selected", 
                                  font=("Arial", 9), bg='#f0f0f0', fg='#666666')
        self.file_label.pack(pady=5)
        
        tk.Button(file_frame, text="Browse Data File", 
                 command=self.browse_csv_file, 
                 font=("Arial", 9), bg='#e8e8e8', fg='#333333',
                 relief='raised', bd=1, padx=15, pady=2).pack(pady=2)
        
        tk.Button(file_frame, text="Browse Processed File", 
                 command=self.browse_encrypted_file,
                 font=("Arial", 9), bg='#e8e8e8', fg='#333333',
                 relief='raised', bd=1, padx=15, pady=2).pack(pady=2)
        
        # Status
        self.status_label = tk.Label(main_frame, text="Ready", 
                                    font=("Arial", 9), bg='#f0f0f0', fg='#333333')
        self.status_label.pack(pady=8)
        
        # Action buttons
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=12)
        
        self.process_btn = tk.Button(button_frame, text="Process Data", 
                                    command=self.encrypt_file, state="disabled",
                                    font=("Arial", 9), bg='#d0d0d0', fg='#333333',
                                    relief='raised', bd=1, padx=20, pady=4)
        self.process_btn.pack(side=tk.LEFT, padx=8)
        
        self.extract_btn = tk.Button(button_frame, text="Extract Data", 
                                    command=self.decrypt_file, state="disabled",
                                    font=("Arial", 9), bg='#d0d0d0', fg='#333333',
                                    relief='raised', bd=1, padx=20, pady=4)
        self.extract_btn.pack(side=tk.LEFT, padx=8)
        
        # Info area
        info_frame = tk.LabelFrame(main_frame, text="Information", 
                                  font=("Arial", 9), bg='#f0f0f0', fg='#333333',
                                  relief='groove', bd=1, padx=10, pady=8)
        info_frame.pack(fill=tk.X, pady=8)
        
        info_text = """Process Data: Secure data files for storage
Extract Data: Retrieve processed data files
Supports: CSV, SIP, TXT, XML, JSON formats
Requires access code for data processing"""
        
        tk.Label(info_frame, text=info_text, 
                font=("Arial", 8), bg='#f0f0f0', fg='#666666',
                justify="left").pack(anchor="w")
        
        # Warning
        warning_frame = tk.Frame(main_frame, bg='#f0f0f0')
        warning_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(warning_frame, text="Note: Access code required for data retrieval", 
                font=("Arial", 8), bg='#f0f0f0', fg='#999999').pack()
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
            
    def browse_csv_file(self):
        """Select data file"""
        file_path = filedialog.askopenfilename(
            title="Select data file for processing",
            filetypes=[
                ("CSV files", "*.csv"),
                ("SIP files", "*.sip"),
                ("Text files", "*.txt"),
                ("Data files", "*.dat"),
                ("XML files", "*.xml"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.load_file(file_path, is_encrypted=False)
            
    def browse_encrypted_file(self):
        """Select processed file"""
        file_path = filedialog.askopenfilename(
            title="Select processed file for extraction",
            filetypes=[
                ("Processed files", "*.dat"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.load_file(file_path, is_encrypted=True)
            
    def load_file(self, file_path: str, is_encrypted: bool):
        """Load file and update UI"""
        self.current_file = file_path
        self.is_encrypted_file = is_encrypted
        filename = Path(file_path).name
        
        if is_encrypted:
            self.file_label.config(text=f"{filename}")
            self.process_btn.config(state="disabled")
            self.extract_btn.config(state="normal", bg='#c0c0c0')
            self.status_label.config(text="Processed file loaded - extraction available")
        else:
            file_ext = Path(file_path).suffix.upper()
            self.file_label.config(text=f"{filename}")
            self.process_btn.config(state="normal", bg='#c0c0c0')
            self.extract_btn.config(state="disabled")
            self.status_label.config(text=f"{file_ext} file loaded - processing available")
            
    def get_access_code(self, title: str, confirm: bool = False) -> str:
        """Access code dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("320x180")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 160
        y = (dialog.winfo_screenheight() // 2) - 90
        dialog.geometry(f'+{x}+{y}')
        
        # Main frame
        main_frame = tk.Frame(dialog, bg='#f0f0f0', padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(main_frame, text=title, font=("Arial", 10), 
                bg='#f0f0f0', fg='#333333').pack(pady=(0, 15))
        
        # Access code entry
        tk.Label(main_frame, text="Enter access code:", font=("Arial", 9),
                bg='#f0f0f0', fg='#333333').pack(anchor="w")
        code_var = tk.StringVar()
        code_entry = tk.Entry(main_frame, textvariable=code_var, show="*", 
                             width=30, font=("Arial", 9))
        code_entry.pack(pady=(3, 10), fill=tk.X)
        code_entry.focus()
        
        # Confirm entry if needed
        confirm_var = None
        if confirm:
            tk.Label(main_frame, text="Confirm access code:", font=("Arial", 9),
                    bg='#f0f0f0', fg='#333333').pack(anchor="w")
            confirm_var = tk.StringVar()
            confirm_entry = tk.Entry(main_frame, textvariable=confirm_var, show="*", 
                                   width=30, font=("Arial", 9))
            confirm_entry.pack(pady=(3, 10), fill=tk.X)
        
        result = {'code': None}
        
        def on_ok():
            code = code_var.get()
            if not code:
                messagebox.showerror("Error", "Please enter access code")
                return
                
            if confirm:
                if code != confirm_var.get():
                    messagebox.showerror("Error", "Access codes do not match")
                    return
                    
            result['code'] = code
            dialog.destroy()
            
        def on_cancel():
            dialog.destroy()
            
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="OK", command=on_ok, 
                 font=("Arial", 9), bg='#d0d0d0', fg='#333333',
                 relief='raised', bd=1, padx=15, pady=2).pack(side=tk.LEFT, padx=8)
        tk.Button(button_frame, text="Cancel", command=on_cancel,
                 font=("Arial", 9), bg='#e0e0e0', fg='#333333',
                 relief='raised', bd=1, padx=15, pady=2).pack(side=tk.LEFT, padx=8)
        
        # Enter for OK
        code_entry.bind('<Return>', lambda e: on_ok())
        if confirm:
            confirm_entry.bind('<Return>', lambda e: on_ok())
            
        dialog.wait_window()
        return result['code']
        
    def derive_key(self, code: str, salt: bytes) -> bytes:
        """Derive key from access code"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(code.encode()))
        return key
        
    def encrypt_file(self):
        """Process CSV file"""
        if not self.current_file:
            return
            
        self.status_label.config(text="Processing data...")
        self.root.update()
            
        # Get access code
        code = self.get_access_code("Data Processing", confirm=True)
        if not code:
            self.status_label.config(text="Processing cancelled")
            return
            
        try:
            # Read file
            with open(self.current_file, 'rb') as f:
                data = f.read()
                
            # Generate salt
            salt = os.urandom(16)
            
            # Derive key
            key = self.derive_key(code, salt)
            fernet = Fernet(key)
            
            # Encrypt
            encrypted_data = fernet.encrypt(data)
            
            # Save location
            output_path = filedialog.asksaveasfilename(
                title="Save processed file",
                defaultextension=".dat",
                filetypes=[("Processed files", "*.dat")],
                initialname=Path(self.current_file).stem + ".dat"
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(salt + encrypted_data)
                    
                self.status_label.config(text="Data processing completed")
                messagebox.showinfo("Processing Complete", 
                    f"Data file has been processed successfully.\n\n"
                    f"Original: {Path(self.current_file).name}\n"
                    f"Format: {Path(self.current_file).suffix.upper()}\n"
                    f"Processed: {Path(output_path).name}\n\n"
                    f"Access code required for data extraction.")
            else:
                self.status_label.config(text="Processing cancelled")
                    
        except Exception as e:
            self.status_label.config(text="Processing error")
            messagebox.showerror("Error", f"Processing failed:\n{str(e)}")
            
    def decrypt_file(self):
        """Extract processed file"""
        if not self.current_file:
            return
            
        self.status_label.config(text="Extracting data...")
        self.root.update()
            
        # Get access code
        code = self.get_access_code("Data Extraction")
        if not code:
            self.status_label.config(text="Extraction cancelled")
            return
            
        try:
            # Read processed file
            with open(self.current_file, 'rb') as f:
                data = f.read()
                
            # Extract salt and encrypted data
            salt = data[:16]
            encrypted_data = data[16:]
            
            # Derive key
            key = self.derive_key(code, salt)
            fernet = Fernet(key)
            
            # Decrypt
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Save location - keep original file extension
            original_ext = Path(self.current_file).suffix
            if not original_ext:
                original_ext = ".txt"
                
            output_path = filedialog.asksaveasfilename(
                title="Save extracted data file",
                defaultextension=original_ext,
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("SIP files", "*.sip"),
                    ("Text files", "*.txt"),
                    ("Data files", "*.dat"),
                    ("XML files", "*.xml"),
                    ("JSON files", "*.json"),
                    ("All files", "*.*")
                ],
                initialname=Path(self.current_file).stem + original_ext
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(decrypted_data)
                    
                self.status_label.config(text="Data extraction completed")
                messagebox.showinfo("Extraction Complete", 
                    f"Data file has been extracted successfully.\n\n"
                    f"File: {Path(output_path).name}\n"
                    f"Format: {Path(output_path).suffix.upper()}")
            else:
                self.status_label.config(text="Extraction cancelled")
                    
        except Exception as e:
            self.status_label.config(text="Extraction error")
            if "InvalidToken" in str(e):
                messagebox.showerror("Access Denied", 
                    "Invalid access code.\n\n"
                    "Please verify the access code and try again.")
            else:
                messagebox.showerror("Error", f"Extraction failed:\n{str(e)}")
                
    def run(self):
        """Start application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TaxCalculator()
    app.run() 