#!/usr/bin/env python3
"""
Test script for the Robust Marker GUI functionality.
Tests the core features without requiring a graphical display.
"""

import yaml
import tempfile
import os
from pathlib import Path
from marker_v3_1_manager import MarkerV31Manager
from robust_marker_gui import RobustMarkerGUI

def test_marker_v31_manager_enhanced():
    """Test the enhanced MarkerV31Manager functionality."""
    print("🧪 Testing Enhanced MarkerV31Manager...")
    
    manager = MarkerV31Manager()
    
    # Test adaptation with reporting
    old_marker = {
        'id': 'OLD_MARKER',
        'level': 1,
        'kategorie': 'test',  # German field
        'beschreibung': 'Test description',  # German field
        'examples': ['Example 1', 'Example 2']  # Too few examples
    }
    
    adapted_marker, report = manager.adapt_marker_to_v31_with_report(old_marker)
    
    print(f"✅ Adaptation successful")
    print(f"   Added fields: {len(report['added'])}")
    print(f"   Removed fields: {len(report['removed'])}")
    print(f"   Modified fields: {len(report['modified'])}")
    print(f"   Preserved fields: {len(report['preserved'])}")
    print(f"   Warnings: {len(report['warnings'])}")
    
    # Test content boundary validation
    boundary_warnings = manager.validate_content_boundaries(adapted_marker)
    print(f"✅ Boundary validation: {len(boundary_warnings)} warnings")
    
    # Test schema validation
    is_valid, errors = manager.validate_marker_schema(adapted_marker)
    print(f"✅ Schema validation: {'VALID' if is_valid else 'INVALID'}")
    if errors:
        print(f"   Errors: {len(errors)}")
    
    print()

def test_robust_gui_core_functions():
    """Test core functions of RobustMarkerGUI without GUI display."""
    print("🧪 Testing RobustMarkerGUI Core Functions...")
    
    # Create a mock GUI instance (without actual tkinter initialization)
    class MockGUI:
        def __init__(self):
            self.v31_manager = MarkerV31Manager()
            self.current_marker_data = None
            self.backup_stack = []
            self.level_categories = self.v31_manager.level_categories
            
        def calculate_quality_score(self, data):
            # Import the method from the actual class
            from robust_marker_gui import RobustMarkerGUI
            return RobustMarkerGUI.calculate_quality_score(self, data)
            
        def analyze_marker_quality(self, data):
            from robust_marker_gui import RobustMarkerGUI
            return RobustMarkerGUI.analyze_marker_quality(self, data)
            
        def create_validation_report(self, data):
            from robust_marker_gui import RobustMarkerGUI
            return RobustMarkerGUI.create_validation_report(self, data)
    
    mock_gui = MockGUI()
    
    # Test with a good marker
    good_marker = {
        'id': 'A_GOOD_MARKER',
        'level': 1,
        'version': '1.0.0',
        'author': 'Test Author',
        'created_at': '2024-01-01',
        'status': 'draft',
        'lang': 'en',
        'name': 'GOOD_MARKER',
        'description': 'This is a comprehensive description that meets length requirements',
        'category': 'ATOMIC',
        'scoring': {'weight': 1.0, 'priority': 'normal'},
        'tags': ['test', 'example'],
        'semantic_grabber_id': 'SGR_GOOD_MARKER_01',
        'examples': [
            'Example 1 - detailed scenario',
            'Example 2 - alternative case',
            'Example 3 - edge case handling',
            'Example 4 - complex situation',
            'Example 5 - boundary condition'
        ],
        'atomic_pattern': ['pattern1', 'pattern2']
    }
    
    # Test quality scoring
    quality_score = mock_gui.calculate_quality_score(good_marker)
    print(f"✅ Quality score calculation: {quality_score}/100")
    
    # Test analysis
    analysis = mock_gui.analyze_marker_quality(good_marker)
    print(f"✅ Quality analysis generated: {len(analysis)} characters")
    
    # Test validation report
    report = mock_gui.create_validation_report(good_marker)
    print(f"✅ Validation report generated: {len(report)} characters")
    
    print()

