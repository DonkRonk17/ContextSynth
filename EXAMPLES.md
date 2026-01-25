# ContextSynth Examples

## Comprehensive Usage Examples

---

## Example 1: Basic Project Summary

```bash
python contextsynth.py project .
```

**Output:**
```markdown
# Project Summary: my-app

**Type:** node
**Version:** 1.0.0
**Files:** 23
**Total Lines:** 1,847

> A sample web application

## Technologies
**React**, **Express.js**, **MongoDB**

## Entry Points
- `src/index.js`

## Dependencies
`react`, `express`, `mongoose`, `axios`
```

---

## Example 2: File Analysis

```bash
python contextsynth.py file src/components/UserDashboard.tsx
```

**Output:**
```markdown
# File Summary: UserDashboard.tsx

**Path:** `src/components/UserDashboard.tsx`
**Type:** typescript
**Size:** 4,521 bytes
**Lines:** 156

## Key Elements

- **function** `UserDashboard` (line 12)
  - Main dashboard component
- **function** `useUserData` (line 45)
  - Custom hook for user data
- **function** `formatDate` (line 89)

## Imports

`react`, `@/hooks/useAuth`, `@/components/Card`

## TODOs

- [ ] Add loading state
- [ ] Implement pagination
```

---

## Example 3: JSON Export for CI/CD

```bash
python contextsynth.py project . --format json -o context.json
```

**Output (context.json):**
```json
{
  "path": "/projects/my-app",
  "project_type": "node",
  "name": "my-app",
  "version": "1.0.0",
  "file_count": 23,
  "total_lines": 1847,
  "main_technologies": ["React", "Express.js"],
  "dependencies": ["react", "express", "axios"],
  "todos": ["Add authentication", "Write tests"]
}
```

---

## Example 4: Agent Handoff

```python
from pathlib import Path
from contextsynth import ContextSynth, DetailLevel

def create_handoff_context(project_path: str) -> str:
    """Generate context for agent handoff."""
    synth = ContextSynth(DetailLevel.DETAILED)
    summary = synth.summarize_project(Path(project_path))
    
    return f"""
# AGENT HANDOFF CONTEXT
Generated: {datetime.now().isoformat()}

{synth.format_markdown(summary)}

## Handoff Notes
- Session complete
- Ready for next agent
- Check TODOs above for pending work
"""

# Usage
context = create_handoff_context("./my-app")
print(context)
```

---

## Example 5: Session Start Script

```bash
#!/bin/bash
# session-start.sh

echo "=== SESSION CONTEXT ==="
python contextsynth.py project . --detail brief

echo ""
echo "=== RECENT CHANGES ==="
git log --oneline -5

echo ""
echo "=== TODOS ==="
python contextsynth.py project . --format json | jq '.todos[]'
```

---

## Example 6: Folder Analysis

```bash
python contextsynth.py folder src/components
```

**Output:**
```markdown
# Folder Summary: components

**Path:** `src/components`
**Files:** 12
**Total Lines:** 1,234

## File Types

- typescript: 8
- css: 4

## Files

- `Button.tsx` - Button.tsx - 1 class(es) - 45 lines
- `Card.tsx` - Card.tsx - 1 class(es) - 67 lines
- `Modal.tsx` - Modal.tsx - 2 function(s) - 89 lines
```

---

## Example 7: Multiple Projects Dashboard

```python
from pathlib import Path
from contextsynth import ContextSynth

projects = ["./frontend", "./backend", "./mobile"]

synth = ContextSynth()

print(f"{'Project':<20} {'Type':<10} {'Files':<8} {'Lines':<10}")
print("-" * 50)

for project in projects:
    summary = synth.summarize_project(Path(project))
    print(f"{summary.name:<20} {summary.project_type.value:<10} "
          f"{summary.file_count:<8} {summary.total_lines:<10}")
```

---

## Example 8: Integration with SynapseLink

```python
from pathlib import Path
from contextsynth import ContextSynth
# from synapselink import quick_send

def share_project_context(project_path: str, recipients: str):
    """Share project context via Synapse."""
    synth = ContextSynth()
    summary = synth.summarize_project(Path(project_path))
    
    message = f"""PROJECT CONTEXT UPDATE

{synth.format_text(summary)}

Full markdown summary attached.
"""
    
    # quick_send(recipients, f"Context: {summary.name}", message)
    print(f"Would send to {recipients}:\n{message}")

# Usage
share_project_context("./my-app", "FORGE,CLIO")
```

---

## Example 9: Pre-Build Validation

```python
from pathlib import Path
from contextsynth import ContextSynth

def pre_build_check(project_path: str) -> bool:
    """Check project before building."""
    synth = ContextSynth()
    summary = synth.summarize_project(Path(project_path))
    
    # Check for blockers
    if summary.blockers:
        print(f"[!] {len(summary.blockers)} blocker(s) found:")
        for blocker in summary.blockers:
            print(f"  - {blocker}")
        return False
    
    # Check for critical TODOs
    critical = [t for t in summary.todos if "CRITICAL" in t.upper()]
    if critical:
        print(f"[!] {len(critical)} critical TODO(s):")
        for todo in critical:
            print(f"  - {todo}")
        return False
    
    print("[OK] No blockers, ready to build")
    return True

# Usage
pre_build_check("./my-app")
```

---

## Example 10: Git Hook Integration

```python
#!/usr/bin/env python3
# .git/hooks/pre-commit

from pathlib import Path
from contextsynth import ContextSynth

def update_context_file():
    """Update context file on commit."""
    synth = ContextSynth()
    summary = synth.summarize_project(Path("."))
    
    with open("CONTEXT.md", "w") as f:
        f.write(synth.format_markdown(summary))
    
    print("Updated CONTEXT.md")

if __name__ == "__main__":
    update_context_file()
```

---

## Example 11: Compare Projects

```python
from pathlib import Path
from contextsynth import ContextSynth

def compare_projects(path1: str, path2: str):
    """Compare two projects."""
    synth = ContextSynth()
    
    s1 = synth.summarize_project(Path(path1))
    s2 = synth.summarize_project(Path(path2))
    
    print(f"{'Metric':<20} {s1.name:<15} {s2.name:<15}")
    print("-" * 50)
    print(f"{'Files':<20} {s1.file_count:<15} {s2.file_count:<15}")
    print(f"{'Lines':<20} {s1.total_lines:<15} {s2.total_lines:<15}")
    print(f"{'Dependencies':<20} {len(s1.dependencies):<15} {len(s2.dependencies):<15}")
    print(f"{'TODOs':<20} {len(s1.todos):<15} {len(s2.todos):<15}")

# Usage
compare_projects("./v1", "./v2")
```

---

## Example 12: Quick Context for Debugging

```bash
# One-liner for quick context
python -c "
from contextsynth import ContextSynth
from pathlib import Path
s = ContextSynth().summarize_project(Path('.'))
print(f'{s.name} | {s.project_type.value} | {s.file_count} files | {len(s.todos)} TODOs')
"
```

---

**ContextSynth** - *Instant context. Zero friction.*
