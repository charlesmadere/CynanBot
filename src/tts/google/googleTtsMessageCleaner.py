import re
from typing import Any, Pattern

from .googleTtsMessageCleanerInterface import GoogleTtsMessageCleanerInterface
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...misc import utils as utils


class GoogleTtsMessageCleaner(GoogleTtsMessageCleanerInterface):

    def __init__(
        self,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__extraWhiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

    async def clean(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.removeCheerStrings(message)
        if not utils.isValidStr(message):
            return None

        message = self.__extraWhiteSpaceRegEx.sub(' ', message).strip()

        if len(message) > await self.__ttsSettingsRepository.getMaximumMessageSize():
            message = message[0:await self.__ttsSettingsRepository.getMaximumMessageSize()].strip()

        return message
