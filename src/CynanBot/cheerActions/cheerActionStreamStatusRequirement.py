from enum import Enum, auto

import CynanBot.misc.utils as utils


class CheerActionStreamStatusRequirement(Enum):

    ANY = auto()
    OFFLINE = auto()
    ONLINE = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return CheerActionStreamStatusRequirement.ANY

        text = text.lower()

        if text == 'any':
            return CheerActionStreamStatusRequirement.ANY
        elif text == 'offline':
            return CheerActionStreamStatusRequirement.OFFLINE
        elif text == 'online':
            return CheerActionStreamStatusRequirement.ONLINE
        else:
            raise ValueError(f'unknown CheerActionStreamStatusRequirement: \"{text}\"')

    def getDatabaseString(self) -> str:
        if self is CheerActionStreamStatusRequirement.ANY:
            return 'any'
        elif self is CheerActionStreamStatusRequirement.OFFLINE:
            return 'offline'
        elif self is CheerActionStreamStatusRequirement.ONLINE:
            return 'online'
        else:
            raise RuntimeError(f'unknown CheerActionStreamStatusRequirement: \"{self}\"')
