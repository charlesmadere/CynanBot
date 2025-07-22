from typing import Final

from frozenlist import FrozenList

from .halfLifeTtsHelperInterface import HalfLifeTtsHelperInterface
from ..models.halfLifeSoundFile import HalfLifeSoundFile
from ..models.halfLifeVoice import HalfLifeVoice
from ..parser.halfLifeMessageVoiceParserInterface import HalfLifeMessageVoiceParserInterface
from ..service.halfLifeTtsServiceInterface import HalfLifeTtsServiceInterface
from ..settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...misc import utils as utils


class HalfLifeTtsHelper(HalfLifeTtsHelperInterface):

    def __init__(
        self,
        halfLifeMessageVoiceParser: HalfLifeMessageVoiceParserInterface,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface,
        halfLifeTtsService: HalfLifeTtsServiceInterface,
    ):
        if not isinstance(halfLifeMessageVoiceParser, HalfLifeMessageVoiceParserInterface):
            raise TypeError(f'halfLifeMessageVoiceParser argument is malformed: \"{halfLifeMessageVoiceParser}\"')
        elif not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')
        elif not isinstance(halfLifeTtsService, HalfLifeTtsServiceInterface):
            raise TypeError(f'halfLifeTtsService argument is malformed: \"{halfLifeTtsService}\"')

        self.__halfLifeMessageVoiceParser: Final[HalfLifeMessageVoiceParserInterface] = halfLifeMessageVoiceParser
        self.__halfLifeSettingsRepository: Final[HalfLifeSettingsRepositoryInterface] = halfLifeSettingsRepository
        self.__halfLifeTtsService: Final[HalfLifeTtsServiceInterface] = halfLifeTtsService

    async def generateTts(
        self,
        voice: HalfLifeVoice | None,
        message: str | None,
    ) -> FrozenList[HalfLifeSoundFile] | None:
        if voice is not None and not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        if voice is None:
            voice = await self.__halfLifeSettingsRepository.getDefaultVoice()

        messageVoiceResult = await self.__halfLifeMessageVoiceParser.determineVoiceFromMessage(message)

        if messageVoiceResult is not None:
            voice = messageVoiceResult.voice
            message = messageVoiceResult.message

        return await self.__halfLifeTtsService.findSoundFiles(
            voice = voice,
            message = message,
        )
