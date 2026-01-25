#!/usr/bin/env python3
"""
Comprehensive Test Suite for ContextSynth

Tests all functionality including:
- File analysis and summarization
- Folder summarization
- Project detection and analysis
- Output formatting (markdown, JSON, text)
- CLI interface

Target: 70+ tests with 100% pass rate

Author: ATLAS (Team Brain)
"""

import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from contextsynth import (
    DetailLevel,
    OutputFormat,
    FileType,
    ProjectType,
    CodeElement,
    FileSummary,
    FolderSummary,
    ProjectSummary,
    FileAnalyzer,
    ProjectAnalyzer,
    ContextSynth,
    __version__
)


class TestDetailLevel(unittest.TestCase):
    """Tests for DetailLevel enum."""
    
    def test_brief_value(self):
        """Test brief level."""
        self.assertEqual(DetailLevel.BRIEF.value, "brief")
    
    def test_standard_value(self):
        """Test standard level."""
        self.assertEqual(DetailLevel.STANDARD.value, "standard")
    
    def test_detailed_value(self):
        """Test detailed level."""
        self.assertEqual(DetailLevel.DETAILED.value, "detailed")


class TestOutputFormat(unittest.TestCase):
    """Tests for OutputFormat enum."""
    
    def test_markdown_value(self):
        """Test markdown format."""
        self.assertEqual(OutputFormat.MARKDOWN.value, "markdown")
    
    def test_json_value(self):
        """Test JSON format."""
        self.assertEqual(OutputFormat.JSON.value, "json")
    
    def test_text_value(self):
        """Test text format."""
        self.assertEqual(OutputFormat.TEXT.value, "text")


class TestFileType(unittest.TestCase):
    """Tests for FileType enum."""
    
    def test_python_value(self):
        """Test Python type."""
        self.assertEqual(FileType.PYTHON.value, "python")
    
    def test_javascript_value(self):
        """Test JavaScript type."""
        self.assertEqual(FileType.JAVASCRIPT.value, "javascript")
    
    def test_unknown_value(self):
        """Test unknown type."""
        self.assertEqual(FileType.UNKNOWN.value, "unknown")


class TestProjectType(unittest.TestCase):
    """Tests for ProjectType enum."""
    
    def test_python_value(self):
        """Test Python project."""
        self.assertEqual(ProjectType.PYTHON.value, "python")
    
    def test_node_value(self):
        """Test Node project."""
        self.assertEqual(ProjectType.NODE.value, "node")
    
    def test_generic_value(self):
        """Test generic project."""
        self.assertEqual(ProjectType.GENERIC.value, "generic")


class TestCodeElement(unittest.TestCase):
    """Tests for CodeElement dataclass."""
    
    def test_create_function(self):
        """Test creating function element."""
        elem = CodeElement(
            name="test_func",
            element_type="function",
            line_number=10,
            docstring="Test function",
            parameters=["a", "b"]
        )
        self.assertEqual(elem.name, "test_func")
        self.assertEqual(elem.element_type, "function")
        self.assertEqual(elem.line_number, 10)
        self.assertEqual(elem.parameters, ["a", "b"])
    
    def test_create_class(self):
        """Test creating class element."""
        elem = CodeElement(
            name="TestClass",
            element_type="class",
            line_number=1
        )
        self.assertEqual(elem.name, "TestClass")
        self.assertIsNone(elem.docstring)


class TestFileSummary(unittest.TestCase):
    """Tests for FileSummary dataclass."""
    
    def test_create_summary(self):
        """Test creating file summary."""
        summary = FileSummary(
            path="/test/file.py",
            file_type=FileType.PYTHON,
            size_bytes=1000,
            line_count=50,
            description="Test file",
            key_elements=[],
            imports=[],
            todos=[],
            blockers=[],
            dependencies=[]
        )
        self.assertEqual(summary.path, "/test/file.py")
        self.assertEqual(summary.file_type, FileType.PYTHON)
    
    def test_to_dict(self):
        """Test converting to dict."""
        summary = FileSummary(
            path="/test/file.py",
            file_type=FileType.PYTHON,
            size_bytes=1000,
            line_count=50,
            description="Test",
            key_elements=[
                CodeElement("func", "function", 1)
            ],
            imports=["os"],
            todos=["Fix this"],
            blockers=[],
            dependencies=[]
        )
        d = summary.to_dict()
        self.assertEqual(d["path"], "/test/file.py")
        self.assertEqual(d["file_type"], "python")
        self.assertEqual(len(d["key_elements"]), 1)


