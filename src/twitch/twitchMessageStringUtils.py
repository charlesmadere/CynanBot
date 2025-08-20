import re
from typing import Any, Final, Pattern

from frozenlist import FrozenList

from .twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ..misc import utils as utils


class TwitchMessageStringUtils(TwitchMessageStringUtilsInterface):

    def __init__(self):
        self.__extraWhiteSpaceRegEx: Final[Pattern] = re.compile(r'\s{2,}', re.IGNORECASE)
        self.__userNameRegEx: Final[Pattern] = re.compile(r'^\s*@?(\w+)\s*$', re.IGNORECASE)
        self.__userNameWithCheerRegEx: Final[Pattern] = re.compile(r'^\s*(\w+\d+)\s+@?(\w+)\s*$', re.IGNORECASE)

        self.__cheerRegExes: Final[FrozenList[Pattern]] = FrozenList([
            re.compile(r'(^|\s+)bitboss\d+', re.IGNORECASE),
            re.compile(r'(^|\s+)cheer\d+', re.IGNORECASE),
            re.compile(r'(^|\s+)doodlecheer\d+', re.IGNORECASE),
            re.compile(r'(^|\s+)muxy\d+', re.IGNORECASE),
            re.compile(r'(^|\s+)streamlabs\d+', re.IGNORECASE),
            re.compile(r'(^|\s+)uni\d+', re.IGNORECASE)
        ])
        self.__cheerRegExes.freeze()

    async def getUserNameFromMessage(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        userNameMatch = self.__userNameRegEx.fullmatch(message)

        if userNameMatch is None:
            return None

        userName: str | None = userNameMatch.group(1)

        if utils.isValidStr(userName):
            return userName
        else:
            return None

    async def getUserNameFromCheerMessage(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        userNameMatch = self.__userNameWithCheerRegEx.fullmatch(message)

        if userNameMatch is None:
            return None

        userName: str | None = userNameMatch.group(2)

        if utils.isValidStr(userName):
            return userName
        else:
            return None

    async def removeCheerStrings(self, message: str, repl: str = ' ') -> str:
        if not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(repl, str):
            raise TypeError(f'repl argument is malformed: \"{repl}\"')

        for cheerRegEx in self.__cheerRegExes:
            message = cheerRegEx.sub(repl, message)

        return utils.cleanStr(message)
