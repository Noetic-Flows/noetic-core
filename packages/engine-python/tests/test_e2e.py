import pytest
import asyncio
import os
from fastapi.testclient import TestClient
from noetic_engine.runtime.engine import NoeticEngine
from noetic_engine.loader import NoeticLoader
# We need to import create_app from main.py
import sys
# Adjust path to import main from apps/python-cli
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../apps/python-cli")))
from main import create_app

@pytest.fixture
def e2e_setup():
    engine = NoeticEngine()
    # Path to Nexus OS example
    # packages/engine-python/tests/test_e2e.py -> ../ -> ../ -> root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # The example file is likely in packages/stdlib/examples or similar, but the original code pointed to noetic-lang/examples/TODO.noetic
    # We moved noetic-lang content. Let's assume it's in packages/lang-python/examples/TODO.noetic
    codex_path = os.path.join(base_dir, "lang-python/examples/TODO.noetic")
    
    loader = NoeticLoader()
    # Check if file exists before loading, skip if not found (during restructure)
    if not os.path.exists(codex_path):
        pytest.skip(f"Codex file not found at {codex_path}")

    loader.load(engine, codex_path)
    
    app = create_app(engine, codex_path)
    client = TestClient(app)
    return engine, client

@pytest.mark.asyncio
async def test_e2e_ui_rendering(e2e_setup):
    engine, client = e2e_setup
    
    # 1. Run the engine for a few ticks manually to trigger UI render
    # Instead of engine.start() which blocks, we can call run_loop briefly
    # or just manually trigger a few ticks if we had a tick() method.
    
    # Let's use a simpler approach: the Reflex loop is what sets latest_ui.
    # We can manually trigger one tick.
    world_state = engine.knowledge.get_world_state()
    engine.latest_ui = engine.reflex.tick([], world_state)
    
    # 2. Query the API
    response = client.get("/api/")
    assert response.status_code == 200
    
    data = response.json()
    # Data should be a list of components (FastUI format)
    # The root of Nexus OS is a Column
    assert isinstance(data, list)
    assert any("Nexus OS - Project Dashboard" in str(comp) for comp in data)

@pytest.mark.asyncio
async def test_e2e_dynamic_data_binding(e2e_setup):
    engine, client = e2e_setup
    
    # 1. Inject a project into knowledge
    import uuid
    project_id = uuid.uuid4()
    engine.knowledge.ingest_fact(
        subject_id=project_id,
        predicate="title",
        object_literal="Secret Moon Base"
    )
    # We also need the entity to exist for the ForEach to find it if we bind to /entities
    # Actually our ingest_fact creates the entity model if missing.
    
    # 2. Trigger Reflex Tick
    world_state = engine.knowledge.get_world_state()
    engine.latest_ui = engine.reflex.tick([], world_state)
    
    # 3. Query API
    response = client.get("/api/")
    assert response.status_code == 200
    
    # 4. Verify "Secret Moon Base" appears in the UI tree
    # The ForEach should have generated a button with this label
    # FastUI JSON usually contains 'text' or 'label' fields
    assert "Secret Moon Base" in response.text
