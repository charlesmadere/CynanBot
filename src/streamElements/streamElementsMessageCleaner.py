import re
from typing import Any, Pattern

from .streamElementsMessageCleanerInterface import StreamElementsMessageCleanerInterface
from ..misc import utils as utils
from ..tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface


class StreamElementsMessageCleaner(StreamElementsMessageCleanerInterface):

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

        message = utils.removeCheerStrings(message.strip()).strip()
        message = self.__extraWhiteSpaceRegEx.sub(' ', message.strip()).strip()
        message = utils.replaceAmpersand(message)

        maximumMessageSize = await self.__ttsSettingsRepository.getMaximumMessageSize()
        if len(message) > maximumMessageSize:
            message = message[0:maximumMessageSize].strip()

        return message
