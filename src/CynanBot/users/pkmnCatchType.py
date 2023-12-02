from enum import auto

from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr


class PkmnCatchType(EnumWithToFromStr):

    GREAT = auto()
    NORMAL = auto()
    ULTRA = auto()

    def getSortOrder(self) -> int:
        if self is PkmnCatchType.GREAT:
            return 1
        elif self is PkmnCatchType.NORMAL:
            return 0
        elif self is PkmnCatchType.ULTRA:
            return 2
        else:
            raise RuntimeError(f'unknown PkmnCatchType: \"{self}\"')
