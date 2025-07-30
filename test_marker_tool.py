#!/usr/bin/env python3
"""
Test script for marker_tool.py functionality
"""

import tempfile
import shutil
from pathlib import Path
from marker_tool import MarkerTool, create_marker, validate_marker, convert_marker


def test_marker_tool():
    """Test the MarkerTool class functionality."""
    print("🧪 Testing MarkerTool functionality")
    print("=" * 40)
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        tool = MarkerTool(temp_dir)
        
        # Test 1: Create markers of different levels
        print("\n1. Testing marker creation:")
        levels = [1, 2, 3, 4]
        created_markers = []
        
        for level in levels:
            try:
                marker = tool.create_marker(
                    level=level,
                    name=f"TEST_LEVEL_{level}",
                    author="Test Suite",
                    description=f"Test marker for level {level}",
                    examples=[f"Example {i} for level {level}" for i in range(1, 6)]
                )
                created_markers.append(marker)
                print(f"   ✅ Level {level}: {marker['id']}")
            except Exception as e:
                print(f"   ❌ Level {level}: {e}")
        
        # Test 2: Validation
        print("\n2. Testing validation:")
        for marker in created_markers:
            is_valid, errors = tool.validate_marker(marker)
            print(f"   {marker['id']}: {'✅ Valid' if is_valid else '❌ Invalid'}")
            if errors:
                for error in errors[:2]:
                    print(f"     - {error}")
        
        # Test 3: Loading and saving
        print("\n3. Testing load/save:")
        if created_markers:
            test_marker = created_markers[0]
            marker_id = test_marker['id']
            
            # Load the saved marker
            try:
                loaded = tool.load_marker(marker_id)
                print(f"   ✅ Loaded: {loaded['id']}")
            except Exception as e:
                print(f"   ❌ Load error: {e}")
        
        # Test 4: List markers
        print("\n4. Testing marker listing:")
        markers = tool.list_markers()
        print(f"   Found {len(markers)} markers")
        for marker in markers:
            status = "✅" if marker.get('valid', False) else "❌"
            print(f"     {status} {marker.get('id', 'Unknown')}")
        
        # Test 5: Directory validation
        print("\n5. Testing directory validation:")
        validation = tool.validate_directory()
        print(f"   Total: {validation['total']}")
        print(f"   Valid: {validation['valid']}")
        print(f"   Invalid: {validation['invalid']}")
        
        # Test 6: Statistics
        print("\n6. Testing statistics:")
        stats = tool.get_statistics()
        for key, value in stats.items():
            print(f"   {key.title()}: {value}")


def test_convenience_functions():
    """Test the convenience functions."""
    print("\n\n🔧 Testing convenience functions")
    print("=" * 40)
    
    # Test create_marker
    try:
        marker = create_marker(1, "CONVENIENCE_MARKER", "Test User")
        print(f"✅ Created: {marker['id']}")
    except Exception as e:
        print(f"❌ Create error: {e}")
    
    # Test validate_marker
    try:
        is_valid, errors = validate_marker(marker)
        print(f"✅ Validation: {'Valid' if is_valid else 'Invalid'}")
    except Exception as e:
        print(f"❌ Validation error: {e}")
    
    # Test with invalid data
    try:
        invalid_marker = {"id": "INVALID", "level": "wrong"}
        is_valid, errors = validate_marker(invalid_marker)
        print(f"✅ Invalid test: {'Valid' if is_valid else 'Invalid'} (expected Invalid)")
        print(f"   Errors found: {len(errors)}")
    except Exception as e:
        print(f"❌ Invalid test error: {e}")


def test_conversion():
    """Test marker conversion functionality."""
    print("\n\n🔄 Testing marker conversion")
    print("=" * 40)
    
    # Create old format marker
    old_marker = {
        "id": "OLD_CONVERSION_TEST",
        "level": "1",  # String instead of int
        "beschreibung": "Old format description",
        "kategorie": "old_category",
        "examples": ["Old example 1", "Old example 2"]
    }
    
    try:
        tool = MarkerTool()
        converted = tool.convert_old_marker(old_marker)
        print(f"✅ Converted: {converted['id']}")
        print(f"   Level: {converted['level']}")
        print(f"   Category: {converted['category']}")
        print(f"   Examples: {len(converted['examples'])}")
        
        # Validate converted marker
        is_valid, errors = validate_marker(converted)
        print(f"   Valid: {'✅' if is_valid else '❌'}")
        
    except Exception as e:
        print(f"❌ Conversion error: {e}")


def test_error_handling():
    """Test error handling."""
    print("\n\n⚠️ Testing error handling")
    print("=" * 40)
    
    tool = MarkerTool()
    
    # Test invalid level
    try:
        tool.create_marker(5, "INVALID_LEVEL", "Test")
        print("❌ Should have failed with invalid level")
    except ValueError as e:
        print(f"✅ Caught invalid level: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Test empty name
    try:
        tool.create_marker(1, "", "Test")
        print("❌ Should have failed with empty name")
    except ValueError as e:
        print(f"✅ Caught empty name: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Test loading non-existent marker
    try:
        tool.load_marker("NON_EXISTENT_MARKER")
        print("❌ Should have failed loading non-existent marker")
    except FileNotFoundError as e:
        print(f"✅ Caught file not found: FileNotFoundError")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    print("🧪 Comprehensive MarkerTool Test Suite")
    print("=" * 50)
    
    try:
        test_marker_tool()
        test_convenience_functions()
        test_conversion()
        test_error_handling()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        raise
