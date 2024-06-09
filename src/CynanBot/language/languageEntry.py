from dataclasses import dataclass
from typing import Any

import CynanBot.misc.utils as utils


@dataclass(frozen = True)
class LanguageEntry():
    commandNames: list[str]
    name: str
    flag: str | None = None
    iso6391Code: str | None = None
    wotdApiCode: str | None = None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LanguageEntry):
            return False

        return self.name.casefold() == other.name.casefold()

    def __hash__(self) -> int:
        return hash(self.name.casefold())

    @property
    def primaryCommandName(self) -> str:
        return self.commandNames[0]

    def requireIso6391Code(self) -> str:
        if not utils.isValidStr(self.iso6391Code):
            raise RuntimeError(f'LanguageEntry has no iso6391Code value: ({self})')

        return self.iso6391Code

    def requireWotdApiCode(self) -> str:
        if not utils.isValidStr(self.wotdApiCode):
            raise RuntimeError(f'LanguageEntry has no wotdApiCode value: ({self})')

        return self.wotdApiCode
