#!/usr/bin/env python3
"""
MARKER V3.1 MANAGER
==================

Lean-Deep v3.1 / MEWT Enhanced Marker Schema Management
- Four-sided frame logic (signal, concept, pragmatics, narrative)
- Single structure block (pattern | composed_of | detect_class) 
- Unified scoring syntax (logistic with base/weight/decay)
- Clear activation commands

All markers follow the new v3.1 standard with mandatory fields and level-specific extensions.
"""

import yaml
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path


class MarkerV31Manager:
    """Manager for Lean-Deep v3.1 marker schema implementation."""
    
    def __init__(self):
        """Initialize the v3.1 marker manager."""
        self.version = "3.1"
        
        # Marker prefixes by level
        self.level_prefixes = {
            1: "A_",    # Atomic
            2: "S_",    # Semantic  
            3: "C_",    # Cluster
            4: "MM_"    # Meta
        }
        
        # Categories by level
        self.level_categories = {
            1: "ATOMIC",
            2: "SEMANTIC", 
            3: "CLUSTER",
            4: "META"
        }
        
        # Mandatory fields for all markers
        self.mandatory_fields = [
            "id", "level", "version", "author", "created_at", 
            "status", "lang", "name", "description", "category",
            "scoring", "tags", "semantic_grabber_id", "examples"
        ]
        
        # Level-specific fields
        self.level_specific_fields = {
            1: ["atomic_pattern"],
            2: ["composed_of", "rules"],
            3: ["composed_of", "activation_logic"],
            4: ["composed_of", "trigger_threshold"]
        }
        
        # Valid status values
        self.valid_statuses = ["draft", "review", "released"]
        
        # Valid languages
        self.valid_languages = ["de", "en"]
    
    def create_marker_template(self, level: int, marker_name: str, author: str = "Your Name") -> Dict[str, Any]:
        """
        Creates correct template based on level according to v3.1 specifications.
        
        Args:
            level: Marker level (1-4)
            marker_name: Name without prefix (UPPER_SNAKE_CASE)
            author: Creator name
            
        Returns:
            Complete marker template dict
        """
        if level not in self.level_prefixes:
            raise ValueError(f"Invalid level {level}. Must be 1-4.")
        
        # Ensure marker_name is UPPER_SNAKE_CASE
        if not marker_name.isupper() or not marker_name.replace('_', '').isalnum():
            marker_name = marker_name.upper().replace(' ', '_').replace('-', '_')
        
        prefix = self.level_prefixes[level]
        category = self.level_categories[level]
        marker_id = f"{prefix}{marker_name}"
        
        # Base template with all mandatory fields
        template = {
            "id": marker_id,
            "level": level,
            "version": "1.0.0",
            "author": author,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "status": "draft",
            "lang": "de",
            "name": marker_name,
            "description": f"Description for {marker_name}",
            "category": category,
            "scoring": {
                "weight": 1.0,
                "priority": "mid"
            },
            "tags": [],
            "semantic_grabber_id": f"SGR_{marker_name}_01",
            "examples": [
                "Example 1 - basic usage",
                "Example 2 - alternative form", 
                "Example 3 - edge case",
                "Example 4 - complex scenario",
                "Example 5 - boundary condition"
            ]
        }
        
        # Add level-specific fields
        if level == 1:  # Atomic
            template["atomic_pattern"] = []
        elif level == 2:  # Semantic
            template["composed_of"] = []
            template["rules"] = {}
        elif level == 3:  # Cluster
            template["composed_of"] = []
            template["activation_logic"] = "ANY 1"
        elif level == 4:  # Meta
            template["composed_of"] = []
            template["trigger_threshold"] = 1
        
        return template
    
    def validate_marker_schema(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validates marker against new MEWT Enhanced Schema v3.1.
        
        Args:
            data: Marker data dictionary
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check mandatory fields
        for field in self.mandatory_fields:
            if field not in data:
                errors.append(f"Mandatory field missing: {field}")
                continue
                
            value = data[field]
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"Mandatory field empty: {field}")
        
        # Validate specific field formats and values
        if "level" in data:
            level = data["level"]
            if not isinstance(level, int) or level not in range(1, 5):
                errors.append("Level must be integer 1-4")
            else:
                # Check level-specific fields
                required_fields = self.level_specific_fields.get(level, [])
                for field in required_fields:
                    if field not in data:
                        errors.append(f"Level {level} requires field: {field}")
        
        # Validate ID format
        if "id" in data:
            marker_id = data["id"]
            if not isinstance(marker_id, str):
                errors.append("ID must be string")
            elif not marker_id.isupper():
                errors.append("ID must be UPPER_SNAKE_CASE")
            elif level := data.get("level"):
                expected_prefix = self.level_prefixes.get(level, "")
                if not marker_id.startswith(expected_prefix):
                    errors.append(f"Level {level} ID must start with '{expected_prefix}'")
        
        # Validate name matches ID without prefix
        if "id" in data and "name" in data and "level" in data:
            marker_id = data["id"]
            name = data["name"] 
            level = data["level"]
            expected_prefix = self.level_prefixes.get(level, "")
            expected_name = marker_id.replace(expected_prefix, "", 1)
            if name != expected_name:
                errors.append(f"Name '{name}' should match ID without prefix: '{expected_name}'")
        
        # Validate version format (semver)
        if "version" in data:
            version = data["version"]
            if not isinstance(version, str):
                errors.append("Version must be string")
            elif not self._is_valid_semver(version):
                errors.append("Version must be valid semver (e.g., '1.0.0')")
        
        # Validate created_at format  
        if "created_at" in data:
            created_at = data["created_at"]
            if not isinstance(created_at, str):
                errors.append("created_at must be string")
            elif not self._is_valid_date(created_at):
                errors.append("created_at must be YYYY-MM-DD format")
        
        # Validate status
        if "status" in data:
            status = data["status"]
            if status not in self.valid_statuses:
                errors.append(f"Status must be one of: {self.valid_statuses}")
        
        # Validate language
        if "lang" in data:
            lang = data["lang"]
            if lang not in self.valid_languages:
                errors.append(f"Language must be one of: {self.valid_languages}")
        
        # Validate category matches level
        if "category" in data and "level" in data:
            category = data["category"]
            level = data["level"]
            expected_category = self.level_categories.get(level)
            if category != expected_category:
                errors.append(f"Level {level} must have category '{expected_category}', got '{category}'")
        
        # Validate scoring format
        if "scoring" in data:
            scoring = data["scoring"]
            if not isinstance(scoring, dict):
                errors.append("Scoring must be dictionary")
            else:
                if "weight" not in scoring:
                    errors.append("Scoring must contain 'weight'")
                elif not isinstance(scoring["weight"], (int, float)):
                    errors.append("Scoring weight must be number")
                
                if "priority" not in scoring:
                    errors.append("Scoring must contain 'priority'")
        
        # Validate examples (minimum 5 required)
        if "examples" in data:
            examples = data["examples"]
            if not isinstance(examples, list):
                errors.append("Examples must be list")
            elif len(examples) < 5:
                errors.append(f"Minimum 5 examples required, got {len(examples)}")
            elif any(not isinstance(ex, str) or not ex.strip() for ex in examples):
                errors.append("All examples must be non-empty strings")
        
        # Validate semantic_grabber_id uniqueness format
        if "semantic_grabber_id" in data:
            sgr_id = data["semantic_grabber_id"]
            if not isinstance(sgr_id, str):
                errors.append("semantic_grabber_id must be string")
            elif not sgr_id.startswith("SGR_"):
                errors.append("semantic_grabber_id must start with 'SGR_'")
        
        return len(errors) == 0, errors
    
    def generate_filename(self, marker_id: str) -> str:
        """
        Generates correct filename from marker ID.
        
        Args:
            marker_id: Marker ID (e.g., "A_LITTLE_TIME")
            
        Returns:
            Filename (e.g., "A_LITTLE_TIME.yaml")
        """
        return f"{marker_id}.yaml"
    
    def get_level_from_id(self, marker_id: str) -> Optional[int]:
        """
        Extracts level from marker ID based on prefix.
        
        Args:
            marker_id: Marker ID string
            
        Returns:
            Level number or None if invalid
        """
        for level, prefix in self.level_prefixes.items():
            if marker_id.startswith(prefix):
                return level
        return None
    
    def convert_old_marker_to_v31(self, old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts an old marker format to v3.1 schema.
        
        Args:
            old_data: Old marker data
            
        Returns:
            Converted v3.1 marker data
        """
        # Determine level from existing data or ID
        level = old_data.get("level", 1)
        if isinstance(level, str):
            try:
                level = int(level)
            except ValueError:
                level = 1
        
        # Generate marker name from ID or use existing name
        marker_id = old_data.get("id", "UNKNOWN_MARKER")
        if level in self.level_prefixes:
            prefix = self.level_prefixes[level]
            if marker_id.startswith(prefix):
                marker_name = marker_id[len(prefix):]
            else:
                marker_name = marker_id
                marker_id = f"{prefix}{marker_name}"
        else:
            marker_name = marker_id.replace("A_", "").replace("S_", "").replace("C_", "").replace("MM_", "")
        
        # Create new template
        author = old_data.get("author", "Migration")
        new_data = self.create_marker_template(level, marker_name, author)
        
        # Preserve existing values where possible
        preserve_fields = [
            "description", "version", "author", "created_at", 
            "status", "lang", "tags", "examples"
        ]
        
        for field in preserve_fields:
            if field in old_data and old_data[field]:
                new_data[field] = old_data[field]
        
        # Handle old category mapping
        if "kategorie" in old_data:
            new_data["category"] = self.level_categories[level]
        elif "category" in old_data:
            new_data["category"] = self.level_categories[level]
        
        # Ensure minimum examples
        if len(new_data.get("examples", [])) < 5:
            existing_examples = new_data.get("examples", [])
            while len(existing_examples) < 5:
                existing_examples.append(f"Example {len(existing_examples) + 1}")
            new_data["examples"] = existing_examples
        
        return new_data
    
    def adapt_marker_to_v31_with_report(self, marker_data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Adapts a marker to v3.1 format with detailed change reporting.
        
        Args:
            marker_data: Original marker data
            
        Returns:
            Tuple of (adapted_data, changes_report)
        """
        original_data = marker_data.copy()
        changes_report = {
            "added": [],
            "removed": [],
            "modified": [],
            "preserved": [],
            "warnings": []
        }
        
        # Start with conversion
        adapted_data = self.convert_old_marker_to_v31(marker_data)
        
        # Analyze changes
        original_keys = set(original_data.keys())
        adapted_keys = set(adapted_data.keys())
        
        # Track added fields
        added_keys = adapted_keys - original_keys
        for key in added_keys:
            changes_report["added"].append({
                "field": key,
                "value": adapted_data[key],
                "reason": f"Required by v3.1 schema"
            })
        
        # Track removed fields
        removed_keys = original_keys - adapted_keys
        for key in removed_keys:
            changes_report["removed"].append({
                "field": key,
                "value": original_data[key],
                "reason": f"Not part of v3.1 schema"
            })
        
        # Track modified fields
        common_keys = original_keys & adapted_keys
        for key in common_keys:
            original_value = original_data[key]
            adapted_value = adapted_data[key]
            
            if original_value != adapted_value:
                changes_report["modified"].append({
                    "field": key,
                    "original_value": original_value,
                    "new_value": adapted_value,
                    "reason": f"Adapted to v3.1 requirements"
                })
            else:
                changes_report["preserved"].append({
                    "field": key,
                    "value": original_value
                })
        
        # Add specific warnings for content preservation
        if "examples" in adapted_data:
            original_examples = original_data.get("examples", [])
            adapted_examples = adapted_data["examples"]
            
            if len(adapted_examples) > len(original_examples):
                changes_report["warnings"].append(
                    f"Added {len(adapted_examples) - len(original_examples)} placeholder examples to meet minimum requirement"
                )
        
        # Check for old German field names
        german_fields = ["kategorie", "beschreibung", "erstellungsdatum"]
        for field in german_fields:
            if field in original_data:
                changes_report["warnings"].append(
                    f"German field '{field}' was converted to English equivalent"
                )
        
        return adapted_data, changes_report
    
    def validate_content_boundaries(self, marker_data: Dict[str, Any]) -> List[str]:
        """
        Validates content boundaries and structure integrity.
        
        Args:
            marker_data: Marker data to validate
            
        Returns:
            List of boundary validation warnings
        """
        warnings = []
        
        # Check for content completeness
        required_content_fields = ["description", "examples"]
        for field in required_content_fields:
            if field not in marker_data or not marker_data[field]:
                warnings.append(f"Missing or empty required content field: {field}")
            elif isinstance(marker_data[field], str) and len(marker_data[field].strip()) < 10:
                warnings.append(f"Content field '{field}' appears incomplete (too short)")
        
        # Check examples quality
        if "examples" in marker_data:
            examples = marker_data["examples"]
            if isinstance(examples, list):
                for i, example in enumerate(examples):
                    if not isinstance(example, str) or len(example.strip()) < 5:
                        warnings.append(f"Example {i+1} appears incomplete or too short")
                    elif example.strip().lower() in ["example", "todo", "tbd", "placeholder"]:
                        warnings.append(f"Example {i+1} appears to be a placeholder")
        
        # Check for consistent field types
        expected_types = {
            "level": int,
            "version": str,
            "created_at": str,
            "tags": list,
            "examples": list,
            "scoring": dict
        }
        
        for field, expected_type in expected_types.items():
            if field in marker_data:
                if not isinstance(marker_data[field], expected_type):
                    warnings.append(f"Field '{field}' has incorrect type: expected {expected_type.__name__}")
        
        return warnings
    
    def _is_valid_semver(self, version: str) -> bool:
        """Check if version string is valid semver format."""
        try:
            parts = version.split('.')
            if len(parts) != 3:
                return False
            for part in parts:
                int(part)  # Should not raise exception
            return True
        except (ValueError, AttributeError):
            return False
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Check if date string is valid YYYY-MM-DD format."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False


# Test function
def test_marker_v31_manager():
    """Test the v3.1 marker manager functionality."""
    manager = MarkerV31Manager()
    
    print("Testing Marker V3.1 Manager...")
    
    # Test template creation for each level
    for level in range(1, 5):
        print(f"\n--- Testing Level {level} ---")
        template = manager.create_marker_template(level, "TEST_MARKER", "Test Author")
        print(f"Template ID: {template['id']}")
        print(f"Category: {template['category']}")
        
        # Test validation
        is_valid, errors = manager.validate_marker_schema(template)
        print(f"Validation: {'✅ PASS' if is_valid else '❌ FAIL'}")
        if errors:
            for error in errors:
                print(f"  - {error}")
        
        # Test filename generation
        filename = manager.generate_filename(template['id'])
        print(f"Filename: {filename}")
    
    print("\n--- Testing Invalid Marker ---")
    invalid_marker = {"id": "invalid", "level": "wrong"}
    is_valid, errors = manager.validate_marker_schema(invalid_marker)
    print(f"Validation: {'✅ PASS' if is_valid else '❌ FAIL'}")
    for error in errors[:5]:  # Show first 5 errors
        print(f"  - {error}")
    
    print("\nV3.1 Manager test completed!")


if __name__ == "__main__":
    test_marker_v31_manager()