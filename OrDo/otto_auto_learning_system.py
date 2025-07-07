#!/usr/bin/env python3
"""
🧠 OTTO AUTO LEARNING SYSTEM
============================================================
🎯 Automatisches Lern- und Verdichtungssystem für Otto
📝 Analysiert Jammeldateien und erkennt Muster
💎 Erstellt Kristalle aus verdichteten Erkenntnissen
⏰ Läuft automatisch alle 2 Stunden
============================================================
"""

import os
import json
import yaml
import glob
from datetime import datetime, timedelta
from typing import Dict, List, Any
import re
from collections import defaultdict
import logging

class OttoAutoLearningSystem:
    def __init__(self):
        self.jam_files_dir = "otto_jam_files"
        self.crystals_dir = "otto_crystals"
        self.markers_dir = "otto_markers"
        self.compression_logs_dir = "otto_compression_logs"
        self.clusters_dir = "otto_clusters"
        
        # Erstelle Ordner falls nicht vorhanden
        for dir_path in [self.jam_files_dir, self.crystals_dir, self.compression_logs_dir, self.clusters_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        self.setup_logging()
        
    def setup_logging(self):
        """Richtet Logging für das Lernsystem ein"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{self.compression_logs_dir}/otto_learning.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_markers(self) -> Dict[str, Any]:
        """Lädt alle verfügbaren Marker"""
        markers = {}
        
        # Lade Marker aus verschiedenen Quellen
        marker_sources = [
            f"{self.markers_dir}/*.yaml",
            f"{self.markers_dir}/*.json",
            "otto_subconscious/marker_processing/*.yaml"
        ]
        
        for pattern in marker_sources:
            for file_path in glob.glob(pattern):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if file_path.endswith('.yaml'):
                            marker_data = yaml.safe_load(f)
                        else:
                            marker_data = json.load(f)
                        
                        if marker_data:
                            markers[os.path.basename(file_path)] = marker_data
                            self.logger.info(f"Marker geladen: {file_path}")
                except Exception as e:
                    self.logger.warning(f"Fehler beim Laden von {file_path}: {e}")
        
        return markers
    
    def analyze_jam_files(self) -> List[Dict[str, Any]]:
        """Analysiert alle Jammeldateien und extrahiert Muster"""
        jam_entries = []
        
        # Lade alle Jammeldateien
        jam_patterns = [
            f"{self.jam_files_dir}/*.json",
            f"{self.jam_files_dir}/*.yaml",
            f"{self.jam_files_dir}/*.txt"
        ]
        
        for pattern in jam_patterns:
            for file_path in glob.glob(pattern):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if file_path.endswith('.json'):
                            data = json.load(f)
                        elif file_path.endswith('.yaml'):
                            data = yaml.safe_load(f)
                        else:
                            # Für .txt Dateien - einfache Textanalyse
                            content = f.read()
                            data = self.analyze_text_content(content)
                        
                        if data:
                            jam_entries.append({
                                'file': file_path,
                                'timestamp': datetime.now().isoformat(),
                                'data': data
                            })
                            
                except Exception as e:
                    self.logger.warning(f"Fehler beim Analysieren von {file_path}: {e}")
        
        return jam_entries
    
    def analyze_text_content(self, content: str) -> Dict[str, Any]:
        """Analysiert Textinhalt und extrahiert Muster"""
        analysis = {
            'word_count': len(content.split()),
            'sentences': len(re.split(r'[.!?]+', content)),
            'keywords': self.extract_keywords(content),
            'emotion_markers': self.detect_emotion_markers(content),
            'topic_clusters': self.identify_topic_clusters(content)
        }
        return analysis
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extrahiert wichtige Schlüsselwörter"""
        # Einfache Keyword-Extraktion
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = defaultdict(int)
        
        # Filtere häufige Wörter
        stop_words = {'der', 'die', 'das', 'und', 'in', 'zu', 'den', 'mit', 'sich', 'des', 'auf', 'für', 'ist', 'im', 'dem', 'nicht', 'ein', 'eine', 'auch', 'als', 'an', 'auch', 'auf', 'bei', 'seit', 'vom', 'zum', 'zur', 'über', 'unter', 'vor', 'hinter', 'neben', 'zwischen'}
        
        for word in words:
            if len(word) > 3 and word not in stop_words:
                word_freq[word] += 1
        
        # Top 10 Keywords
        return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    def detect_emotion_markers(self, text: str) -> Dict[str, int]:
        """Erkennt Emotionsmarker im Text"""
        emotion_patterns = {
            'freude': [r'\b(freut|glücklich|toll|super|großartig)\b'],
            'ärger': [r'\b(ärgert|wütend|frustriert|genervt)\b'],
            'trauer': [r'\b(traurig|trauert|traurig|deprimiert)\b'],
            'angst': [r'\b(ängstlich|fürchtet|sorgen|besorgt)\b'],
            'überraschung': [r'\b(überrascht|erstaunt|verblüfft)\b']
        }
        
        emotions = {}
        for emotion, patterns in emotion_patterns.items():
            count = 0
            for pattern in patterns:
                count += len(re.findall(pattern, text.lower()))
            if count > 0:
                emotions[emotion] = count
        
        return emotions
    
    def identify_topic_clusters(self, text: str) -> List[str]:
        """Identifiziert Themencluster"""
        topics = []
        
        # Einfache Themenerkennung basierend auf Schlüsselwörtern
        topic_keywords = {
            'technologie': ['computer', 'software', 'programm', 'code', 'system'],
            'arbeit': ['projekt', 'aufgabe', 'deadline', 'meeting', 'arbeit'],
            'beziehung': ['freund', 'partner', 'familie', 'liebe', 'beziehung'],
            'gesundheit': ['krank', 'arzt', 'medizin', 'gesund', 'wohlbefinden'],
            'finanzen': ['geld', 'kosten', 'preis', 'budget', 'finanzen']
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    topics.append(topic)
                    break
        
        return list(set(topics))
    
    def create_crystal(self, insights: Dict[str, Any]) -> str:
        """Erstellt einen neuen Kristall aus Erkenntnissen"""
        crystal_id = f"crystal_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        crystal_data = {
            'id': crystal_id,
            'created_at': datetime.now().isoformat(),
            'insights': insights,
            'type': 'auto_learning_crystal',
            'confidence': self.calculate_confidence(insights)
        }
        
        crystal_file = f"{self.crystals_dir}/{crystal_id}.json"
        with open(crystal_file, 'w', encoding='utf-8') as f:
            json.dump(crystal_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Neuer Kristall erstellt: {crystal_id}")
        return crystal_id
    
    def calculate_confidence(self, insights: Dict[str, Any]) -> float:
        """Berechnet Konfidenz für die Erkenntnisse"""
        # Einfache Konfidenz-Berechnung basierend auf Datenqualität
        confidence = 0.0
        
        if 'keywords' in insights and insights['keywords']:
            confidence += 0.3
        
        if 'emotion_markers' in insights and insights['emotion_markers']:
            confidence += 0.3
        
        if 'topic_clusters' in insights and insights['topic_clusters']:
            confidence += 0.4
        
        return min(confidence, 1.0)
    
    def compress_old_data(self) -> Dict[str, Any]:
        """Verdichtet alte Daten und erstellt Zusammenfassungen"""
        compression_stats = {
            'files_processed': 0,
            'crystals_created': 0,
            'clusters_identified': 0,
            'compression_ratio': 0.0
        }
        
        # Analysiere alle Jammeldateien
        jam_entries = self.analyze_jam_files()
        compression_stats['files_processed'] = len(jam_entries)
        
        if jam_entries:
            # Erstelle Kristalle aus den Erkenntnissen
            for entry in jam_entries:
                if 'data' in entry and entry['data']:
                    crystal_id = self.create_crystal(entry['data'])
                    compression_stats['crystals_created'] += 1
            
            # Identifiziere Cluster
            clusters = self.identify_clusters(jam_entries)
            compression_stats['clusters_identified'] = len(clusters)
            
            # Speichere Cluster
            self.save_clusters(clusters)
            
            # Berechne Komprimierungsrate
            if len(jam_entries) > 0:
                compression_stats['compression_ratio'] = len(clusters) / len(jam_entries)
        
        return compression_stats
    
    def identify_clusters(self, jam_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifiziert Cluster aus Jammeldateien"""
        clusters = []
        
        # Gruppiere nach Themen
        topic_groups = defaultdict(list)
        emotion_groups = defaultdict(list)
        
        for entry in jam_entries:
            if 'data' in entry and entry['data']:
                data = entry['data']
                
                # Gruppiere nach Themen
                if 'topic_clusters' in data:
                    for topic in data['topic_clusters']:
                        topic_groups[topic].append(entry)
                
                # Gruppiere nach Emotionen
                if 'emotion_markers' in data:
                    for emotion in data['emotion_markers']:
                        emotion_groups[emotion].append(entry)
        
        # Erstelle Cluster aus Gruppen
        for topic, entries in topic_groups.items():
            if len(entries) >= 2:  # Mindestens 2 Einträge für einen Cluster
                cluster = {
                    'id': f"cluster_topic_{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'type': 'topic',
                    'name': topic,
                    'entries': len(entries),
                    'created_at': datetime.now().isoformat(),
                    'confidence': len(entries) / len(jam_entries) if jam_entries else 0
                }
                clusters.append(cluster)
        
        for emotion, entries in emotion_groups.items():
            if len(entries) >= 2:
                cluster = {
                    'id': f"cluster_emotion_{emotion}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'type': 'emotion',
                    'name': emotion,
                    'entries': len(entries),
                    'created_at': datetime.now().isoformat(),
                    'confidence': len(entries) / len(jam_entries) if jam_entries else 0
                }
                clusters.append(cluster)
        
        return clusters
    
    def save_clusters(self, clusters: List[Dict[str, Any]]):
        """Speichert Cluster"""
        for cluster in clusters:
            cluster_file = f"{self.clusters_dir}/{cluster['id']}.json"
            with open(cluster_file, 'w', encoding='utf-8') as f:
                json.dump(cluster, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Cluster gespeichert: {cluster['id']}")
    
    def run_learning_cycle(self):
        """Führt einen kompletten Lernzyklus durch"""
        self.logger.info("🧠 Starte Otto Auto Learning Cycle...")
        
        try:
            # Lade Marker
            markers = self.load_markers()
            self.logger.info(f"📝 {len(markers)} Marker geladen")
            
            # Verdichte Daten
            compression_stats = self.compress_old_data()
            
            # Logge Ergebnisse
            self.logger.info(f"✅ Lernzyklus abgeschlossen:")
            self.logger.info(f"   📁 Dateien verarbeitet: {compression_stats['files_processed']}")
            self.logger.info(f"   💎 Kristalle erstellt: {compression_stats['crystals_created']}")
            self.logger.info(f"   🎯 Cluster identifiziert: {compression_stats['clusters_identified']}")
            self.logger.info(f"   📊 Komprimierungsrate: {compression_stats['compression_ratio']:.1%}")
            
            # Speichere Lernstatistik
            self.save_learning_stats(compression_stats)
            
        except Exception as e:
            self.logger.error(f"❌ Fehler im Lernzyklus: {e}")
    
    def save_learning_stats(self, stats: Dict[str, Any]):
        """Speichert Lernstatistiken"""
        stats_file = f"{self.compression_logs_dir}/learning_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

def main():
    """Hauptfunktion für das Auto Learning System"""
    print("🧠 OTTO AUTO LEARNING SYSTEM")
    print("=" * 60)
    print("🎯 Automatisches Lern- und Verdichtungssystem")
    print("📝 Analysiert Jammeldateien und erkennt Muster")
    print("💎 Erstellt Kristalle aus verdichteten Erkenntnissen")
    print("⏰ Läuft automatisch alle 2 Stunden")
    print("=" * 60)
    
    # Erstelle und starte das Lernsystem
    learning_system = OttoAutoLearningSystem()
    learning_system.run_learning_cycle()
    
    print("✅ Auto Learning System abgeschlossen!")

if __name__ == "__main__":
    main() 