# Future
from __future__ import annotations

# Standard Library
import logging
from typing import Final, Literal, NamedTuple

# My stuff
from .client import *
from .exceptions import *
from .http import *
from .objects import *
from .utils import *
from .values import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: Final[VersionInfo] = VersionInfo(major=0, minor=1, micro=3, releaselevel="final", serial=0)

__title__: Final[str] = "spotipy"
__author__: Final[str] = "Axelancerr"
__copyright__: Final[str] = "Copyright 2021-present Axelancerr"
__license__: Final[str] = "MIT"
__version__: Final[str] = "0.1.3"
__maintainer__: Final[str] = "Aaron Hennessey"
__source__: Final[str] = "https://github.com/Axelware/spoti.py"

logging.getLogger("spotipy")
