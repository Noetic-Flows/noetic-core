import sys
import os
import pytest

# Add paths to sys.path
cwd = os.getcwd()
sys.path.append(os.path.join(cwd, "noetic-lang/src"))
sys.path.append(os.path.join(cwd, "engines/python"))

# Run pytest
exit_code = pytest.main(["engines/python/tests/knowledge/test_stack.py"])
sys.exit(exit_code)
