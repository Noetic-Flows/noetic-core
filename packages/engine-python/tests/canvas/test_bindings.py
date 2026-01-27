import pytest
from noetic_stage.renderer import CanvasRenderer
from noetic_stage.schema import Text, Binding, Column, ForEach
from noetic_knowledge.store.schema import WorldState

@pytest.fixture
def renderer():
    return CanvasRenderer()

def test_resolve_text_binding(renderer):
    context = {
        "entities": {
            "p1": {"species": "Fern", "health": 80}
        }
    }
    
    # 1. Simple Binding
    comp = Text(content=Binding(bind="/entities/p1/species", fallback="Unknown"))
    result = renderer.render(comp, context)
    
    # FastUI c.Text(text="Fern")
    assert hasattr(result, "text")
    assert result.text == "Fern"

def test_resolve_nested_binding(renderer):
    context = {
        "world": {
            "status": "online",
            "metadata": {"version": "1.0"}
        }
    }
    
    comp = Text(content=Binding(bind="/world/metadata/version"))
    result = renderer.render(comp, context)
    assert result.text == "1.0"

def test_foreach_iteration(renderer):
    context = {
        "items": [
            {"name": "Item A"},
            {"name": "Item B"}
        ]
    }
    
    # ForEach iterating over /items, as 'item', template is Text binding to /item/name
    comp = ForEach(
        items=Binding(bind="/items"),
        var="item",
        template=Text(content=Binding(bind="/item/name"))
    )
    
    result = renderer.render(comp, context)
    
    # FastUI c.Div(components=[c.Text(text="Item A"), c.Text(text="Item B")])
    assert len(result.components) == 2
    assert result.components[0].text == "Item A"
    assert result.components[1].text == "Item B"

def test_binding_fallback(renderer):
    context = {"a": 1}
    comp = Text(content=Binding(bind="/b", fallback="Missing"))
    result = renderer.render(comp, context)
    assert result.text == "Missing"
