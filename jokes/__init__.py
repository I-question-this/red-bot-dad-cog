import os
import inspect
import sys

from .joke import Joke

# Add all python files to the __all__ variable, except for __init__.py
__all__ = list(name.replace(".py", "") for name in
               (filter(lambda name: name != "__init__.py" and ".py" in name,
os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".")))))

# Dictionary to save registered Joke objects
JOKES = dict()

# Go through all modules in "dad.jokes" aka "here"
for module in __all__:
    # Import this package
    __import__("dad.jokes", fromlist=[module])
    # Check each class in the imported module for Joke objects
    for class_name, cls in inspect.getmembers(sys.modules[
            f"dad.jokes.{module}"], inspect.isclass):
        # Ensure that it's a proper non-abstract Joke class
        if issubclass(cls, Joke) and not cls == Joke:
            obj = cls()
            # Register the joke
            JOKES[obj.name] = obj