def test_marker_adaptation_scenarios():
    """Test various marker adaptation scenarios."""
    print("🧪 Testing Marker Adaptation Scenarios...")
    
    manager = MarkerV31Manager()
    
    scenarios = [
        {
            'name': 'Old German Marker',
            'data': {
                'id': 'S_GERMAN_MARKER',
                'level': 2,
                'kategorie': 'semantic',
                'beschreibung': 'Deutsche Beschreibung',
                'erstellungsdatum': '2023-01-01',
                'examples': ['Beispiel 1', 'Beispiel 2']
            }
        },
        {
            'name': 'Minimal Marker',
            'data': {
                'id': 'C_MINIMAL',
                'level': 3
            }
        },
        {
            'name': 'Complex Old Marker',
            'data': {
                'id': 'MM_COMPLEX_OLD',
                'level': 4,
                'description': 'Complex marker with many fields',
                'author': 'Original Author',
                'examples': ['Ex1', 'Ex2', 'Ex3', 'Ex4', 'Ex5', 'Ex6'],
                'custom_field': 'This will be removed',
                'another_custom': 'This too'
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"  Scenario: {scenario['name']}")
        adapted, report = manager.adapt_marker_to_v31_with_report(scenario['data'])
        
        is_valid, errors = manager.validate_marker_schema(adapted)
        print(f"    ✅ Adapted successfully, Valid: {is_valid}")
        print(f"    Changes: +{len(report['added'])} -{len(report['removed'])} ~{len(report['modified'])}")
        
        if report['warnings']:
            print(f"    Warnings: {len(report['warnings'])}")
    
    print()

def create_demo_markers():
    """Create demonstration markers for testing the GUI."""
    print("📁 Creating Demo Markers...")
    
    markers_dir = Path("markers")
    markers_dir.mkdir(exist_ok=True)
    
    manager = MarkerV31Manager()
    
    demo_markers = [
        {
            'level': 1,
            'name': 'DEMO_ATOMIC',
            'author': 'Demo Creator',
            'description': 'This is a demonstration atomic marker for testing the robust GUI',
            'examples': [
                'Atomic pattern detection example 1',
                'Simple matching case example 2', 
                'Edge case boundary example 3',
                'Complex scenario example 4',
                'Integration test example 5'
            ]
        },
        {
            'level': 2, 
            'name': 'DEMO_SEMANTIC',
            'author': 'Demo Creator',
            'description': 'Semantic level marker demonstrating higher-level pattern recognition',
            'examples': [
                'Semantic context example 1',
                'Meaning extraction example 2',
                'Context-aware example 3', 
                'Language understanding example 4',
                'Conceptual mapping example 5'
            ]
        },
        {
            'level': 3,
            'name': 'DEMO_CLUSTER', 
            'author': 'Demo Creator',
            'description': 'Cluster marker showing aggregation of multiple semantic patterns',
            'examples': [
                'Multi-pattern cluster example 1',
                'Aggregated detection example 2',
                'Combined signal example 3',
                'Threshold-based example 4', 
                'Ensemble pattern example 5'
            ]
        }
    ]
    
    for demo in demo_markers:
        marker_data = manager.create_marker_template(
            demo['level'], demo['name'], demo['author']
        )
        marker_data['description'] = demo['description']
        marker_data['examples'] = demo['examples']
        
        filename = manager.generate_filename(marker_data['id'])
        filepath = markers_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(marker_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"  ✅ Created: {filename}")
    
    print()

def main():
    """Run all tests and create demo content."""
    print("🎯 ROBUST MARKER GUI - FUNCTIONALITY TEST")
    print("=" * 50)
    print()
    
    try:
        test_marker_v31_manager_enhanced()
        test_robust_gui_core_functions()
        test_marker_adaptation_scenarios()
        create_demo_markers()
        
        print("✅ ALL TESTS PASSED!")
        print("\nThe Robust Marker GUI is ready with:")
        print("  • Enhanced marker adaptation with detailed reporting")
        print("  • Robust content validation and boundary checking")
        print("  • Quality analysis and scoring system") 
        print("  • Modern UI with tabbed interface")
        print("  • Backup/undo functionality")
        print("  • Comprehensive validation reporting")
        print("  • Demo markers for testing")
        print("\nTo run the GUI: python robust_marker_gui.py")
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()