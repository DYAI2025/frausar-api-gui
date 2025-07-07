# CSV Tresor App

A simple, secure CSV file encryption utility with password protection.

## Overview

CSV Tresor App is a lightweight desktop application designed for secure encryption and decryption of CSV files. The application provides an easy-to-use interface for protecting sensitive data with strong encryption.

## Features

- **Simple Interface**: Clean, professional design
- **CSV Encryption**: Secure file encryption with password protection
- **Strong Security**: PBKDF2 key derivation + Fernet 256-bit encryption
- **Local Processing**: No network connections required
- **Cross-platform**: Windows, macOS, Linux support

## Installation

### Quick Start (Recommended)

1. Download the appropriate executable:
   - Windows: `CSVTresor.exe`
   - macOS: `CSVTresor.app`
2. Double-click to run - no installation required

### From Source

```bash
# Install dependencies
pip install cryptography

# Run application
python3 csv_tresor.py
```

### Build Standalone

```bash
# Run build script
python3 build_csv_tresor.py
```

## Usage

### Encrypting Files

1. Click **"Browse CSV File"** to select input file
2. Click **"Encrypt File"** button
3. Enter password when prompted
4. Confirm password
5. Choose location to save encrypted file (.encrypted format)

### Decrypting Files

1. Click **"Browse Encrypted File"** to select .encrypted file
2. Click **"Decrypt File"** button
3. Enter the password used during encryption
4. Choose location to save decrypted CSV file

## Security Features

- **Encryption**: Fernet (AES 128 + HMAC SHA256)
- **Key Derivation**: PBKDF2 with SHA256 (100,000 iterations)
- **Local Processing**: No cloud connections
- **Password Protection**: Strong password-based encryption

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8+ (for source version)
- **Disk Space**: 20MB available space
- **Memory**: 256MB RAM minimum

## Important Notes

- Passwords are case-sensitive
- Lost passwords cannot be recovered
- Encrypted files require the correct password for decryption
- Keep passwords secure and separate from encrypted files
- All processing is performed locally

## Technical Specifications

- **Encryption Algorithm**: Fernet (symmetric encryption)
- **Key Derivation Function**: PBKDF2 with SHA256
- **Salt Length**: 16 bytes (randomly generated)
- **Key Derivation Iterations**: 100,000
- **Supported File Encodings**: UTF-8, Latin-1

## Privacy & Security

- No telemetry or data collection
- All processing performed locally
- No network connections required
- No personal information stored

## License

This software is provided as-is for data processing purposes. Use in accordance with applicable data protection regulations.

## Contributing

This project welcomes contributions. Please ensure all contributions maintain the privacy and security standards of the project.

---

*This application is designed for legitimate data protection purposes. Users are responsible for compliance with applicable laws and regulations.* 