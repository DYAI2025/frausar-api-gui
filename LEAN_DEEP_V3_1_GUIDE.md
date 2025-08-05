# Lean-Deep v3.1 / MEWT Enhanced Marker Schema

## 🎯 Overview

The new Lean-Deep v3.1 marker schema provides a standardized, comprehensive format for all marker types. Every marker follows the four-sided frame logic and unified structure requirements.

## 📋 Schema Requirements

### Mandatory Fields (All Levels)

All markers **must** include these 14 fields in the exact order:

1. `id` - EN, UPPER_SNAKE_CASE with level prefix (e.g., "A_LITTLE_TIME")
2. `level` - Integer 1-4 (1=Atomic, 2=Semantic, 3=Cluster, 4=Meta)  
3. `version` - Semver format (e.g., "1.0.0")
4. `author` - Creator name (Firstname, Nick, or Team)
5. `created_at` - Date in YYYY-MM-DD format
6. `status` - One of: "draft", "review", "released"
7. `lang` - Language code: "de" or "en"
8. `name` - UPPER_SNAKE_CASE, identical to ID without prefix
9. `description` - Brief description (DE/EN)
10. `category` - Auto-mapped: "ATOMIC", "SEMANTIC", "CLUSTER", "META"
11. `scoring` - Object with `weight` (number) and `priority` (string)
12. `tags` - Array of strings
13. `semantic_grabber_id` - Unique ID (e.g., "SGR_LITTLE_TIME_01")
14. `examples` - Array with **minimum 5 varied examples**

### Level-Specific Fields

#### Level 1 (Atomic)
- `atomic_pattern` - Array defining atomic patterns

#### Level 2 (Semantic)  
- `composed_of` - Array of component references
- `rules` - Object with semantic rules

#### Level 3 (Cluster)
- `composed_of` - Array of component references  
- `activation_logic` - String with logic (e.g., "ANY 1", "SUM(weight)>=0.7 WITHIN 48h")

#### Level 4 (Meta)
- `composed_of` - Array of component references
- `trigger_threshold` - Number for threshold

## 🏗️ Framework Principles

### Four-Sided Frame Logic
Every marker incorporates:
- **Signal** - Detection patterns
- **Concept** - Semantic meaning
- **Pragmatics** - Context usage  
- **Narrative** - Story structure

### Single Structure Block
Each marker has exactly one of:
- `pattern` (atomic detection)
- `composed_of` (semantic composition)
- `detect_class` (classification logic)

### Unified Scoring Syntax
Logistic scoring with:
- `base` - Base score
- `weight` - Weighting factor
- `decay` - Decay parameters

### Clear Activation Commands
Examples:
- `"ANY 1"` - Any single match triggers
- `"SUM(weight)>=0.7 WITHIN 48h"` - Weighted sum threshold within timeframe
- `"ALL 3"` - All three components required

## 🚀 Usage Examples

### Creating Templates

```python
from marker_v3_1_manager import MarkerV31Manager

manager = MarkerV31Manager()

# Level 1 Atomic Marker
atomic_marker = manager.create_marker_template(1, "ISOLATION_SIGNAL", "Author Name")

# Level 2 Semantic Marker  
semantic_marker = manager.create_marker_template(2, "EMOTIONAL_CONTEXT", "Author Name")

# Level 3 Cluster Marker
cluster_marker = manager.create_marker_template(3, "BEHAVIOR_CLUSTER", "Author Name")

# Level 4 Meta Marker
meta_marker = manager.create_marker_template(4, "PATTERN_META", "Author Name")
```

### Validation

```python
# Validate against v3.1 schema
is_valid, errors = manager.validate_marker_schema(marker_data)

if not is_valid:
    for error in errors:
        print(f"❌ {error}")
```

### Converting Old Formats

```python
# Convert old marker to v3.1
old_data = yaml.safe_load(old_yaml_content)
new_data = manager.convert_old_marker_to_v31(old_data)
```

## 🛠️ Tools

### GUI Application
Run the enhanced Smart Marker GUI:
```bash
python smart_marker_gui.py
```

Features:
- Level selection dropdown (1-4)
- Category auto-fill based on level
- Template generator for each level
- Real-time v3.1 schema validation
- Conversion tools for old formats
- Enforced minimum 5 examples

### CLI Tool  
Use the command-line interface:
```bash
# Create new marker
python cli_demo.py --create 1 --name EXAMPLE_MARKER --author "Your Name"

# Validate existing marker
python cli_demo.py --validate path/to/marker.yaml

# Convert old format
python cli_demo.py --convert old_marker.yaml
```

### Batch Testing
Run comprehensive tests:
```bash
python test_v3_1_functionality.py
```

## 📄 Example Marker

```yaml
id: A_LITTLE_TIME
level: 1
version: 1.0.0
author: DYAI2025
created_at: '2025-07-28'
status: draft
lang: de
name: LITTLE_TIME
description: Atomic marker for time-related expressions
category: ATOMIC
scoring:
  weight: 1.0
  priority: mid
tags: []
semantic_grabber_id: SGR_LITTLE_TIME_01
examples:
- "wenig Zeit haben"
- "keine Zeit"
- "Zeitdruck"
- "schnell machen müssen"
- "unter Zeitnot stehen"
atomic_pattern: []
```

## ✅ Validation Rules

The v3.1 schema enforces:

1. **Field Completeness**: All 14 mandatory fields present
2. **Type Safety**: Correct data types for all fields
3. **Format Validation**: 
   - ID in UPPER_SNAKE_CASE with correct prefix
   - Version in semver format (x.y.z)
   - Date in YYYY-MM-DD format
4. **Level Consistency**: 
   - Category matches level
   - Required level-specific fields present
5. **Quality Requirements**:
   - Minimum 5 examples
   - Non-empty required fields
6. **Uniqueness**: semantic_grabber_id follows pattern

## 🔄 Migration Guide

### From Old Format
Old markers are automatically converted:
- Level extracted from existing data or inferred
- ID gets proper prefix based on level
- Category auto-mapped to v3.1 standards
- Missing fields filled with defaults
- Examples padded to minimum 5

### Breaking Changes
- `kategorie` → `category` (with fixed values)
- Level must be integer 1-4
- ID format enforced (UPPER_SNAKE_CASE with prefixes)
- Minimum 5 examples required
- Additional mandatory fields

## 🎯 Benefits

- **Standardization**: All markers follow same structure
- **Validation**: Comprehensive error checking
- **Interoperability**: Consistent format across tools
- **Quality**: Enforced minimums (5 examples)
- **Scalability**: Clear level hierarchy
- **Automation**: Template generation and conversion

## 📞 Support

The v3.1 implementation includes:
- Detailed error messages for validation failures
- Automatic conversion from old formats
- Template generation for all levels
- CLI and GUI tools for easy usage
- Comprehensive test suite for validation
