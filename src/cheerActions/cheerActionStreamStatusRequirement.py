from enum import Enum, auto


class CheerActionStreamStatusRequirement(Enum):

    ANY = auto()
    OFFLINE = auto()
    ONLINE = auto()
