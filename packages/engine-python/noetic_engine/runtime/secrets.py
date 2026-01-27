import os
import re
from typing import Dict, Any

class SecretsManager:
    """
    Handles secure retrieval and injection of secrets (API Keys, Passwords).
    Prevents secrets from being stored in Knowledge or Logs.
    """
    def __init__(self, prefix: str = "NOETIC_SECRET_"):
        self.prefix = prefix

    def get_secret(self, key: str) -> str:
        """
        Fetches secret from environment or vault.
        """
        env_key = f"{self.prefix}{key}"
        val = os.getenv(env_key)
        if not val:
            raise KeyError(f"Secret {key} not found in environment ({env_key})")
        return val

    def inject_secrets(self, data: Any) -> Any:
        """
        Recursively scans data for {{secrets.KEY}} placeholders and replaces them.
        """
        if isinstance(data, str):
            # Find all {{secrets.XYZ}}
            matches = re.findall(r"{{secrets\.([A-Z0-9_]+)}}", data)
            for key in matches:
                secret_val = self.get_secret(key)
                data = data.replace(f"{{{{secrets.{key}}}}}", secret_val)
            return data
        
        elif isinstance(data, dict):
            return {k: self.inject_secrets(v) for k, v in data.items()}
        
        elif isinstance(data, list):
            return [self.inject_secrets(i) for i in data]
        
        return data
