from enum import Enum, auto


class ChatterItemType(Enum):

    AIR_STRIKE = auto()
    BANANA = auto()
    CASSETTE_TAPE = auto()
    GRENADE = auto()

    @property
    def humanName(self) -> str:
        match self:
            case ChatterItemType.AIR_STRIKE: return 'Air Strike'
            case ChatterItemType.BANANA: return 'Banana'
            case ChatterItemType.CASSETTE_TAPE: return 'Cassette Tape'
            case ChatterItemType.GRENADE: return 'Grenade'
            case _: raise ValueError(f'Unknown ChatterItemType value: \"{self}\"')

    @property
    def pluralHumanName(self) -> str:
        match self:
            case ChatterItemType.AIR_STRIKE: return 'Air Strikes'
            case ChatterItemType.BANANA: return 'Bananas'
            case ChatterItemType.CASSETTE_TAPE: return 'Cassette Tapes'
            case ChatterItemType.GRENADE: return 'Grenades'
            case _: raise ValueError(f'Unknown ChatterItemType value: \"{self}\"')
