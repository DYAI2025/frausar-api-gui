#!/usr/bin/env python3
"""
Test script for v3.1 marker functionality
"""

import yaml
from pathlib import Path
from marker_v3_1_manager import MarkerV31Manager

def test_v31_functionality():
    """Test the complete v3.1 functionality."""
    print("🧪 Testing Lean-Deep v3.1 Marker Functionality")
    print("=" * 50)
    
    manager = MarkerV31Manager()
    test_dir = Path("test_markers")
    test_dir.mkdir(exist_ok=True)
    
    # Test 1: Template Creation for all levels
    print("\n1. Testing Template Creation:")
    for level in range(1, 5):
        template = manager.create_marker_template(level, f"TEST_LEVEL_{level}", "Test Author")
        
        # Validate template
        is_valid, errors = manager.validate_marker_schema(template)
        
        print(f"   Level {level}: {template['id']} - {'✅ VALID' if is_valid else '❌ INVALID'}")
        if errors:
            for error in errors[:2]:
                print(f"     - {error}")
        
        # Save test file
        filename = manager.generate_filename(template['id'])
        with open(test_dir / filename, 'w', encoding='utf-8') as f:
            yaml.dump(template, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    # Test 2: Schema Validation with various invalid cases
    print("\n2. Testing Schema Validation:")
    
    # Invalid marker - missing fields
    invalid_marker = {"id": "INVALID_MARKER", "level": 1}
    is_valid, errors = manager.validate_marker_schema(invalid_marker)
    print(f"   Invalid marker: {'✅ VALID' if is_valid else '❌ INVALID'} ({len(errors)} errors)")
    
    # Invalid level
    invalid_level = manager.create_marker_template(1, "TEST_INVALID", "Test")
    invalid_level["level"] = 5  # Invalid level
    is_valid, errors = manager.validate_marker_schema(invalid_level)
    print(f"   Invalid level: {'✅ VALID' if is_valid else '❌ INVALID'} ({len(errors)} errors)")
    
    # Invalid examples count
    invalid_examples = manager.create_marker_template(1, "TEST_EXAMPLES", "Test")
    invalid_examples["examples"] = ["Only one example"]  # Less than 5
    is_valid, errors = manager.validate_marker_schema(invalid_examples)
    print(f"   Invalid examples: {'✅ VALID' if is_valid else '❌ INVALID'} ({len(errors)} errors)")
    
    # Test 3: Conversion from old format
    print("\n3. Testing Old Format Conversion:")
    
    old_marker = {
        "id": "OLD_MARKER",
        "level": "2",  # String instead of int
        "beschreibung": "Old style description",
        "kategorie": "old_category",
        "examples": ["Old example 1", "Old example 2"]
    }
    
    converted = manager.convert_old_marker_to_v31(old_marker)
    is_valid, errors = manager.validate_marker_schema(converted)
    print(f"   Converted marker: {converted['id']} - {'✅ VALID' if is_valid else '❌ INVALID'}")
    print(f"   Level: {converted['level']}, Category: {converted['category']}")
    print(f"   Examples count: {len(converted['examples'])}")
    
    # Test 4: Multi-marker YAML processing
    print("\n4. Testing Multi-Marker YAML:")
    
    # Create multi-marker YAML
    template1 = manager.create_marker_template(1, "MULTI_MARKER_1", "Test")
    template2 = manager.create_marker_template(2, "MULTI_MARKER_2", "Test")
    
    yaml1 = yaml.dump(template1, default_flow_style=False, allow_unicode=True, sort_keys=False)
    yaml2 = yaml.dump(template2, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    multi_yaml = f"{yaml1}\n---\n\n{yaml2}"
    
    # Parse and validate
    blocks = multi_yaml.split('\n---\n')
    valid_count = 0
    for i, block in enumerate(blocks):
        try:
            data = yaml.safe_load(block.strip())
            if data:
                is_valid, errors = manager.validate_marker_schema(data)
                if is_valid:
                    valid_count += 1
                print(f"   Block {i+1}: {data.get('id', 'Unknown')} - {'✅ VALID' if is_valid else '❌ INVALID'}")
        except Exception as e:
            print(f"   Block {i+1}: ❌ ERROR - {str(e)}")
    
    print(f"   Total valid markers: {valid_count}/{len(blocks)}")
    
    # Test 5: Level-specific field validation
    print("\n5. Testing Level-Specific Fields:")
    
    level_tests = [
        (1, "atomic_pattern"),
        (2, "composed_of"), 
        (3, "activation_logic"),
        (4, "trigger_threshold")
    ]
    
    for level, required_field in level_tests:
        template = manager.create_marker_template(level, f"LEVEL_TEST_{level}", "Test")
        
        # Test with field present
        is_valid, errors = manager.validate_marker_schema(template)
        print(f"   Level {level} with {required_field}: {'✅ VALID' if is_valid else '❌ INVALID'}")
        
        # Test with field missing  
        del template[required_field]
        is_valid, errors = manager.validate_marker_schema(template)
        print(f"   Level {level} without {required_field}: {'✅ VALID' if is_valid else '❌ INVALID'} (expected invalid)")
    
    print("\n🎯 Test Summary:")
    print(f"   Created test files in: {test_dir}")
    print(f"   All v3.1 features tested")
    print("\n✅ v3.1 Functionality Tests Completed!")

if __name__ == "__main__":
    test_v31_functionality()