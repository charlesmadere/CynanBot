import re
from typing import Any, Collection, Pattern

from frozenlist import FrozenList

from .commodoreSamMessageCleanerInterface import CommodoreSamMessageCleanerInterface
from ..misc import utils as utils
from ..tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class CommodoreSamMessageCleaner(CommodoreSamMessageCleanerInterface):

    def __init__(
        self,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
    ):
        if not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')

        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__twitchMessageStringUtils: TwitchMessageStringUtilsInterface = twitchMessageStringUtils

        self.__commodoreSamInputArgumentRegExes: Collection[Pattern] = self.__buildCommodoreSamInputArgumentRegExes()
        self.__terminalExploitRegExes: Collection[Pattern] = self.__buildTerminalExploitRegExes()

    def __buildCommodoreSamInputArgumentRegExes(self) -> FrozenList[Pattern]:
        regExes: FrozenList[Pattern] = FrozenList()

        # purge mouth input argument(s)
        regExes.append(re.compile(r'(?:^|\s+)-mouth(?:\s+(?:\d+)?)?', re.IGNORECASE))

        # purge pitch input argument(s)
        regExes.append(re.compile(r'(?:^|\s+)-pitch(?:\s+(?:\d+)?)?', re.IGNORECASE))

        # purge speed input argument(s)
        regExes.append(re.compile(r'(?:^|\s+)-speed(?:\s+(?:\d+)?)?', re.IGNORECASE))

        # purge throat input argument(s)
        regExes.append(re.compile(r'(?:^|\s+)-throat(?:\s+(?:\d+)?)?', re.IGNORECASE))

        regExes.freeze()
        return regExes

    def __buildTerminalExploitRegExes(self) -> FrozenList[Pattern]:
        regExes: FrozenList[Pattern] = FrozenList()

        # purge potentially dangerous/tricky characters
        regExes.append(re.compile(r'[\[\]<>&%;=\"|^~`\\]', re.IGNORECASE))

        # purge what might be directory traversal sequences
        regExes.append(re.compile(r'\.{2}', re.IGNORECASE))

        regExes.freeze()
        return regExes

    async def clean(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.cleanStr(message)
        message = await self.__twitchMessageStringUtils.removeCheerStrings(message)
        if not utils.isValidStr(message):
            return None

        message = await self.__purge(self.__commodoreSamInputArgumentRegExes, message)
        if not utils.isValidStr(message):
            return None

        message = await self.__purge(self.__terminalExploitRegExes, message)
        if not utils.isValidStr(message):
            return None

        message = utils.cleanStr(message)

        maximumMessageSize = await self.__ttsSettingsRepository.getMaximumMessageSize()
        if len(message) > maximumMessageSize:
            message = message[0:maximumMessageSize].strip()

        if not utils.isValidStr(message):
            return None

        return message

    async def __purge(
        self,
        regExes: Collection[Pattern],
        message: str | None
    ) -> str | None:
        if not utils.isValidStr(message):
            return None

        repeat = True

        while repeat:
            repeat = False

            for regEx in regExes:
                if regEx.search(message) is None:
                    continue

                repeat = True
                message = regEx.sub(' ', message).strip()

                if not utils.isValidStr(message):
                    return None

        if not utils.isValidStr(message):
            return None

        return message.strip()
