import asyncio
import logging
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from noetic_engine.runtime.engine import NoeticEngine
from noetic_engine.loader import NoeticLoader

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start engine in the background when FastAPI starts
    codex_path = app.state.codex_path
    engine = app.state.engine
    
    loader = NoeticLoader()
    loader.load(engine, codex_path)
    
    # Run engine start in a task so it doesn't block lifespan
    task = asyncio.create_task(engine.start())
    logger.info(f"Noetic Engine background task started with codex: {codex_path}")
    
    yield
    
    # Shutdown
    await engine.stop()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

def create_app(engine: NoeticEngine, codex_path: str):
    app = FastAPI(lifespan=lifespan)
    app.state.engine = engine
    app.state.codex_path = codex_path

    @app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
    def api_index(event: Optional[str] = None) -> list[AnyComponent]:
        """
        Returns the latest UI tree rendered by the Reflex loop.
        Processes an optional 'event' trigger.
        """
        if event:
            logger.info(f"Processing Event: {event}")
            if event.startswith("project."):
                # Resolve title from world state
                ws = engine.knowledge.get_world_state()
                title = "Unknown Project"
                # Check for project by ID string or name alias
                for eid, entity in ws.entities.items():
                    if str(eid) == event or entity.attributes.get("name") == event:
                        title = entity.attributes.get("title", "Unnamed")
                        break
                
                summary = f"Viewing details for: {title}. Status is active."
                logger.info(f"Updating local state: selected_project_summary = {summary}")
                engine.reflex.manager.update("selected_project_summary", summary)
            else:
                engine.push_event(event, {})
            
            # Small delay to ensure any background DB writes are finalized 
            import time
            time.sleep(0.1)
            
            # Force refresh so latest_ui is updated before we return it
            engine.refresh_ui()
            logger.info(f"UI Refreshed. Summary in local_state: {engine.reflex.manager.local_state.get('selected_project_summary')}")

        if engine.latest_ui is not None:
            ui = engine.latest_ui
            components = ui if isinstance(ui, list) else [ui]
            logger.info(f"Rendering UI with {len(components)} components. Event param: {event}")
            # logger.debug(f"UI Tree: {components}")
            return components
        
        return [c.Page(components=[c.Text(text="Engine starting... please refresh in a moment.")])]

    @app.get("/{path:path}")
    async def html_landing() -> HTMLResponse:
        """
        Serves the prebuilt HTML shell.
        """
        return HTMLResponse(prebuilt_html(title="Noetic Nexus OS"))
    
    # -----------------------------
    # Agent Server Protocol (ASP)
    # -----------------------------
    from fastapi import WebSocket, WebSocketDisconnect
    
    @app.websocket("/ws/asp")
    async def asp_endpoint(websocket: WebSocket):
        await websocket.accept()
        logger.info("ASP Client Connected")
        
        # Subscribe to Engine Updates
        queue = engine.subscribe()
        
        async def receive_loop():
            try:
                while True:
                    # 1. Receive Message
                    message = await websocket.receive_json()
                    msg_type = message.get("type")
                    
                    if msg_type == "CONNECT":
                        await websocket.send_json({
                            "type": "ACK",
                            "status": "CONNECTED", 
                            "server_time": 0
                        })
                    
                    elif msg_type == "INTENT":
                        payload = message.get("payload", {})
                        engine.push_event("user.intent", payload)
                        await websocket.send_json({
                            "type": "CONFIRMATION",
                            "status": "RECEIVED",
                            "ref_id": message.get("ref_id")
                        })
                    else:
                        logger.warning(f"Unknown ASP message type: {msg_type}")
            except RuntimeError:
                logger.info("Client Disconnected (Receive Loop)")
            except WebSocketDisconnect:
                logger.info("WebSocket Disconnected (Receive Loop)")
                
        async def send_loop():
            try:
                while True:
                    # 2. Broadcast Updates
                    msg = await queue.get()
                    await websocket.send_json(msg)
            except RuntimeError:
                 logger.info("Client Disconnected (Send Loop)")
            except WebSocketDisconnect:
                 logger.info("WebSocket Disconnected (Send Loop)")

        # Run both loops handling clean shutdown
        try:
            receiver = asyncio.create_task(receive_loop())
            sender = asyncio.create_task(send_loop())
            done, pending = await asyncio.wait(
                [receiver, sender], 
                return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()
        finally:
            engine.unsubscribe(queue)
            logger.info("ASP Client Session Ended")

    return app

# -----------------------------
# Module Access (for Uvicorn)
# -----------------------------
# We instantiate a default engine/app so `uvicorn noetic_engine.server:app` works.
_engine = NoeticEngine()
app = create_app(_engine, "./noetic.db")
