from typing import Any

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

    async def clean(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.cleanStr(message)
        message = await self.__twitchMessageStringUtils.removeCheerStrings(message)
        if not utils.isValidStr(message):
            return None

        # TODO
        return message
