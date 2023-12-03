from enum import auto

from typing_extensions import override

from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr

import CynanBot.misc.utils as utils


class DatabaseType(EnumWithToFromStr):

    POSTGRESQL = auto()
    SQLITE = auto()

    @override
    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'postgres':
            return DatabaseType.POSTGRESQL
        return super().fromStr(text)