class TestFolderSummary(unittest.TestCase):
    """Tests for FolderSummary dataclass."""
    
    def test_create_summary(self):
        """Test creating folder summary."""
        summary = FolderSummary(
            path="/test/folder",
            file_count=10,
            total_lines=500,
            file_types={"python": 5, "javascript": 5},
            files=[],
            description="Test folder"
        )
        self.assertEqual(summary.path, "/test/folder")
        self.assertEqual(summary.file_count, 10)
    
    def test_to_dict(self):
        """Test converting to dict."""
        summary = FolderSummary(
            path="/test",
            file_count=5,
            total_lines=100,
            file_types={"python": 5},
            files=[],
            description="Test"
        )
        d = summary.to_dict()
        self.assertIn("file_types", d)


class TestProjectSummary(unittest.TestCase):
    """Tests for ProjectSummary dataclass."""
    
    def test_create_summary(self):
        """Test creating project summary."""
        summary = ProjectSummary(
            path="/test/project",
            project_type=ProjectType.PYTHON,
            name="test-project",
            description="A test project",
            version="1.0.0",
            file_count=100,
            total_lines=5000,
            main_technologies=["Python", "Flask"],
            dependencies=["flask", "requests"],
            dev_dependencies=["pytest"],
            entry_points=["main.py"],
            key_files=[],
            todos=[],
            blockers=[],
            recent_changes=[]
        )
        self.assertEqual(summary.name, "test-project")
        self.assertEqual(summary.version, "1.0.0")
    
    def test_to_dict(self):
        """Test converting to dict."""
        summary = ProjectSummary(
            path="/test",
            project_type=ProjectType.NODE,
            name="test",
            description="Test",
            version="1.0",
            file_count=10,
            total_lines=100,
            main_technologies=[],
            dependencies=[],
            dev_dependencies=[],
            entry_points=[],
            key_files=[],
            todos=[],
            blockers=[],
            recent_changes=[]
        )
        d = summary.to_dict()
        self.assertEqual(d["project_type"], "node")


class TestFileAnalyzer(unittest.TestCase):
    """Tests for FileAnalyzer class."""
    
    def test_detect_python_file(self):
        """Test detecting Python file."""
        ftype = FileAnalyzer.detect_file_type(Path("test.py"))
        self.assertEqual(ftype, FileType.PYTHON)
    
    def test_detect_javascript_file(self):
        """Test detecting JavaScript file."""
        ftype = FileAnalyzer.detect_file_type(Path("app.js"))
        self.assertEqual(ftype, FileType.JAVASCRIPT)
    
    def test_detect_typescript_file(self):
        """Test detecting TypeScript file."""
        ftype = FileAnalyzer.detect_file_type(Path("app.ts"))
        self.assertEqual(ftype, FileType.TYPESCRIPT)
    
    def test_detect_json_file(self):
        """Test detecting JSON file."""
        ftype = FileAnalyzer.detect_file_type(Path("config.json"))
        self.assertEqual(ftype, FileType.JSON_FILE)
    
    def test_detect_markdown_file(self):
        """Test detecting Markdown file."""
        ftype = FileAnalyzer.detect_file_type(Path("README.md"))
        self.assertEqual(ftype, FileType.MARKDOWN)
    
    def test_detect_unknown_file(self):
        """Test detecting unknown file."""
        ftype = FileAnalyzer.detect_file_type(Path("file.xyz"))
        self.assertEqual(ftype, FileType.UNKNOWN)
    
    def test_analyze_python_file(self):
        """Test analyzing Python file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text('''
def hello():
    """Say hello."""
    print("Hello")

class MyClass:
    """A class."""
    pass

import os
from pathlib import Path

# TODO: Add more functions
''')
            
            summary = FileAnalyzer.analyze_file(filepath)
            
            self.assertEqual(summary.file_type, FileType.PYTHON)
            self.assertGreater(len(summary.key_elements), 0)
            self.assertIn("os", summary.imports)
            self.assertGreater(len(summary.todos), 0)
    
    def test_analyze_javascript_file(self):
        """Test analyzing JavaScript file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.js"
            filepath.write_text('''
function greet() {
    console.log("Hello");
}

const add = (a, b) => a + b;

class Calculator {
    add(a, b) {
        return a + b;
    }
}

import React from 'react';
const fs = require('fs');
''')
            
            summary = FileAnalyzer.analyze_file(filepath)
            
            self.assertEqual(summary.file_type, FileType.JAVASCRIPT)
            self.assertGreater(len(summary.key_elements), 0)
    
    def test_extract_todos(self):
        """Test extracting TODOs."""
        content = '''
# TODO: Fix this bug
// TODO: Add feature
/* TODO: Refactor */
'''
        todos = FileAnalyzer._extract_todos(content)
        self.assertGreater(len(todos), 0)
    
    def test_extract_blockers(self):
        """Test extracting blockers."""
        content = '''
# FIXME: This is broken
// HACK: Temporary workaround
/* BUG: Known issue */
'''
        blockers = FileAnalyzer._extract_blockers(content)
        self.assertGreater(len(blockers), 0)


