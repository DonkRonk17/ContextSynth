# ContextSynth Integration Examples

## Copy-Paste Ready Code

---

## 1. AgentHandoff Integration

```python
"""Enrich agent handoff with project context."""
from pathlib import Path
from contextsynth import ContextSynth
# from agenthandoff import create_handoff

def create_rich_handoff(project_path: str) -> dict:
    synth = ContextSynth()
    summary = synth.summarize_project(Path(project_path))
    
    return {
        "project_context": synth.format_markdown(summary),
        "summary": synth.format_text(summary),
        "data": summary.to_dict()
    }

handoff = create_rich_handoff("./my-app")
```

---

## 2. SynapseLink Integration

```python
"""Share context via Synapse."""
from pathlib import Path
from contextsynth import ContextSynth
# from synapselink import quick_send

def share_context(project_path: str, recipients: str):
    synth = ContextSynth()
    summary = synth.summarize_project(Path(project_path))
    
    message = f"""PROJECT CONTEXT: {summary.name}

{synth.format_text(summary)}

Dependencies: {len(summary.dependencies)}
TODOs: {len(summary.todos)}
"""
    
    # quick_send(recipients, f"Context: {summary.name}", message)
    print(message)

share_context("./project", "FORGE,CLIO")
```

---

## 3. DevSnapshot Integration

```python
"""Include context in dev snapshots."""
from pathlib import Path
from contextsynth import ContextSynth

def enhanced_snapshot(project_path: str) -> dict:
    synth = ContextSynth()
    summary = synth.summarize_project(Path(project_path))
    
    return {
        "timestamp": datetime.now().isoformat(),
        "project": {
            "name": summary.name,
            "type": summary.project_type.value,
            "files": summary.file_count,
            "lines": summary.total_lines
        },
        "todos": summary.todos,
        "blockers": summary.blockers
    }

snapshot = enhanced_snapshot(".")
```

---

## 4. CI/CD Pipeline

```yaml
# GitHub Actions
name: Build with Context

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate Context
        run: |
          python contextsynth.py project . --format json -o context.json
          echo "Project: $(jq -r '.name' context.json)"
          echo "TODOs: $(jq '.todos | length' context.json)"
      
      - name: Upload Context
        uses: actions/upload-artifact@v3
        with:
          name: project-context
          path: context.json
```

---

## 5. Pre-Commit Hook

```python
#!/usr/bin/env python3
"""Git pre-commit hook to update context."""
from pathlib import Path
from contextsynth import ContextSynth

def update_context():
    synth = ContextSynth()
    summary = synth.summarize_project(Path("."))
    
    with open("CONTEXT.md", "w") as f:
        f.write(synth.format_markdown(summary))
    
    # Stage the file
    import subprocess
    subprocess.run(["git", "add", "CONTEXT.md"])

if __name__ == "__main__":
    update_context()
```

---

## 6. Session Start Script

```bash
#!/bin/bash
# session-start.sh

PROJECT_PATH="${1:-.}"

echo "=== PROJECT CONTEXT ==="
python contextsynth.py project "$PROJECT_PATH" --detail brief --format text

echo ""
echo "=== KEY FILES ==="
python contextsynth.py project "$PROJECT_PATH" --format json | \
    jq -r '.key_files[].path' | head -5

echo ""
echo "=== TODOs ==="
python contextsynth.py project "$PROJECT_PATH" --format json | \
    jq -r '.todos[]' | head -5
```

---

## 7. Multi-Project Dashboard

```python
"""Dashboard for multiple projects."""
from pathlib import Path
from contextsynth import ContextSynth

def project_dashboard(projects: list):
    synth = ContextSynth()
    
    print(f"{'Project':<20} {'Type':<10} {'Files':<8} {'TODOs':<6}")
    print("-" * 50)
    
    for project in projects:
        try:
            summary = synth.summarize_project(Path(project))
            print(f"{summary.name:<20} {summary.project_type.value:<10} "
                  f"{summary.file_count:<8} {len(summary.todos):<6}")
        except Exception as e:
            print(f"{project:<20} ERROR: {e}")

# Usage
project_dashboard(["./frontend", "./backend", "./mobile"])
```

---

## 8. TaskFlow Integration

```python
"""Add context to tasks."""
from pathlib import Path
from contextsynth import ContextSynth

def enrich_task(task: dict) -> dict:
    if "project_path" not in task:
        return task
    
    synth = ContextSynth()
    summary = synth.summarize_project(Path(task["project_path"]))
    
    task["context"] = {
        "name": summary.name,
        "type": summary.project_type.value,
        "technologies": summary.main_technologies,
        "todos": len(summary.todos)
    }
    
    return task

# Usage
task = {"id": 1, "project_path": "./my-app"}
task = enrich_task(task)
```

---

**ContextSynth** - *Instant context. Zero friction.*
