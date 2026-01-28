# **The Cognitive Nexus Architecture: Unifying Temporal, Procedural, and Value-Based Memory for Autonomous General Intelligence**

## **1. Introduction: The Cognitive Horizon and the Memory Gap**

The advancement of Large Language Models (LLMs) has ushered in a new epoch of artificial intelligence, characterized by models that exhibit unprecedented capabilities in generation, reasoning, and coding. Yet, as we transition from the paradigm of the "chatbot"—a stateless, reactive interlocutor—to that of the "autonomous agent"—a persistent, goal-directed entity—we encounter a fundamental barrier: the memory gap. While models like GPT-4, Claude 3, and Gemini 1.5 have expanded context windows to millions of tokens 1, this quantitative increase has not translated into a qualitative leap in long-term coherence or skill acquisition. The "Context Window Fallacy"—the belief that a larger buffer equates to memory—ignores the computational reality of quadratic attention scaling, the cognitive reality of attention dilution, and the systemic reality of episodic evanescence.

This report presents the **Cognitive Nexus Architecture (CNA)**, a comprehensive design framework for a next-generation AI memory system. The CNA is not merely a storage solution; it is a *cognitive operating system* designed to bridge the chasm between transient activation and permanent wisdom. It achieves this by synthesizing the most advanced mechanisms from the 2024-2025 research landscape, specifically integrating the temporal knowledge graphs of **Zep** 2, the value-based reinforcement learning of **MemRL** 3, the procedural distillation of **Memp** 4, the generative latent spaces of **MemGen** 5, the massive editing capabilities of **CoMEM** 6, the structural consolidation of **EverMemOS** 7, and the personalization hierarchies of **Mem0**.8 Furthermore, it incorporates critical infrastructure insights from **Aeon** 9 and forgetting mechanics from **A-MEM** 10 to create a system that is robust, efficient, and biologically plausible.

The analysis that follows is exhaustive. We dissect the limitations of current architectures, rigorously evaluate the component technologies, and propose a unified, neuro-symbolic architecture that addresses the "Stability-Plasticity Dilemma"—the ability to learn continuously without catastrophic forgetting. The CNA represents a shift from "Retrieval-Augmented Generation" (RAG) to **"Memory-Augmented Cognition" (MAC)**, where memory is an active, evolving participant in the reasoning process.

### **1.1 The Context Window Paradox**

The prevailing trend in LLM development has been the pursuit of infinite context. Models boasting 128k, 1M, or even 10M token windows promise to hold entire libraries in active memory. However, this approach is fundamentally flawed as a solution for agentic memory for three primary reasons:

First, **Computational Insolvency**. The Transformer attention mechanism scales quadratically, ![][image1], with sequence length. While techniques like Ring Attention and FlashAttention mitigate this, the sheer memory bandwidth required to move massive KV caches prevents sub-second latency for real-time agents. An agent that must re-read a year's worth of logs (10M tokens) to answer a simple query like "What is my username?" is operationally non-viable.1

Second, **The "Lost-in-the-Middle" Phenomenon**. Empirical evidence suggests that as context expands, retrieval accuracy for facts located in the middle of the sequence degrades significantly. This "attention dilution" creates a fuzzy, unreliable memory where facts are accessible only if they are recent or prime.11

Third, **Episodic Evanescence**. Context is transient. It exists only for the duration of the session. True agency requires *cross-session persistence*—the ability to wake up on Day 100 with the accumulated wisdom of Days 1-99 intact, structured, and instantly accessible.

### **1.2 The Shift to Neuro-Symbolic Memory**

To overcome these limitations, we must look to architectures that decouple memory from the model's weights and context window. The solution lies in **Neuro-Symbolic** systems. "Neuro" refers to the use of embeddings and latent representations (as seen in MemGen and Vector RAG) which capture semantic nuance. "Symbolic" refers to structured, graph-based representations (as seen in Zep and Graphiti) which capture explicit relationships and logic.

The CNA fuses these approaches. It acknowledges that human memory is not a single store but a complex system of interacting faculties: sensory buffers, working memory, semantic knowledge, and procedural skills. By mapping the specialized AI systems of 2025—Zep, MemRL, Memp, etc.—to these biological faculties, we can engineer a system that mimics the resilience and adaptability of biological cognition.

---

## **2. Deconstructing the State-of-the-Art: Component Analysis**

Before synthesizing the CNA, we must rigorously analyze the constituent technologies to understand their specific "superpowers" and the gaps they leave unfilled.

### **2.1 Zep and Graphiti: The Semantic Backbone**

**Zep** addresses the primary failure mode of Vector RAG: the loss of structure and time. In a standard vector store, the sentences "John lives in NY" (from 2020\) and "John lives in London" (from 2024\) are semantically similar. A query "Where does John live?" might retrieve both, causing hallucination.

**Core Innovation: The Temporal Knowledge Graph** Zep's engine, **Graphiti**, moves beyond static vectors to dynamic graphs. It extracts entities (Nodes) and relationships (Edges) but adds a critical dimension: *validity time*. An edge is not just (User)--\>(NY); it is (User)--\>(NY). This allows for **Deep Memory Retrieval (DMR)**, enabling the system to reason about the *state of the world at a specific time*.2

* **Benchmark Dominance:** Zep outperforms MemGPT on the DMR benchmark (94.8% vs 93.4%) and shows massive gains (up to 18.5%) on LongMemEval.13  
* **Architectural Role:** Zep provides the **Semantic Truth** of the CNA. It is the "ledger" of facts that prevents the agent from drifting into inconsistency.

### **2.2 MemRL: The Value-Based Controller**

**MemRL** 3 introduces a paradigm shift from "Similarity-Based Retrieval" to "Utility-Based Retrieval." Standard RAG assumes that the most *similar* document is the most *relevant*. MemRL challenges this.

**Core Innovation: The Q-Value of Memory**

In problem-solving scenarios, the most useful memory might be semantically distant. If an agent is stuck on a Python KeyError, a generic Python tutorial (high similarity) might be less useful than a C++ memory about "hash map collision handling" (low similarity but high conceptual utility). MemRL uses Reinforcement Learning to learn this.

* **The Triplet:** Memories are stored as ![][image2].  
* **The Update Rule:** ![][image3].  
* **Architectural Role:** MemRL provides the **Wisdom** of the CNA. It allows the system to optimize its own retrieval policy based on environmental feedback, filtering out "distractor" memories that confuse standard RAG.

### **2.3 Memp: The Procedural Engine**

While Zep handles facts and MemRL handles utility, **Memp** 4 focuses on **Procedural Memory**—the knowledge of "how."

* **Core Innovation: Trajectory Distillation.** Memp records successful agent workflows (e.g., "Search Web \-\> Filter Results \-\> Summarize"). It then *generalizes* these into abstract scripts, replacing specific variables with placeholders.  
* **Architectural Role:** Memp provides the **Skill** of the CNA. It prevents the agent from having to re-derive the logic for common tasks, significantly reducing token usage and logic errors.

### **2.4 MemGen: The Latent Weaver**