class TestProjectAnalyzer(unittest.TestCase):
    """Tests for ProjectAnalyzer class."""
    
    def test_detect_node_project(self):
        """Test detecting Node.js project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg_json = Path(tmpdir) / "package.json"
            pkg_json.write_text('{"name": "test"}')
            
            ptype = ProjectAnalyzer.detect_project_type(Path(tmpdir))
            self.assertEqual(ptype, ProjectType.NODE)
    
    def test_detect_python_project(self):
        """Test detecting Python project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            req_txt = Path(tmpdir) / "requirements.txt"
            req_txt.write_text("flask==2.0.0")
            
            ptype = ProjectAnalyzer.detect_project_type(Path(tmpdir))
            self.assertEqual(ptype, ProjectType.PYTHON)
    
    def test_detect_rust_project(self):
        """Test detecting Rust project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cargo = Path(tmpdir) / "Cargo.toml"
            cargo.write_text('[package]\nname = "test"')
            
            ptype = ProjectAnalyzer.detect_project_type(Path(tmpdir))
            self.assertEqual(ptype, ProjectType.RUST)
    
    def test_detect_generic_project(self):
        """Test detecting generic project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ptype = ProjectAnalyzer.detect_project_type(Path(tmpdir))
            self.assertEqual(ptype, ProjectType.GENERIC)
    
    def test_analyze_node_project(self):
        """Test analyzing Node.js project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create package.json
            pkg_json = Path(tmpdir) / "package.json"
            pkg_json.write_text(json.dumps({
                "name": "test-project",
                "version": "1.0.0",
                "description": "A test project",
                "dependencies": {"express": "^4.18.0"},
                "devDependencies": {"jest": "^29.0.0"}
            }))
            
            # Create index.js
            index_js = Path(tmpdir) / "index.js"
            index_js.write_text('console.log("Hello");')
            
            summary = ProjectAnalyzer.analyze_project(Path(tmpdir))
            
            self.assertEqual(summary.project_type, ProjectType.NODE)
            self.assertEqual(summary.name, "test-project")
            self.assertEqual(summary.version, "1.0.0")
            self.assertIn("express", summary.dependencies)
    
    def test_analyze_python_project(self):
        """Test analyzing Python project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create requirements.txt
            req_txt = Path(tmpdir) / "requirements.txt"
            req_txt.write_text("flask>=2.0.0\nrequests")
            
            # Create main.py
            main_py = Path(tmpdir) / "main.py"
            main_py.write_text('print("Hello")')
            
            summary = ProjectAnalyzer.analyze_project(Path(tmpdir))
            
            self.assertEqual(summary.project_type, ProjectType.PYTHON)
            self.assertIn("flask", summary.dependencies)


