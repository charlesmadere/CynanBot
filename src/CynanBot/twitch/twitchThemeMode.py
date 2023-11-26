from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchThemeMode(Enum):

    DARK = auto()
    LIGHT = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'dark':
            return TwitchThemeMode.DARK
        elif text == 'light':
            return TwitchThemeMode.LIGHT
        else:
            raise ValueError(f'unknown TwitchThemeMode: \"{text}\"')
