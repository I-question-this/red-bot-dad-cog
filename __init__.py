from abc import ABC
import inspect
import sys
# Import all the files that are relevant joke files
from .jokes import __all__ as all_joke_files

# Dictionary to save registered Joke objects
JOKES = dict()

# Go through all the possible jokes.
for joke_file in all_joke_files:
    # Import this sub-package/file
    __import__("dad.jokes", fromlist=[joke_file])
    # Check each class in that sub-package/file
    for class_name, obj in inspect.getmembers(sys.modules[
            f"dad.jokes.{joke_file}"], inspect.isclass):
        # Ensure that it's a proper XJoke file
        if "Joke" in class_name and not "Joke" == class_name:
            # Create an instance
            inst = obj() 
            # Register the joke
            JOKES[inst.name] = inst


# Set up Dad bot
from .dad import Dad
def setup(bot):
    bot.add_cog(Dad(bot, JOKES))
