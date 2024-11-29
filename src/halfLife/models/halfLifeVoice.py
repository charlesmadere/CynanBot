from enum import Enum, auto


class HalfLifeVoice(Enum):

    ALL = auto()
    BARNEY = auto()
    FEMALE = auto()
    MALE = auto()
    POLICE = auto()
    SCIENTIST = auto()
    SOLDIER = auto()

    @property
    def value(self) -> str:
        match self:
            case HalfLifeVoice.ALL: return 'all'
            case HalfLifeVoice.BARNEY: return 'barney'
            case HalfLifeVoice.FEMALE: return 'female'
            case HalfLifeVoice.MALE: return 'male'
            case HalfLifeVoice.POLICE: return 'police'
            case HalfLifeVoice.SCIENTIST: return 'scientist'
            case HalfLifeVoice.SOLDIER: return 'soldier'
            case _: raise RuntimeError(f'unknown HalfLifeVoice: \"{self}\"')