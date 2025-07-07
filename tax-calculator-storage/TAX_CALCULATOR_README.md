# Tax Calculator Storage v2.1

## Overview

Tax Calculator Storage is a data processing utility designed for secure handling of CSV files containing tax calculation data. This application provides basic file processing capabilities with access code protection.

## Features

- Multi-format data file processing and storage
- Data extraction from processed files
- Access code protection for data security
- Simple file management interface
- Compatible with CSV, SIP, TXT, XML, JSON and other formats

## System Requirements

- Windows 10/11, macOS 10.14+, or Linux
- Python 3.8+ (for source version)
- 50MB available disk space

## Installation

### Option 1: Standalone Executable (Recommended)

1. Download `TaxCalculatorStorage.exe` (Windows) or `TaxCalculatorStorage.app` (macOS)
2. Double-click to run - no installation required

### Option 2: Python Source

```bash
# Install dependencies
pip install cryptography

# Run application
python3 tax_calculator.py
```

### Option 3: Build from Source

```bash
# Run build script
python3 build_tax_calculator.py
```

## Usage

### Processing Data Files

1. Click "Browse Data File" to select input file (CSV, SIP, TXT, XML, JSON, etc.)
2. Click "Process Data" button
3. Enter access code (required for data extraction)
4. Confirm access code
5. Choose location to save processed file (.dat format)

### Extracting Processed Files

1. Click "Browse Processed File" to select .dat file
2. Click "Extract Data" button
3. Enter access code used during processing
4. Choose location to save extracted file (original format preserved)

## File Formats

- **Input**: CSV (.csv), SIP (.sip), Text (.txt), XML (.xml), JSON (.json), Data (.dat)
- **Processed**: Encrypted data files (.dat)
- **Output**: Original format preserved (CSV, SIP, TXT, XML, JSON, etc.)

## Security

- Access code protection using PBKDF2 key derivation
- 256-bit encryption for processed files
- Local processing only - no network connections
- Access code is required for data extraction

## Important Notes

- Access codes are case-sensitive
- Lost access codes cannot be recovered
- Processed files cannot be opened without correct access code
- Keep access codes secure and separate from processed files

## Technical Specifications

- Encryption: Fernet (symmetric encryption)
- Key Derivation: PBKDF2 with SHA256
- Salt Length: 16 bytes
- Iterations: 100,000

## Support

For technical issues, verify:
1. File permissions are correct
2. Access code is entered correctly
3. Input file is in supported format (CSV, SIP, TXT, XML, JSON)
4. Sufficient disk space available

## Version History

- v2.1: Current release with improved interface
- v2.0: Added access code confirmation
- v1.0: Initial release

## License

This software is provided as-is for data processing purposes. Use in accordance with applicable data protection regulations. 