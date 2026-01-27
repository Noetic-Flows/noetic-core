from typing import List, Any, Dict, Optional
from noetic_stage.renderer import CanvasRenderer
from noetic_stage.reflex import ReflexManager
from noetic_stage.schema import Component
from noetic_knowledge import WorldState

class ReflexSystem:
    """
    Manages the 'Reflex Loop' (System 1) - UI rendering and Input handling.
    Runs synchronously at 60Hz.
    """
    def __init__(self):
        self.renderer = CanvasRenderer()
        self.manager = ReflexManager()
        self.root_component: Optional[Component] = None

    def set_root(self, root: Component):
        self.root_component = root

    def render_now(self, world_state: WorldState) -> Any:
        """
        Forces an immediate re-render of the UI with current state.
        """
        merged_context = self.manager.merge_state(world_state)
        if self.root_component:
            return self.renderer.render(self.root_component, merged_context)
        return {}

    def tick(self, events: List[Any], world_state: WorldState) -> Any:
        """
        Performs one frame of the Reflex Loop.
        """
        # 1. Handle Events (Stub)
        for event in events:
            pass
            
        # 2. Merge State
        merged_context = self.manager.merge_state(world_state)
        
        # 3. Render
        if self.root_component:
            return self.renderer.render(self.root_component, merged_context)
            
        return {}
