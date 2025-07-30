#!/usr/bin/env python3
"""
Semantischer Wächter & Beispiel-Generator (Lean-Deep 3.1)
=========================================================

Ein KI-getriebenes Tool für die MarkerEngine, das die semantische Integrität 
der Marker-Knowledge-Base schützt und hochwertige Beispiele generiert.

Epic-ID: EPIC-KB-002
Autor: Claude Opus 4.0
Version: 1.0.0
"""

import yaml
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarkerLevel(Enum):
    """Marker-Ebenen nach Lean-Deep 3.1"""
    ATOMIC = "A_"
    SEMANTIC = "S_"
    CLUSTER = "C_"
    META = "MM_"

class ValidationResult(Enum):
    """Validierungsergebnisse"""
    VALID = "valid"
    INVALID_SCHEMA = "invalid_schema"
    INVALID_SEMANTICS = "invalid_semantics"
    AMBIGUOUS_FRAME = "ambiguous_frame"

@dataclass
class FrameAnalysis:
    """Analyse-Ergebnis eines Marker-Frames"""
    is_clear: bool
    is_coherent: bool
    is_specific: bool
    clarity_score: float
    coherence_score: float
    specificity_score: float
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class ValidationReport:
    """Detaillierter Validierungsbericht"""
    result: ValidationResult
    marker_id: str
    frame_analysis: Optional[FrameAnalysis]
    schema_errors: List[str] = field(default_factory=list)
    semantic_errors: List[str] = field(default_factory=list)
    is_suitable_for_examples: bool = False
    confidence: float = 0.0

