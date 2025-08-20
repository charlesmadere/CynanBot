from typing import Any

from .microsoftSamMessageCleanerInterface import MicrosoftSamMessageCleanerInterface
from ..misc import utils as utils
from ..tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class MicrosoftSamMessageCleaner(MicrosoftSamMessageCleanerInterface):

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

    async def clean(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.cleanStr(message)
        message = await self.__twitchMessageStringUtils.removeCheerStrings(message)

        maximumMessageSize = await self.__ttsSettingsRepository.getMaximumMessageSize()
        if len(message) > maximumMessageSize:
            message = message[0:maximumMessageSize].strip()

        # this shouldn't be necessary but Python sux at type checking
        if not utils.isValidStr(message):
            return None

        return message
