from typing import Dict, Optional, Any
from noetic_engine.runtime.executors.flow import FlowExecutor

class FlowManager:
    def __init__(self, skill_registry: Optional[Any] = None):
        self._flows: Dict[str, FlowExecutor] = {}
        self.skills = skill_registry

    def register(self, flow_def: Dict[str, Any]):
        flow_id = flow_def.get("id")
        if not flow_id:
            return
        
        executor = FlowExecutor(flow_def, skill_registry=self.skills)
        self._flows[flow_id] = executor

    def get_executor(self, flow_id: str) -> Optional[FlowExecutor]:
        return self._flows.get(flow_id)
