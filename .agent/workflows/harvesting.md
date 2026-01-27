---
description: Knowledge Harvesting and Memory Persistence
---

# Knowledge Harvesting Workflow

Use this workflow at the end of a session or after significant progress is made.

1. **Insight Identification**: Scan the conversation history for key decisions, new facts, or architectural shifts.
2. **Update vision.md/architecture.md**: If the system's core has shifted, update these files immediately.
3. **Task Delta**:
    - Mark completed items in `notes/tasks/master_list.md`.
    - Extract "future considerations" into `notes/tasks/to_do.md`.
4. **NotebookLM Sync**:
    - Identify if any new notes should be added to a Google NotebookLM for deep research.
    - Use `mcp_notebooklm` to suggest source additions.
5. **Session Wrap-up**: Brief Taylor on the "Current State of the Mesh".
