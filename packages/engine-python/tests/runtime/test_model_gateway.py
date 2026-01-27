import pytest
from unittest.mock import AsyncMock
from noetic_engine.cognition.gateway import ModelGateway, ModelProvider

class MockProvider(ModelProvider):
    def __init__(self, name, success=True):
        self.name = name
        self.success = success
        
    async def generate(self, prompt: str):
        if not self.success:
            raise Exception("Provider failed")
        return f"Response from {self.name}"

@pytest.mark.asyncio
async def test_gateway_routing_local_first():
    gateway = ModelGateway()
    
    local = MockProvider("local", success=True)
    cloud = MockProvider("cloud", success=True)
    
    gateway.register_provider("local", local, priority=10)
    gateway.register_provider("cloud", cloud, priority=1)
    
    response = await gateway.generate("Hello")
    assert response == "Response from local"

@pytest.mark.asyncio
async def test_gateway_failover():
    gateway = ModelGateway()
    
    local = MockProvider("local", success=False)
    cloud = MockProvider("cloud", success=True)
    
    gateway.register_provider("local", local, priority=10)
    gateway.register_provider("cloud", cloud, priority=1)
    
    response = await gateway.generate("Hello")
    assert response == "Response from cloud"
