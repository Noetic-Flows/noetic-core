import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class JudgementRecord(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action_id: str
    total_cost: float
    breakdown: List[Dict[str, Any]]
    veto: bool = False
    violation_reason: Optional[str] = None

class AuditLogger:
    """
    Records the 'Why' behind Conscience decisions.
    Provides structured history and telemetry-ready events.
    """
    def __init__(self, history_limit: int = 100):
        self.history: List[JudgementRecord] = []
        self.history_limit = history_limit
    
    def log_judgement(self, 
                      action_id: str, 
                      total_cost: float, 
                      contributing_principles: List[Dict[str, Any]]):
        """
        Logs the outcome of a judgement and stores it in history.
        """
        record = JudgementRecord(
            action_id=action_id,
            total_cost=total_cost,
            breakdown=contributing_principles
        )
        self._add_to_history(record)
        
        # Telemetry-ready structured log
        if contributing_principles:
            logger.info(f"Judgement for '{action_id}': Cost={total_cost}")
            for entry in contributing_principles:
                logger.debug(f"  + {entry['id']} ({entry.get('affects', 'unknown')}): {entry['cost']}")
        else:
            logger.debug(f"Judgement for '{action_id}': Cost={total_cost} (Clean)")

    def log_violation(self, principle_id: str, reason: str, action_id: str = "unknown"):
        """
        Logs a hard veto and stores it in history.
        """
        record = JudgementRecord(
            action_id=action_id,
            total_cost=float('inf'),
            breakdown=[{"id": principle_id, "cost": float('inf')}],
            veto=True,
            violation_reason=reason
        )
        self._add_to_history(record)
        logger.warning(f"VETO TRIGGERED by '{principle_id}' on action '{action_id}': {reason}")

    def get_history(self) -> List[JudgementRecord]:
        return self.history

    def _add_to_history(self, record: JudgementRecord):
        self.history.append(record)
        if len(self.history) > self.history_limit:
            self.history.pop(0)
