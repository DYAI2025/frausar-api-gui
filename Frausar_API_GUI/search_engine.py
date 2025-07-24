#!/usr/bin/env python3
"""
SEARCH ENGINE
=============

Intelligente Such-Engine für Marker-Filtering
- Live-Suche mit Fuzzy-Matching
- Icon-basierte Filterung
- Performance-optimierte Suche
"""

import re
import time
from typing import List, Dict, Any, Optional, Tuple
from difflib import SequenceMatcher
from collections import defaultdict


class FuzzyMatcher:
    """Fuzzy-Matching für bessere Suchergebnisse."""
    
    def __init__(self, threshold: float = 0.6):
        """Initialisiert den FuzzyMatcher."""
        self.threshold = threshold
    
    def similarity(self, a: str, b: str) -> float:
        """Berechnet die Ähnlichkeit zwischen zwei Strings."""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def fuzzy_match(self, query: str, text: str) -> bool:
        """Prüft ob ein Text fuzzy zum Query passt."""
        if not query or not text:
            return False
        
        # Exakte Teilstring-Suche (schneller)
        if query.lower() in text.lower():
            return True
        
        # Fuzzy-Matching für ähnliche Wörter
        words_query = query.lower().split()
        words_text = text.lower().split()
        
        for word_query in words_query:
            for word_text in words_text:
                if self.similarity(word_query, word_text) >= self.threshold:
                    return True
        
        return False


class FilterManager:
    """Verwaltet verschiedene Filter-Typen."""
    
    def __init__(self):
        """Initialisiert den FilterManager."""
        self.active_filters = {}
        self.filter_history = []
    
    def add_filter(self, filter_type: str, value: Any) -> None:
        """Fügt einen Filter hinzu."""
        self.active_filters[filter_type] = value
        self.filter_history.append((filter_type, value, time.time()))
    
    def remove_filter(self, filter_type: str) -> None:
        """Entfernt einen Filter."""
        if filter_type in self.active_filters:
            del self.active_filters[filter_type]
    
    def clear_all_filters(self) -> None:
        """Löscht alle Filter."""
        self.active_filters.clear()
    
    def get_active_filters(self) -> Dict[str, Any]:
        """Gibt alle aktiven Filter zurück."""
        return self.active_filters.copy()
    
    def get_filter_summary(self) -> str:
        """Erstellt eine Zusammenfassung der aktiven Filter."""
        if not self.active_filters:
            return "Keine Filter aktiv"
        
        parts = []
        for filter_type, value in self.active_filters.items():
            parts.append(f"{filter_type}: {value}")
        
        return " | ".join(parts)


