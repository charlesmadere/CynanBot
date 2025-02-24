import re
from typing import Any, Collection, Pattern

from frozenlist import FrozenList

from .commodoreSamMessageCleanerInterface import CommodoreSamMessageCleanerInterface
from ..misc import utils as utils
from ..tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class CommodoreSamMessageCleaner(CommodoreSamMessageCleanerInterface):

    def __init__(
        self,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface
    ):
        if not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')

        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__twitchMessageStringUtils: TwitchMessageStringUtilsInterface = twitchMessageStringUtils

        self.__inputArgumentRegExes: Collection[Pattern] = self.__buildInputArgumentRegExes()
        self.__extraWhiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

    def __buildInputArgumentRegExes(self) -> FrozenList[Pattern]:
        inputArgumentRegExes: FrozenList[Pattern] = FrozenList()

        # purge pitch input arguments
        inputArgumentRegExes.append(re.compile(r'(?:^|\s+)-pitch(?:\s+(?:\d+)?)?', re.IGNORECASE))

        # purge speed input arguments
        inputArgumentRegExes.append(re.compile(r'(?:^|\s+)-speed(?:\s+(?:\d+)?)?', re.IGNORECASE))

        inputArgumentRegExes.freeze()
        return inputArgumentRegExes

    async def clean(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.cleanStr(message)
        message = await self.__twitchMessageStringUtils.removeCheerStrings(message)
        if not utils.isValidStr(message):
            return None

        message = await self.__purgeInputArguments(message)
        if not utils.isValidStr(message):
            return None

        # TODO more shenanigans need to be purged tbh

        message = self.__extraWhiteSpaceRegEx.sub(' ', message).strip()

        maximumMessageSize = await self.__ttsSettingsRepository.getMaximumMessageSize()
        if len(message) > maximumMessageSize:
            message = message[0:maximumMessageSize].strip()

        if not utils.isValidStr(message):
            return None

        return message

    async def __purgeInputArguments(self, message: str | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        repeat = True

        while repeat:
            repeat = False

            for inputArgumentRegEx in self.__inputArgumentRegExes:
                if inputArgumentRegEx.search(message) is None:
                    continue

                repeat = True
                message = inputArgumentRegEx.sub(' ', message).strip()

                if not utils.isValidStr(message):
                    return None

        if not utils.isValidStr(message):
            return None

        return message.strip()
