# Technical Specification: Noetic Knowledge Engine (v3.0)

**Module:** `noetic.knowledge`
**Core Philosophy:** "Context as a Shared Program"
**Status:** Architecture Frozen

---

## 1. Executive Summary

The **Noetic Knowledge Engine** transforms the concept of "Memory" from a passive database into an active **Cognitive Operating System**. It addresses the twin failures of current Agentic AI: **Token Bloat** (Context Window overflow) and **Siloed Reality** (Multi-agent coordination failure).

The architecture unifies **AgentProg** (Stack-based memory management) with a **Shared Semantic Environment** (Federated Knowledge Graph).

1. **The Virtual Machine Model:** We treat the Agent's context window like a CPU Cache. It has a **Stack** (Short-term scope) and a **Heap** (Long-term storage). Data is strictly scoped; when a task finishes, its noise is Garbage Collected.
2. **The Hive Mind Model:** Agents do not possess private databases. They view a **Shared Heap** through strictly permissioned **Scopes**. When one agent updates the world state, all subscribed agents perceive it instantly.

---

## 2. Architecture: The Tri-Layer Brain

The module is divided into three functional layers, mimicking a biological brain's hierarchy.

### 2.1 Layer 1: Working Memory (The Stack)

**Module:** `noetic.knowledge.working`
**Role:** The "RAM" — Finite, Fast, Scoped.

This layer implements the **AgentProg** architecture.

- **Memory Frames:** Context is segmented into nested frames (Stack).
- **Local Variables:** Logs, scratchpad thoughts, and intermediate tool outputs exist _only_ within the active frame.
- **Garbage Collection:** When a frame is popped (Task Complete), all local variables are destroyed. Only the explicit **Return Value** is promoted to the Heap.

**The Stack Object:**

```python
class MemoryFrame:
    id: UUID
    goal: str               # "Research Vendor X"
    scope_permissions: List # ["READ:project:1", "WRITE:scratchpad"]
    local_log: List[str]    # [ "Try 1 failed", "Try 2 success" ]
    return_value: Any       # None until pop()

```

### 2.2 Layer 2: The Tri-Store (The Heap)

**Module:** `noetic.knowledge.store`
**Role:** The "Hard Drive" — Infinite, Structured, Shared.

The Heap is not a single database. It is a **Tri-Store** composed of three specialized distinct memory types.

#### A. Semantic Store (The "What")

- **Structure:** Temporal Knowledge Graph (Zep / Graphiti).
- **Content:** Entities (`User`, `Server`) and Relationships (`OWNED_BY`).
- **Retrieval:** **Community Detection (Leiden).** We retrieve "Cluster Summaries" rather than raw nodes to provide holistic context.

#### B. Episodic Store (The "When")

- **Structure:** Hierarchical Event Log.
- **Content:** The narrative history of the agent's life.
- **Optimization:** **AgentFold.** Raw logs are compressed into "Folded Summaries" (e.g., _"User debugged the auth module for 4 hours"_) during the Sleep Cycle.

#### C. Procedural Store (The "How")

- **Structure:** Vector Database of **Goal Embeddings**.
- **Content:** **Distilled Skills (Memp).** Reusable scripts derived from successful past trajectories.
- **Function:** Solves "Compounding Errors" by allowing agents to execute proven paths without re-reasoning.

### 2.3 Layer 3: The Nexus (The CPU)

**Module:** `noetic.knowledge.nexus`
**Role:** The "Assembler" — Weighting, Budgeting, Shaping.

The Nexus is the interface between the Data and the LLM. It assembles the prompt dynamically based on the **Context Budget**.

**The Relevance Formula ():**

- **S (Semantic):** Vector similarity.
- **T (Temporal):** Time decay ().
- **G (Graph):** Distance in the Knowledge Graph.
- **I (Salience):** Intrinsic importance score (Safety = 1.0, Chit-chat = 0.1).

---

## 3. The Shared Semantic Environment (SSE)

To enable Multi-Agent Systems (Swarm Intelligence), the Heap is **Federated**.

### 3.1 The Ontology (The Dictionary)

**File:** `noetic/knowledge/ontology.py`
We define a strict schema that all agents must respect. This prevents semantic drift (e.g., Agent A using "Client" vs. Agent B using "Customer").

```python
class Project(Entity):
    status: Literal["ACTIVE", "ARCHIVED"]
    owner: User
    deadline: datetime

```

_Constraint:_ The Knowledge Store rejects writes that violate the Ontology.

### 3.2 Graph Scopes (The Window)

Agents do not connect directly to the Database. They connect via a **GraphScope**.

- **Root Agent:** Sees the `GlobalScope`.
- **Child Agent:** Sees a `RestrictedScope` (Mount).

**Mounting Protocol:**
When spawning a child:

```python
scope = parent.knowledge.create_scope(
    mounts=[
        {"id": "project:123", "access": "RW"},  # Read-Write
        {"id": "global_config", "access": "R"}   # Read-Only
    ]
)

```

### 3.3 The "Blackboard" Sync (Pub/Sub)

We implement **Real-Time State Synchronization**.

1. **Write:** Agent A updates `project:123.status = "DONE"`.
2. **Emit:** The Store emits event `GRAPH_UPDATE:project:123`.
3. **React:** Agent B (who has `project:123` in its Scope) receives the signal via `knowledge.nexus.on_update()`.
4. **Interrupt:** If Agent B was planning based on the old status, it triggers a **Cognitive Interrupt** to re-plan.

---

## 4. The API Definition

The public interface for `noetic.knowledge`.

```python
class KnowledgeEngine:
    # --- AgentProg (Stack Operations) ---
    def push_frame(self, goal: str, constraints: List[str]):
        """Creates a new isolated context scope."""
        pass

    def pop_frame(self, result: Any):
        """Destroys scope, garbage collects logs, promotes result to Heap."""
        pass

    # --- Tri-Store (Heap Operations) ---
    async def query(self, natural_language_query: str) -> str:
        """
        Smart Retrieval:
        1. Check Procedural Store for matching Skills.
        2. Check Semantic Store (Graph) for Facts.
        3. Check Episodic Store for History.
        4. Assemble into weighted context string.
        """
        pass

    # --- SSE (Blackboard Operations) ---
    def create_scope(self, mounts: List[Dict]) -> 'KnowledgeEngine':
        """Returns a new Knowledge instance restricted to specific nodes."""
        pass

    def subscribe(self, node_id: str, callback: Callable):
        """Watch a specific node for changes from other agents."""
        pass

    # --- Maintenance ---
    async def run_sleep_cycle(self):
        """
        Offline Optimization:
        1. Distill Skills (Memp).
        2. Fold Episodes (AgentFold).
        3. Prune Graph (Leiden Clustering).
        """
        pass

```

---

## 5. Implementation Roadmap

1. **Phase 1: The Core Stores:** Implement `noetic.knowledge.store` with Graph and Vector backends.
2. **Phase 2: The AgentProg Stack:** Implement `noetic.knowledge.working` with `MemoryFrame` logic.
3. **Phase 3: The Assembler:** Implement `noetic.knowledge.nexus` with the Relevance Formula.
4. **Phase 4: The SSE:** Implement `GraphScope` and the Pub/Sub bus for multi-agent sync.
