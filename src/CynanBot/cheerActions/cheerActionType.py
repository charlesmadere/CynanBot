from enum import auto

from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr


class CheerActionType(EnumWithToFromStr):

    TIMEOUT = auto()
