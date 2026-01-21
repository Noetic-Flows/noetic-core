import pytest
from uuid import uuid4
from noetic_engine.conscience import Evaluator, Principle, JudgementContext
from noetic_engine.knowledge import KnowledgeStore

@pytest.fixture
def store():
    return KnowledgeStore(db_url="sqlite:///:memory:")

def test_tag_inheritance_logic(store):
    evaluator = Evaluator()
    
    # 1. Setup Ontology in Knowledge: tag.database.write IS-A tag.destructive
    # For tags, we can use UUIDs or names. If we use names, we must convert to UUID if KnowledgeStore requires it.
    # KnowledgeStore currently requires UUID for subject_id. 
    # Let's generate consistent UUIDs for our tag names.
    import uuid
    
    dest_name = "tag.destructive"
    write_name = "tag.database.write"
    
    # We'll use names as UUID strings if we want to be simple, 
    # or just use proper UUIDs and match them.
    # Let's use string-based IDs for this test to match the 'tags' list.
    # KnowledgeStore ingest_fact expects UUID objects.
    
    u_dest = uuid.uuid5(uuid.NAMESPACE_DNS, dest_name)
    u_write = uuid.uuid5(uuid.NAMESPACE_DNS, write_name)
    
    store.ingest_fact(u_write, "is_a", object_entity_id=u_dest)
    
    # 2. Principle targeting 'tag.destructive' (UUID string)
    p1 = Principle(
        id="p.no_destructive",
        affects="val.safety",
        logic={
            "if": [
                {"in": [str(u_dest), {"var": "tags"}]},
                500.0,
                0.0
            ]
        }
    )
    
    # 3. Action tagged with 'tag.database.write' (UUID string)
    ctx = JudgementContext(
        agent_id="agent-1",
        action_id="db.delete_user",
        tags=[str(u_write)],
        world_state={}
    )
    
    # 4. Evaluate
    result = evaluator.judge(ctx, [p1], store=store)
    
    assert str(u_dest) in ctx.tags
    assert result.cost == 500.0
