import os
import inspect
import sys

from .joke import Joke
from .chores import ChoreJoke
from .her import HerJoke
from .i_am_dad import IAmDadJoke
from .ok_boomer import OkBoomerJoke
from .rank import RankJoke
from .smashing import SmashingJoke

# Dictionary to save registered Joke objects
JOKES = {
    "ChoreJoke": ChoreJoke(),
    "HerJoke": HerJoke(),
    "IAmDadJoke": IAmDadJoke(),
    "OkBoomerJoke": OkBoomerJoke(),
    "RankJoke": RankJoke(),
    "SmashingJoke": SmashingJoke()
}

