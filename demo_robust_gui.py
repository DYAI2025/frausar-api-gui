#!/usr/bin/env python3
"""
Demonstration script showing the Robust Marker GUI functionality.
Creates sample data and showcases key features.
"""

import yaml
from pathlib import Path
from marker_v3_1_manager import MarkerV31Manager

def demonstrate_marker_adaptation():
    """Demonstrate the enhanced marker adaptation functionality."""
    print("🔄 DEMONSTRATING MARKER ADAPTATION")
    print("=" * 50)
    
    manager = MarkerV31Manager()
    
    # Create an old-style marker with German field names
    old_marker = {
        'id': 'LEGACY_MARKER',
        'level': '2',  # String instead of int
        'kategorie': 'semantic',  # German field name
        'beschreibung': 'Ein alter Marker mit deutschen Feldnamen',  # German field
        'erstellungsdatum': '2023-01-01',  # German field
        'author': 'Legacy Author',
        'examples': [
            'Beispiel 1',
            'Beispiel 2'
        ],
        'custom_old_field': 'This will be removed',
        'another_legacy_field': 'Also removed'
    }
    
    print("📥 Original marker:")
    print(yaml.dump(old_marker, default_flow_style=False, allow_unicode=True))
    
    # Adapt to v3.1 with detailed reporting
    adapted_marker, changes_report = manager.adapt_marker_to_v31_with_report(old_marker)
    
    print("📤 Adapted marker:")
    print(yaml.dump(adapted_marker, default_flow_style=False, allow_unicode=True))
    
    print("📊 DETAILED CHANGE REPORT")
    print("-" * 30)
    
    if changes_report['added']:
        print(f"\n➕ ADDED FIELDS ({len(changes_report['added'])}):")
        for item in changes_report['added']:
            print(f"  • {item['field']}: {item['value']}")
            print(f"    Reason: {item['reason']}")
    
    if changes_report['removed']:
        print(f"\n➖ REMOVED FIELDS ({len(changes_report['removed'])}):")
        for item in changes_report['removed']:
            print(f"  • {item['field']}: {item['value']}")
            print(f"    Reason: {item['reason']}")
    
    if changes_report['modified']:
        print(f"\n🔄 MODIFIED FIELDS ({len(changes_report['modified'])}):")
        for item in changes_report['modified']:
            print(f"  • {item['field']}")
            print(f"    Old: {item['original_value']}")
            print(f"    New: {item['new_value']}")
            print(f"    Reason: {item['reason']}")
    
    if changes_report['preserved']:
        print(f"\n✅ PRESERVED FIELDS ({len(changes_report['preserved'])}):")
        for item in changes_report['preserved']:
            print(f"  • {item['field']}")
    
    if changes_report['warnings']:
        print(f"\n⚠️ WARNINGS ({len(changes_report['warnings'])}):")
        for warning in changes_report['warnings']:
            print(f"  • {warning}")
    
    # Validate the result
    is_valid, errors = manager.validate_marker_schema(adapted_marker)
    print(f"\n✅ VALIDATION RESULT: {'VALID' if is_valid else 'INVALID'}")
    if errors:
        for error in errors:
            print(f"  ❌ {error}")
    
    print("\n" + "=" * 50)
    return adapted_marker

def demonstrate_content_validation():
    """Demonstrate content boundary validation."""
    print("🔍 DEMONSTRATING CONTENT VALIDATION")
    print("=" * 50)
    
    manager = MarkerV31Manager()
    
    # Create a marker with various content issues
    problematic_marker = {
        'id': 'A_PROBLEMATIC',
        'level': 1,
        'version': '1.0.0',
        'author': 'Test Author',
        'created_at': '2024-01-01',
        'status': 'draft',
        'lang': 'en',
        'name': 'PROBLEMATIC',
        'description': 'Short',  # Too short
        'category': 'ATOMIC',
        'scoring': {'weight': 1.0, 'priority': 'normal'},
        'tags': ['test'],
        'semantic_grabber_id': 'SGR_PROBLEMATIC_01',
        'examples': [
            'Example',  # Placeholder-like
            'TODO',     # Placeholder
            'A very short example',  # Too short
            'This is a proper example with sufficient detail',
            'Another good example with meaningful content'
        ],
        'atomic_pattern': ['pattern1']
    }
    
    print("📋 Marker with content issues:")
    print(yaml.dump(problematic_marker, default_flow_style=False, allow_unicode=True))
    
    # Validate content boundaries
    warnings = manager.validate_content_boundaries(problematic_marker)
    
    print("⚠️ CONTENT VALIDATION WARNINGS:")
    for i, warning in enumerate(warnings, 1):
        print(f"  {i}. {warning}")
    
    print("\n" + "=" * 50)

