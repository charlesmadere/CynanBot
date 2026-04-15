import re
from typing import Any, Pattern, Final

from .googleTtsMessageCleanerInterface import GoogleTtsMessageCleanerInterface
from ..misc import utils as utils
from ..tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface


class GoogleTtsMessageCleaner(GoogleTtsMessageCleanerInterface):

    def __init__(
        self,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
    ):
        if not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__extraWhiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

    async def clean(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.cleanStr(message)
        message = self.__extraWhiteSpaceRegEx.sub(' ', message).strip()

        maximumMessageSize = await self.__ttsSettingsRepository.getMaximumMessageSize()
        if len(message) > maximumMessageSize:
            message = message[0:maximumMessageSize].strip()

        # this shouldn't be necessary but Python sux at type checking
        if not utils.isValidStr(message):
            return None

        return message
