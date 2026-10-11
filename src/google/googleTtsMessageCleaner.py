from typing import Any, Final

import emoji

from .googleTtsMessageCleanerInterface import GoogleTtsMessageCleanerInterface
from .settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ..misc import utils as utils
from ..tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface


class GoogleTtsMessageCleaner(GoogleTtsMessageCleanerInterface):

    def __init__(
        self,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
    ):
        if not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__googleSettingsRepository: Final[GoogleSettingsRepositoryInterface] = googleSettingsRepository
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

    async def clean(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.cleanStr(message)

        # this shouldn't be necessary but Python sux at type checking
        if not utils.isValidStr(message):
            return None

        maximumMessageSize = await self.__ttsSettingsRepository.getMaximumMessageSize()

        if len(message) > maximumMessageSize:
            message = message[0:maximumMessageSize].strip()

        # this shouldn't be necessary but Python sux at type checking
        if not utils.isValidStr(message):
            return None

        message = await self.__limitEmojiSequences(message)

        # this shouldn't be necessary but Python sux at type checking
        if not utils.isValidStr(message):
            return None

        return message

    async def __limitEmojiSequences(
        self,
        message: str | None,
    ) -> str | None:
        if not utils.isValidStr(message):
            return None

        emojisList = emoji.emoji_list(message)

        if emojisList is None or len(emojisList) == 0:
            return message

        maxConsecutiveEmojis = await self.__googleSettingsRepository.getMaxConsecutiveEmojis()

        result: list[str] = list()
        lastEnd = 0
        consecutiveCount = 0

        for e in emojisList:
            start = e['match_start']
            end = e['match_end']

            betweenText = message[lastEnd:start]

            if betweenText.strip():
                consecutiveCount = 0

            result.append(betweenText)

            consecutiveCount += 1
            if consecutiveCount <= maxConsecutiveEmojis:
                result.append(e['emoji'])

            lastEnd = end

        result.append(message[lastEnd:])
        return utils.cleanStr(''.join(result))
