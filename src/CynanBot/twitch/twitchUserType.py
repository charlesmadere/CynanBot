from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class TwitchUserType(Enum):

    ADMIN = auto()
    GLOBAL_MOD = auto()
    NORMAL = auto()
    STAFF = auto()

    @classmethod
    def fromStr(ctls, text: Optional[str]):
        if not utils.isValidStr(text):
            return TwitchUserType.NORMAL

        text = text.lower()

        if text == 'admin':
            return TwitchUserType.ADMIN
        elif text == 'global_mod':
            return TwitchUserType.GLOBAL_MOD
        elif text == 'staff':
            return TwitchUserType.STAFF
        else:
            return TwitchUserType.NORMAL

    def __str__(self) -> str:
        if self is TwitchUserType.ADMIN:
            return 'admin'
        elif self is TwitchUserType.GLOBAL_MOD:
            return 'global_mod'
        elif self is TwitchUserType.NORMAL:
            return 'normal'
        elif self is TwitchUserType.STAFF:
            return 'staff'
        else:
            raise RuntimeError(f'unknown TwitchUserType: \"{self}\"')
