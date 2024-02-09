from enum import auto

from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr


class CheerActionBitRequirement(EnumWithToFromStr):

    EXACT = auto()
    GREATER_THAN_OR_EQUAL_TO = auto()
