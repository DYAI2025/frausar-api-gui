import pytest
import pandas as pd
from datetime import datetime
import sys
import os

# Fügt das Projektverzeichnis zum Python-Pfad hinzu, um Backend-Module zu importieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.analysis.core import analyze_monthly_scores

@pytest.fixture
def sample_chat_df():
    """Erzeugt einen Beispiel-Chat-DataFrame für Tests."""
    data = [
        {'timestamp': datetime(2024, 1, 10), 'author': 'Ben', 'message': 'Das ist gut und ein danke von mir.'},
        {'timestamp': datetime(2024, 1, 20), 'author': 'Zoe', 'message': 'Das ist ein Problem.'},
        {'timestamp': datetime(2024, 2, 5), 'author': 'Ben', 'message': 'Nochmal danke!'},
        {'timestamp': datetime(2024, 2, 15), 'author': 'Zoe', 'message': 'Das ist schlecht und noch ein Problem.'},
        {'timestamp': datetime(2024, 3, 1), 'author': 'Ben', 'message': 'Keine relevanten Wörter.'}
    ]
    return pd.DataFrame(data)

@pytest.fixture
def sample_markers_config():
    """Erzeugt eine Beispiel-Marker-Konfiguration für Tests."""
    return {
        'markers': {
            'positive': {'keywords': ['gut', 'danke'], 'score': 1},
            'negative': {'keywords': ['schlecht', 'problem'], 'score': -2}
        }
    }

def test_analyze_monthly_scores(sample_chat_df, sample_markers_config):
    """Testet die monatliche Score-Analyse und Aggregation."""
    result_df = analyze_monthly_scores(sample_chat_df, sample_markers_config)

    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 3
    assert 'month' in result_df.columns
    assert 'score' in result_df.columns

    # Erwartete Scores pro Monat:
    # Januar: (1 für 'gut' + 1 für 'danke') + (-2 für 'problem') = 0
    # Februar: (1 für 'danke') + (-2 für 'schlecht' + -2 für 'problem') = -3
    # März: 0
    expected_scores = {
        pd.Timestamp('2024-01-01'): 0,
        pd.Timestamp('2024-02-01'): -3,
        pd.Timestamp('2024-03-01'): 0,
    }

    # Konvertiert das Ergebnis in ein einfach zu prüfendes Format
    result_scores = result_df.set_index('month')['score'].to_dict()
    assert result_scores == expected_scores

def test_analyze_monthly_scores_by_author(sample_chat_df, sample_markers_config):
    """Testet die monatliche Score-Analyse, aufgeschlüsselt nach Autor."""
    result_df = analyze_monthly_scores(sample_chat_df, sample_markers_config)

    assert 'author' in result_df.columns
    
    # Erwartete Scores:
    # Ben: Jan: 2 (gut, danke), Feb: 1 (danke), Mar: 0 -> Total 3
    # Zoe: Jan: -2 (problem), Feb: -4 (schlecht, problem) -> Total -6
    
    ben_scores = result_df[result_df['author'] == 'Ben'].set_index('month')['score'].to_dict()
    zoe_scores = result_df[result_df['author'] == 'Zoe'].set_index('month')['score'].to_dict()

    expected_ben = {
        pd.Timestamp('2024-01-01'): 2,
        pd.Timestamp('2024-02-01'): 1
    }
    expected_zoe = {
        pd.Timestamp('2024-01-01'): -2,
        pd.Timestamp('2024-02-01'): -4
    }

    # Wir vergleichen nur die Monate, in denen Scores erwartet werden
    # (Ben hat im März einen 0-Score, der durch groupby wegfällt)
    assert ben_scores == expected_ben
    assert zoe_scores == expected_zoe

def test_analyze_with_empty_dataframe():
    """Testet das Verhalten der Analysefunktion mit einem leeren DataFrame."""
    empty_df = pd.DataFrame(columns=['timestamp', 'author', 'message'])
    markers = {'markers': {'test': {'keywords': ['a'], 'score': 1}}}
    result = analyze_monthly_scores(empty_df, markers)
    
    assert result.empty
    assert 'month' in result.columns
    assert 'score' in result.columns 