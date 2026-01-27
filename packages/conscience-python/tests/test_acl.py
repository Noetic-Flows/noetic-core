import pytest
from noetic_lang.core import IdentityContext, ACL
from noetic_conscience.acl import AccessControlEngine

def test_acl_allow():
    ace = AccessControlEngine()
    
    # Define Policy
    ace.add_policy(ACL(role="admin", permissions=["read", "write", "execute"], resource_pattern="*"))
    ace.add_policy(ACL(role="viewer", permissions=["read"], resource_pattern="*"))
    
    # Identity
    user = IdentityContext(user_id="u1", roles=["viewer"])
    
    # Check
    assert ace.check(user, "read", "doc:123") == True
    assert ace.check(user, "write", "doc:123") == False

def test_acl_resource_pattern():
    ace = AccessControlEngine()
    ace.add_policy(ACL(role="editor", permissions=["write"], resource_pattern="project:A:*"))
    
    user = IdentityContext(user_id="u2", roles=["editor"])
    
    assert ace.check(user, "write", "project:A:doc1") == True
    assert ace.check(user, "write", "project:B:doc1") == False
