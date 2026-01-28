# Immediate To-Do Queue

## Priority 0: Stabilize the Nervous System (ASP)
The immediate goal is to ensure rock-solid communication between the Python Engine and the Next.js Web Hub.

- [ ] **Engine: Verify WebSocket Protocol**
    - Audit `packages/engine-python/noetic_engine/server.py` for correct `CONNECT`, `INTENT`, and `ACK` handling.
    - Ensure `push_event` in Engine correctly broadcasts to the WebSocket queue.

- [ ] **Client: Implement Web Hub Logic**
    - Flesh out `apps/web-hub/src/app` to connect to `ws://localhost:8000/ws/asp`.
    - Implement a visual indicator for "Connection Status" (Red/Green).
    - Render the `FastUI` payload received from the engine.

- [ ] **Integration Test: The "Ping" Flow**
    - Create a simple `.noetic` flow that just echoes back a message.
    - Verify it works end-to-end from Web Hub -> Engine -> Web Hub.
