# Agentic Intent Contract (AIC) Design

The AIC is a cryptographically signed document that accompanies every request as it flows through the Agentic Mesh. It ensures that no matter where a task is executed (local device, cloud server, or external agent), it adheres to the user's constraints.

## Contract Structure

A contract consists of several nested modules:

### 1. Header (Identity & Provenance)
- `request_id`: Unique UUID for the intent flow.
- `user_id`: Encrypted identifier.
- `origin_device`: Hardware ID of the initiating device.
- `timestamp`: Issued at.
- `signature`: Cryptographic proof of origin.

### 2. Capability Scopes (Least Privilege)
Defines exactly what tools the agent is allowed to touch.
- `allowed_integrations`: List of approved n8n nodes or MCP tools.
- `max_compute_budget`: Credits or time limits.
- `data_read_scope`: Folders, databases, or API categories accessible.
- `data_write_scope`: Destinations for output.

### 3. Safety & Security Guardrails
Hard constraints enforced by the mesh middleware.
- `pii_filter`: (Boolean) Enable/Disable PII detection.
- `redacted_entities`: Custom list of strings or patterns to mask.
- `safety_threshold`: Minimum safety score from a guardrail model (e.g., Llama Guard).
- `enterprise_policy_id`: Reference to specialized corporate rules.

### 4. User Preferences
Soft and hard constraints on behavior.
- `tone`: [Concise, Empathetic, Technical, etc.]
- `human_in_the_loop`: [Always, High-Stakes Only, Never]
- `notification_policy`: How to inform the user of progress.

## Enforcement Mechanism

1.  **Creation**: The primary orchestrator (ADK) creates the AIC based on the user's initial prompt and current session state.
2.  **Validation**: Every node in the mesh (n8n worker, sub-agent) must validate the AIC signature before execution.
3.  **Auditing**: Contracts are logged to a tamper-resistant "Intent Ledger" for later review.
4.  **Rotation**: Contracts are short-lived and must be refreshed for long-running workflows.

## Safety Effort Alignment
The AIC implements the "Constraint-Based Agency" model, prioritizing safety by design. By explicitly defining what an agent *cannot* do before it tries to do anything, we mitigate the risks of model hallucinations or misaligned goal pursuit.
