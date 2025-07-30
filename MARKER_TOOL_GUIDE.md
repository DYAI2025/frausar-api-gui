# Marker Tool - Unified Interface

The `marker_tool.py` module provides a unified, high-level interface for all marker operations in the Lean-Deep v3.1 / MEWT Enhanced schema system.

## Features

- **Easy marker creation** with templates for all levels (1-4)
- **Comprehensive validation** against v3.1 schema
- **Format conversion** from old formats to v3.1
- **Batch operations** for processing multiple markers
- **File I/O management** with automatic directory handling
- **Error handling and reporting** with detailed feedback
- **Statistics tracking** for operation monitoring

## Quick Start

### Simple Usage

```python
from marker_tool import create_marker, validate_marker, convert_marker

# Create a new marker
marker = create_marker(1, "MY_MARKER", "Author Name")

# Validate a marker
is_valid, errors = validate_marker(marker)

# Convert old format to v3.1
converted = convert_marker(old_marker_data)
```

### Advanced Usage

```python
from marker_tool import MarkerTool

# Create tool instance
tool = MarkerTool("./my_markers")

# Create marker with custom options
marker = tool.create_marker(
    level=2,
    name="COMPLEX_MARKER",
    author="Your Name",
    description="Custom description",
    examples=[
        "Custom example 1",
        "Custom example 2",
        "Custom example 3",
        "Custom example 4",
        "Custom example 5"
    ]
)

# Load existing marker
loaded = tool.load_marker("A_EXISTING_MARKER")

# List all markers
markers = tool.list_markers()
for marker in markers:
    print(f"{marker['id']}: {'✅' if marker['valid'] else '❌'}")

# Validate entire directory
validation = tool.validate_directory()
print(f"Valid: {validation['valid']}/{validation['total']}")

# Batch convert old format markers
results = tool.batch_convert("./old_markers", "./converted_markers")
print(f"Converted: {results['converted']}/{results['total']}")
```

## API Reference

### MarkerTool Class

#### Constructor
- `MarkerTool(marker_directory="./markers")` - Initialize with marker directory

#### Marker Operations
- `create_marker(level, name, author, description=None, examples=None, save=True)` - Create new marker
- `validate_marker(marker_data)` - Validate marker against v3.1 schema
- `load_marker(identifier)` - Load marker from file
- `save_marker(marker_data, filename=None)` - Save marker to file
- `convert_old_marker(old_data, save=True)` - Convert old format to v3.1

#### Batch Operations
- `list_markers(pattern="*.yaml")` - List all markers in directory
- `validate_directory(directory=None)` - Validate all markers in directory
- `batch_convert(source_directory, target_directory=None)` - Convert multiple markers

#### Utility
- `get_statistics()` - Get operation statistics
- `reset_statistics()` - Reset statistics

### Convenience Functions

- `create_marker(level, name, author, **kwargs)` - Quick marker creation
- `validate_marker(marker_data)` - Quick validation
- `convert_marker(old_data)` - Quick conversion

## Integration

The marker tool integrates seamlessly with existing components:

- **marker_v3_1_manager.py** - Uses the core manager for schema operations
- **smart_marker_gui.py** - Can be enhanced to use marker_tool for operations
- **cli_demo.py** - Continues to work with existing functionality
- **test_v3_1_functionality.py** - Validates the underlying schema system

## Error Handling

The tool provides comprehensive error handling:

```python
try:
    marker = tool.create_marker(5, "INVALID_LEVEL", "Test")
except ValueError as e:
    print(f"Validation error: {e}")
except RuntimeError as e:
    print(f"Creation error: {e}")
```

## Examples

### Create Level 1 Atomic Marker
```python
marker = create_marker(
    level=1,
    name="TIME_PRESSURE",
    author="Researcher",
    description="Atomic marker for time pressure indicators",
    examples=[
        "wenig Zeit haben",
        "unter Zeitdruck stehen", 
        "schnell machen müssen",
        "keine Zeit für Details",
        "deadline approaching"
    ]
)
```

### Validate Existing Markers
```python
tool = MarkerTool()
validation = tool.validate_directory()

for marker in validation['markers']:
    if not marker['valid']:
        print(f"❌ {marker['id']}: {', '.join(marker['errors'][:2])}")
```

### Convert Old Format
```python
# Convert single old marker
old_marker = {
    "id": "OLD_MARKER",
    "level": "2",
    "beschreibung": "Old description",
    "kategorie": "emotional"
}

converted = convert_marker(old_marker)
print(f"Converted: {converted['id']}")
```

## Testing

Run the comprehensive test suite:

```bash
python test_marker_tool.py
```

Test integration:

```bash
python marker_tool.py
```

The tool includes built-in testing and validation to ensure reliability and compatibility with the v3.1 schema system.