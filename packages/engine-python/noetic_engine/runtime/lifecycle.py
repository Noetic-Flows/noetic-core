from typing import Any, Optional
import time
import asyncio

class LifecycleManager:
    """
    Manages the lifecycle of the Noetic Engine.
    Handles idle timeouts, sleep modes, and cleanup.
    """
    def __init__(self, engine: Any, idle_timeout: float = 300.0, rem_timeout: float = 600.0):
        self.engine = engine
        self.last_interaction = time.monotonic()
        self.state = "AWAKE" # AWAKE, IDLE, REM
        self.state_entry_time = self.last_interaction
        self.idle_timeout = idle_timeout
        self.rem_timeout = rem_timeout
        self.maintenance_task = None

    async def notify_interaction(self):
        """
        Called when an interaction occurs (UI event, etc.)
        Resets the idle timer.
        """
        self.last_interaction = time.monotonic()
        if self.state != "AWAKE":
            # Cancel maintenance task if running
            if self.maintenance_task and not self.maintenance_task.done():
                self.maintenance_task.cancel()
                try:
                    await self.maintenance_task
                except asyncio.CancelledError:
                    pass
            
            print(f"Lifecycle: Waking up from {self.state}.")
            self.state = "AWAKE"
            self.state_entry_time = self.last_interaction

    async def tick(self):
        """
        Called every frame. Checks for idle state.
        """
        if self.state == "REM":
            return

        now = time.monotonic()
        
        if self.state == "AWAKE":
            elapsed = now - self.last_interaction
            if elapsed > self.idle_timeout:
                self.state = "IDLE"
                self.state_entry_time = now
                print("Lifecycle: Entering IDLE state.")
        
        if self.state == "IDLE":
            # Check for REM transition based on time spent in IDLE
            elapsed_idle = now - self.state_entry_time
            if elapsed_idle > self.rem_timeout:
                await self.enter_rem_sleep()

    async def enter_rem_sleep(self):
        print("Lifecycle: Entering REM sleep.")
        self.state = "REM"
        self.state_entry_time = time.monotonic()
        # Trigger consolidation
        if hasattr(self.engine.knowledge, "run_sleep_cycle"):
             # We store the task
             self.maintenance_task = asyncio.create_task(self.engine.knowledge.run_sleep_cycle())