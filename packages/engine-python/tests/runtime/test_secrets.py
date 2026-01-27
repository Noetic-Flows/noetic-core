import pytest
import os
from noetic_engine.runtime.secrets import SecretsManager

def test_secrets_injection():
    # Use environment variables as mock vault for now
    os.environ["NOETIC_SECRET_API_KEY"] = "sk-123"
    
    manager = SecretsManager()
    
    # 1. Fetch secret
    key = manager.get_secret("API_KEY")
    assert key == "sk-123"
    
    # 2. Inject into payload
    payload = {"url": "https://api.com", "token": "{{secrets.API_KEY}}"}
    injected = manager.inject_secrets(payload)
    
    assert injected["token"] == "sk-123"

def test_secrets_redaction():
    manager = SecretsManager()
    os.environ["NOETIC_SECRET_PASS"] = "password123"
    
    # Ensure logging/printing doesn't leak
    # (Manual check or mock logger)
    pass
