import pytest
import time
from datetime import datetime, timedelta
from uuid import uuid4
from noetic_knowledge.store.store import KnowledgeStore

@pytest.fixture
def store():
    return KnowledgeStore(db_url="sqlite:///:memory:", collection_name=f"test_time_{uuid4().hex}")

def test_time_travel_world_state(store):
    user_id = uuid4()
    
    # 1. Fact at T1: Location = Home
    t1 = datetime.utcnow() - timedelta(minutes=10)
    # We can't easily force valid_from in ingest_fact currently as it uses NOW()
    # Let's see if we can update it or if we should add it to ingest_fact
    
    fact1 = store.ingest_fact(user_id, "location", object_literal="home")
    # Manually backdate for test
    session = store._get_session()
    f1_model = session.get(store.models.FactModel, fact1.id) if hasattr(store, 'models') else None
    # Actually I'll just wait a bit or use mocks if I can't backdate
    
    # Let's assume we can pass valid_from to ingest_fact (Gap identified!)
    
def test_time_travel_logic(store):
    user_id = uuid4()
    
    # Since ingest_fact uses utcnow(), we'll do real-time steps with small sleeps if needed,
    # or better, I will implement 'valid_from' parameter in ingest_fact.
    
    # But first, let's test what we have by sequence.
    
    # State A
    store.ingest_fact(user_id, "status", object_literal="hungry")
    time.sleep(0.1)
    checkpoint_1 = datetime.utcnow()
    time.sleep(0.1)
    
    # State B (Contradiction triggers valid_until on old fact)
    store.ingest_fact(user_id, "status", object_literal="full")
    checkpoint_2 = datetime.utcnow()
    
    # Query at checkpoint_1: should be 'hungry'
    state_1 = store.get_world_state(snapshot_time=checkpoint_1)
    assert len(state_1.facts) == 1
    assert state_1.facts[0].object_literal == "hungry"
    
    # Query at checkpoint_2: should be 'full'
    state_2 = store.get_world_state(snapshot_time=checkpoint_2)
    assert len(state_2.facts) == 1
    assert state_2.facts[0].object_literal == "full"
