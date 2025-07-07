# Tax Calculator Storage

A simple, secure data processing utility for tax-related calculations and file management.

## Overview

Tax Calculator Storage is a minimalist desktop application designed for secure handling of various data file formats. The application provides basic file processing capabilities with access code protection, making it suitable for sensitive data management.

## Features

- **Multi-format support**: CSV, SIP, TXT, XML, JSON, DAT files
- **Secure processing**: Strong encryption with access code protection
- **Format preservation**: Original file format maintained during extraction
- **Local processing**: No network connections required
- **Simple interface**: Clean, professional design
- **Cross-platform**: Windows, macOS, Linux support

## Installation

### Quick Start (Recommended)

1. Download the appropriate executable:
   - Windows: `TaxCalculatorStorage.exe`
   - macOS: `TaxCalculatorStorage.app`
2. Double-click to run - no installation required

### From Source

```bash
# Install dependencies
pip install cryptography

# Run application
python3 tax_calculator.py
```

### Build Standalone

```bash
# Run build script
python3 build_tax_calculator.py
```

## Usage

### Processing Files

1. Click **"Browse Data File"** to select input file
2. Choose from supported formats (CSV, SIP, TXT, XML, JSON, DAT)
3. Click **"Process Data"** button
4. Enter access code when prompted
5. Confirm access code
6. Choose location to save processed file (.dat format)

### Extracting Files

1. Click **"Browse Processed File"** to select .dat file
2. Click **"Extract Data"** button
3. Enter the access code used during processing
4. Choose location to save extracted file
5. Original format will be preserved

## File Formats

- **Input**: CSV (.csv), SIP (.sip), Text (.txt), XML (.xml), JSON (.json), Data (.dat)
- **Processed**: Encrypted data files (.dat)
- **Output**: Original format preserved

## Security Features

- **Encryption**: Fernet (AES 128 + HMAC SHA256)
- **Key Derivation**: PBKDF2 with SHA256 (100,000 iterations)
- **Local Processing**: No cloud connections
- **Access Protection**: Strong password-based encryption

## Test Files

Use the included test file creator to generate sample data:

```bash
python3 test_files_creator.py
```

This creates anonymized test files in various formats for testing purposes.

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8+ (for source version)
- **Disk Space**: 50MB available space
- **Memory**: 512MB RAM minimum

## Important Notes

- Access codes are case-sensitive
- Lost access codes cannot be recovered
- Processed files require the correct access code for extraction
- Keep access codes secure and separate from processed files
- All processing is performed locally

## Technical Specifications

- **Encryption Algorithm**: Fernet (symmetric encryption)
- **Key Derivation Function**: PBKDF2 with SHA256
- **Salt Length**: 16 bytes (randomly generated)
- **Key Derivation Iterations**: 100,000
- **Supported File Encodings**: UTF-8, Latin-1

## Troubleshooting

**File not recognized:**
- Ensure file is in supported format
- Check file permissions
- Verify file is not corrupted

**Processing failed:**
- Verify sufficient disk space
- Check file access permissions
- Ensure valid file format

**Extraction failed:**
- Verify correct access code
- Check processed file integrity
- Ensure sufficient disk space

## Privacy & Security

- No telemetry or data collection
- All processing performed locally
- No network connections required
- Test data is fully anonymized
- No personal information stored

## License

This software is provided as-is for data processing purposes. Use in accordance with applicable data protection regulations.

## Contributing

This project welcomes contributions. Please ensure all contributions maintain the privacy and security standards of the project.

---

*This application is designed for legitimate data processing purposes. Users are responsible for compliance with applicable laws and regulations.* 