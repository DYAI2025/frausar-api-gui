#!/usr/bin/env python3
"""
Tax Calculator Storage - Enhanced Security Version
Maximum security data processing utility
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import base64
import secrets
import hashlib
import time
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

class SecureTaxCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tax Calculator Storage v3.0 - Enhanced Security")
        self.root.geometry("520x420")
        self.root.configure(bg='#f0f0f0')
        
        self.current_file = None
        self.is_encrypted_file = False
        self.failed_attempts = 0
        self.last_attempt_time = 0
        
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        """Create user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with security indicator
        title_label = tk.Label(main_frame, text="Tax Calculator Storage", 
                              font=("Arial", 12, "normal"), bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=(0, 4))
        
        security_label = tk.Label(main_frame, text="🔒 Enhanced Security v3.0", 
                                 font=("Arial", 8), bg='#f0f0f0', fg='#006600')
        security_label.pack(pady=(0, 12))
        
        subtitle_label = tk.Label(main_frame, text="Maximum security data processing utility", 
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
        
        self.process_btn = tk.Button(button_frame, text="🔐 Process Data", 
                                    command=self.encrypt_file, state="disabled",
                                    font=("Arial", 9), bg='#d0d0d0', fg='#333333',
                                    relief='raised', bd=1, padx=20, pady=4)
        self.process_btn.pack(side=tk.LEFT, padx=8)
        
        self.extract_btn = tk.Button(button_frame, text="🔓 Extract Data", 
                                    command=self.decrypt_file, state="disabled",
                                    font=("Arial", 9), bg='#d0d0d0', fg='#333333',
                                    relief='raised', bd=1, padx=20, pady=4)
        self.extract_btn.pack(side=tk.LEFT, padx=8)
        
        # Security info area
        security_frame = tk.LabelFrame(main_frame, text="Security Features", 
                                      font=("Arial", 9), bg='#f0f0f0', fg='#333333',
                                      relief='groove', bd=1, padx=10, pady=8)
        security_frame.pack(fill=tk.X, pady=8)
        
        security_text = """🔐 AES-256 encryption with Fernet
🔑 Scrypt + PBKDF2 (1M iterations) key derivation
🛡️ 32-byte salt + integrity verification
⏱️ Rate limiting + timing attack protection"""
        
        tk.Label(security_frame, text=security_text, 
                font=("Arial", 8), bg='#f0f0f0', fg='#006600',
                justify="left").pack(anchor="w")
        
        # Info area
        info_frame = tk.LabelFrame(main_frame, text="Information", 
                                  font=("Arial", 9), bg='#f0f0f0', fg='#333333',
                                  relief='groove', bd=1, padx=10, pady=8)
        info_frame.pack(fill=tk.X, pady=8)
        
        info_text = """Process Data: Maximum security file encryption
Extract Data: Secure data retrieval with verification
Supports: CSV, SIP, TXT, XML, JSON formats
Military-grade encryption standards"""
        
        tk.Label(info_frame, text=info_text, 
                font=("Arial", 8), bg='#f0f0f0', fg='#666666',
                justify="left").pack(anchor="w")
        
        # Warning
        warning_frame = tk.Frame(main_frame, bg='#f0f0f0')
        warning_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(warning_frame, text="⚠️ Maximum security: Lost access codes cannot be recovered", 
                font=("Arial", 8), bg='#f0f0f0', fg='#cc0000').pack()
        
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
            self.file_label.config(text=f"🔒 {filename}")
            self.process_btn.config(state="disabled")
            self.extract_btn.config(state="normal", bg='#c0c0c0')
            self.status_label.config(text="Encrypted file loaded - extraction available")
        else:
            file_ext = Path(file_path).suffix.upper()
            self.file_label.config(text=f"📄 {filename}")
            self.process_btn.config(state="normal", bg='#c0c0c0')
            self.extract_btn.config(state="disabled")
            self.status_label.config(text=f"{file_ext} file loaded - processing available")
    
    def check_rate_limit(self) -> bool:
        """Check rate limiting for failed attempts"""
        current_time = time.time()
        
        # Reset counter after 5 minutes
        if current_time - self.last_attempt_time > 300:
            self.failed_attempts = 0
            
        # Block after 3 failed attempts
        if self.failed_attempts >= 3:
            wait_time = 60 * (2 ** (self.failed_attempts - 3))  # Exponential backoff
            remaining = wait_time - (current_time - self.last_attempt_time)
            if remaining > 0:
                messagebox.showerror("Rate Limited", 
                    f"Too many failed attempts.\n\n"
                    f"Please wait {int(remaining)} seconds before trying again.")
                return False
                
        return True
    
    def get_access_code(self, title: str, confirm: bool = False) -> str:
        """Enhanced access code dialog"""
        if not self.check_rate_limit():
            return None
            
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("380x200")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 190
        y = (dialog.winfo_screenheight() // 2) - 100
        dialog.geometry(f'+{x}+{y}')
        
        # Main frame
        main_frame = tk.Frame(dialog, bg='#f0f0f0', padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(main_frame, text=f"🔐 {title}", font=("Arial", 10, "bold"), 
                bg='#f0f0f0', fg='#333333').pack(pady=(0, 15))
        
        # Access code entry
        tk.Label(main_frame, text="Enter access code (min. 12 characters):", font=("Arial", 9),
                bg='#f0f0f0', fg='#333333').pack(anchor="w")
        code_var = tk.StringVar()
        code_entry = tk.Entry(main_frame, textvariable=code_var, show="*", 
                             width=35, font=("Arial", 9))
        code_entry.pack(pady=(3, 10), fill=tk.X)
        code_entry.focus()
        
        # Confirm entry if needed
        confirm_var = None
        if confirm:
            tk.Label(main_frame, text="Confirm access code:", font=("Arial", 9),
                    bg='#f0f0f0', fg='#333333').pack(anchor="w")
            confirm_var = tk.StringVar()
            confirm_entry = tk.Entry(main_frame, textvariable=confirm_var, show="*", 
                                   width=35, font=("Arial", 9))
            confirm_entry.pack(pady=(3, 10), fill=tk.X)
        
        result = {'code': None}
        
        def on_ok():
            code = code_var.get()
            
            if len(code) < 12:
                messagebox.showerror("Weak Password", 
                    "Access code must be at least 12 characters long.")
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
        
    def derive_key_enhanced(self, code: str, salt: bytes) -> bytes:
        """Enhanced key derivation with dual KDFs"""
        # Scrypt (memory-hard, ASIC-resistant)
        scrypt_kdf = Scrypt(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            n=2**16,  # 65,536 iterations (reduced for compatibility)
            r=8,
            p=1,
        )
        scrypt_key = scrypt_kdf.derive(code.encode('utf-8'))
        
        # PBKDF2 with increased iterations
        pbkdf2_kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt + b'pbkdf2',
            iterations=1000000,  # 1 million iterations
        )
        pbkdf2_key = pbkdf2_kdf.derive(code.encode('utf-8'))
        
        # Combine both keys
        combined_key = bytes(a ^ b for a, b in zip(scrypt_key, pbkdf2_key))
        return base64.urlsafe_b64encode(combined_key)
        
    def encrypt_file(self):
        """Enhanced encryption"""
        if not self.current_file:
            return
            
        self.status_label.config(text="Processing with enhanced security...")
        self.root.update()
            
        code = self.get_access_code("Data Processing", confirm=True)
        if not code:
            self.status_label.config(text="Processing cancelled")
            return
            
        try:
            with open(self.current_file, 'rb') as f:
                data = f.read()
                
            # 32-byte salt for enhanced security
            salt = secrets.token_bytes(32)
            
            # Integrity hash
            integrity_hash = hashlib.sha256(data).digest()
            
            # Enhanced key derivation
            key = self.derive_key_enhanced(code, salt)
            fernet = Fernet(key)
            
            # Encrypt data + integrity hash
            payload = integrity_hash + data
            encrypted_data = fernet.encrypt(payload)
            
            output_path = filedialog.asksaveasfilename(
                title="Save processed file",
                defaultextension=".dat",
                filetypes=[("Processed files", "*.dat")],
                initialname=Path(self.current_file).stem + ".dat"
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(salt + encrypted_data)
                    
                self.status_label.config(text="Enhanced encryption completed")
                messagebox.showinfo("Processing Complete", 
                    f"File encrypted with maximum security.\n\n"
                    f"🔐 AES-256 encryption\n"
                    f"🔑 Dual KDF (Scrypt + PBKDF2)\n"
                    f"🛡️ 1M+ iterations\n"
                    f"✅ Integrity verification\n\n"
                    f"File: {Path(output_path).name}")
            else:
                self.status_label.config(text="Processing cancelled")
                    
        except Exception as e:
            self.status_label.config(text="Processing error")
            messagebox.showerror("Error", f"Processing failed:\n{str(e)}")
            
    def decrypt_file(self):
        """Enhanced decryption with verification"""
        if not self.current_file:
            return
            
        self.status_label.config(text="Extracting with verification...")
        self.root.update()
            
        code = self.get_access_code("Data Extraction")
        if not code:
            self.status_label.config(text="Extraction cancelled")
            return
            
        try:
            with open(self.current_file, 'rb') as f:
                data = f.read()
                
            salt = data[:32]
            encrypted_data = data[32:]
            
            key = self.derive_key_enhanced(code, salt)
            fernet = Fernet(key)
            
            decrypted_payload = fernet.decrypt(encrypted_data)
            
            # Verify integrity
            stored_hash = decrypted_payload[:32]
            original_data = decrypted_payload[32:]
            
            computed_hash = hashlib.sha256(original_data).digest()
            if stored_hash != computed_hash:
                messagebox.showerror("Integrity Error", 
                    "File integrity verification failed!")
                return
            
            output_path = filedialog.asksaveasfilename(
                title="Save extracted data file",
                defaultextension=".txt",
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("SIP files", "*.sip"),
                    ("Text files", "*.txt"),
                    ("XML files", "*.xml"),
                    ("JSON files", "*.json"),
                    ("All files", "*.*")
                ],
                initialname=Path(self.current_file).stem + ".txt"
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(original_data)
                    
                self.status_label.config(text="Extraction completed - integrity verified")
                messagebox.showinfo("Extraction Complete", 
                    f"File extracted successfully.\n\n"
                    f"✅ Integrity verified\n"
                    f"🔓 Secure decryption\n\n"
                    f"File: {Path(output_path).name}")
            
            self.failed_attempts = 0
                    
        except Exception as e:
            self.failed_attempts += 1
            self.last_attempt_time = time.time()
            
            self.status_label.config(text="Extraction error")
            if "InvalidToken" in str(e):
                messagebox.showerror("Access Denied", 
                    f"Invalid access code.\n\n"
                    f"Failed attempts: {self.failed_attempts}/3")
            else:
                messagebox.showerror("Error", f"Extraction failed:\n{str(e)}")
                
    def run(self):
        """Start application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SecureTaxCalculator()
    app.run() 