**MemGen** 5 operates at a sub-symbolic level. It argues that converting thought back into text (decoding) is lossy.

* **Core Innovation: Latent Tokens.** MemGen uses a "Memory Weaver" to compress contexts into dense vector sequences (Latent Tokens) that are injected directly into the LLM's attention layers. This is akin to "telepathy" between the memory and the model—transferring the *state* rather than the *words*.  
* **Architectural Role:** MemGen provides the **Intuition** of the CNA. It allows for high-bandwidth context transfer that captures tone and nuance better than text.

### **2.5 EverMemOS and HiMem: Structural Organization**

**EverMemOS** 7 and **HiMem** 14 solve the problem of *segmentation*. A continuous stream of interaction is noisy.

* **EverMemOS:** Introduces the **MemCell** (atomic unit of episode \+ facts) and **MemScene** (clusters of cells).  
* **HiMem:** Introduces **Event-Surprise Segmentation**. It cuts the stream when the topic shifts (cosine distance) or when "surprise" (perplexity) spikes.  
* **Architectural Role:** These provide the **Ingestion Pipeline**, organizing raw chaos into structured archives.

### **2.6 CoMEM and A-MEM: Maintenance and Hygiene**

**CoMEM** 6 enables **Mass Editing**—fixing thousands of wrong facts instantly without retraining. **A-MEM** 10 introduces **Forgetting Curves** (Ebbinghaus), ensuring the memory doesn't become a digital hoard of useless trivia.

---

## **3. The Cognitive Nexus Architecture (CNA): System Design**

The CNA is designed as a biological biomimetic system, composed of five distinct but interconnected subsystems. Unlike monolithic vector stores, the CNA functions as a metabolic cycle of information.

### **3.1 Subsystem 1: The Sensory Ingestion Layer (The Thalamus)**

The Ingestion Layer is the gateway for all data. It is designed for ultra-low latency and high-throughput segmentation. It does not "store" long-term data; it buffers and segments it.

**3.1.1 The Zero-Copy Ring Buffer** Inspired by **Aeon** 9, the entry point is a memory-mapped Ring Buffer implemented in C++. This buffer accepts raw tokens from the LLM and User. Using a **Zero-Copy Bridge** (via NanoBind), the Python logic can read this buffer without serialization overhead, ensuring sub-millisecond access times.

**3.1.2 Dual-Channel Segmentation (HiMem Logic)** As data flows through the buffer, two lightweight monitor models (running on CPU or a small GPU slice) analyze it in real-time 14:

* **Channel A (Semantic Shift):** A sliding window embedding model calculates the cosine similarity between the current window and the active "Event Centroid." If similarity drops below ![][image4], an **Event Boundary** is flagged.  
* **Channel B (Surprise Monitor):** A small language model measures the perplexity (PPL) of incoming tokens. A spike in PPL (indicating a user correction, error, or sudden context switch) triggers a **Surprise Boundary**.

**3.1.3 The Raw Episode Object**

When a boundary is triggered, the buffer flushes the accumulated tokens into a **Raw Episode Object**. This object is tagged with:

* *Timestamp (Start/End)*  
* *Trigger Type (Topic vs. Surprise)*  
* *Source ID (User/System)*  
* *Latent State (The final KV-Cache state from the LLM)*

### **3.2 Subsystem 2: The Working Memory Workspace (The Prefrontal Cortex)**

The Working Memory (WM) is the agent's "active consciousness." It manages the immediate context window sent to the LLM.

**3.2.1 The Latent Scratchpad (MemGen Integration)** Standard agents paste retrieved text into the prompt. The CNA uses **MemGen's Memory Weaver**.5

* When a new turn begins, the WM retrieves relevant **Latent Tokens** from the previous turn (stored in the Raw Episode).  
* These tokens are injected into the LLM's residual stream via a LoRA adapter.  
* **Benefit:** This restores the model's "mental state" (mood, reasoning depth, immediate constraints) without consuming context tokens.

**3.2.2 The Attention Executive**

The WM also manages the "Attention Budget." It decides which retrieved facts (from Long-Term Memory) are promoted to the System Prompt (explicit instruction) and which are relegated to the Context Window (background info). This prioritization is driven by **MemRL's utility scores**—only high-utility memories get "System Prompt" privileges.

### **3.3 Subsystem 3: The Consolidation Engine (The Hippocampus)**

This is the asynchronous processing core. While the agent interacts with the user, the Consolidation Engine runs in the background (the "Dreaming" phase), transforming Raw Episodes into structured long-term memories.

**3.3.1 The MemCell Factory (EverMemOS)** The engine takes a Raw Episode and passes it through an extraction pipeline 7:

1. **Summarization:** "User asked about Python; System provided code."  
2. **Foresight Extraction:** "User implies they will deploy this code tomorrow." (This creates a "Future Trigger").  
3. **Atomic Fact Extraction:** Extracts (Entity, Relation, Entity) triplets.

**3.3.2 The Graphiti Synthesis (Zep)** The extracted facts are reconciled with the **Temporal Knowledge Graph** 2:

* **Entity Resolution:** "He" is resolved to node:User\_001.  
* **Temporal Logic:** If the new fact says "User is in London" but the Graph says "User is in NY (since 2024)," the system updates the NY edge to valid\_end: \<today\> and creates the London edge with valid\_start: \<today\>.  
* **Conflict Detection:** If the contradiction is fundamental (e.g., "User is a vegetarian" vs "User ate steak"), the system flags it for the **CoMEM Mass-Editor**.

**3.3.3 The Trajectory Miner (Memp)** If the episode contained a successful problem-solving sequence (indicated by a positive outcome), **Memp** engages 4:

* It traces the chain of thought.  
* It generalizes the steps into a script (e.g., Template: API\_Debug\_Sequence).  
* This script is stored in the Procedural Memory.

**3.3.4 The Forgetting Filter (A-MEM)** Not all memories are kept. The engine applies an **Ebbinghaus Decay Function**.10

* ![][image5] where ![][image6] is the "Significance" score (derived from MemRL utility).  
* Memories with low strength are pruned or moved to "Cold Storage" (S3), keeping the active index lean.

### **3.4 Subsystem 4: The Neocortical Storage Hierarchy**

The CNA utilizes a **Polyglot Persistence** strategy, using specialized datastores for different memory types.

| Storage Tier  | Technology             | Content Type                    | Retrieval Method                |
| :------------ | :--------------------- | :------------------------------ | :------------------------------ |
| **Hot (L1)**  | **Aeon Atlas (RAM)**   | Working Memory, Active Indices  | Pointer-based, Latent Injection |
| **Warm (L2)** | **Neo4j / FalkorDB**   | Zep Knowledge Graph             | Cypher, Vector Similarity       |
| **Warm (L2)** | **Vector DB (Milvus)** | Memp Scripts, Episode Summaries | Dense Retrieval (HNSW)          |
| **Cold (L3)** | **Object Store (S3)**  | Archived Episodes, Full Logs    | ID-based, Batch Retrieval       |

