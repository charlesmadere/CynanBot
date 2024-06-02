from __future__ import annotations

from enum import auto

from typing_extensions import override

import CynanBot.misc.utils as utils
from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr


class DatabaseType(EnumWithToFromStr):

    POSTGRESQL = auto()
    SQLITE = auto()

    @override
    @classmethod
    def fromStr(cls, text: str) -> DatabaseType:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        match text:
            case 'postgres': return DatabaseType.POSTGRESQL
            case _: return super().fromStr(text)
