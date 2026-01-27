from typing import Protocol, List, Tuple
import logging

logger = logging.getLogger(__name__)

class ModelProvider(Protocol):
    async def generate(self, prompt: str) -> str:
        ...

class ModelGateway:
    """
    Routes inference requests to the best available provider (Local > Peer > Cloud).
    """
    def __init__(self):
        # List of (priority, provider)
        self.providers: List[Tuple[int, ModelProvider]] = []

    def register_provider(self, name: str, provider: ModelProvider, priority: int = 0):
        self.providers.append((priority, provider))
        # Sort by priority descending
        self.providers.sort(key=lambda x: x[0], reverse=True)

    async def generate(self, prompt: str) -> str:
        for priority, provider in self.providers:
            try:
                return await provider.generate(prompt)
            except Exception as e:
                logger.warning(f"Provider failed: {e}")
                continue
        
        raise RuntimeError("All inference providers failed")
