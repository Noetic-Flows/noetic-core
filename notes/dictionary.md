# The Noetic Dictionary

## Core Concepts

**Codex (`.noetic`)**
A self-contained, transportable file defining a Flow. It includes the Agents, their Persona, Knowledge dependencies, and Stanza definitions needed to execute a task.

**Flow**
A dynamic application state assembled to achieve a user goal. Unlike an "App" (static), a Flow is transient and adaptable.

**Stanza**
A distinct phase of execution within a Flow. Analogous to a "Scene" in a play or a "State" in a State Machine.
*   *Agentic Stanza:* "Here is the goal, figure it out." (Non-deterministic)
*   *Procedural Stanza:* "Follow these exact steps." (Deterministic)

**IntentNode**
The atomic unit of work inside a Stanza. Can be an Action, a Decision, or a split in control flow.

## Memory

**Seed**
A portable "Knowledge Pack" (often a JSON graph dump) that can be installed into an Agent's memory to give it instant proficiency in a domain (e.g., "GDPR Compliance Seed").

**Stack (FlowStack)**
Short-term, scoped memory relevant only to the current Stanza. Cleared upon completion.

**Heap (Tri-Store)**
Long-term memory including Episodic (logs), Semantic (facts), and Procedural (skills) data.

## Runtime

**ASP (Agent Server Protocol)**
The WebSocket protocol used to communicate between the Noetic Engine (Server) and clients (Web Hub, CLI).

**Conscience**
The safety module that evaluates proposed actions against a set of Principles before execution.

**Shadow Action**
A high-stakes action (like sending an email or deleting a file) that is "staged" by the Agent but requires explicit user approval via a UI card.
