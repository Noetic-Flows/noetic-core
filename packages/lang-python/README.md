# Noetic Language (v3.0)

The **Noetic Language** is the portable schema definition for the Noetic Ecosystem. It defines the "Codex"—the static definition of an Agent's intelligence—independent of the runtime engine (Python, Rust, Swift).

## Structure

- **`spec/`**: JSON Schemas (Language Agnostic Source of Truth).
- **`src/`**: Python SDK (`pydantic` models) for `noetic-python`.
- **`stdlib/`**: The Standard Library of reusable Stanzas and Agents.

## Usage

```bash
pip install noetic-lang
```

```python
from noetic_lang.core import StanzaDefinition, AgentDefinition

# Validate a stanza file
stanza = StanzaDefinition.model_validate_json(open("my_stanza.noetic").read())
```