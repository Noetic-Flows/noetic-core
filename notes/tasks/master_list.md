# Master Task List

## Vision
To build **Noetic**, a "Software 3.0" operating system where users define intents ("Flows") and AI Agents orchestrate the execution using a rigorous architecture of Stanzas, Memory (Stack/Heap), and Safety (Conscience).

## Phase 1: The Core Engine (Current Focus)
- [/] **Federated Monorepo Setup**
    - [x] Structure (`packages/`, `apps/`)
    - [x] Core dependencies (`engine-python`, `lang-python`)
- [/] **Noetic Engine (`packages/engine-python`)**
    - [x] Runtime Loop
    - [x] FastUI Integration
    - [/] **Agent Server Protocol (ASP)**
        - [x] WebSocket Endpoint (`/ws/asp`)
        - [ ] Message Validation & Error Handling
        - [ ] Connection Heartbeats
- [/] **The Clients**
    - [x] Python CLI (`apps/python-cli`)
    - [/] **Web Hub (`apps/web-hub`)**
        - [x] Next.js Scaffold
        - [ ] ASP Client Implementation
        - [ ] Reflex/FastUI Rendering Component

## Phase 2: Cognition & Memory
- [ ] **Knowledge Graph Integration**
    - [ ] Implement `knowledge-python`
    - [ ] AgentProg Memory Stack (Working Memory)
    - [ ] Long-Term Store (Vector/Graph)
- [ ] **Cognitive Control**
    - [ ] Planner/Evaluator Loop
    - [ ] Metacognition Interrupts

## Phase 3: Safety & Interface
- [ ] **Conscience Module**
    - [ ] Principle Evaluation Engine
    - [ ] Cost Simulation
- [ ] **Noetic Stage**
    - [ ] Generative UI Protocol
    - [ ] Voice/Avatar Integration

## Phase 4: Ecosystem
- [ ] **Standard Library (`stdlib`)**
    - [ ] Research Stanza
    - [ ] Coding Stanza
- [ ] **Marketplace**
    - [ ] `.noetic` Codex Export/Import