class SemanticGuardian:
    """
    Der Semantische Wächter - Stufe 1: Validierung & Eignungsprüfung
    
    Analysiert Marker-Frames auf Klarheit, Kohärenz und Spezifität.
    Entscheidet, ob ein Marker für die Beispiel-Generierung geeignet ist.
    """
    
    # Lean-Deep 3.1 Schema Definition
    REQUIRED_FIELDS = {
        "id": str,
        "frame": dict,
    }
    
    FRAME_FIELDS = {
        "signal": list,
        "concept": str, 
        "pragmatics": str,
        "narrative": str
    }
    
    STRUCTURE_FIELDS = ["pattern", "composed_of", "detect_class"]
    
    # Verbotene Legacy-Felder
    FORBIDDEN_FIELDS = {
        "level", "marker_name", "description", "category", 
        "name", "version", "author", "created_at", "status", "lang"
    }
    
    def __init__(self):
        """Initialisiert den Semantischen Wächter"""
        self.validation_stats = {
            "total_validated": 0,
            "valid_markers": 0,
            "schema_violations": 0,
            "semantic_issues": 0,
            "ambiguous_frames": 0
        }
    
    def validate_marker(self, marker_data: Dict[str, Any], marker_id: str = None) -> ValidationReport:
        """
        Vollständige Validierung eines Markers
        
        Args:
            marker_data: Der zu validierende Marker
            marker_id: Optional - Marker-ID für Logging
            
        Returns:
            ValidationReport mit detailliertem Ergebnis
        """
        self.validation_stats["total_validated"] += 1
        
        if not marker_id:
            marker_id = marker_data.get("id", "UNKNOWN")
        
        logger.info(f"🔍 Validiere Marker: {marker_id}")
        
        # Schritt 1: Schema-Validierung
        schema_errors = self._validate_schema(marker_data)
        if schema_errors:
            self.validation_stats["schema_violations"] += 1
            return ValidationReport(
                result=ValidationResult.INVALID_SCHEMA,
                marker_id=marker_id,
                frame_analysis=None,
                schema_errors=schema_errors,
                is_suitable_for_examples=False,
                confidence=0.0
            )
        
        # Schritt 2: Frame-Analyse
        frame_analysis = self._analyze_frame(marker_data["frame"], marker_id)
        
        # Schritt 3: Semantische Kohärenz
        semantic_errors = self._validate_semantics(marker_data, frame_analysis)
        
        # Entscheidung über Eignung
        is_suitable = self._determine_suitability(frame_analysis, semantic_errors)
        confidence = self._calculate_confidence(frame_analysis, semantic_errors)
        
        # Ergebnis bestimmen
        if semantic_errors:
            result = ValidationResult.INVALID_SEMANTICS
            self.validation_stats["semantic_issues"] += 1
        elif not frame_analysis.is_clear or not frame_analysis.is_coherent:
            result = ValidationResult.AMBIGUOUS_FRAME
            self.validation_stats["ambiguous_frames"] += 1
        else:
            result = ValidationResult.VALID
            self.validation_stats["valid_markers"] += 1
        
        return ValidationReport(
            result=result,
            marker_id=marker_id,
            frame_analysis=frame_analysis,
            schema_errors=schema_errors,
            semantic_errors=semantic_errors,
            is_suitable_for_examples=is_suitable,
            confidence=confidence
        )
    
    def _validate_schema(self, marker_data: Dict[str, Any]) -> List[str]:
        """
        Validiert die Einhaltung des Lean-Deep 3.1 Schemas
        
        Returns:
            Liste der Schema-Fehler
        """
        errors = []
        
        # Pflichtfelder prüfen
        for field, expected_type in self.REQUIRED_FIELDS.items():
            if field not in marker_data:
                errors.append(f"Fehlendes Pflichtfeld: {field}")
            elif not isinstance(marker_data[field], expected_type):
                errors.append(f"Falscher Typ für {field}: erwartet {expected_type.__name__}, erhalten {type(marker_data[field]).__name__}")
        
        # ID-Präfix validieren
        if "id" in marker_data:
            marker_id = marker_data["id"]
            valid_prefixes = [level.value for level in MarkerLevel]
            if not any(marker_id.startswith(prefix) for prefix in valid_prefixes):
                errors.append(f"Ungültiges ID-Präfix: {marker_id}. Erlaubt: {valid_prefixes}")
        
        # Frame-Struktur validieren
        if "frame" in marker_data:
            frame = marker_data["frame"]
            for field, expected_type in self.FRAME_FIELDS.items():
                if field not in frame:
                    errors.append(f"Fehlendes Frame-Feld: {field}")
                elif not isinstance(frame[field], expected_type):
                    errors.append(f"Falscher Typ für frame.{field}: erwartet {expected_type.__name__}")
        
        # Struktur-Block validieren (genau einer muss vorhanden sein)
        structure_fields_present = [field for field in self.STRUCTURE_FIELDS if field in marker_data]
        if len(structure_fields_present) != 1:
            errors.append(f"Genau ein Struktur-Feld erforderlich {self.STRUCTURE_FIELDS}, gefunden: {structure_fields_present}")
        
        # Verbotene Legacy-Felder prüfen
        forbidden_found = [field for field in self.FORBIDDEN_FIELDS if field in marker_data]
        if forbidden_found:
            errors.append(f"Verbotene Legacy-Felder gefunden: {forbidden_found}")
        
        return errors
    
    def _analyze_frame(self, frame: Dict[str, Any], marker_id: str) -> FrameAnalysis:
        """
        Tiefgreifende Analyse der Frame-Semantik
        
        Args:
            frame: Der vierdimensionale Frame
            marker_id: Marker-ID für Logging
            
        Returns:
            FrameAnalysis mit detaillierter Bewertung
        """
        logger.debug(f"📊 Analysiere Frame für {marker_id}")
        
        issues = []
        recommendations = []
        
        # Klarheit analysieren (Clarity)
        clarity_score = self._assess_clarity(frame, issues, recommendations)
        
        # Kohärenz analysieren (Coherence) 
        coherence_score = self._assess_coherence(frame, issues, recommendations)
        
        # Spezifität analysieren (Specificity)
        specificity_score = self._assess_specificity(frame, issues, recommendations)
        
        # Schwellenwerte für Eignung (realistischer angepasst)
        CLARITY_THRESHOLD = 0.6
        COHERENCE_THRESHOLD = 0.6
        SPECIFICITY_THRESHOLD = 0.4
        
        is_clear = clarity_score >= CLARITY_THRESHOLD
        is_coherent = coherence_score >= COHERENCE_THRESHOLD
        is_specific = specificity_score >= SPECIFICITY_THRESHOLD
        
        return FrameAnalysis(
            is_clear=is_clear,
            is_coherent=is_coherent,
            is_specific=is_specific,
            clarity_score=clarity_score,
            coherence_score=coherence_score,
            specificity_score=specificity_score,
            issues=issues,
            recommendations=recommendations
        )
    
    def _assess_clarity(self, frame: Dict[str, Any], issues: List[str], recommendations: List[str]) -> float:
        """Bewertet die Klarheit des Frames"""
        score = 1.0
        
        # Signal-Klarheit
        signals = frame.get("signal", [])
        if not signals:
            issues.append("Keine Signale definiert")
            score -= 0.3
        elif len(signals) < 2:
            issues.append("Zu wenige Signale für robuste Erkennung")
            recommendations.append("Mindestens 2-3 charakteristische Signale definieren")
            score -= 0.1
        
        # Prüfe auf vage Signale
        vague_indicators = ["etc", "usw", "...", "und so weiter", "ähnlich"]
        for signal in signals:
            if any(indicator in signal.lower() for indicator in vague_indicators):
                issues.append(f"Vages Signal: '{signal}'")
                score -= 0.1
        
        # Concept-Klarheit
        concept = frame.get("concept", "")
        if not concept:
            issues.append("Konzept nicht definiert")
            score -= 0.2
        elif len(concept.split()) > 3:
            issues.append("Konzept zu komplex (>3 Wörter)")
            recommendations.append("Konzept auf 1-3 präzise Begriffe reduzieren")
            score -= 0.1
        
        # Pragmatics-Klarheit
        pragmatics = frame.get("pragmatics", "")
        if not pragmatics:
            issues.append("Pragmatik nicht definiert")
            score -= 0.2
        
        # Narrative-Klarheit
        narrative = frame.get("narrative", "")
        if not narrative:
            issues.append("Narrativ nicht definiert")
            score -= 0.2
        
        return max(0.0, score)
    
    def _assess_coherence(self, frame: Dict[str, Any], issues: List[str], recommendations: List[str]) -> float:
        """Bewertet die Kohärenz zwischen Frame-Dimensionen"""
        score = 1.0
        
        # Kohärenz zwischen Signal und Concept
        signals = frame.get("signal", [])
        concept = frame.get("concept", "").lower()
        
        if signals and concept:
            # Prüfe semantische Verbindung
            concept_words = concept.split()
            signal_text = " ".join(signals).lower()
            
            # Einfache Überlappungs-Heuristik
            overlap = any(word in signal_text for word in concept_words if len(word) > 3)
            if not overlap:
                issues.append("Schwache Verbindung zwischen Signal und Concept")
                score -= 0.2
        
        # Kohärenz zwischen Pragmatics und Narrative
        pragmatics = frame.get("pragmatics", "").lower()
        narrative = frame.get("narrative", "").lower()
        
        # Narrative-Pragmatics Konsistenz
        narrative_pragmatic_conflicts = [
            ("offer", "aggression"), ("threat", "support"), 
            ("withdrawal", "engagement"), ("loop", "resolution")
        ]
        
        for narr, prag in narrative_pragmatic_conflicts:
            if narr in narrative and prag in pragmatics:
                issues.append(f"Konflikt: Narrativ '{narr}' vs Pragmatik '{prag}'")
                score -= 0.3
        
        return max(0.0, score)
    
    def _assess_specificity(self, frame: Dict[str, Any], issues: List[str], recommendations: List[str]) -> float:
        """Bewertet die Spezifität des Frames"""
        score = 1.0
        
        # Generische Begriffe erkennen
        generic_terms = {
            "signal": ["text", "nachricht", "aussage", "wort", "phrase"],
            "concept": ["kommunikation", "verhalten", "muster", "ausdruck"],
            "pragmatics": ["wirkung", "effekt", "einfluss", "reaktion"], 
            "narrative": ["story", "geschichte", "verlauf", "entwicklung"]
        }
        
        for field, generic_list in generic_terms.items():
            value = frame.get(field, "")
            if isinstance(value, list):
                value = " ".join(value)
            value = value.lower()
            
            for generic in generic_list:
                if generic in value and len(value.split()) <= 2:
                    issues.append(f"Zu generisch: {field} = '{value}'")
                    recommendations.append(f"Spezifischere Begriffe für {field} verwenden")
                    score -= 0.15
        
        return max(0.0, score)
    
    def _validate_semantics(self, marker_data: Dict[str, Any], frame_analysis: FrameAnalysis) -> List[str]:
        """Validiert die semantische Konsistenz des gesamten Markers"""
        errors = []
        
        marker_id = marker_data.get("id", "")
        frame = marker_data.get("frame", {})
        
        # Level-spezifische Validierung
        if marker_id.startswith("A_"):
            # Atomic Marker müssen 'pattern' haben
            if "pattern" not in marker_data:
                errors.append("Atomic Marker benötigt 'pattern'-Feld")
        elif marker_id.startswith(("S_", "C_", "MM_")):
            # Höhere Level müssen 'composed_of' haben
            if "composed_of" not in marker_data:
                errors.append("Semantic/Cluster/Meta Marker benötigen 'composed_of'-Feld")
        
        # Frame-Konsistenz mit ID-Level
        narrative = frame.get("narrative", "")
        if marker_id.startswith("C_") and "loop" in narrative:
            # Cluster mit Loop-Narrativ sind oft problematisch
            if frame_analysis.coherence_score < 0.8:
                errors.append("Loop-Narrative in Cluster-Markern erfordern besonders hohe Kohärenz")
        
        return errors
    
    def _determine_suitability(self, frame_analysis: FrameAnalysis, semantic_errors: List[str]) -> bool:
        """Entscheidet über die Eignung für Beispiel-Generierung"""
        if semantic_errors:
            return False
        
        if not frame_analysis.is_clear:
            return False
        
        if not frame_analysis.is_coherent:
            return False
        
        # Auch bei niedriger Spezifität können wir Beispiele generieren, 
        # aber mit Warnungen
        return True
    
    def _calculate_confidence(self, frame_analysis: FrameAnalysis, semantic_errors: List[str]) -> float:
        """Berechnet Confidence-Score für die Validierung"""
        if semantic_errors:
            return 0.0
        
        # Gewichteter Durchschnitt der Frame-Scores
        confidence = (
            frame_analysis.clarity_score * 0.4 +
            frame_analysis.coherence_score * 0.4 +
            frame_analysis.specificity_score * 0.2
        )
        
        return confidence
    
    def get_validation_stats(self) -> Dict[str, int]:
        """Gibt Validierungsstatistiken zurück"""
        return self.validation_stats.copy()


