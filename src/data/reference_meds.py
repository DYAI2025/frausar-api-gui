"""
Referenz-Medikamentenliste für Normalisierung und Mapping
"""

import re
from typing import Dict, List, Tuple, Optional

# Referenz-Medikamentenliste mit Standardnamen, Abkürzungen und Kategorien
REFERENCE_MEDICATIONS = {
    # Schmerzmittel
    "Tramadol 225mg": {
        "category": "Schmerzmittel",
        "abbreviations": ["trama", "tram", "tramadol", "trama 225"],
        "dosage_variants": ["225mg", "225"],
        "price_per_unit": 0.0  # Wird später befüllt
    },
    "Tramadol 50mg": {
        "category": "Schmerzmittel", 
        "abbreviations": ["trama 50", "tram 50", "tramadol 50"],
        "dosage_variants": ["50mg", "50"],
        "price_per_unit": 0.0
    },
    "Ibuprofen 400mg": {
        "category": "Schmerzmittel",
        "abbreviations": ["ibu", "ibuprofen", "ibu 400"],
        "dosage_variants": ["400mg", "400"],
        "price_per_unit": 0.0
    },
    
    # Sedativa/Anxiolytika
    "Xanax bars 3mg": {
        "category": "Sedativa",
        "abbreviations": ["xanax", "xanax 3", "xanax bar", "alprazolam"],
        "dosage_variants": ["3mg", "3"],
        "price_per_unit": 0.0
    },
    "Alprazolam 1mg": {
        "category": "Sedativa",
        "abbreviations": ["alpra", "alp", "alprazolam 1"],
        "dosage_variants": ["1mg", "1"],
        "price_per_unit": 0.0
    },
    "Zopiclon 7.5mg": {
        "category": "Sedativa",
        "abbreviations": ["zopi", "zopic", "zopiclon"],
        "dosage_variants": ["7.5mg", "7.5"],
        "price_per_unit": 0.0
    },
    
    # Stimulanzien
    "Methylphenidate 10mg": {
        "category": "Stimulanzien",
        "abbreviations": ["methyl", "mph", "methylphenidate", "ritalin"],
        "dosage_variants": ["10mg", "10"],
        "price_per_unit": 0.0
    },
    "Methylphenidate 20mg": {
        "category": "Stimulanzien",
        "abbreviations": ["methyl 20", "mph 20", "methylphenidate 20", "ritalin 20"],
        "dosage_variants": ["20mg", "20"],
        "price_per_unit": 0.0
    },
    
    # Weitere häufige Medikamente
    "Paracetamol 500mg": {
        "category": "Schmerzmittel",
        "abbreviations": ["para", "paracetamol", "para 500"],
        "dosage_variants": ["500mg", "500"],
        "price_per_unit": 0.0
    },
    "Aspirin 100mg": {
        "category": "Schmerzmittel",
        "abbreviations": ["aspirin", "asp", "acetylsalicylsäure"],
        "dosage_variants": ["100mg", "100"],
        "price_per_unit": 0.0
    }
}

# Kompilierte Regex-Pattern für bessere Performance
DOSAGE_PATTERNS = [
    re.compile(r'(\d+(?:\.\d+)?)\s*mg', re.IGNORECASE),
    re.compile(r'(\d+(?:\.\d+)?)\s*ml', re.IGNORECASE),
    re.compile(r'(\d+(?:\.\d+)?)\s*g', re.IGNORECASE),
    re.compile(r'(\d+(?:\.\d+)?)\s*units?', re.IGNORECASE)
]

QUANTITY_PATTERNS = [
    re.compile(r'(\d+)\s*x', re.IGNORECASE),
    re.compile(r'(\d+)\s*stück', re.IGNORECASE),
    re.compile(r'(\d+)\s*tablets?', re.IGNORECASE),
    re.compile(r'(\d+)\s*pills?', re.IGNORECASE)
]

def load_reference_data() -> Dict:
    """
    Lädt die Referenz-Medikamentenliste
    
    Returns:
        Dict: Referenz-Medikamentendaten
    """
    return REFERENCE_MEDICATIONS

def get_medication_by_abbreviation(abbreviation: str) -> Optional[str]:
    """
    Findet Medikament anhand von Abkürzung
    
    Args:
        abbreviation: Abkürzung oder Teilname
        
    Returns:
        Optional[str]: Vollständiger Medikamentenname oder None
    """
    abbreviation_lower = abbreviation.lower().strip()
    
    for medication, data in REFERENCE_MEDICATIONS.items():
        # Exakte Übereinstimmung mit Abkürzungen
        for abbrev in data["abbreviations"]:
            if abbreviation_lower == abbrev.lower():
                return medication
        
        # Teilstring-Matching für flexible Erkennung
        for abbrev in data["abbreviations"]:
            if abbreviation_lower in abbrev.lower() or abbrev.lower() in abbreviation_lower:
                return medication
                
    return None

def extract_dosage_from_text(text: str) -> Optional[str]:
    """
    Extrahiert Dosage-Information aus Text
    
    Args:
        text: Input-Text
        
    Returns:
        Optional[str]: Extrahierte Dosage oder None
    """
    for pattern in DOSAGE_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0)
    return None

def extract_quantity_from_text(text: str) -> Optional[int]:
    """
    Extrahiert Mengen-Information aus Text
    
    Args:
        text: Input-Text
        
    Returns:
        Optional[int]: Extrahierte Menge oder None
    """
    for pattern in QUANTITY_PATTERNS:
        match = pattern.search(text)
        if match:
            return int(match.group(1))
    return None

def get_all_categories() -> List[str]:
    """
    Gibt alle verfügbaren Kategorien zurück
    
    Returns:
        List[str]: Liste aller Kategorien
    """
    return list(set(data["category"] for data in REFERENCE_MEDICATIONS.values()))

def get_medications_by_category(category: str) -> List[str]:
    """
    Gibt alle Medikamente einer Kategorie zurück
    
    Args:
        category: Kategorie-Name
        
    Returns:
        List[str]: Liste der Medikamente in der Kategorie
    """
    return [med for med, data in REFERENCE_MEDICATIONS.items() 
            if data["category"].lower() == category.lower()] 