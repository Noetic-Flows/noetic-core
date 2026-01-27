from typing import List
from noetic_lang.core import IdentityContext, ACL
import fnmatch

class AccessControlEngine:
    def __init__(self):
        self.policies: List[ACL] = []

    def add_policy(self, policy: ACL):
        self.policies.append(policy)

    def check(self, identity: IdentityContext, permission: str, resource_id: str) -> bool:
        """
        Checks if the identity has the permission on the resource.
        """
        # 1. Iterate over user's roles
        for role in identity.roles:
            # 2. Find matching policies
            for policy in self.policies:
                if policy.role == role:
                    # 3. Check Resource Pattern
                    if fnmatch.fnmatch(resource_id, policy.resource_pattern):
                        # 4. Check Permission
                        if permission in policy.permissions or "admin" in policy.permissions:
                            return True
        return False
