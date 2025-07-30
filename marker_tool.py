#!/usr/bin/env python3
"""
MARKER TOOL - Unified Interface for Lean-Deep v3.1 Marker Operations
=====================================================================

This module provides a unified, high-level interface for all marker operations
in the Lean-Deep v3.1 / MEWT Enhanced schema system.

Features:
- Easy marker creation and templates
- Comprehensive validation
- Format conversion (old to v3.1)
- Batch operations
- File I/O management
- Error handling and reporting
"""

import yaml
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Union
from datetime import datetime

from marker_v3_1_manager import MarkerV31Manager


class MarkerTool:
    """
    High-level interface for marker operations using Lean-Deep v3.1 schema.
    
    This class provides a simple, intuitive API for working with markers
    while abstracting the complexity of the underlying v3.1 schema management.
    """
    
    def __init__(self, marker_directory: str = "./markers"):
        """
        Initialize the MarkerTool.
        
        Args:
            marker_directory: Directory to store marker files (default: "./markers")
        """
        self.manager = MarkerV31Manager()
        self.marker_dir = Path(marker_directory)
        self.marker_dir.mkdir(exist_ok=True)
        
        # Statistics tracking
        self.stats = {
            'created': 0,
            'validated': 0,
            'errors': 0,
            'converted': 0
        }
    
    def create_marker(self, level: int, name: str, author: str = "Unknown", 
                     description: str = None, examples: List[str] = None,
                     save: bool = True) -> Dict[str, Any]:
        """
        Create a new marker with the v3.1 schema.
        
        Args:
            level: Marker level (1-4)
            name: Marker name (will be converted to UPPER_SNAKE_CASE)
            author: Creator name
            description: Optional description (auto-generated if None)
            examples: Optional list of examples (defaults provided if None)
            save: Whether to save to file immediately
            
        Returns:
            Created marker data dictionary
            
        Raises:
            ValueError: If level is invalid or name is empty
            RuntimeError: If marker creation fails
        """
        if not name or not name.strip():
            raise ValueError("Marker name cannot be empty")
        
        if level not in range(1, 5):
            raise ValueError(f"Level must be 1-4, got {level}")
        
        try:
            # Clean and format name
            clean_name = self._clean_name(name)
            
            # Create template
            marker = self.manager.create_marker_template(level, clean_name, author)
            
            # Override description if provided
            if description:
                marker['description'] = description
            
            # Override examples if provided
            if examples:
                if len(examples) < 5:
                    # Pad with default examples if less than 5
                    examples.extend([f"Example {i+len(examples)+1}" for i in range(5-len(examples))])
                marker['examples'] = examples
            
            # Validate the created marker
            is_valid, errors = self.manager.validate_marker_schema(marker)
            if not is_valid:
                raise RuntimeError(f"Created marker validation failed: {', '.join(errors)}")
            
            # Save if requested
            if save:
                self.save_marker(marker)
            
            self.stats['created'] += 1
            return marker
            
        except Exception as e:
            self.stats['errors'] += 1
            raise RuntimeError(f"Failed to create marker: {str(e)}")
    
    def validate_marker(self, marker_data: Union[Dict[str, Any], str, Path]) -> Tuple[bool, List[str]]:
        """
        Validate a marker against the v3.1 schema.
        
        Args:
            marker_data: Marker data (dict, YAML string, or file path)
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            # Handle different input types
            if isinstance(marker_data, (str, Path)):
                if Path(marker_data).exists():
                    # It's a file path
                    with open(marker_data, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                else:
                    # It's a YAML string
                    data = yaml.safe_load(marker_data)
            else:
                # It's already a dict
                data = marker_data
            
            if not data:
                return False, ["Empty or invalid YAML data"]
            
            # Validate using manager
            is_valid, errors = self.manager.validate_marker_schema(data)
            self.stats['validated'] += 1
            
            if not is_valid:
                self.stats['errors'] += 1
            
            return is_valid, errors
            
        except Exception as e:
            self.stats['errors'] += 1
            return False, [f"Validation error: {str(e)}"]
    
    def load_marker(self, identifier: Union[str, Path]) -> Dict[str, Any]:
        """
        Load a marker from file.
        
        Args:
            identifier: Marker ID, filename, or full path
            
        Returns:
            Marker data dictionary
            
        Raises:
            FileNotFoundError: If marker file not found
            RuntimeError: If loading fails
        """
        try:
            # Try to resolve the file path
            file_path = self._resolve_marker_path(identifier)
            
            if not file_path.exists():
                raise FileNotFoundError(f"Marker file not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                raise RuntimeError("Empty or invalid marker file")
            
            return data
            
        except FileNotFoundError:
            raise
        except Exception as e:
            self.stats['errors'] += 1
            raise RuntimeError(f"Failed to load marker: {str(e)}")
    
    def save_marker(self, marker_data: Dict[str, Any], 
                   filename: str = None) -> Path:
        """
        Save a marker to file.
        
        Args:
            marker_data: Marker data dictionary
            filename: Optional custom filename (auto-generated if None)
            
        Returns:
            Path to saved file
            
        Raises:
            ValueError: If marker data is invalid
            RuntimeError: If saving fails
        """
        try:
            # Validate before saving
            is_valid, errors = self.validate_marker(marker_data)
            if not is_valid:
                raise ValueError(f"Cannot save invalid marker: {', '.join(errors)}")
            
            # Generate filename if not provided
            if filename is None:
                filename = self.manager.generate_filename(marker_data['id'])
            
            file_path = self.marker_dir / filename
            
            # Save with proper formatting
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(marker_data, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
            
            return file_path
            
        except Exception as e:
            self.stats['errors'] += 1
            raise RuntimeError(f"Failed to save marker: {str(e)}")
    
    def convert_old_marker(self, old_data: Union[Dict[str, Any], str, Path],
                          save: bool = True) -> Dict[str, Any]:
        """
        Convert an old format marker to v3.1.
        
        Args:
            old_data: Old marker data (dict, YAML string, or file path)
            save: Whether to save converted marker
            
        Returns:
            Converted marker data
            
        Raises:
            RuntimeError: If conversion fails
        """
        try:
            # Handle different input types
            if isinstance(old_data, (str, Path)):
                if Path(old_data).exists():
                    with open(old_data, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                else:
                    data = yaml.safe_load(old_data)
            else:
                data = old_data
            
            if not data:
                raise RuntimeError("Empty or invalid old marker data")
            
            # Convert using manager
            converted = self.manager.convert_old_marker_to_v31(data)
            
            # Validate conversion result
            is_valid, errors = self.validate_marker(converted)
            if not is_valid:
                raise RuntimeError(f"Conversion produced invalid marker: {', '.join(errors)}")
            
            # Save if requested
            if save:
                self.save_marker(converted)
            
            self.stats['converted'] += 1
            return converted
            
        except Exception as e:
            self.stats['errors'] += 1
            raise RuntimeError(f"Failed to convert marker: {str(e)}")
    
    def list_markers(self, pattern: str = "*.yaml") -> List[Dict[str, Any]]:
        """
        List all markers in the marker directory.
        
        Args:
            pattern: File pattern to match (default: "*.yaml")
            
        Returns:
            List of marker info dictionaries
        """
        markers = []
        
        try:
            for file_path in self.marker_dir.glob(pattern):
                try:
                    data = self.load_marker(file_path)
                    info = {
                        'file': file_path.name,
                        'path': str(file_path),
                        'id': data.get('id', 'Unknown'),
                        'level': data.get('level', 'Unknown'),
                        'category': data.get('category', 'Unknown'),
                        'author': data.get('author', 'Unknown'),
                        'examples_count': len(data.get('examples', [])),
                        'valid': self.validate_marker(data)[0]
                    }
                    markers.append(info)
                except Exception as e:
                    # Add error marker entry
                    markers.append({
                        'file': file_path.name,
                        'path': str(file_path),
                        'id': 'ERROR',
                        'error': str(e),
                        'valid': False
                    })
        
        except Exception as e:
            self.stats['errors'] += 1
            
        return markers
    
    def validate_directory(self, directory: str = None) -> Dict[str, Any]:
        """
        Validate all markers in a directory.
        
        Args:
            directory: Directory path (uses marker_dir if None)
            
        Returns:
            Validation summary dictionary
        """
        if directory:
            target_dir = Path(directory)
        else:
            target_dir = self.marker_dir
        
        results = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'errors': [],
            'markers': []
        }
        
        try:
            for file_path in target_dir.glob("*.yaml"):
                results['total'] += 1
                
                try:
                    data = self.load_marker(file_path)
                    is_valid, errors = self.validate_marker(data)
                    
                    marker_result = {
                        'file': file_path.name,
                        'id': data.get('id', 'Unknown'),
                        'valid': is_valid,
                        'errors': errors
                    }
                    
                    results['markers'].append(marker_result)
                    
                    if is_valid:
                        results['valid'] += 1
                    else:
                        results['invalid'] += 1
                        results['errors'].extend(errors)
                
                except Exception as e:
                    results['invalid'] += 1
                    error_msg = f"{file_path.name}: {str(e)}"
                    results['errors'].append(error_msg)
                    results['markers'].append({
                        'file': file_path.name,
                        'valid': False,
                        'errors': [str(e)]
                    })
        
        except Exception as e:
            self.stats['errors'] += 1
            results['errors'].append(f"Directory validation error: {str(e)}")
        
        return results
    
    def batch_convert(self, source_directory: str, 
                     target_directory: str = None) -> Dict[str, Any]:
        """
        Convert all old format markers in a directory to v3.1.
        
        Args:
            source_directory: Directory containing old format markers
            target_directory: Directory to save converted markers (uses marker_dir if None)
            
        Returns:
            Conversion summary dictionary
        """
        source_dir = Path(source_directory)
        target_dir = Path(target_directory) if target_directory else self.marker_dir
        target_dir.mkdir(exist_ok=True)
        
        results = {
            'total': 0,
            'converted': 0,
            'failed': 0,
            'errors': [],
            'converted_files': []
        }
        
        try:
            for file_path in source_dir.glob("*.yaml"):
                results['total'] += 1
                
                try:
                    # Load old marker
                    with open(file_path, 'r', encoding='utf-8') as f:
                        old_data = yaml.safe_load(f)
                    
                    # Convert to v3.1
                    converted = self.convert_old_marker(old_data, save=False)
                    
                    # Save to target directory
                    target_file = target_dir / self.manager.generate_filename(converted['id'])
                    with open(target_file, 'w', encoding='utf-8') as f:
                        yaml.dump(converted, f, default_flow_style=False,
                                 allow_unicode=True, sort_keys=False)
                    
                    results['converted'] += 1
                    results['converted_files'].append({
                        'source': str(file_path),
                        'target': str(target_file),
                        'id': converted['id']
                    })
                
                except Exception as e:
                    results['failed'] += 1
                    error_msg = f"{file_path.name}: {str(e)}"
                    results['errors'].append(error_msg)
        
        except Exception as e:
            self.stats['errors'] += 1
            results['errors'].append(f"Batch conversion error: {str(e)}")
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get operation statistics.
        
        Returns:
            Statistics dictionary
        """
        return self.stats.copy()
    
    def reset_statistics(self) -> None:
        """Reset operation statistics."""
        self.stats = {
            'created': 0,
            'validated': 0,
            'errors': 0,
            'converted': 0
        }
    
    def _clean_name(self, name: str) -> str:
        """Clean and format marker name to UPPER_SNAKE_CASE."""
        # Remove any non-alphanumeric characters except spaces and underscores
        cleaned = re.sub(r'[^a-zA-Z0-9\s_]', '', name.strip())
        
        # Replace spaces with underscores
        cleaned = cleaned.replace(' ', '_')
        
        # Convert to uppercase
        cleaned = cleaned.upper()
        
        # Remove multiple consecutive underscores
        cleaned = re.sub(r'_{2,}', '_', cleaned)
        
        # Remove leading/trailing underscores
        cleaned = cleaned.strip('_')
        
        if not cleaned:
            raise ValueError("Marker name contains no valid characters")
        
        return cleaned
    
    def _resolve_marker_path(self, identifier: Union[str, Path]) -> Path:
        """Resolve marker identifier to file path."""
        if isinstance(identifier, Path):
            return identifier
        
        # If it's already a full path
        path = Path(identifier)
        if path.is_absolute() and path.exists():
            return path
        
        # Try as filename in marker directory
        if identifier.endswith('.yaml'):
            return self.marker_dir / identifier
        
        # Try as marker ID
        return self.marker_dir / f"{identifier}.yaml"


