import asyncio
import time
from typing import Optional
from noetic_knowledge import KnowledgeStore
from noetic_engine.skills import SkillRegistry
from noetic_engine.skills.library.system.control import WaitSkill, LogSkill
from noetic_engine.skills.library.memory import MemorizeSkill, RecallSkill
from noetic_engine.cognition.adk_adapter import ADKAdapter
from noetic_engine.runtime.mesh import MeshOrchestrator
from .reflex import ReflexSystem
from .scheduler import Scheduler
from .lifecycle import LifecycleManager
from .flow_manager import FlowManager

class NoeticEngine:
    def __init__(self, db_url: str = "sqlite:///:memory:"):
        self.running = False
        
        # 1. Initialize Core Subsystems
        self.knowledge = KnowledgeStore(db_url=db_url)
        self.skills = SkillRegistry()
        
        # 2. Initialize Mesh & Brain (Replaces CognitiveSystem)
        self.mesh = MeshOrchestrator()
        self.subscribers = [] # List of asyncio.Queue for ASP streaming
        
        # In the future, we load the AgentDefinition from a file/DB
        # For now, we mock the primary definition
        self.primary_agent_def = "TODO: Load from AgentDefinition" 
        self.brain = ADKAdapter(self.mesh, self.primary_agent_def)
        
        self.latest_ui = None
        
        # 3. Register core skills
        self.skills.register(WaitSkill())
        self.skills.register(LogSkill())
        self.skills.register(MemorizeSkill())
        self.skills.register(RecallSkill())
        
        # 4. Initialize Reflex Loop
        self.reflex = ReflexSystem()
        
        # [PRODUCTION] Set Default System Visage
        from noetic_engine.visages.system import SystemDashboardVisage
        
        self.system_visage = SystemDashboardVisage(self)
        self.reflex.set_visage(self.system_visage)

        self.scheduler = Scheduler(target_fps=30)
        self.lifecycle = LifecycleManager(self)
        self.flow_manager = FlowManager()

    async def start(self):
        self.running = True
        print("Noetic Engine Starting...")
        # Start the Brain (ADK)
        await self.brain.start()
        await self.run_loop()

    async def stop(self):
        self.running = False
        print("Noetic Engine Stopping...")
        await self.brain.stop()

    def push_event(self, event_type: str, payload: dict = None):
        """
        Public API to inject events into the Noetic Engine (e.g. from UI).
        """
        self.knowledge.push_event(event_type, payload)
        # Also notify the brain? 
        # For now, ADK polls or we can push to it if ADKAdapter supports it.
        # asyncio.create_task(self.brain.process_user_input(str(payload), None))

    def refresh_ui(self):
        """
        Forces an immediate re-render of the latest UI.
        """
        world_state = self.knowledge.get_world_state()
        self.latest_ui = self.reflex.render_now(world_state)

    async def run_loop(self):
        """
        The main Bi-Cameral Execution Loop (Reflex only).
        Cognition happens in background ADKAdapter task.
        """
        print("Noetic Engine Loop Running...")
        while self.running:
            start_time = time.monotonic()

            try:
                # --- 1. REFLEX PHASE (Fast) ---
                world_state = self.knowledge.get_world_state()
                events = self.skills.poll_inputs()
                
                # Update Lifecycle
                if events:
                    await self.lifecycle.notify_interaction()
                await self.lifecycle.tick()
                
                # Update UI
                self.latest_ui = self.reflex.tick(events, world_state)
                
                # Broadcast State Update
                if self.latest_ui:
                    self._broadcast_state(self.latest_ui)

                # --- 2. COGNITIVE PHASE (Handled by ADKAdapter background task) ---
                # We do NOT block here.

            except Exception as e:
                # Reflex Loop Failure is CRITICAL
                print(f"CRITICAL: Reflex Loop Failure: {e}")
                self.running = False
                raise e

            # --- 3. SLEEP ---
            await self.scheduler.sleep_until_next_tick(start_time)

    def subscribe(self) -> asyncio.Queue:
        """
        Subscribes to the engine's state update stream.
        Returns an asyncio.Queue that receives state updates.
        """
        queue = asyncio.Queue()
        self.subscribers.append(queue)
        print(f"New subscriber registered. Total subscribers: {len(self.subscribers)}")
        
        # Send latest state immediately if available
        if self.latest_ui:
             msg = self._build_state_msg(self.latest_ui)
             queue.put_nowait(msg)
             
        return queue

    def unsubscribe(self, queue: asyncio.Queue):
        if queue in self.subscribers:
            self.subscribers.remove(queue)
            print(f"Subscriber removed. Total subscribers: {len(self.subscribers)}")

    def _build_state_msg(self, ui_state):
        # Helper to serialize UI
        # ui_state is list[AnyComponent]. Pydantic models need .model_dump()
        # But for simplicity in this prototype, we'll let FastAPI/Starlette's json encoder handle it 
        # OR we manually dump if they are Pydantic models.
        # fastui components ARE pydantic models.
        payload_ui = []
        if isinstance(ui_state, list):
            payload_ui = [c.model_dump(mode='json') for c in ui_state]
        else:
            payload_ui = [ui_state.model_dump(mode='json')]

        return {
            "type": "STATE_UPDATE",
            "payload": {
                "ui": payload_ui
            }
        }

    def _broadcast_state(self, ui_state):
        """
        Pushes the current UI state to all subscribers.
        """
        try:
            msg = self._build_state_msg(ui_state)
            print(f"[DEBUG] Generated State Update: {str(msg)[:200]}...") # Truncate for sanity
        except Exception as e:
            print(f"[ERROR] Failed to build state msg: {e}")
            return

        # Cleanup closed loops
        for q in self.subscribers:
            if not q.full():
                q.put_nowait(msg)

