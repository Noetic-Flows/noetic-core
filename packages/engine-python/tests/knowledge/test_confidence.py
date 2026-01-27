import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from noetic_knowledge.store.schema import Fact

def test_fact_decay():
    now = datetime.utcnow()
    past = now - timedelta(hours=24) # 1 day ago
    
    # 1. Axiomatic Fact (Should not decay)
    f_axiom = Fact(
        id=uuid4(),
        subject_id=uuid4(),
        predicate="is_a",
        object_literal="test",
        valid_from=past,
        confidence=1.0,
        source_type="axiom"
    )
    
    assert f_axiom.current_confidence == 1.0
    
    # 2. Inference Fact (Should decay)
    f_inf = Fact(
        id=uuid4(),
        subject_id=uuid4(),
        predicate="thinks",
        object_literal="test",
        valid_from=past,
        confidence=1.0,
        source_type="inference"
    )
    
    # After 24h, decay is 0.9
    assert abs(f_inf.current_confidence - 0.9) < 0.001
    
    # 3. Future fact (Should not decay or be weird)
    f_future = Fact(
        id=uuid4(),
        subject_id=uuid4(),
        predicate="will_be",
        object_literal="test",
        valid_from=now + timedelta(hours=1),
        confidence=1.0,
        source_type="inference"
    )
    assert f_future.current_confidence == 1.0
