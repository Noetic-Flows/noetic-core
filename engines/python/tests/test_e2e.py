import pytest
import asyncio
import os
from fastapi.testclient import TestClient
from noetic_engine.runtime.engine import NoeticEngine
from noetic_engine.loader import NoeticLoader
# We need to import create_app from main.py
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import create_app

@pytest.fixture
def e2e_setup():
    engine = NoeticEngine()
    # Path to Nexus OS example
    # tests/test_e2e.py -> python/ -> engines/ -> root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    codex_path = os.path.join(base_dir, "noetic-lang/examples/TODO.noetic")
    
    loader = NoeticLoader()
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
