# Codex Agent Instructions: Frausar Marker Engine/GUI

This repository hosts the new API/GUI implementation for the Frausar system. The goal is to implement a robust marker management interface (the Marker Engine/GUI) that allows users to create, edit and validate marker definitions stored as YAML files.

## Features

1. **Marker Creation**
   - Provide a GUI (PyQt5/6 or Streamlit) allowing users to add markers individually.
   - Support bulk import of multiple YAML marker blocks separated by `---`.
   - Validate YAML syntax and required fields on input.
   - Attempt automatic fixes for common typos or missing fields. Display all unresolved issues with line number and suggestions.
   - Save each valid marker to a separate YAML file (`<id>.yaml` or `<markername>.yaml`) in the configured marker directory.

2. **Marker Display & Edit**
   - Offer a list of existing markers.
   - Open any marker in the editor to view or modify the YAML. Run validation before saving updates.
   - Detect invalid or corrupt YAML files and flag them clearly without crashing the GUI.

3. **Error Handling**
   - Implement a mapping of common field mistakes to valid names for auto-repair (e.g. `kategorie` → `category`).
   - For unresolved errors provide an interactive list of issues with line numbers and suggestions for manual correction.

4. **Architecture**
   - Python ≥3.9 with PyQt5/6 or Streamlit for the GUI.
   - Use `ruamel.yaml` or `pyyaml` for YAML parsing.
   - All repair and validation logic should be encapsulated in reusable modules so other parts of the Frausar system (e.g. API layer) can leverage them.
   - Design the code to allow future REST API endpoints.
   - Write unit tests for core functions: marker creation, bulk import, auto-correction, file IO.

5. **Usability**
   - Provide clear feedback when importing markers in bulk (e.g. "5 successful, 2 errors – see details").
   - Ensure the GUI remains responsive and never fails silently on errors.
   - Keep interface simple and intuitive.

6. **Future Proofing**
   - Organize modules so additional features (e.g. API endpoints or more complex workflows) can be integrated easily.
   - Keep documentation up to date with inline comments and docstrings.

## Development Notes

- When implementing new features, follow best practices with descriptive commit messages.
- Run available tests (`pytest`) before committing changes. If tests are added later, they must also be executed.
- If dependencies are required, include them in the project's `requirements_ai.txt` or a separate `requirements.txt`.
- This AGENTS.md file is the baseline instruction for Codex. No other AGENTS.md files currently override these instructions.

