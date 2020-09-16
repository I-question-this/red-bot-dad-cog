import os
import inspect
import sys

from .joke import Joke
from .becky import BeckyJoke
from .chores import ChoreJoke
from .her import HerJoke
from .i_am_dad import IAmDadJoke
from .ok_boomer import OkBoomerJoke
from .rank import RankJoke
from .smashing import SmashingJoke
from .thats_fair import ThatsFairJoke

# Dictionary to save registered Joke objects
JOKES = {
    "BeckyJoke": BeckyJoke(),
    "ChoreJoke": ChoreJoke(),
    "HerJoke": HerJoke(),
    "IAmDadJoke": IAmDadJoke(),
    "OkBoomerJoke": OkBoomerJoke(),
    "RankJoke": RankJoke(),
    "SmashingJoke": SmashingJoke(),
    "ThatsFairJoke": ThatsFairJoke()
}