**3.4.1 The Atlas Index (Aeon)** For the highest speed, the embedding index is hosted in **Atlas**, Aeon's memory-mapped B+ Tree.9 This allows SIMD-accelerated similarity search directly on the raw memory pages, bypassing the latency of standard HTTP-based Vector DBs.

### **3.5 Subsystem 5: The Metacognitive Controller (The Frontal Lobe)**

The Controller is the decision-making unit that governs *retrieval*. It answers the question: "Given query ![][image7], what should I remember?"

**3.5.1 The Q-Value Retrieval Algorithm (MemRL)**

Standard systems retrieve based on ![][image8]. The CNA retrieves based on **Expected Utility** ![][image9].

The scoring function for a memory candidate ![][image10] is:

![][image11]

* **Sim:** Semantic similarity (from Atlas).  
* **Q:** The learned utility score from **MemRL**.  
* **Recency:** Decay factor from **A-MEM**.  
* **GraphCentrality:** Importance score from **Zep**.

**3.5.2 The Feedback Loop**

After the agent generates a response, the user's reaction (explicit feedback or implicit sentiment) acts as a Reward signal (![][image12]).

* The system performs a **Temporal Difference (TD)** update on the Q-values of the memories *that were retrieved*.  
* ![][image13].  
* This allows the system to learn: "When asked about SQL optimization, that specific obscure blog post (memory ![][image10]) is highly useful," boosting its Q-value for future queries even if semantic similarity is imperfect.

**3.5.3 The Mass-Editing Verifier (CoMEM)**

Before outputting, the Controller runs a **Fact Check**.

* It extracts claims from the generated response.  
* It checks them against the **Immutable Facts** in the Zep Graph.  
* If a contradiction is found (e.g., "User is in NY" when Graph says "London"), the **CoMEM** module intercepts. It constructs a "correction prompt" using IKE (In-Context Knowledge Editing) demonstrations and forces a regeneration.

---

## **4\. Implementation Strategy: Engineering the Nexus**

Building the CNA requires navigating complex systems engineering challenges. The integration of Python-based LLM logic with C++ based high-performance indexing is non-trivial.

### **4.1 The "Zero-Copy" Bridge Architecture**

To satisfy the latency requirements of real-time interaction (sub-50ms retrieval), the CNA cannot rely on REST APIs for internal communication. We propose a **Shared Memory Architecture** inspired by Aeon.9

* **The Core (C++):** The Atlas Index, the Ring Buffer, and the Q-Value Table reside in a shared memory segment managed by a C++ daemon.  
* **The Shell (Python):** The LLM logic runs in Python. It uses **NanoBind** to map the shared memory segment into its own address space as NumPy arrays.  
* **Benefit:** This eliminates the serialization/deserialization (SERDES) overhead. The Python controller can calculate cosine similarities or update Q-values for millions of items in microseconds using vectorized CPU instructions (AVX-512).

### **4.2 Data Structures: The Holo-Node**

We define a unified data schema, the **Holo-Node**, which encapsulates the multi-modal nature of memory in the CNA.

```json
{  
  "uuid": "550e8400-e29b-...",  
  "type": "MemCell",  
  "content\_text": "User successfully deployed the container.",  
  "content\_latent": "\<binary\_blob\_pointer\>", // Pointer to MemGen latent vector  
  "embedding": \[0.012, \-0.93,...\], // 1536-dim vector  
  "temporal\_metadata": {  
    "created\_at": "2025-10-27T10:00:00Z",  
    "valid\_start": "2025-10-27T10:00:00Z",  
    "valid\_end": null  
  },  
  "graph\_links":,  
  "memrl\_stats": {  
    "q\_value": 0.85,  
    "access\_count": 14,  
    "last\_accessed": "2025-11-01T08:30:00Z"  
  }  
}
```

This structure allows any module (Zep, MemRL, Memp) to access the facets of the memory it needs without redundant storage.

### **4.3 Scalability and Graph Partitioning**

As the Temporal Knowledge Graph grows, traversal becomes expensive. We employ **Community Detection Algorithms** (e.g., Leiden or Louvain) to partition the graph into "Memory Shards" (e.g., "Work Persona", "Gaming Persona").

* **Routing:** The Controller predicts the relevant shard based on the query intent.  
* **Benefit:** Retrieval scope is limited to the relevant shard, keeping latency logarithmic ![][image14] rather than linear.

---

## **5. Theoretical Evaluation and Performance Projections**

Based on the reported metrics of the constituent systems, we can project the performance of the integrated CNA.

### **5.1 Deep Memory Retrieval (DMR)**

**Baseline (MemGPT):** 93.4% Accuracy.

**Zep Standalone:** 94.8% Accuracy.

**CNA Projection:** **\>98% Accuracy.**

* *Reasoning:* Zep's graph structure provides the 94.8% baseline. The addition of **MemRL** allows the system to filter out "distractor nodes" (nodes that are semantically similar but factually irrelevant) based on past utility. The **CoMEM** verifier adds a final safety layer against hallucination.

### **5.2 Procedural Success Rate (ALFWorld Benchmark)**

**Baseline (ReAct):** \~50-60% Success.

**Memp Standalone:** \~70-80% Success.

**CNA Projection:** **\~85-90% Success.**

* *Reasoning:* Memp provides the scripts. **MemGen** adds the latent "mindset" required to execute them faithfully. The **HiMem** segmentation ensures that the "context" for the task is clean and unpolluted by irrelevant previous conversations.

### **5.3 Latency Budget**

**Standard RAG:** \~200-500ms (Embedding \+ Vector DB HTTP Call \+ Reranking).

**CNA (Aeon Core):** **\~20-50ms.**

* *Reasoning:* The Zero-Copy bridge removes the HTTP and JSON overhead. The Atlas Index (memory-mapped) is orders of magnitude faster than a remote Vector DB.

---

## **6\. Second and Third-Order Insights**

### **6.1 The Emergence of "Intuition"**

By combining **MemGen** (Latent Memory) and **MemRL** (Value-Based Retrieval), the CNA creates a computational analogue to intuition. Intuition in humans is often described as "knowing without knowing why"—a rapid, pattern-matched retrieval of a solution strategy without explicit reasoning.

