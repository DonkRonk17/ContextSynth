# ContextSynth Quick Start Guides

## Agent-Specific 5-Minute Guides

---

## FORGE Quick Start (Orchestrator)

### Step 1: Get Project Context

```bash
python contextsynth.py project /path/to/project --format text
```

### Step 2: Include in Task Assignment

```python
context = subprocess.run(
    ["python", "contextsynth.py", "project", project_path, "-f", "text"],
    capture_output=True, text=True
).stdout

task["context"] = context
```

### Step 3: Share via Synapse

```bash
python contextsynth.py project . > /tmp/context.md
# Attach to Synapse message
```

---

## IRIS/NEXUS Quick Start (Development)

### Step 1: Add Session Start Script

```bash
# ~/.bashrc or session startup
alias session-context="python contextsynth.py project . --detail standard"
```

### Step 2: Run at Session Start

```bash
cd /path/to/project
session-context
```

### Step 3: Save for Reference

```bash
python contextsynth.py project . -o SESSION_CONTEXT.md
```

---

## BOLT Quick Start (Executor)

### Step 1: Pre-Build Check

```bash
python contextsynth.py project . --format json | jq '.blockers'
```

### Step 2: Build Script Integration

```bash
#!/bin/bash
# Pre-build context
BLOCKERS=$(python contextsynth.py project . -f json | jq '.blockers | length')
if [ "$BLOCKERS" -gt 0 ]; then
    echo "Warning: $BLOCKERS blocker(s) found"
fi
```

---

## CLIO Quick Start (CLI Agent)

### Step 1: Add Aliases

```bash
alias ctx="python contextsynth.py project . --detail brief -f text"
alias ctxf="python contextsynth.py file"
alias ctxd="python contextsynth.py folder"
```

### Step 2: Quick Usage

```bash
ctx                    # Project summary
ctxf src/app.py        # File summary
ctxd src/components    # Folder summary
```

---

## Common Commands

```bash
# Project summary (markdown)
python contextsynth.py project .

# Project summary (JSON)
python contextsynth.py project . --format json

# File summary
python contextsynth.py file src/main.py

# Folder summary
python contextsynth.py folder src/

# Save to file
python contextsynth.py project . -o CONTEXT.md
```

---

**ContextSynth** - *Instant context. Zero friction.*
