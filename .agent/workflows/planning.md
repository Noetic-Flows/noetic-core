---
description: Structured Project Planning and Task Decomposition
---

# Project Planning Workflow

Use this workflow when starting a new project or a complex task that requires coordination.

1. **Intent Extraction**: Ask Taylor for the high-level goal.
2. **Context Assembly**:
    - Search `.agent/persona.md` for grounding.
    - Search `notes/` for relevant project history.
    - Query NotebookLM for strategic insights if applicable.
3. **Draft implementation_plan.md**:
    - Define outcomes, not just outputs.
    - List high-stakes actions requiring `INTERRUPT`.
4. **Decomposition**:
    - Break the plan into `task.md` items.
    - Populate `notes/tasks/to_do.md` with the immediate next steps.
5. **Approval**: Call `notify_user` with the plan and wait for the "Shadow Action" approval.

// turbo
6. Initialize the development environment (venv, docker, etc.).
