from typing import Any

import CynanBot.misc.utils as utils


class LanguageEntry():

    def __init__(
        self,
        commandNames: list[str],
        name: str,
        flag: str | None = None,
        iso6391Code: str | None = None,
        wotdApiCode: str | None = None
    ):
        if not utils.areValidStrs(commandNames) or not isinstance(commandNames, list):
            raise ValueError(f'commandNames argument is malformed: \"{commandNames}\"')
        elif not utils.isValidStr(name):
            raise ValueError(f'name argument is malformed: \"{name}\"')
        elif flag is not None and not isinstance(flag, str):
            raise ValueError(f'flag argument is malformed: \"{flag}\"')
        elif iso6391Code is not None and not isinstance(iso6391Code, str):
            raise ValueError(f'iso6391Code argument is malformed: \"{iso6391Code}\"')
        elif wotdApiCode is not None and not isinstance(wotdApiCode, str):
            raise ValueError(f'wotdApiCode argument is malformed: \"{wotdApiCode}\"')

        self.__commandNames: list[str] = commandNames
        self.__name: str = name
        self.__flag: str | None = flag
        self.__iso6391Code: str | None = iso6391Code
        self.__wotdApiCode: str | None = wotdApiCode

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LanguageEntry):
            return False

        return self.__name.lower() == other.__name.lower()

    def getCommandNames(self) -> list[str]:
        return self.__commandNames

    def getFlag(self) -> str | None:
        return self.__flag

    def getIso6391Code(self) -> str | None:
        return self.__iso6391Code

    def getName(self) -> str:
        return self.__name

    def getPrimaryCommandName(self) -> str:
        return self.__commandNames[0]

    def getWotdApiCode(self) -> str | None:
        return self.__wotdApiCode

    def hasFlag(self) -> bool:
        return utils.isValidStr(self.__flag)

    def __hash__(self) -> int:
        return hash(self.__name.lower())

    def hasIso6391Code(self) -> bool:
        return utils.isValidStr(self.__iso6391Code)

    def hasWotdApiCode(self) -> bool:
        return utils.isValidStr(self.__wotdApiCode)

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireIso6391Code(self) -> str:
        iso6391Code = self.__iso6391Code

        if not utils.isValidStr(iso6391Code):
            raise RuntimeError(f'This LanguageEntry ({self}) has no ISO 639-1 code!')

        return iso6391Code

    def requireWotdApiCode(self) -> str:
        wotdApiCode = self.__wotdApiCode

        if not utils.isValidStr(wotdApiCode):
            raise RuntimeError(f'This LanguageEntry ({self}) has no WOTD API code!')

        return wotdApiCode

    def toDictionary(self) -> dict[str, Any]:
        return {
            'commandNames': self.__commandNames,
            'flag': self.__flag,
            'name': self.__name,
            'wotdApiCode': self.__wotdApiCode
        }
