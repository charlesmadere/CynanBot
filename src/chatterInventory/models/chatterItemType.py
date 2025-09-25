from enum import Enum, auto


class ChatterItemType(Enum):

    AIR_STRIKE = auto()
    ANIMAL_PET = auto()
    BANANA = auto()
    CASSETTE_TAPE = auto()
    GASHAPON = auto()
    GRENADE = auto()
    TM_36 = auto()
    VORE = auto()

    @property
    def humanName(self) -> str:
        match self:
            case ChatterItemType.AIR_STRIKE: return 'Air Strike'
            case ChatterItemType.ANIMAL_PET: return 'Pet Animal'
            case ChatterItemType.BANANA: return 'Banana'
            case ChatterItemType.CASSETTE_TAPE: return 'Cassette Tape'
            case ChatterItemType.GASHAPON: return 'Gashapon/ガシャポン'
            case ChatterItemType.GRENADE: return 'Grenade'
            case ChatterItemType.TM_36: return 'TM 36'
            case ChatterItemType.VORE: return 'Vore'
            case _: raise ValueError(f'Unknown ChatterItemType value: \"{self}\"')

    @property
    def pluralHumanName(self) -> str:
        match self:
            case ChatterItemType.AIR_STRIKE: return 'Air Strikes'
            case ChatterItemType.ANIMAL_PET: return 'Animal Pets'
            case ChatterItemType.BANANA: return 'Bananas'
            case ChatterItemType.CASSETTE_TAPE: return 'Cassette Tapes'
            case ChatterItemType.GASHAPON: return 'Gashapons/ガシャポン'
            case ChatterItemType.GRENADE: return 'Grenades'
            case ChatterItemType.TM_36: return 'TM 36\'s'
            case ChatterItemType.VORE: return 'Vores'
            case _: raise ValueError(f'Unknown ChatterItemType value: \"{self}\"')
