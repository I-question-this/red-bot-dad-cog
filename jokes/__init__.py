import os
import inspect
import sys

from .joke import Joke
from .becky import BeckyJoke
from .bonk import BonkJoke
from .chores import ChoreJoke
from .favoritsm import FavoritismJoke
from .her import HerJoke
from .i_am_dad import IAmDadJoke
from .naughty import NaughtyJoke
from .ok_boomer import OkBoomerJoke
from .rank import RankJoke
from .senpai import SenpaiJoke
from .simply import SimplyJoke
from .smashing import SmashingJoke
from .spongebob_chicken import SpongebobChickenJoke
from .stickbug import StickbugJoke
from .thats_fair import ThatsFairJoke


# Dictionary to save registered Joke objects
JOKES = {
    "BeckyJoke": BeckyJoke(),
    "BonkJoke": BonkJoke(),
    "ChoreJoke": ChoreJoke(),
    "FavoritismJoke": FavoritismJoke(),
    "HerJoke": HerJoke(),
    "IAmDadJoke": IAmDadJoke(),
    "NaughtyJoke": NaughtyJoke(),
    "OkBoomerJoke": OkBoomerJoke(),
    "RankJoke": RankJoke(),
    "SenpaiJoke": SenpaiJoke(),
    "SimplyJoke": SimplyJoke(),
    "SmashingJoke": SmashingJoke(),
    "SpongebobChickenJoke": SpongebobChickenJoke(),
    "StickbugJoke": StickbugJoke(),
    "ThatsFairJoke": ThatsFairJoke()
}

