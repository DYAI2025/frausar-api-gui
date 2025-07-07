#!/usr/bin/env python3
"""
Test Files Creator - Erstellt Struktur-Templates ohne vorausgefüllte Werte
ALLE DATEN ANONYMISIERT FÜR SICHERHEIT - NUR STRUKTUREN
"""

import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path

def create_test_csv():
    """Erstelle Test-CSV-Struktur ohne Werte"""
    data = [
        ["Name", "Age", "City", "Department"],
        ["[Name]", "[Age]", "[City]", "[Department]"],
        ["[Name]", "[Age]", "[City]", "[Department]"],
        ["[Name]", "[Age]", "[City]", "[Department]"]
    ]
    
    with open("test_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print("✅ test_data.csv erstellt (nur Struktur)")

def create_test_sip():
    """Erstelle Test-SIP-Struktur ohne echte Daten"""
    sip_content = """INVITE sip:[user]@[domain] SIP/2.0
Via: SIP/2.0/UDP [client].[domain]:5060;branch=z9hG4bK-[branch]
From: "[User A]" <sip:[usera]@[domain]>;tag=[tag]
To: "[User B]" <sip:[userb]@[domain]>
Call-ID: [callid]@[domain]
CSeq: 1 INVITE
Contact: <sip:[usera]@[client].[domain]:5060>
Content-Type: application/sdp
Content-Length: [length]

v=0
o=[user] [session] [version] IN IP4 [client].[domain]
s=[session description]
c=IN IP4 [client].[domain]
t=0 0
m=audio [port] RTP/AVP 0
a=rtpmap:0 PCMU/8000"""
    
    with open("test_session.sip", "w", encoding="utf-8") as f:
        f.write(sip_content)
    print("✅ test_session.sip erstellt (nur Struktur)")

def create_test_json():
    """Erstelle Test-JSON-Struktur ohne Werte"""
    data = {
        "users": [
            {
                "id": "[ID]",
                "name": "[Name]",
                "role": "[Role]",
                "department": "[Department]",
                "attributes": ["[Attribute1]", "[Attribute2]", "[Attribute3]"]
            },
            {
                "id": "[ID]",
                "name": "[Name]", 
                "role": "[Role]",
                "department": "[Department]",
                "attributes": ["[Attribute1]", "[Attribute2]", "[Attribute3]"]
            }
        ],
        "organization": "[Organization]",
        "location": "[Location]"
    }
    
    with open("test_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("✅ test_data.json erstellt (nur Struktur)")

def create_test_xml():
    """Erstelle Test-XML-Struktur ohne Werte"""
    root = ET.Element("organization")
    
    # Organization info
    ET.SubElement(root, "name").text = "[Organization Name]"
    ET.SubElement(root, "location").text = "[Location]"
    
    # Users
    users = ET.SubElement(root, "users")
    
    user1 = ET.SubElement(users, "user", id="[ID1]")
    ET.SubElement(user1, "name").text = "[Name]"
    ET.SubElement(user1, "role").text = "[Role]"
    ET.SubElement(user1, "department").text = "[Department]"
    
    user2 = ET.SubElement(users, "user", id="[ID2]")
    ET.SubElement(user2, "name").text = "[Name]"
    ET.SubElement(user2, "role").text = "[Role]"
    ET.SubElement(user2, "department").text = "[Department]"
    
    tree = ET.ElementTree(root)
    tree.write("test_data.xml", encoding="utf-8", xml_declaration=True)
    print("✅ test_data.xml erstellt (nur Struktur)")

def create_test_txt():
    """Erstelle Test-TXT-Struktur ohne Werte"""
    content = """Data Report Template
====================

User Information:
- [Name], [Role], [Department]
- [Name], [Role], [Department]  
- [Name], [Role], [Department]

Summary:
Total users: [Count]
Primary location: [Location]
Department: [Department Name]

Notes:
[Additional information]
[Status updates]
"""
    
    with open("test_report.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ test_report.txt erstellt (nur Struktur)")

def create_test_dat():
    """Erstelle Test-DAT-Struktur ohne Werte"""
    content = """# Configuration Template
SERVER_IP=[IP_ADDRESS]
SERVER_PORT=[PORT]
DATABASE_NAME=[DB_NAME]
USERNAME=[USERNAME]
PASSWORD=[PASSWORD]
MAX_CONNECTIONS=[NUMBER]
TIMEOUT=[SECONDS]
DEBUG_MODE=[TRUE/FALSE]
LOG_LEVEL=[LEVEL]
"""
    
    with open("test_config.dat", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ test_config.dat erstellt (nur Struktur)")

def main():
    """Erstelle alle Test-Strukturen ohne Werte"""
    print("🔧 Erstelle Struktur-Templates für Tax Calculator...")
    print("🔒 NUR STRUKTUREN - KEINE ECHTEN WERTE!")
    print()
    
    create_test_csv()
    create_test_sip()
    create_test_json()
    create_test_xml()
    create_test_txt()
    create_test_dat()
    
    print()
    print("✅ Alle Struktur-Templates erstellt!")
    print("📁 Verfügbare Dateien:")
    
    test_files = [
        "test_data.csv",
        "test_session.sip", 
        "test_data.json",
        "test_data.xml",
        "test_report.txt",
        "test_config.dat"
    ]
    
    for file in test_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"   • {file} ({size} bytes)")
    
    print()
    print("💡 Diese Struktur-Templates können Sie mit Tax Calculator Storage testen:")
    print("   1. Laden Sie eine Template-Datei in Tax Calculator")
    print("   2. Verschlüsseln Sie sie mit einem Passwort")
    print("   3. Testen Sie die Entschlüsselung")
    print()
    print("🔒 SICHERHEIT: Nur Strukturen, keine echten Daten!")

if __name__ == "__main__":
    main() 