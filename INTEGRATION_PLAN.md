# ContextSynth Integration Plan

## Team Brain Agent Integration Strategy

---

## Integration Goals

1. **Instant Context**: One-click summaries for any project
2. **Session Efficiency**: Reduce context-gathering time by 10+ minutes
3. **Handoff Quality**: Rich context for agent transitions
4. **Automation Ready**: JSON output for CI/CD

---

## Agent-Specific Integrations

### FORGE (Orchestrator)

**Use Case:** Pre-task context gathering

```python
from contextsynth import ContextSynth

def prepare_task_context(project_path: str) -> str:
    synth = ContextSynth()
    summary = synth.summarize_project(Path(project_path))
    return synth.format_text(summary)

# Include in task assignment
context = prepare_task_context("./project")
task["context"] = context
```

---

### IRIS/NEXUS (Development Agents)

**Use Case:** Session start context

```bash
# Add to session startup
python contextsynth.py project . > .session-context.md
cat .session-context.md
```

---

### BOLT (Executor)

**Use Case:** Build context verification

```bash
# Pre-build context
python contextsynth.py project . --format json | jq '{
  name: .name,
  todos: (.todos | length),
  blockers: (.blockers | length)
}'
```

---

### CLIO (CLI Agent)

**Use Case:** Quick project summaries

```bash
# Quick context
alias ctx="python contextsynth.py project . --detail brief --format text"
```

---

## Tool Interoperability

### Combines with AgentHandoff

```python
from agenthandoff import create_handoff
from contextsynth import ContextSynth

synth = ContextSynth()
context = synth.format_markdown(synth.summarize_project(Path(".")))
handoff = create_handoff(context=context)
```

### Combines with SynapseLink

```python
from synapselink import quick_send
from contextsynth import ContextSynth

synth = ContextSynth()
summary = synth.summarize_project(Path("."))

quick_send(
    "FORGE",
    f"Project Update: {summary.name}",
    synth.format_text(summary)
)
```

### Combines with DevSnapshot

```python
from devsnapshot import capture_snapshot
from contextsynth import ContextSynth

# Enrich snapshot with project context
synth = ContextSynth()
summary = synth.summarize_project(Path("."))
snapshot = capture_snapshot()
snapshot["project_context"] = summary.to_dict()
```

---

## Deployment Scenarios

### Per-Session

```bash
# Run at session start
python contextsynth.py project . > SESSION_CONTEXT.md
```

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
python contextsynth.py project . > CONTEXT.md
git add CONTEXT.md
```

### CI/CD Pipeline

```yaml
- name: Generate Context
  run: python contextsynth.py project . --format json -o context.json
```

---

## Implementation Checklist

- [ ] Deploy to shared tools location
- [ ] Add session start aliases for each agent
- [ ] Configure CI/CD context generation
- [ ] Set up Synapse integration
- [ ] Document in MEMORY_CORE

---

**ContextSynth** - *Instant context. Zero friction.*