class ExampleGenerator:
    """
    Der Beispiel-Generator - Stufe 2: Konfigurierbare Beispiel-Generierung
    
    Generiert nur für semantisch klare Marker realitätsnahe, vielfältige Beispiele.
    Bewertet die eigenen Beispiele und verwirft ungeeignete.
    """
    
    def __init__(self):
        """Initialisiert den Beispiel-Generator"""
        self.generation_stats = {
            "total_requests": 0,
            "successful_generations": 0,
            "rejected_low_quality": 0,
            "examples_generated": 0
        }
    
    def generate_examples(self, marker_data: Dict[str, Any], num_examples: int = 5) -> Tuple[List[str], List[str]]:
        """
        Generiert neue Beispiele für einen validierten Marker
        
        Args:
            marker_data: Validierter Marker
            num_examples: Gewünschte Anzahl Beispiele
            
        Returns:
            Tuple (erfolgreiche_beispiele, warnungen)
        """
        self.generation_stats["total_requests"] += 1
        
        marker_id = marker_data.get("id", "UNKNOWN")
        frame = marker_data.get("frame", {})
        
        logger.info(f"🎯 Generiere {num_examples} Beispiele für {marker_id}")
        
        # Frame-Analyse für Generierung
        signals = frame.get("signal", [])
        concept = frame.get("concept", "")
        pragmatics = frame.get("pragmatics", "")
        narrative = frame.get("narrative", "")
        
        # Beispiel-Templates basierend auf Frame-Dimensionen
        examples = []
        warnings = []
        
        # Verschiedene Generierungsstrategien
        strategies = [
            self._generate_direct_signal_examples,
            self._generate_contextual_examples, 
            self._generate_variation_examples,
            self._generate_conversational_examples
        ]
        
        for strategy in strategies:
            if len(examples) >= num_examples:
                break
            
            try:
                new_examples = strategy(frame, marker_id)
                examples.extend(new_examples)
            except Exception as e:
                logger.warning(f"Generierungsstrategie fehlgeschlagen: {e}")
        
        # Qualitätsbewertung und Filterung
        filtered_examples = []
        for example in examples[:num_examples * 2]:  # Generiere mehr als nötig
            if self._evaluate_example_quality(example, frame, marker_id):
                filtered_examples.append(example)
                if len(filtered_examples) >= num_examples:
                    break
        
        # Statistiken aktualisieren
        self.generation_stats["examples_generated"] += len(filtered_examples)
        if filtered_examples:
            self.generation_stats["successful_generations"] += 1
        
        # Warnungen generieren
        if len(filtered_examples) < num_examples:
            shortage = num_examples - len(filtered_examples)
            warnings.append(f"WARNUNG: Nur {len(filtered_examples)} von {num_examples} angeforderten Beispielen erfüllten die Qualitätsanforderung.")
            self.generation_stats["rejected_low_quality"] += shortage
        
        return filtered_examples, warnings
    
    def _generate_direct_signal_examples(self, frame: Dict[str, Any], marker_id: str) -> List[str]:
        """Generiert Beispiele direkt aus den Signalen"""
        signals = frame.get("signal", [])
        concept = frame.get("concept", "")
        
        examples = []
        
        # Direkte Signal-Verwendung (ohne Anführungszeichen)
        for signal in signals[:3]:  # Maximal 3 direkte Beispiele
            if isinstance(signal, str) and len(signal) > 3:
                examples.append(signal)
        
        # Fallback wenn keine Signale: generiere aus Konzept
        if not examples and concept:
            examples.append(f"Ich denke an {concept.lower()}.")
        
        return examples
    
    def _generate_contextual_examples(self, frame: Dict[str, Any], marker_id: str) -> List[str]:
        """Generiert kontextuelle Variationen"""
        signals = frame.get("signal", [])
        concept = frame.get("concept", "").lower()
        pragmatics = frame.get("pragmatics", "").lower()
        narrative = frame.get("narrative", "").lower()
        
        examples = []
        
        # Kontextuelle Templates basierend auf Pragmatik
        if "unterstützung" in pragmatics or "support" in pragmatics:
            base_signal = signals[0] if signals else "ich bin da"
            examples.extend([
                f'"{base_signal}, wann immer du mich brauchst."',
                f'"Falls etwas ist: {base_signal}."'
            ])
        
        elif "destabilisierung" in pragmatics or "destabilization" in pragmatics:
            if signals:
                examples.extend([
                    f'"{signals[0]} ... aber irgendwie bin ich unsicher."',
                    f'"Einerseits {signals[0]}, andererseits weiß ich nicht."'
                ])
        
        elif "bindung" in concept:
            examples.extend([
                f'"Wir haben eine besondere Verbindung."',
                f'"Zwischen uns ist etwas Einzigartiges."'
            ])
        
        return examples
    
    def _generate_variation_examples(self, frame: Dict[str, Any], marker_id: str) -> List[str]:
        """Generiert Variationen mit verschiedenen Formulierungen"""
        signals = frame.get("signal", [])
        
        examples = []
        variation_patterns = [
            "Kannst du verstehen, dass {}?",
            "Manchmal fühle ich {}, weißt du?", 
            "{} - das beschreibt es am besten.",
            "Wie soll ich das sagen... {}",
        ]
        
        if signals:
            base_signal = signals[0] if signals else ""
            for pattern in variation_patterns[:2]:
                try:
                    examples.append(f'"{pattern.format(base_signal)}"')
                except:
                    continue
        
        return examples
    
    def _generate_conversational_examples(self, frame: Dict[str, Any], marker_id: str) -> List[str]:
        """Generiert dialogische Beispiele"""
        signals = frame.get("signal", [])
        narrative = frame.get("narrative", "").lower()
        
        examples = []
        
        if "loop" in narrative and signals:
            # Dialog-Loop-Muster
            signal = signals[0] if signals else "ich bin verwirrt"
            examples.extend([
                f'"A: {signal} B: Wie meinst du das? A: Ich weiß auch nicht... es ist kompliziert."',
                f'"Immer wenn wir reden, komme ich zu: {signal}"'
            ])
        elif len(signals) >= 2:
            # Zwei-Personen-Dialog
            examples.append(f'"A: {signals[0]} B: {signals[1]}"')
        
        return examples
    
    def _evaluate_example_quality(self, example: str, frame: Dict[str, Any], marker_id: str) -> bool:
        """
        Bewertet die Qualität eines generierten Beispiels
        
        Args:
            example: Das zu bewertende Beispiel
            frame: Der ursprüngliche Frame
            marker_id: Marker-ID
            
        Returns:
            True wenn das Beispiel die Qualitätsanforderungen erfüllt
        """
        # Grundlegende Qualitätsprüfungen
        if not example or len(example.strip()) < 5:  # Weniger streng
            return False
        
        # Entferne Anführungszeichen für Analyse
        clean_example = example.strip('"').strip("'")
        
        # Längen-Check
        if len(clean_example) > 200:  # Zu lang
            return False
        
        if len(clean_example.split()) < 2:  # Mindestens 2 Wörter
            return False
        
        # Signal-Relevanz prüfen - weniger streng
        signals = frame.get("signal", [])
        concept = frame.get("concept", "").lower()
        pragmatics = frame.get("pragmatics", "").lower()
        
        example_lower = clean_example.lower()
        
        # Erweiterte Relevanz-Prüfung
        signal_match = any(signal.lower() in example_lower for signal in signals if isinstance(signal, str) and len(signal) > 2)
        concept_words = concept.split()
        concept_match = any(word in example_lower for word in concept_words if len(word) > 2)
        
        # Pragmatik-Relevanz (für Fälle ohne direkte Signal-Matches)
        pragmatic_words = pragmatics.split()
        pragmatic_match = any(word in example_lower for word in pragmatic_words if len(word) > 3)
        
        # Mindestens eine Art von Relevanz
        if not (signal_match or concept_match or pragmatic_match):
            # Letzte Chance: Enthält das Beispiel typische Sprach-Indikatoren?
            common_indicators = ["ich", "du", "wir", "bin", "ist", "wenn", "aber", "und"]
            has_indicators = any(indicator in example_lower for indicator in common_indicators)
            if not has_indicators:
                return False
        
        # Kohärenz mit Pragmatik
        # Negative Pragmatik-Konflikte
        if "unterstützung" in pragmatics and any(neg in example_lower for neg in ["hass", "ablehnung", "ignorier"]):
            return False
        
        if "destabilisierung" in pragmatics and "stabil" in example_lower:
            return False
        
        return True
    
    def get_generation_stats(self) -> Dict[str, int]:
        """Gibt Generierungsstatistiken zurück"""
        return self.generation_stats.copy()


