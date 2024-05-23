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

        match text:
            case 'any': return CheerActionStreamStatusRequirement.ANY
            case 'offline': return CheerActionStreamStatusRequirement.OFFLINE
            case 'online': return CheerActionStreamStatusRequirement.ONLINE
            case _: raise ValueError(f'unknown CheerActionStreamStatusRequirement: \"{text}\"')

    def getDatabaseString(self) -> str:
        match self:
            case CheerActionStreamStatusRequirement.ANY: return 'any'
            case CheerActionStreamStatusRequirement.OFFLINE: return 'offline'
            case CheerActionStreamStatusRequirement.ONLINE: return 'online'
            case _: raise RuntimeError(f'unknown CheerActionStreamStatusRequirement: \"{self}\"')
