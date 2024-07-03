from enum import auto

from ..misc.enumWithToFromStr import EnumWithToFromStr


class PkmnCatchType(EnumWithToFromStr):

    GREAT = auto()
    NORMAL = auto()
    ULTRA = auto()
