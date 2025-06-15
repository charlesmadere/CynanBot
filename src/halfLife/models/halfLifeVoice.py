from enum import Enum, auto


class HalfLifeVoice(Enum):

    ALL = auto()
    BARNEY = auto()
    HEV = auto()
    INTERCOM = auto()
    POLICE = auto()
    SCIENTIST = auto()
    SOLDIER = auto()

    @property
    def humanName(self) -> str:
        match self:
            case HalfLifeVoice.ALL: return 'All'
            case HalfLifeVoice.BARNEY: return 'Barney'
            case HalfLifeVoice.HEV: return 'Hazardous EnVironment suit (HEV)'
            case HalfLifeVoice.INTERCOM: return 'Intercom'
            case HalfLifeVoice.POLICE: return 'Police'
            case HalfLifeVoice.SCIENTIST: return 'Scientist'
            case HalfLifeVoice.SOLDIER: return 'Soldier'
            case _: raise RuntimeError(f'unknown HalfLifeVoice: \"{self}\"')

    @property
    def keyName(self) -> str:
        match self:
            case HalfLifeVoice.ALL: return 'all'
            case HalfLifeVoice.BARNEY: return 'barney'
            case HalfLifeVoice.HEV: return 'hev'
            case HalfLifeVoice.INTERCOM: return 'intercom'
            case HalfLifeVoice.POLICE: return 'police'
            case HalfLifeVoice.SCIENTIST: return 'scientist'
            case HalfLifeVoice.SOLDIER: return 'soldier'
            case _: raise RuntimeError(f'unknown HalfLifeVoice: \"{self}\"')
