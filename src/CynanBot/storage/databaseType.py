from enum import Enum, auto

import CynanBot.misc.utils as utils


class DatabaseType(Enum):

    POSTGRESQL = auto()
    SQLITE = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text in ('postgres', 'postgresql'):
            return DatabaseType.POSTGRESQL
        elif text == 'sqlite':
            return DatabaseType.SQLITE
        else:
            raise ValueError(f'unknown DatabaseType: \"{text}\"')