In CNA, when a query arrives, MemRL might assign a high Q-value to a memory cluster based on subtle, non-semantic features (e.g., the *structure* of the user's error message). Simultaneously, MemGen injects the latent state associated with that cluster. The model "feels" the solution path before it generates a single token. This suggests that CNA agents will exhibit "expert" characteristics—skipping intermediate reasoning steps that novices (standard LLMs) require.

### **6.2 The Self-Healing Knowledge Base**

The combination of **Zep's Temporal Graph** and **CoMEM's Mass Editing** solves the problem of "Knowledge Drift." In standard systems, old data pollutes the store. In CNA, the *conflict* between old and new data is explicit. The system can be configured to run "Nightly Reconciliation Jobs" where the LLM reviews temporal conflicts in the graph and decides whether to "forget" (decay) the old fact or "archive" it. This makes the knowledge base self-cleaning and anti-fragile.

### **6.3 The Privacy Paradox of Perfect Memory**

The CNA's ability to perfectly track temporal states and procedural habits creates profound privacy implications. An agent using CNA knows not just *what* the user said, but *when*, in *what context*, and *how* that relates to every other interaction. This "Panopticon of Self" requires strict governance. The **A-MEM** forgetting curve is not just an optimization; it is a privacy feature. We can tune the decay parameters ![][image15] to ensure that granular details of user behavior fade over time, preserving only high-level preferences—a "Right to be Forgotten" implemented at the algorithmic level.

---

## **7\. Future Directions: Toward the Neuro-Symbolic Singularity**

The Cognitive Nexus Architecture represents the convergence of previously distinct AI sub-fields: Knowledge Representation (Zep), Reinforcement Learning (MemRL), and Generative AI (MemGen).

### **7.1 Neuro-Symbolic Compression**

A key area for future research is **Graph-to-Latent Compression**. Currently, Zep stores graphs and MemGen stores latents. A future iteration of CNA could train a specialized "Graph Encoder" that compresses a Zep subgraph directly into a MemGen latent token. This would allow the agent to "load" complex knowledge structures (e.g., the entire organizational chart of a company) into its working memory as a single token, bypassing context limits entirely.

### **7.2 Hardware-Native Memory**

The reliance on Aeon's Atlas suggests a move toward hardware-software co-design. Future AI accelerators (NPUs) should include dedicated "Memory Fabric" optimized for B+ Tree traversal and Graph Pointer chasing, moving the CNA logic from software (C++) to silicon.

### **7.3 Conclusion**

The barrier to AGI is not just reasoning; it is continuity. Without memory, intelligence is a fleeting spark. The **Cognitive Nexus Architecture** provides the fuel to turn that spark into a sustained flame. By rigorously organizing time, value, procedure, and state, it grants AI agents the most human of capabilities: a life history, a learning curve, and a sense of self.

---

# **Appendix: Comparative Summary of Integrated Systems**

| System        | Core Contribution to CNA        | Key Mechanism               | CNA Subsystem                  |
| :------------ | :------------------------------ | :-------------------------- | :----------------------------- |
| **Zep**       | Temporal Structure & Factuality | Temporal Knowledge Graph    | **Consolidation & Storage**    |
| **MemRL**     | Utility & Policy Optimization   | Q-Value RL Update           | **Metacognitive Controller**   |
| **Memp**      | Procedural Skill Acquisition    | Trajectory Distillation     | **Consolidation & Storage**    |
| **MemGen**    | Latent Context & Intuition      | Latent Token Injection      | **Working Memory**             |
| **EverMemOS** | Episodic Organization           | MemCell / MemScene          | **Consolidation**              |
| **HiMem**     | Event Segmentation              | Event-Surprise Dual Channel | **Ingestion**                  |
| **CoMEM**     | Error Correction                | Mass-Editing / IKE          | **Controller (Verification)**  |
| **Aeon**      | Low-Latency Infrastructure      | Zero-Copy / Atlas Index     | **Infrastructure / Ingestion** |
| **A-MEM**     | Forgetting Mechanics            | Ebbinghaus Decay            | **Consolidation**              |
| **Mem0**      | User Personalization            | User/Session Hierarchy      | **Storage Hierarchy**          |

This architecture, defined by the seamless integration of these technologies, stands as the robust, scalable, and cognitive solution to the memory crisis in modern AI.

---

#### **Works cited**

1. LLM context windows: what they are & how they work \- Redis, accessed January 26, 2026, [https://redis.io/blog/llm-context-windows/](https://redis.io/blog/llm-context-windows/)  
2. Zep: A Temporal Knowledge Graph Architecture for Agent Memory, accessed January 26, 2026, [https://arxiv.org/html/2501.13956](https://arxiv.org/html/2501.13956)  
3. MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory (Jan 2026\) \- YouTube, accessed January 26, 2026, [https://www.youtube.com/watch?v=M5uy61yPYOY](https://www.youtube.com/watch?v=M5uy61yPYOY)  
4. \[Quick Review\] Memp: Exploring Agent Procedural Memory \- Liner, accessed January 26, 2026, [https://liner.com/review/memp-exploring-agent-procedural-memory](https://liner.com/review/memp-exploring-agent-procedural-memory)  
5. MemGen: Generative Latent Memory for LLMs \- Emergent Mind, accessed January 26, 2026, [https://www.emergentmind.com/topics/memgen-framework](https://www.emergentmind.com/topics/memgen-framework)  
6. COMEM: In-Context Retrieval-Augmented Mass ... \- ACL Anthology, accessed January 26, 2026, [https://aclanthology.org/2024.findings-naacl.151.pdf](https://aclanthology.org/2024.findings-naacl.151.pdf)  
7. \[Literature Review\] EverMemOS: A Self-Organizing Memory ..., accessed January 26, 2026, [https://www.themoonlight.io/en/review/evermemos-a-self-organizing-memory-operating-system-for-structured-long-horizon-reasoning](https://www.themoonlight.io/en/review/evermemos-a-self-organizing-memory-operating-system-for-structured-long-horizon-reasoning)  
8. mem0ai/mem0: Universal memory layer for AI Agents \- GitHub, accessed January 26, 2026, [https://github.com/mem0ai/mem0](https://github.com/mem0ai/mem0)  
9. Aeon: High-Performance Neuro-Symbolic Memory Management for Long-Horizon LLM Agents \- arXiv, accessed January 26, 2026, [https://arxiv.org/html/2601.15311v1](https://arxiv.org/html/2601.15311v1)  
10. A-Mem: Agentic Memory for LLM Agents \- arXiv, accessed January 26, 2026, [https://arxiv.org/html/2502.12110v1](https://arxiv.org/html/2502.12110v1)  
11. Cognitive Workspace: Active Memory Management for LLMs An Empirical Study of Functional Infinite Context \- arXiv, accessed January 26, 2026, [https://arxiv.org/html/2508.13171v1](https://arxiv.org/html/2508.13171v1)  
12. zep:atemporal knowledge graph architecture for agent memory \- arXiv, accessed January 26, 2026, [https://arxiv.org/pdf/2501.13956](https://arxiv.org/pdf/2501.13956)  
13. Zep AI Introduces a Smarter Memory Layer for AI Agents Outperforming the MemGPT in the Deep Memory Retrieval (DMR) Benchmark \- MarkTechPost, accessed January 26, 2026, [https://www.marktechpost.com/2025/02/04/zep-ai-introduces-a-smarter-memory-layer-for-ai-agents-outperforming-the-memgpt-in-the-deep-memory-retrieval-dmr-benchmark/](https://www.marktechpost.com/2025/02/04/zep-ai-introduces-a-smarter-memory-layer-for-ai-agents-outperforming-the-memgpt-in-the-deep-memory-retrieval-dmr-benchmark/)  
14. HiMem: Hierarchical Long-Term Memory for LLM Long-Horizon Agents \- arXiv, accessed January 26, 2026, [https://arxiv.org/html/2601.06377v1](https://arxiv.org/html/2601.06377v1)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAYCAYAAAC4CK7hAAAC00lEQVR4Xu2WW6gNYRiGX+djIkQR25kihSIXIodSitxwQUnZFCVRJIedkuKCwoVQO3HhghSFkjYuXJBTIqLIhQulnJKz993fDP/+1sxas9Y03Kynnlrzff/MrPkP3/8DdeqUowudSNv5xP+ggQ7ywYwcokfoc7rM5QbSUS5WkRX0Mb1Nt9C99BN9QCf8bdaGXvQeneoTGRlNZ0a/J9NfdPGfrDGePnOxVEbQO3Suiw+jN+gHOsnlxGl60AdrZDn9Svv4BNnlA0mMo69hvZvEbFhPXXNxDfk3WCfkpTN9Qjf7RMQAOscHQ7rRp/SHTwToJR9hHzM8iGskrgTXeWim633QcdkHQvbB/uBJn3Dch7WbH8Te0R3Bda1o2iyNfmt2TAlyIZ9pVx8UY2AjUWl6dIA9RB+yKIqpmuha087Tg56ix2D3rqKX6F16HlZqQw7AOmgBPYrktSj0vsTppcqkpKpOOdRLaifjUjg9ulYx8GykjbD8reha01M8omej30K9Hz87tmeQD1FunQ8KVSMlT/iEQ9VE7VSK1cNC9V6x3nGjAJVv/XHld7vcdfrGxbKi2dPkg+IF7GXxdEliFqyN1kO/IL4ziscf5ulIW1xsHuyeTS6elfd0jw+KC7AHb/WJCB0ZrtKfdKXLrYXdG35ciDbIJhdrhvXqYNizVTGrQe/TeithDSx50SdIe9hi/Q6bWp4lsHvTjg/aD2YE1xohjWq8F21DaedUQu9LKi6tvdIC203Dh3aH9d4XlB4XYnS00IMX+kSEOide4GIkrP122hdWYHRYrAbdn1RcWtFxQD2v6bOBnoP1nAqAqlU5XsL2oSRe+QCsBOvc9hB2rqqWt7CRLUsDXQ0buv5tU6kchlWoJLQOkhiC6tdGjA6xhTAUNv2m+UQBjIW9rzD20zM+WADHfaAItM60uaZVsDxoFG4i+3TPjSpQ2uaYh06ofU3V+ef8BvSnixq4/p9aAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPcAAAAZCAYAAADtwrihAAALtklEQVR4Xu2bB5ClRRHH/yaMmFARBW9VVBADBowgCAhSIiYMGEEQMWBpmbX0FgoQocpYRsIBgmBCzBFdFEkKapktRVREtAyYc5jf9XS93n5feG/f3nm3fr+qrts384WZnp4O895JAwMDAwMDAwMDAwMbKA/IDQMDA/9TrlnkfrlxKTwvNwwMDIxx9SKbFZlL7euKdxc5KDdOwyG5oXKjIr8q8usivyzy8yK/KLJ3vGgFc/ciP55QXl7v2RhYVeQauXEj42oyvUe7vLLIDuGahdr+0yKXF9kp9PWxaZGnF7lFaHtmkX8W+Y/snRn0eqCWV7c3KPKNInvljkk4rcgJuTHBgJnQWbljCdxZ9qzX5I51wLNl79ozd0zJKUWenxsDXy/y2Ny4AYPRrhSeUeTM3Bhg7c/OjZUu+9hR5rCvm9ofIbvnOakd0OuTc6PM5me1d2xsPjd2casify9y/9yROFU2oefmjiVA+s+zHpo71gEs+j9k3m8W8Px3TW3XDn9/UIsjxsD6A9tkk7ZxVJFX5MbKUuzjDTL7ZcNOCjY/q70fWuSqItfKHW28sMif1X8DKQ0T2jZ3LIEPFPlbkevnjgRp1yxwPyXFl3LHlGwtm3scD+ndceHzp2R12HLQN+++/uVgud/R97y+/i6wzS67PE/Nh1JLtQ8iKOn/NGDzffbex/YyOySjmIh3FjknNybuKHto04ReJqs9eMbNZEb/8SLnVnHuVeSiIl+ROROyhYuLXFhkk3DdbrLU/2tFzi+yRnZiCCiHdzFmahrOCT5Zr/1wke3qdXBwbWfcv5G96/jQPw2kfTzHuY4szXtKaIvGeZMiJxb5lmwMpOs7F/miTE/PGl269jnfLHIfmY6Y+3eLnKTFzoJDHOb0uSJfluntBaH/9kU+WuQAmR4wJvR/TLiGTINxfaf2Z25Y5EjZsxHu3732EXW+X+QHsrFuVeS9MqeGsbdFRubOmC+RrQFRz9ezb06TcActXpsMNsN5kb8TeCfv67KPF8mcAs+PsCb/LnJGaMt69UCZbT7bOzbxsdr+qNrmvE/jDg+b/72mSM0/K9tAXaAMlBAnBAz+XbJ0lf6vyp5109pPHe9KpW4hAj5Gdi2LzOfb1H4m8o4i/yry6NoGpLscYgBZBnUO97M41MCuSIzu9Po3MIbXyq7dT/aum4f+aeC0kueQwi0U+Un9vGW4JvKFIvvI5vQkWdp3mWwMnyjyO9lCMXb0guFjgCyop4c4regcMQoOjnC0gIO5osg29TNrwwbnXRy+bCFzEOgzrgc1ISVY3hD3lDlvHNCmtY3DRJwp72JOOG/e+UOZ3dypXoeTw+AzGPylsucAJR3XYdQ3Vv+cJsFts409ZBsogj5Yizb7YD4nFflrkTfWNgfb5B63Sch69Y2abT7aOzpeKHI9mXPD0USwsSYIBHkftoLyX5cbEzwsTwiYFF78vrJ+Bhk95NGyCUXwzFy7a2o/rLaTCTgsNsZGNAc84Etl1x3uF1UukKVnkQ/J0n+UPAsYOO98iOwwhcyEKNbGEeFvIhf3Eq2JjHhwP/x5nMwBEDnYkLE0QndsTDc4Mp0HjbrXGgkOjUhyW1kEBa5bJXMeOAz0B7eWGRDR8sVavCFuKTtRxqDiyTDfiLCpMfaXyJ75B5k+eJ5DVM8bjGyHU2VswyGKMVfeQQbTNadJccfbBodYBIUm2uyDIEVmwnNXp7431/YY0bNedw594DYfwbE8QWbjf5FtdAfHx7yaYD1xrL2wWHj6V+WOBAvP4NzDOngqjJOFp3+nxd1rBxw3O5A+4xGzQv9UBS+HMWHc1EL+9RLKo25iY7FB4mGWKyh76N/KjHMWtpXNLToOvPfbw+fb1TYn1lZkKNxPVIU4byLf3WT9zDdCeuc6ZfOQqfAONs1bZFHvYfVaNgvjxDnEhUcvDqWCHwBRLvwo9PFu3rWmyL6yjIiMbEFmxNyHweHIuS7by3xtd8jkWA+yjwjRysfE9V1zmhQifd44EZw+WUkGe2qzjwfWf8kyWNsITjgHkazXnE67zUd87xDlGf8hoe+RGg+kDs/C+fTC5mYC86k9wsB5+c9yR4BUkw23SWjDmPDMERR6lZprfN5xnuxUkWiHgol0GSLH2akNg+D+Q1M7bWQEs+BlwKmhjWgTv104We0nodSjbSkWMF+ev2dqJ4LRjh6JFryf6E/mcG+NO03gF4Ztta/jG3Q+tGGw3kZ6yVxwFhnPmrITZ5OSXjue7kaDzbhO++bUBY6H51yZOyr8RoPAhN1lKCm77IPgsZDayKLYLzi+TJNeocvmgVKMAEvJ47xJo5InQwDzbKwXUrdcV0T4ioFBn5Y7KizIHzW+4fDG3AfUFcACZoX6BqadDKAPrsuRg7GRAm4uU2aMDg+uf+Mlp/m6w/EIemDuqGxd5Nsa99bAeDAGNr/DdV7TAmcKOMEY7Umzeef59fMZMuPpgyyn6VQ48jbZmHiHv5PNQdbUNIcIkTg7cbI5xooD8nX+dG3ziNYE/ZPMqQucLM8hm2uCuR6eGyscmHXZx+OLPK3+jYMFL7FwgFwf1yzqFf14X7b5GLAIrpy/5M1KXd0GATDaUyffk/1Aow08C4M7OHdUMCb6X5naPyOLsrvLTrfBFbpr/TynUSpNe1MqwuHH9uEz13naBCgS58L74IgiT6x/U0/5RudgK0Y16jtSwiav7tCH8+OdnlZH2KSkdaSxEaI1aSw/ZuDeg0IfJUfUFTUoqWNktWzDk97CsWr25HfR4hqZursr+lESEEU+Xz9TAgGRlzq6CTd+d+KuZ4e5+Jpw6gsn1ramzMvHTH/fnNhAc6OuMTgr4Fwi6w/2kv02gXVogm8WuuwDXbJBcSA4LqB0YNyk6g/X6EcpWa+v1ki30ebntLh03KL2xTMvsgPa2uBEHvuYiNM1WpQMi4Px8TI3tAwHYPTniEE6RLpODbhNbcNIuZYJsCmJ9n6SSurKVysRPDsp4y6hDYcRD568JiZlxCioR9zAqYFgTmYAHlngHNl9R4e2zI6ya3JJgocnlbxMNh7Sv8glsvmx2NyPxwcOoTCaOH5/vnt6HBnRkfk499D4jzQOkB3kYCDgm68LNhPv49SaNNAjtZcGMdIyfjI6MgtwJx4PPOE9sq9neL8HANJ6olisn3kXTtfHzKbsmxOOhdq9bYPC+zW+GdiQrH1X5oBD67IPnB2RlczNx0OQYm2YC+8ltYesVxyH6zbafLR34H3sEzIz4B7OcvJ8HBwRDokAMRGkm6S0MSXZR/blPqkak3EhimVFUzcR/VFE5DCZ5/QoCqtkKSCbmBRvj9BH+kKdSSqK5+ffk2W/oIscnz4DSsMocAQcUDkYHdejbN4dIYXFcRF5M9Tu3IuBomgEXZBC8S+GiVArRa/rMDeMAj3Oy746onT4iMadJM8mc7pIdkLKNwK7xAsqjPVMme4wzNVafGBGecB4+yDy8q5zQxtr93rZAdMamVNG//uFa8g+cGS5FmcDe00ZsyAMHaf1VtmPfRgztbhvoKeqf05EZtYh2kmG7IloeJbs8HKhfia6doFz7rIPoi+62j+07SA7W2DMHs2dqFecsRNtvmkeRPgrZBky475c7Zvbg010EJ0QTTBS0pilsJnGT74dvFUGQ8IQm8BzsSikwF3pchMoMRoGEA23TG0RDC0a+XLBWKi3HWo29/4ZPDHj4BoynBjVI7RvJzP4NrbKDS2g/6Y1w8HjHMnYMhwwNa0n8CzKnAzrSfRsSr9hkjkdqclsk6iPM8rOp4s++8C2M2QobfNp02ubzWPj6Ih/ObvgXgIimV8TnDXhdKcCo+hL6VYapJ1s7KZaen1B9CCaDbRDmroSoXQhCu9fP+8my2RwZk2Q6bDp25x/J6SQeOf/F/bVjP9Hdkao2ShzSIUvTX0DI5byDcfGAFkD51GUb5xbUJb4IVyGrIhvZJqyo4nh+7WBgYH1ByVJPseKUAbgBPgNw0z4ie3AwMCGQ9MZyMDAwMDAwMCK4L9XR9QbrwsNkAAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACYAAAAZCAYAAABdEVzWAAAB8ElEQVR4Xu2V3yufURzHP37MUDaUHxPW3EnckgvuNHJDiaQ0dmdxtclquFUMJSWltVZC+bG48PMCa43/wJZ7lrtxu73ffc7Tc3ZMD9/2/aKeV716Op/zPM85z/l8znlEQkJCQkKiShxshVvwGzyAh+b6Fdb5t8aWEXgGV+EKPDfXZTgPS/1bY0cD/AyTTTsT/vS7b488mGS12+GO1f7fJMIsN3gdFkVT61IJX7jBCBiHc24wCKbzF2xzO8ASfOMGIyAbprrBIOrhb1jixONFN0eFEycpsNBqZ4jucuKWCSf00Gp75ErAZKfhBUywYq/gtuhKfoRNJs4BxuAo7IOz8DmcgvumrxeuwWdGlsgP+Eh8ZuAg3ID5VvwvvsB1Nwh6RAewGRatF48F0cmUiR43RSY+AQdE708X/fCnpq8APhHNyAmsNvFLcLfYX+PB+npttZk6riBf7MGJP4ZdcNOK82ycFH1vB9xz+iKmWHQFuM2bYRVsFF1dD06GqWRtnYrWKmmBuybOj+FqcfJDpv+7uZJaWG61A+HyH8O3sNvEONAn0RSxvt6LFjk3DQf/AN+J1luOPiJp8Ei07phuUgM7RdP9UvTjbwQf4ItdmB53o/B/S/51iPI4euDEWG/eLo4a/LX1u8G7AP8aPNWv3F33nj8s0k8y9EheZQAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,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>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAZCAYAAADqrKTxAAAA8ElEQVR4XmNgGHkgAogNgZgNytcCYnaENCoASS4D4j4gvgHEV4DYD4gfAzEzkjo4OAXEi9HE+IH4JxBXo4mDgTwQ/wfiLHQJIDgOxFbogiAA8gNI0xogZkSTqwViFjQxMFBhgGgC4cNArIkqjRssZUBoBOGrDERqBjlzMwNC4x0gZkJRgQcEAvFnBohGUDRgAKzBCQQLGHBo4gTi5+iCUDAFiF+iC4KAExD/AWI+NHFhIP4IxF1o4mDQxABxwkQgZkUSXwnEBxhwxM9+IM4H4nVA/AmINwFxJxDPA2JRJHUowAGJrQ/EMUCciSQ2CqgGAE8JK/4m+0RxAAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAaCAYAAABozQZiAAABN0lEQVR4Xu2TvSuGURiHb/JVDGIiWSwWkyTZ5A+QxcJCFonFqCxKKaNFkUE2lBQS+QcYfBVGFixKDBau030fHXfniZ2rrt7n/f3u5+095zmPyD85BrEfa31RRAXO4K197uErLllXSAde4jE2JXkXvov+UJZufMEdLHVdYAE/sM8XdfiAd1jvusiA6M0bvlixYtgXCe2iM+e58BGr0sLRKzp3k4azFi6mYYZ50bntNDyxcCgNM1yIzs2lYdioEDakoWNcdGbZF0dWdCZZWHulXccncY+NXxPGlOjNE/Z9RHRdB1iOW/iMbdZ/owxP8QlbcN3yGtzFa9GTV0hY7ya+4RlO4pro5sTHV40ldp2lVfQkjWKP6D+JrEr+2BZyiGO4j9Ou+5GwkcFw5n/9TkeuRF/PZpf/ST4BOgJAkgGOXpwAAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGEAAAAZCAYAAAAhd0APAAAFTElEQVR4Xu2ZZaitVRCGX7s7Ma8tGNiFwhUsDExUVBB/XAMVFLt/2F3YCpcLtmL+sO9RsQsVW+zCbsWe58y3PLPnfHvvb8O5RzfsB144e2Z9tWJm1jrSgAEDBgzogXVNM2Vjn7Cqad5sbMpCpt1N65tmr2xLmBb+t8X4sIfpumysgQ/dzrSXaT3TdK3u/4w1TU+Z5smOblxlGjKda3rW9In8A980rTzSbJiNTNsk21jBCnjJNFd2JB43vWi62HSe6T3Th6atQpte+dz0rek70zemHVrdLSxn+kzelmu4dqfgn2R6QD2s5vuyoeId043ZaJwsn3ljzf6m19R+Rs9tesL0fXZUzCn3fWCaNfmawqCeYfrbdE3yRY6Wt3khOwK7mL7KxjoWMP2ZjRW8xH7ZOA151XRENgZukH/4rtkRYIXQZuvsaAirayX5PaYmX2FB+TvQhsjRjhnUcBB4WW7GBZl9TUtm4zSE99ggGyu2l/sfyo7EFHm7Q7KjAfObXq/+/tL0fvBFrjRdKn9Ot7B8dzbUsYjpL9Nz8llIUpm+pcUIy5juNR2b7OSOJ01vmNY2LW26Ra1t6dwH5QlryLRFZY/8Ypo5G+UT5CP5R2+bfJm75O0IF72yo+mK6u9n5BEix/TN5d9E2PxDHiI7cYzqv2kUl8hfvIiYOjE2MGY0vSxfqr/JZw1QRdG5s5k+Nr0tzzErVH4G+HJ5rC3VAgP0SvV35K1sqKAQ4L1Ifu3yBcxi+lHelpXTKxfKq0O4WX6f5Ufcw994m3xg8DGhusH9ls3GdtAxxK8yEFQHrJLCbvLBApJfSXz7yGcdL8ZMZiAWrXzAvViScXVdVtnJR5Gn0+/CqfL2zPJObKmR96d66RXyQXn3s+T3iSv2NI2ES3wk8G7wTj0VMXTURNOn8ofsHHwryhPS4mqtGlap7GW2svwi2NZKNioKwkuG8FUHg8h9TsiOxEXydvdkR0MoDAoHyO9VCpM15KVwAV+TcpgB6FgkHKX6eHWi/CGUWBlm/cbZaBwnv2bDZGdFxVXAIBKirg62AmGtjpJsD86OAHnjXXm7dZKvKazQAh3Mvc6U35swFPcuv8tL4m7QH5tkY4HO/zobKw6VdxQzPEPyBRJSrKjul8fjmMjIF3eG33C4/OM2k8f3+GHPh78jR8qvOTvY8rFAaXNBsvcCIbdQytSb5O8cCwIqRvYrTWAVcOpQC7OZh+QjCQaHTdodyQ4l5ADJl2MOoON/0ugwQEfnUpFk9oV8AKlGYlxlJtexurwSebT6Tby/3XRO9ZtvIR9dr9GV3VLy53RK6IWYy0jyTESKlMnBDnubTk+2duypDs8+Xt6hxPcSkki2xFVme925BztartlUrZ1XBidvtEioq4XfdBCDxS6cQXjMtFjw09HtjitKcuajShl5vulA+QqksqkLrY/IrzslOwJUPcT+CcnOABAt4uDArepeKhd477YQPg6TH5TRMYws5SVVUrvKglVD0uZMJNbHbOqomFjCEeJohuTG2RCVEPuLSAlTdVAik49+MP0qD03U6tyLA8dCHkRqejpyarIXmNUM4s/yOF8GGAil+As8j+fTlnegmsyRJDOUDRFmc4EK5yD5ZqwbzOC85Fm6JTRFcocUmFl1K40V2HHmyPMUZSOHZew9YoKngqHYyJBAH87GcWAO+QTvKxhcNoSTsqMNDASrp+ikVvcwhCjCXpMJNpaQJ9l8ko/6DnaoHJ9PSPY65jNdKz/jqVsBwEEbG8rxhoO9Tnnofw+1NTmr7lCxH+D/EJz4tq2K+gXiab9CDsp5c8CAAaP4B8lOGigIdloeAAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAZCAYAAACsGgdbAAACQ0lEQVR4Xu2WO2hUURCGx2dMVEyRKmAjmsIH2GinRYwgWAgWKdP4agJipSCIIgoqQkqLQBrFpAloUDBNCgOSSoTYWIiiSXxFEVtR/5+ZA+PknLvZ3WDj/vCx58zsmfvfe8+cXZGWWqpLa8Ex42DINaJUa01MNKPN4B24Ak6HXCNinfdgU0wkrQYvwdtl8MjW0OQzGyftBYvgI1gwXoP1lu+03AfRG5wTrZmMsV7RZNJv8CAGnW6DOzbOmUy6K1rrbEyYroHLMSh1mIyFN7jxILhg4yqTfEqstSsmTE/BgRiUOkzucfM28MLNL4LjNi6Z3C5ah681p3bwFayLCVmGSRb/BFa52FUw4uY+VzJ5StTkaEyYDoEnMWiqaZLFv4BxMAlmRS824L/kVDJ5T3RdqeN54+dj0FTT5H1wE/SBo+CW6MW2+i85lUyyY7luR0yYpsH+GDTVNMljocfNt4BXbs7D+5yb50xyPQ3Oh3jSRvBZygd2pcmdosW9usAJN+dr59NNyplM+3EsxJOOgIcx6FRpkkdLNOnFTuRhv83FciYvidbJ7TnWeC66nUqqNMlmKZlkR/MJToR4zmS/aJ0bIU5dB49jMKhokhfjuRVN8s73gSnLHf47nTXZAd6IHubpp5A3eRLMiK6p0hKT7DBu4p+iJsh344fFf9knX1NUziS1W3RrLIJh0R+DIaltkFpislmVTFLs3l5wBnSHXJX+qclG9f+a/CbasdxzzYp1WG9FTbJrud8ID/5mlWr5PzEtrYj+ANOOiF2+6BMdAAAAAElFTkSuQmCC>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAaCAYAAABRqrc5AAAA/ElEQVR4Xu2RMUtCURTHTw4RWg5q0Bb0FZS+QIurDkqbU1NTi7S6iYMguOjckosO4iguCYJNtTSFuATuggj2u+8e66ifIHo/+PHe+Z9z373cJxIS8hcp4BRf8RKvsY8vmh/hIw7xHdt4HKxUznCAp7jEN3zClPafsYN5rd0mGyxqHXCH93iuTbfziek3sWTqmPi5hsl+qItvXpgsiitTO6ri59yJDnAn+NjLbsQvsHziRN/jJg+KNbZsCBXZ/Uha67L4yx6LP21AVpu320AZ4dzUJfFzGcxhzfTkARfy+0e2fMnuoLv8GfawK+YUDlckbKAk9wOI4JU+Q/4H3+CpLN3eDPy6AAAAAElFTkSuQmCC>

[image11]: <data:image/png;base64,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>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAZCAYAAADuWXTMAAABFElEQVR4XmNgGAUUAU4gfg7EH6D4IxC/AeIXQHwZiCcAsQJMMS5QB8T/gbgYTTwZKj4bTRwF7GKAKDJGE8+Dil9FE4cDFiD+wgBxNjOa3DYGiOYMNHE4MGeAKNiCJAYysBCI/wHxKiBmQpJDAWUMEM3rgDiSAaIJFFj3gDgESR1WAHNaPQPEecuB+A8DERpBfvwExcj+PcAAMUAcSQwDmDJAbN2BJr4EKu6DJo4CYP6tRBO/DRV3RBNHAdsZIIqskMQkoWIgrA8V40VIQ4AAAyR+fwExO5K4AgNCsxYQcwDxCSAWBEkaMEDS71cg/gbFn4F4I0gSCkDJEaR5BhCvAOIcJDmCgBGIjYA4AYgtUaVGAX0AAIVOP49bg9hJAAAAAElFTkSuQmCC>

[image13]: <data:image/png;base64,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>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEwAAAAZCAYAAACb1MhvAAAEfUlEQVR4Xu2YaaxdUxTH/4oWRVND0A8SU80xlQQlCCKoCEFRKT4YwwctHxBDROODCBLEmCuRaJUqUSSoSNMWSWOIeYqZIjEXNa6ftfd7+66ec959dd8rcn/JP+/stfY9Z5+91157nSf16NHjf86epjWj8T/Epqato7FTNjedYDrJtEXwVXGy6ZFgGyP/7Yhg/7fCeN8w7RIdTZxpetu00HSR6QbTL6bFqp+4vUzfmrZJ7V1Nv5r+TBqb7MPBeaav5eP5xvSq2qP+UNNXpk9NH6a/rcI/1fRx0a5lZ9MXpnWiI0Gk8fL3BvvZ8oeuF+xwl4Z/wjLvmabJn8/iR54x7RaNiT1M+0ZjyWj5A4iKOjYy/WH63bR2sq1met10Se4UuEOrZsLGm542rSuPMsbAJGRGmT5Rc6p4MBpKrpfflBdsYqm8H9EIbEXax/T1aOc21U8Y+WLDaByADUzbRWMFpJXL0vV18jG0+rzSfqY5RbsKtvQa0Qg7yKOGPEWir4OXyzlpQrKdktp5AiNVE0ZCfdL0lHwVX5bfp4SJudv0gul50z2ma01PyHfB5P6ulZA2JqbrLeXv93O/++/JJNc1wbj3iUa4WO58LjoCB8r7sS3ZwsCDadflvThh+5t+NJ3Y10M6SP5Clxe21+SHTF7hO03L5HmS6OFQaeJd08ii/bB8HJn5ph2LdhX0Py0agYTYyXacLu/HYDIteS6oo5wwXuBN+akVYdsQOTkJ8xtO6MyRyXZ6Yatje3kklhws/z0LsJbpA3n+bYL+F0Yj/CB3nh8dBaub3pH34+TJcNKgOsoJ2ztdt8oOCSIO35WpzfWMfreOSLamMWbOUfUhxEIdJ4/oWcFXBQt4TTQCtQiDOTw6Cihg6fORfIUyC0zPFu1IOWGnpmu2V+RYue/+1CaK2ZJ5q99i+s60WWo3MVvVJcFZ8vFeJd/WA0GquTQa4VH5YNlyVRDGJN/lpknBR9KmCKwjTxhJ/LB0fV9bD2eq3HdTapO0SfSULBwKTF4n1TfbjAAo81eGvMszSCGUHQNBX2rPFThX7pwbHfIKmVX/Sb4tIrerP4KqIJrwc8Kub/rS9FJbD+dq+RbIXwpEMrUSEzCYb1MOAxJ6HYyloype3pc0sgIUb4QqZcWUwk7RR61CjmPfV0G+4MZ8dEdYZRYB/07Jxvfmb6bjcydjnOkz082FjYh+wHSFPB9dYDpKzZO3sXy8j6k9bZRwGhO5ncC4N4nGDBHQku9bBjdPXrjdKq9j6iC0uXFZJgBVNRU2eYf7fF/4jpZvM05nXvBFeeiXp1b+pIr6XNW59iF5nUXpwW4gfRzS1sNhEcqgaIJnDQgf12eYDpDnnU54S15UDhaeRQnA1otwz63kpzMTSf7ZXV4rvq/6COom+cTuOmzpV0wzo+MfwBbdNtjIgY/Lo5OJHCpYDL6rhxSSNQmdSr4bUAJQfJIDKaipmxaZblTnkb+y8PXSdHB0Db67ODy6ufpEL4uRP8WGGtLEEg3+nwIrzXC92FDByT4c+bFHjwr+AgPhAtUnEQrWAAAAAElFTkSuQmCC>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAaCAYAAACD+r1hAAAAwElEQVR4Xu3QPwtBURzG8R9SopRBUUpKLBaDyWKzeCvegt1ucCeTlBWjNyBhkJQXYFJiksT3dM7hXLPNfepT9z6/8+d2RYL8Z3LoY4MB6v6xP02c0EEYbZyRNnMPNfMsJVwwtAWJ4S56odq0Q0gNMnjg8F76yRpXLJGwpfqUJ8a2cLIQPWu5ZVn0DV23NFnh9l2qjERf62aGvegbUmggaYcF0adt0cMcVWRxxBQTRO0GFfUH8qgg7vQRFJ33IL/PC3wpISbzUvT0AAAAAElFTkSuQmCC>