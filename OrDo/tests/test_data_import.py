import pytest
import pandas as pd
import yaml
import sys
import os

# Fügt das Projektverzeichnis zum Python-Pfad hinzu, um Backend-Module zu importieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.data_import.readers import load_yaml_markers, load_chat_log_from_txt

@pytest.fixture
def temp_marker_file(tmp_path):
    """Erzeugt eine temporäre Marker-YAML-Datei für Tests."""
    content = {
        'markers': {
            'positive': {'keywords': ['gut', 'danke'], 'score': 1},
            'negative': {'keywords': ['schlecht', 'problem'], 'score': -1}
        }
    }
    file_path = tmp_path / "markers.yaml"
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(content, f)
    return str(file_path)

@pytest.fixture
def temp_chat_file(tmp_path):
    """Erzeugt eine temporäre Chat-Log-Datei für Tests."""
    content = (
        "[01.01.24, 10:00:00] User1: Das war gut.\n"
        "[01.01.24, 10:05:00] User2: Das ist ein Problem.\n"
        "Und es geht weiter."
    )
    file_path = tmp_path / "chat.txt"
    file_path.write_text(content, encoding='utf-8')
    return str(file_path)

def test_load_yaml_markers_success(temp_marker_file):
    """Testet das erfolgreiche Laden von Markern aus einer YAML-Datei."""
    markers = load_yaml_markers(temp_marker_file)
    assert 'markers' in markers
    assert 'positive' in markers['markers']
    assert markers['markers']['negative']['score'] == -1

def test_load_chat_log_from_txt_success(temp_chat_file):
    """Testet das erfolgreiche Laden und Parsen eines Chat-Logs."""
    df = load_chat_log_from_txt(temp_chat_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'timestamp' in df.columns
    assert 'author' in df.columns
    assert 'message' in df.columns
    assert df.iloc[0]['author'] == 'User1'
    assert "Und es geht weiter." in df.iloc[1]['message']
    assert pd.api.types.is_datetime64_any_dtype(df['timestamp'])

def test_load_non_existent_files():
    """Testet, ob bei nicht existierenden Dateien ein FileNotFoundError ausgelöst wird."""
    with pytest.raises(FileNotFoundError):
        load_yaml_markers("non_existent_file.yaml")
    
    with pytest.raises(FileNotFoundError):
        load_chat_log_from_txt("non_existent_file.txt") 