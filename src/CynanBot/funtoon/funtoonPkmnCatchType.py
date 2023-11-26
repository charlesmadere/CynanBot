from enum import Enum, auto


class FuntoonPkmnCatchType(Enum):

    GREAT = auto()
    NORMAL = auto()
    ULTRA = auto()

    def toStr(self) -> str:
        if self is FuntoonPkmnCatchType.GREAT:
            return 'great'
        elif self is FuntoonPkmnCatchType.NORMAL:
            return 'normal'
        elif self is FuntoonPkmnCatchType.ULTRA:
            return 'ultra'
        else:
            raise RuntimeError(f'unknown FuntoonPkmnCatchType: \"{self}\"')
