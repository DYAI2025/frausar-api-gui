#!/usr/bin/env python3
"""
CLI Demo for Lean-Deep v3.1 Marker Functionality
================================================

This demonstrates the new v3.1 marker schema capabilities without requiring a GUI.
"""

import yaml
import argparse
from pathlib import Path
from marker_v3_1_manager import MarkerV31Manager

def main():
    parser = argparse.ArgumentParser(description="Lean-Deep v3.1 Marker CLI Demo")
    parser.add_argument("--create", metavar="LEVEL", type=int, choices=range(1, 5),
                        help="Create template for level (1-4)")
    parser.add_argument("--name", metavar="NAME", type=str, 
                        help="Marker name (UPPER_SNAKE_CASE)")
    parser.add_argument("--author", metavar="AUTHOR", type=str, default="CLI User",
                        help="Author name")
    parser.add_argument("--validate", metavar="FILE", type=str,
                        help="Validate YAML file against v3.1 schema")
    parser.add_argument("--convert", metavar="FILE", type=str,
                        help="Convert old marker file to v3.1")
    parser.add_argument("--output", metavar="DIR", type=str, default="./markers",
                        help="Output directory")
    
    args = parser.parse_args()
    
    manager = MarkerV31Manager()
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    print("🎯 Lean-Deep v3.1 Marker CLI")
    print("=" * 40)
    
    if args.create and args.name:
        # Create new template
        print(f"\n📝 Creating Level {args.create} template: {args.name}")
        
        try:
            template = manager.create_marker_template(args.create, args.name, args.author)
            
            # Validate
            is_valid, errors = manager.validate_marker_schema(template)
            print(f"✅ Template created: {template['id']}")
            print(f"   Category: {template['category']}")
            print(f"   Examples: {len(template['examples'])}")
            print(f"   Validation: {'✅ PASS' if is_valid else '❌ FAIL'}")
            
            if errors:
                for error in errors:
                    print(f"   - {error}")
            
            # Save file
            filename = manager.generate_filename(template['id'])
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(template, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            print(f"💾 Saved: {filepath}")
            
            # Display YAML
            print(f"\n📄 Generated YAML:")
            print("-" * 30)
            yaml_content = yaml.dump(template, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(yaml_content)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    elif args.validate:
        # Validate existing file
        file_path = Path(args.validate)
        print(f"\n🧪 Validating: {file_path}")
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Handle multi-marker files
            blocks = content.split('\n---\n')
            
            for i, block in enumerate(blocks):
                if not block.strip():
                    continue
                    
                print(f"\n--- Block {i+1} ---")
                
                try:
                    data = yaml.safe_load(block.strip())
                    if not data:
                        print("❌ Empty YAML block")
                        continue
                    
                    is_valid, errors = manager.validate_marker_schema(data)
                    
                    marker_id = data.get('id', 'Unknown')
                    level = data.get('level', 'Unknown')
                    category = data.get('category', 'Unknown')
                    examples_count = len(data.get('examples', []))
                    
                    print(f"ID: {marker_id}")
                    print(f"Level: {level}, Category: {category}")
                    print(f"Examples: {examples_count}")
                    print(f"Validation: {'✅ PASS' if is_valid else '❌ FAIL'}")
                    
                    if errors:
                        print("Errors:")
                        for error in errors:
                            print(f"  - {error}")
                
                except yaml.YAMLError as e:
                    print(f"❌ YAML Parse Error: {str(e)}")
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    elif args.convert:
        # Convert old format to v3.1
        file_path = Path(args.convert)
        print(f"\n🔄 Converting to v3.1: {file_path}")
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                old_data = yaml.safe_load(f)
            
            if not old_data:
                print("❌ Empty or invalid YAML")
                return
            
            # Convert to v3.1
            new_data = manager.convert_old_marker_to_v31(old_data)
            
            # Validate result
            is_valid, errors = manager.validate_marker_schema(new_data)
            
            print(f"✅ Converted: {old_data.get('id', 'Unknown')} → {new_data['id']}")
            print(f"   Level: {new_data['level']}")
            print(f"   Category: {new_data['category']}")
            print(f"   Examples: {len(new_data['examples'])}")
            print(f"   Validation: {'✅ PASS' if is_valid else '❌ FAIL'}")
            
            if errors:
                print("Validation errors:")
                for error in errors:
                    print(f"  - {error}")
            
            # Save converted file
            filename = manager.generate_filename(new_data['id'])
            filepath = output_dir / f"converted_{filename}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(new_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            print(f"💾 Saved converted file: {filepath}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    else:
        # Show help and examples
        print("\n💡 Examples:")
        print("  # Create Level 1 atomic marker")
        print("  python cli_demo.py --create 1 --name EXAMPLE_MARKER --author 'Your Name'")
        print()
        print("  # Create Level 2 semantic marker") 
        print("  python cli_demo.py --create 2 --name COMPLEX_ANALYSIS")
        print()
        print("  # Validate existing marker file")
        print("  python cli_demo.py --validate test_markers/A_TEST_LEVEL_1.yaml")
        print()
        print("  # Convert old format to v3.1")
        print("  python cli_demo.py --convert old_marker.yaml")
        print()
        print("📋 v3.1 Schema Requirements:")
        print("  ✓ All mandatory fields (id, level, version, author, etc.)")
        print("  ✓ Level-specific fields (atomic_pattern, composed_of, etc.)")
        print("  ✓ Minimum 5 examples")
        print("  ✓ Proper ID format with level prefixes (A_, S_, C_, MM_)")
        print("  ✓ Category auto-mapping based on level")
        print()
        parser.print_help()

if __name__ == "__main__":
    main()