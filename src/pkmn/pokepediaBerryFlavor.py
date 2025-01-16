from enum import Enum, auto


class PokepediaBerryFlavor(Enum):

    BITTER = auto()
    DRY = auto()
    SOUR = auto()
    SPICY = auto()
    SWEET = auto()

    def getBerryFlavorId(self) -> int:
        match self:
            case PokepediaBerryFlavor.BITTER: return 4
            case PokepediaBerryFlavor.DRY: return 2
            case PokepediaBerryFlavor.SOUR: return 5
            case PokepediaBerryFlavor.SPICY: return 1
            case PokepediaBerryFlavor.SWEET: return 3
            case _: raise RuntimeError(f'unknown PokepediaBerryFlavor: \"{self}\"')

    def toStr(self) -> str:
        match self:
            case PokepediaBerryFlavor.BITTER: return 'Bitter'
            case PokepediaBerryFlavor.DRY: return 'Dry'
            case PokepediaBerryFlavor.SOUR: return 'Sour'
            case PokepediaBerryFlavor.SPICY: return 'Spicy'
            case PokepediaBerryFlavor.SWEET: return 'Sweet'
            case _: raise RuntimeError(f'unknown PokepediaBerryFlavor: \"{self}\"')
