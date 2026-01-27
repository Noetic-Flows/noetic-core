import pytest
from uuid import uuid4
from noetic_knowledge.store.store import KnowledgeStore

@pytest.mark.asyncio
async def test_audit_log_folding():
    store = KnowledgeStore(db_url="sqlite:///:memory:")
    
    # Mock Summarizer
    async def mock_summarize(logs):
        return f"Summary of {len(logs)} actions"
    store.summarizer = mock_summarize
    
    agent_id = uuid4()
    
    # 1. Ingest Repetitive Logs (e.g. "Thinking...", "Thinking...")
    # Using 'audit.trace' predicate
    for i in range(10):
        store.ingest_fact(agent_id, "audit.trace", object_literal=f"Step {i}", allow_multiple=True)
        
    # 2. Run Folding
    # We need to expose _fold_episodes or a public method for audit folding specifically?
    # run_sleep_cycle calls _fold_episodes.
    # We should update _fold_episodes to handle 'audit.trace' too, or general 'folding' logic.
    
    # Let's assume we update the store to fold 'audit.trace' as well
    await store.run_sleep_cycle()
    
    # 3. Verify
    state = store.get_world_state()
    traces = [f for f in state.facts if f.predicate == "audit.trace"]
    summaries = [f for f in state.facts if f.predicate == "audit.summary"]
    
    assert len(traces) == 0, "Raw traces should be archived"
    assert len(summaries) == 1
    assert summaries[0].object_literal == "Summary of 10 actions"