class TestContextSynth(unittest.TestCase):
    """Tests for ContextSynth class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.synth = ContextSynth()
        self.tmpdir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
    
    def test_init_default(self):
        """Test default initialization."""
        synth = ContextSynth()
        self.assertEqual(synth.detail_level, DetailLevel.STANDARD)
    
    def test_init_brief(self):
        """Test brief initialization."""
        synth = ContextSynth(DetailLevel.BRIEF)
        self.assertEqual(synth.detail_level, DetailLevel.BRIEF)
    
    def test_summarize_file(self):
        """Test file summarization."""
        filepath = Path(self.tmpdir) / "test.py"
        filepath.write_text("def hello():\n    pass")
        
        summary = self.synth.summarize_file(filepath)
        
        self.assertIsInstance(summary, FileSummary)
        self.assertEqual(summary.file_type, FileType.PYTHON)
    
    def test_summarize_folder(self):
        """Test folder summarization."""
        # Create test files
        (Path(self.tmpdir) / "test1.py").write_text("print(1)")
        (Path(self.tmpdir) / "test2.py").write_text("print(2)")
        
        summary = self.synth.summarize_folder(Path(self.tmpdir))
        
        self.assertIsInstance(summary, FolderSummary)
        self.assertEqual(summary.file_count, 2)
    
    def test_summarize_project(self):
        """Test project summarization."""
        # Create package.json
        (Path(self.tmpdir) / "package.json").write_text('{"name": "test"}')
        
        summary = self.synth.summarize_project(Path(self.tmpdir))
        
        self.assertIsInstance(summary, ProjectSummary)
        self.assertEqual(summary.project_type, ProjectType.NODE)
    
    def test_format_markdown_file(self):
        """Test markdown formatting for file."""
        filepath = Path(self.tmpdir) / "test.py"
        filepath.write_text("def hello():\n    pass")
        
        summary = self.synth.summarize_file(filepath)
        markdown = self.synth.format_markdown(summary)
        
        self.assertIn("# File Summary", markdown)
        self.assertIn("test.py", markdown)
    
    def test_format_json_file(self):
        """Test JSON formatting for file."""
        filepath = Path(self.tmpdir) / "test.py"
        filepath.write_text("def hello():\n    pass")
        
        summary = self.synth.summarize_file(filepath)
        json_str = self.synth.format_json(summary)
        
        data = json.loads(json_str)
        self.assertIn("path", data)
        self.assertIn("file_type", data)
    
    def test_format_text_file(self):
        """Test text formatting for file."""
        filepath = Path(self.tmpdir) / "test.py"
        filepath.write_text("def hello():\n    pass")
        
        summary = self.synth.summarize_file(filepath)
        text = self.synth.format_text(summary)
        
        self.assertIn("File:", text)
        self.assertIn("Type:", text)
    
    def test_format_markdown_project(self):
        """Test markdown formatting for project."""
        (Path(self.tmpdir) / "package.json").write_text('{"name": "test", "version": "1.0.0"}')
        
        summary = self.synth.summarize_project(Path(self.tmpdir))
        markdown = self.synth.format_markdown(summary)
        
        self.assertIn("# Project Summary", markdown)
    
    def test_format_json_project(self):
        """Test JSON formatting for project."""
        (Path(self.tmpdir) / "package.json").write_text('{"name": "test"}')
        
        summary = self.synth.summarize_project(Path(self.tmpdir))
        json_str = self.synth.format_json(summary)
        
        data = json.loads(json_str)
        self.assertIn("project_type", data)


class TestCLI(unittest.TestCase):
    """Tests for CLI interface."""
    
    def test_file_command(self):
        """Test file command."""
        import sys
        from io import StringIO
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text("print('hello')")
            
            captured = StringIO()
            sys.stdout = captured
            
            try:
                from contextsynth import main
                with patch('sys.argv', ['contextsynth', 'file', str(filepath)]):
                    main()
            except SystemExit:
                pass
            finally:
                sys.stdout = sys.__stdout__
            
            output = captured.getvalue()
            self.assertIn("File Summary", output)
    
    def test_project_command(self):
        """Test project command."""
        import sys
        from io import StringIO
        
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text('{"name": "test"}')
            
            captured = StringIO()
            sys.stdout = captured
            
            try:
                from contextsynth import main
                with patch('sys.argv', ['contextsynth', 'project', tmpdir]):
                    main()
            except SystemExit:
                pass
            finally:
                sys.stdout = sys.__stdout__
            
            output = captured.getvalue()
            self.assertIn("Project Summary", output)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_empty_file(self):
        """Test analyzing empty file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "empty.py"
            filepath.write_text("")
            
            summary = FileAnalyzer.analyze_file(filepath)
            self.assertEqual(summary.line_count, 1)  # Even empty file has 1 line
    
    def test_binary_file(self):
        """Test handling binary file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.bin"
            filepath.write_bytes(b'\x00\x01\x02\x03')
            
            summary = FileAnalyzer.analyze_file(filepath)
            self.assertEqual(summary.file_type, FileType.UNKNOWN)
    
    def test_nonexistent_file(self):
        """Test with non-existent file."""
        synth = ContextSynth()
        # Should not crash - returns summary with empty content
        summary = synth.summarize_file(Path("C:/nonexistent/path.py"))
        self.assertEqual(summary.line_count, 1)
        self.assertEqual(summary.size_bytes, 0)
    
    def test_malformed_python(self):
        """Test analyzing malformed Python."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "broken.py"
            filepath.write_text("def broken(\n  syntax error here")
            
            # Should fall back to regex analysis
            summary = FileAnalyzer.analyze_file(filepath)
            self.assertIsInstance(summary, FileSummary)
    
    def test_deeply_nested_project(self):
        """Test project with deep nesting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create deep structure
            deep = Path(tmpdir) / "a" / "b" / "c" / "d"
            deep.mkdir(parents=True)
            (deep / "deep.py").write_text("print('deep')")
            (Path(tmpdir) / "package.json").write_text('{"name": "test"}')
            
            synth = ContextSynth()
            summary = synth.summarize_project(Path(tmpdir))
            
            self.assertIsInstance(summary, ProjectSummary)


class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    def test_full_node_project(self):
        """Test full Node.js project analysis."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create realistic project structure
            (Path(tmpdir) / "package.json").write_text(json.dumps({
                "name": "my-app",
                "version": "2.0.0",
                "description": "A sample application",
                "dependencies": {
                    "express": "^4.18.0",
                    "react": "^18.0.0"
                },
                "devDependencies": {
                    "jest": "^29.0.0"
                }
            }))
            
            (Path(tmpdir) / "README.md").write_text("# My App\n\nA sample application.")
            
            src = Path(tmpdir) / "src"
            src.mkdir()
            (src / "index.js").write_text('''
import express from 'express';
// TODO: Add routes
const app = express();
export default app;
''')
            
            synth = ContextSynth(DetailLevel.DETAILED)
            summary = synth.summarize_project(Path(tmpdir))
            
            self.assertEqual(summary.name, "my-app")
            self.assertEqual(summary.version, "2.0.0")
            self.assertIn("express", summary.dependencies)
            self.assertIn("react", summary.dependencies)
    
    def test_full_python_project(self):
        """Test full Python project analysis."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create realistic project structure
            (Path(tmpdir) / "requirements.txt").write_text("flask>=2.0.0\nrequests\npytest")
            
            (Path(tmpdir) / "main.py").write_text('''
"""Main application module."""

from flask import Flask

# TODO: Add authentication

app = Flask(__name__)

def create_app():
    """Create and configure the app."""
    return app

if __name__ == "__main__":
    app.run()
''')
            
            synth = ContextSynth()
            summary = synth.summarize_project(Path(tmpdir))
            
            self.assertEqual(summary.project_type, ProjectType.PYTHON)
            self.assertIn("flask", summary.dependencies)


class TestVersion(unittest.TestCase):
    """Test version information."""
    
    def test_version_exists(self):
        """Test that version is defined."""
        self.assertEqual(__version__, "1.0.0")


if __name__ == '__main__':
    unittest.main(verbosity=2)
