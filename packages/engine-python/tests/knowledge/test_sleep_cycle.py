import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from noetic_knowledge.store.store import KnowledgeStore
from noetic_knowledge.store.schema import Fact

@pytest.fixture
def store():
    # Use in-memory DB
    return KnowledgeStore(db_url="sqlite:///:memory:", collection_name=f"test_sleep_{uuid4().hex}")

@pytest.mark.asyncio
async def test_pruning_expired_events(store):
    # 1. Ingest some "transient" events/facts
    # We simulate this by ingesting facts and manually setting their valid_from to the past
    # In a real scenario, we might have a 'transient' tag.
    
    user_id = uuid4()
    
    # Active fact
    f1 = store.ingest_fact(user_id, "status", object_literal="active")
    
    # Old fact (simulate by accessing DB directly or waiting, but for test speed we might need to mock time or access DB)
    # Let's just create a fact and then manually expire it to see if 'prune' hard deletes it 
    # OR testing that 'run_sleep_cycle' identifies 'stale' facts.
    
    # Better approach for "Folding":
    # 1. Ingest many small facts.
    # 2. Run sleep cycle with a mock "summarizer".
    # 3. Assert small facts are archived (valid_until set) and new summary fact exists.
    pass

@pytest.mark.asyncio
async def test_consolidation_logic(store):
    # Mock a summarizer function
    async def mock_summarize(facts):
        return "User performed 5 steps."
    
    store.summarizer = mock_summarize
    
    subject_id = uuid4()
    
    # 1. Ingest facts to be folded
    # Predicate "episodic_log" is a good candidate for folding
    facts = []
    for i in range(5):
        f = store.ingest_fact(subject_id, "episodic_log", object_literal=f"step {i}", allow_multiple=True)
        facts.append(f)
        
    # 2. Run Sleep Cycle
    # We expect run_sleep_cycle to trigger 'fold_episodes'
    await store.run_sleep_cycle()
    
    # 3. Assertions
    state = store.get_world_state()
    
    # Filter facts for our subject
    active_facts = [f for f in state.facts if f.subject_id == subject_id and f.predicate == "episodic_log"]
    
    # Debug info if assertion fails
    if len(active_facts) > 0:
        print(f"Active facts remaining: {[f.object_literal for f in active_facts]}")
        
    assert len(active_facts) == 0, "Raw episodic logs should be archived"
    
    # Check for summary fact
    summary_facts = [f for f in state.facts if f.subject_id == subject_id and f.predicate == "episodic_summary"]
    assert len(summary_facts) == 1
    assert summary_facts[0].object_literal == "User performed 5 steps."
