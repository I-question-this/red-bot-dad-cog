import os
import sys

# Add all python files to the __all__ variable.
__all__ = list(name.replace(".py", "") for name in
               (filter(lambda name: name != "__init__.py" and ".py" in name,
os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".")))))
