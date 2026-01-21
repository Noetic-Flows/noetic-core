from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import json
from .logic import LogicEngine
from .veto import VetoSwitch, PolicyViolationError
from .audit import AuditLogger

class JudgementContext(BaseModel):
    agent_id: str
    action_id: str
    action_args: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    world_state: Dict[str, Any] = Field(default_factory=dict)

class JudgementResult(BaseModel):
    allowed: bool
    cost: float
    breakdown: List[Dict[str, Any]] # List of contributing principles

class Principle(BaseModel):
    id: str
    affects: str # e.g. "val.privacy"
    description: Optional[str] = None
    logic: Dict[str, Any] # JsonLogic rule

class Evaluator:
    def __init__(self, safety_mode: str = "fail_closed"):
        self.logic_engine = LogicEngine(safety_mode=safety_mode)
        self.audit = AuditLogger()
        # VetoSwitch is static

    def judge(self, context: JudgementContext, principles: List[Principle], store: Optional[Any] = None) -> JudgementResult:
        """
        Evaluates the action against the provided principles.
        """
        total_cost = 0.0
        contributing = []
        
        # 1. Tag Expansion (Inheritance)
        tags = context.tags
        if store and hasattr(store, "get_all_parent_tags"):
            tags = store.get_all_parent_tags(tags)
            context.tags = tags # Update context with expanded tags
            
        # 2. Prepare data for JsonLogic
        data = context.model_dump()
        data["action"] = {
            "id": context.action_id,
            **context.action_args
        }
        
        data_json = json.dumps(data, default=str)

        for principle in principles:
            # Check if principle applies (filtering)?
            # README says: "2. Filter: It discards Principles that don't apply to the current Action tags."
            # But the Principle schema in README didn't show 'applies_to_tags'. 
            # I'll assume for now we evaluate all provided principles, or the logic handles it.
            # Or maybe the Principle object should have a 'tags' field?
            # I'll stick to evaluating logic. If logic returns 0, it means it doesn't apply/no cost.
            
            rule_json = json.dumps(principle.logic)
            
            cost = self.logic_engine.evaluate(rule_json, data_json)
            
            try:
                VetoSwitch.check(cost, principle.id, data)
            except PolicyViolationError as e:
                self.audit.log_violation(principle.id, e.reason, action_id=context.action_id)
                raise e
            
            if cost > 0:
                total_cost += cost
                contributing.append({
                    "id": principle.id,
                    "cost": cost,
                    "affects": principle.affects
                })

        self.audit.log_judgement(context.action_id, total_cost, contributing)

        return JudgementResult(
            allowed=True,
            cost=total_cost,
            breakdown=contributing
        )