# Convenience functions for easy usage
def create_marker(level: int, name: str, author: str = "Unknown", **kwargs) -> Dict[str, Any]:
    """
    Quick marker creation function.
    
    Args:
        level: Marker level (1-4)
        name: Marker name
        author: Creator name
        **kwargs: Additional arguments for MarkerTool.create_marker()
        
    Returns:
        Created marker data
    """
    tool = MarkerTool()
    return tool.create_marker(level, name, author, **kwargs)


def validate_marker(marker_data: Union[Dict[str, Any], str, Path]) -> Tuple[bool, List[str]]:
    """
    Quick marker validation function.
    
    Args:
        marker_data: Marker data to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    tool = MarkerTool()
    return tool.validate_marker(marker_data)


def convert_marker(old_data: Union[Dict[str, Any], str, Path]) -> Dict[str, Any]:
    """
    Quick marker conversion function.
    
    Args:
        old_data: Old format marker data
        
    Returns:
        Converted v3.1 marker data
    """
    tool = MarkerTool()
    return tool.convert_old_marker(old_data)


# Example usage and testing
if __name__ == "__main__":
    print("🛠️ Marker Tool v3.1 - Unified Interface")
    print("=" * 40)
    
    # Create tool instance
    tool = MarkerTool()
    
    # Example: Create a new marker
    print("\n📝 Creating example marker...")
    try:
        marker = tool.create_marker(
            level=1,
            name="TEST_MARKER_TOOL",
            author="Marker Tool",
            description="Test marker created by marker_tool.py",
            examples=[
                "Example 1 - demonstration",
                "Example 2 - testing functionality", 
                "Example 3 - validation check",
                "Example 4 - integration test",
                "Example 5 - final verification"
            ]
        )
        print(f"✅ Created marker: {marker['id']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example: List markers
    print("\n📋 Listing markers...")
    markers = tool.list_markers()
    for marker in markers[:3]:  # Show first 3
        status = "✅" if marker.get('valid', False) else "❌"
        print(f"   {status} {marker.get('id', 'Unknown')} - {marker.get('file', 'Unknown')}")
    
    if len(markers) > 3:
        print(f"   ... and {len(markers) - 3} more")
    
    # Example: Validate directory
    print("\n🧪 Validating marker directory...")
    validation = tool.validate_directory()
    print(f"   Total: {validation['total']}, Valid: {validation['valid']}, Invalid: {validation['invalid']}")
    
    # Show statistics
    print("\n📊 Statistics:")
    stats = tool.get_statistics()
    for key, value in stats.items():
        print(f"   {key.title()}: {value}")
    
    print("\n✅ Marker Tool test completed!")