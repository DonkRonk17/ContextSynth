# 📋 ContextSynth

## Instant Context Summarizer for Any File or Project

**Generate one-click context summaries for files, folders, and entire projects. Perfect for handoffs, reviews, and session starts.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: 56 Passing](https://img.shields.io/badge/tests-56%20passing-brightgreen.svg)](test_contextsynth.py)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](requirements.txt)

---

## 📖 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [CLI Reference](#-cli-reference)
- [API Reference](#-api-reference)
- [Output Formats](#-output-formats)
- [Examples](#-examples)
- [Integration with Team Brain](#-integration-with-team-brain)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)
- [Credits](#-credits)

---

## 🔥 The Problem

**Context switching is expensive.** AI agents and developers constantly need quick context:

- Starting a new session? What's the project about?
- Handing off to another agent? What was done?
- Reviewing code? What's in this file?
- Debugging? What are the dependencies?

**Manual context gathering:**
- Open multiple files
- Scan for important elements
- Note dependencies
- Find TODOs and blockers
- Format for sharing

**Time wasted: 5-15 minutes per context switch.**

---

## 🎯 The Solution

**ContextSynth** generates instant summaries with one command:

```bash
python contextsynth.py project .

# Project Summary: my-app

**Type:** node
**Version:** 2.0.0
**Files:** 47
**Total Lines:** 3,892

> A modern web application built with React

## Technologies
**React**, **Express.js**, **Tailwind CSS**, **Socket.IO**

## Entry Points
- `src/index.js`
- `server/app.js`

## Dependencies
`react`, `express`, `socket.io`, `tailwindcss`, `axios`

## TODOs
- [ ] Add authentication
- [ ] Implement caching
- [ ] Write tests

## Recent Changes
- abc1234 feat: Add user dashboard
- def5678 fix: Socket connection issues
```

**Time saved: 10+ minutes per session.**

---

## ⚡ Installation

### Option 1: Direct Use (Recommended)

```bash
# Clone or download
git clone https://github.com/DonkRonk17/ContextSynth.git
cd ContextSynth

# Use directly (zero dependencies!)
python contextsynth.py project /path/to/project
```

### Option 2: Add to PATH

```bash
# Copy to tools directory
cp contextsynth.py ~/tools/

# Add alias (bash/zsh)
alias context="python ~/tools/contextsynth.py"
```

### Requirements

- **Python 3.8+** (uses dataclasses, pathlib)
- **Zero external dependencies** (standard library only)
- **Cross-platform** (Windows, macOS, Linux)

---

## 🚀 Quick Start

### 1. Summarize a Project

```bash
python contextsynth.py project .
```

### 2. Summarize a File

```bash
python contextsynth.py file src/app.py
```

### 3. Summarize a Folder

```bash
python contextsynth.py folder src/components
```

### 4. Export as JSON

```bash
python contextsynth.py project . --format json -o summary.json
```

---

## 📘 Usage

### Python API

```python
from pathlib import Path
from contextsynth import ContextSynth, DetailLevel

# Initialize with detail level
synth = ContextSynth(DetailLevel.DETAILED)

# Summarize project
summary = synth.summarize_project(Path("./my-app"))

# Format as markdown
markdown = synth.format_markdown(summary)
print(markdown)

# Or as JSON
json_str = synth.format_json(summary)
```

### Detail Levels

| Level | Description |
|-------|-------------|
| `BRIEF` | One-liners, minimal detail |
| `STANDARD` | Key points, moderate detail (default) |
| `DETAILED` | Full analysis, all elements |

---

## 💻 CLI Reference

### Commands

#### `project` - Summarize a Project

```bash
python contextsynth.py project [PATH] [OPTIONS]

Arguments:
  PATH              Project directory (default: current directory)

Options:
  --format, -f      Output format: markdown, json, text (default: markdown)
  --detail, -d      Detail level: brief, standard, detailed (default: standard)
  --output, -o      Save to file
```

**Examples:**

```bash
# Current project
python contextsynth.py project

# Specific project
python contextsynth.py project ./my-app

# JSON output
python contextsynth.py project . --format json

# Save to file
python contextsynth.py project . -o PROJECT_SUMMARY.md
```

#### `file` - Summarize a File

```bash
python contextsynth.py file <PATH> [OPTIONS]

Arguments:
  PATH              Path to file

Options:
  --format, -f      Output format
  --output, -o      Save to file
```

#### `folder` - Summarize a Folder

```bash
python contextsynth.py folder <PATH> [OPTIONS]

Arguments:
  PATH              Path to folder

Options:
  --format, -f      Output format
  --output, -o      Save to file
```

---

## 📚 API Reference

### Classes

#### `ContextSynth`

Main synthesis class.

```python
class ContextSynth:
    def __init__(self, detail_level: DetailLevel = DetailLevel.STANDARD)
    
    def summarize_file(self, filepath: Path) -> FileSummary
    def summarize_folder(self, folder_path: Path) -> FolderSummary
    def summarize_project(self, project_path: Path) -> ProjectSummary
    
    def format_markdown(self, summary: Any) -> str
    def format_json(self, summary: Any) -> str
    def format_text(self, summary: Any) -> str
```

#### `FileSummary`

```python
@dataclass
class FileSummary:
    path: str
    file_type: FileType
    size_bytes: int
    line_count: int
    description: str
    key_elements: List[CodeElement]
    imports: List[str]
    todos: List[str]
    blockers: List[str]
    dependencies: List[str]
```

#### `ProjectSummary`

```python
@dataclass
class ProjectSummary:
    path: str
    project_type: ProjectType
    name: str
    description: str
    version: Optional[str]
    file_count: int
    total_lines: int
    main_technologies: List[str]
    dependencies: List[str]
    dev_dependencies: List[str]
    entry_points: List[str]
    key_files: List[FileSummary]
    todos: List[str]
    blockers: List[str]
    recent_changes: List[str]
```

### Enums

#### `DetailLevel`

```python
class DetailLevel(Enum):
    BRIEF = "brief"
    STANDARD = "standard"
    DETAILED = "detailed"
```

#### `FileType`

```python
class FileType(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JSON_FILE = "json"
    MARKDOWN = "markdown"
    # ... and more
```

#### `ProjectType`

```python
class ProjectType(Enum):
    PYTHON = "python"
    NODE = "node"
    REACT = "react"
    RUST = "rust"
    TAURI = "tauri"
    GENERIC = "generic"
```

---

## 📄 Output Formats

### Markdown (Default)

Best for documentation and sharing:

```markdown
# Project Summary: my-app

**Type:** node
**Version:** 1.0.0
**Files:** 23

## Technologies
**React**, **TypeScript**

## Dependencies
`react`, `typescript`, `axios`
```

### JSON

Best for programmatic use:

```json
{
  "name": "my-app",
  "project_type": "node",
  "version": "1.0.0",
  "file_count": 23,
  "dependencies": ["react", "typescript", "axios"]
}
```

### Text

Best for quick terminal viewing:

```
Project: my-app
Type: node
Version: 1.0.0
Files: 23
Technologies: React, TypeScript
```

---

## 📝 Examples

### Example 1: Session Start Context

```bash
# First thing when starting a session
python contextsynth.py project . > SESSION_CONTEXT.md

# Now you have full project context!
```

### Example 2: Agent Handoff

```python
from contextsynth import ContextSynth
from pathlib import Path

def prepare_handoff(project_path: str) -> str:
    """Prepare context for agent handoff."""
    synth = ContextSynth()
    summary = synth.summarize_project(Path(project_path))
    
    handoff = f"""
# Agent Handoff Context

{synth.format_markdown(summary)}

## Current Status
- Session complete at {datetime.now()}
- Ready for next agent
"""
    return handoff
```

### Example 3: Code Review Context

```bash
# Get context for a specific file before review
python contextsynth.py file src/components/UserDashboard.tsx

# Output includes:
# - Key functions/classes
# - Imports
# - TODOs
# - Blockers
```

### Example 4: CI/CD Integration

```yaml
# Generate project summary on every build
- name: Generate Context Summary
  run: |
    python contextsynth.py project . --format json -o context.json
    
- name: Upload Context
  uses: actions/upload-artifact@v3
  with:
    name: project-context
    path: context.json
```

---

## 🤖 Integration with Team Brain

### For FORGE (Orchestrator)

Pre-task context gathering:

```python
def get_task_context(project_path: str) -> str:
    synth = ContextSynth(DetailLevel.BRIEF)
    summary = synth.summarize_project(Path(project_path))
    return synth.format_text(summary)
```

### For IRIS/NEXUS (Development Agents)

Session start:

```bash
# Add to session startup
python contextsynth.py project . > .session-context.md
echo "Context loaded for session"
```

### For BOLT (Executor)

Build context:

```bash
# Pre-build context check
python contextsynth.py project . --format json | jq '.todos | length'
# Shows number of TODOs to address
```

### Combines with AgentHandoff

```python
from agenthandoff import create_handoff
from contextsynth import ContextSynth

# Enrich handoff with project context
synth = ContextSynth()
context = synth.format_markdown(synth.summarize_project(Path(".")))
handoff = create_handoff(context=context)
```

---

## 🔧 Troubleshooting

### "No project type detected"

The project doesn't have standard config files. Create one:

```bash
# For Node.js
npm init -y

# For Python
echo "flask>=2.0" > requirements.txt
```

### Large projects are slow

Use brief mode:

```bash
python contextsynth.py project . --detail brief
```

### Missing elements in summary

Use detailed mode:

```bash
python contextsynth.py project . --detail detailed
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 👏 Credits

### Created By
**ATLAS** (Team Brain - Cursor Sonnet 4.5 Agent)  
Tool Creator, QA Specialist, Automation Engineer

### Requested By
**Copilot VSCode** (Tool Request #25)

### Owner
**Logan Smith** / **Metaphy LLC**

### Team Brain Contributors
- **FORGE** - Orchestrator, Protocol Designer
- **CLIO** - CLI Agent, Trophy Keeper
- **IRIS** - Desktop Development Specialist
- **NEXUS** - VS Code Integration Specialist

---

## 📊 Version History

### v1.0.0 (January 24, 2026)
- Initial release
- File, folder, and project summarization
- Python and JavaScript/TypeScript analysis
- Markdown, JSON, and text output
- Git integration for recent changes
- TODO and blocker extraction
- 56 tests with 100% pass rate

---

**ContextSynth** - *Instant context. Zero friction.*

For the Maximum Benefit of Life. 🔆⚒️🔗
