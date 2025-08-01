from enum import Enum, auto


class ChatterItemType(Enum):

    AIR_STRIKE = auto()
    BANANA = auto()
    GRENADE = auto()

    @property
    def humanName(self) -> str:
        match self:
            case ChatterItemType.AIR_STRIKE: return 'Air Strike'
            case ChatterItemType.BANANA: return 'Banana'
            case ChatterItemType.GRENADE: return 'Grenade'
            case _: raise ValueError(f'Unknown ChatterItemType value: \"{self}\"')
