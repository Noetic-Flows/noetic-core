import pytest
from fastapi.testclient import TestClient
from noetic_engine.server import create_app
from noetic_engine.runtime.engine import NoeticEngine

@pytest.fixture
def test_client_ws():
    # Setup Mock Engine
    engine = NoeticEngine(db_url="sqlite:///:memory:")
    # We don't need to load a full codex, just the app + engine
    app = create_app(engine, codex_path="") 
    client = TestClient(app)
    return client

def test_websocket_connection(test_client_ws):
    with test_client_ws.websocket_connect("/ws/asp") as websocket:
        # 1. Send Connection Payload
        connect_msg = {
            "type": "CONNECT",
            "client_id": "test_client",
            "version": "1.0"
        }
        websocket.send_json(connect_msg)
        
        # 2. Expect ACK
        ack = websocket.receive_json()
        assert ack["type"] == "ACK"
        assert ack["status"] == "CONNECTED"

def test_intent_lifecycle(test_client_ws):
    with test_client_ws.websocket_connect("/ws/asp") as websocket:
        # Handshake
        websocket.send_json({"type": "CONNECT", "client_id": "test", "version": "1.0"})
        websocket.receive_json() # ACK
        
        # Send Intent
        intent_msg = {
            "type": "INTENT",
            "payload": {
                "text": "Hello World"
            }
        }
        websocket.send_json(intent_msg)
        
        # Expect Update (Engine should echo or process)
        # Detailed assertion depends on implementation, but we check we get *something*
        response = websocket.receive_json()
        assert response["type"] == "STATE_UPDATE" or response["type"] == "CONFIRMATION"

def test_state_streams(test_client_ws):
    with test_client_ws.websocket_connect("/ws/asp") as websocket:
        # Handshake
        websocket.send_json({"type": "CONNECT", "client_id": "test", "version": "1.0"})
        websocket.receive_json() # ACK
        
        # Access the underlying engine from app state
        # Note: TestClient wraps the app, we need to access the state carefully if possible
        # Or, we can trigger via API if we have one. 
        # But wait, TestClient runs the app in the same process usually.
        engine = test_client_ws.app.state.engine
        
        # Force a UI refresh which should broadcast a state update
        engine.refresh_ui()
        
        # We should receive the broadcast
        msg = websocket.receive_json()
        assert msg["type"] == "STATE_UPDATE"
        assert "payload" in msg
        assert "ui" in msg["payload"]
