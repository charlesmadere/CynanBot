from enum import auto

from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr


class CheerActionType(EnumWithToFromStr):

    SOUND_ALERT = auto()
    TIMEOUT = auto()
