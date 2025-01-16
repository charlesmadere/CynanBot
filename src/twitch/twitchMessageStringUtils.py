import re
from typing import Any, Pattern

from .twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ..misc import utils as utils


class TwitchMessageStringUtils(TwitchMessageStringUtilsInterface):

    def __init__(self):
        self.__userNameRegEx: Pattern = re.compile(r'^\s*@?(\w+)\s*$', re.IGNORECASE)
        self.__userNameWithCheerRegEx: Pattern = re.compile(r'^\s*(\w+\d+)\s+@?(\w+)\s*$', re.IGNORECASE)

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
