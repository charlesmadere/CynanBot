from enum import Enum, auto


class PokepediaDamageMultiplier(Enum):

    ZERO = auto()
    ZERO_POINT_TWO_FIVE = auto()
    ZERO_POINT_FIVE = auto()
    ONE = auto()
    TWO = auto()
    FOUR = auto()

    def getEffectDescription(self) -> str:
        if self is PokepediaDamageMultiplier.ZERO:
            return 'damage from'
        elif self is PokepediaDamageMultiplier.ZERO_POINT_TWO_FIVE or self is PokepediaDamageMultiplier.ZERO_POINT_FIVE:
            return 'resistant to'
        elif self is PokepediaDamageMultiplier.ONE:
            raise RuntimeError(f'{self} should not be used with this method!')
        elif self is PokepediaDamageMultiplier.TWO or self is PokepediaDamageMultiplier.FOUR:
            return 'weak to'
        else:
            raise RuntimeError(f'unknown PokepediaDamageMultiplier: \"{self}\"')

    def toStr(self) -> str:
        match self:
            case PokepediaDamageMultiplier.ZERO: return '0x'
            case PokepediaDamageMultiplier.ZERO_POINT_TWO_FIVE: return '0.25x'
            case PokepediaDamageMultiplier.ZERO_POINT_FIVE: return '0.5x'
            case PokepediaDamageMultiplier.ONE: return '1x'
            case PokepediaDamageMultiplier.TWO: return '2x'
            case PokepediaDamageMultiplier.FOUR: return '4x'
            case _: raise RuntimeError(f'unknown PokepediaDamageMultiplier: \"{self}\"')
