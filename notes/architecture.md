# Noetic Architecture: The Federated Brain

The Noetic architecture facilitates a "Federated Monorepo" where distinct parts of the "Brain" (Memory, Safety, UI) are built as standalone, publishable libraries.

## 1. The Brain (The OS)
The cognitive core that runs as a background server (`noetic_engine`).

- **The Engine Loop:** An Actor-Critic architecture that continuously runs `Perceive -> Plan -> Act -> Evaluate`.
- **Memory Architecture:**
    - **IntentNode (The Stack):** Working memory scoped to the current active "Stanza". Automatically garbage collected when the task ends.
    - **Tri-Store (The Heap):** Long-term persistence stored in SQLite/libSQL.
        - *Episodic:* Logs of past actions.
        - *Semantic:* Knowledge graph of facts and relationships.
        - *Procedural:* "Skills" or cached plans.
- **The Conscience:** A safety interceptor that acts as a gateway for all tool calls and high-stakes actions.

## 2. The Machine (The Client)
The runtime environments where the user interacts with the Brain.

- **FastUI / Reflex:** The Server-Driven UI protocol. The Engine renders the UI tree, and the Client (Web Hub, CLI, VSCode) simply displays it.
- **The Web Hub:** A Next.js application acting as the primary "Visual Cortex" for the user.
- **ASP (Agent Server Protocol):** The WebSocket-based standard (similar to LSP) that connects The Brain to The Machine.

## 3. The Protocol (The Language)
The data structures that define the system (`packages/spec`).

- **Codex (`.noetic`):** A portable file format wrapping a complete Flow definition.
- **Stanza:** A distinct phase of execution (e.g., "Research Stanza", "Coding Stanza").
- **IntentNode:** Atomic units of work within a Stanza.

## 4. Connectivity
- **MCP (Model Context Protocol):** The standard interface for tools and data sources.
