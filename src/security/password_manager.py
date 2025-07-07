"""
Passwort-Manager für Verschlüsselung von CSV-Dateien
"""

import os
import base64
from typing import Optional
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordManager:
    """
    Verwaltet Passwort-basierte Verschlüsselung für CSV-Dateien
    """
    
    def __init__(self):
        self.salt_length = 16
        self.iterations = 100000
    
    def _derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        """
        Leitet Verschlüsselungsschlüssel aus Passwort ab
        
        Args:
            password: User-Passwort
            salt: Salt für Key-Derivation
            
        Returns:
            bytes: Abgeleiteter Verschlüsselungsschlüssel
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_csv_file(self, csv_file_path: str, output_path: str, password: str) -> bool:
        """
        Verschlüsselt CSV-Datei mit Passwort
        
        Args:
            csv_file_path: Pfad zur Input-CSV
            output_path: Pfad für verschlüsselte Ausgabe
            password: Verschlüsselungspasswort
            
        Returns:
            bool: True wenn erfolgreich
        """
        try:
            # 1. CSV-Datei lesen
            with open(csv_file_path, 'rb') as file:
                csv_data = file.read()
            
            # 2. Salt generieren
            salt = os.urandom(self.salt_length)
            
            # 3. Schlüssel ableiten
            key = self._derive_key_from_password(password, salt)
            fernet = Fernet(key)
            
            # 4. Daten verschlüsseln
            encrypted_data = fernet.encrypt(csv_data)
            
            # 5. Salt + verschlüsselte Daten speichern
            with open(output_path, 'wb') as file:
                file.write(salt + encrypted_data)
            
            return True
            
        except Exception as e:
            print(f"Fehler bei der Verschlüsselung: {e}")
            return False
    
    def decrypt_csv_file(self, encrypted_file_path: str, output_path: str, password: str) -> bool:
        """
        Entschlüsselt passwortgeschützte CSV-Datei
        
        Args:
            encrypted_file_path: Pfad zur verschlüsselten Datei
            output_path: Pfad für entschlüsselte CSV
            password: Entschlüsselungspasswort
            
        Returns:
            bool: True wenn erfolgreich
        """
        try:
            # 1. Verschlüsselte Datei lesen
            with open(encrypted_file_path, 'rb') as file:
                encrypted_content = file.read()
            
            # 2. Salt extrahieren
            salt = encrypted_content[:self.salt_length]
            encrypted_data = encrypted_content[self.salt_length:]
            
            # 3. Schlüssel ableiten
            key = self._derive_key_from_password(password, salt)
            fernet = Fernet(key)
            
            # 4. Entschlüsseln
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # 5. CSV speichern
            with open(output_path, 'wb') as file:
                file.write(decrypted_data)
            
            return True
            
        except Exception as e:
            print(f"Fehler bei der Entschlüsselung: {e}")
            return False
    
    def validate_password(self, encrypted_file_path: str, password: str) -> bool:
        """
        Validiert Passwort gegen verschlüsselte Datei
        
        Args:
            encrypted_file_path: Pfad zur verschlüsselten Datei
            password: Zu validierendes Passwort
            
        Returns:
            bool: True wenn Passwort korrekt
        """
        try:
            with open(encrypted_file_path, 'rb') as file:
                encrypted_content = file.read()
            
            salt = encrypted_content[:self.salt_length]
            encrypted_data = encrypted_content[self.salt_length:]
            
            key = self._derive_key_from_password(password, salt)
            fernet = Fernet(key)
            
            # Versuche zu entschlüsseln (wirft Exception bei falschem Passwort)
            fernet.decrypt(encrypted_data)
            return True
            
        except:
            return False
    
    def get_file_info(self, encrypted_file_path: str) -> dict:
        """
        Gibt Informationen über verschlüsselte Datei zurück
        
        Args:
            encrypted_file_path: Pfad zur verschlüsselten Datei
            
        Returns:
            dict: Datei-Informationen
        """
        try:
            file_path = Path(encrypted_file_path)
            
            if not file_path.exists():
                return {'error': 'Datei nicht gefunden'}
            
            file_size = file_path.stat().st_size
            
            return {
                'file_path': str(file_path),
                'file_size_bytes': file_size,
                'file_size_kb': round(file_size / 1024, 2),
                'salt_length': self.salt_length,
                'encrypted_data_size': file_size - self.salt_length,
                'encryption_algorithm': 'Fernet (AES 128)',
                'key_derivation': f'PBKDF2-SHA256 ({self.iterations} iterations)'
            }
            
        except Exception as e:
            return {'error': str(e)}

# Convenience-Funktion für einfachen Zugriff
def encrypt_csv(csv_path: str, output_path: str, password: str) -> bool:
    """
    Convenience-Funktion für CSV-Verschlüsselung
    
    Args:
        csv_path: Pfad zur CSV-Datei
        output_path: Pfad für verschlüsselte Ausgabe
        password: Passwort
        
    Returns:
        bool: True wenn erfolgreich
    """
    manager = PasswordManager()
    return manager.encrypt_csv_file(csv_path, output_path, password) 