class SearchEngine:
    """Hauptklasse für die Such-Engine."""
    
    def __init__(self, fuzzy_threshold: float = 0.6):
        """Initialisiert die SearchEngine."""
        self.fuzzy_matcher = FuzzyMatcher(fuzzy_threshold)
        self.filter_manager = FilterManager()
        self.search_cache = {}
        self.last_search_time = 0
        self.cache_timeout = 5.0  # 5 Sekunden Cache
    
    def live_search(self, query: str, markers: List[Dict[str, Any]], 
                   use_fuzzy: bool = True) -> List[Dict[str, Any]]:
        """Führt eine Live-Suche durch."""
        start_time = time.time()
        
        # Cache-Check
        cache_key = f"{query}_{len(markers)}_{use_fuzzy}"
        if (cache_key in self.search_cache and 
            time.time() - self.last_search_time < self.cache_timeout):
            return self.search_cache[cache_key]
        
        if not query.strip():
            # Leere Suche - alle Marker zurückgeben
            result = markers
        else:
            # Suche durchführen
            result = self._perform_search(query, markers, use_fuzzy)
        
        # Cache aktualisieren
        self.search_cache[cache_key] = result
        self.last_search_time = time.time()
        
        search_time = time.time() - start_time
        print(f"Suche abgeschlossen in {search_time:.3f}s - {len(result)} Ergebnisse")
        
        return result
    
    def _perform_search(self, query: str, markers: List[Dict[str, Any]], 
                       use_fuzzy: bool) -> List[Dict[str, Any]]:
        """Führt die eigentliche Suche durch."""
        results = []
        query_lower = query.lower()
        
        for marker in markers:
            score = 0
            matched_fields = []
            
            # ID-Suche (höchste Priorität)
            if 'id' in marker:
                id_str = str(marker['id']).lower()
                if query_lower in id_str:
                    score += 10
                    matched_fields.append('id')
                elif use_fuzzy and self.fuzzy_matcher.fuzzy_match(query, id_str):
                    score += 8
                    matched_fields.append('id')
            
            # Beschreibung-Suche
            if 'description' in marker:
                desc_str = str(marker['description']).lower()
                if query_lower in desc_str:
                    score += 5
                    matched_fields.append('description')
                elif use_fuzzy and self.fuzzy_matcher.fuzzy_match(query, desc_str):
                    score += 3
                    matched_fields.append('description')
            
            # Kategorie-Suche
            if 'category' in marker:
                cat_str = str(marker['category']).lower()
                if query_lower in cat_str:
                    score += 3
                    matched_fields.append('category')
                elif use_fuzzy and self.fuzzy_matcher.fuzzy_match(query, cat_str):
                    score += 2
                    matched_fields.append('category')
            
            # Beispiele-Suche
            if 'examples' in marker and isinstance(marker['examples'], list):
                for example in marker['examples']:
                    example_str = str(example).lower()
                    if query_lower in example_str:
                        score += 2
                        matched_fields.append('examples')
                        break
                    elif use_fuzzy and self.fuzzy_matcher.fuzzy_match(query, example_str):
                        score += 1
                        matched_fields.append('examples')
                        break
            
            # Nur Marker mit Treffern hinzufügen
            if score > 0:
                marker_copy = marker.copy()
                marker_copy['_search_score'] = score
                marker_copy['_matched_fields'] = matched_fields
                results.append(marker_copy)
        
        # Nach Relevanz sortieren
        results.sort(key=lambda x: x.get('_search_score', 0), reverse=True)
        
        return results
    
    def apply_filters(self, markers: List[Dict[str, Any]], 
                     filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Wendet Filter auf Marker an."""
        filtered_markers = markers
        
        for filter_type, filter_value in filters.items():
            if not filter_value:  # Leere Filter ignorieren
                continue
            
            if filter_type == 'category':
                filtered_markers = [
                    m for m in filtered_markers
                    if m.get('category', '').lower() == filter_value.lower()
                ]
            
            elif filter_type == 'format':
                filtered_markers = [
                    m for m in filtered_markers
                    if m.get('format', '').lower() == filter_value.lower()
                ]
            
            elif filter_type == 'level':
                if isinstance(filter_value, (int, str)):
                    try:
                        level = int(filter_value)
                        filtered_markers = [
                            m for m in filtered_markers
                            if m.get('level', 0) == level
                        ]
                    except ValueError:
                        pass
            
            elif filter_type == 'error_only':
                if filter_value:
                    filtered_markers = [
                        m for m in filtered_markers
                        if 'error' in m
                    ]
                else:
                    filtered_markers = [
                        m for m in filtered_markers
                        if 'error' not in m
                    ]
            
            elif filter_type == 'min_level':
                try:
                    min_level = int(filter_value)
                    filtered_markers = [
                        m for m in filtered_markers
                        if m.get('level', 0) >= min_level
                    ]
                except ValueError:
                    pass
            
            elif filter_type == 'max_level':
                try:
                    max_level = int(filter_value)
                    filtered_markers = [
                        m for m in filtered_markers
                        if m.get('level', 0) <= max_level
                    ]
                except ValueError:
                    pass
        
        return filtered_markers
    
    def get_search_statistics(self, markers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Erstellt Statistiken für die Marker-Liste."""
        stats = {
            'total_markers': len(markers),
            'categories': defaultdict(int),
            'formats': defaultdict(int),
            'levels': defaultdict(int),
            'error_markers': 0,
            'valid_markers': 0
        }
        
        for marker in markers:
            # Kategorien zählen
            category = marker.get('category', 'unknown')
            stats['categories'][category] += 1
            
            # Formate zählen
            format_type = marker.get('format', 'unknown')
            stats['formats'][format_type] += 1
            
            # Levels zählen
            level = marker.get('level', 0)
            stats['levels'][level] += 1
            
            # Fehler-Marker zählen
            if 'error' in marker:
                stats['error_markers'] += 1
            else:
                stats['valid_markers'] += 1
        
        # Füge zusammengefasste Statistiken hinzu
        stats['unique_categories'] = len(stats['categories'])
        stats['unique_formats'] = len(stats['formats'])
        stats['unique_levels'] = len(stats['levels'])
        
        return stats
    
    def get_search_suggestions(self, query: str, markers: List[Dict[str, Any]]) -> List[str]:
        """Generiert Suchvorschläge basierend auf der Query."""
        suggestions = set()
        
        if not query.strip():
            return list(suggestions)
        
        query_lower = query.lower()
        
        for marker in markers:
            # ID-Vorschläge
            if 'id' in marker:
                id_str = str(marker['id'])
                if query_lower in id_str.lower():
                    suggestions.add(id_str)
            
            # Kategorie-Vorschläge
            if 'category' in marker:
                cat_str = str(marker['category'])
                if query_lower in cat_str.lower():
                    suggestions.add(cat_str)
            
            # Beschreibung-Vorschläge (erste Wörter)
            if 'description' in marker:
                desc_str = str(marker['description'])
                words = desc_str.split()[:3]  # Erste 3 Wörter
                for word in words:
                    if query_lower in word.lower():
                        suggestions.add(word)
        
        # Sortieren und limitieren
        sorted_suggestions = sorted(suggestions, key=lambda x: len(x))
        return sorted_suggestions[:10]  # Maximal 10 Vorschläge
    
    def clear_cache(self) -> None:
        """Löscht den Such-Cache."""
        self.search_cache.clear()
        self.last_search_time = 0
    
    def get_performance_info(self) -> Dict[str, Any]:
        """Gibt Performance-Informationen zurück."""
        return {
            'cache_size': len(self.search_cache),
            'cache_timeout': self.cache_timeout,
            'last_search_time': self.last_search_time,
            'fuzzy_threshold': self.fuzzy_matcher.threshold
        }


# Test-Funktion
def test_search_engine():
    """Testet die SearchEngine."""
    engine = SearchEngine()
    
    # Test-Marker
    test_markers = [
        {
            'id': 'TEST_MARKER_1',
            'description': 'Ein Test-Marker für die Suche',
            'category': 'test',
            'level': 1,
            'format': 'txt'
        },
        {
            'id': 'PRODUCTION_MARKER',
            'description': 'Ein Produktions-Marker',
            'category': 'production',
            'level': 2,
            'format': 'yaml'
        },
        {
            'id': 'ERROR_MARKER',
            'description': 'Ein fehlerhafter Marker',
            'category': 'error',
            'level': 1,
            'format': 'json',
            'error': 'Syntax-Fehler'
        }
    ]
    
    # Test-Suche
    results = engine.live_search('test', test_markers)
    print(f"Suche nach 'test': {len(results)} Ergebnisse")
    
    # Test-Filterung
    filters = {'category': 'test'}
    filtered = engine.apply_filters(test_markers, filters)
    print(f"Filter nach Kategorie 'test': {len(filtered)} Ergebnisse")
    
    # Test-Statistiken
    stats = engine.get_search_statistics(test_markers)
    print(f"Statistiken: {stats}")


if __name__ == "__main__":
    test_search_engine() 