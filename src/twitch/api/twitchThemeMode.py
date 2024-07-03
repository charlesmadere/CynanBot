from enum import auto

from ...misc.enumWithToFromStr import EnumWithToFromStr


class TwitchThemeMode(EnumWithToFromStr):

    DARK = auto()
    LIGHT = auto()
