import json
import os
import sys

# Ensure we can import the local package
# Script is in packages/lang-python/scripts/
# Package is in packages/lang-python/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from noetic_lang.core import StanzaDefinition, FlowDefinition, AgentDefinition, IdentityContext, ACL

# Output to packages/spec/schemas/
# ../../spec/schemas
SPEC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../spec/schemas"))
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
    write_schema(IdentityContext, "identity.schema.json")
    write_schema(ACL, "acl.schema.json")
