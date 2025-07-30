#!/usr/bin/env python3
"""
ROBUST MARKER GUI - LEAN-DEEP V3.1 ENHANCED
==========================================

Eine moderne, robuste GUI für die professionelle Verwaltung von Lean-Deep v3.1 Markern.
- Modernes, intuitives Design mit deutlich verbesserter UX/UI
- Einheitliches Fenster mit klar strukturierten Bereichen  
- Robuste Marker-Anpassung mit Backup/Undo-Funktionalität
- Umfassender Vorschau-Modus mit detaillierter Analyse
- Präzise Änderungsberichte (hinzugefügt/entfernt)
- Vollständige Lean-Deep 3.1 Kompatibilität mit Inhaltsschutz
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import yaml
import os
import re
import uuid
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from marker_v3_1_manager import MarkerV31Manager

class RobustMarkerGUI:
    """Robuste, moderne GUI für Lean-Deep v3.1 Marker-Verwaltung."""
    
    def __init__(self):
        """Initialize the robust marker GUI."""
        self.root = tk.Tk()
        self.root.title("🎯 Robust Marker GUI - Lean-Deep v3.1 Professional")
        self.root.geometry("1600x1000")
        self.root.minsize(1200, 800)
        
        # Core managers
        self.v31_manager = MarkerV31Manager()
        
        # Directories
        self.marker_dir = Path.cwd() / "markers"
        self.backup_dir = Path.cwd() / "backups"
        self.marker_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        # State management
        self.current_marker_data = None
        self.current_marker_file = None
        self.backup_stack = []  # For undo functionality
        self.unsaved_changes = False
        self.preview_mode = False
        
        # UI Variables
        self.setup_variables()
        
        # Initialize UI
        self.setup_modern_ui()
        self.setup_styles()
        self.refresh_marker_list()
        
        # Bind events
        self.setup_event_bindings()
        
    def setup_variables(self):
        """Setup UI control variables."""
        self.search_var = tk.StringVar()
        self.filter_level_var = tk.StringVar(value="All")
        self.filter_category_var = tk.StringVar(value="All")
        self.preview_var = tk.BooleanVar(value=False)
        self.auto_save_var = tk.BooleanVar(value=True)
        
        # Search functionality
        self.search_var.trace_add("write", self.filter_markers)
        
    def setup_styles(self):
        """Setup modern styling for the GUI."""
        style = ttk.Style()
        
        # Configure modern theme colors
        style.theme_use('clam')
        
        # Define color scheme
        bg_color = "#f0f0f0"
        accent_color = "#2196F3"
        success_color = "#4CAF50"
        warning_color = "#FF9800"
        error_color = "#F44336"
        
        # Configure styles
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), foreground=accent_color)
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground=success_color)
        style.configure('Warning.TLabel', foreground=warning_color)
        style.configure('Error.TLabel', foreground=error_color)
        
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        style.configure('Primary.TButton', background=accent_color)
        
    def setup_modern_ui(self):
        """Setup the modern, professional UI layout."""
        # Main container with notebook for organized sections
        self.main_notebook = ttk.Notebook(self.root)
        self.main_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Marker Management
        self.management_frame = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.management_frame, text="📋 Marker Management")
        
        # Tab 2: Preview & Analysis
        self.preview_frame = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.preview_frame, text="👁️ Preview & Analysis")
        
        # Tab 3: Batch Operations
        self.batch_frame = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.batch_frame, text="⚡ Batch Operations")
        
        # Setup each tab
        self.setup_management_tab()
        self.setup_preview_tab()
        self.setup_batch_tab()
        
        # Status bar at bottom
        self.setup_status_bar()
        
    def setup_management_tab(self):
        """Setup the main marker management interface."""
        # Top toolbar
        toolbar = ttk.Frame(self.management_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # File operations
        file_frame = ttk.LabelFrame(toolbar, text="📁 File Operations")
        file_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Button(file_frame, text="🆕 New", command=self.new_marker, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(file_frame, text="📂 Open", command=self.open_marker, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(file_frame, text="💾 Save", command=self.save_marker, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(file_frame, text="💾 Save As", command=self.save_marker_as, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        # Edit operations
        edit_frame = ttk.LabelFrame(toolbar, text="✏️ Edit Operations")
        edit_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Button(edit_frame, text="🔄 Undo", command=self.undo_changes, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(edit_frame, text="🔧 Adapt v3.1", command=self.adapt_to_v31, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(edit_frame, text="✅ Validate", command=self.validate_marker, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        # View options
        view_frame = ttk.LabelFrame(toolbar, text="👁️ View Options")
        view_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Checkbutton(view_frame, text="Preview Mode", variable=self.preview_var,
                       command=self.toggle_preview_mode).pack(side=tk.LEFT, padx=2)
        ttk.Checkbutton(view_frame, text="Auto-Save", variable=self.auto_save_var).pack(side=tk.LEFT, padx=2)
        
        # Main content area with panedwindow
        main_paned = ttk.PanedWindow(self.management_frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel: Marker list and search
        left_panel = ttk.Frame(main_paned)
        main_paned.add(left_panel, weight=1)
        
        self.setup_marker_list_panel(left_panel)
        
        # Right panel: Editor and details
        right_panel = ttk.Frame(main_paned)
        main_paned.add(right_panel, weight=2)
        
        self.setup_editor_panel(right_panel)
        
    def setup_marker_list_panel(self, parent):
        """Setup the marker list panel with search and filters."""
        # Search and filter section
        search_frame = ttk.LabelFrame(parent, text="🔍 Search & Filter")
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Search entry
        search_entry_frame = ttk.Frame(search_frame)
        search_entry_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(search_entry_frame, text="Search:").pack(side=tk.LEFT)
        search_entry = ttk.Entry(search_entry_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Filter controls
        filter_frame = ttk.Frame(search_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Level:").pack(side=tk.LEFT)
        level_combo = ttk.Combobox(filter_frame, textvariable=self.filter_level_var,
                                  values=["All", "1 - Atomic", "2 - Semantic", "3 - Cluster", "4 - Meta"],
                                  state="readonly", width=12)
        level_combo.pack(side=tk.LEFT, padx=(5, 10))
        level_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_markers())
        
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT)
        cat_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category_var,
                                values=["All", "ATOMIC", "SEMANTIC", "CLUSTER", "META"],
                                state="readonly", width=12)
        cat_combo.pack(side=tk.LEFT, padx=(5, 0))
        cat_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_markers())
        
        # Marker list
        list_frame = ttk.LabelFrame(parent, text="📁 Available Markers")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview with more detailed columns
        columns = ("Name", "Level", "Category", "Author", "Status", "Modified")
        self.marker_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=15)
        
        # Configure columns
        self.marker_tree.heading("#0", text="ID")
        self.marker_tree.column("#0", width=150)
        
        for col in columns:
            self.marker_tree.heading(col, text=col)
            self.marker_tree.column(col, width=80)
        
        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.marker_tree.yview)
        tree_scroll_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.marker_tree.xview)
        self.marker_tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        
        # Pack treeview and scrollbars
        self.marker_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        self.marker_tree.bind("<<TreeviewSelect>>", self.on_marker_select)
        self.marker_tree.bind("<Double-1>", self.on_marker_double_click)
        
        # Context menu
        self.setup_context_menu()
        
    def setup_editor_panel(self, parent):
        """Setup the marker editor panel."""
        # Editor notebook for organized editing
        editor_notebook = ttk.Notebook(parent)
        editor_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # YAML Editor tab
        yaml_frame = ttk.Frame(editor_notebook)
        editor_notebook.add(yaml_frame, text="📝 YAML Editor")
        self.setup_yaml_editor(yaml_frame)
        
        # Form Editor tab
        form_frame = ttk.Frame(editor_notebook)
        editor_notebook.add(form_frame, text="📋 Form Editor")
        self.setup_form_editor(form_frame)
        
        # Validation Results tab
        validation_frame = ttk.Frame(editor_notebook)
        editor_notebook.add(validation_frame, text="✅ Validation")
        self.setup_validation_panel(validation_frame)
        
    def setup_yaml_editor(self, parent):
        """Setup the YAML editor with syntax highlighting and validation."""
        # Editor toolbar
        editor_toolbar = ttk.Frame(parent)
        editor_toolbar.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(editor_toolbar, text="🔧 Format YAML", 
                  command=self.format_yaml).pack(side=tk.LEFT, padx=2)
        ttk.Button(editor_toolbar, text="📋 Insert Template", 
                  command=self.insert_template).pack(side=tk.LEFT, padx=2)
        ttk.Button(editor_toolbar, text="🔍 Validate Syntax", 
                  command=self.validate_yaml_syntax).pack(side=tk.LEFT, padx=2)
        
        # Main text editor
        editor_frame = ttk.Frame(parent)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.yaml_editor = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.NONE, 
            font=('Consolas', 11),
            undo=True,
            maxundo=50
        )
        self.yaml_editor.pack(fill=tk.BOTH, expand=True)
        
        # Bind change events
        self.yaml_editor.bind('<KeyRelease>', self.on_editor_change)
        self.yaml_editor.bind('<Button-1>', self.on_editor_change)
        
    def setup_form_editor(self, parent):
        """Setup the structured form editor."""
        # Scrollable form
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        self.setup_form_fields(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_form_fields(self, parent):
        """Setup structured form fields for marker editing."""
        # Basic Information
        basic_frame = ttk.LabelFrame(parent, text="📋 Basic Information")
        basic_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # ID and Name
        row1 = ttk.Frame(basic_frame)
        row1.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(row1, text="ID:").pack(side=tk.LEFT, anchor=tk.W, padx=(0, 5))
        self.id_var = tk.StringVar()
        id_entry = ttk.Entry(row1, textvariable=self.id_var, width=30)
        id_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row1, text="Name:").pack(side=tk.LEFT, anchor=tk.W, padx=(0, 5))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(row1, textvariable=self.name_var, width=30)
        name_entry.pack(side=tk.LEFT)
        
        # Level and Category
        row2 = ttk.Frame(basic_frame)
        row2.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(row2, text="Level:").pack(side=tk.LEFT, anchor=tk.W, padx=(0, 5))
        self.level_var = tk.StringVar()
        level_combo = ttk.Combobox(row2, textvariable=self.level_var,
                                  values=["1", "2", "3", "4"], state="readonly", width=10)
        level_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row2, text="Category:").pack(side=tk.LEFT, anchor=tk.W, padx=(0, 5))
        self.category_var = tk.StringVar()
        cat_combo = ttk.Combobox(row2, textvariable=self.category_var,
                                values=["ATOMIC", "SEMANTIC", "CLUSTER", "META"], state="readonly", width=15)
        cat_combo.pack(side=tk.LEFT)
        
        # Author and Status
        row3 = ttk.Frame(basic_frame)
        row3.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(row3, text="Author:").pack(side=tk.LEFT, anchor=tk.W, padx=(0, 5))
        self.author_var = tk.StringVar()
        author_entry = ttk.Entry(row3, textvariable=self.author_var, width=25)
        author_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row3, text="Status:").pack(side=tk.LEFT, anchor=tk.W, padx=(0, 5))
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(row3, textvariable=self.status_var,
                                   values=["draft", "review", "released"], state="readonly", width=15)
        status_combo.pack(side=tk.LEFT)
        
        # Description
        desc_frame = ttk.LabelFrame(parent, text="📝 Description")
        desc_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.description_text = scrolledtext.ScrolledText(desc_frame, height=4, wrap=tk.WORD)
        self.description_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Examples
        examples_frame = ttk.LabelFrame(parent, text="💡 Examples")
        examples_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        examples_toolbar = ttk.Frame(examples_frame)
        examples_toolbar.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(examples_toolbar, text="➕ Add Example", 
                  command=self.add_example).pack(side=tk.LEFT, padx=2)
        ttk.Button(examples_toolbar, text="➖ Remove Selected", 
                  command=self.remove_example).pack(side=tk.LEFT, padx=2)
        
        self.examples_listbox = tk.Listbox(examples_frame, height=8)
        self.examples_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind form changes
        self.bind_form_changes()
        
    def setup_validation_panel(self, parent):
        """Setup the validation results panel."""
        # Validation toolbar
        val_toolbar = ttk.Frame(parent)
        val_toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(val_toolbar, text="🔍 Validate All", 
                  command=self.validate_comprehensive).pack(side=tk.LEFT, padx=2)
        ttk.Button(val_toolbar, text="📊 Generate Report", 
                  command=self.generate_validation_report).pack(side=tk.LEFT, padx=2)
        ttk.Button(val_toolbar, text="🗑️ Clear Results", 
                  command=self.clear_validation_results).pack(side=tk.LEFT, padx=2)
        
        # Results display
        self.validation_text = scrolledtext.ScrolledText(parent, height=25, wrap=tk.WORD)
        self.validation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_preview_tab(self):
        """Setup the detailed preview and analysis tab."""
        # Preview toolbar
        preview_toolbar = ttk.Frame(self.preview_frame)
        preview_toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(preview_toolbar, text="🔄 Refresh Preview", 
                  command=self.refresh_preview).pack(side=tk.LEFT, padx=2)
        ttk.Button(preview_toolbar, text="📊 Detailed Analysis", 
                  command=self.show_detailed_analysis).pack(side=tk.LEFT, padx=2)
        ttk.Button(preview_toolbar, text="🔍 Schema Check", 
                  command=self.check_schema_compliance).pack(side=tk.LEFT, padx=2)
        
        # Preview content with notebook
        preview_notebook = ttk.Notebook(self.preview_frame)
        preview_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Formatted preview
        formatted_frame = ttk.Frame(preview_notebook)
        preview_notebook.add(formatted_frame, text="📋 Formatted View")
        
        self.preview_text = scrolledtext.ScrolledText(formatted_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Schema analysis
        schema_frame = ttk.Frame(preview_notebook)
        preview_notebook.add(schema_frame, text="🔍 Schema Analysis")
        
        self.schema_text = scrolledtext.ScrolledText(schema_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.schema_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Comparison view (for showing changes)
        comparison_frame = ttk.Frame(preview_notebook)
        preview_notebook.add(comparison_frame, text="🔄 Change Analysis")
        
        self.comparison_text = scrolledtext.ScrolledText(comparison_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.comparison_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_batch_tab(self):
        """Setup the batch operations tab."""
        # Batch operations toolbar
        batch_toolbar = ttk.Frame(self.batch_frame)
        batch_toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(batch_toolbar, text="📁 Select Directory", 
                  command=self.select_batch_directory).pack(side=tk.LEFT, padx=2)
        ttk.Button(batch_toolbar, text="🔄 Convert All to v3.1", 
                  command=self.batch_convert_to_v31).pack(side=tk.LEFT, padx=2)
        ttk.Button(batch_toolbar, text="✅ Validate All", 
                  command=self.batch_validate).pack(side=tk.LEFT, padx=2)
        ttk.Button(batch_toolbar, text="💾 Backup All", 
                  command=self.batch_backup).pack(side=tk.LEFT, padx=2)
        
        # Progress and results
        progress_frame = ttk.LabelFrame(self.batch_frame, text="📊 Progress")
        progress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready for batch operations")
        self.progress_label.pack(pady=2)
        
        # Batch results
        results_frame = ttk.LabelFrame(self.batch_frame, text="📋 Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.batch_results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        self.batch_results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_status_bar(self):
        """Setup the status bar at the bottom."""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status label
        self.status_label = ttk.Label(self.status_frame, text="Ready - Robust Marker GUI v3.1")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # File info
        self.file_info_label = ttk.Label(self.status_frame, text="No file loaded")
        self.file_info_label.pack(side=tk.RIGHT, padx=5)
        
        # Unsaved changes indicator
        self.unsaved_indicator = ttk.Label(self.status_frame, text="", foreground="orange")
        self.unsaved_indicator.pack(side=tk.RIGHT, padx=5)
        
    def setup_context_menu(self):
        """Setup context menu for marker list."""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Open", command=self.open_selected_marker)
        self.context_menu.add_command(label="Edit", command=self.edit_selected_marker)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Duplicate", command=self.duplicate_marker)
        self.context_menu.add_command(label="Delete", command=self.delete_selected_marker)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Create Backup", command=self.backup_selected_marker)
        self.context_menu.add_command(label="Adapt to v3.1", command=self.adapt_selected_to_v31)
        
        self.marker_tree.bind("<Button-3>", self.show_context_menu)
        
    def setup_event_bindings(self):
        """Setup various event bindings."""
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_marker())
        self.root.bind('<Control-o>', lambda e: self.open_marker())
        self.root.bind('<Control-s>', lambda e: self.save_marker())
        self.root.bind('<Control-z>', lambda e: self.undo_changes())
        self.root.bind('<F5>', lambda e: self.refresh_marker_list())
        
        # Window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
    # Core Functionality Methods
    
    def new_marker(self):
        """Create a new marker using template."""
        if self.unsaved_changes:
            if not self.confirm_discard_changes():
                return
        
        # Template selection dialog
        template_dialog = MarkerTemplateDialog(self.root, self.v31_manager)
        if template_dialog.result:
            self.current_marker_data = template_dialog.result
            self.current_marker_file = None
            self.load_marker_to_editor()
            self.update_status("New marker created from template")
            
    def open_marker(self):
        """Open an existing marker file."""
        if self.unsaved_changes:
            if not self.confirm_discard_changes():
                return
                
        file_path = filedialog.askopenfilename(
            title="Open Marker File",
            initialdir=self.marker_dir,
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        
        if file_path:
            self.load_marker_file(file_path)
            
    def save_marker(self):
        """Save the current marker."""
        if not self.current_marker_file:
            return self.save_marker_as()
            
        try:
            # Get data from editor
            if self.get_current_editor_data():
                # Create backup before saving
                self.create_backup(self.current_marker_file)
                
                # Save to file
                with open(self.current_marker_file, 'w', encoding='utf-8') as f:
                    yaml.dump(self.current_marker_data, f, default_flow_style=False, 
                             allow_unicode=True, sort_keys=False)
                
                self.unsaved_changes = False
                self.update_unsaved_indicator()
                self.update_status(f"Marker saved: {self.current_marker_file.name}")
                self.refresh_marker_list()
                return True
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save marker: {str(e)}")
            return False
            
    def save_marker_as(self):
        """Save marker with new filename."""
        if not self.get_current_editor_data():
            return False
            
        # Generate suggested filename
        marker_id = self.current_marker_data.get('id', 'NEW_MARKER')
        suggested_name = self.v31_manager.generate_filename(marker_id)
        
        file_path = filedialog.asksaveasfilename(
            title="Save Marker As",
            initialdir=self.marker_dir,
            initialfile=suggested_name,
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.current_marker_file = Path(file_path)
                return self.save_marker()
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save marker: {str(e)}")
                return False
        return False
        
    def adapt_to_v31(self):
        """Adapt current marker to Lean-Deep v3.1 format with detailed reporting."""
        if not self.current_marker_data:
            messagebox.showwarning("Warning", "No marker loaded to adapt!")
            return
            
        try:
            # Create backup before adaptation
            original_data = self.current_marker_data.copy()
            self.add_to_backup_stack(original_data)
            
            # Perform adaptation
            adapted_data, changes_report = self.v31_manager.adapt_marker_to_v31_with_report(
                self.current_marker_data
            )
            
            self.current_marker_data = adapted_data
            self.load_marker_to_editor()
            
            # Show detailed changes report
            self.show_adaptation_report(changes_report)
            
            self.unsaved_changes = True
            self.update_unsaved_indicator()
            self.update_status("Marker adapted to v3.1 format")
            
        except Exception as e:
            messagebox.showerror("Adaptation Error", f"Failed to adapt marker: {str(e)}")
            
    def validate_marker(self):
        """Validate current marker against v3.1 schema."""
        if not self.get_current_editor_data():
            return
            
        is_valid, errors = self.v31_manager.validate_marker_schema(self.current_marker_data)
        
        # Update validation display
        self.validation_text.config(state=tk.NORMAL)
        self.validation_text.delete(1.0, tk.END)
        
        if is_valid:
            self.validation_text.insert(tk.END, "✅ MARKER IS VALID\n\n")
            self.validation_text.insert(tk.END, "All v3.1 schema requirements met.\n")
            
            # Show additional info
            level = self.current_marker_data.get('level', 'Unknown')
            category = self.current_marker_data.get('category', 'Unknown')
            examples_count = len(self.current_marker_data.get('examples', []))
            
            self.validation_text.insert(tk.END, f"\nMarker Details:\n")
            self.validation_text.insert(tk.END, f"Level: {level}\n")
            self.validation_text.insert(tk.END, f"Category: {category}\n")
            self.validation_text.insert(tk.END, f"Examples: {examples_count}\n")
            
        else:
            self.validation_text.insert(tk.END, "❌ MARKER IS INVALID\n\n")
            self.validation_text.insert(tk.END, "Schema validation errors:\n\n")
            
            for i, error in enumerate(errors, 1):
                self.validation_text.insert(tk.END, f"{i}. {error}\n")
                
        self.validation_text.config(state=tk.DISABLED)
        self.update_status(f"Validation: {'VALID' if is_valid else 'INVALID'}")
        
    def undo_changes(self):
        """Undo the last changes using backup stack."""
        if not self.backup_stack:
            messagebox.showinfo("Undo", "No changes to undo!")
            return
            
        # Restore from backup stack
        previous_data = self.backup_stack.pop()
        self.current_marker_data = previous_data
        self.load_marker_to_editor()
        
        self.update_status(f"Changes undone. {len(self.backup_stack)} undo steps remaining")
        
    # Helper Methods
    
    def get_current_editor_data(self):
        """Get marker data from current editor (YAML or Form)."""
        try:
            # Get from YAML editor
            yaml_content = self.yaml_editor.get(1.0, tk.END).strip()
            if yaml_content:
                self.current_marker_data = yaml.safe_load(yaml_content)
                return True
            return False
        except yaml.YAMLError as e:
            messagebox.showerror("YAML Error", f"Invalid YAML format: {str(e)}")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse editor data: {str(e)}")
            return False
            
    def load_marker_to_editor(self):
        """Load current marker data to all editors."""
        if not self.current_marker_data:
            return
            
        # Load to YAML editor
        yaml_content = yaml.dump(self.current_marker_data, default_flow_style=False,
                                allow_unicode=True, sort_keys=False)
        self.yaml_editor.delete(1.0, tk.END)
        self.yaml_editor.insert(tk.END, yaml_content)
        
        # Load to form editor
        self.load_to_form_editor()
        
        # Update preview
        self.refresh_preview()
        
    def load_to_form_editor(self):
        """Load marker data to form editor fields."""
        if not self.current_marker_data:
            return
            
        # Basic fields
        self.id_var.set(self.current_marker_data.get('id', ''))
        self.name_var.set(self.current_marker_data.get('name', ''))
        self.level_var.set(str(self.current_marker_data.get('level', 1)))
        self.category_var.set(self.current_marker_data.get('category', ''))
        self.author_var.set(self.current_marker_data.get('author', ''))
        self.status_var.set(self.current_marker_data.get('status', 'draft'))
        
        # Description
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, self.current_marker_data.get('description', ''))
        
        # Examples
        self.examples_listbox.delete(0, tk.END)
        for example in self.current_marker_data.get('examples', []):
            self.examples_listbox.insert(tk.END, example)
            
    def create_backup(self, file_path):
        """Create a timestamped backup of the marker file."""
        if not file_path or not file_path.exists():
            return
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{file_path.stem}_{timestamp}.yaml"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(file_path, backup_path)
        
    def add_to_backup_stack(self, data):
        """Add data to backup stack for undo functionality."""
        self.backup_stack.append(data.copy())
        # Limit backup stack size
        if len(self.backup_stack) > 20:
            self.backup_stack.pop(0)
            
    def update_status(self, message):
        """Update the status bar message."""
        self.status_label.config(text=message)
        
    def update_unsaved_indicator(self):
        """Update the unsaved changes indicator."""
        if self.unsaved_changes:
            self.unsaved_indicator.config(text="● Unsaved changes")
        else:
            self.unsaved_indicator.config(text="")
            
    def confirm_discard_changes(self):
        """Ask user to confirm discarding unsaved changes."""
        return messagebox.askyesno(
            "Unsaved Changes", 
            "You have unsaved changes. Do you want to discard them?"
        )
        
    # Event Handlers
    
    def on_marker_select(self, event):
        """Handle marker selection in the tree."""
        selection = self.marker_tree.selection()
        if selection:
            item = self.marker_tree.item(selection[0])
            marker_id = item['text']
            self.show_marker_preview(marker_id)
            
    def on_marker_double_click(self, event):
        """Handle double-click on marker to open for editing."""
        selection = self.marker_tree.selection()
        if selection:
            item = self.marker_tree.item(selection[0])
            marker_id = item['text']
            marker_file = self.marker_dir / f"{marker_id}.yaml"
            if marker_file.exists():
                self.load_marker_file(marker_file)
                
    def on_editor_change(self, event):
        """Handle changes in the editor."""
        if not self.unsaved_changes:
            self.unsaved_changes = True
            self.update_unsaved_indicator()
            
    def on_window_close(self):
        """Handle window close event."""
        if self.unsaved_changes:
            if not self.confirm_discard_changes():
                return
        self.root.destroy()
        
    def show_context_menu(self, event):
        """Show context menu for marker list."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    # Placeholder methods for advanced features
    
    def refresh_marker_list(self):
        """Refresh the marker list display."""
        # Clear current items
        for item in self.marker_tree.get_children():
            self.marker_tree.delete(item)
            
        # Load markers from directory
        if self.marker_dir.exists():
            for file_path in self.marker_dir.glob("*.yaml"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        
                    if data:
                        marker_id = data.get('id', file_path.stem)
                        name = data.get('name', marker_id)
                        level = data.get('level', '')
                        category = data.get('category', '')
                        author = data.get('author', '')
                        status = data.get('status', '')
                        modified = file_path.stat().st_mtime
                        modified_str = datetime.fromtimestamp(modified).strftime('%Y-%m-%d')
                        
                        self.marker_tree.insert('', 'end', text=marker_id,
                                              values=(name, level, category, author, status, modified_str))
                except Exception:
                    # Skip problematic files
                    continue
                    
        self.update_status(f"Loaded {len(self.marker_tree.get_children())} markers")
        
    def filter_markers(self, *args):
        """Filter markers based on search and filter criteria."""
        # This would implement the filtering logic
        pass
        
    def load_marker_file(self, file_path):
        """Load a marker file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.current_marker_data = yaml.safe_load(f)
                
            self.current_marker_file = Path(file_path)
            self.load_marker_to_editor()
            self.unsaved_changes = False
            self.update_unsaved_indicator()
            self.update_status(f"Loaded: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load marker: {str(e)}")
            
    def show_marker_preview(self, marker_id):
        """Show preview of selected marker."""
        marker_file = self.marker_dir / f"{marker_id}.yaml"
        if marker_file.exists():
            try:
                with open(marker_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete(1.0, tk.END)
                
                # Format preview
                preview_content = self.format_marker_preview(data)
                self.preview_text.insert(tk.END, preview_content)
                
                self.preview_text.config(state=tk.DISABLED)
                
            except Exception as e:
                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(tk.END, f"Error loading preview: {str(e)}")
                self.preview_text.config(state=tk.DISABLED)
                
    def format_marker_preview(self, data):
        """Format marker data for preview display."""
        if not data:
            return "No data available"
            
        lines = []
        lines.append(f"🎯 {data.get('name', 'Unknown Marker')}")
        lines.append("=" * 50)
        lines.append(f"ID: {data.get('id', 'N/A')}")
        lines.append(f"Level: {data.get('level', 'N/A')}")
        lines.append(f"Category: {data.get('category', 'N/A')}")
        lines.append(f"Author: {data.get('author', 'N/A')}")
        lines.append(f"Status: {data.get('status', 'N/A')}")
        lines.append(f"Created: {data.get('created_at', 'N/A')}")
        lines.append("")
        lines.append("📝 Description:")
        lines.append(data.get('description', 'No description available'))
        lines.append("")
        
        examples = data.get('examples', [])
        lines.append(f"💡 Examples ({len(examples)}):")
        for i, example in enumerate(examples[:5], 1):
            lines.append(f"{i}. {example}")
        if len(examples) > 5:
            lines.append(f"... and {len(examples) - 5} more")
            
        return "\n".join(lines)
        
    # Advanced feature implementations
    
    def refresh_preview(self):
        """Refresh the preview display."""
        if self.current_marker_data:
            preview_content = self.format_marker_preview(self.current_marker_data)
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, preview_content)
            self.preview_text.config(state=tk.DISABLED)
    
    def show_detailed_analysis(self):
        """Show detailed analysis of current marker."""
        if not self.current_marker_data:
            messagebox.showwarning("Warning", "No marker loaded for analysis!")
            return
            
        analysis = self.analyze_marker_quality(self.current_marker_data)
        
        self.schema_text.config(state=tk.NORMAL)
        self.schema_text.delete(1.0, tk.END)
        self.schema_text.insert(tk.END, analysis)
        self.schema_text.config(state=tk.DISABLED)
        
        # Switch to schema analysis tab
        for i, tab_id in enumerate(self.main_notebook.tabs()):
            if "Preview" in self.main_notebook.tab(tab_id, "text"):
                self.main_notebook.select(i)
                break
    
    def analyze_marker_quality(self, data):
        """Analyze marker quality and structure."""
        lines = []
        lines.append("🔍 DETAILED MARKER ANALYSIS")
        lines.append("=" * 50)
        
        # Basic info
        lines.append(f"ID: {data.get('id', 'N/A')}")
        lines.append(f"Level: {data.get('level', 'N/A')} ({self.level_categories.get(data.get('level', 0), 'Unknown')})")
        lines.append(f"Status: {data.get('status', 'N/A')}")
        lines.append("")
        
        # Schema compliance
        is_valid, errors = self.v31_manager.validate_marker_schema(data)
        lines.append(f"📋 Schema Compliance: {'✅ VALID' if is_valid else '❌ INVALID'}")
        if errors:
            lines.append("Validation Issues:")
            for error in errors:
                lines.append(f"  • {error}")
        lines.append("")
        
        # Content quality analysis
        lines.append("📝 Content Quality Analysis:")
        
        # Description analysis
        description = data.get('description', '')
        if description:
            lines.append(f"Description: {len(description)} characters")
            if len(description) < 20:
                lines.append("  ⚠️ Description appears very short")
            elif len(description) > 500:
                lines.append("  ⚠️ Description is quite long")
            else:
                lines.append("  ✅ Description length appropriate")
        else:
            lines.append("  ❌ No description provided")
        
        # Examples analysis
        examples = data.get('examples', [])
        lines.append(f"Examples: {len(examples)} provided (minimum 5 required)")
        if len(examples) < 5:
            lines.append(f"  ❌ Need {5 - len(examples)} more examples")
        else:
            lines.append("  ✅ Minimum examples requirement met")
            
        # Check example quality
        placeholder_count = 0
        for example in examples:
            if isinstance(example, str) and example.lower().strip() in ['example', 'todo', 'placeholder']:
                placeholder_count += 1
        
        if placeholder_count > 0:
            lines.append(f"  ⚠️ {placeholder_count} placeholder examples detected")
        
        lines.append("")
        
        # Structure analysis
        lines.append("🏗️ Structure Analysis:")
        required_fields = self.v31_manager.mandatory_fields
        present_fields = [field for field in required_fields if field in data]
        missing_fields = [field for field in required_fields if field not in data]
        
        lines.append(f"Required fields present: {len(present_fields)}/{len(required_fields)}")
        if missing_fields:
            lines.append("Missing required fields:")
            for field in missing_fields:
                lines.append(f"  • {field}")
        else:
            lines.append("  ✅ All required fields present")
        
        return "\n".join(lines)
    
    def check_schema_compliance(self):
        """Check schema compliance and display results."""
        if not self.current_marker_data:
            messagebox.showwarning("Warning", "No marker loaded for schema check!")
            return
            
        is_valid, errors = self.v31_manager.validate_marker_schema(self.current_marker_data)
        boundary_warnings = self.v31_manager.validate_content_boundaries(self.current_marker_data)
        
        self.schema_text.config(state=tk.NORMAL)
        self.schema_text.delete(1.0, tk.END)
        
        self.schema_text.insert(tk.END, "🔍 SCHEMA COMPLIANCE CHECK\n")
        self.schema_text.insert(tk.END, "=" * 40 + "\n\n")
        
        if is_valid:
            self.schema_text.insert(tk.END, "✅ SCHEMA VALID\n\n")
        else:
            self.schema_text.insert(tk.END, "❌ SCHEMA INVALID\n\n")
            self.schema_text.insert(tk.END, "Validation Errors:\n")
            for i, error in enumerate(errors, 1):
                self.schema_text.insert(tk.END, f"{i}. {error}\n")
            self.schema_text.insert(tk.END, "\n")
        
        if boundary_warnings:
            self.schema_text.insert(tk.END, "⚠️ CONTENT WARNINGS\n\n")
            for i, warning in enumerate(boundary_warnings, 1):
                self.schema_text.insert(tk.END, f"{i}. {warning}\n")
        
        self.schema_text.config(state=tk.DISABLED)
    
    def format_yaml(self):
        """Format the YAML content in the editor."""
        try:
            content = self.yaml_editor.get(1.0, tk.END).strip()
            if not content:
                return
                
            # Parse and re-format
            data = yaml.safe_load(content)
            formatted = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            self.yaml_editor.delete(1.0, tk.END)
            self.yaml_editor.insert(tk.END, formatted)
            
            self.update_status("YAML formatted")
            
        except yaml.YAMLError as e:
            messagebox.showerror("YAML Error", f"Cannot format invalid YAML: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to format YAML: {str(e)}")
    
    def insert_template(self):
        """Insert a template at cursor position."""
        template_dialog = MarkerTemplateDialog(self.root, self.v31_manager)
        if template_dialog.result:
            template_yaml = yaml.dump(template_dialog.result, default_flow_style=False,
                                    allow_unicode=True, sort_keys=False)
            
            # Insert at cursor position
            cursor_pos = self.yaml_editor.index(tk.INSERT)
            self.yaml_editor.insert(cursor_pos, template_yaml)
            
            self.update_status("Template inserted")
    
    def validate_yaml_syntax(self):
        """Validate YAML syntax only."""
        content = self.yaml_editor.get(1.0, tk.END).strip()
        if not content:
            messagebox.showinfo("Validation", "No content to validate!")
            return
            
        try:
            yaml.safe_load(content)
            messagebox.showinfo("Syntax Validation", "✅ YAML syntax is valid!")
            self.update_status("YAML syntax valid")
        except yaml.YAMLError as e:
            messagebox.showerror("Syntax Error", f"❌ YAML syntax error:\n{str(e)}")
            self.update_status("YAML syntax invalid")
    
    def add_example(self):
        """Add a new example to the examples list."""
        example_text = tk.simpledialog.askstring("New Example", "Enter example text:")
        if example_text and example_text.strip():
            self.examples_listbox.insert(tk.END, example_text.strip())
            self.sync_form_to_current_data()
    
    def remove_example(self):
        """Remove selected example from the list."""
        selection = self.examples_listbox.curselection()
        if selection:
            self.examples_listbox.delete(selection[0])
            self.sync_form_to_current_data()
        else:
            messagebox.showwarning("Warning", "Please select an example to remove!")
    
    def sync_form_to_current_data(self):
        """Sync form data to current marker data."""
        if not self.current_marker_data:
            self.current_marker_data = {}
            
        # Update from form fields
        self.current_marker_data['id'] = self.id_var.get()
        self.current_marker_data['name'] = self.name_var.get()
        
        try:
            self.current_marker_data['level'] = int(self.level_var.get())
        except ValueError:
            pass
            
        self.current_marker_data['category'] = self.category_var.get()
        self.current_marker_data['author'] = self.author_var.get()
        self.current_marker_data['status'] = self.status_var.get()
        
        # Description
        self.current_marker_data['description'] = self.description_text.get(1.0, tk.END).strip()
        
        # Examples
        examples = []
        for i in range(self.examples_listbox.size()):
            examples.append(self.examples_listbox.get(i))
        self.current_marker_data['examples'] = examples
        
        # Update YAML editor
        yaml_content = yaml.dump(self.current_marker_data, default_flow_style=False,
                                allow_unicode=True, sort_keys=False)
        self.yaml_editor.delete(1.0, tk.END)
        self.yaml_editor.insert(tk.END, yaml_content)
        
        self.unsaved_changes = True
        self.update_unsaved_indicator()
    
    def bind_form_changes(self):
        """Bind form field changes to sync function."""
        # This would bind all form fields to trigger sync_form_to_current_data
        # For now, we'll implement manual sync when needed
        pass
    
    def validate_comprehensive(self):
        """Perform comprehensive validation."""
        if not self.get_current_editor_data():
            return
            
        self.validation_text.config(state=tk.NORMAL)
        self.validation_text.delete(1.0, tk.END)
        
        self.validation_text.insert(tk.END, "🔍 COMPREHENSIVE VALIDATION\n")
        self.validation_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Schema validation
        is_valid, errors = self.v31_manager.validate_marker_schema(self.current_marker_data)
        self.validation_text.insert(tk.END, f"📋 Schema Validation: {'✅ PASS' if is_valid else '❌ FAIL'}\n")
        
        if errors:
            for error in errors:
                self.validation_text.insert(tk.END, f"  • {error}\n")
        self.validation_text.insert(tk.END, "\n")
        
        # Content boundary validation
        boundary_warnings = self.v31_manager.validate_content_boundaries(self.current_marker_data)
        self.validation_text.insert(tk.END, f"🔍 Content Boundaries: {len(boundary_warnings)} warnings\n")
        
        for warning in boundary_warnings:
            self.validation_text.insert(tk.END, f"  ⚠️ {warning}\n")
        self.validation_text.insert(tk.END, "\n")
        
        # Quality analysis
        quality_score = self.calculate_quality_score(self.current_marker_data)
        self.validation_text.insert(tk.END, f"⭐ Quality Score: {quality_score}/100\n\n")
        
        self.validation_text.config(state=tk.DISABLED)
    
    def calculate_quality_score(self, data):
        """Calculate a quality score for the marker."""
        score = 0
        
        # Basic requirements (40 points)
        is_valid, _ = self.v31_manager.validate_marker_schema(data)
        if is_valid:
            score += 40
        
        # Content quality (30 points)
        description = data.get('description', '')
        if len(description) >= 20:
            score += 15
        if len(description) >= 50:
            score += 15
        
        # Examples quality (30 points)
        examples = data.get('examples', [])
        if len(examples) >= 5:
            score += 15
        
        # Check for non-placeholder examples
        real_examples = [ex for ex in examples if ex.lower().strip() not in ['example', 'todo', 'placeholder']]
        if len(real_examples) >= 5:
            score += 15
        
        return min(score, 100)
    
    def generate_validation_report(self):
        """Generate a detailed validation report."""
        if not self.current_marker_data:
            messagebox.showwarning("Warning", "No marker loaded for report generation!")
            return
            
        report_content = self.create_validation_report(self.current_marker_data)
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        marker_id = self.current_marker_data.get('id', 'UNKNOWN')
        report_filename = f"validation_report_{marker_id}_{timestamp}.txt"
        
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            messagebox.showinfo("Report Generated", f"Validation report saved as:\n{report_filename}")
            self.update_status(f"Report generated: {report_filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
    
    def create_validation_report(self, data):
        """Create detailed validation report content."""
        lines = []
        lines.append("LEAN-DEEP V3.1 MARKER VALIDATION REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Marker ID: {data.get('id', 'Unknown')}")
        lines.append("")
        
        # Schema validation
        is_valid, errors = self.v31_manager.validate_marker_schema(data)
        lines.append("SCHEMA VALIDATION")
        lines.append("-" * 20)
        lines.append(f"Status: {'PASS' if is_valid else 'FAIL'}")
        
        if errors:
            lines.append("\nValidation Errors:")
            for i, error in enumerate(errors, 1):
                lines.append(f"{i}. {error}")
        
        lines.append("")
        
        # Content analysis
        lines.append("CONTENT ANALYSIS")
        lines.append("-" * 20)
        
        boundary_warnings = self.v31_manager.validate_content_boundaries(data)
        if boundary_warnings:
            lines.append("Content Boundary Warnings:")
            for i, warning in enumerate(boundary_warnings, 1):
                lines.append(f"{i}. {warning}")
        else:
            lines.append("No content boundary issues detected.")
        
        lines.append("")
        
        # Quality score
        quality_score = self.calculate_quality_score(data)
        lines.append("QUALITY ASSESSMENT")
        lines.append("-" * 20)
        lines.append(f"Overall Score: {quality_score}/100")
        
        if quality_score >= 90:
            lines.append("Rating: Excellent")
        elif quality_score >= 70:
            lines.append("Rating: Good")
        elif quality_score >= 50:
            lines.append("Rating: Acceptable")
        else:
            lines.append("Rating: Needs Improvement")
        
        return "\n".join(lines)
    
    def clear_validation_results(self):
        """Clear validation results display."""
        self.validation_text.config(state=tk.NORMAL)
        self.validation_text.delete(1.0, tk.END)
        self.validation_text.config(state=tk.DISABLED)
        self.update_status("Validation results cleared")
    
    def show_adaptation_report(self, report):
        """Show detailed adaptation report."""
        self.comparison_text.config(state=tk.NORMAL)
        self.comparison_text.delete(1.0, tk.END)
        
        self.comparison_text.insert(tk.END, "🔄 MARKER ADAPTATION REPORT\n")
        self.comparison_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Added fields
        if report["added"]:
            self.comparison_text.insert(tk.END, f"➕ ADDED FIELDS ({len(report['added'])})\n")
            for item in report["added"]:
                self.comparison_text.insert(tk.END, f"  • {item['field']}: {item['value']}\n")
                self.comparison_text.insert(tk.END, f"    Reason: {item['reason']}\n")
            self.comparison_text.insert(tk.END, "\n")
        
        # Removed fields
        if report["removed"]:
            self.comparison_text.insert(tk.END, f"➖ REMOVED FIELDS ({len(report['removed'])})\n")
            for item in report["removed"]:
                self.comparison_text.insert(tk.END, f"  • {item['field']}: {item['value']}\n")
                self.comparison_text.insert(tk.END, f"    Reason: {item['reason']}\n")
            self.comparison_text.insert(tk.END, "\n")
        
        # Modified fields
        if report["modified"]:
            self.comparison_text.insert(tk.END, f"🔄 MODIFIED FIELDS ({len(report['modified'])})\n")
            for item in report["modified"]:
                self.comparison_text.insert(tk.END, f"  • {item['field']}\n")
                self.comparison_text.insert(tk.END, f"    Old: {item['original_value']}\n")
                self.comparison_text.insert(tk.END, f"    New: {item['new_value']}\n")
                self.comparison_text.insert(tk.END, f"    Reason: {item['reason']}\n")
            self.comparison_text.insert(tk.END, "\n")
        
        # Preserved fields
        if report["preserved"]:
            self.comparison_text.insert(tk.END, f"✅ PRESERVED FIELDS ({len(report['preserved'])})\n")
            for item in report["preserved"]:
                self.comparison_text.insert(tk.END, f"  • {item['field']}\n")
            self.comparison_text.insert(tk.END, "\n")
        
        # Warnings
        if report["warnings"]:
            self.comparison_text.insert(tk.END, f"⚠️ WARNINGS ({len(report['warnings'])})\n")
            for warning in report["warnings"]:
                self.comparison_text.insert(tk.END, f"  • {warning}\n")
        
        self.comparison_text.config(state=tk.DISABLED)
        
        # Switch to comparison tab
        for i, tab_id in enumerate(self.main_notebook.tabs()):
            if "Preview" in self.main_notebook.tab(tab_id, "text"):
                self.main_notebook.select(i)
                break
    
    # Placeholder implementations for remaining methods
    def select_batch_directory(self): 
        messagebox.showinfo("Info", "Batch operations coming soon!")
    
    def batch_convert_to_v31(self): 
        messagebox.showinfo("Info", "Batch conversion coming soon!")
    
    def batch_validate(self): 
        messagebox.showinfo("Info", "Batch validation coming soon!")
    
    def batch_backup(self): 
        messagebox.showinfo("Info", "Batch backup coming soon!")
    
    def open_selected_marker(self): 
        self.on_marker_double_click(None)
    
    def edit_selected_marker(self): 
        self.on_marker_double_click(None)
    
    def duplicate_marker(self): 
        messagebox.showinfo("Info", "Marker duplication coming soon!")
    
    def delete_selected_marker(self): 
        messagebox.showinfo("Info", "Marker deletion coming soon!")
    
    def backup_selected_marker(self): 
        messagebox.showinfo("Info", "Individual backup coming soon!")
    
    def adapt_selected_to_v31(self): 
        messagebox.showinfo("Info", "Selected marker adaptation coming soon!")
    
    def toggle_preview_mode(self): 
        # Toggle between edit and preview modes
        self.preview_mode = self.preview_var.get()
        self.update_status(f"Preview mode: {'ON' if self.preview_mode else 'OFF'}")
        
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


class MarkerTemplateDialog:
    """Dialog for selecting marker template options."""
    
    def __init__(self, parent, v31_manager):
        self.result = None
        self.v31_manager = v31_manager
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Marker Template")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
        
        # Center on parent
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
        
    def setup_dialog(self):
        """Setup the template selection dialog."""
        # Title
        title_label = ttk.Label(self.dialog, text="Create New Marker", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Template options frame
        options_frame = ttk.LabelFrame(self.dialog, text="Template Options")
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Level selection
        ttk.Label(options_frame, text="Level:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.level_var = tk.StringVar(value="1")
        level_combo = ttk.Combobox(options_frame, textvariable=self.level_var,
                                  values=["1", "2", "3", "4"], state="readonly")
        level_combo.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Name entry
        ttk.Label(options_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(options_frame, textvariable=self.name_var)
        name_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Author entry
        ttk.Label(options_frame, text="Author:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.author_var = tk.StringVar(value="Author Name")
        author_entry = ttk.Entry(options_frame, textvariable=self.author_var)
        author_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        options_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="Create", command=self.create_template).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
        
    def create_template(self):
        """Create the template and close dialog."""
        level = int(self.level_var.get())
        name = self.name_var.get().strip()
        author = self.author_var.get().strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter a marker name!")
            return
            
        try:
            self.result = self.v31_manager.create_marker_template(level, name, author)
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create template: {str(e)}")
            
    def cancel(self):
        """Cancel dialog."""
        self.dialog.destroy()


def main():
    """Main function to start the Robust Marker GUI."""
    app = RobustMarkerGUI()
    app.run()


if __name__ == "__main__":
    main()