class MarkerExampleProcessor:
    """
    Hauptschnittstelle: Koordiniert Wächter und Generator
    
    Implementiert den zweistufigen Prozess:
    1. Semantische Validierung durch Guardian
    2. Intelligente Beispiel-Generierung durch Generator
    """
    
    def __init__(self):
        """Initialisiert den Marker-Beispiel-Prozessor"""
        self.guardian = SemanticGuardian()
        self.generator = ExampleGenerator()
    
    def process_marker_file(self, file_path: Path, num_examples: int = 5, backup: bool = True) -> Dict[str, Any]:
        """
        Verarbeitet eine Marker-Datei komplett
        
        Args:
            file_path: Pfad zur Marker-YAML-Datei
            num_examples: Anzahl zu generierender Beispiele
            backup: Ob ein Backup erstellt werden soll
            
        Returns:
            Verarbeitungsreport mit Ergebnissen
        """
        logger.info(f"🚀 Verarbeite Marker-Datei: {file_path}")
        
        # Datei laden
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                marker_data = yaml.safe_load(f)
        except Exception as e:
            return {
                "success": False,
                "error": f"Fehler beim Laden der Datei: {e}",
                "file_path": str(file_path)
            }
        
        # Backup erstellen
        if backup:
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
            try:
                with open(backup_path, 'w', encoding='utf-8') as f:
                    yaml.dump(marker_data, f, default_flow_style=False, allow_unicode=True)
                logger.info(f"📦 Backup erstellt: {backup_path}")
            except Exception as e:
                logger.warning(f"Backup-Erstellung fehlgeschlagen: {e}")
        
        # Stufe 1: Validierung
        validation_report = self.guardian.validate_marker(marker_data)
        
        if not validation_report.is_suitable_for_examples:
            return {
                "success": False,
                "error": "GENERIERUNG ABGELEHNT: Marker-Frame ist semantisch nicht eindeutig.",
                "validation_report": validation_report,
                "file_path": str(file_path)
            }
        
        # Stufe 2: Beispiel-Generierung
        new_examples, warnings = self.generator.generate_examples(marker_data, num_examples)
        
        if not new_examples:
            return {
                "success": False,
                "error": "Keine gültigen Beispiele konnten generiert werden.",
                "validation_report": validation_report,
                "warnings": warnings,
                "file_path": str(file_path)
            }
        
        # Beispiele zu Marker hinzufügen
        existing_examples = marker_data.get("examples", [])
        
        # Neue Beispiele anhängen
        if existing_examples:
            # Kommentar-Trennung hinzufügen
            if "examples" not in marker_data:
                marker_data["examples"] = []
            marker_data["examples"].extend(["# --- Neu generierte Beispiele ---"] + new_examples)
        else:
            marker_data["examples"] = new_examples
        
        # Datei speichern
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(marker_data, f, default_flow_style=False, allow_unicode=True)
            logger.info(f"✅ Datei erfolgreich aktualisiert: {file_path}")
        except Exception as e:
            return {
                "success": False,
                "error": f"Fehler beim Speichern der Datei: {e}",
                "validation_report": validation_report,
                "new_examples": new_examples,
                "warnings": warnings,
                "file_path": str(file_path)
            }
        
        return {
            "success": True,
            "validation_report": validation_report,
            "new_examples": new_examples,
            "examples_added": len(new_examples),
            "warnings": warnings,
            "file_path": str(file_path)
        }
    
    def generate_examples_for_marker(self, marker_data: Dict[str, Any], num_examples: int = 5) -> Dict[str, Any]:
        """
        Generiert Beispiele für einen einzelnen Marker (ohne Datei-IO)
        
        Args:
            marker_data: Marker-Daten
            num_examples: Anzahl Beispiele
            
        Returns:
            Generierungsreport
        """
        # Stufe 1: Validierung
        validation_report = self.guardian.validate_marker(marker_data)
        
        if not validation_report.is_suitable_for_examples:
            return {
                "success": False,
                "error": "GENERIERUNG ABGELEHNT: Marker-Frame ist semantisch nicht eindeutig.",
                "validation_report": validation_report
            }
        
        # Stufe 2: Beispiel-Generierung
        new_examples, warnings = self.generator.generate_examples(marker_data, num_examples)
        
        return {
            "success": True,
            "validation_report": validation_report,
            "new_examples": new_examples,
            "warnings": warnings
        }
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Gibt umfassende Statistiken zurück"""
        return {
            "validation_stats": self.guardian.get_validation_stats(),
            "generation_stats": self.generator.get_generation_stats()
        }


def main():
    """Hauptfunktion für CLI-Usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Semantischer Wächter & Beispiel-Generator")
    parser.add_argument("file_path", help="Pfad zur Marker-YAML-Datei")
    parser.add_argument("--examples", "-e", type=int, default=5, help="Anzahl zu generierender Beispiele")
    parser.add_argument("--no-backup", action="store_true", help="Kein Backup erstellen")
    parser.add_argument("--stats", action="store_true", help="Statistiken anzeigen")
    
    args = parser.parse_args()
    
    processor = MarkerExampleProcessor()
    
    file_path = Path(args.file_path)
    if not file_path.exists():
        logger.error(f"Datei nicht gefunden: {file_path}")
        return 1
    
    result = processor.process_marker_file(
        file_path=file_path,
        num_examples=args.examples,
        backup=not args.no_backup
    )
    
    if result["success"]:
        logger.info("🎉 Verarbeitung erfolgreich abgeschlossen!")
        logger.info(f"✨ {result['examples_added']} neue Beispiele hinzugefügt")
        
        if result["warnings"]:
            for warning in result["warnings"]:
                logger.warning(warning)
    else:
        logger.error(f"❌ Verarbeitung fehlgeschlagen: {result['error']}")
        return 1
    
    if args.stats:
        stats = processor.get_comprehensive_stats()
        logger.info(f"📊 Statistiken: {stats}")
    
    return 0


if __name__ == "__main__":
    exit(main())