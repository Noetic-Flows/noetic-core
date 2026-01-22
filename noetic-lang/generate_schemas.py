import json
import os
import sys

# Ensure we can import the local package even if not installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from noetic_lang.core import StanzaDefinition, FlowDefinition, AgentDefinition

SPEC_DIR = os.path.join(os.path.dirname(__file__), "spec")
os.makedirs(SPEC_DIR, exist_ok=True)

def write_schema(model, filename):
    schema = model.model_json_schema()
    path = os.path.join(SPEC_DIR, filename)
    with open(path, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"Generated {path}")

if __name__ == "__main__":
    print(f"Generating schemas in {SPEC_DIR}...")
    write_schema(StanzaDefinition, "stanza.schema.json")
    write_schema(FlowDefinition, "flow.schema.json")
    write_schema(AgentDefinition, "agent.schema.json")
