#!/usr/bin/env python3
"""
Test-Skript für Frausar AI-Integration
======================================

Automatisierte Tests für die wichtigsten Funktionen der AI-Integration.
"""

import sys
import asyncio
import requests
import pandas as pd
from pathlib import Path
import time
import logging

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test-Konfiguration
BASE_URL = "http://localhost:8000"
TEST_TIMEOUT = 30  # Sekunden


class AIIntegrationTester:
    """Test-Klasse für die AI-Integration."""
    
    def __init__(self):
        self.test_results = []
        self.demo_file = Path("Frausar_API_GUI/data/demo_data.csv")
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Loggt ein Testergebnis."""
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
    
    def test_api_health(self):
        """Testet die API-Verfügbarkeit."""
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                self.log_test("API Health Check", True, "API ist erreichbar")
                return True
            else:
                self.log_test("API Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health Check", False, f"Fehler: {e}")
            return False
    
    def test_api_status(self):
        """Testet den API-Status-Endpunkt."""
        try:
            response = requests.get(f"{BASE_URL}/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                self.log_test("API Status", True, f"Status: {status['system_status']}")
                return True
            else:
                self.log_test("API Status", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Status", False, f"Fehler: {e}")
            return False
    
    def test_file_upload(self):
        """Testet den Datei-Upload."""
        try:
            if not self.demo_file.exists():
                self.log_test("File Upload", False, "Demo-Datei nicht gefunden")
                return None
            
            with open(self.demo_file, "rb") as f:
                files = {"file": f}
                response = requests.post(f"{BASE_URL}/upload", files=files, timeout=10)
            
            if response.status_code == 200:
                upload_data = response.json()
                filename = upload_data["filename"]
                self.log_test("File Upload", True, f"Datei hochgeladen: {filename}")
                return filename
            else:
                self.log_test("File Upload", False, f"Status: {response.status_code}")
                return None
        except Exception as e:
            self.log_test("File Upload", False, f"Fehler: {e}")
            return None
    
    def test_data_cleaning(self, filename: str):
        """Testet die Datenbereinigung."""
        try:
            clean_request = {"filename": filename}
            response = requests.post(f"{BASE_URL}/clean", json=clean_request, timeout=10)
            
            if response.status_code == 200:
                clean_data = response.json()
                self.log_test("Data Cleaning Start", True, f"Agent: {clean_data['agent_name']}")
                return True
            else:
                self.log_test("Data Cleaning Start", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Data Cleaning Start", False, f"Fehler: {e}")
            return False
    
    def test_agent_status(self):
        """Testet den Agenten-Status."""
        try:
            response = requests.get(f"{BASE_URL}/agent/data_cleaning/status", timeout=5)
            if response.status_code == 200:
                agent_status = response.json()
                self.log_test("Agent Status", True, f"Status: {agent_status['status']}")
                return True
            else:
                self.log_test("Agent Status", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Agent Status", False, f"Fehler: {e}")
            return False
    
    def test_result_retrieval(self):
        """Testet das Abrufen der Ergebnisse."""
        try:
            # Warten bis Verarbeitung abgeschlossen
            max_wait = 60  # Sekunden
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                response = requests.get(f"{BASE_URL}/result", timeout=5)
                if response.status_code == 200:
                    result_data = response.json()
                    self.log_test("Result Retrieval", True, 
                                f"Daten: {result_data['total_rows']} Zeilen, {result_data['total_columns']} Spalten")
                    return True
                elif response.status_code == 400:
                    # Noch nicht fertig, warten
                    time.sleep(2)
                    continue
                else:
                    self.log_test("Result Retrieval", False, f"Status: {response.status_code}")
                    return False
            
            self.log_test("Result Retrieval", False, "Timeout - Verarbeitung zu lang")
            return False
            
        except Exception as e:
            self.log_test("Result Retrieval", False, f"Fehler: {e}")
            return False
    
    def test_demo_data_integrity(self):
        """Testet die Integrität der Demo-Daten."""
        try:
            if not self.demo_file.exists():
                self.log_test("Demo Data Integrity", False, "Demo-Datei nicht gefunden")
                return False
            
            df = pd.read_csv(self.demo_file)
            
            # Grundlegende Checks
            if len(df) == 0:
                self.log_test("Demo Data Integrity", False, "Leere Datei")
                return False
            
            if len(df.columns) == 0:
                self.log_test("Demo Data Integrity", False, "Keine Spalten")
                return False
            
            # Spezifische Checks für unsere Demo-Daten
            expected_columns = ["Name", "Age", "Salary", "Department", "JoinDate", "Email", "Rating", "IsActive"]
            missing_columns = set(expected_columns) - set(df.columns)
            
            if missing_columns:
                self.log_test("Demo Data Integrity", False, f"Fehlende Spalten: {missing_columns}")
                return False
            
            self.log_test("Demo Data Integrity", True, f"Shape: {df.shape}, Spalten: {list(df.columns)}")
            return True
            
        except Exception as e:
            self.log_test("Demo Data Integrity", False, f"Fehler: {e}")
            return False
    
    def run_all_tests(self):
        """Führt alle Tests aus."""
        logger.info("="*60)
        logger.info("Starte Frausar AI-Integration Tests")
        logger.info("="*60)
        
        # 1. API-Verfügbarkeit testen
        if not self.test_api_health():
            logger.error("API nicht erreichbar - Tests abgebrochen")
            return False
        
        # 2. API-Status testen
        self.test_api_status()
        
        # 3. Demo-Daten integrität testen
        if not self.test_demo_data_integrity():
            logger.error("Demo-Daten fehlerhaft - Tests abgebrochen")
            return False
        
        # 4. Datei-Upload testen
        filename = self.test_file_upload()
        if not filename:
            logger.error("Upload fehlgeschlagen - Tests abgebrochen")
            return False
        
        # 5. Datenbereinigung starten
        if not self.test_data_cleaning(filename):
            logger.error("Datenbereinigung fehlgeschlagen - Tests abgebrochen")
            return False
        
        # 6. Agenten-Status testen
        self.test_agent_status()
        
        # 7. Ergebnisse abrufen
        self.test_result_retrieval()
        
        # Zusammenfassung
        self.print_summary()
        
        return True
    
    def print_summary(self):
        """Gibt eine Test-Zusammenfassung aus."""
        logger.info("="*60)
        logger.info("TEST-ZUSAMMENFASSUNG")
        logger.info("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        logger.info(f"Gesamt: {total_tests} Tests")
        logger.info(f"Bestanden: {passed_tests} Tests")
        logger.info(f"Fehlgeschlagen: {failed_tests} Tests")
        
        if failed_tests > 0:
            logger.info("\nFehlgeschlagene Tests:")
            for result in self.test_results:
                if not result["success"]:
                    logger.info(f"  - {result['test']}: {result['message']}")
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        logger.info(f"\nErfolgsrate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            logger.info("🎉 Tests erfolgreich abgeschlossen!")
        else:
            logger.error("❌ Tests zeigen Probleme auf")


def main():
    """Hauptfunktion für Tests."""
    try:
        tester = AIIntegrationTester()
        success = tester.run_all_tests()
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Tests durch Benutzer abgebrochen")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Kritischer Test-Fehler: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 