def demonstrate_quality_analysis():
    """Demonstrate quality scoring and analysis."""
    print("⭐ DEMONSTRATING QUALITY ANALYSIS")
    print("=" * 50)
    
    manager = MarkerV31Manager()
    
    # Create markers with different quality levels
    markers = [
        {
            'name': 'High Quality Marker',
            'data': manager.create_marker_template(1, 'HIGH_QUALITY', 'Expert Author')
        },
        {
            'name': 'Medium Quality Marker', 
            'data': {
                'id': 'A_MEDIUM_QUALITY',
                'level': 1,
                'version': '1.0.0',
                'author': 'Author',
                'created_at': '2024-01-01',
                'status': 'draft',
                'lang': 'en',
                'name': 'MEDIUM_QUALITY',
                'description': 'Basic description',
                'category': 'ATOMIC',
                'scoring': {'weight': 1.0, 'priority': 'normal'},
                'tags': ['test'],
                'semantic_grabber_id': 'SGR_MEDIUM_01',
                'examples': ['Ex1', 'Ex2', 'Ex3', 'Ex4', 'Ex5'],  # Short examples
                'atomic_pattern': ['pattern']
            }
        },
        {
            'name': 'Low Quality Marker',
            'data': {
                'id': 'A_LOW_QUALITY',
                'level': 1,
                'description': 'Bad',  # Too short
                'examples': ['Ex1', 'Ex2']  # Too few
            }
        }
    ]
    
    # Mock quality calculation (simplified version)
    def calculate_quality_score(data):
        score = 0
        
        # Schema validation (40 points)
        is_valid, _ = manager.validate_marker_schema(data)
        if is_valid:
            score += 40
        
        # Description quality (30 points)
        description = data.get('description', '')
        if len(description) >= 20:
            score += 15
        if len(description) >= 50:
            score += 15
        
        # Examples quality (30 points)
        examples = data.get('examples', [])
        if len(examples) >= 5:
            score += 15
        
        real_examples = [ex for ex in examples if ex.lower().strip() not in ['example', 'todo', 'placeholder']]
        if len(real_examples) >= 5:
            score += 15
        
        return min(score, 100)
    
    for marker in markers:
        print(f"📊 {marker['name']}:")
        
        is_valid, errors = manager.validate_marker_schema(marker['data'])
        quality_score = calculate_quality_score(marker['data'])
        
        print(f"  Schema Valid: {'✅' if is_valid else '❌'}")
        print(f"  Quality Score: {quality_score}/100")
        
        if quality_score >= 90:
            rating = "Excellent"
        elif quality_score >= 70:
            rating = "Good"
        elif quality_score >= 50:
            rating = "Acceptable"
        else:
            rating = "Needs Improvement"
        
        print(f"  Rating: {rating}")
        
        if errors:
            print(f"  Issues: {len(errors)} validation errors")
        
        print()
    
    print("=" * 50)

def create_feature_showcase():
    """Create a comprehensive feature showcase."""
    print("🎯 ROBUST MARKER GUI - FEATURE SHOWCASE")
    print("=" * 60)
    print()
    
    # Demonstrate each key feature
    adapted_marker = demonstrate_marker_adaptation()
    print()
    
    demonstrate_content_validation()
    print()
    
    demonstrate_quality_analysis()
    print()
    
    # Show v3.1 compliance
    print("✅ LEAN-DEEP V3.1 COMPLIANCE FEATURES")
    print("=" * 50)
    print("• Four-sided frame logic support")
    print("• Unified scoring syntax validation") 
    print("• Level-specific field requirements")
    print("• Mandatory 5+ examples enforcement")
    print("• Semantic grabber ID validation")
    print("• Category-level consistency checks")
    print()
    
    # Show GUI advantages
    print("🎨 GUI DESIGN IMPROVEMENTS")
    print("=" * 50)
    print("• Modern tabbed interface (Management/Preview/Batch)")
    print("• Dual-editor approach (YAML + Form)")
    print("• Live validation with immediate feedback")
    print("• Advanced search and filtering")
    print("• Context menus for quick actions")
    print("• Responsive layout with adjustable panels")
    print("• Professional styling with consistent colors")
    print()
    
    # Show robustness features
    print("🛡️ ROBUSTNESS & STABILITY FEATURES")
    print("=" * 50)
    print("• Automatic backup before changes")
    print("• Multi-level undo functionality")
    print("• Graceful error handling")
    print("• Input validation at all levels")
    print("• Content preservation during adaptation")
    print("• Detailed change reporting")
    print("• Quality scoring and analysis")
    print()
    
    print("🎉 DEMONSTRATION COMPLETE!")
    print("The Robust Marker GUI provides a professional,")
    print("stable, and user-friendly solution for Lean-Deep v3.1")
    print("marker management with significant improvements over")
    print("the previous GUI in design, functionality, and reliability.")

if __name__ == "__main__":
    create_feature_showcase()