import pytest
import multiprocessing
import time
import os
import uvicorn
from playwright.sync_api import Page, expect
from noetic_engine.runtime.engine import NoeticEngine
# We need to import create_app from main.py
import sys
# Adjust path to import main from apps/python-cli
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../apps/python-cli")))
from noetic_engine.server import create_app

def run_test_server(port, codex_path):
    print(f"DEBUG: Starting test server on port {port}")
    db_file = f"test_e2e_{port}.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        
    try:
        engine = NoeticEngine(db_url=f"sqlite:///{db_file}")
        from noetic_engine.loader import NoeticLoader
        loader = NoeticLoader()
        loader.load(engine, codex_path)
        
        # We need to manually tick the engine to have initial UI
        world_state = engine.knowledge.get_world_state()
        engine.latest_ui = engine.reflex.tick([], world_state)
        
        app = create_app(engine, codex_path)
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
    except Exception as e:
        print(f"ERROR in test server: {e}")

@pytest.fixture(scope="module")
def server():
    port = 8001
    # tests/test_playwright.py -> ... -> root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Adjusted path to example
    codex_path = os.path.join(base_dir, "lang-python/examples/TODO.noetic")
    
    # Use spawn to avoid issues with open files/sockets
    ctx = multiprocessing.get_context('spawn')
    proc = ctx.Process(target=run_test_server, args=(port, codex_path))
    proc.start()
    
    # Wait for server to be responsive
    import requests
    max_retries = 10
    connected = False
    for i in range(max_retries):
        try:
            requests.get(f"http://127.0.0.1:{port}", timeout=1)
            connected = True
            break
        except:
            time.sleep(1)
    
    if not connected:
        proc.terminate()
        # Skip if server fails to start (likely due to environment issues in restricted CLI)
        # pytest.skip("Test server failed to start")
        raise RuntimeError("Test server failed to start")
        
    yield f"http://127.0.0.1:{port}"
    
    proc.terminate()
    proc.join()

def test_browser_project_selection(server, page: Page):
    # 1. Open the app
    page.goto(server)
    time.sleep(1)
    
    # 2. Wait for initial render
    expect(page.get_by_text("Nexus OS - Project Dashboard")).to_be_visible()
    
    # 3. Check for "Secret Moon Base" button in sidebar
    moon_base_btn = page.get_by_role("button", name="Secret Moon Base")
    expect(moon_base_btn).to_be_visible()
    
    # 4. Click the button
    moon_base_btn.click()
    
    # 5. Verify the content area updates
    # Give the engine a moment to process the event and for FastUI to reload
    time.sleep(1)
    
    expect(page.get_by_text("Viewing details for: Secret Moon Base")).to_be_visible()

def test_browser_crisis_protocol(server, page: Page):
    page.goto(server)
    
    crisis_btn = page.get_by_role("button", name="Trigger Crisis Protocol")
    expect(crisis_btn).to_be_visible()
    
    # Click should trigger event, we check if we are still on the page
    crisis_btn.click()
    
    # Should stay on the dashboard (after redirect)
    expect(page.get_by_text("Nexus OS - Project Dashboard")).to_be_visible()
